# ESP32-P4 bench bring-up

This ESP-IDF project defaults to an **Espressif ESP32-P4-Function-EV-Board hardware v1.5.2** software/bench profile. It is not a selected production board. Espressif's [current EOL board list includes this board](https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32p4/eol/eol-boards.html); procurement must confirm availability or qualify another supported board separately. The [board guide](https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32p4/esp32-p4-function-ev-board/user_guide.html) and [schematic](https://dl.espressif.com/dl/schematics/esp32-p4-function-ev-board-schematics_v1.52.pdf) document a 16 MB SPI NOR flash, IP101GRI 10/100 RMII PHY and RJ45, ES8311 mono codec/analog microphone, NS4150B speaker amplifier, and optional MIPI-CSI camera accessory. The guide says the P4 supports up to 32 MB PSRAM; record the actual fitted silicon and detected memory on the bench. The example camera accessory is 2 MP; its [module data sheet](https://dl.espressif.com/dl/schematics/camera_datasheet.pdf) labels it AS-AG638A32M2-50, while [Espressif's SC2336 sensor component](https://github.com/espressif/esp-video-components/blob/master/esp_cam_sensor/sensors/sc2336/include/sc2336.h) identifies a possible driver and I2C address. Verify the delivered sensor and adapter before relying on that driver. The board's microSD slot is unused.

## Build and run

Use **ESP-IDF release/v5.5** for the initial reproducibility target. In an initialized ESP-IDF shell:

```sh
cd firmware/p4
idf.py set-target esp32p4
idf.py build
idf.py -p PORT flash monitor
```

The build uses the 16 MB NOR partition table in `partitions.csv`: two 4 MB OTA application slots plus NVS/OTA metadata; it has no filesystem or SD partition. The default project starts from NOR without mounting storage. OTA verification, signed updates, rollback and production key provisioning are future work; the presence of two slots alone does not establish recoverable updates. The current app uses neither NVS writes nor network credentials.

Serial output reports detected flash bytes and ESP-IDF available PSRAM heap bytes, probes the ES8311 and possible SC2336 I2C addresses for acknowledgement, then starts the wired IP101 Ethernet path. Link-up and a DHCP address are reported asynchronously. **An I2C ACK is neither sensor identification nor proof of camera capture or audio input/output.** Missing camera accessory may produce no ACK; an unpowered sensor may also fail to ACK. No Wi-Fi fallback is configured. No relay, unlock, access credential, media transport, cloud or Home Assistant logic is present.

## Board/BSP boundary and smoke scope

`components/board_support/include/board_support.h` defines the board-neutral configuration consumed by the app and smoke components. The only current profile is `components/board_support/boards/function_ev_v152.c`; it owns the Function EV pin, PHY and I2C probe choices. `Kconfig.projbuild` selects the profile, with `sdkconfig.defaults` choosing the EOL bench reference by default. The application, Ethernet and I2C smoke components contain no Function EV GPIO/address constants. The network path follows [ESP-IDF Ethernet MAC/PHY APIs](https://docs.espressif.com/projects/esp-idf/en/v5.5/esp32p4/api-reference/network/esp_eth.html); compare the bench board against [Espressif's P4 IP101 example settings](https://github.com/espressif/esp-idf/blob/release/v5.5/examples/ethernet/iperf/sdkconfig.ci.default_ip101_esp32p4v1) before flashing a different revision. `components/peripheral_smoke/` performs bounded 100 ms I2C address probes; these are presence checks, not device identification. `components/net_smoke/` initializes only wired Ethernet.

The default `sdkconfig.defaults` includes Espressif's pre-v3 P4 and RMII settings for the Function EV bench profile. They are **not** product defaults: a P4X or Waveshare target must use the settings appropriate to its actual SoC revision, PHY interface and NOR capacity.

To add a verified **Waveshare ESP32-P4 Ethernet/PoE** target later, create its own profile under `board_support/boards/` and Kconfig choice after the exact SKU and PCB/SoC revision, schematic, PHY and PoE implementation are known. Record its flash/PSRAM, camera and audio wiring and power limits, then update the BSP selection and supported PHY factory without adding board-specific pins to `main/`, `net_smoke/` or `peripheral_smoke/`. Do not inherit Function EV pin values or its 16 MB flash assumption silently. Production board selection remains open. [Hardware assumptions](../../hardware/p4/README.md) list the data needed for that target.

## Device acceptance gates still required

1. Read actual PCB and SoC revisions, fitted camera sensor/adapter and NOR/PSRAM capacity. Boot with no SD card, interrupt power repeatedly, and confirm boot from NOR.
2. Build and flash with the pinned ESP-IDF, then demonstrate wired link and DHCP on direct LAN and through the single-CAT6 switch/PoE assembly. Check both P4 and independent S3 have distinct MAC/IP addresses and remain wired.
3. Use a pinned Espressif video component release to identify the camera, capture frames, exercise JPEG and H.264 hardware encoding, and record format, throughput, frame loss and memory. The SoC's documented Baseline H.264 1080p30 rating is not a board result.
4. Initialize ES8311/I2S; capture actual microphone samples and play a measured speaker tone. Measure PA load and acoustic behavior. I2C ACK alone is insufficient.
5. Measure PoE input and every regulated rail during cold start, camera/encoder, speaker peaks and heater worst case. Reset/overload the P4 branch and prove the S3 direct RoomKey ring still works. Repeat with HA and NVR down.
6. Test partition/OTA rollback on the selected NOR and board; choose secure boot/signing and wear policy before a deployed image.

The single-feed network and power design, alternative options and open test points are in [hardware/p4/README.md](../../hardware/p4/README.md). WP3 owns RTSP/WebRTC, Opus/AEC, interactive latency and end-to-end resource budgets.

## Current validation status

The files are source-only until built with ESP-IDF and run on hardware. This workspace had no `idf.py`, RISC-V ESP toolchain, board or PoE assembly at authoring time. The listed device gates are **not yet passed**.
