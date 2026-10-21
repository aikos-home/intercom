# Wiring: the door box (as built, 16–20 October 2026)

This is the wiring **as it runs in the printed v3 box**, not a plan. Everything is soldered, with 10–15 cm of slack on
every wire, so the whole harness can move to the next box as one piece. Each section says how it was checked.
Wire colours and numbers are the ones used in this box; they only make the photos and the sheets match. The number on a
tape flag at both ends is what counts. The German sheets the box was soldered from:
[`docs/wiring-sheets/`](../docs/wiring-sheets/) (round 1 the distribution board, round 2 the computer carrier); where the
box differs from a sheet, this page says so.

| Computer | Board | Runs (20 Oct 2026) | Built, waiting to be flashed |
|---|---|---|---|
| **Bell** | Waveshare ESP32-S3-ETH + plug-on *PoE Module (B)* | `bell/aikos-intercom-bell-bridge.yaml` 0.3.21 | 0.3.23 (climate sensors, 60 ms debounce, direct ring to the talk computer) |
| **Talk computer** | ESP32-S3-N16R8 dev board, silkscreen "HW678" | `talk_computer/aikos-intercom-talk.yaml` 0.7.20 | 0.7.21 (direct ring from the bell, "leave a message") |
| **Screen** | LilyGO T5-4.7-S3 Touch, board "Screen-4.7-S3 V2.4" | `aikos-intercom-screen.yaml` 0.7.14 | 0.7.15 (radar, targeted ring, "leave a message", quiet hours) |

```
switch port (PoE) ══ Ethernet ══ BELL ── 5 V, GND, 3V3, button line, I2C ── DISTRIBUTION BOARD ──┬── screen (5 V) ── radar
                                  │                                                              ├── amplifier ── speaker
                                  │  ↑ Wi-Fi "aikos"                                              ├── brass button (+ 10 kΩ EOL)
                                  ├── 5 V, GND, 4 supervision wires ── TALK COMPUTER             ├── SHT31 (outdoor chamber)
                                  │                                     ├── I2S ── amplifier      └── BME280 (on the board)
                                  │                                     └── I2S ── microphone
```

The bell is the only wired computer. The talk computer and the screen reach the network over the bell's own Wi-Fi
("aikos"), which the bell bridges into the LAN. Measured at the switch port with everything in the box: **4.82 W**
(the radar adds about 0.4 W to the bench figure of 4.13 W).

## Rules that broke boards or cost hours

- **Power off before every wiring change:** switch the PoE port off (or pull the LAN plug), then solder, then power on.
  Moving a signal wire under power on 4 Oct 2026 took the talk computer off the network; a live re-plug of the 5 V
  jumpers killed a talk board on 2 Oct 2026.
- **Never USB and PoE at the same time** on any of the three. They all hang on the same 5 V rail, so a USB cable on any
  of them feeds the others backwards.
- **No breadboard or jumper contacts in the box.** Two faults on the bench were loose contacts (amplifier GND: distorted
  sound; button pull-up: the bell read a held button). In the box everything is soldered or under a screw terminal.
- **Stranded wire throws single strands.** On 17 Oct 2026 the box's 3V3 and GND rails beeped through each other: one
  stray strand of a thick wire touched the next pin. Twist and tin every end, look at every joint with a loupe or a
  phone zoom, beep 3V3 against GND before the first power-on.
- **Bell pin 37 (3V3_EN) is never connected,** not even by a solder bridge: it sits between GND and 3V3, and pulling it
  low switches the bell's 3.3 V off.

## 1. Distribution board (30 × 70 mm, 10 × 24 holes)

Plated double-sided prototype board on a clip socket at the back wall, bottom left. Components face the front.
Columns A–J from the left, rows 1–24 from the top, as seen from the front in the box. Under the board there are only
3 mm: legs and wires are cut to 1 mm at the back.

**Strips at the back** (bare wire, soldered at every hole of the strip):

| Strip | Holes | Net |
|---|---|---|
| GND rail | A1–A24 | GND |
| 5 V rail | B1–B7 | 5 V (B8 stays empty) |
| 3V3 rail | J9–J24 | 3V3 from the bell |
| Button node | E10–E13 | bell GPIO1 (the measured node) |
| Button line | I13–I15 | towards the brass button |
| SCL | F16–F20 | I2C clock |
| SDA | G16–G20 | I2C data |
| BME VCC | D19–D20 | |
| BME GND | E18–E20 | |

**Parts on the front:** R1 10 kΩ E11–J11 (pull-up), C1 100 nF E12–A12 (filter), R2 1 kΩ E13–I13 (series, protects the
GPIO against ESD from the brass button). **BME280** (GY-BME280, 6 pins) with its header in D20–I20: VCC D20, GND E20,
SCL F20, SDA G20, CSB H20 and SDO I20 soldered only (nothing else on them: address 0x76). Two insulated bridges on the
front: **D19 → J19** (BME VCC to 3V3) and **E18 → A18** (BME GND to GND). C1–J7 stays free for the heater switch.
Sheet: `docs/wiring-sheets/kasten-runde1-verteiler.svg`.

**The 16 wires of the board:**

| No. | Hole | Net | Colour | Length | Goes to |
|---|---|---|---|---|---|
| 1 | A1 | GND | black, thick | 30 cm | bell GND (right row, between IO16 and IO17) |
| 2 | B1 | 5 V | red, thick | 30 cm | bell VBUS (right row, bottom) |
| 3 | A3 | GND | black, thick | 30 cm | screen edge hole 3 (GND) |
| 4 | B3 | 5 V | red, thick | 30 cm | screen edge hole 1 (VBUS) |
| 5 | A5 | GND | white, thick | 20 cm | amplifier GND |
| 6 | B5 | 5 V | green, thick | 20 cm | amplifier Vin |
| 7 | J9 | 3V3 | orange | 30 cm | bell 3V3 (right row) |
| 8 | E10 | button node | blue | 30 cm | bell IO1 (right row) |
| 9 | I15 | button line | yellow | 15 cm | brass button, terminal 1 |
| 10 | A15 | GND | black | 15 cm | brass button, terminal 2 |
| 11 | F16 | SCL | green | 30 cm | bell IO18 (right row) |
| 12 | G16 | SDA | white | 30 cm | bell IO17 (right row) |
| 13 | J17 | 3V3 | orange | 15 cm | SHT31 VIN |
| 14 | A17 | GND | black | 15 cm | SHT31 GND |
| 15 | F17 | SCL | green | 15 cm | SHT31 SCL |
| 16 | G17 | SDA | white | 15 cm | SHT31 SDA |

"Thick" = 0.34–0.5 mm² for power; the signal wires are 0.05 mm² stranded, twisted per group and held with hot glue
next to every joint, so they bend in the glue and not at the solder.

Checked (owner, 17 Oct 2026, no power): no continuous beep between GND, 5 V and 3V3; SCL against SDA no beep; every GND,
5 V, 3V3, SCL and SDA wire end beeps to its rail, including the BME pins and the SHT31 pads.

## 2. Bell header in the box

The bell lies on the computer carrier with its **label side to the front and USB-C and LAN socket at the bottom**. In
that position the row with VBUS, GND and 3V3 is on the **outside right**, the row with IO33…IO20 faces the talk computer
(rotate [`bell/PINOUT.md`](bell/PINOUT.md) by 180°: it is drawn with USB-C at the top).

Right row, top to bottom: IO43 · IO44 · GND · IO0 · **IO1** (8) · IO2 · IO3 · GND · IO15 · **RUN** (22) · **IO18** (11) ·
IO16 · **GND** (1) · **IO17** (12) · IO21 · **3V3** (7) · 3V3_EN ✕ · GND · VSYS · **VBUS** (2 + 17).

Left row, top to bottom: IO33 · IO34 · GND · IO35 · IO36 · IO37 · **IO38** (21) · **GND** (18) · **IO39** (20) ·
**IO40** (19) · IO41 · IO42 · GND · IO45 · IO46 · IO47 · IO48 · GND · IO19 · IO20.

(Numbers in brackets = wire numbers.) Free and never used: IO0, IO3, IO45, IO46 (strapping), IO33–IO37 (PSRAM),
IO43/IO44 (UART0), IO19/IO20 (USB). Every joint on a header pin has its own piece of heat shrink.

## 3. Talk computer in the box

Module side to the carrier, pins to the front, antenna up, USB-C down. From the front the **TX row is on the left**, the
**3V3 row on the right** (towards the bell).

3V3 row, top to bottom: **3V3** (26) · 3V3 · **RST** (19) · 4 · 5 · **6** (27) · 7 · **15** (23) · **16** (24) ·
**17** (25) · **18** (21) · **8** (20) · 3 ✕ · 46 ✕ · **9** (22) · 10 · 11 · 12 · 13 · 14 · **5Vin** (17) · **GND** (18).

TX row, top to bottom: GND · TX · RX · **1** (28) · **2** (29) · 42 · 41 · 40 · 39 · 38 · 37 · 36 · 35 · 0 ✕ · 45 ✕ · 48 ·
47 · 21 · 20 · 19 · **GND** (30) · GND.

## 4. Bell ↔ talk computer (both on the carrier, they always move together)

| No. | Bell | Talk computer | Colour | What |
|---|---|---|---|---|
| 17 | VBUS (together with wire 2) | 5Vin | red, thick, 15 cm | 5 V. Works as an input without the board's IN-OUT bridge |
| 18 | GND (left row, under IO38) | GND (3V3 row, bottom) | black, thick, 10 cm | |
| 19 | IO40 | RST | yellow | the bell can reset the talk computer (open-drain) |
| 20 | IO39 | 8 | yellow | heartbeat of the bell |
| 21 | IO38 | 18 | yellow | heartbeat of the talk computer |
| 22 | RUN | 9 | yellow | the talk computer can reset the bell (open-drain) |

17 and 22 run up the outside of the bell and over its top end. Firmware: `components/aikos_peer_guard`. Each computer
toggles its heartbeat pin once per second; if the other's heartbeat stops for 30 s, it pulls the other's reset line low
for 200 ms (at most 3 times an hour, never before it has seen a heartbeat, never in its first 2 minutes).

**Proven in the box (2026-10-21):** heartbeats 20/21 both ways (the sensors "Talk computer heartbeat" on the bell and "Bell
heartbeat" on the talk computer are on). Reset wires with the test actions `test_reset_talk` (bell, from 0.3.25) and
`test_reset_bell` (talk computer, from 0.7.25), the same 200 ms pulse the guard sends to a hung peer: wire 19 restarted the
talk computer (its values came back fresh), wire 22 restarted the bell (uptime 241 s -> 4 s).

## 5. Amplifier (MAX98357A) and speaker

The amplifier sits on the back of the display carrier plate. Pins: LRC, BCLK, DIN, GAIN, SD, GND, Vin.

| Amplifier | From | Colour |
|---|---|---|
| LRC | talk 16 (wire 24) | red — a signal, not power |
| BCLK | talk 15 (wire 23) | orange |
| DIN | talk 17 (wire 25) | black — a signal, not ground |
| GAIN, SD | free (9 dB) | |
| GND | board A5 (wire 5) | white, thick |
| Vin | board B5 (wire 6) | green, thick |
| terminal + / − | speaker + / − (VISATON K 40 SQ, 8 Ω) | twisted pair, about 20 cm |

Checked in the box (20 Oct 2026): test tones and a spoken sentence from Home Assistant, the owner: "klingt sauber".

## 6. Microphone (INMP441)

| Microphone | Talk computer | Colour |
|---|---|---|
| VDD | 3V3 (top of the 3V3 row, wire 26) | yellow |
| SD | GPIO6 (wire 27) | white |
| SCK | GPIO1 (wire 28) | green |
| WS | GPIO2 (wire 29) | brown |
| GND | GND (TX row, second to last, wire 30) | blue |
| L/R | bridged to GND on the module | left channel |

The five wires are twisted together (35 cm). The module sits in the front pocket with its smooth side (the sound hole)
flat on the gasket, so nothing may stick out on that side. Checked in the box: a sentence spoken at the closed front
came back as text on the screen.

## 7. Brass button

The button has screw terminals. Wire 9 (line) and wire 10 (GND) go one into each terminal, and the **10 kΩ end-of-line
resistor** goes across the two terminals, its legs wrapped around the bare wire ends (not tinned: solder under a screw
loosens). Heat shrink on the resistor, so its legs never touch the brass. The resistor has to sit **at the button**:
anywhere else a cut wire between it and the button would still read as "idle".

| Line | Volts at the bell's GPIO1 |
|---|---|
| idle | 1.99–2.03 (box 20 Oct 2026: 1.99) |
| pressed | 0.34–0.47 |
| cable cut | 3.18 |
| idle at ≈ 0.7 | the 10 kΩ pull-up (or its 3V3) has no contact: reads as a held button |

## 8. Climate sensors (one I2C bus from the bell, 100 kHz)

| Part | Where | Address | Wires |
|---|---|---|---|
| BME280 (GY-BME280) | on the distribution board | 0x76 (CSB, SDO open) | on the board, section 1 |
| SHT31-D | outdoor chamber, on the pin of the chamber lid, label side to the lid | 0x44 | 13–16 through the lid's cable hole (sealed with silicone) |

Bell: SDA = IO17, SCL = IO18. Both modules bring their own pull-ups to 3V3. Firmware from bell 0.3.23 (scans the bus at
boot and logs what answers).

## 9. Screen power and radar

The screen's unpopulated 2 × 20 hole row at one long edge; the row **right at the board edge** reads (component side
up, USB-C on the left) **VBUS · VBUS · GND · RX · TX** …; the labels are printed next to the holes.

| Hole | Goes to |
|---|---|
| 1 · VBUS | wire 4 (5 V from the board) |
| 2 · VBUS | radar VCC (white) |
| 3 · GND | wire 3 (GND from the board) |
| GND | radar GND (yellow) |
| 4 · RX (GPIO44) | radar TX (orange) |
| 5 · TX (GPIO43) | radar RX (blue) |

Solder from the component side and cut flush on the other side: the e-paper glass lies there. The radar (HLK-LD2410C)
sits glued behind the speaker grille; its OUT pin stays free. The radar wires are 30 cm: the screen comes off with the
front plate while the radar stays in the box. Holes 1 and 2 beep through each other on purpose (both are VBUS).
UART0 is free for the radar because the screen logs over USB. Firmware from screen 0.7.15.

## 10. Heater foil: parked, not connected

The foil (Adafruit 1481, about 5 W at 5 V) is clamped between the e-paper and its board. Its two thin leads are
extended to 30 cm (crimped: a lever clamp found no contact on them), each end insulated on its own, and parked at the
distribution board. It stays disconnected until the bell can
switch it: a logic-level MOSFET on the board (free area C1–J7), the 73 °C thermal fuse in series, and the governor in the
bell's firmware (box dew point and margin are already in 0.3.23). On the bench the rail stood at 4.8 V with the heater on.

**Switch chosen (2026-10-21):** an **HW-532** module (FR120N, opto-isolated input that takes a 3.3 V signal; load side
rated 5-30 V, so our 5 V rail is at its low end, enough for this foil) instead of a bare MOSFET on the board. Control
from **bell GPIO16 (header pin 32)**, signal GND from pin 33 next to it; the module's supply from the 5 V rail; its output
to the foil with the 73 °C fuse in series. Terminal names on the module still to be read off the module itself (sellers
print PWM/GND and +/LOAD/- or LOAD+/LOAD-): the sheet comes after a photo of it.
**Governor in bell 0.3.26** (dry-run 21.10., foil not wired): slow PWM, 10 s period; heats when the box dew point margin
falls below the target (default 6 K; margin 0 K = full) or the box gets colder than the minimum (default 3 °C; full 5 K
below), never at 40 °C or more, never without valid readings (about 3 min after a restart), at most "Heater maximum power"
(default 60 %), and only while "Heater allowed" is on (off from the factory). Power: the foil roughly doubles the box's
draw (4.82 W today); after wiring, a full-load test (heater 100 %, speaker test, screen page change) must show no restart.

## 10a. Door light: firmware ready, strip not wired

the owner's SK6812 RGBW strip (5 V, 60/m, 5050, pads +5V / DIN / DO / GND; from the RoomKey parts) under the canopy in the
diffuser: 3 LEDs fit the 57 mm there (width to be checked against the 10 mm channel). **Data from bell GPIO15 (header
pin 29), GND on pin 28 next to it**, +5V and GND from the distribution board; three wires through the cable hole under
the diffuser. DIN wants >= 3.5 V at 5 V supply: 3.3 V usually works on a short wire, a 74AHCT125 makes it certain.
Firmware: bell 0.3.27, light "Door light" (RGBW), off after a restart; about 1.2 W at full white. While it is on, the
heater pauses (PoE budget).

## 11. Before the first power-on

No power, multimeter on beep:

| Measure | Good |
|---|---|
| bell VBUS against bell GND | no continuous beep |
| bell 3V3 against bell GND | no continuous beep |
| bell 3V3_EN against 3V3 and against GND | no beep |
| talk 5Vin against talk GND | no continuous beep |
| screen hole 1 against hole 3 | a short chirp (capacitors), no continuous beep |

Then no USB cable on any board, no loose wire ends or cut legs in the box, plug the LAN cable in, PoE on, watch and smell
for 30 s. First power-on in the box on 20 Oct 2026 (front sheet off):

| What | Result |
|---|---|
| Network | all three computers answer; the talk computer's Wi-Fi at −29 dBm |
| Button line, idle | 1.99 V (bench: 2.02 V); "line cut" and "line shorted" both off |
| Two presses | counted by the bell, received by the screen both directly and via Home Assistant |
| Supervision wires | no reset in either direction |
| Microphone | delivers audio, noise floor −54.9 dB; a sentence at the closed front came back as text on the screen |
| Speaker | a tone sweep and a spoken message from Home Assistant played clean |
| Power at the switch port | 4.82 W (heater not connected) |

Not measured yet in the box: the line voltage while pressed, R1 and R2 as numbers, the climate sensors and the radar
(their firmware is built but not yet on the devices), whether each computer sees the other's heartbeat (logged once
after a boot), and a full call with a room key.

## 12. Service USB: not wired yet

Three USB-C breakouts in the bottom of the box, one per computer, are not wired. Each gets D+, D− and GND of its
computer, **never VBUS** (the computers run on PoE, and USB power on top would feed the rail backwards), and only then
the breakouts are potted.
