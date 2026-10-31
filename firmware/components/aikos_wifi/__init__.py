"""aikos_wifi: the door screen and the talk computer prefer the bell's Wi-Fi "aikos", the house Wi-Fi is their fallback.

aikos bausteine/tuerstation.md H3 (the owner, 2026-10-03): "Wenn aikos wifi verfügbar ist, sollen screen und [talk] es nutzen,
wenn nicht dann main wifi". "aikos" is the bell's own network (bridged into the house LAN, same 192.168.1.x), with its own
password only these devices know. The house Wi-Fi stays the one entered via Improv: it is in no file.

  aikos_wifi:
    password: !secret aikos_wifi_password
    bell: 192.168.x.y        # probed while on the house Wi-Fi: answers = "aikos" is back

No `networks:` under `wifi:` (that would make ESPHome forget the Improv-entered house Wi-Fi). This block adds "aikos" at boot,
ahead of the house Wi-Fi, so a scan that sees both takes "aikos". On the house Wi-Fi it pings the bell every minute; once the
bell answers, it switches back to "aikos" (ESPHome's own roaming only moves between access points of the SAME network).
"""

import esphome.codegen as cg
from esphome.components.safe_mode import SafeModeComponent
import esphome.config_validation as cv
from esphome.const import CONF_ID, CONF_PASSWORD, CONF_SSID

DEPENDENCIES = ["wifi"]
CODEOWNERS = ["@aikos-home"]

CONF_BELL = "bell"
CONF_SAFE_MODE_ID = "safe_mode_id"

aikos_wifi_ns = cg.esphome_ns.namespace("aikos_wifi")
AikosWifi = aikos_wifi_ns.class_("AikosWifi", cg.Component)

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(AikosWifi),
        cv.Optional(CONF_SSID, default="aikos"): cv.ssid,
        cv.Required(CONF_PASSWORD): cv.All(cv.string_strict, cv.Length(min=8, max=63)),
        cv.Required(CONF_BELL): cv.ipv4address,
        # aikos H4 stage 2: a firmware counts as good only after 2 min healthy (the gateway answers); this block then
        # confirms it through ESPHome's safe_mode (clears the boot counter, cancels the bootloader's rollback)
        cv.GenerateID(CONF_SAFE_MODE_ID): cv.use_id(SafeModeComponent),
    }
).extend(cv.COMPONENT_SCHEMA)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    cg.add(var.set_ssid(config[CONF_SSID]))
    cg.add(var.set_password(config[CONF_PASSWORD]))
    cg.add(var.set_bell(str(config[CONF_BELL])))
    cg.add(var.set_safe_mode(await cg.get_variable(config[CONF_SAFE_MODE_ID])))
    # ESPHome narrows its scans to the one network it knows when only one is configured in YAML (none here: the house
    # Wi-Fi comes from Improv); with "aikos" added at runtime the scans must see every network
    cg.add_define("USE_WIFI_MULTI_SSID")
