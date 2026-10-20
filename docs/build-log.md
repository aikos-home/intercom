# Build log

What happened, in order, including the dead ends. Dates are 2026.

## August: a doorbell that works

- The old doorbell had been dead for a long time: its button's circuit board had died from rain.
- First version: a plain brass button on an existing two-wire cable into an ESP32 indoors,
  running ESPHome, with a push notification through Home Assistant. No chime.
- **Lesson:** a floating input pin on a long cable acts as an antenna. At one point it
  produced 134 phantom rings in 15 minutes. The fix became the supervised line: pull-up,
  series resistor, filter capacitor and an end-of-line resistor at the button, so idle,
  pressed and a cut wire give three different voltages.
- **Lesson:** a component only does something if current can flow *through* it. A resistor
  plugged into an empty breadboard row changed nothing, and only the multimeter showed it.

## 17 September: from doorbell to intercom

- New goal: a small e-paper screen at the door, later speech in both directions.
- **Hard rule from day one: no camera at the door, ever.**
- Front design in five rounds of dimensioned drawings (generated in Python, true scale):
  - v2: portrait screen, one button, speaker grille;
  - v3: flush in the wall, a separate brass roof cap, a cable pipe bending into the wall;
  - v4: back to one folded sheet, with a brass cable pipe rising in front of the wall (rejected);
  - v5: no pipe, 100 × 260 mm, LED band in the fold with a quarter-round diffuser.

## 18 September: CAD

- The front sheet, the in-wall box, a carrier plate and the diffuser modelled in FreeCAD,
  driven by scripts. First prints of the sheet (in two parts, it is taller than the print bed)
  and the box.
- The speaker changed from a 3 W waterproof part to the smaller VISATON K 40 SQ: it is quieter on
  paper (0.5 W) but louder in practice (82 dB vs 74 dB at 1 W / 1 m). Sensitivity beats wattage.

## 24 September: parts, architecture, explorer

- Most parts arrived and were identified (some sold under vague names: an opto-coupled MOSFET
  module turned out to be usable because its optocoupler drives the gate from 12 V).
- Architecture settled:
  - **one** ready-made outdoor PoE cable instead of three cables plus a power cable;
  - three computers: a wired doorbell computer, a talk computer on WiFi, a screen computer
    on WiFi;
  - two-way talk via the community VoIP Stack for ESPHome, with walkie-talkie mode as the
    fallback.
- The [explorer](../explorer/) was built to make the whole system understandable, including
  every wire and every solder joint.

## 25 September: a roadmap

- Eight milestones from the bench to the door, with a separate track that proves the box can be
  sealed before the real brass plate is bought. See the [roadmap](roadmap.md).

## 29 September: the screen computer

- The LilyGO T5-4.7-S3 Touch arrived. The sources disagreed about its touch chip: LilyGO's wiki
  says GT911, their own driver code expects an L58. Only the GT911 has an ESPHome driver.
- A scan of the board's I²C bus answered it: **GT911 at address 0x5D** (it answers "911" when
  asked for its product id), plus the PCF8563 clock chip at 0x51. The script is
  [`tools/touch_scan.py`](../tools/touch_scan.py); it runs on MicroPython.
- **Lesson:** read out the whole flash before flashing anything. The factory program went into a
  16 MB backup first, so it can be put back byte for byte.
- Measured with a caliper, because LilyGO publishes none of it: seven mounting holes, the touch glass,
  the visible picture area and the folded stack ([numbers](../hardware/parts/lilygo-t5-s3-touch-measured.md)).
- **Surprise:** the screen arrives loose on two ribbons and is folded onto the board by the buyer.
- **Lesson:** a datasheet's active area is not what you see. The glass's white print hides almost 1 mm
  on every side, and the brass window has to be sized to what is visible.

- The screen runs ESPHome. The community driver wiped the whole panel black and white before every
  picture: two seconds of flashing, which at a door looks like a fault. The driver in
  [`firmware/`](../firmware/README.md#screen-computer) now moves each pixel only by the difference between its
  old and new grey, all changed rows in one sweep, in a background task so touch is never ignored.
  A tap changes the picture in about half a second, without a flash.
- **Lesson:** lightening a pixel also fades its neighbours. Thin lines next to changed pixels vanished
  until the driver re-darkened them.

- A demo with eight test pages settled what the screen can show: text from 32 px at a normal
  distance, about 8 distinguishable greys, QR codes at any size ([findings](screen-ux.md)).
- **Lesson:** a flash-free change to another page always left the previous page behind as a faint
  trace, however carefully the old picture was undone. One short black-white flash (about a second)
  clears it. So the screen flashes briefly on a real page change and stays calm within a page.
- **Lesson:** e-paper must be driven balanced. A test animation that lightened pixels more than it had
  darkened them left a faint ring after about a hundred frames that even a flash did not remove at once.

## 30 September – 4 October: three computers on one cable

- The doorbell computer moved boards. The WT32-ETH01 booted once, then always started in download
  mode: its IO0 is both the boot-mode pin and the Ethernet clock input, and the oscillator holds it
  low. Pull-ups of 10 kΩ and 1 kΩ did not win, and a doorbell must restart on its own after a power
  cut. The Waveshare ESP32-S3-ETH took over: no clock on a boot pin, USB-C, PoE via a plug-on module.
  It started on the first try and Home Assistant found it by itself.
- **Lesson:** read the boot line before blaming the software. `boot:0x3` means the chip never ran any
  program at all; the [probe scripts](../tools/wt32/) show it without unplugging anything.

- The bell rings, on the bench: brass button, supervised line on a breadboard, firmware in
  [`firmware/bell/`](../firmware/bell/), updates over the network. Slow presses 10 of 10; storm ringing
  filmed in slow motion, 14 of 15 counted, and the 15th only grazed the contact for 1 ms.
- **Lesson:** ESPHome collects API updates for 100 ms by default. Two quick presses inside one batch
  arrive as one, so storm ringing showed 2 of 5. Setting the batch delay to 0 fixed it.
- **Lesson:** a loose wire on an analog pin looks like a press, and a half-closed brass contact
  hovers right at a single threshold. The internal pull-up and a two-threshold hysteresis fixed both.
- Cable cut and short circuit are both reported, after 10 and 60 seconds.

- The box got its talk computer and its own Wi-Fi (1–4 October). All three computers now run on the bench from one
  PoE cable: the doorbell computer is the only wired one, runs the Wi-Fi "aikos" and bridges it into the LAN; the
  talk computer (microphone, amplifier, speaker) and the screen join it. Wiring: [`firmware/WIRING.md`](../firmware/WIRING.md).
- Two-way talk with the room keys runs through the shared voice library; the screen shows "Sprechen" after a ring,
  the call, and the transcripts.
- Self-healing for a box in the wall: a firmware counts as good only after 2 minutes healthy, 5 failed boots start a
  safe firmware (doorbell computer: its own, in the factory partition), runtime guards restart a stuck network, and
  the doorbell and talk computers watch each other over four wires and reset each other.
- **Lesson:** ESPHome's `safe_mode` marks the running firmware good on every orderly restart by default
  (`boot_is_good_on_shutdown`), which silently defeats the rollback. Off, and the guards restart without shutdown hooks.
- **Lesson:** a bridged Ethernet + Wi-Fi port stalled the bell until the task watchdog fired: the bridge's 16-entry
  forwarding table overflowed and every frame was flooded. 128 entries and all-multicast off fixed it.
- **Lesson:** after a bell restart the screen paired the new boot id with the old press number, counted a phantom
  press and then skipped the real ones. A new boot id now waits for its own press number.
- **Lesson:** on 4 October two faults were breadboard contacts. The amplifier's ground had no contact (distorted sound
  on every speaker, its 5 V read 4.4 V), and the button line's pull-up came loose (the line idled at 0.75 V instead of
  2.02 V, which reads as a held button). Beep-test the ground and supply path before blaming a part; in the box,
  solder or clamp.
- **Lesson:** moving a wire with the power on took the talk computer off the network until a power cycle, and two days
  earlier a live re-plug of the 5 V jumpers killed a board. Power off first, every time.
- Power at the switch port with everything idle: 4.13 W, of which the screen takes about 1.75 W.

## 4–14 October: tested end to end, and a heater on the PoE cable

- A test press without touching the button (an API action that holds the button state like a closed contact) made the
  whole ring path testable from a script. Storm ringing, 20 presses in 2.7 s: 20 of 20 at the doorbell computer, in
  Home Assistant and on the screen, over both of its paths. From the press to the drawn ring page: 1.4 s, 1.1 s of it
  the page-change flash.
- Door speech reached the screen as text 4 s after the visitor paused, but up to 21 s when the transcriber found no
  pause in the room noise. The transcriber's pause detection and echo cut were reworked on its side.
- The first chat bubble of a call flashes once: drawn without a flash over the grey placeholder, it left a ghost.
- **A fixed rule for the screen:** text is black on white or white on black, never on grey and never grey.
- The heater pad (5 V, about 5 W) ran on the doorbell computer's plug-on PoE module, together with everything else:
  **9.37 W** at the switch port, the 5 V rail at 4.8 V under load (5.0 V without), the module barely warm, no restart
  during seven rounds of calls with screen flashes and full-level gongs. So the one PoE cable carries the heater, and
  the industrial splitter is not needed for the load.
- Not tested: a cold start in frost. The module has no published temperature range. The riskiest moment is a start
  after a long power cut in frost; once running, the box heats itself. The fallback is the industrial splitter.
- **Lesson:** the heater's thin leads made no contact in a lever clamp, even with ferrules. Crimp thin leads onto a
  thicker wire before any clamp.
- **Lesson:** a firmware update that never got marked as good rolled back silently at the next restart: the 60 ms
  debounce of version 0.3.22 was never active. Check the running version after every update.
- The first doorbell (the ESP32 indoors from August) was retired.

## 12–20 October: the v3 box, wired inside

- The box went through versions v3.0 to v3.7 within a few days, each change a measured finding from the printed part:
  [`hardware/`](../hardware/). It is surface-mounted on the solid wooden door frame and 60 mm deep. The doorbell and
  talk computers share one carrier that slides out downwards, the display sits on a carrier plate held by two tongues
  and two screws, and the climate sensor for outdoor air has its own chamber.
- All wiring inside the box is soldered, with 10–15 cm of reserve in every wire so the parts can move to the next box
  without cutting anything. A small perfboard distributes 5 V, 3.3 V and ground and carries the button-line circuit and
  the box's climate sensor. Pin by pin: [`firmware/WIRING.md`](../firmware/WIRING.md).
- **Lesson:** a single stray strand at the climate sensor shorted 3.3 V to ground. The beep test found it before
  the power did.
- **First power-on in the box (20 October):** all three computers came up and joined the network, the button line
  idled at 1.99 V (2.02 V on the bench), two presses reached the screen over both paths, the supervision wires reset
  nobody, the microphone delivered audio, and a tone sweep and a spoken message played clean through the speaker.
- Still open in the box: the firmware for the two climate sensors (written) and the radar, the heater switch, the
  light under the roof and the service USB ports.

## Next

The plan from here is the [roadmap](roadmap.md): all hardware on the table, measure and
alpha-print the box, build the software on the bench, prove the box can be sealed, then a beta
box on the desk, a pre-release box and finally the door.
