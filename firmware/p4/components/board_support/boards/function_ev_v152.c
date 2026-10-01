#include "board_support.h"

/* Espressif Function EV hardware v1.5.2 only: EOL software/bench reference. */
static const struct p4_i2c_probe probes[] = {
    {"ES8311 codec", 0x18},
    {"possible SC2336 camera", 0x30},
};

const struct p4_board_config p4_function_ev_v152 = {
    .name = "Espressif Function EV v1.5.2 (EOL bench reference)",
    .ethernet = {
        .phy_kind = P4_PHY_IP101,
        .mdc_gpio = 31,
        .mdio_gpio = 52,
        .reset_gpio = 51,
        .phy_address = 1,
    },
    .i2c = {
        .port = 0,
        .sda_gpio = 7,
        .scl_gpio = 8,
        .probes = probes,
        .probe_count = sizeof(probes) / sizeof(probes[0]),
    },
};
