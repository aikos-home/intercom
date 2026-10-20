# Klingelbox

**An open-hardware door intercom: a brass front beside the door, an e-paper touch screen,
two-way talk with the rooms, and one PoE cable. Built on ESP32, ESPHome and Home Assistant. No camera, ever.**

[Deutsch](README.de.md)

> Status: prototype. All electronics are soldered into the printed v3 box and have run in it since
> 20 October 2026, on the desk. The metal front is not ordered yet, and nothing is installed at a door.
> State of this page: 20 October 2026.

<p align="center">
  <img src="docs/images/intercom-render.jpg" width="330" alt="AI-generated concept render: a brushed brass door plate with a folded rain roof and a warm light band under it, a slotted speaker grille, a portrait e-paper screen saying Hallo! Bitte klingeln. with a QR code, engraved placeholder names and a round brass button">
  &nbsp;&nbsp;
  <a href="https://github.com/aikos-home/roomkey"><img src="https://github.com/aikos-home/roomkey/raw/main/docs/north-star.jpg" width="200" alt="AI-generated concept render of the RoomKey: a white light-switch frame with a portrait touch screen key in the middle and a soft amber glow"></a>
  <br><em>Target design: AI-generated concept renders (Google Gemini), not photos of built devices. The engraved names are
  placeholders. Right: its counterpart in the rooms, the <a href="https://github.com/aikos-home/roomkey">RoomKey</a>.
  Both are part of <a href="https://github.com/aikos-home">aikos</a>.</em>
</p>

<p align="center">
  <img src="hardware/front-sheet/layout-v5-referenz.png" width="520" alt="Front view and side section of the brass front: speaker grille, portrait e-paper screen, engraved names, round brass button, folded rain roof with a light band">
</p>

## What it is

- **A doorbell first.** A plain brass button on a supervised line: idle, pressed and a cut wire
  read as three different voltages, so a broken wire is reported instead of going silent. The
  ring reaches the phone before anything else happens at the door.
- **A screen at the door.** A 4.7" e-paper touch screen behind a window in the brass: greetings,
  notices, a QR code. It keeps its image without power and stays readable in sunlight.
- **Talk.** A microphone and a speaker behind the brass for two-way conversation with the
  [RoomKey](https://github.com/aikos-home/roomkey) touch keys in the rooms, and a live transcript of both
  sides on the door screen. Planned: voice messages and push-to-talk into the house.
- **One cable.** Data and power arrive over a single outdoor PoE cable. No power supply at the
  door, no switch in the box.
- **Local.** Everything runs on ESPHome and Home Assistant at home.
- **Private by design.** No camera. The microphone only opens after a visitor presses
  something or someone indoors holds a room key, and the screen says so. Nothing is recorded.

## Explore it

![The explorer: every part of the intercom from the house network through the wall into the box and the brass front, with colour-coded wires](docs/images/explorer.png)

The [explorer](explorer/) is an interactive map of the whole system: switch wire types on and
off, tap any part for what it is and why it was chosen, and follow walkthroughs of a ring, the
power path, winter heating and a call. Download
[`explorer/dist/klingelbox-explorer.html`](explorer/dist/klingelbox-explorer.html) and open it in
a browser. A hosted version is planned.

## How it works

Three small computers share one cable and one 5 V rail. The doorbell computer is the only wired one; it runs
a Wi-Fi of its own for the other two and bridges it into the house network.

| Computer | Board | Link | Job |
|---|---|---|---|
| Doorbell | Waveshare ESP32-S3-ETH + PoE Module (B) | wired | button line, climate sensors, Wi-Fi and 5 V for the box; later heater and light |
| Talk | ESP32-S3-N16R8 dev board ("HW678") | Wi-Fi | microphone, amplifier, calls |
| Screen | LilyGO T5-4.7-S3 Touch | Wi-Fi | e-paper touch screen; later the radar |

The bell runs on its own board, so a crash or an update in the audio code can never silence it. Details, power,
the winter heater and the box: [docs/architecture.md](docs/architecture.md).

## Repository

| Path | What |
|---|---|
| [`docs/architecture.md`](docs/architecture.md) | how it works, power, winter, talk, mechanics |
| [`docs/bom.md`](docs/bom.md) | what to buy, with the traps (fake "touch" listings, copper-clad cable) |
| [`docs/roadmap.md`](docs/roadmap.md) | the milestones from parts on the desk to the door, and the decisions still to lock in |
| [`docs/build-log.md`](docs/build-log.md) | what happened so far, including the dead ends |
| [`docs/family-app.md`](docs/family-app.md) | the planned self-hosted app for the household |
| [`hardware/`](hardware/) | the v3 box with all its printed parts, the print and assembly guide, the front, part drawings |
| [`explorer/`](explorer/) | the interactive map and its build |
| [`firmware/`](firmware/) | ESPHome firmware for all three computers: [doorbell](firmware/bell/), [talk](firmware/talk_computer/), screen (fast refresh, demo) |
| [`firmware/WIRING.md`](firmware/WIRING.md) | how everything is wired inside the box, wire by wire, with the soldering sheets |
| [`docs/screen-ux.md`](docs/screen-ux.md) | what the door screen can and cannot show, tested on the panel |
| [`tools/`](tools/) | the privacy scan that runs before every push, and bench test scripts |

The Home Assistant automations are not in this repo yet.

## Safety

- The surge protector only protects when it is earthed. That, and anything on 230 V, is a job
  for an electrician.
- The e-paper panel is rated 0 to +50 °C. Outdoors it needs the heater, and the heater needs
  its thermal fuse.
- Switch the PoE port off before touching any wire in the box.
- Never plug a board's USB into a computer while the box's 5 V rail is live, unless the cable
  blocks power.

## Licences

- Code (scripts, explorer, firmware): [MIT](LICENSE), except the screen driver in
  `firmware/components/lilygo_t5_47_plus/`, which keeps its upstream licence (GPLv3 for C/C++)
- Hardware designs (CAD scripts, STL, STEP, drawings): [CERN-OHL-P-2.0](LICENSES/CERN-OHL-P-2.0.txt)
- Documentation and images: [CC BY 4.0](LICENSES/CC-BY-4.0.txt)

Designed and written with [Claude Code](https://claude.com/claude-code).
