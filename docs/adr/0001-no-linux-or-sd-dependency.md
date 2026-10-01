# ADR-0001: Outdoor runtime needs neither Linux nor SD

Status: accepted for architecture v2, 2026-10-01.

## Context

The multimedia outdoor unit needs camera, codec, audio and networking, but is exposed to abrupt power loss and must boot as an appliance. OpenChime's current Chime uses a Buildroot Linux image and SD-backed A/B root filesystems. SDLLABS has selected an ESP32-P4/ESP-IDF/FreeRTOS direction; its exact board and media capability still need proof.

## Decision

Use ESP32-P4 firmware booting from on-board NOR flash. Core operation, including media startup, configuration needed to run, and recovery, has no Linux, SD card, writable system filesystem, database, or cloud prerequisite. Optional removable storage may hold noncritical data only. Separate bounded configuration from runtime; design signed/verified updates and recoverable A/B or equivalent rollback supported by the chosen flash layout. Bell and indoor controller update independently.

## Consequences

WP2 must choose a board/flash/partition layout and demonstrate Ethernet, camera, codec and audio without SD. WP3 must establish actual ESP-IDF media feasibility and resource limits; Linux libraries or Pi drivers cannot be assumed portable. NOR writes need wear bounds. Failed updates must return to known-good firmware. Exact secure-boot, flash encryption and signing choices require board-specific design and validation.

## Rejected alternatives

Pi/Buildroot as the required outdoor computer, and SD-backed boot/rootfs, violate the appliance constraint. A removable card remains acceptable solely for optional noncritical recording/export.
