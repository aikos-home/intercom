#include "../access_core.h"

#include <assert.h>
#include <openssl/crypto.h>
#include <openssl/hmac.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

static const uint8_t p4_id[8] = {1, 2, 3, 4, 5, 6, 7, 8};
static const uint8_t keypad_id[8] = {8, 7, 6, 5, 4, 3, 2, 1};
static const uint8_t test_key[32] = {0x28, 0xb9, 0xd6, 0x82, 0x31, 0xc5, 0x42, 0x7f,
    0x81, 0x05, 0xe9, 0x33, 0x6b, 0x21, 0x3a, 0x19, 0x51, 0x64, 0x88, 0x94,
    0xa2, 0xf9, 0x3d, 0x9b, 0xd4, 0x41, 0x76, 0x07, 0x5e, 0x35, 0x2b, 0x90};

struct fixture {
    struct ac_controller controller;
    bool output;
    bool cutoff_armed;
    bool fail_arm;
    bool fail_relay_off;
    unsigned rng_count;
    unsigned credential_calls;
};

static bool principal_kind(void *user, const uint8_t id[8], enum ac_principal_kind *kind)
{
    (void)user;
    if (memcmp(id, p4_id, 8) == 0) { *kind = AC_PRINCIPAL_P4; return true; }
    if (memcmp(id, keypad_id, 8) == 0) { *kind = AC_PRINCIPAL_DIRECT_KEYPAD; return true; }
    return false;
}

static bool random16(void *user, uint8_t out[16])
{
    struct fixture *f = user;
    ++f->rng_count;
    for (unsigned i = 0; i < 16; ++i) out[i] = (uint8_t)(f->rng_count + i);
    return true;
}

static bool verify_mac(void *user, const uint8_t id[8], uint8_t key_id,
                       const uint8_t frame[AC_SIGNED_LEN], const uint8_t tag[32])
{
    (void)user;
    enum ac_principal_kind kind;
    uint8_t calculated[32];
    unsigned int len = 0;
    if (!principal_kind(user, id, &kind) || key_id != 7) return false;
    if (!HMAC(EVP_sha256(), test_key, sizeof(test_key), frame, AC_SIGNED_LEN,
              calculated, &len) || len != 32) return false;
    bool result = CRYPTO_memcmp(calculated, tag, 32) == 0;
    OPENSSL_cleanse(calculated, sizeof(calculated));
    return result;
}

static bool verify_credential(void *user, const uint8_t id[8], const uint8_t cred_id[8],
                              const uint8_t payload[32], uint8_t cred_class)
{
    struct fixture *f = user;
    (void)id;
    (void)cred_id;
    (void)cred_class;
    ++f->credential_calls;
    /* Deliberate fake policy: tests control acceptance, not a PIN design. */
    return payload[0] == 0xa5;
}

static bool arm_cutoff(void *user, uint32_t max_ms)
{
    struct fixture *f = user;
    assert(max_ms == AC_CUTOFF_MS);
    if (f->fail_arm) return false;
    f->cutoff_armed = true;
    return true;
}

static bool force_cutoff_off(void *user)
{
    ((struct fixture *)user)->cutoff_armed = false;
    return true;
}
static bool set_relay(void *user, bool on)
{
    struct fixture *f = user;
    assert(!on || f->cutoff_armed);
    if (!on && f->fail_relay_off) return false;
    f->output = on;
    return true;
}

static void setup(struct fixture *f)
{
    memset(f, 0, sizeof(*f));
    const struct ac_callbacks cb = {principal_kind, random16, verify_mac,
        verify_credential, arm_cutoff, force_cutoff_off, set_relay};
    assert(ac_init(&f->controller, &cb, f));
    assert(!f->output && !f->cutoff_armed);
}

static void frame(struct fixture *f, uint8_t out[AC_FRAME_LEN], const uint8_t id[8],
                  uint8_t cls, bool good_credential, uint64_t now_ms)
{
    uint8_t challenge[16];
    assert(ac_issue_challenge(&f->controller, id, true, now_ms, challenge) == AC_OK);
    memset(out, 0, AC_FRAME_LEN);
    memcpy(out, "ACR1", 4);
    out[4] = 1;
    out[5] = 1;
    out[6] = cls;
    out[7] = 7;
    memcpy(out + 9, id, 8);
    out[17] = (uint8_t)f->rng_count;
    memcpy(out + 33, challenge, 16);
    out[49] = 9;
    out[57] = good_credential ? 0xa5 : 0x51;
    unsigned int len = 0;
    assert(HMAC(EVP_sha256(), test_key, sizeof(test_key), out, AC_SIGNED_LEN,
                out + AC_SIGNED_LEN, &len));
    assert(len == 32);
}

static void test_valid_and_replay(void)
{
    struct fixture f;
    uint8_t request[AC_FRAME_LEN];
    setup(&f);
    frame(&f, request, p4_id, 1, true, 100);
    assert(ac_handle_request(&f.controller, request, sizeof(request), p4_id, true, 101) == AC_OK);
    assert(f.output && f.cutoff_armed);
    assert(ac_handle_request(&f.controller, request, sizeof(request), p4_id, true, 102) != AC_OK);
    ac_tick(&f.controller, 350);
    assert(f.output);
    ac_tick(&f.controller, 351);
    assert(!f.output && !f.cutoff_armed);
}

static void test_malformed_and_auth(void)
{
    struct fixture f;
    uint8_t request[AC_FRAME_LEN];
    setup(&f);
    frame(&f, request, p4_id, 1, true, 100);
    assert(ac_handle_request(&f.controller, request, sizeof(request) - 1, p4_id, true, 101) == AC_MALFORMED);
    request[8] = 1;
    assert(ac_handle_request(&f.controller, request, sizeof(request), p4_id, true, 101) == AC_MALFORMED);
    request[8] = 0;
    assert(ac_handle_request(&f.controller, request, sizeof(request), p4_id, false, 101) == AC_UNCONFIDENTIAL);
    assert(ac_handle_request(&f.controller, request, sizeof(request), keypad_id, true, 101) == AC_PEER_MISMATCH);
    request[57] ^= 1;
    assert(ac_handle_request(&f.controller, request, sizeof(request), p4_id, true, 101) == AC_AUTH_FAILED);
    assert(!f.output && f.credential_calls == 0);
}

static void test_expiry_class_and_lockout(void)
{
    struct fixture f;
    uint8_t request[AC_FRAME_LEN];
    setup(&f);
    frame(&f, request, p4_id, 1, true, 100);
    assert(ac_handle_request(&f.controller, request, sizeof(request), p4_id, true, 5101) == AC_EXPIRED);
    assert(!f.output);
    frame(&f, request, p4_id, 2, true, 5200);
    assert(ac_handle_request(&f.controller, request, sizeof(request), p4_id, true, 5201) == AC_CLASS_DENIED);
    assert(f.credential_calls == 0);
    for (unsigned i = 0; i < 3; ++i) {
        uint64_t at = 6300 + (uint64_t)i * 1100;
        frame(&f, request, p4_id, 1, false, at);
        assert(ac_handle_request(&f.controller, request, sizeof(request), p4_id, true, at + 1) == AC_CREDENTIAL_DENIED);
    }
    assert(ac_issue_challenge(&f.controller, p4_id, true, 10000, request) == AC_RATE_LIMITED);
    assert(!f.output);
}

static void test_cutoff_and_direct_keypad(void)
{
    struct fixture f;
    uint8_t request[AC_FRAME_LEN];
    setup(&f);
    frame(&f, request, keypad_id, 2, true, 100);
    f.fail_arm = true;
    assert(ac_handle_request(&f.controller, request, sizeof(request), keypad_id, true, 101) == AC_HARDWARE_FAULT);
    assert(!f.output && f.controller.fault_latched);
    setup(&f);
    frame(&f, request, keypad_id, 2, true, 100);
    assert(ac_handle_request(&f.controller, request, sizeof(request), keypad_id, true, 101) == AC_OK);
    ac_fault(&f.controller);
    assert(!f.output && !f.cutoff_armed && f.controller.fault_latched);
}

static void test_peer_binding_and_stale_signed_frame(void)
{
    struct fixture f;
    uint8_t old_request[AC_FRAME_LEN], current_request[AC_FRAME_LEN], challenge[16];
    setup(&f);
    assert(ac_issue_challenge(&f.controller, p4_id, false, 100, challenge) == AC_UNCONFIDENTIAL);
    assert(f.rng_count == 0);
    frame(&f, old_request, p4_id, 1, true, 100);
    frame(&f, current_request, p4_id, 1, true, 101);
    assert(ac_handle_request(&f.controller, old_request, sizeof(old_request),
                             p4_id, true, 102) == AC_REPLAY);
    assert(ac_handle_request(&f.controller, current_request, sizeof(current_request),
                             keypad_id, true, 102) == AC_PEER_MISMATCH);
    assert(ac_handle_request(&f.controller, current_request, sizeof(current_request),
                             p4_id, true, 102) == AC_OK);
    assert(f.output);
}

static void test_busy_does_not_consume_credential(void)
{
    struct fixture f;
    uint8_t p4_request[AC_FRAME_LEN], keypad_request[AC_FRAME_LEN];
    setup(&f);
    frame(&f, p4_request, p4_id, 1, true, 100);
    assert(ac_handle_request(&f.controller, p4_request, sizeof(p4_request),
                             p4_id, true, 101) == AC_OK);
    assert(f.credential_calls == 1);
    frame(&f, keypad_request, keypad_id, 2, true, 102);
    assert(ac_handle_request(&f.controller, keypad_request, sizeof(keypad_request),
                             keypad_id, true, 103) == AC_BUSY);
    assert(f.credential_calls == 1);
}

static void test_failed_relay_off_forces_independent_cutoff(void)
{
    struct fixture f;
    uint8_t request[AC_FRAME_LEN];
    setup(&f);
    frame(&f, request, p4_id, 1, true, 100);
    assert(ac_handle_request(&f.controller, request, sizeof(request),
                             p4_id, true, 101) == AC_OK);
    f.fail_relay_off = true;
    ac_tick(&f.controller, 351);
    assert(f.output); /* Failed GPIO deassertion in the mock. */
    assert(!f.cutoff_armed); /* Independent cutoff removed physical power. */
    assert(f.controller.fault_latched);
}

int main(void)
{
    test_valid_and_replay();
    test_malformed_and_auth();
    test_expiry_class_and_lockout();
    test_cutoff_and_direct_keypad();
    test_peer_binding_and_stale_signed_frame();
    test_busy_does_not_consume_credential();
    test_failed_relay_off_forces_independent_cutoff();
    puts("access_core: all host tests passed");
    return 0;
}
