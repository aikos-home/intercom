"""aikos_firmware: the normal firmware and the device's own SAFE firmware (aikos H4 stage 4, the owner 2026-10-03).

The flash holds a fixed safe firmware in the `factory` partition and the normal firmware in app0/app1 (OTA). After 5 failed
boots in a row ESPHome's safe_mode reports a boot loop; the normal firmware then boots the safe one:

  safe_mode:
    on_safe_mode:
      - lambda: aikos_firmware::boot_safe_firmware();
  aikos_firmware:
    role: normal

The safe firmware (role: safe) tries the normal firmware again after `retry_normal_after` (default 60 min); if that still
fails 5 times, it is back. `aikos_firmware::boot_normal_firmware()` also serves a button in Home Assistant.
"""

import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.const import CONF_ID

CODEOWNERS = ["@aikos-home"]

CONF_ROLE = "role"
CONF_RETRY_NORMAL_AFTER = "retry_normal_after"

aikos_firmware_ns = cg.esphome_ns.namespace("aikos_firmware")
AikosFirmware = aikos_firmware_ns.class_("AikosFirmware", cg.Component)

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(AikosFirmware),
        cv.Required(CONF_ROLE): cv.one_of("normal", "safe", lower=True),
        cv.Optional(CONF_RETRY_NORMAL_AFTER, default="60min"): cv.positive_time_period_milliseconds,
    }
).extend(cv.COMPONENT_SCHEMA)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    cg.add(var.set_safe_role(config[CONF_ROLE] == "safe"))
    cg.add(var.set_retry_ms(config[CONF_RETRY_NORMAL_AFTER].total_milliseconds))
