// aikos Intercom Screen: a spoken reply from inside, shown as text (TEST, speed test with RoomKey, 2026-09-30).
//
// Contract (aikos vertraege.md §6): sensor.talk_transcript, state = ISO timestamp of the newest transcript,
// attribute "text" = the transcript, attribute "device" = who spoke. State and attributes arrive as separate API
// messages, so a new transcript is taken SETTLE_MS after the last of them. The first values after boot are old news.
// The screen also listens to binary_sensor.doorbell_button and measures ring -> text and ring -> picture itself.
// Speaker (§6 since 17:48): attribute "speaker" = a name or role the speaker said ("Max", "Paketdienst · DHL")
// turns the title into "<name> sagt:"; attribute "message" = the text without greeting and introduction replaces the
// text (if it is empty, only the introduction was said: then the full text is shown).
// HA sends an attribute only when it CHANGES (same speaker twice = sent once), so the last value received is the
// current one; RoomKey always sets both (empty string = none), so an old name cannot outlive a new transcript.
#pragma once

#include <cmath>
#include <cstdint>
#include <cstdio>
#include <string>
#include "esphome/components/display/display.h"
#include "esphome/components/font/font.h"
#include "esphome/core/log.h"

namespace aikos_talk {

static const uint32_t SETTLE_MS = 150;         // state and attributes of one transcript arrive this close together
static const uint32_t SHOW_MS = 60000;         // outside a conversation: then back to the normal pages
static const uint32_t RING_WINDOW_MS = 120000;  // a transcript this soon after a ring answers that ring

enum Result : int { NOTHING = 0, PAGE = 1, MEASURED = 2 };

struct Assets {
  esphome::font::Font *title = nullptr;  // 48 px
  esphome::font::Font *big = nullptr;    // 40 px, GF_Latin_Core
  esphome::font::Font *small = nullptr;  // 32 px, GF_Latin_Core, for long texts
  esphome::font::Font *info = nullptr;   // 24 px
  esphome::font::Font *icon = nullptr;   // Material Symbols 72 px
};
inline Assets assets;

// latest values from Home Assistant
inline std::string stamp, text, device;
inline std::string speaker_in, message_in;
inline uint32_t speaker_ms = 0, message_ms = 0;  // when they arrived
inline bool primed = false;
inline uint32_t first_change_ms = 0, last_change_ms = 0;  // 0 = nothing pending
inline uint32_t ring_ms = 0;
inline bool conversation = false;  // the talk computer's "In call": the room's words stay while it lasts (R8)

// the message on screen
inline bool active = false, close_request = false, drawn = false, measured = false;
inline std::string msg, from, speaker;
inline uint32_t arrived_ms = 0;
inline float ring_to_text_s = NAN, ring_to_screen_s = NAN;

inline bool is_void(const std::string &s) { return s.empty() || s == "unknown" || s == "unavailable"; }

inline void on_ring(uint32_t now) { ring_ms = now | 1; }

inline void on_stamp(const std::string &s, uint32_t now) {
  if (!primed) {  // whatever HA holds at connect is old news
    primed = true;
    stamp = s;
    return;
  }
  if (s == stamp || is_void(s)) {
    stamp = s;
    return;
  }
  stamp = s;
  if (first_change_ms == 0)
    first_change_ms = now | 1;
  last_change_ms = now | 1;
}

inline void on_text(const std::string &t, uint32_t now) {
  text = t;
  if (last_change_ms != 0)
    last_change_ms = now | 1;  // part of the transcript that is arriving
}

inline void on_device(const std::string &d) { device = d; }

inline void on_speaker(const std::string &s, uint32_t now) {
  speaker_in = s;
  speaker_ms = now | 1;
  if (last_change_ms != 0)
    last_change_ms = now | 1;
}

inline void on_message(const std::string &m, uint32_t now) {
  message_in = m;
  message_ms = now | 1;
  if (last_change_ms != 0)
    last_change_ms = now | 1;
}

// Whisper writes symbols like "♪♪" or "¶¶" for silence or noise: nothing to show at the door. A word needs a letter
// or digit: ASCII, or a UTF-8 lead byte of Latin-1 letters / Latin Extended (0xC3..0xC9; 0xC2 is symbols like ¶ °).
inline bool has_word(const std::string &s) {
  for (unsigned char c : s)
    if ((c >= '0' && c <= '9') || (c >= 'A' && c <= 'Z') || (c >= 'a' && c <= 'z') || (c >= 0xC3 && c <= 0xC9))
      return true;
  return false;
}

inline void close() {
  if (active)
    close_request = true;
}

// T3 (2026-10-01): the words used to go after 60 s although the conversation was still on, so a visitor who looked a
// little later saw "Verbunden" without them. Now they stay until the conversation ends (2 min without sound).
inline void set_conversation(bool on) {
  conversation = on;
  if (!on)
    close();
}

// one line, whitespace collapsed
inline std::string clean(const std::string &in) {
  std::string out;
  bool space = false;
  for (char c : in) {
    if (c == ' ' || c == '\n' || c == '\r' || c == '\t') {
      space = !out.empty();
    } else {
      if (space)
        out += ' ';
      out += c;
      space = false;
    }
  }
  return out;
}

// Called often. refresh_done: no picture pending or running. Returns PAGE and/or MEASURED.
inline int update(uint32_t now, bool refresh_done) {
  int r = NOTHING;
  if (last_change_ms != 0 && now - last_change_ms >= SETTLE_MS) {
    const uint32_t arrived = first_change_ms;
    first_change_ms = last_change_ms = 0;
    const std::string m = clean(message_in);
    const std::string t = m.empty() ? clean(text) : m;
    if (!has_word(t)) {
      ESP_LOGI("talk", "transcript without words ignored (%u bytes)", (unsigned) t.size());
    } else {
      msg = t;
      from = is_void(device) ? std::string() : device;
      speaker = is_void(speaker_in) ? std::string() : clean(speaker_in);
      arrived_ms = arrived;
      const bool answers = ring_ms != 0 && arrived - ring_ms < RING_WINDOW_MS;
      ring_to_text_s = answers ? (arrived - ring_ms) / 1000.0f : NAN;
      ring_to_screen_s = NAN;
      active = true;
      close_request = drawn = measured = false;
      ESP_LOGI("talk", "transcript (%u chars) from '%s', speaker '%s', %.1f s after the ring", (unsigned) msg.size(),
               from.c_str(), speaker.c_str(), ring_to_text_s);
      r |= PAGE;
    }
  }
  if (active && drawn && !measured && refresh_done) {
    measured = true;
    if (!std::isnan(ring_to_text_s))
      ring_to_screen_s = (now - ring_ms) / 1000.0f;
    ESP_LOGI("talk", "on screen %.1f s after the ring (%u ms after the transcript)", ring_to_screen_s,
             (unsigned) (now - arrived_ms));
    r |= MEASURED;
  }
  if (active && (close_request || (!conversation && now - arrived_ms >= SHOW_MS))) {
    active = close_request = false;
    r |= PAGE;
  }
  return r;
}

inline void seconds(char *buf, size_t n, float s) {
  const int tenths = (int) lroundf(s * 10.0f);
  snprintf(buf, n, "%d,%d s", tenths / 10, tenths % 10);
}

// Word wrap into at most max_lines lines of width w (s comes from clean(): single spaces, no leading space).
// Returns false if the text did not fit (last line marked with " ..."). Python twin tested: scratchpad wrap_test.py.
inline bool wrap(esphome::display::Display &it, esphome::font::Font *f, const std::string &s, int w, int max_lines,
                 std::string *lines, int &count) {
  using esphome::display::TextAlign;
  auto width = [&](size_t from, size_t len) {
    int x1, y1, cw, ch;
    it.get_text_bounds(0, 0, s.substr(from, len).c_str(), f, TextAlign::TOP_LEFT, &x1, &y1, &cw, &ch);
    return cw;
  };
  count = 0;
  size_t pos = 0;
  while (pos < s.size() && s[pos] == ' ')  // a leading space would never move the line on (raw call-log text)
    pos++;
  while (pos < s.size() && count < max_lines) {
    size_t end = pos;  // the line so far is s[pos, end)
    while (true) {
      size_t next = s.find(' ', end == pos ? pos : end + 1);  // end of the next word (never the space we stand on)
      if (next == std::string::npos)
        next = s.size();
      if (width(pos, next - pos) > w)
        break;
      end = next;
      if (end >= s.size())
        break;
    }
    if (end == pos) {  // the first word alone is wider than the line: cut it at a character boundary
      size_t next = s.find(' ', pos);
      if (next == std::string::npos)
        next = s.size();
      size_t cut = next - pos;
      while (cut > 0 && width(pos, cut) > w) {
        cut--;
        while (cut > 0 && ((uint8_t) s[pos + cut] & 0xC0) == 0x80)
          cut--;
      }
      if (cut == 0) {  // not even one character fits: take one anyway
        cut = 1;
        while (pos + cut < s.size() && ((uint8_t) s[pos + cut] & 0xC0) == 0x80)
          cut++;
      }
      end = pos + cut;
    }
    lines[count++] = s.substr(pos, end - pos);
    pos = end;
    while (pos < s.size() && s[pos] == ' ')
      pos++;
  }
  if (pos >= s.size())
    return true;
  lines[count - 1] += " ...";  // (rare) more than fits: mark the cut
  return false;
}

// Draws the whole page and returns true while a message is shown.
inline bool draw(esphome::display::Display &it) {
  using esphome::display::COLOR_OFF;
  using esphome::display::COLOR_ON;
  using esphome::display::TextAlign;
  const Assets &a = assets;
  if (!active || a.big == nullptr)
    return false;
  drawn = true;
  it.fill(COLOR_OFF);

  it.print(24, 22, a.icon, COLOR_ON, TextAlign::TOP_LEFT, "\U0000e029");  // mic
  if (speaker.empty()) {
    it.print(112, 58, a.title, COLOR_ON, TextAlign::CENTER_LEFT, "Nachricht");
  } else {  // "Max sagt:" in the Latin-Core font (names are free text); smaller if it would not fit
    const std::string title = speaker + " sagt:";
    int x1, y1, w, h;
    it.get_text_bounds(0, 0, title.c_str(), a.big, TextAlign::TOP_LEFT, &x1, &y1, &w, &h);
    it.print(112, 58, w <= 404 ? a.big : a.small, COLOR_ON, TextAlign::CENTER_LEFT, title.c_str());
  }
  if (!from.empty())
    it.print(112, 104, a.info, COLOR_ON, TextAlign::CENTER_LEFT, from.c_str());
  it.line(24, 140, 516, 140, COLOR_ON);
  it.line(24, 141, 516, 141, COLOR_ON);

  static std::string lines[16];
  int n = 0;
  const int top = 168, bottom = 840;
  esphome::font::Font *f = a.big;
  int step = 52;
  if (!wrap(it, f, msg, 492, (bottom - top) / step, lines, n)) {
    f = a.small;
    step = 42;
    wrap(it, f, msg, 492, (bottom - top) / step, lines, n);
  }
  for (int k = 0; k < n; k++)
    it.print(24, top + k * step, f, COLOR_ON, TextAlign::TOP_LEFT, lines[k].c_str());

  // speed test line
  it.line(24, 860, 516, 860, COLOR_ON);
  char t1[16], t2[16], buf[96];
  if (std::isnan(ring_to_text_s)) {
    it.print(24, 874, a.info, COLOR_ON, TextAlign::TOP_LEFT, "ohne Klingeln davor");
  } else {
    seconds(t1, sizeof t1, ring_to_text_s);
    if (std::isnan(ring_to_screen_s))
      snprintf(buf, sizeof buf, "Klingeln bis Text %s", t1);
    else {
      seconds(t2, sizeof t2, ring_to_screen_s);
      snprintf(buf, sizeof buf, "Klingeln bis Text %s, bis Bild %s", t1, t2);
    }
    it.print(24, 874, a.info, COLOR_ON, TextAlign::TOP_LEFT, buf);
  }
  it.print(516, 910, a.info, COLOR_ON, TextAlign::TOP_RIGHT, "antippen: schließen");
  return true;
}

}  // namespace aikos_talk
