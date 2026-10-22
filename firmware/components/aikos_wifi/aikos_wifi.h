// aikos_wifi: prefer the bell's Wi-Fi "aikos", fall back to the house Wi-Fi, come back by itself (see __init__.py).
#pragma once

#include <atomic>
#include <ping/ping_sock.h>
#include "esphome/components/safe_mode/safe_mode.h"
#include "esphome/components/wifi/wifi_component.h"
#include "esphome/core/component.h"

namespace esphome::aikos_wifi {

class AikosWifi : public Component {
 public:
  // right after WiFiComponent::setup() (WIFI = 250) loaded the house Wi-Fi from flash and started its first scan;
  // that scan is evaluated in the Wi-Fi loop, so after setup, and then already sees "aikos"
  float get_setup_priority() const override { return setup_priority::WIFI - 1.0f; }
  void setup() override;
  void loop() override;
  void dump_config() override;

  void set_ssid(const char *ssid) { this->ssid_ = ssid; }
  void set_password(const char *password) { this->password_ = password; }
  void set_bell(const char *bell) { this->bell_ = bell; }
  void set_safe_mode(safe_mode::SafeModeComponent *sm) { this->safe_mode_ = sm; }

  // bench test (API action): to the house Wi-Fi now, as if "aikos" had gone; the normal logic must bring the device
  // back to "aikos" once the bell answers
  void test_leave_aikos();

 protected:
  void start_probe_(uint32_t now);
  void switch_to_aikos_(uint32_t now);
  static void on_ping_success_(esp_ping_handle_t hdl, void *args);
  static void on_ping_end_(esp_ping_handle_t hdl, void *args);

  // Network guard (aikos H4, 2026-10-03: the talk computer stayed associated but dead for 12 min, nothing rebooted it):
  // while connected, ping the gateway every minute; no reply for 5 min = the network stack is stuck -> reboot.
  // Independent of Home Assistant (a wrong HA address must not cause reboots). Not connected at all: ESPHome's own Wi-Fi
  // reboot_timeout covers that.
  struct GuardProbe {
    std::atomic<bool> running{false};
    std::atomic<bool> done{false};
    std::atomic<uint32_t> replies{0};
  };
  void guard_network_(uint32_t now);
  void start_guard_probe_();
  static void on_guard_success_(esp_ping_handle_t hdl, void *args);
  static void on_guard_end_(esp_ping_handle_t hdl, void *args);
  GuardProbe guard_;
  uint32_t guard_next_{0};
  uint32_t alive_ms_{0};
  // H4 stage 2: healthy = connected and the gateway answered within 90 s; 2 min of that confirms the firmware
  safe_mode::SafeModeComponent *safe_mode_{nullptr};
  uint32_t healthy_since_{0};
  bool confirmed_{false};

  const char *ssid_{"aikos"};
  const char *password_{""};
  const char *bell_{""};
  bool active_{false};      // "aikos" was added (needs the Improv-entered house Wi-Fi as the second network)
  bool on_aikos_{false};
  bool on_other_{false};    // connected, but not to "aikos" (the house Wi-Fi)
  bool after_switch_{false};  // a switch to "aikos" is under way: if it ends on the house Wi-Fi, the backoff applies
  uint32_t next_probe_{0};  // earliest time for the next bell probe (millis), always set relative to a recent "now"
  uint32_t backoff_{0};     // wait after a switch that ended back on the house Wi-Fi; doubles up to an hour
  uint32_t switches_{0};
  // one probe at a time: the ping task writes, loop() reads
  std::atomic<bool> probing_{false};
  std::atomic<bool> probe_done_{false};
  std::atomic<uint32_t> probe_replies_{0};
};

}  // namespace esphome::aikos_wifi
