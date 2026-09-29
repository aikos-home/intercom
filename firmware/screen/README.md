# Screen computer firmware

ESPHome firmware for the screen at the door: a LilyGO T5-4.7-S3 Touch (board V2.4) with a 4.7" e-paper
panel (ED047TC1, 960 × 540, 16 grey levels) and a GT911 touch chip. Bench-tested on 29 September 2026.

| File | What |
|---|---|
| `screen-test.yaml` | bench test page: orientation arrow, five touch targets, border lines |
| `components/lilygo_t5_47_plus/` | the display, touch and battery driver (**GPLv3**, see below), with the fast refresh |

## Build and flash

Needs ESPHome 2026.3 or newer (tested with 2026.9.0).

```
esphome compile screen-test.yaml
esptool --port COMx --after watchdog-reset write-flash 0x0 .esphome/build/klingel-screen-test/build/firmware.factory.bin
```

- **Windows:** build from PowerShell or cmd, not from Git Bash. ESP-IDF refuses to install from an MSYS shell.
- **First flash:** hold `STR_IO0`, tap `REST`, release `STR_IO0`, then flash. After that the USB port resets the
  board by itself. Use `--after watchdog-reset`: a plain reset can leave the chip in download mode.
- **Orientation:** `rotation: 270` gives portrait with the ribbon end of the glass at the bottom.
- **Touch:** no `transform`. The GT911 already reports portrait 540 × 960 in exactly this orientation.
  The upstream example (`swap_xy` + `mirror_y`) is for landscape.
- **Glass print:** the white print of the touch glass hides the outer 7–9 px of the panel on every edge.
  Keep content at least 10 px from the edge.

## How the screen updates without flashing

The upstream driver wipes the whole panel black and white before every picture (2 s, a full flash). That
looks like a defect to anyone at the door. The driver here keeps the flash for rare clean-ups and updates
everything else like an e-reader. These are the rules, in this order:

1. **Compare, don't clear.** The driver keeps a copy of what the panel shows. A new picture is compared
   with it pixel by pixel; unchanged pixels get no voltage at all.
2. **Move each pixel by exactly the difference.** Grey level `v` (0 black … 15 white) is darkness
   `d = 15 − v`. The panel drives a picture in 15 frames, and a pixel of darkness `d` normally gets frames
   `0 … d−1`. So a pixel going from `d_old` to `d_new` is darkened in frames `[d_old, d_new)` or lightened
   in frames `[d_new, d_old)`: the very frames that separate the two levels. No detour through white or
   black, so no flash.
3. **One sweep.** All changed rows are driven in the same sweep of 15 frames, whatever their number, plus
   one neutral frame so no pixel is left holding a voltage. Only the changed stretch of each row is computed.
4. **Re-darken the fringe.** Lightening spills over onto neighbouring pixels and fades thin dark lines that
   did not change. Every unchanged dark pixel within 2 px of a lightened one is darkened again.
5. **Never block the input.** Refreshing runs in its own task. The main loop only hands over the newest
   picture and keeps reading touch; if pictures pile up, the panel jumps straight to the newest one.
6. **Clean up now and then.** Small updates leave faint traces. A full refresh with the flash runs at boot,
   every `full_update_every` partial refreshes (default 30, 0 = never), when more than half the screen
   changes, and on request (`id(epaper).request_full_update()`, e.g. at night).
7. **Power off after every picture**, as the original driver does.

Measured on the bench: a tap changes the picture in 0.4–0.6 s (the original driver: 2.0–2.3 s), with no
flash and no visible shadow.

The panel stands on its side: its rows run across the portrait page. A line of text across the page
therefore touches about 300 of the 540 panel rows, and more rows mean a slower update.

## Licence of the driver

`components/lilygo_t5_47_plus/` is a modified copy of
[hbast/lilygo_t5_47_plus](https://github.com/hbast/lilygo_t5_47_plus) v1.0.0, which derives from
[vroland/epdiy](https://github.com/vroland/epdiy) and LilyGO's
[LilyGo-EPD47](https://github.com/Xinyuan-LilyGO/LilyGo-EPD47). It keeps the ESPHome licence of its
source: the C and C++ files are **GPLv3**, the Python files MIT ([LICENSE](components/lilygo_t5_47_plus/LICENSE)).
The changes for the fast refresh are in `display.cpp`, `display.h`, `display.py` and `epd_draw_plan`
in `epd_driver.c` / `epd_driver.h`, under the same terms. Everything else in this
repository stays MIT.
