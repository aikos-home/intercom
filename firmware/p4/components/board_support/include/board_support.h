#pragma once

#include <stddef.h>
#include <stdint.h>

/* Board-neutral capabilities. A new target supplies a profile, not new app logic. */
enum p4_phy_kind {
    P4_PHY_IP101 = 1,
};

struct p4_ethernet_config {
    enum p4_phy_kind phy_kind;
    int mdc_gpio;
    int mdio_gpio;
    int reset_gpio;
    int phy_address;
};

struct p4_i2c_probe {
    const char *label;
    uint8_t address;
};

struct p4_i2c_config {
    int port;
    int sda_gpio;
    int scl_gpio;
    const struct p4_i2c_probe *probes;
    size_t probe_count;
};

struct p4_board_config {
    const char *name;
    struct p4_ethernet_config ethernet;
    struct p4_i2c_config i2c;
};

const struct p4_board_config *p4_board_get(void);
void p4_board_report_memory(void);
