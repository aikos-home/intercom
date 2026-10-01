# ADR-0002: Physical unlock authority stays indoors

Status: accepted for architecture v2, 2026-10-01.

## Context

The outdoor panel can be removed or shorted. OpenChime's proposed Ring hardware places strike/gate relay control at that panel. SDLLABS requires a stronger physical trust boundary.

## Decision

Place all strike/gate switching, actuator power paths, credential policy, request verification, replay state and maximum-on cutoff on a protected indoor controller. P4 may collect input and send an authenticated, short-lived access request; it cannot directly energize outputs. No outdoor wire pair may unlock by shorting. HA, MQTT and NVR have no direct relay interface. Indoor request-to-exit and door-contact inputs are separately wired to the controller. Tamper never triggers unlock.

The indoor verifier must reject unauthenticated, malformed, stale or replayed requests, apply rate limits and credential policy, and keep relays de-energized at boot, reset and fault. A firmware timer plus an independent maximum-on mechanism bound pulse length. PINs are not stored or logged in plaintext; temporary credentials have bounded time/uses and revocation. Caller ID alone cannot authorize a main entrance.

## Consequences

WP4 must specify principal identity, key provisioning/rotation, authentication, freshness and reboot behavior before coding. Physical P4 compromise remains able to submit attempts as its own principal; indoor lockout and constrained permissions limit that risk. Controller loss means no remote unlock. Exact fail-secure/egress behavior, actuator polarity, cutoff circuit, and local code requirements need hardware review before installation.

## Rejected alternatives

Outdoor relay GPIO, a generic `unlock` MQTT topic, or HA automation directly operating a relay would cross the physical boundary and are prohibited.
