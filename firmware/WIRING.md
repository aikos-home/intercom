# Wiring: the three door computers on one PoE cable

This is the wiring **as it runs on the bench on 4 October 2026**, not a plan. Each section says how it was
checked. Wire colours are the bench jumpers, listed only to make the photos and the text match; use any colour.

| Computer | Board | Firmware (4 Oct 2026) |
|---|---|---|
| **Bell** | Waveshare ESP32-S3-ETH + plug-on *PoE Module (B)* | `bell/aikos-intercom-bell-bridge.yaml` 0.3.20 |
| **Talk computer** | ESP32-S3-N16R8 dev board, silkscreen "HW678" | `talk_computer/aikos-intercom-talk.yaml` 0.7.20 |
| **Screen** | LilyGO T5-4.7-S3 Touch, board "Screen-4.7-S3 V2.4" | `aikos-intercom-screen.yaml` 0.7.12 |

```
switch port (PoE) ══ Ethernet ══ BELL (RJ45 + PoE module) ── 5 V + GND ──┬── talk computer (5Vin)
                                     │  ↑ Wi-Fi "aikos"                    ├── amplifier (Vin) ── speaker
                                     │  button line (breadboard)           └── screen (VBUS)
                                     └── 4 supervision wires ── talk computer ── microphone
```

The bell is the only wired computer. The talk computer and the screen reach the network over the bell's own
Wi-Fi ("aikos"), which the bell bridges into the LAN.

## Rules that broke boards or cost hours

- **Power off before every wiring change:** switch the PoE port off (or pull USB), then change wires, then power
  on. Moving a signal wire under power on 4 Oct 2026 took the talk computer off the network (its LED blinked)
  until a power cycle; a live re-plug of the 5 V jumpers killed a talk board on 2 Oct 2026.
- **Never USB and PoE at the same time** on the bell, the talk computer or the screen. They all hang on the same
  5 V rail, so a USB cable on any of them can feed the others backwards.
- **No breadboard contacts in the box.** On 4 Oct 2026 two faults were loose breadboard or jumper contacts:
  - the amplifier's GND had no contact: the sound was distorted on every speaker, and the amp's Vin read 4.4 V
    instead of 5 V. Most likely its current went back through the input pins (the missing 0.6 V is one diode
    drop). After re-seating, the GND beeped through and the sound was clean;
  - the button line's 10 kΩ pull-up lost contact, so the line idled at 0.75 V instead of 2.02 V, which reads as
    a held button ("Line shorted"), and the bell ignored presses.

  Solder or clamp everything that goes into the box, and run 5 V and GND over short, thick wires.

## 1. Power: one 5 V rail from the bell

Checked: the owner's description of the breadboard (3 Oct 2026); the talk computer's pins read out one by one
(4 Oct 2026); continuity beeped from the amplifier's GND pin to the talk computer's GND pin (4 Oct 2026).

| From | To | Notes |
|---|---|---|
| bell header pin 40 (VBUS) | breadboard **row 25** | 5.0 V when the bell runs on PoE |
| bell header pin 33 (GND) | breadboard **row 27** | |
| bell header pin 38 (GND) | talk computer **GND** (pin row with 3V3, last pin) | direct, grey |
| row 25 | talk computer **5Vin** (second-to-last pin of the 3V3 row) | red. Works as an input without the board's IN-OUT solder bridge |
| row 25 | amplifier **Vin** | red |
| row 27 | amplifier **GND** | blue |
| row 25 | screen **VBUS** (see section 5) | thick red, soldered at the screen |
| row 27 | screen **GND** (see section 5) | thick black, soldered at the screen |

Draw at the switch port (UniFi): bell alone 1.17 W · bell + talk computer 1.59 W · plus microphone and amplifier
idle 2.38 W · plus the screen **4.13 W**.

## 2. Talk computer (HW678) pin by pin

Read out by the owner, pin by pin, on 4 Oct 2026. The board has two pin rows; the labels are printed next to the pins.

**Row with 3V3 · 3V3 · RST · 4 · 5 · 6 · 7 · 15 · 16 · 17 · 18 · 8 · 3 · 46 · 9 · 10 · 11 · 12 · 13 · 14 · 5Vin · GND**

| Pin | Colour | Goes to |
|---|---|---|
| 3V3 | orange | microphone VDD |
| RST | black | bell **GPIO40** (header pin 11): the bell can reset the talk computer |
| 6 | black | microphone **SD** (data) |
| 15 | purple | amplifier **BCLK** |
| 16 | blue | amplifier **LRC** |
| 17 | orange | amplifier **DIN** |
| 18 | white | bell **GPIO38** (header pin 14): heartbeat of the talk computer |
| 8 | yellow | bell **GPIO39** (header pin 12): heartbeat of the bell |
| 9 | brown | bell **CHIP_UP** (header pin 30, printed "RUN"): the talk computer can reset the bell |
| 5Vin | red | breadboard row 25 |
| GND | grey | bell header pin 38 |

Nothing on 4, 5, 7, 3 and **46** (strapping pin: keep it free).

**Row with GND · TX · RX · 1 · 2 · 42 · 41 · 40 · 39 · 38 · 37 · 36 · 35 · 0 · 45 · 48 · 47 · 21 · 20 · 19 · GND · GND**

| Pin | Colour | Goes to |
|---|---|---|
| 1 | orange | microphone **SCK** |
| 2 | purple | microphone **WS** |
| GND (bottom) | grey | microphone **GND** |
| GND (bottom) | grey | microphone **L/R** (low = left channel) |

Nothing on 0 and 45 (strapping pins: a wire there can stop the board from booting).

> The first wiring sheet had the microphone on GPIO 4 / 5 / 6. The box was wired SCK → 1, WS → 2 and SD → GND,
> so the microphone delivered only silence. SD was moved to 6, and the firmware (0.7.19+) reads SCK on GPIO1 and
> WS on GPIO2.

## 3. Microphone (INMP441 module)

| Microphone | Talk computer |
|---|---|
| VDD | 3V3 |
| GND | GND |
| L/R | GND (left channel, as in the firmware) |
| SD | GPIO6 |
| SCK | GPIO1 |
| WS | GPIO2 |

Checked on 4 Oct 2026: speech at about 30 cm reads around −16 dBFS, the room around −57 dBFS.

## 4. Amplifier (MAX98357A breakout) and speaker

Read out by the owner on 4 Oct 2026, with the board's screw terminal at the top: from the left LRC, BCLK, DIN,
GAIN, SD, GND, Vin. Each signal wire beeped from the talk computer's pin to the amplifier's pin.

| Amplifier | Goes to |
|---|---|
| LRC | talk computer GPIO16 |
| BCLK | talk computer GPIO15 |
| DIN | talk computer GPIO17 |
| GAIN | free (9 dB) |
| SD | free |
| GND | breadboard row 27 |
| Vin | breadboard row 25 (5 V) |
| screw terminal + / − | speaker + / − (VISATON K 40 SQ, 8 Ω, 40 × 40 mm) |

The firmware plays a test gong only on demand (button "Test chime" in Home Assistant) at full level; speech is
capped at −6 dB (`talk_computer/talk_volume.h`). The door itself never chimes.

## 5. Screen (LilyGO T5-4.7-S3, board V2.4)

Checked on 4 Oct 2026: labels read on the board, soldered, no short between the two wires (beep test), boots on
PoE and joins "aikos" at −34 dBm.

The board has an unpopulated 2 × 20 hole row at one long edge. Component side up, USB-C on the left: the row
**right at the board edge** reads from the left **VBUS · VBUS · GND** · RX · TX … (LilyGO schematic V2.4,
connector P8: pins 2 and 4 VBUS, pin 6 GND).

| Hole (edge row, from the left) | Goes to |
|---|---|
| 1 · VBUS | thick red wire → breadboard row 25 |
| 2 · VBUS | free (connected to hole 1 on the board) |
| 3 · GND | thick black wire → breadboard row 27 |

Solder the wires from the component side and cut them flush on the other side: the e-paper glass lies there.
The screen's USB-C stays unplugged while PoE is on.

## 6. Supervision wires between the bell and the talk computer

Firmware: `components/aikos_peer_guard`. Each computer toggles a heartbeat pin once per second while it runs; if
the other one's heartbeat stops for 30 s, it pulls the other's reset line low for 200 ms (at most 3 times an hour,
never before it has seen a heartbeat, never in the first 2 minutes).

| Wire | Bell | Talk computer |
|---|---|---|
| bell's heartbeat | GPIO39 (pin 12) → | GPIO8 |
| talk's heartbeat | GPIO38 (pin 14) ← | GPIO18 |
| reset the talk computer | GPIO40 (pin 11, open-drain) → | RST |
| reset the bell | CHIP_UP (pin 30, printed "RUN") ← | GPIO9 (open-drain) |

⚠️ Bell pin 37 (3V3_EN) is **not** the reset: pulling it low switches the bell's 3.3 V off. Never connect it.

## 7. Bell: the button line

Built on 30 Sep 2026 (second, small breadboard); not re-read pin by pin since. On 4 Oct 2026 the pull-up was
re-seated and the line measured 2.02 V idle again. Full table: [`bell/PINOUT.md`](bell/PINOUT.md).

| Breadboard | What |
|---|---|
| row 1 | bell 3V3 (pin 36) |
| row 5 | bell GPIO1 (pin 25), the measured node |
| row 8 | line toward the button |
| row 10 | bell GND (pin 28) |
| 1e–5e | 10 kΩ pull-up |
| 5b–10b | 100 nF |
| 5d–8d | 1 kΩ (stands in for the cable run) |
| 8c–10c | 10 kΩ end-of-line (sits at the button in the real install) |
| 8a, 10e | the brass button |

| Line | Volts at GPIO1 |
|---|---|
| idle | 2.02–2.03 |
| pressed | 0.34–0.47 |
| cable cut | 3.18 |
| idle at ≈ 0.7 | the 10 kΩ pull-up (or its 3V3 wire) has no contact: reads as a held button |
