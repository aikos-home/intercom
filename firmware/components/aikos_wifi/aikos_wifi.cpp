// aikos_wifi: prefer the bell's Wi-Fi "aikos", fall back to the house Wi-Fi, come back by itself (see __init__.py).
#include "aikos_wifi.h"

#include <algorithm>
#include <cstring>
#include <esp_wifi.h>
#include <lwip/ip_addr.h>
#include "esphome/components/wifi/wifi_component.h"
#include "esphome/core/application.h"
#include "esphome/core/hal.h"
#include "esphome/core/log.h"

namespace esphome::aikos_wifi {

static const char *const TAG = "aikos_wifi";

static constexpr int8_t AIKOS_PRIORITY = 1;          // the house Wi-Fi has 0: a scan that sees both takes "aikos"
static constexpr uint32_t SETTLE_MS = 60000;         // on the house Wi-Fi this long before the first probe
static constexpr uint32_t PROBE_EVERY_MS = 60000;    // bell silent: ask again in a minute
static constexpr uint32_t BACKOFF_MIN_MS = 300000;   // a switch ended back on the house Wi-Fi: 5 min, 10, 20, 40, 60
static constexpr uint32_t BACKOFF_MAX_MS = 3600000;

static constexpr uint32_t GUARD_EVERY_MS = 60000;   // network guard: ping the gateway every minute while connected
static constexpr uint32_t GUARD_DEAD_MS = 300000;   // ... no reply for 5 min = stuck -> reboot

static bool reached(uint32_t now, uint32_t when) { return static_cast<int32_t>(now - when) >= 0; }

void AikosWifi::setup() {
  auto *wifi = wifi::global_wifi_component;
  this->backoff_ = BACKOFF_MIN_MS;
  this->alive_ms_ = millis();
  this->guard_next_ = millis();
  if (!wifi->has_sta()) {
    // nothing entered via Improv yet: ESPHome runs its setup access point; that path stays untouched
    ESP_LOGW(TAG, "no house Wi-Fi entered yet (Improv): '%s' not added", this->ssid_);
    return;
  }
  // WiFiComponent::start() loaded the Improv-entered house Wi-Fi from flash and selected it
  wifi::WiFiAP house = wifi->get_sta();
  wifi::WiFiAP aikos;
  aikos.set_ssid(this->ssid_);
  aikos.set_password(this->password_);
  aikos.set_priority(AIKOS_PRIORITY);
  wifi->clear_sta();
  wifi->init_sta(2);
  wifi->add_sta(aikos);
  wifi->add_sta(house);
  this->active_ = true;
  ESP_LOGI(TAG, "'%s' first, the house Wi-Fi as fallback", this->ssid_);
}

void AikosWifi::loop() {
  const uint32_t now = millis();
  this->guard_network_(now);
  if (!this->active_)
    return;
  auto *wifi = wifi::global_wifi_component;

  if (this->probe_done_.load()) {
    this->probe_done_ = false;
    this->probing_ = false;
    const uint32_t replies = this->probe_replies_.load();
    if (replies > 0 && this->on_other_ && wifi->is_connected()) {
      this->switch_to_aikos_(now);
    } else {
      this->next_probe_ = now + PROBE_EVERY_MS;
    }
  }

  if (!wifi->is_connected()) {
    this->on_aikos_ = false;
    this->on_other_ = false;
    return;
  }
  char ssid[wifi::SSID_BUFFER_SIZE];
  const char *current = wifi->wifi_ssid_to(ssid);
  if (current[0] == 0)  // just disconnected, ESPHome's connected flag not refreshed yet: neither network
    return;
  if (std::strcmp(current, this->ssid_) == 0) {
    if (!this->on_aikos_)
      ESP_LOGI(TAG, "on '%s'", this->ssid_);
    this->on_aikos_ = true;
    this->on_other_ = false;
    this->after_switch_ = false;
    this->backoff_ = BACKOFF_MIN_MS;
    return;
  }
  if (!this->on_other_) {
    // just connected to the house Wi-Fi: give it a minute before asking for the bell; after a failed switch the backoff
    // set in switch_to_aikos_() applies instead
    this->on_other_ = true;
    this->on_aikos_ = false;
    if (!this->after_switch_)
      this->next_probe_ = now + SETTLE_MS;
    this->after_switch_ = false;
    ESP_LOGI(TAG, "on the house Wi-Fi; back to '%s' once the bell (%s) answers", this->ssid_, this->bell_);
  }
  if (this->probing_ || wifi->is_roaming() || !reached(now, this->next_probe_))
    return;
  this->start_probe_(now);
}

void AikosWifi::start_probe_(uint32_t now) {
  esp_ping_config_t cfg = ESP_PING_DEFAULT_CONFIG();
  if (ipaddr_aton(this->bell_, &cfg.target_addr) == 0) {
    ESP_LOGE(TAG, "bell address '%s' unreadable", this->bell_);
    this->mark_failed();
    return;
  }
  cfg.count = 2;
  cfg.interval_ms = 500;
  cfg.timeout_ms = 1000;
  esp_ping_callbacks_t cbs{};
  cbs.cb_args = this;
  cbs.on_ping_success = &AikosWifi::on_ping_success_;
  cbs.on_ping_end = &AikosWifi::on_ping_end_;
  esp_ping_handle_t hdl = nullptr;
  this->probe_replies_ = 0;
  this->probe_done_ = false;
  if (esp_ping_new_session(&cfg, &cbs, &hdl) != ESP_OK) {
    this->next_probe_ = now + PROBE_EVERY_MS;
    return;
  }
  this->probing_ = true;
  esp_ping_start(hdl);
}

// ping task
void AikosWifi::on_ping_success_(esp_ping_handle_t hdl, void *args) {
  auto *self = static_cast<AikosWifi *>(args);
  self->probe_replies_.fetch_add(1);
}

// ping task, after the last reply or timeout: deleting here only flags the task, which then frees itself
void AikosWifi::on_ping_end_(esp_ping_handle_t hdl, void *args) {
  auto *self = static_cast<AikosWifi *>(args);
  esp_ping_delete_session(hdl);
  self->probe_done_ = true;
}

void AikosWifi::switch_to_aikos_(uint32_t now) {
  this->switches_++;
  ESP_LOGI(TAG, "the bell answers: switching to '%s' (switch %u, if it fails: next try in %u min)", this->ssid_,
           (unsigned) this->switches_, (unsigned) (this->backoff_ / 60000));
  this->next_probe_ = now + this->backoff_;
  this->after_switch_ = true;
  this->backoff_ = std::min(this->backoff_ * 2, BACKOFF_MAX_MS);
  // Disconnect only: ESPHome's own reconnect then scans and ranks "aikos" (priority 1) above the house Wi-Fi (0, and
  // marked down as the network just lost); if "aikos" fails, the same retry finds the house again. A direct
  // start_connecting() races with the old network's disconnect event and ends in a 30 s scan timeout (bench 03.10.).
  esp_wifi_disconnect();
}

void AikosWifi::test_leave_aikos() {
  if (!this->active_)
    return;
  auto *wifi = wifi::global_wifi_component;
  if (!this->on_aikos_) {
    ESP_LOGW(TAG, "test: not on '%s', nothing to leave", this->ssid_);
    return;
  }
  ESP_LOGW(TAG, "test: leaving '%s' for the house Wi-Fi", this->ssid_);
  // the reconnect scan ranks the bell's access point last; ESPHome clears these marks after the next connection
  wifi->set_sta_priority(wifi->wifi_bssid(), -100);
  esp_wifi_disconnect();
}

void AikosWifi::guard_network_(uint32_t now) {
  auto *wifi = wifi::global_wifi_component;
  if (this->guard_.done.load()) {
    this->guard_.done = false;
    this->guard_.running = false;
    if (this->guard_.replies.load() > 0)
      this->alive_ms_ = now;
  }
  if (!wifi->is_connected()) {
    this->alive_ms_ = now;  // not connected at all: ESPHome's Wi-Fi reboot_timeout covers that case
    return;
  }
  if (!this->guard_.running.load() && reached(now, this->guard_next_)) {
    this->guard_next_ = now + GUARD_EVERY_MS;
    this->start_guard_probe_();
  }
  // H4 stage 2: confirm this firmware once it has been healthy for 2 min (only once per boot)
  const bool healthy = this->guard_.replies.load() > 0 || now - this->alive_ms_ < 90000;
  if (!healthy || this->alive_ms_ == 0) {
    this->healthy_since_ = 0;
  } else if (this->healthy_since_ == 0) {
    this->healthy_since_ = now == 0 ? 1 : now;
  } else if (!this->confirmed_ && now - this->healthy_since_ >= 120000 && this->safe_mode_ != nullptr) {
    this->confirmed_ = true;
    ESP_LOGI(TAG, "healthy for 2 min (gateway answers): firmware confirmed, boot counter cleared");
    this->safe_mode_->mark_successful();
  }
  if (now - this->alive_ms_ > GUARD_DEAD_MS) {
    ESP_LOGE(TAG, "connected, but the gateway has not answered for %u min: network stuck, rebooting",
             (unsigned) (GUARD_DEAD_MS / 60000));
    App.reboot();  // NOT safe_reboot(): that marks the running image good and clears the boot-loop counter (aikos H4)
  }
}

void AikosWifi::start_guard_probe_() {
  esp_netif_t *sta = wifi::global_wifi_component->get_esp_netif_sta();
  esp_netif_ip_info_t ip{};
  if (sta == nullptr || esp_netif_get_ip_info(sta, &ip) != ESP_OK || ip.gw.addr == 0)
    return;  // no gateway yet: next round
  esp_ping_config_t cfg = ESP_PING_DEFAULT_CONFIG();
  ip_addr_set_ip4_u32(&cfg.target_addr, ip.gw.addr);  // works with and without IPv6 in lwIP
  cfg.count = 3;
  cfg.interval_ms = 500;
  cfg.timeout_ms = 1000;
  esp_ping_callbacks_t cbs{};
  cbs.cb_args = &this->guard_;
  cbs.on_ping_success = &AikosWifi::on_guard_success_;
  cbs.on_ping_end = &AikosWifi::on_guard_end_;
  esp_ping_handle_t hdl = nullptr;
  this->guard_.replies = 0;
  this->guard_.done = false;
  if (esp_ping_new_session(&cfg, &cbs, &hdl) != ESP_OK)
    return;
  this->guard_.running = true;
  esp_ping_start(hdl);
}

// ping task
void AikosWifi::on_guard_success_(esp_ping_handle_t hdl, void *args) {
  static_cast<GuardProbe *>(args)->replies.fetch_add(1);
}

void AikosWifi::on_guard_end_(esp_ping_handle_t hdl, void *args) {
  esp_ping_delete_session(hdl);
  static_cast<GuardProbe *>(args)->done = true;
}

void AikosWifi::dump_config() {
  ESP_LOGCONFIG(TAG,
                "aikos Wi-Fi:\n"
                "  Network: '%s' first, house Wi-Fi (Improv) as fallback: %s\n"
                "  Bell probed on the house Wi-Fi: %s",
                this->ssid_, this->active_ ? "yes" : "no house Wi-Fi entered", this->bell_);
}

}  // namespace esphome::aikos_wifi
