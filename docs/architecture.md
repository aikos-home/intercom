# Architecture

State: 20 October 2026. Prototype stage: everything is built into the printed v3 box and runs on the desk, nothing is
installed at the door yet. How the box is wired, pin by pin: [`firmware/WIRING.md`](../firmware/WIRING.md).

The interactive version of this page is the [explorer](../explorer/). It shows every part, wire,
joint and solder spot, and walks through what happens on a ring, in winter, at dusk and during a call.

## The idea in one picture

```
 house network                technical room               wall          box on the door frame              front
 ─────────────                ──────────────               ────          ─────────────────────              ─────
 Home Assistant ── LAN ── PoE switch (on a UPS) ── surge ── one outdoor ── split ── doorbell computer ── button line, climate sensors
       │                                          protector  Cat6 cable    gland     + PoE module          │
       │                                          (earthed)                            │ 5 V rail ─────────┤
       │                                                                               │                   ├── talk computer ── mic, amplifier, speaker
       │                                                                               │ Wi-Fi "aikos"     └── screen computer ── e-paper touch, radar
       └── room keys, phone, transcription ◄── LAN ◄── bridged by the doorbell computer ┘
```

- **One cable.** A single outdoor Cat6 cable carries data and power (PoE, about 48 V) from the switch into the box.
  There is no power supply at the door and no switch in the box.
- **Three small computers, each with one job.** They share the 5 V rail and ground. The doorbell computer is the only
  wired one: it runs its own Wi-Fi "aikos" for the other two and bridges it into the LAN.
- **Four supervision wires** between the doorbell and the talk computer: a heartbeat each way and a reset line each
  way, so each can restart the other if it hangs.

| Computer | Board | Link | Job |
|---|---|---|---|
| Doorbell computer | Waveshare ESP32-S3-ETH (W5500) with its plug-on PoE Module (B) | wired | button line, climate sensors, Wi-Fi "aikos", 5 V for the box; later the heater and the light |
| Talk computer | ESP32-S3-N16R8 dev board ("HW678") | Wi-Fi "aikos" | microphone, amplifier, two-way talk |
| Screen computer | LilyGO T5-4.7-S3 Touch (H716) | Wi-Fi "aikos" | 4.7" e-paper touch screen behind the window; later the radar |

Why three and not one: the bell is the one function that must never fail. A crash or an update in the audio code
cannot take it down when it runs on its own board. The e-paper panel is a parallel panel that needs its own driver
board anyway.

## The ring path (the part that must always work)

1. The brass button sits on a **supervised line**: 10 kΩ pull-up to 3.3 V, 1 kΩ series resistor, 100 nF to ground
   (all three on the distribution board), and a 10 kΩ end-of-line resistor soldered straight across the button.
   That gives three distinct voltages on an analog (ADC1) input:

   | State | Voltage (bench, with the ESP's internal pull-up on) |
   |---|---|
   | idle | 2.03 V (1.99 V in the box) |
   | pressed | 0.34 to 0.47 V (a half-closed contact: 0.6 to 0.9 V) |
   | wire cut | 3.18 V |

   A cut or corroded wire is reported instead of going silent. The pull-up exists because a floating input on the
   first prototype produced 134 phantom rings in 15 minutes.
2. The doorbell computer samples the line every millisecond. A press starts below 1.30 V and ends only above 1.60 V
   and after 60 ms released, so a wobbly contact is still one press. Every change goes to Home Assistant at once
   (ESPHome's default 100 ms batching is off). Details: [`firmware/bell/`](../firmware/bell/).
3. The press goes out **twice at the same moment**: to Home Assistant, which notifies the phone, and directly to the
   room keys and the door screen over encrypted UDP, so the gong sounds even while Home Assistant restarts. Each
   receiver rings once per press, whichever path arrives first.
4. Nothing on the ring path waits for the screen, the talk computer or Wi-Fi. Measured on the bench: storm ringing
   with 20 presses in 2.7 s arrived 20 of 20 everywhere; from the press to the drawn ring page 1.4 s.

## Power

| Stage | Detail |
|---|---|
| Switch port | PoE (802.3af), the switch on a UPS so a short power cut does not stop the bell |
| Surge protector | Ubiquiti ETH-SP-G2 in the technical room, before the outdoor cable; only works when earthed (electrician's job) |
| PoE to 5 V | the doorbell computer's plug-on **PoE Module (B)**; its 5 V (header pin 40, VBUS) feeds the whole box |
| Distribution | a 30 × 70 mm perfboard: 5 V, 3.3 V and ground rails, soldered, no clamps |
| 3.3 V | from the doorbell computer (pin 36) for the button line and the two climate sensors; the talk computer makes its own for the microphone |
| Heater | 5 V pad, about 5 W, between the e-paper panel and its board. **Not connected yet:** it waits for a logic-level MOSFET on the distribution board and the firmware that switches it |

Measured at the switch port: **4.13 W** with everything idle on the bench (the screen alone about 1.75 W), **4.82 W**
with everything running in the box (20 October, heater not connected), **9.37 W** with the heater on (bench, 7 October). The 5 V rail sags from 5.0 to 4.8 V under the heater; the USB floor is 4.75 V, so the
heater and the light will need a shared limit. A separate industrial PoE splitter is not needed for this load; it
stays the fallback if the module fails in frost (it has no published temperature range, and a cold start in frost
was not tested).

## Winter

The e-paper panel is rated 0 to +50 °C; the box sees frost. Two sensors on one I²C bus of the doorbell computer:

- **SHT31-D** in its own small chamber at the bottom of the box, with openings to the outdoor air: outdoor
  temperature and humidity.
- **BME280** on the distribution board: temperature, humidity and pressure of the box air.

The heater is planned to **fail cold**: off at boot, off if a sensor fails, off during calls, a firmware cut-off
around 40 °C, and a 73 °C one-shot thermal fuse in series as the last line of defence. Below about +2 °C the screen
does not refresh. None of the heater control is written yet.

## Two-way talk

- **Voice link:** the shared library `aikos_voice` from [aikos-home/aikos](https://github.com/aikos-home/aikos)
  (tag `voice-v2.1.0`). The door is the arbiter of a call. A call starts when the visitor taps "Sprechen" on the
  screen after a ring, or when someone indoors holds the button of a room key. Room keys and the screen talk to the
  door directly over encrypted links; Home Assistant is not in the audio path.
- **During a call** the door microphone stays open. Toward the room keys it is muted while the door speaker plays, so
  the visitor does not hear themselves. A call ends after 10 s of silence, or after 5 minutes at the most.
- **Transcripts:** a copy of the door audio goes to a transcription server in the house network. What both sides say
  appears as chat bubbles on the door screen.
- **Audio parts:** INMP441 MEMS microphone, MAX98357A I²S amplifier (GAIN open = 9 dB), VISATON K 40 SQ speaker, clamped with a
  gasket behind the grille. Speech is capped at −6 dB in the firmware; the door never chimes.
- **Privacy:** the microphone opens only after a visitor presses something or someone indoors holds a room key, and
  the screen says so. Nothing is recorded. (In Germany, § 201 StGB makes recording the spoken word without consent a
  criminal offence.)

Not designed yet: push-to-talk into speakers inside the house, and voice messages delivered to a phone.

## Self-healing

A box in the wall must never need hands:

- A firmware counts as good only after 2 minutes healthy; until then the bootloader can roll back.
- Five failed boots in a row start a safe firmware (doorbell computer: its own plain bell in the factory partition).
- Runtime guards restart a stuck network; the doorbell and the talk computer watch each other over the four
  supervision wires.
- The last resort is a power cycle of the switch port, from Home Assistant.

## Mechanics (v3 box)

- **Box:** 3D-printed in PETG, 92 × 252 × 60 mm, surface-mounted on the solid wooden door frame with four countersunk
  wood screws. Two counter-strips are laid into channels during a print pause and the collar is printed over them;
  the 18 screws of the front bite into them (printed stand-ins in v3, stainless steel later).
- **Inside, front to back:** the display on a carrier plate (hung on two tongues, two screws at the bottom; the
  amplifier sits on its back), behind it one carrier for the doorbell and talk computers that slides out downwards,
  and the distribution board on a clip socket at the bottom.
- **Front:** a steel sheet with the display window, screwed onto the counter-strips with O-rings under every screw,
  and the brass sheet on top. In v3 both are printed stand-ins of the same shape; the metal is not ordered yet.
- **Grille block** behind the speaker grille: the speaker is clamped from the front with a foam rubber gasket, and
  the radar sits in a glued frame behind the grille.
- **Cable entry:** a split M20 cable gland, so the cable with its moulded plug goes through; the cable is tied to
  five eyelets in an S-curve as strain relief.
- **Service:** three USB-C breakouts in the bottom, data lines only, one per computer (planned, not wired yet).
- **No camera. Ever.** This is a design rule, not an open question.

Drawings, STL files and the print and assembly guide: [`hardware/`](../hardware/).

## Open points

The light under the roof (COB strip and level shifter), the heater switch and its firmware, the radar firmware, the
service USB ports, a cold start in frost, a water test, and the metal front. The roadmap: [roadmap.md](roadmap.md).
