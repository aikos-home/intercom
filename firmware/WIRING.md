# Wiring: the door box, as built

This is the wiring **as it was soldered into the printed v3 box between 16 and 20 October 2026**, not a plan. It
replaces the breadboard wiring of 4 October (still in the git history of this file); the pins on the three computers
did not change, only how they are connected. Each section says how it was checked.

The sheets the box was soldered from, in German, are in [`docs/wiring-sheets/`](../docs/wiring-sheets/):
[round 1, the distribution board](../docs/wiring-sheets/kasten-runde1-verteiler.svg) and
[round 2, the computer carrier](../docs/wiring-sheets/kasten-runde2-traeger.svg). Where the box differs from a sheet,
this page says so.

| Computer | Board | Firmware |
|---|---|---|
| **Bell** | Waveshare ESP32-S3-ETH + plug-on *PoE Module (B)* | `bell/aikos-intercom-bell-bridge.yaml` |
| **Talk computer** | ESP32-S3-N16R8 dev board, silkscreen "HW678" | `talk_computer/aikos-intercom-talk.yaml` |
| **Screen** | LilyGO T5-4.7-S3 Touch, board "Screen-4.7-S3 V2.4" | `aikos-intercom-screen.yaml` |

```
switch port (PoE) ══ Ethernet ══ BELL (RJ45 + PoE module)
                                   │ pin 40 VBUS, pin 33 GND ── distribution board ──┬── screen (VBUS) ── radar
                                   │ pin 36 3V3, pin 25 button node, I2C 31/34 ──────┤── amplifier ── speaker
                                   │                                                  ├── brass button (+ end-of-line 10 kΩ)
                                   │                                                  └── SHT31 (outdoor chamber), BME280 (on the board)
                                   ├── 5 V, GND and 4 supervision wires ── TALK COMPUTER ── microphone
                                   │                                                    └── I2S ── amplifier
                                   └── Wi-Fi "aikos" for the talk computer and the screen
```

## Rules that broke boards or cost hours

- **Power off before every wiring change:** switch the PoE port off, then touch wires, then power on. Moving a signal
  wire under power once took the talk computer off the network until a power cycle; a live re-plug of the 5 V
  jumpers killed a talk board.
- **Never USB and PoE at the same time** on the bell, the talk computer or the screen. They all hang on the same
  5 V rail, so a USB cable on any of them can feed the others backwards.
- **Nothing clamped, nothing plugged.** Two of the bench faults were loose breadboard contacts (an amplifier ground,
  the button line's pull-up). In the box every joint is soldered.
- **Beep-test before the first power-on.** A single stray strand at the BME280 shorted 3.3 V to ground; the beep test
  found it, the power never saw it.
- **Reserve in every wire.** The computer carrier slides 40 mm down and then out to the front, the display plate comes
  out to the front, and the display comes off with the front sheet. Every wire has 10–15 cm more than its path needs,
  so a part can be taken out, or moved to the next box, without cutting anything.

Wires: power 5 V and GND in thick stranded wire, signals in thin stranded wire (the prototype uses 0.05 mm² for the
signals; 0.14 mm² is easier to handle). Each wire carries a tape flag with its number at both ends.

## 1. The distribution board

A 30 × 70 mm perfboard with 10 × 24 plated holes, on a printed clip socket at the bottom of the box, components to the
front. Columns A–J from the left, rows 1–24 from the top (the top points to the bell). Under the board there are only
3 mm, so every lead is cut to 1 mm at the back.

**Rails and strips** (bare wire on the back, soldered at every hole):

| Strip | Holes | Net |
|---|---|---|
| GND | A1–A24 | ground |
| 5 V | B1–B7 | 5 V from the bell's PoE module |
| 3V3 | J9–J24 | 3.3 V from the bell |
| button node | E10–E13 | the bell's analog input |
| button line | I13–I15 | toward the button |
| SCL | F16–F20 | I²C clock |
| SDA | G16–G20 | I²C data |
| BME VCC | D19–D20 | |
| BME GND | E18–E20 | |

**Parts:**

| Part | Holes | What |
|---|---|---|
| R1 10 kΩ | E11–J11 | pull-up of the button node |
| C1 100 nF | E12–A12 | filter on the button node |
| R2 1 kΩ | E13–I13 | series resistor toward the button |
| BME280 (GY-BME280, 6 pins) | header in D20–I20: VCC, GND, SCL, SDA, CSB, SDO | chip to the front, the module hangs down over rows 21–24. CSB and SDO are soldered but connected to nothing (I²C address 0x76) |
| bridge | D19 → J19, insulated, on the front | BME280 VCC to 3.3 V |
| bridge | E18 → A18, insulated, on the front | BME280 GND to ground |

C1–J7 stay free for the heater switch and the LED level shifter.

**16 wires leave the board:**

| # | Hole | Net | Length | Other end |
|---|---|---|---|---|
| 1 | A1 | GND | 30 cm, thick | bell header pin 33 (GND) |
| 2 | B1 | 5 V | 30 cm, thick | bell header pin 40 (VBUS), together with wire 17 |
| 3 | A3 | GND | 30 cm, thick | screen, edge-row hole 3 (GND) |
| 4 | B3 | 5 V | 30 cm, thick | screen, edge-row hole 1 (VBUS) |
| 5 | A5 | GND | 20 cm, thick | amplifier GND |
| 6 | B5 | 5 V | 20 cm, thick | amplifier Vin |
| 7 | J9 | 3V3 | 30 cm | bell header pin 36 (3V3) |
| 8 | E10 | button node | 30 cm | bell header pin 25 (GPIO1) |
| 9 | I15 | button line | 15 cm | button, one terminal |
| 10 | A15 | GND | 15 cm | button, the other terminal |
| 11 | F16 | SCL | 30 cm | bell header pin 31 (GPIO18) |
| 12 | G16 | SDA | 30 cm | bell header pin 34 (GPIO17) |
| 13 | J17 | 3V3 | 15 cm | SHT31 VIN |
| 14 | A17 | GND | 15 cm | SHT31 GND |
| 15 | F17 | SCL | 15 cm | SHT31 SCL |
| 16 | G17 | SDA | 15 cm | SHT31 SDA |

Differences from sheet 1: wires 5 and 6 are thick, wire 9 is yellow, and wires 7–16 are 0.05 mm² (the sheet says
"nothing under 0.14").

Checked on 17 October, without power, by beep test: no continuous beep between GND, 5 V and 3V3 or between SCL and
SDA; every GND, 5 V, 3V3, SCL and SDA wire beeps through to its strip and to the BME280 pins; wires 13–16 beep
through to the SHT31 pads.

## 2. The computer carrier: bell ↔ talk computer

The bell and the talk computer sit on one carrier, so the wires between them never move when the carrier slides out.
Seen from the front: talk computer at the top left, bell at the right below it, all USB sockets pointing down. The
bell's row with VBUS (pins 21–40) lies on the outside right, its row with pins 1–20 faces the talk computer.

| # | Bell | Talk computer | What |
|---|---|---|---|
| 17 | pin 40 VBUS | 5Vin | 5 V, thick (shares pin 40 with wire 2) |
| 18 | pin 13 GND | GND (last pin of the 3V3 row) | ground, thick |
| 19 | pin 11 GPIO40 | RST | the bell can reset the talk computer |
| 20 | pin 12 GPIO39 | 8 | the bell's heartbeat |
| 21 | pin 14 GPIO38 | 18 | the talk computer's heartbeat |
| 22 | pin 30 RUN (CHIP_UP) | 9 | the talk computer can reset the bell |

The supervision logic is in `components/aikos_peer_guard`: each computer toggles its heartbeat pin once per second; if
the other one's heartbeat stops for 30 s, it pulls the other's reset line low for 200 ms (at most 3 times an hour, never
before it has seen a heartbeat, never in the first 2 minutes).

⚠️ Bell pin 37 (3V3_EN) is **not** a reset: pulling it low switches the bell's 3.3 V off. Nothing on it, not even
solder. Also free on the talk computer: 0, 45, 46 and 3 (strapping pins).

The distribution wires land on the bell's outer row: 1 → pin 33, 2 → pin 40, 7 → pin 36, 8 → pin 25, 11 → pin 31,
12 → pin 34.

Checked on 20 October by beep test, all six; no continuous beep between VBUS, 3V3 and GND on either board.

## 3. Talk computer → amplifier and microphone

| # | Talk computer | Goes to |
|---|---|---|
| 23 | 15 | amplifier BCLK |
| 24 | 16 | amplifier LRC |
| 25 | 17 | amplifier DIN |
| 26 | 3V3 (top pin of the 3V3 row) | microphone VDD |
| 27 | 6 | microphone SD |
| 28 | 1 | microphone SCK |
| 29 | 2 | microphone WS |
| 30 | GND (TX row, second to last) | microphone GND |

Lengths: 23–25 20 cm (the amplifier sits on the back of the display plate), 26–30 35 cm (the microphone sits at the
bottom right of the front). Checked by beep test on 20 October, all eight.

**Microphone (INMP441):** VDD, GND, SD, SCK and WS from wires 26–30; L/R bridged to GND on the microphone itself (left
channel, as in the firmware). The smooth side with the sound hole lies on the gasket in the mic pocket.

**Amplifier (MAX98357A):** LRC, BCLK and DIN from wires 24, 23 and 25; GND and Vin from the distribution board (wires 5
and 6); GAIN and SD free (9 dB, always on). The speaker (VISATON K 40 SQ, 8 Ω) hangs on the screw terminal over a
twisted pair of about 20 cm.

## 4. Button, climate chamber, screen, radar

**Button:** wires 9 and 10 go into the button's two screw terminals. The 10 kΩ end-of-line resistor sits in the same
terminals, one leg under each screw, with heat shrink over it. It has to sit at the button: anywhere else a cut wire
would read as "idle".

**SHT31:** wires 13–16 run through the cable hole of the chamber lid to the four pads VIN, GND, SCL, SDA. The board sits
on the lid's pin with its print toward the lid; the lid is glued onto the chamber walls and its cable hole sealed with
silicone. The chamber has three small openings to the outdoor air.

**Screen (LilyGO T5-4.7-S3, board V2.4):** the board has an unpopulated 2 × 20 hole row along one long edge; the row
right at the edge reads VBUS · VBUS · GND · RX · TX … (LilyGO schematic V2.4, connector P8).

| Edge-row hole | Goes to |
|---|---|
| 1 · VBUS | wire 4 (5 V from the distribution board) |
| 2 · VBUS | radar VCC (connected to hole 1 on the board) |
| 3 · GND | wire 3 (GND from the distribution board) |
| a GND hole of the row | radar GND |
| RX | radar TX |
| TX | radar RX |

Solder from the component side and cut flush on the other side: the e-paper glass lies there. The screen's own USB-C
stays unplugged while PoE is on.

**Radar (HLK-LD2410C):** in its glued frame behind the grille, four thin wires of about 30 cm to the screen as above;
OUT stays free. It runs on 5 V, its UART on 3.3 V. **No firmware yet:** the screen's RX/TX holes are the chip's
UART0, which the firmware still uses for its log; the log has to move to USB first.

**Heater (5 V pad between the panel and its board):** **not connected.** Its leads are extended (crimped, not clamped),
insulated at the ends and parked at the distribution board, until a logic-level MOSFET on the board (C1–J7) and the
firmware that switches it exist.

**Service USB (three breakouts in the bottom):** not wired yet. They get D+, D− and GND of one computer each, never
VBUS, before they are potted.

## 5. First power-on in the box (20 October 2026)

Before: beep test without power, no continuous beep between bell VBUS and GND, bell 3V3 and GND, talk 5Vin and GND (the
screen's VBUS against GND chirps briefly: its capacitors charging). The front sheet was off.

After switching the PoE port on:

| What | Result |
|---|---|
| Network | all three computers answer; the talk computer's Wi-Fi at −29 dBm |
| Button line, idle | 1.99 V (bench: 2.02 V); "line cut" and "line shorted" both off |
| Two presses | counted by the bell, received by the screen both directly and via Home Assistant |
| Supervision wires | no reset in either direction |
| Microphone | delivers audio, noise floor −54.9 dB |
| Speaker | a tone sweep and a spoken message played clean |
| Power at the switch port | 4.82 W (heater not connected) |

Not measured yet in the box: the line voltage while pressed, the resistances of R1 and R2 as a number, the climate
sensors (their firmware, bell 0.3.23, is written but not yet on the device), and a full call with a room key and the
transcript.
