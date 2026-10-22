// eth_wifi_bridge: the bell's Ethernet and its Wi-Fi access point as one layer-2 network (see __init__.py).
//
// ACCESS HACK, on purpose and only here: ESPHome's EthernetComponent is `final` and keeps its esp_netif pointer
// protected. ESPHome uses that pointer for DHCP (start_connect_), the reported address and the default route, so after
// building the bridge it has to point at br0. Making `protected` public for this one include changes no layout.
#define protected public
#include "esphome/components/ethernet/ethernet_component.h"
#undef protected

#include "eth_wifi_bridge.h"

#include <cstdlib>
#include <cstring>
#include <freertos/FreeRTOS.h>
#include <freertos/task.h>
#include <esp_eth.h>
#include <esp_netif_net_stack.h>
#include <esp_ota_ops.h>
#include <esp_wifi.h>
#include <lwip/sockets.h>
#include "esphome/core/application.h"
#include "esphome/core/hal.h"
#include "esphome/core/log.h"
#ifdef USE_MDNS
#include <mdns.h>
#endif

namespace esphome::eth_wifi_bridge {

static const char *const TAG = "eth_wifi_bridge";

void EthWifiBridge::setup() {
  esp_event_handler_register(WIFI_EVENT, WIFI_EVENT_AP_STACONNECTED, &EthWifiBridge::wifi_event_, this);
  esp_event_handler_register(WIFI_EVENT, WIFI_EVENT_AP_STADISCONNECTED, &EthWifiBridge::wifi_event_, this);
}

// event task: only store; loop() logs
void EthWifiBridge::wifi_event_(void *arg, esp_event_base_t base, int32_t id, void *data) {
  auto *self = static_cast<EthWifiBridge *>(arg);
  if (id == WIFI_EVENT_AP_STACONNECTED) {
    auto *e = static_cast<wifi_event_ap_staconnected_t *>(data);
    for (int i = 0; i < 6; i++)
      self->last_mac_[i] = e->mac[i];
    self->sta_joins_ = self->sta_joins_ + 1;
  } else if (id == WIFI_EVENT_AP_STADISCONNECTED) {
    auto *e = static_cast<wifi_event_ap_stadisconnected_t *>(data);
    for (int i = 0; i < 6; i++)
      self->last_mac_[i] = e->mac[i];
    self->last_leave_reason_ = e->reason;
    self->sta_leaves_ = self->sta_leaves_ + 1;
  }
}

void EthWifiBridge::loop() {
  const uint32_t now = millis();
  if (!this->built_) {
    if (now - this->last_try_ < 500)
      return;
    this->last_try_ = now;
    this->built_ = this->build_();
    return;
  }
  // Safety net, first boot after an OTA only: no address on br0 within 40 s = reboot before ESPHome marks this firmware
  // good (after 1 min), so the bootloader rolls back to the previous firmware by itself. Never in normal operation.
  if (this->pending_verify_) {
    esp_netif_ip_info_t ip{};
    const bool has_ip = esp_netif_get_ip_info(this->br_, &ip) == ESP_OK && ip.ip.addr != 0;
    if (has_ip) {
      this->pending_verify_ = false;
      ESP_LOGI(TAG, "br0 got " IPSTR ": the bridge works", IP2STR(&ip.ip));
    } else if (now - this->built_ms_ > 40000) {
      ESP_LOGE(TAG, "br0 has no address after 40 s: rebooting, the previous firmware comes back");
      App.reboot();  // NOT safe_reboot(): that marks the running image good and clears the boot-loop counter (aikos H4)
    }
  }
  // br0 exists in lwIP once Ethernet has started again (the glue starts it on the Ethernet start event)
  if (!this->ap_added_ && esp_netif_get_netif_impl(this->br_) != nullptr)
    this->add_ap_port_();
#ifdef USE_MDNS
  if (!this->mdns_added_) {
    esp_netif_ip_info_t ip{};
    if (esp_netif_get_ip_info(this->br_, &ip) == ESP_OK && ip.ip.addr != 0) {
      // mDNS knows the predefined interfaces (ETH_DEF, WIFI_AP_DEF) only; the bell's address now lives on br0
      if (mdns_register_netif(this->br_) == ESP_OK)
        mdns_netif_action(this->br_, static_cast<mdns_event_actions_t>(MDNS_EVENT_ENABLE_IP4 | MDNS_EVENT_ANNOUNCE_IP4));
      this->mdns_added_ = true;
    }
  }
#else
  this->mdns_added_ = true;
#endif
  this->guard_tcp_(now);
  if (now - this->last_status_ >= 15000) {  // bench diagnostics
    this->last_status_ = now;
    esp_netif_ip_info_t ip{};
    esp_netif_get_ip_info(this->br_, &ip);
    wifi_sta_list_t list{};
    esp_wifi_ap_get_sta_list(&list);
    ESP_LOGI(TAG, "promiscuous %s, all multicast OFF %s", esp_err_to_name(this->promisc_result_),
             esp_err_to_name(this->mcast_result_));
    ESP_LOGI(TAG, "br0 " IPSTR ", ap port %s (%s), stations now %d, joins %u, leaves %u, last %02x:%02x:%02x:%02x:%02x:%02x reason %u",
             IP2STR(&ip.ip), this->ap_added_ ? "added" : "not added", esp_err_to_name(this->ap_add_result_), list.num,
             (unsigned) this->sta_joins_, (unsigned) this->sta_leaves_, this->last_mac_[0], this->last_mac_[1],
             this->last_mac_[2], this->last_mac_[3], this->last_mac_[4], this->last_mac_[5],
             (unsigned) this->last_leave_reason_);
    this->log_cpu_();
  }
}

void EthWifiBridge::guard_tcp_(uint32_t now) {
  static constexpr uint32_t EVERY_MS = 60000, TIMEOUT_MS = 5000;
  static constexpr uint8_t FAILURES_TO_REBOOT = 3;
  if (this->tcp_fd_ < 0) {
    if (static_cast<int32_t>(now - this->tcp_next_) < 0)
      return;
    this->tcp_next_ = now + EVERY_MS;
    auto *eth = ethernet::global_eth_component;
    esp_netif_ip_info_t ip{};
    if (eth == nullptr || !eth->is_connected() || esp_netif_get_ip_info(this->br_, &ip) != ESP_OK || ip.ip.addr == 0) {
      this->tcp_failures_ = 0;  // no link or no address: nothing to judge (and nothing a reboot would fix)
      return;
    }
    struct sockaddr_in to {};
    to.sin_family = AF_INET;
    to.sin_port = htons(443);
    to.sin_addr.s_addr = this->tcp_guard_host_ != nullptr ? inet_addr(this->tcp_guard_host_) : ip.gw.addr;
    int fd = lwip_socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (fd < 0) {
      this->tcp_failures_++;  // no socket at all is a failure of the stack too
    } else {
      lwip_fcntl(fd, F_SETFL, O_NONBLOCK);
      int r = lwip_connect(fd, reinterpret_cast<struct sockaddr *>(&to), sizeof(to));
      if (r == 0 || errno == EINPROGRESS) {
        this->tcp_fd_ = fd;
        this->tcp_started_ = now;
        return;
      }
      lwip_close(fd);
      if (errno == ECONNREFUSED)
        this->tcp_failures_ = 0;
      else
        this->tcp_failures_++;
    }
  } else {
    fd_set wr;
    FD_ZERO(&wr);
    FD_SET(this->tcp_fd_, &wr);
    struct timeval zero {};
    const int ready = lwip_select(this->tcp_fd_ + 1, nullptr, &wr, nullptr, &zero);
    bool done = false, alive = false;
    if (ready > 0) {
      int err = 0;
      socklen_t len = sizeof(err);
      lwip_getsockopt(this->tcp_fd_, SOL_SOCKET, SO_ERROR, &err, &len);
      done = true;
      alive = err == 0 || err == ECONNREFUSED || err == ECONNRESET;
    } else if (now - this->tcp_started_ > TIMEOUT_MS) {
      done = true;
    }
    if (!done)
      return;
    lwip_close(this->tcp_fd_);
    this->tcp_fd_ = -1;
    if (alive) {
      this->tcp_failures_ = 0;
      this->tcp_ok_ms_ = now == 0 ? 1 : now;
    } else {
      this->tcp_failures_++;
      ESP_LOGW(TAG, "TCP guard: no TCP answer from the gateway (%u in a row)", (unsigned) this->tcp_failures_);
    }
  }
  // H4 stage 2: confirm this firmware once it has been healthy for 2 min (only once per boot)
  esp_netif_ip_info_t hip{};
  const bool healthy = this->tcp_ok_ms_ != 0 && now - this->tcp_ok_ms_ < 90000 &&
                       esp_netif_get_ip_info(this->br_, &hip) == ESP_OK && hip.ip.addr != 0;
  if (!healthy) {
    this->healthy_since_ = 0;
  } else if (this->healthy_since_ == 0) {
    this->healthy_since_ = now == 0 ? 1 : now;
  } else if (!this->confirmed_ && now - this->healthy_since_ >= 120000 && this->safe_mode_ != nullptr) {
    this->confirmed_ = true;
    ESP_LOGI(TAG, "healthy for 2 min (br0 address + TCP ok): firmware confirmed, boot counter cleared");
    this->safe_mode_->mark_successful();
  }
  if (this->tcp_failures_ >= FAILURES_TO_REBOOT) {
    ESP_LOGE(TAG, "TCP guard: the TCP stack is dead (%u failures in a row), rebooting", (unsigned) this->tcp_failures_);
    App.reboot();  // NOT safe_reboot(): that marks the running image good and clears the boot-loop counter (aikos H4)
  }
}

// Bench diagnosis (2026-10-03): the bridged bell rebooted by task watchdog with the W5500 receive task running on core 1
// (promiscuous mode hands it every frame of the LAN). Logs the share of one core each task used since the last call.
void EthWifiBridge::log_cpu_() {
#if defined(CONFIG_FREERTOS_USE_TRACE_FACILITY) && defined(CONFIG_FREERTOS_GENERATE_RUN_TIME_STATS)
  static const char *const NAMES[6] = {"w5500_tsk", "tiT", "loopTask", "wifi", "IDLE0", "IDLE1"};
  UBaseType_t count = uxTaskGetNumberOfTasks() + 4;
  auto *st = static_cast<TaskStatus_t *>(malloc(count * sizeof(TaskStatus_t)));
  if (st == nullptr)
    return;
  configRUN_TIME_COUNTER_TYPE total = 0;
  count = uxTaskGetSystemState(st, count, &total);
  uint64_t now[6]{};
  for (UBaseType_t i = 0; i < count; i++) {
    for (int k = 0; k < 6; k++) {
      if (strcmp(st[i].pcTaskName, NAMES[k]) == 0)
        now[k] = st[i].ulRunTimeCounter;
    }
  }
  free(st);
  // 32-bit microsecond counters wrap every ~72 min: unsigned 32-bit differences stay right across one wrap
  const uint32_t dt = (uint32_t) total - (uint32_t) this->cpu_total_;
  if (this->cpu_total_ != 0 && dt > 0) {
    char buf[160];
    int pos = 0;
    for (int k = 0; k < 6 && pos < (int) sizeof(buf); k++)
      pos += snprintf(buf + pos, sizeof(buf) - pos, "%s %u%%  ", NAMES[k], (unsigned) ((uint64_t) (uint32_t) (now[k] - this->cpu_prev_[k]) * 100 / dt));
    ESP_LOGI(TAG, "cpu (share of one core): %s", buf);
  }
  this->cpu_total_ = total;
  for (int k = 0; k < 6; k++)
    this->cpu_prev_[k] = now[k];
#endif
}

bool EthWifiBridge::build_() {
  auto *eth = ethernet::global_eth_component;
  if (eth == nullptr) {
    ESP_LOGE(TAG, "no Ethernet component");
    this->mark_failed();
    return true;
  }
  this->eth_port_ = eth->get_esp_netif();
  this->ap_port_ = esp_netif_get_handle_from_ifkey("WIFI_AP_DEF");
  if (this->eth_port_ == nullptr || this->ap_port_ == nullptr) {
    ESP_LOGD(TAG, "waiting for Ethernet and the access point");
    return false;
  }
  esp_ota_img_states_t state;
  const esp_partition_t *running = esp_ota_get_running_partition();
  this->pending_verify_ = running != nullptr && esp_ota_get_state_partition(running, &state) == ESP_OK &&
                          state == ESP_OTA_IMG_PENDING_VERIFY;
  this->built_ms_ = millis();

  esp_eth_handle_t eth_handle = eth->get_eth_handle();
  uint8_t mac[6];
  if (esp_eth_ioctl(eth_handle, ETH_CMD_G_MAC_ADDR, mac) != ESP_OK) {
    ESP_LOGE(TAG, "could not read the Ethernet MAC");
    this->mark_failed();
    return true;
  }

  // Stop Ethernet: on the next start event the glue adds the Ethernet port and starts br0, and ESPHome runs DHCP again,
  // then on br0. The ports themselves carry no address (bridge ports are pure layer 2).
  esp_eth_stop(eth_handle);
  esp_netif_dhcpc_stop(this->eth_port_);
  esp_netif_dhcps_stop(this->ap_port_);
  esp_netif_ip_info_t zero{};
  esp_netif_set_ip_info(this->eth_port_, &zero);
  esp_netif_set_ip_info(this->ap_port_, &zero);

  static bridgeif_config_t bridge_cfg;  // must outlive br0
  // 128, not 16: on the house LAN 16 fill within seconds, and every peer not in the table (e.g. a new API client) gets
  // each reply flooded to both ports (core dump 03.10. 18:41: tiT stuck sending a flooded TCP ACK)
  bridge_cfg.max_fdb_dyn_entries = 128;
  bridge_cfg.max_fdb_sta_entries = 2;
  bridge_cfg.max_ports = 2;
  esp_netif_inherent_config_t base = ESP_NETIF_INHERENT_DEFAULT_BR();  // DHCP client, IP_EVENT_ETH_GOT_IP like Ethernet
  memcpy(base.mac, mac, sizeof(mac));  // the bell keeps its Ethernet MAC, so its DHCP reservation still applies
  base.bridge_info = &bridge_cfg;
  base.route_prio = 100;
  esp_netif_config_t cfg{};
  cfg.base = &base;
  cfg.stack = ESP_NETIF_NETSTACK_DEFAULT_BR;
  this->br_ = esp_netif_new(&cfg);
  if (this->br_ == nullptr) {
    ESP_LOGE(TAG, "could not create br0");
    esp_eth_start(eth_handle);
    this->mark_failed();
    return true;
  }
  this->glue_ = esp_netif_br_glue_new();
  esp_err_t err = esp_netif_br_glue_add_port(this->glue_, this->eth_port_);
  if (err == ESP_OK)
    err = esp_netif_br_glue_add_wifi_port(this->glue_, this->ap_port_);
  if (err == ESP_OK)
    err = esp_netif_attach(this->br_, this->glue_);
  if (err != ESP_OK) {
    ESP_LOGE(TAG, "bridge setup failed: %s", esp_err_to_name(err));
    esp_eth_start(eth_handle);
    this->mark_failed();
    return true;
  }

  eth->eth_netif_ = this->br_;  // ESPHome's DHCP, reported address and default route now use br0
  // The W5500 normally drops frames for other MACs and all multicast. The bridge forwards for the devices on the access
  // point, so it must see their unicast (e.g. the DHCP offer to a phone) and multicast (mDNS) too (as in the IDF example).
  bool on = true;
  this->promisc_result_ = esp_eth_ioctl(eth_handle, ETH_CMD_S_PROMISCUOUS, &on);
  // all-multicast OFF (the W5500 then blocks IPv4 multicast): the LAN's mDNS/SSDP/streaming multicast no longer reaches the
  // receive task over SPI. Screen and talk computer need none of it (fixed addresses; broadcast and unicast still pass).
  bool off = false;
  this->mcast_result_ = esp_eth_ioctl(eth_handle, ETH_CMD_S_ALL_MULTICAST, &off);
  err = esp_eth_start(eth_handle);
  ESP_LOGI(TAG, "bridge br0 built (Ethernet + access point), MAC %02x:%02x:%02x:%02x:%02x:%02x, Ethernet restart: %s",
           mac[0], mac[1], mac[2], mac[3], mac[4], mac[5], esp_err_to_name(err));
  return true;
}

void EthWifiBridge::add_ap_port_() {
  esp_err_t err = esp_netif_bridge_add_port(this->br_, this->ap_port_);
  this->ap_add_result_ = err;
  ESP_LOGI(TAG, "access point added to br0: %s", esp_err_to_name(err));
  this->ap_added_ = true;  // also on error: no retry storm; the glue adds it again on the next access point start
}

void EthWifiBridge::dump_config() {
  ESP_LOGCONFIG(TAG, "Ethernet + Wi-Fi bridge (br0): %s, access point port %s, rollback guard %s",
                this->built_ ? "built" : "waiting", this->ap_added_ ? "added" : "pending",
                this->pending_verify_ ? "armed" : "off");
  if (this->br_ != nullptr) {
    esp_netif_ip_info_t ip{};
    if (esp_netif_get_ip_info(this->br_, &ip) == ESP_OK)
      ESP_LOGCONFIG(TAG, "  br0 address: " IPSTR, IP2STR(&ip.ip));
  }
}

}  // namespace esphome::eth_wifi_bridge
