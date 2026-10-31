// aikos Intercom Screen: every press of the brass button, heard on two paths (2026-09-30).
//
// Path D (direct): the bell sends (boot_id, presses, ringing) by encrypted UDP straight to this screen, like to the
// RoomKeys (packet_transport, port 18511): no Home Assistant in the way, so the screen reacts while HA restarts.
// Path H (Home Assistant): the same numbers as HA sensors.
// A press is identified by (boot_id, press number), exactly as on the RoomKeys: the first path to report a new
// press wins, the second one only adds its arrival time (-> "lead" of the direct path). Nothing counts twice.
// The first numbers after the screen boots are old news (the bell's count so far), not a press.
#pragma once

#include <cstdint>
#include "esphome/core/log.h"

namespace aikos_ring {

enum Path : char { DIRECT = 'D', HA = 'H' };

struct Press {
  uint32_t boot = 0;
  int number = -1;          // -1 = nothing known yet
  uint32_t first_ms = 0;    // arrival on the first path
  char first = 0;           // which path was first
  bool direct = false, ha = false;
  bool real = false;        // false = a baseline (count at start, or 0 after the bell restarted), not a press
};

inline Press last;                        // the newest press or baseline
static const int KEEP = 16;               // the newest presses, so a late report during storm ringing still matches
static const uint32_t LATE_MS = 10000;    // a second path later than this is not "the same ring on both paths": after an
                                          // HA outage HA re-sends the count when it is back (system test W2, 2026-10-01)
inline Press recent[KEEP];
inline int head = 0;
inline uint32_t via_direct = 0, via_ha = 0, first_direct = 0, first_ha = 0;
inline int lead_ms = 0;                   // HA arrival minus direct arrival of the last press seen on both paths
inline bool lead_new = false, count_new = false;
inline void (*on_press)(uint32_t now) = nullptr;  // a new press: the page reacts

// latest numbers per path (boot id and press number arrive as separate values)
inline uint32_t d_boot = 0, h_boot = 0;
inline int d_press = -1, h_press = -1;

inline void report(Path path, uint32_t boot, int number, uint32_t now) {
  if (boot == 0 || number < 0)
    return;
  if (last.number < 0) {  // first numbers after the screen started: the bell's count so far
    last = Press{boot, number, now, (char) path, path == DIRECT, path == HA, false};
    return;
  }
  for (Press &p : recent) {  // a press we know, now seen on this path too
    if (!p.real || p.boot != boot || p.number != number)
      continue;
    bool &seen = path == DIRECT ? p.direct : p.ha;
    if (seen)
      return;
    seen = true;
    if (now - p.first_ms > LATE_MS) {
      ESP_LOGI("ring", "press %d via %s only %u s later (e.g. HA back after an outage): not counted", number,
               path == DIRECT ? "direct" : "HA", (unsigned) ((now - p.first_ms) / 1000));
      return;
    }
    (path == DIRECT ? via_direct : via_ha)++;
    count_new = true;
    lead_ms = p.first == DIRECT ? (int) (now - p.first_ms) : -(int) (now - p.first_ms);
    lead_new = true;
    ESP_LOGI("ring", "press %d also via %s, direct path %s by %d ms", number, path == DIRECT ? "direct" : "HA",
             lead_ms >= 0 ? "ahead" : "behind", lead_ms >= 0 ? lead_ms : -lead_ms);
    return;
  }
  if (boot == last.boot && number <= last.number)
    return;  // the baseline, or older than everything we keep
  if (number == 0) {  // the bell restarted and nobody pressed yet: new baseline, no press
    last = Press{boot, 0, now, (char) path, path == DIRECT, path == HA, false};
    return;
  }
  // a new press (a jump of more than one means a lost report: still one ring)
  last = Press{boot, number, now, (char) path, path == DIRECT, path == HA, true};
  recent[head] = last;
  head = (head + 1) % KEEP;
  (path == DIRECT ? via_direct : via_ha)++;
  (path == DIRECT ? first_direct : first_ha)++;
  count_new = true;
  ESP_LOGI("ring", "press %d first via %s", number, path == DIRECT ? "direct" : "HA");
  if (on_press != nullptr)
    on_press(now);
}

// A new boot id comes BEFORE the new boot's press number (both in one packet, boot_id first; on HA in any order). The
// number still held belongs to the old boot: paired with the new id it looked like a press (bench 2026-10-04: the bell
// restarted at count 40 -> phantom press "40" -> its real presses 1, 2 were "older" and ignored). So a new id waits for
// its own number.
inline void direct_boot(float x, uint32_t now) {
  const uint32_t b = (uint32_t) x;
  if (b != d_boot)
    d_press = -1;
  d_boot = b;
  report(DIRECT, d_boot, d_press, now);
}
inline void direct_presses(float x, uint32_t now) {
  d_press = (int) x;
  report(DIRECT, d_boot, d_press, now);
}
inline void ha_boot(float x, uint32_t now) {
  if (x != x)  // NaN: unknown / unavailable in HA
    return;
  const uint32_t b = (uint32_t) x;
  if (b != h_boot)
    h_press = -1;  // as on the direct path: the number held belongs to the old boot
  h_boot = b;
  report(HA, h_boot, h_press, now);
}
inline void ha_presses(float x, uint32_t now) {
  if (x != x)
    return;
  h_press = (int) x;
  report(HA, h_boot, h_press, now);
}

}  // namespace aikos_ring
