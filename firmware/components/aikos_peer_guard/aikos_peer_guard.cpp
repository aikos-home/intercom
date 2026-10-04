// aikos_peer_guard: devices in the door box bring each other back by wire (see __init__.py).
#include "aikos_peer_guard.h"

#include "esphome/core/log.h"

namespace esphome::aikos_peer_guard {

static const char *const TAG = "aikos_peer_guard";
static constexpr uint32_t BEAT_HALF_MS = 500;  // 1 Hz square wave
static constexpr uint32_t GRACE_MS = 120000;   // no reset in the first 2 min after our boot or after a reset
static constexpr uint32_t PULSE_MS = 200;      // reset pulse on the peer's EN
static constexpr uint32_t HOUR_MS = 3600000;

static bool reached(uint32_t now, uint32_t when) { return static_cast<int32_t>(now - when) >= 0; }

void AikosPeerGuard::add_peer(const char *name, InternalGPIOPin *heartbeat_in, InternalGPIOPin *reset_out,
                              uint32_t timeout_ms, int max_per_hour, sensor::Sensor *resets) {
  Peer p{};
  p.name = name;
  p.heartbeat_in = heartbeat_in;
  p.reset_out = reset_out;
  p.timeout_ms = timeout_ms;
  p.max_per_hour = max_per_hour;
  p.resets_sensor = resets;
  this->peers_.push_back(p);
}

void AikosPeerGuard::setup() {
  const uint32_t now = millis();
  this->heartbeat_out_->setup();
  this->heartbeat_out_->digital_write(false);
  for (auto &p : this->peers_) {
    p.heartbeat_in->setup();
    p.heartbeat_in->pin_mode(gpio::FLAG_INPUT | gpio::FLAG_PULLDOWN);  // an unwired input stays low: no false heartbeat
    // NOT reset_out->setup(): that makes it a push-pull output at the register's default LOW, a short reset pulse to the
    // peer on every boot of this device (bell boot resets talk, talk boot resets bell...). Level first, then open-drain:
    // open-drain high = released (high-impedance), the peer's own pull-up holds its EN.
    p.reset_out->digital_write(true);
    p.reset_out->pin_mode(gpio::FLAG_OUTPUT | gpio::FLAG_OPEN_DRAIN);
    p.last_level = p.heartbeat_in->digital_read();
    p.last_edge_ms = now;
    p.grace_until_ms = now + GRACE_MS;
    p.hour_start_ms = now;
    if (p.resets_sensor != nullptr)
      p.resets_sensor->publish_state(0);
  }
}

void AikosPeerGuard::loop() {
  const uint32_t now = millis();
  // our own heartbeat: only while the loop runs and (if given) the device says it is healthy
  if (now - this->last_beat_ms_ >= BEAT_HALF_MS) {
    this->last_beat_ms_ = now;
    if (!this->healthy_ || this->healthy_()) {
      this->beat_level_ = !this->beat_level_;
      this->heartbeat_out_->digital_write(this->beat_level_);
    }
  }
  for (auto &p : this->peers_) {
    if (p.pulse_until_ms != 0) {  // a reset pulse is running: release the line when it is over
      if (reached(now, p.pulse_until_ms)) {
        p.reset_out->digital_write(true);
        p.pulse_until_ms = 0;
      }
      continue;
    }
    const bool level = p.heartbeat_in->digital_read();
    if (level != p.last_level) {
      p.last_level = level;
      p.last_edge_ms = now;
      if (!p.seen)
        ESP_LOGI(TAG, "heartbeat of '%s' seen: watching it", p.name);
      p.seen = true;
    }
    if (now - p.hour_start_ms >= HOUR_MS) {
      p.hour_start_ms = now;
      p.resets_this_hour = 0;
    }
    if (!p.seen || !reached(now, p.grace_until_ms) || now - p.last_edge_ms < p.timeout_ms)
      continue;
    if (this->inhibit_ && this->inhibit_())
      continue;  // ring or call in progress: not now
    if (p.resets_this_hour >= p.max_per_hour) {
      if (p.resets_this_hour == p.max_per_hour) {
        ESP_LOGE(TAG, "'%s' still silent after %d resets this hour: giving up until the hour is over", p.name,
                 p.max_per_hour);
        p.resets_this_hour++;  // log once
      }
      continue;
    }
    p.resets_this_hour++;
    p.resets_total++;
    ESP_LOGW(TAG, "no heartbeat from '%s' for %u s: resetting it (%d this hour)", p.name,
             (unsigned) ((now - p.last_edge_ms) / 1000), p.resets_this_hour);
    p.reset_out->digital_write(false);  // pull its EN low
    p.pulse_until_ms = now + PULSE_MS;
    p.grace_until_ms = now + GRACE_MS;  // give it time to boot before judging again
    p.last_edge_ms = now;
    if (p.resets_sensor != nullptr)
      p.resets_sensor->publish_state(p.resets_total);
  }
}

void AikosPeerGuard::dump_config() {
  ESP_LOGCONFIG(TAG, "aikos peer guard:");
  LOG_PIN("  Heartbeat out: ", this->heartbeat_out_);
  for (auto &p : this->peers_) {
    ESP_LOGCONFIG(TAG, "  Peer '%s': timeout %u s, at most %d resets per hour", p.name, (unsigned) (p.timeout_ms / 1000),
                  p.max_per_hour);
    LOG_PIN("    Heartbeat in: ", p.heartbeat_in);
    LOG_PIN("    Reset out: ", p.reset_out);
  }
}

}  // namespace esphome::aikos_peer_guard
