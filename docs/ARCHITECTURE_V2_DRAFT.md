# SDLLABS Intercom — Architecture v2 Draft

Status: handoff draft for Codex. This document is intentionally architectural, not a claim of implemented functionality.

## Design objective

Build a local-first video intercom and access-control system using the strongest ideas from Aikos Intercom and OpenChime while keeping the outdoor runtime firmware-based and eliminating Linux/SD-card dependence.

## Component ownership

### Bell MCU — critical path

Owns:
- supervised physical button input;
- pressed/cut/short diagnostics;
- ring event identity;
- direct encrypted RoomKey delivery;
- HA event publication;
- bell health/watchdog telemetry.

Must not depend on:
- P4;
- camera;
- audio;
- NVR;
- Home Assistant for direct ringing.

### ESP32-P4 — outdoor multimedia/UI

Owns:
- camera;
- hardware video codec pipeline;
- microphone/speaker;
- interactive intercom transport;
- keypad/touch UI;
- tamper sensing;
- creation of authenticated access requests.

Must not own:
- strike relay;
- gate relay;
- final credential policy authority.

### Indoor access controller — trusted actuator

Owns:
- request authentication;
- replay state;
- credential/access policy;
- door contact;
- request-to-exit;
- strike/gate relay;
- maximum relay-on safety timer;
- local audit events.

Safe default:
- locked;
- relay inactive;
- reject unauthenticated/stale/replayed requests.

### Home Assistant

Owns:
- orchestration;
- UI;
- notifications;
- automation;
- optional credential administration workflows.

Must not be required for:
- direct doorbell chime;
- basic local access policy if credentials are provisioned to the trusted controller.

### NVR

Owns:
- recording;
- retention;
- video analytics if desired.

Must not be required for live bell operation.

## Network segmentation recommendation

Place intercom devices in a dedicated VLAN.

Prefer explicit allow rules:
- bell -> RoomKeys required ring transport;
- bell -> HA required API/event traffic;
- P4 -> NVR required stream;
- P4 <-> local intercom signalling service as designed;
- management access from trusted admin VLAN only;
- access controller accepts only authenticated application protocol from explicitly allowed peers.

No inbound Internet exposure is required.

## Physical security boundary

The wall/front plate is untrusted.

Anything accessible after removing the outdoor panel must be treated as attacker-controlled.

Therefore:
- no unlock relay outdoors;
- no wire pair outdoors that directly unlocks by shorting;
- tamper is a signal, not an unlock mechanism;
- keys/secrets stored outdoors should be scoped so compromise does not grant permanent unrestricted actuation where avoidable.

## Storage model

Outdoor:
- firmware in NOR flash;
- minimal persistent configuration;
- avoid high-frequency writes;
- no required SD card;
- no required database.

Indoor controller:
- small durable credential/policy state;
- write rate bounded;
- recovery behaviour specified.

Server:
- logs;
- NVR recordings;
- optional management database.

## Update model

Target:
- signed firmware where platform support permits;
- rollback-capable OTA;
- known-good fallback;
- boot health confirmation;
- failed update must not leave unlock relay active.

Bell and access controller updates should be independently deployable from multimedia updates.

## Open decisions

Codex should research and produce ADRs before committing to:
- exact ESP32-P4 board/kit pinout;
- camera sensor;
- RTSP implementation;
- WebRTC stack;
- Opus/AEC library strategy;
- authentication primitive/protocol encoding;
- provisioning and secret rotation;
- keypad hardware;
- indoor controller MCU;
- whether e-paper remains a separate board or is integrated/replaced in a later hardware revision.
