"""eth_wifi_bridge: the bell's Ethernet and its Wi-Fi access point as ONE network (layer-2 bridge).

aikos bausteine/tuerstation.md H3 (the owner, 2026-10-03): the bell provides Wi-Fi for the door screen and the talk computer,
in the same network as the house (devices keep 192.168.1.x from the house DHCP), with the house Wi-Fi as their fallback.

  network:
    priority: [ethernet, wifi]
  wifi:
    ap: {ssid: ..., password: ...}   # the access point; no station networks
  eth_wifi_bridge:

ESPHome sets up Ethernet and the access point as usual; this block then puts both into an ESP-IDF bridge (br0, the
official esp_netif_br_glue), moves the bell's own address onto br0 and points ESPHome's Ethernet at br0.
"""

import esphome.codegen as cg
from esphome.components.safe_mode import SafeModeComponent
from esphome.components.esp32 import add_idf_sdkconfig_option, include_builtin_idf_component
import esphome.config_validation as cv
from esphome.const import CONF_ID

DEPENDENCIES = ["ethernet", "wifi"]
CODEOWNERS = ["@aikos-home"]

eth_wifi_bridge_ns = cg.esphome_ns.namespace("eth_wifi_bridge")
EthWifiBridge = eth_wifi_bridge_ns.class_("EthWifiBridge", cg.Component)

CONF_CORE_DUMP = "core_dump"
CONF_TCP_GUARD_HOST = "tcp_guard_host"
CONF_SAFE_MODE_ID = "safe_mode_id"

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(EthWifiBridge),
        # bench only: a crash prints a core dump of all tasks to the USB console. Never on a bell without a PC on USB.
        cv.Optional(CONF_CORE_DUMP, default=False): cv.boolean,
        # TCP guard target (default: the gateway of br0); only for testing the guard with an address that never answers
        cv.Optional(CONF_TCP_GUARD_HOST): cv.ipv4address,
        # aikos H4 stage 2: the firmware counts as good only after 2 min healthy (address on br0 + TCP guard ok)
        cv.GenerateID(CONF_SAFE_MODE_ID): cv.use_id(SafeModeComponent),
    }
).extend(cv.COMPONENT_SCHEMA)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    add_idf_sdkconfig_option("CONFIG_ESP_NETIF_BRIDGE_EN", True)
    # ESPHome builds lwIP with room for one bridge port only; br0 has two (Ethernet + access point)
    add_idf_sdkconfig_option("CONFIG_LWIP_BRIDGEIF_MAX_PORTS", 2)
    # the bridge keeps its state in lwIP netif client data (as in the ESP-IDF bridge example)
    add_idf_sdkconfig_option("CONFIG_LWIP_NUM_NETIF_CLIENT_DATA", 1)
    # bench diagnosis (2026-10-03): CPU share per task in the 15 s status line (W5500 receive task vs. ESPHome's loop)
    add_idf_sdkconfig_option("CONFIG_FREERTOS_USE_TRACE_FACILITY", True)
    add_idf_sdkconfig_option("CONFIG_FREERTOS_GENERATE_RUN_TIME_STATS", True)
    cg.add(var.set_safe_mode(await cg.get_variable(config[CONF_SAFE_MODE_ID])))
    if CONF_TCP_GUARD_HOST in config:
        cg.add(var.set_tcp_guard_host(str(config[CONF_TCP_GUARD_HOST])))
    if config[CONF_CORE_DUMP]:
        # bench diagnosis (2026-10-03): on a crash, print a core dump of ALL tasks to the console (USB), decoded with
        # esp-coredump + xtensa GDB against firmware.elf -> where loopTask and the lwIP task wait during the hang
        include_builtin_idf_component("espcoredump")  # ESPHome leaves it out by default
        add_idf_sdkconfig_option("CONFIG_ESP_COREDUMP_ENABLE_TO_NONE", False)
        add_idf_sdkconfig_option("CONFIG_ESP_COREDUMP_ENABLE_TO_UART", True)
        add_idf_sdkconfig_option("CONFIG_ESP_COREDUMP_DATA_FORMAT_ELF", True)
        add_idf_sdkconfig_option("CONFIG_ESP_COREDUMP_CHECKSUM_CRC32", True)
