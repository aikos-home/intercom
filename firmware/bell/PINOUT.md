# Bell computer: Waveshare ESP32-S3-ETH (+ PoE Module (B)) — header pinout and bench wiring

Bench state 4 Oct 2026; the whole box (talk computer, amplifier, screen) is in [`../WIRING.md`](../WIRING.md).

Source: Waveshare wiki https://www.waveshare.com/wiki/ESP32-S3-ETH, image "ESP32-S3-ETH-details-15" (checked 2026-10-02).
View: label side, USB-C at the top. Pico-style 2 × 20 header, 2.54 mm pitch, rows 17.78 mm apart.

| Pin | Left row | Bench use | | Pin | Right row | Bench use |
|---|---|---|---|---|---|---|
| 40 | VBUS | **5 V on PoE → breadboard row 25** (talk 5Vin, amp Vin, screen VBUS) | | 1 | GPIO20 (USB D+) | avoid |
| 39 | VSYS | free | | 2 | GPIO19 (USB D−) | avoid |
| 38 | GND | **→ talk computer GND** | | 3 | GND | |
| 37 | 3V3_EN | never connect (to GND it switches 3V3 off) | | 4 | GPIO48 | free |
| 36 | 3V3 | **→ breadboard row 1** | | 5 | GPIO47 | free |
| 35 | GPIO21 | free | | 6 | GPIO46 | strapping, avoid |
| 34 | GPIO17 | free | | 7 | GPIO45 | strapping, avoid |
| 33 | GND | **→ breadboard row 27** (amp GND, screen GND) | | 8 | GND | |
| 32 | GPIO16 | free | | 9 | GPIO42 | free |
| 31 | GPIO18 | free | | 10 | GPIO41 | free |
| 30 | CHIP_UP (printed RUN) | **← talk GPIO9** (the talk computer can reset the bell) | | 11 | GPIO40 | **→ talk RST** (reset out, open-drain) |
| 29 | GPIO15 | free | | 12 | GPIO39 | **→ talk GPIO8** (heartbeat out) |
| 28 | GND | **→ breadboard row 10** | | 13 | GND | |
| 27 | GPIO3 | strapping, avoid | | 14 | GPIO38 | **← talk GPIO18** (heartbeat in) |
| 26 | GPIO2 | free | | 15 | GPIO37 | PSRAM, never |
| 25 | GPIO1 | **button line → breadboard row 5** (`line_pin`) | | 16 | GPIO36 | PSRAM, never |
| 24 | GPIO0 | strapping (BOOT), avoid | | 17 | GPIO35 | PSRAM, never |
| 23 | GND | | | 18 | GND | |
| 22 | GPIO44 (UART0 RX) | avoid | | 19 | GPIO34 | PSRAM, never |
| 21 | GPIO43 (UART0 TX) | avoid | | 20 | GPIO33 | PSRAM, never |

Inside the board, not on the header: W5500 Ethernet GPIO11 MOSI, 12 MISO, 13 CLK, 14 CS, 10 INT, 9 RST; microSD GPIO6 MOSI,
5 MISO, 7 CLK, 4 CS. PoE: VBUS measured 5.0 V on PoE (2026-10-02); never PoE and USB-C power at the same time.

## Breadboard: supervised button line (30.09.2026)

| Where | What |
|---|---|
| row 1 | 3V3 (pin 36) |
| row 5 | GPIO1 (pin 25), the measured node |
| row 8 | line toward the button |
| row 10 | GND (pin 28) |
| 1e–5e | 10 kΩ pull-up |
| 5b–10b | 100 nF filter |
| 5d–8d | 1 kΩ series |
| 8c–10c | 10 kΩ end-of-line (at the button in the real install) |
| 8a, 10e | button wires |

Levels: idle 2.03 V, pressed 0.34–0.47 V, wire break 3.18 V ("line cut"). Idle ≈ 0.7 V = the 10 kΩ pull-up or its 3V3 wire
has no contact (4 Oct 2026): reads as a held button.
