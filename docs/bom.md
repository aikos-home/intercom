# What to buy (bill of materials)

State: 20 October 2026, for the v3 box as it is built and running on the desk. Prices from the first edition
(24 September 2026) are kept where they were read off a product page; everything else has no price here. Parts marked
**later** are not built in yet: do not buy those blind.

Parts marked **measure** have dimensions the maker does not publish. The drawings in
[hardware/parts](../hardware/parts/) show what is known and what still has to be measured.

## Indoors: network and power

| Qty | Part | Why | Notes |
|---|---|---|---|
| 1 | PoE switch port, 802.3af or better | data + power down one cable | put the switch on a UPS |
| 1 | Ubiquiti ETH-SP-G2 surge protector | protects the house network from the outdoor cable | **must be earthed by an electrician**; datasheet lists 802.3af only |
| 1 | Short patch cable | switch → surge protector | |

## Through the wall

| Qty | Part | Why | Notes |
|---|---|---|---|
| 1 | Ready-made outdoor Cat6 cable, goobay **55432** (10 m) | the one cable | solid copper AWG 24/1, U/UTP, double PE jacket, UV-resistant, -40 to +75 °C, outer Ø 6.0–6.6 mm; about €11–13. **Not** goobay 94389: almost the same title, but copper-clad aluminium |
| 1 | Split cable gland **M20** for a 6–8 mm cable: OBO V-TEC TB20 06-08 (with split lock nut), or PFLITSCH USG 22053 PC + lock nut 1420/220 GGM + sealing insert UFE 53p8 | the moulded plug goes through, then the gland seals | the v3 box has a Ø20.5 mm hole for it |

## The three computers

| Qty | Part | Why | Notes |
|---|---|---|---|
| 1 | Waveshare ESP32-S3-ETH + plug-on **PoE Module (B)** | doorbell computer, wired; its PoE module feeds the whole box with 5 V | about €25–32; USB-C, so no serial adapter. Pin headers come loose and must be soldered. The module has no published temperature range (see the build log) |
| 1 | ESP32-S3-N16R8 dev board (silkscreen "HW678") | talk computer, on Wi-Fi | the WT32-ETH01 planned first is **not** recommended: see [`firmware/bell/`](../firmware/bell/README.md#why-not-the-wt32-eth01) |
| 1 | LilyGO T5-4.7-S3 **Touch** (SKU H716) | screen computer + 4.7" e-paper, 960 × 540 | about €55 at OpenELAB; several marketplace listings with a touch photo are **not** touch versions. Touch chip on ours: GT911 at I²C 0x5D, which ESPHome supports (check yours with `tools/touch_scan.py`). Arrives loose: the panel is folded onto the board by the buyer |

There is **no separate PoE splitter and no 12 → 5 V converter** in the v3 box: the PoE module carried everything
including the heater on the desk (9.37 W at the port). An industrial splitter rated down to −40 °C stays the
fallback if the module ever fails in frost.

## Distribution and wiring in the box

| Qty | Part | Why | Notes |
|---|---|---|---|
| 1 | Perfboard 30 × 70 mm, 10 × 24 holes, plated, with 4 corner holes | 5 V, 3.3 V and ground rails, button-line circuit, the box's climate sensor | the v3 box holds it on a printed clip socket; parts on it at most 10 mm high |
| – | Silicone-insulated stranded wire, 0.34–0.5 mm² (power) and 0.14–0.25 mm² (signals) | everything is soldered, nothing is clamped | thinner wire breaks when the parts move to a new box; leave 10–15 cm reserve in every wire |
| – | Heat shrink, tape flags for numbering, hot glue | insulation, labels, strain relief at the board edge | |
| 1 | USB-C breakout ×3 (data lines only) | service ports in the bottom, one per computer | **later**: D+, D− and GND only, the V pad stays free; solder the wires before potting |

## Audio

| Qty | Part | Why | Notes |
|---|---|---|---|
| 1 | INMP441 I²S MEMS microphone module | voice at the door | 3.3 V only; measured Ø13 × 2.53 mm; the sound hole is centred on the smooth side (no components), which faces the front |
| 1 | Adafruit MAX98357A I²S amplifier | drives the speaker | measured 20 × 20 mm, 12.2 mm high. GAIN open (9 dB), speech capped at −6 dB in the firmware. Its GND needs a solid connection: a loose ground distorted every sound |
| 1 | VISATON K 40 SQ, 8 Ω, IP65/67 front | speaker behind the grille | 40 × 40 mm, Ø35 cut-out; datasheet 11.5 mm deep, 4 × Ø3.4 on 32 × 32, measured 12 mm high and Ø3.6 on 32.4; about €5.50 |
| – | Closed-cell foam rubber, 2 mm | gasket between speaker and grille block | 40 × 40, Ø35 hole in the middle, 4 × Ø3.6 on 32.4 |
| 1 | ePTFE membrane Ø12 + 2 gaskets 10/13 × 1 mm | keeps water out of the mic holes | in the mic pocket, in front of the microphone |

## Sensors

| Qty | Part | Why | Notes |
|---|---|---|---|
| 1 | SHT31-D module | outdoor temperature and humidity, in its own chamber | measured 13.22 × 10.5 mm, hole Ø3; I²C 0x44 |
| 1 | BME280 module (GY-BME280, 6 pins) | temperature, humidity and pressure of the box air, on the distribution board | many "BMP280" boards look the same and have no humidity: check the chip ID (0x60) |
| 1 | HLK-LD2410C 24 GHz radar module | presence in front of the door, behind the grille | 5 V, UART at 3.3 V, to the screen computer; **firmware later** |

## Heater and light

| Qty | Part | Why | Notes |
|---|---|---|---|
| 1 | Adafruit 1481 heating pad, 5 V (about 5 W) | keeps the e-paper above 0 °C | sits between the panel and its board; load-tested on the PoE module. Its thin leads make no contact in a lever clamp: crimp them to thicker wire. **Connected later** |
| 1 | Logic-level N-MOSFET, fully on at 3.3 V gate drive | switches the heater from a 3.3 V pin | **later**, type not chosen. The opto-coupled FR120N modules sold for this do not switch properly from a 5 V supply |
| 1 | Thermal fuse 73 °C | one-shot overheat cut-off in series with the heater | soldering heat can blow it: crimp the leads |
| 1 | COB LED strip, 5 V, addressable (WS2812B type), 10 mm wide, e.g. BTF-LIGHTING FCOB | light under the roof | **later**, not chosen. Under the roof there is room for 10 mm × 57 mm or 5 mm × 66 mm. RGBW types at 12 V (WS2814) do not fit |
| 1 | SN74AHCT125N (DIP-14) | lifts the 3.3 V LED data to 5 V | **later**, on the distribution board |
| – | 1000 µF / 25 V low-ESR capacitor | at the LED strip | **later** |

## Button line

| Qty | Part | Why | Notes |
|---|---|---|---|
| 1 | A plain (dumb) brass push button, no electronics | the doorbell | the prototype uses a Ø48.5 mm ring, sealed with an O-ring 26 × 2 mm |
| 2 | 10 kΩ resistor | pull-up (on the distribution board) + end-of-line (soldered across the button contacts) | the end-of-line one must sit at the button, or a cut wire reads as idle |
| 1 | 1 kΩ resistor, 1 × 100 nF ceramic capacitor ("104") | series resistor and filter, on the distribution board | |
| – | Adhesive-lined heat shrink | seals the joint behind the button | |

## Enclosure (v3 box)

Everything below is for the printed v3 box; the full list with the step where each part goes in is in the
[print and assembly guide](../hardware/v3/). The final front is a steel sheet with a brass sheet on top; in v3 both
are printed stand-ins, and the metal is **not ordered yet**.

| Qty | Part | Why | Notes |
|---|---|---|---|
| ~0.5 kg | PETG | box and all printed parts | a Bambu Lab A1 prints everything; the box needs a print pause for the counter-strips |
| – | White PLA | diffuser under the roof | |
| 8 | M3 heat-set inserts (hole Ø4.0 × 6) | clamp ring, plate supports, button disc, USB cover | |
| 4 | Wood screws 4.0 × 30–35, countersunk (head Ø8, 90°) | box onto the door frame | the heads must sit flush: the computer carrier slides over them |
| 2 + 2 | M3 × 14 button head (ISO 7380) + O-rings 3 × 1.5 | speaker clamp ring, from the front | |
| 2 | M3 × 8, head at most Ø6 × 3 | display carrier plate | |
| 18 + 18 | M3 × 10 countersunk (ISO 14581, Torx) + O-rings 3 × 1 NBR | the steel sheet into the counter-strips | in PETG only hand-tight |
| 4 | M3 × 4 countersunk | the brass onto the steel | × 6 is too long |
| 2 | M3 × 8 button head, security Torx (pin) | USB cover | |
| – | Double-sided adhesive foam, 2 mm, non-conductive | under the doorbell computer | |
| ≥ 10 | Cable ties, 3.6 mm wide | the cable in an S-curve along five eyelets, five more eyelets on the wall | |
| – | Potting resin, neutral-cure silicone, superglue, hot glue | USB field, seals, glued parts (the radar frame is held by hot glue) | acetic-cure silicone corrodes brass |

## Tools and consumables

Soldering iron, solder with flux, a multimeter with a beep test (used before every first power-on), side cutters,
a crimper for butt connectors, Kapton tape, isopropyl alcohol, and a real USB-C data cable for flashing the S3 boards.

## Optional

| Qty | Part | Why |
|---|---|---|
| 1 | Home Assistant Voice PE (+ USB-C 5 V / 3 A supply, not included) | a chime inside the house |

## Not needed any more (so you do not buy them by mistake)

- A PoE splitter and a 12 → 5 V converter (the doorbell computer's PoE module does it), lever clamps and breadboards in
  the box (everything is soldered).
- A power supply in the technical room, passive PoE injector sets, a separate DC cable.
- Field-installable RJ45 plugs and cable rolls: the ready-made outdoor cable replaces them.
- A switch inside the box: Wi-Fi from the doorbell computer reaches the other two centimetres away.
- The pressure vent of the earlier box versions: v3 has none.
