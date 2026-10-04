// aikos_firmware: normal firmware <-> the device's own safe firmware in the factory partition (see __init__.py).
#pragma once

#include <cstdint>
#include "esphome/core/component.h"

namespace esphome::aikos_firmware {

// Free functions: safe_mode's on_safe_mode runs before the other components exist.
bool boot_safe_firmware();    // remember the running OTA slot, boot the factory partition (false: none, or already there)
bool boot_normal_firmware();  // boot the remembered OTA slot again (false: no valid normal image)
bool running_safe_firmware();

class AikosFirmware : public Component {
 public:
  void set_safe_role(bool safe) { this->safe_role_ = safe; }
  void set_retry_ms(uint32_t ms) { this->retry_ms_ = ms; }
  void setup() override;
  void loop() override;
  void dump_config() override;
  float get_setup_priority() const override { return setup_priority::LATE; }

 protected:
  bool safe_role_{false};
  uint32_t retry_ms_{3600000};
};

}  // namespace esphome::aikos_firmware
