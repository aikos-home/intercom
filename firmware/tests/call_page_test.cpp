// Unit tests for the door screen's call page state (call/call_page.h). Exit code 1 = a rule broke.
// Build and run on a PC:
//   g++ -std=c++17 -Wall -Wextra -I ../call call_page_test.cpp -o call_page_test && ./call_page_test
//   (Windows without a compiler: python -m ziglang c++ ... from the PyPI package "ziglang")
#include <cstdio>
#include <string>
#include "call_page.h"

static int failed = 0, passed = 0;
static void check(bool ok, const char *what) {
  if (ok) {
    passed++;
  } else {
    failed++;
    printf("FAIL: %s\n", what);
  }
}

using aikos_call::Msg;

static void reset() {
  aikos_call::n_msgs = 0;
  aikos_call::log_n = 0;
  aikos_call::log_active = false;
  aikos_call::door_call_id = 0;
  aikos_call::door_call_known = false;
}

int main() {
  const Msg a{"1", "door", "Paketdienst", "Ich habe ein Paket"};
  const Msg b{"2", "room", "Max", "Bitte vor die Tür legen"};
  const Msg c{"3", "door", "", "Hallo?"};
  const Msg call1[] = {a, b};
  const Msg call2[] = {c};

  // ── R22: the last call's chat never shows at the next call, not even briefly ──
  reset();
  aikos_call::set_door_call(0);  // boot: no call
  aikos_call::set_door_call(41);  // call 41 starts
  aikos_call::set_log_active(true);
  aikos_call::set_messages(call1, 2);
  check(aikos_call::n_msgs == 2, "call 41: its two messages are shown");
  aikos_call::set_door_call(41);  // the broadcast repeats every second
  check(aikos_call::n_msgs == 2, "the same call id again: the chat stays");
  uint32_t v = aikos_call::chat_version;
  aikos_call::set_door_call(0);  // call 41 ends; HA hasn't said so yet
  check(aikos_call::n_msgs == 0, "the end (id 0) forgets the chat before HA knows");
  check(aikos_call::chat_version != v, "forgetting counts as a change (the screen redraws)");
  aikos_call::set_door_call(42);  // the next call, HA still on the old call (active, old list: the bug of 23:1x)
  check(aikos_call::n_msgs == 0, "R22: call 42 starts with an empty chat although HA still says active");
  aikos_call::set_log_active(true);  // HA repeats active: nothing old comes back
  check(aikos_call::n_msgs == 0, "R22: HA's active again brings nothing of call 41 back");
  aikos_call::set_messages(call2, 1);  // the new call's first words
  check(aikos_call::n_msgs == 1 && aikos_call::msgs[0] == c, "call 42: only its own message");

  // a new id straight after another (the 0 between them was missed): forgotten as well
  reset();
  aikos_call::set_door_call(7);
  aikos_call::set_log_active(true);
  aikos_call::set_messages(call1, 2);
  aikos_call::set_door_call(8);
  check(aikos_call::n_msgs == 0, "id 7 -> 8 without 0 in between: forgotten");

  // ── the log shows its messages only while its call is on ──
  reset();
  aikos_call::set_door_call(0);
  aikos_call::set_messages(call1, 2);  // a list while the log says no call
  check(aikos_call::n_msgs == 0, "log not active: nothing shown");
  aikos_call::set_log_active(true);  // HA delivered messages_json before active (order of attributes)
  check(aikos_call::n_msgs == 2, "active arrives after the list: the kept list is shown");
  aikos_call::set_log_active(false);
  check(aikos_call::n_msgs == 0, "the log's call is over: nothing shown");

  // ── boot in the middle of a call ──
  reset();
  aikos_call::set_log_active(true);  // HA connects first and sends the running call
  aikos_call::set_messages(call1, 2);
  aikos_call::set_door_call(9);  // then the first broadcast: nothing of an earlier call can be on this screen
  check(aikos_call::n_msgs == 2, "boot during a call: the first id after boot keeps the running call's chat");

  // ── the screen still sees "only added at the end" (ink only) ──
  reset();
  aikos_call::set_door_call(0);
  aikos_call::set_door_call(10);
  aikos_call::set_log_active(true);
  aikos_call::set_messages(call1, 1);
  aikos_call::set_messages(call1, 2);
  check(aikos_call::appended, "a message added at the end: appended");

  // ── R27: the device keeps the newest 10; the oldest falling out is still "added at the end" ──
  Msg many[14];
  for (int i = 0; i < 14; i++)
    many[i] = Msg{std::to_string(100 + i), "door", "Besucher", "Satz " + std::to_string(i)};
  reset();
  aikos_call::set_door_call(0);
  aikos_call::set_door_call(11);
  aikos_call::set_log_active(true);
  aikos_call::set_messages(many, 10);
  check(aikos_call::MAX_MSGS == 10 && aikos_call::n_msgs == 10, "R27: ten messages fill the window");
  aikos_call::set_messages(many + 1, 10);  // the log's newest 10 after one more message
  check(aikos_call::appended && aikos_call::dropped == 1, "R27: one new, the oldest out: appended, 1 dropped");
  check(aikos_call::msgs[0] == many[1] && aikos_call::msgs[9] == many[10], "R27: the window holds messages 1..10");
  aikos_call::set_messages(many + 3, 10);  // two more at once
  check(aikos_call::appended && aikos_call::dropped == 2, "R27: two new at once: appended, 2 dropped");
  Msg renamed[10];
  for (int i = 0; i < 10; i++)
    renamed[i] = many[3 + i];
  renamed[4].who = "Paketdienst";  // R25: the identity sticks to an earlier message
  aikos_call::set_messages(renamed, 10);
  check(!aikos_call::appended, "R27: an earlier message changed: not appended (a new page)");
  aikos_call::set_messages(many, 14);  // more than the window: the newest are kept
  check(aikos_call::n_msgs == 10 && aikos_call::msgs[0] == many[4] && aikos_call::msgs[9] == many[13],
        "R27: 14 given: the newest 10 are kept");
  aikos_call::set_messages(call1, 2);
  check(!aikos_call::appended, "a list with nothing of the old one: not appended");
  aikos_call::set_messages(call1, 2);
  aikos_call::set_messages(call1, 1);
  check(!aikos_call::appended, "a shorter list: not appended");

  printf("%d passed, %d failed\n", passed, failed);
  return failed == 0 ? 0 : 1;
}
