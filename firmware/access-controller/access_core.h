#ifndef SDLLABS_ACCESS_CORE_H
#define SDLLABS_ACCESS_CORE_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/* Portable policy core. No board pin, network, clock, storage or crypto driver. */
#define AC_FRAME_LEN 121u
#define AC_SIGNED_LEN 89u
#define AC_CHALLENGE_LEN 16u
#define AC_MAX_PRINCIPALS 4u
#define AC_CHALLENGE_TTL_MS 5000u
#define AC_RETRY_MS 1000u
#define AC_LOCKOUT_MS 30000u
#define AC_PULSE_MS 250u
#define AC_CUTOFF_MS 500u

enum ac_principal_kind { AC_PRINCIPAL_P4 = 1, AC_PRINCIPAL_DIRECT_KEYPAD = 2 };
enum ac_result {
    AC_OK = 0, AC_MALFORMED, AC_UNCONFIDENTIAL, AC_PEER_MISMATCH, AC_UNKNOWN_PRINCIPAL,
    AC_NO_CHALLENGE, AC_EXPIRED, AC_REPLAY, AC_AUTH_FAILED,
    AC_RATE_LIMITED, AC_CLASS_DENIED, AC_CREDENTIAL_DENIED,
    AC_BUSY, AC_HARDWARE_FAULT
};

struct ac_callbacks {
    /* Must consult an indoor provisioned allowlist; never trust packet labels. */
    bool (*principal_kind)(void *user, const uint8_t principal[8],
                           enum ac_principal_kind *kind);
    /* CSPRNG; returns false if entropy is unavailable. */
    bool (*random16)(void *user, uint8_t out[AC_CHALLENGE_LEN]);
    /* Verify HMAC-SHA-256 over exactly AC_SIGNED_LEN bytes using an indoor key.
       Must reject unknown/revoked key IDs and compare tags in constant time. */
    bool (*verify_mac)(void *user, const uint8_t principal[8], uint8_t key_id,
                       const uint8_t frame[AC_SIGNED_LEN],
                       const uint8_t tag[32]);
    /* Payload is sensitive and valid only during this call. No log or retention.
       Adapter verifies credential, not-before/expiry/usage and revocation. */
    bool (*verify_credential)(void *user, const uint8_t principal[8],
                              const uint8_t credential_id[8],
                              const uint8_t payload[32], uint8_t credential_class);
    /* Independent hardware cutoff, capable of dropping output if MCU stalls. */
    bool (*arm_cutoff)(void *user, uint32_t maximum_ms);
    /* Must force the independent cutoff into its de-energized safe state,
       including if set_relay(false) fails. Never bypass the safety cutoff. */
    bool (*force_cutoff_off)(void *user);
    /* Board must be electrically off before firmware starts. */
    bool (*set_relay)(void *user, bool energized);
};

struct ac_slot {
    uint8_t principal[8];
    uint8_t challenge[AC_CHALLENGE_LEN];
    uint64_t issued_ms;
    uint64_t retry_after_ms;
    uint64_t lock_until_ms;
    uint8_t failures;
    bool used;
    bool challenge_active;
};

struct ac_controller {
    struct ac_callbacks cb;
    void *user;
    struct ac_slot slots[AC_MAX_PRINCIPALS];
    uint64_t relay_deadline_ms;
    bool relay_on;
    bool fault_latched;
};

bool ac_init(struct ac_controller *controller, const struct ac_callbacks *callbacks,
             void *user);
enum ac_result ac_issue_challenge(struct ac_controller *controller,
                                  const uint8_t authenticated_peer[8],
                                  bool authenticated_confidential_channel,
                                  uint64_t now_ms,
                                  uint8_t out[AC_CHALLENGE_LEN]);
enum ac_result ac_handle_request(struct ac_controller *controller,
                                 const uint8_t *frame, size_t len,
                                 const uint8_t authenticated_peer[8],
                                 bool authenticated_confidential_channel,
                                 uint64_t now_ms);
void ac_tick(struct ac_controller *controller, uint64_t now_ms);
void ac_fault(struct ac_controller *controller);

#endif
