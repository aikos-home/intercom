# Doorbell computer firmware

Stock ESPHome (tested with 2026.9.0, ESP-IDF) plus four small local components in [`../components/`](../components/).
The doorbell computer reads the brass button over a supervised line and reports every press to Home Assistant and,
directly, to the room keys and the door screen. It is the only wired computer in the door box: it also runs the
Wi-Fi "aikos" for the screen and the talk computer and bridges it into the LAN. Wiring of the whole box:
[`../WIRING.md`](../WIRING.md); header pins: [`PINOUT.md`](PINOUT.md).

| File | What it is |
|---|---|
| [`bell-core.yaml`](bell-core.yaml) | The bell logic, the same on every board: line sampling, press detection, line supervision, diagnostics |
| [`aikos-intercom-bell.yaml`](aikos-intercom-bell.yaml) | The board file: Waveshare ESP32-S3-ETH (W5500 Ethernet, PoE via its plug-on module), direct ring targets, self-healing, supervision wires to the talk computer |
| [`aikos-intercom-bell-aptest.yaml`](aikos-intercom-bell-aptest.yaml) | + an access point (bench step, kept as the base of the next file) |
| [`aikos-intercom-bell-bridge.yaml`](aikos-intercom-bell-bridge.yaml) | **What runs at the door:** + Wi-Fi "aikos" bridged into the LAN (`eth_wifi_bridge`) |
| [`aikos-intercom-bell-bridge-diag.yaml`](aikos-intercom-bell-bridge-diag.yaml) | The same with a core dump on crash and test actions, for the bench |
| [`aikos-intercom-bell-safe.yaml`](aikos-intercom-bell-safe.yaml) | The SAFE firmware in the factory partition (see below) |
| [`partitions-bell.csv`](partitions-bell.csv) | Flash layout: factory 3 MB (safe firmware) + two 6 MB OTA slots |
| [`net_watchdog.h`](net_watchdog.h) | Restart if the link is up but nothing can be sent |
| [`wt32eth-intercom-bell.yaml`](wt32eth-intercom-bell.yaml) | The first try on a WT32-ETH01, kept for the record: see *Why not the WT32-ETH01* below |
| [`secrets.example.yaml`](secrets.example.yaml) | Copy to `secrets.yaml` (never commit it) and fill in your own keys |

First flash over USB-C (the safe firmware's factory image, then the normal firmware over the network):

```bash
esphome compile aikos-intercom-bell-safe.yaml      # write its firmware.factory.bin at 0x0 over USB
esphome run aikos-intercom-bell-bridge.yaml        # then OTA, into the app slots; the factory partition stays
```

## It heals itself

A box in the wall must never need hands. What the bell does about it:

- **A firmware counts as good only after 2 minutes healthy** (bridge up, a TCP connection to the gateway works).
  Until then the bootloader can roll back to the previous image.
- **5 failed boots in a row** start the **safe firmware** from the factory partition: the plain bell (Ethernet only,
  no bridge, no access point). It still rings to Home Assistant and the screen and accepts updates. It tries the
  normal firmware again after 60 minutes, or on its "Start normal firmware" button.
- **Runtime guards** restart the bell when the network is stuck: a TCP guard in the bridge firmware (3 failed
  connections to the gateway in a row while the link is up), the network watchdog in the safe firmware. They use a
  plain restart, and `safe_mode: boot_is_good_on_shutdown` is false: ESPHome's default would mark the running image
  good on every orderly restart, which defeats the rollback.
- **The bell and the talk computer watch each other by wire** (`aikos_peer_guard`): a 1 Hz heartbeat each way; if
  one stops for 30 s, the other pulls its reset line (at most 3 times an hour, never before it has seen a heartbeat).
- In Home Assistant, an automation can power-cycle the switch port when the bell stays unreachable (not in this repo).

## Wi-Fi "aikos"

`eth_wifi_bridge` puts the Ethernet port and the bell's access point into one layer-2 bridge, so the screen and the
talk computer get their addresses from the house DHCP like any LAN device. Two settings were needed against a stall
seen on the bench (the network task blocked the main loop until the task watchdog fired): a forwarding table of
128 entries (16 overflowed and flooded every frame) and the W5500 with all-multicast off.

## Direct ring path

Every press goes to Home Assistant **and**, at the same time, straight to the room keys and the door screen over encrypted UDP (ESPHome
`packet_transport`, port 18511, unicast to each key's address, rolling code against replays), so the gong still
sounds while Home Assistant restarts. Each packet carries `boot_id` (24-bit random per boot; `packet_transport`
sends values as 32-bit floats, so larger integers would arrive rounded), `presses` (press number since boot) and
`ringing` (on while the button is held, off on release or after the adjustable maximum duration: holding rings one
continuous gong, like a school bell). A key rings once per new `(boot_id, presses)`, whichever path delivers it first.

## The supervised line

```
3V3 ── 10 kΩ ──┬── IO1 (ADC1)          at the button, at the far end of the cable:
               ├── 100 nF ── GND
               └── 1 kΩ ── cable ────┬──────────┐
                                     │  button   10 kΩ (end-of-line)
               GND ─── cable ────────┴──────────┘
```

The end-of-line resistor turns "nobody rings" and "cable cut" into two different voltages. Measured on
the bench (the ESP's internal pull-up is switched on too, see below):

| Line | Volts at the pin | Entity |
|---|---|---|
| idle | 2.03 | all clear |
| pressed | 0.34–0.47 (firm), 0.6–0.9 (half-closed contact) | *Doorbell button* on, one *Doorbell* event |
| cable cut | 3.18 | *Line cut* after 10 s |
| shorted | 0.0 | one press, then *Line shorted* after 60 s |

Keep `line_installed: "false"` until the line is wired: a floating ADC pin rings by itself.

## What the bench taught us

Each of these cost presses before it was fixed:

- **ESPHome batches API updates for 100 ms by default.** A fast on/off pair inside one batch reaches
  Home Assistant only as its last state, so storm ringing showed 2 of 5 presses. `api: batch_delay: 0ms`
  sends every change at once, and saves up to 100 ms of delay.
- **A loose signal wire looked like a held press.** A floating ESP32-S3 ADC pin reads about 0.1 V. The
  chip's internal pull-up is switched on after the ADC is set up (the ADC driver resets the pad), so a
  loose wire now reads as a cut cable.
- **A half-closed brass contact hovers between 0.6 and 0.9 V** and was counted twice. Hysteresis: a
  press starts below 1.30 V and ends only above 1.60 V.
- **A median filter hid very short contacts.** It is gone; the 100 nF on the line smooths enough. The
  line is sampled every millisecond (diagnostic *Line samples per second*, about 980).

Result on the bench: 10 of 10 slow presses; filmed storm ringing at about 5.7 presses per second, 14 of
15 counted, and the 15th only grazed the contact for 1 ms. Every counted press reached Home Assistant
exactly once. Grazes are deliberately not counted: that would make the line sensitive to noise on a
long outdoor cable.

## Why not the WT32-ETH01

The WT32-ETH01 was the first choice and was dropped. Its IO0 is both the boot-mode strapping pin and
the input for the 50 MHz Ethernet clock. On this unit the oscillator holds IO0 low while it is off, so
after one lucky start the chip always booted into download mode (`boot:0x3`), with or without a
network cable. Pull-ups of 10 kΩ and even 1 kΩ from IO0 to 3V3 did not win. A doorbell must come back
on its own after a power cut, so the board is unfit for this job. Others report the same symptom; if
your WT32 hangs at boot, the scripts in [`tools/wt32/`](../../tools/wt32/) show what IO0 does without
unplugging anything.
