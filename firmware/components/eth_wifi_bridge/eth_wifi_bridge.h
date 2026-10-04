// eth_wifi_bridge: the bell's Ethernet and its Wi-Fi access point as one layer-2 network (see __init__.py).
#pragma once

#include "esphome/components/safe_mode/safe_mode.h"
#include "esphome/core/component.h"
#include <esp_netif.h>
#include <esp_netif_br_glue.h>

namespace esphome::eth_wifi_bridge {

class EthWifiBridge : public Component {
 public:
  // after Ethernet and Wi-Fi have created their interfaces; the work itself waits in loop() until both exist
  float get_setup_priority() const override { return setup_priority::AFTER_WIFI; }
  void setup() override;
  void loop() override;
  void dump_config() override;
  void set_tcp_guard_host(const char *host) { this->tcp_guard_host_ = host; }
  void set_safe_mode(safe_mode::SafeModeComponent *sm) { this->safe_mode_ = sm; }

 protected:
  bool build_();         // stop Ethernet, make br0, add both ports, hand br0 to ESPHome, start Ethernet again
  void add_ap_port_();   // the access point is already running, so its start event (which adds it) has passed
  void log_cpu_();       // bench diagnosis: CPU share of the tasks that matter, since the last call
  // TCP guard (aikos H4, 03.10.): a bell whose TCP stack is dead still answers ping (bell 0.3.10, 13:03) and ESPHome's loop
  // keeps feeding the watchdog. Every minute: non-blocking TCP connect to the gateway (port 443); a refusal counts as alive
  // (the stack answered). 3 failures in a row while the Ethernet link is up -> reboot. Home Assistant is not involved.
  void guard_tcp_(uint32_t now);
  const char *tcp_guard_host_{nullptr};
  int tcp_fd_{-1};
  uint32_t tcp_started_{0};
  uint32_t tcp_next_{0};
  uint8_t tcp_failures_{0};
  // H4 stage 2: healthy = address on br0 and a TCP answer within 90 s; 2 min of that confirms the firmware
  safe_mode::SafeModeComponent *safe_mode_{nullptr};
  uint32_t tcp_ok_ms_{0};
  uint32_t healthy_since_{0};
  bool confirmed_{false};

  esp_netif_t *br_{nullptr};
  esp_netif_t *eth_port_{nullptr};
  esp_netif_t *ap_port_{nullptr};
  esp_netif_br_glue_handle_t glue_{nullptr};
  bool built_{false};
  bool ap_added_{false};
  bool mdns_added_{false};
  uint32_t last_try_{0};
  uint32_t built_ms_{0};
  bool pending_verify_{false};  // first boot after an OTA: a reboot now rolls back to the previous firmware
  // diagnostics (bench): what the access point sees, logged every 15 s at INFO
  static void wifi_event_(void *arg, esp_event_base_t base, int32_t id, void *data);
  esp_err_t ap_add_result_{ESP_FAIL};
  esp_err_t promisc_result_{ESP_FAIL}, mcast_result_{ESP_FAIL};
  uint32_t last_status_{0};
  volatile uint32_t sta_joins_{0}, sta_leaves_{0};
  volatile uint8_t last_mac_[6]{};
  volatile uint16_t last_leave_reason_{0};
  uint64_t cpu_total_{0};
  uint64_t cpu_prev_[6]{};
};

}  // namespace esphome::eth_wifi_bridge
