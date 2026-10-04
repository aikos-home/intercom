# Talk computer firmware

The door's talk computer: microphone and speaker, on Wi-Fi. Board: an ESP32-S3-N16R8 dev board (silkscreen "HW678"),
with an INMP441 microphone and a MAX98357A amplifier driving a VISATON K 40 SQ. Wiring: [`../WIRING.md`](../WIRING.md).

| File | What it is |
|---|---|
| [`aikos-intercom-talk.yaml`](aikos-intercom-talk.yaml) | The firmware (ESPHome 2026.9.0, ESP-IDF) |
| [`talk_volume.h`](talk_volume.h) | Speaker level: speech is capped at −6 dB, only the on-demand test gong gets full level |
| [`rtp_talk.h`](rtp_talk.h) | Voice v1 (walkie-talkie over RTP), kept for the record; v2 uses the shared library below |
| [`secrets.example.yaml`](secrets.example.yaml) | Copy to `secrets.yaml` (never commit it) and fill in your own keys |

What it does:

- **Voice:** the shared voice link `aikos_voice` (pulled from [aikos-home/aikos](https://github.com/aikos-home/aikos),
  pinned to the tag `voice-v2.1.0`) with the door as the arbiter of a call: a call starts when the visitor presses
  "Sprechen" on the screen after a ring, or when a room key holds its button. Room keys and the screen talk to it
  directly over encrypted `packet_transport` links; Home Assistant is not in the audio path.
- **Wi-Fi:** prefers the bell's own Wi-Fi "aikos" (`aikos_wifi`); the house Wi-Fi, entered once via Improv and never in
  a file, is the fallback.
- **Self-healing:** a firmware counts as good only after 2 minutes with the gateway answering; 5 failed boots in a row
  start ESPHome's safe mode; the gateway guard restarts after 5 minutes without an answer; the bell can reset this
  board over a wire and the other way round (`aikos_peer_guard`).
- **No chime at the door:** the test gong plays only on the Home Assistant button "Test chime".

Flash over the board's port labelled "USB" (native USB, logs too); a factory-fresh board needs BOOT + RST once.
PSRAM is off: the board in use fails the PSRAM self-test, and the firmware fits in internal RAM.
