// aikos_peer_guard: devices in the door box bring each other back by wire (see __init__.py).
#pragma once

#include <functional>
#include <vector>
#include "esphome/components/binary_sensor/binary_sensor.h"
#include "esphome/components/sensor/sensor.h"
#include "esphome/core/component.h"
#include "esphome/core/hal.h"

namespace esphome::aikos_peer_guard {

class AikosPeerGuard : public Component {
 public:
  void set_heartbeat_out(InternalGPIOPin *pin) { this->heartbeat_out_ = pin; }
  void set_healthy(std::function<bool()> &&f) { this->healthy_ = std::move(f); }
  void set_inhibit(std::function<bool()> &&f) { this->inhibit_ = std::move(f); }
  void add_peer(const char *name, InternalGPIOPin *heartbeat_in, InternalGPIOPin *reset_out, uint32_t timeout_ms,
                int max_per_hour, sensor::Sensor *resets, binary_sensor::BinarySensor *heartbeat);
  void setup() override;
  void loop() override;
  void dump_config() override;
  float get_setup_priority() const override { return setup_priority::HARDWARE; }

 protected:
  struct Peer {
    const char *name;
    InternalGPIOPin *heartbeat_in;
    InternalGPIOPin *reset_out;
    uint32_t timeout_ms;
    int max_per_hour;
    sensor::Sensor *resets_sensor;
    binary_sensor::BinarySensor *heartbeat_sensor;
    uint32_t real_edge_ms{0};  // the last edge that really came over the wire (last_edge_ms is also moved by a reset)
    int published{-1};         // the heartbeat sensor's last state (-1 = none yet)
    bool last_level{false};
    bool seen{false};  // a heartbeat edge was seen at least once: only then can a missing one mean "hung"
    uint32_t last_edge_ms{0};
    uint32_t grace_until_ms{0};
    uint32_t pulse_until_ms{0};
    uint32_t hour_start_ms{0};
    int resets_this_hour{0};
    uint32_t resets_total{0};
  };
  InternalGPIOPin *heartbeat_out_{nullptr};
  std::function<bool()> healthy_;
  std::function<bool()> inhibit_;
  std::vector<Peer> peers_;
  bool beat_level_{false};
  uint32_t last_beat_ms_{0};
};

}  // namespace esphome::aikos_peer_guard
