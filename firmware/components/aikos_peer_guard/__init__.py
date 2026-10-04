"""aikos_peer_guard: devices in the door box bring each other back by wire (aikos H4, decided 2026-10-03).

Each device toggles its heartbeat pin at 1 Hz while its loop runs (and its `healthy` lambda, if given, says so). A peer
watches that heartbeat; if it stops for `timeout` (30 s), the peer pulls the device's reset line (EN) low for 200 ms.
Safety: no reset before the heartbeat was seen at least once (a missing or loose wire never resets anything), none in the
first 2 min after our boot or after a reset, at most `max_resets_per_hour` per peer, never while `inhibit` returns true
(ring, call). Every reset is logged and counted in an optional sensor for Home Assistant.

  aikos_peer_guard:
    heartbeat_out: GPIO39
    peers:
      - name: talk
        heartbeat_in: GPIO38
        reset_out: GPIO40          # open-drain: pulls the peer's EN low, otherwise high-impedance
        resets:
          name: Talk computer resets by the bell
"""

import esphome.codegen as cg
from esphome import pins
from esphome.components import sensor
import esphome.config_validation as cv
from esphome.const import CONF_ID, CONF_NAME, CONF_TIMEOUT

CODEOWNERS = ["@aikos-home"]
AUTO_LOAD = ["sensor"]

CONF_HEARTBEAT_OUT = "heartbeat_out"
CONF_HEARTBEAT_IN = "heartbeat_in"
CONF_RESET_OUT = "reset_out"
CONF_PEERS = "peers"
CONF_HEALTHY = "healthy"
CONF_INHIBIT = "inhibit"
CONF_RESETS = "resets"
CONF_MAX_RESETS_PER_HOUR = "max_resets_per_hour"

aikos_peer_guard_ns = cg.esphome_ns.namespace("aikos_peer_guard")
AikosPeerGuard = aikos_peer_guard_ns.class_("AikosPeerGuard", cg.Component)

PEER_SCHEMA = cv.Schema(
    {
        cv.Required(CONF_NAME): cv.string_strict,
        cv.Required(CONF_HEARTBEAT_IN): pins.internal_gpio_input_pin_schema,
        cv.Required(CONF_RESET_OUT): pins.internal_gpio_output_pin_schema,
        cv.Optional(CONF_TIMEOUT, default="30s"): cv.positive_time_period_milliseconds,
        cv.Optional(CONF_MAX_RESETS_PER_HOUR, default=3): cv.int_range(min=1, max=10),
        cv.Optional(CONF_RESETS): sensor.sensor_schema(accuracy_decimals=0, icon="mdi:restart-alert"),
    }
)

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(AikosPeerGuard),
        cv.Required(CONF_HEARTBEAT_OUT): pins.internal_gpio_output_pin_schema,
        cv.Optional(CONF_HEALTHY): cv.returning_lambda,
        cv.Optional(CONF_INHIBIT): cv.returning_lambda,
        cv.Optional(CONF_PEERS, default=[]): cv.ensure_list(PEER_SCHEMA),
    }
).extend(cv.COMPONENT_SCHEMA)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    cg.add(var.set_heartbeat_out(await cg.gpio_pin_expression(config[CONF_HEARTBEAT_OUT])))
    if CONF_HEALTHY in config:
        cg.add(var.set_healthy(await cg.process_lambda(config[CONF_HEALTHY], [], return_type=cg.bool_)))
    if CONF_INHIBIT in config:
        cg.add(var.set_inhibit(await cg.process_lambda(config[CONF_INHIBIT], [], return_type=cg.bool_)))
    for peer in config[CONF_PEERS]:
        heartbeat_in = await cg.gpio_pin_expression(peer[CONF_HEARTBEAT_IN])
        reset_out = await cg.gpio_pin_expression(peer[CONF_RESET_OUT])
        resets = await sensor.new_sensor(peer[CONF_RESETS]) if CONF_RESETS in peer else cg.nullptr
        cg.add(
            var.add_peer(
                peer[CONF_NAME],
                heartbeat_in,
                reset_out,
                peer[CONF_TIMEOUT].total_milliseconds,
                peer[CONF_MAX_RESETS_PER_HOUR],
                resets,
            )
        )
