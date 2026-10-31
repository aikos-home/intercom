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
- **Rings straight from the bell** (0.7.21): the bell's press counter arrives over `packet_transport`
  (`../ring/ring_path.h` counts each press once), so a key that holds within 2 minutes answers that ring, without HA.
- **Leave a message** (0.7.21): while the screen records ("Nachricht hinterlassen"), the door microphone is open as in a
  call, so the words reach the transcriber and the call log; the end of the recording ends the call unless a room key
  answered meanwhile.
- **Speech output** (0.7.21): the Home Assistant action `allow_tts {host, ms}` lets one trusted source play at the door
  for up to 60 s (RTP like a key), outside of calls too: the door part of a later `aikos.say`.
- **Announcement cue** (0.7.26, the owner 22.10.): the action `tts_cue` (no fields) plays a short soft two-note tone
  (660 → 990 Hz, 0.23 s, at the speech volume) at once, so the wait for a synthesised voice is not dead air; skipped
  during a call. aikos calls it when it starts making a sentence, then `allow_tts` and the stream as before.
- **No echo in the transcript** (0.7.27): the door mic's copy to the transcriber pauses while the door speaker
  plays (a key or the app holding, a TTS sentence, a tone) and 600 ms after. Before, a resident's words came out of the
  speaker, into the door mic and back into the call log as the visitor's (aikos_voice mutes only the path to the keys).
- **Message recorder** (0.7.23): `text` "Message recorder" (`host:port`) gets the door microphone in addition, and only
  while a message is recorded (audio is kept for "Nachricht hinterlassen" only, never for calls); `test_message {ms}`
  records one without a finger on the screen.
- **App participant** (0.7.24): `app_join {host, ms}` sends the door microphone to an app service's socket during a call
  for up to 60 s (refresh it); the app takes part like a key through `key_state {host, state}` with the same `ip:port`
  and sends its RTP from exactly there. No change to `aikos_voice`.
- **Supervision test** (0.7.25): `test_reset_bell` pulls the bell's reset line for 200 ms, as the guard would.
- **No chime at the door:** the test gong plays only on the Home Assistant button "Test chime".

Flash over the board's port labelled "USB" (native USB, logs too); a factory-fresh board needs BOOT + RST once.
PSRAM is off: the board in use fails the PSRAM self-test, and the firmware fits in internal RAM.
