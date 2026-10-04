// aikos Intercom Screen: the door UI (proposal 1, canvas "Türbildschirm UI", 2026-09-30), portrait 540 x 960.
//
// One start page with a "stage" on top (rest / "Es klingelt") and four tiles below; the answer "<name> sagt:" is its
// own page. NO FLASH only where the change mostly ADDS ink: rest -> "Es klingelt", a new transcript on the open answer
// page, the recording bar, drawing strokes. Everything else is a true page change (short flash, ~1 s): partial
// updates that lighten large areas or paint grey fills over old content leave ghosts (the owner's photo 2026-09-30:
// the old note and tile icons showed through the grey consent band after a partial rest -> answer switch).
// Rules from the bench (UX-SCREEN-RULES.md): visitor text >= 32 px, touch areas >= 90 px, 24 px margin,
// only well separated greys, lines >= 2 px, nothing animates endlessly.
// The door reveals nothing: never "nobody home", never the alarm state, never setup from outside.
// Placeholder copy: the owner writes the wording.
//
// Voice v2 (R17, 2026-10-01): after a ring the visitor taps "Sprechen" once and then just talks; the call page shows
// who inside speaks or listens and the whole call as a chat (from aikos's call log). A new chat line that still fits
// below the last one only adds ink (no flash); a line that needs a new page, paging back, or a vanishing button
// flashes. "Nachricht hinterlassen" stays until someone answers. No notice about text at the door any more (R17.17).
//
// Uses aikos_talk (talk/talk_page.h: wrap), aikos_call (call/call_page.h: the call) and demo:: (demo/demo.h).
#pragma once

#include <algorithm>
#include <cstdint>
#include <cstdio>
#include <string>
#include "esphome/components/display/display.h"
#include "esphome/components/font/font.h"
#include "esphome/components/qr_code/qr_code.h"
#include "esphome/core/log.h"

namespace door_ui {

using esphome::display::Display;
using esphome::display::TextAlign;
using Font = esphome::font::Font;

// paper grey 0 (black) .. 255 (white); the driver draws COLOR_ON as black ink
inline esphome::Color paper(int grey) {
  const uint8_t c = 255 - grey;
  return esphome::Color(c, c, c);
}
inline const esphome::Color INK = esphome::display::COLOR_ON;
inline const esphome::Color PAPER = esphome::display::COLOR_OFF;
inline const esphome::Color MID = paper(140);    // grey text: level 8, clearly lighter than black
inline const esphome::Color LIGHT = paper(205);  // band fill: level 12

namespace icon {
static const char *const DOORBELL = "\U0000efff";
static const char *const SOUTH = "\U0000f1e3";
static const char *const RINGING = "\U0000e7f7";  // notifications_active
static const char *const BEDTIME = "\U0000f159";
static const char *const PACKAGE = "\U0000f569";
static const char *const PERSON_SEARCH = "\U0000f106";
static const char *const MIC = "\U0000e31d";
static const char *const DRAW = "\U0000e746";
static const char *const QR = "\U0000e00a";
static const char *const VOICE = "\U0000e91f";  // record_voice_over
static const char *const SUBTITLES = "\U0000e048";
static const char *const WAVE = "\U0000e1b8";  // graphic_eq
static const char *const VOICEMAIL = "\U0000e0d9";
static const char *const BACK = "\U0000e5c4";
static const char *const GROUPS = "\U0000f233";
static const char *const PERSON = "\U0000f0d3";
static const char *const SEND = "\U0000e163";
static const char *const CLOSE = "\U0000e5cd";
static const char *const CHECK = "\U0000f0be";
static const char *const ERASER = "\U0000e6d0";
static const char *const UP = "\U0000e5ce";    // expand_less
static const char *const DOWN = "\U0000e5cf";  // expand_more
}  // namespace icon

struct Assets {
  Font *r32 = nullptr, *r40 = nullptr;                     // Roboto regular, Latin Core (free text from HA)
  Font *m32 = nullptr, *m40 = nullptr, *m48 = nullptr;     // Roboto medium
  Font *b44 = nullptr, *b48 = nullptr, *b60 = nullptr;     // Roboto bold
  Font *i48 = nullptr, *i64 = nullptr, *i96 = nullptr, *i120 = nullptr;  // Material Symbols
  esphome::qr_code::QrCode *friends = nullptr;
};
inline Assets a;

enum View { START, RINGING, CALL, PICK, MESSAGE, RECORDING, SENT, DRAW, FRIENDS };
static const char *const VIEW_NAMES[] = {"start", "ringing", "call", "pick", "message", "recording", "sent", "draw", "friends"};

static const uint32_t WAIT_MS = 45000;        // ringing: offer the message after this
static const uint32_t RING_SHOW_MS = 120000;  // ringing: back to rest after this
static const uint32_t SUBPAGE_IDLE_MS = 60000;
static const uint32_t REC_MAX_MS = 60000;
static const uint32_t SENT_SHOW_MS = 15000;
static const uint32_t CLEANUP_MS = 120000;    // a flash 2 min after the last change, while nobody looks
static const int MAX_TARGETS = 5;
static const uint32_t SPEAK_GRACE_MS = 8000;  // after "Sprechen" the call page waits this long for the talk computer

// state
inline View view = START;
inline uint32_t view_ms = 0, ring_ms = 0, last_touch_ms = 0, last_change_ms = 0, rec_ms = 0;
inline bool waited = false, talking = false, quiet = false, sent_drawing = false;
inline int rec_step = -1;
inline uint32_t seen_transcript = 0;
inline bool call_active = false, seen_call = false;  // a room key answered (HA: the talk computer's "In call")
inline std::string language, language_name;          // spoken language of the transcript (§6), "de" = none shown
inline std::string sign, note, ring_target = "allen im Haus";
inline std::string targets[MAX_TARGETS] = {"Alle im Haus"};
inline int n_targets = 1;
inline uint32_t partials_since_flash = 0;
// the call page's chat: messages [chat_first, n) are on the screen; latest = it follows new messages
inline int chat_first = 0;
inline bool chat_latest = true, shown_answered = false, speak_request = false;
inline uint32_t seen_chat = 0, seen_status = 0, speak_ms = 0;
inline Display *disp = nullptr;  // for measuring text outside the draw lambda (set at boot)
// requests to the YAML glue
inline bool want_page = false, want_partial = false;
inline bool full_needed = true;  // false = only new ink on the canvas: draw just that onto the last picture
// drawing
inline bool stroke = false;
inline int last_x = 0, last_y = 0;
static const int CANVAS_TOP = 133, CANVAS_BOTTOM = 686;

inline bool is_home(View v) { return v == START || v == RINGING || v == CALL; }

// no flash only when the new picture mostly adds ink to the old one (v2: ringing swaps the tiles for two buttons)
inline bool ink_only(View from, View to) { return from == to; }

// flash: a page change even on the same view (new content that erases old content, UX rule "erasing = flash")
inline void go(View v, uint32_t now, bool flash = false) {
  const bool page = flash || !ink_only(view, v);
  if (v != view) {
    ESP_LOGI("ui", "%s -> %s (%s)", VIEW_NAMES[view], VIEW_NAMES[v], page ? "page change" : "partial");
    talking = false;  // only a new view lets go of the talk button, new words on the same page must not
    stroke = false;
  }
  view = v;
  view_ms = now;
  full_needed = true;
  (page ? want_page : want_partial) = true;
}
inline void changed() {
  want_partial = true;
  full_needed = true;
}

// ---------------------------------------------------------------------------------------------- inputs
inline void rang(uint32_t now) {  // the brass button (either path, first one)
  ring_ms = now;
  waited = false;
  ring_target = "allen im Haus";
  go(RINGING, now);
}

// new wording in place = a small partial update; appearing or vanishing moves the layout = a page change
inline void set_sign(const std::string &s) {
  const bool moves = s.empty() != sign.empty();
  sign = s;
  if (view == START) {
    changed();
    if (moves)
      want_page = true;
  }
}
inline void set_note(const std::string &s) {
  const bool moves = s.empty() != note.empty();
  note = s;
  if (view == START || view == RINGING) {
    changed();
    if (moves)
      want_page = true;
  }
}
inline void set_quiet(bool q) {  // the stage and a whole tile swap: a page change
  quiet = q;
  if (view == START) {
    full_needed = true;
    want_page = true;
  }
}
inline void set_targets(const std::string &csv) {
  n_targets = 0;
  size_t pos = 0;
  while (pos <= csv.size() && n_targets < MAX_TARGETS) {
    size_t end = csv.find(',', pos);
    if (end == std::string::npos)
      end = csv.size();
    std::string t = csv.substr(pos, end - pos);
    while (!t.empty() && t.front() == ' ')
      t.erase(0, 1);
    while (!t.empty() && t.back() == ' ')
      t.pop_back();
    if (!t.empty())
      targets[n_targets++] = t;
    pos = end + 1;
  }
  if (n_targets == 0) {
    targets[0] = "Alle im Haus";
    n_targets = 1;
  }
  if (view == PICK)
    changed();
}

// The call state comes straight from the talk computer (its encrypted broadcast, every second) and, as a fallback,
// from HA. Without HA the screen still keeps the call page (system test F2, 2026-10-01: it fell back to the start page
// after ~7 s because it only knew the call through HA).
inline bool ha_call = false, direct_call = false;
inline uint32_t direct_ms = 0;
static const uint32_t DIRECT_FRESH_MS = 3000;
inline void set_call(bool on) { ha_call = on; }  // via Home Assistant
inline void set_call_direct(bool on, uint32_t now) {
  direct_call = on;
  direct_ms = now | 1;
}
inline void set_language(const std::string &code, const std::string &name) {  // v2: the call log carries it
  language = code;
  language_name = name;
}

// ---------------------------------------------------------------------------------------------- drawing helpers
// Speed: ESPHome sets every pixel of a filled_rectangle() on its own; a page of frames took over 1.2 s and swallowed
// touches (drawing hardly worked). The driver's fill_rect() writes whole buffer rows; set at boot.
inline void (*fast_rect)(int x, int y, int w, int h, esphome::Color c) = nullptr;
inline void rect(Display &it, int x, int y, int w, int h, esphome::Color c) {
  if (w <= 0 || h <= 0)
    return;
  if (fast_rect != nullptr)
    fast_rect(x, y, w, h, c);
  else
    it.filled_rectangle(x, y, w, h, c);
}
inline void fill_round(Display &it, int x, int y, int w, int h, int r, esphome::Color c) {
  r = std::max(0, std::min(r, std::min(w, h) / 2));
  const int cx0 = x + r, cx1 = x + w - 1 - r, cy0 = y + r, cy1 = y + h - 1 - r;
  rect(it, cx0, y, cx1 - cx0 + 1, h, c);
  rect(it, x, cy0, w, cy1 - cy0 + 1, c);
  if (r > 0) {
    it.filled_circle(cx0, cy0, r, c);
    it.filled_circle(cx1, cy0, r, c);
    it.filled_circle(cx0, cy1, r, c);
    it.filled_circle(cx1, cy1, r, c);
  }
}
// an outline only (the page is already paper): four bands and four quarter rings
inline void frame(Display &it, int x, int y, int w, int h, int r, int t, esphome::Color line, esphome::Color inside) {
  (void) inside;
  r = std::max(t, std::min(r, std::min(w, h) / 2));
  rect(it, x + r, y, w - 2 * r, t, line);
  rect(it, x + r, y + h - t, w - 2 * r, t, line);
  rect(it, x, y + r, t, h - 2 * r, line);
  rect(it, x + w - t, y + r, t, h - 2 * r, line);
  const int ro = 4 * r * r, ri = 4 * (r - t) * (r - t);  // doubled units: pixel centres sit at .5
  for (int dy = 0; dy < r; dy++) {
    for (int dx = 0; dx < r; dx++) {
      const int ex = 2 * (r - dx) - 1, ey = 2 * (r - dy) - 1;  // twice the distance from the corner centre
      const int d = ex * ex + ey * ey;
      if (d > ro || d <= ri)
        continue;
      it.draw_pixel_at(x + dx, y + dy, line);                  // top left
      it.draw_pixel_at(x + w - 1 - dx, y + dy, line);          // top right
      it.draw_pixel_at(x + dx, y + h - 1 - dy, line);          // bottom left
      it.draw_pixel_at(x + w - 1 - dx, y + h - 1 - dy, line);  // bottom right
    }
  }
}

enum Action {
  NONE,
  GO_PICK,
  GO_MESSAGE,
  GO_DRAW,
  GO_FRIENDS,
  GO_BACK,
  TARGET,
  RECORD,
  SEND,
  CANCEL,
  CLEAR,
  SEND_DRAWING,
  SPEAK,
  OLDER,
  NEWEST
};
struct Hit {
  int x, y, w, h, action, arg;
};
inline Hit hits[16];
inline int n_hits = 0;
inline void hit(int x, int y, int w, int h, int action, int arg = 0) {
  if (n_hits < 16)
    hits[n_hits++] = Hit{x, y, w, h, action, arg};
}

// wrapped text; returns the number of lines
inline int text(Display &it, Font *f, int x, int y, int step, esphome::Color c, TextAlign align, const std::string &s,
                int width, int max_lines) {
  static std::string lines[8];
  int n = 0;
  aikos_talk::wrap(it, f, s, width, std::min(max_lines, 8), lines, n);
  for (int k = 0; k < n; k++)
    it.print(x, y + k * step, f, c, align, lines[k].c_str());
  return n;
}
inline int count_lines(Display &it, Font *f, const std::string &s, int width, int max_lines) {
  static std::string lines[8];
  int n = 0;
  aikos_talk::wrap(it, f, s, width, std::min(max_lines, 8), lines, n);
  return n;
}

inline void back_button(Display &it) {
  frame(it, 24, 24, 200, 90, 16, 3, INK, PAPER);
  it.print(38, 69, a.i48, INK, TextAlign::CENTER_LEFT, icon::BACK);
  it.print(96, 69, a.m32, INK, TextAlign::CENTER_LEFT, "Zurück");
  hit(24, 24, 200, 90, GO_BACK);
}

// a wide button: icon + one or two label lines, centred
inline void wide_button(Display &it, int y, int h, bool filled, const char *ico, Font *ifont, Font *f, const char *l1,
                        const char *l2, int action, int border = 3) {
  const esphome::Color fg = filled ? PAPER : INK;
  if (filled)
    fill_round(it, 24, y, 492, h, 20, INK);
  else
    frame(it, 24, y, 492, h, 20, border, INK, PAPER);
  int x1, y1, w1, h1, w2 = 0;
  it.get_text_bounds(0, 0, l1, f, TextAlign::TOP_LEFT, &x1, &y1, &w1, &h1);
  if (l2 != nullptr)
    it.get_text_bounds(0, 0, l2, f, TextAlign::TOP_LEFT, &x1, &y1, &w2, &h1);
  int iw = 0;
  if (ico != nullptr)
    it.get_text_bounds(0, 0, ico, ifont, TextAlign::TOP_LEFT, &x1, &y1, &iw, &h1);
  const int gap = ico != nullptr ? 18 : 0;
  const int total = iw + gap + std::max(w1, w2);
  const int x = 270 - total / 2;
  const int cy = y + h / 2;
  if (ico != nullptr)
    it.print(x, cy, ifont, fg, TextAlign::CENTER_LEFT, ico);
  if (l2 == nullptr) {
    it.print(x + iw + gap, cy, f, fg, TextAlign::CENTER_LEFT, l1);
  } else {
    it.print(x + iw + gap, cy - 2, f, fg, TextAlign::BOTTOM_LEFT, l1);
    it.print(x + iw + gap, cy + 2, f, fg, TextAlign::TOP_LEFT, l2);
  }
  hit(24, y, 492, h, action);
}

// ---------------------------------------------------------------------------------------------- pages
inline void draw_stage(Display &it) {  // y 24 .. 404, centred column
  const int top = 24, height = 380, W = 470;
  if (view == RINGING) {
    const std::string who = "bei " + ring_target;
    const std::string status = waited ? "Niemand kommt? Hinterlassen Sie gern eine Nachricht." : "Einen Moment bitte.";
    const int n_who = count_lines(it, a.r40, who, W, 2), n_st = count_lines(it, a.r32, status, W, 3);
    const int h = 120 + 10 + 66 + 10 + n_who * 48 + 14 + n_st * 40;
    int y = top + (height - h) / 2;
    it.print(270, y, a.i120, INK, TextAlign::TOP_CENTER, icon::RINGING);
    y += 130;
    it.print(270, y, a.b60, INK, TextAlign::TOP_CENTER, "Es klingelt");
    y += 76;
    y += text(it, a.r40, 270, y, 48, INK, TextAlign::TOP_CENTER, who, W, 2) * 48 + 14;
    text(it, a.r32, 270, y, 40, waited ? INK : MID, TextAlign::TOP_CENTER, status, W, 3);
  } else if (quiet) {
    const std::string s = "Die Klingel ist jetzt leise. Hinterlassen Sie gern eine Nachricht.";
    const int n = count_lines(it, a.r32, s, W, 3);
    const int h = 96 + 14 + 56 + 14 + n * 40;
    int y = top + (height - h) / 2;
    it.print(270, y, a.i96, INK, TextAlign::TOP_CENTER, icon::BEDTIME);
    y += 110;
    it.print(270, y, a.m48, INK, TextAlign::TOP_CENTER, "Ruhezeit");
    y += 70;
    text(it, a.r32, 270, y, 40, INK, TextAlign::TOP_CENTER, s, W, 3);
  } else {
    const std::string s = "Zum Klingeln den Messingknopf drücken";
    const int n = count_lines(it, a.m40, s, 492, 3);
    const int h = (sign.empty() ? 0 : 40 + 14) + 96 + 14 + n * 48 + 14 + 64;
    int y = top + (height - h) / 2;
    if (!sign.empty()) {
      text(it, a.r32, 270, y, 40, MID, TextAlign::TOP_CENTER, sign, W, 1);
      y += 54;
    }
    it.print(270, y, a.i96, INK, TextAlign::TOP_CENTER, icon::DOORBELL);
    y += 110;
    y += text(it, a.m40, 270, y, 48, INK, TextAlign::TOP_CENTER, s, 492, 3) * 48 + 14;
    it.print(270, y, a.i64, INK, TextAlign::TOP_CENTER, icon::SOUTH);
  }
}

inline void draw_home(Display &it) {
  draw_stage(it);
  int y0 = 424;
  if (!note.empty()) {
    const int n = count_lines(it, a.r32, note, 380, 2);
    const int h = std::max(48, n * 40) + 32;
    frame(it, 24, y0, 492, h, 16, 3, INK, PAPER);
    it.print(44, y0 + h / 2, a.i48, INK, TextAlign::CENTER_LEFT, icon::PACKAGE);
    text(it, a.r32, 108, y0 + (h - n * 40) / 2 + 2, 40, INK, TextAlign::TOP_LEFT, note, 380, 2);
    y0 += h + 20;
  }
  if (view == RINGING) {  // v2 (the owner): "Sprechen" right after the ring; the message until someone answers
    wide_button(it, y0, 180, true, icon::MIC, a.i64, a.m40, "Sprechen", "einmal antippen", SPEAK);
    wide_button(it, y0 + 200, 110, !waited ? false : true, icon::VOICEMAIL, a.i48, a.m32, "Nachricht hinterlassen",
                nullptr, GO_MESSAGE);
    return;
  }
  const int th = (936 - y0 - 16) / 2, tw = 238;
  struct Tile {
    const char *ico, *l1, *l2;
    int action;
  };
  static const Tile TILES[4] = {{icon::PERSON_SEARCH, "Bei jemandem", "klingeln", GO_PICK},
                                {icon::MIC, "Nachricht", "hinterlassen", GO_MESSAGE},
                                {icon::DRAW, "Malen", nullptr, GO_DRAW},
                                {icon::QR, "Für Freunde", nullptr, GO_FRIENDS}};
  const bool msg_hot = (view == RINGING && waited) || (view == START && quiet);
  for (int k = 0; k < 4; k++) {
    const int x = 24 + (k % 2) * (tw + 16), y = y0 + (k / 2) * (th + 16);
    const bool hot = k == 1 && msg_hot;
    const esphome::Color fg = hot ? PAPER : INK;
    if (hot)
      fill_round(it, x, y, tw, th, 18, INK);
    else
      frame(it, x, y, tw, th, 18, 3, INK, PAPER);
    it.print(x + 16, y + 16, a.i64, fg, TextAlign::TOP_LEFT, TILES[k].ico);
    const int lines = TILES[k].l2 == nullptr ? 1 : 2;
    const int ly = y + th - 16 - lines * 38;
    it.print(x + 16, ly, a.m32, fg, TextAlign::TOP_LEFT, TILES[k].l1);
    if (TILES[k].l2 != nullptr)
      it.print(x + 16, ly + 38, a.m32, fg, TextAlign::TOP_LEFT, TILES[k].l2);
    hit(x, y, tw, th, TILES[k].action);
  }
}

// ── the call page: who speaks, who listens, the chat
static const int CHAT_TOP = 190, BUBBLE_W = 430, PAD = 14, LABEL_H = 38, LINE_H = 40, BUBBLE_GAP = 14;
static const int PAGE_BTN_H = 90;  // "Ältere" / "Neueste": touch areas >= 90 px

inline int chat_bottom() { return aikos_call::answered ? 936 : 822; }  // the message button until someone answers
inline int bubble_h(const aikos_call::Msg &m) {
  const int n = disp != nullptr ? count_lines(*disp, a.r32, m.text, BUBBLE_W - 2 * PAD, 6) : 2;
  return PAD + LABEL_H + std::max(1, n) * LINE_H + PAD;
}
// the bubble heights of the current chat, measured once per change of the chat. Measuring text is slow: when every
// layout question measured every bubble again, the UI tick grew from 127 to 222 ms per message at 16 messages (call of
// 2026-10-02 09:54, long YouTube transcripts).
inline int heights[aikos_call::MAX_MSGS];
inline uint32_t heights_version = 0xFFFFFFFF;
inline int msg_h(int i) {
  if (heights_version != aikos_call::chat_version) {
    for (int k = 0; k < aikos_call::n_msgs; k++)
      heights[k] = bubble_h(aikos_call::msgs[k]);
    heights_version = aikos_call::chat_version;
  }
  return heights[i];
}
inline int area_top(int first) { return CHAT_TOP + (first > 0 ? PAGE_BTN_H + BUBBLE_GAP : 0); }
inline int area_bottom(bool latest) { return chat_bottom() - (latest ? 0 : PAGE_BTN_H + BUBBLE_GAP); }
// do messages [first, n) fit on the page?
inline bool chat_fits(int first, bool latest) {
  int y = area_top(first);
  for (int i = first; i < aikos_call::n_msgs; i++)
    y += msg_h(i) + BUBBLE_GAP;
  return y - BUBBLE_GAP <= area_bottom(latest);
}
// the first message of the page that ends with the newest one
inline int newest_page_first() {
  for (int first = 0; first < aikos_call::n_msgs; first++)
    if (chat_fits(first, true))
      return first;
  return std::max(0, aikos_call::n_msgs - 1);
}
// the page before `first`: as many older messages as fit, ending just before it
inline int older_page_first(int first) {
  const int bottom = area_bottom(false);
  int y = bottom, k = first;
  while (k > 0) {
    const int h = msg_h(k - 1) + BUBBLE_GAP;
    const int top = area_top(k - 1 > 0 ? 1 : 0);
    if (y - h < top && k < first)
      break;
    y -= h;
    k--;
  }
  return k;
}

inline void draw_bubble(Display &it, const aikos_call::Msg &m, int y) {
  const bool visitor = m.side == "door";
  const int h = bubble_h(m), x = visitor ? 24 : 516 - BUBBLE_W;
  if (visitor)
    frame(it, x, y, BUBBLE_W, h, 16, 3, INK, PAPER);
  else
    fill_round(it, x, y, BUBBLE_W, h, 16, LIGHT);
  text(it, a.m32, x + PAD, y + PAD, LABEL_H, visitor ? INK : INK, TextAlign::TOP_LEFT, aikos_call::label(m),
       BUBBLE_W - 2 * PAD, 1);
  text(it, a.r32, x + PAD, y + PAD + LABEL_H, LINE_H, INK, TextAlign::TOP_LEFT, m.text, BUBBLE_W - 2 * PAD, 6);
}

inline void draw_call(Display &it) {
  // status: who speaks inside, or the visitor's turn. Only the text changes (a small partial update).
  const std::string sp = aikos_call::speaking();
  const std::string status = sp.empty() ? std::string("Bitte jetzt sprechen") : sp;
  frame(it, 24, 24, 492, 100, 18, 3, INK, PAPER);
  it.print(46, 74, a.i64, INK, TextAlign::CENTER_LEFT, sp.empty() ? icon::MIC : icon::WAVE);
  int x1, y1, w, h;
  it.get_text_bounds(0, 0, status.c_str(), a.b44, TextAlign::TOP_LEFT, &x1, &y1, &w, &h);
  it.print(124, 74, w <= 372 ? a.b44 : a.m32, INK, TextAlign::CENTER_LEFT, status.c_str());
  // who listens inside (the owner: with names)
  const std::string ls = aikos_call::listeners();
  text(it, a.r32, 24, 136, 40, MID, TextAlign::TOP_LEFT, ls.empty() ? std::string("Mikrofon an") : ls, 492, 1);
  // the chat
  if (aikos_call::n_msgs == 0) {
    text(it, a.r32, 24, CHAT_TOP + 20, 40, MID, TextAlign::TOP_LEFT, "Hier erscheint das Gespräch als Text.", 492, 2);
  } else {
    if (chat_first > 0) {
      wide_button(it, CHAT_TOP, PAGE_BTN_H, false, icon::UP, a.i48, a.m32, "Ältere", nullptr, OLDER, 2);
    }
    int y = area_top(chat_first);
    const int bottom = area_bottom(chat_latest);
    for (int i = chat_first; i < aikos_call::n_msgs; i++) {
      const int bh = msg_h(i);
      if (y + bh > bottom)
        break;  // the rest is on the next page ("Neueste")
      draw_bubble(it, aikos_call::msgs[i], y);
      y += bh + BUBBLE_GAP;
    }
    if (!chat_latest)
      wide_button(it, chat_bottom() - PAGE_BTN_H, PAGE_BTN_H, false, icon::DOWN, a.i48, a.m32, "Neueste", nullptr,
                  NEWEST, 2);
  }
  if (!aikos_call::answered)
    wide_button(it, 836, 100, false, icon::VOICEMAIL, a.i48, a.m32, "Nachricht hinterlassen", nullptr, GO_MESSAGE);
  shown_answered = aikos_call::answered;
}

inline void draw_pick(Display &it) {
  back_button(it);
  const int n = text(it, a.b44, 24, 134, 52, INK, TextAlign::TOP_LEFT, "Bei wem möchten Sie klingeln?", 492, 2);
  int y = 134 + n * 52 + 20;
  for (int k = 0; k < n_targets; k++) {
    frame(it, 24, y, 492, 104, 18, 3, INK, PAPER);
    it.print(46, y + 52, a.i64, INK, TextAlign::CENTER_LEFT, k == 0 ? icon::GROUPS : icon::PERSON);
    text(it, a.r40, 130, y + 28, 48, INK, TextAlign::TOP_LEFT, targets[k], 370, 1);
    hit(24, y, 492, 104, TARGET, k);
    y += 118;
  }
}

inline void draw_message(Display &it) {
  back_button(it);
  it.print(24, 138, a.i96, INK, TextAlign::TOP_LEFT, icon::VOICEMAIL);
  const int n = text(it, a.b48, 24, 252, 56, INK, TextAlign::TOP_LEFT, "Nachricht hinterlassen", 492, 2);
  text(it, a.r32, 24, 252 + n * 56 + 16, 42, INK, TextAlign::TOP_LEFT,
       "Wir nehmen Ihre Nachricht auf, zeigen sie als Text an und speichern sie für die Bewohner.", 492, 4);
  fill_round(it, 24, 700, 492, 180, 20, INK);
  it.filled_circle(128, 790, 26, PAPER);
  it.print(176, 790, a.m40, PAPER, TextAlign::CENTER_LEFT, "Aufnahme starten");
  hit(24, 700, 492, 180, RECORD);
  it.print(270, 900, a.r32, MID, TextAlign::TOP_CENTER, "Höchstens 1 Minute");
}

inline void draw_recording(Display &it) {
  it.filled_circle(56, 76, 26, INK);
  it.print(100, 76, a.b48, INK, TextAlign::CENTER_LEFT, "Aufnahme läuft");
  // the bar only ever gets darker: ink-only changes leave no ghosts
  const int steps = REC_MAX_MS / 5000, done = std::min(rec_step + 1, steps);
  frame(it, 24, 128, 492, 40, 10, 3, INK, PAPER);
  if (done > 0)
    rect(it, 27, 131, (486 * done) / steps, 34, INK);
  char buf[16];  // elapsed in 5 s steps, like the bar
  snprintf(buf, sizeof buf, "%u:%02u", (unsigned) (done * 5 / 60), (unsigned) (done * 5 % 60));
  it.print(24, 180, a.r32, INK, TextAlign::TOP_LEFT, buf);
  it.print(516, 180, a.r32, MID, TextAlign::TOP_RIGHT, "1:00");
  it.print(24, 236, a.r32, MID, TextAlign::TOP_LEFT, "Erkannt:");
  frame(it, 24, 280, 492, 340, 18, 3, INK, PAPER);
  text(it, a.r32, 48, 304, 42, MID, TextAlign::TOP_LEFT, "Das Mikrofon an der Tür kommt mit dem Sprechrechner.", 444, 3);
  wide_button(it, 640, 160, true, icon::SEND, a.i64, a.m40, "Fertig, senden", nullptr, SEND);
  wide_button(it, 816, 96, false, icon::CLOSE, a.i48, a.m32, "Abbrechen", nullptr, CANCEL);
}

inline void draw_sent(Display &it) {
  it.print(270, 240, a.i120, INK, TextAlign::TOP_CENTER, icon::CHECK);
  it.print(270, 380, a.b60, INK, TextAlign::TOP_CENTER, "Danke!");
  const int n = text(it, a.r40, 270, 470, 48, INK, TextAlign::TOP_CENTER,
                     sent_drawing ? "Ihr Bild ist angekommen." : "Ihre Nachricht ist angekommen.", 492, 2);
  it.print(270, 470 + n * 48 + 40, a.r32, MID, TextAlign::TOP_CENTER, "Gleich wieder zum Start");
}

inline void draw_drawing(Display &it) {
  back_button(it);
  it.print(516, 69, a.b44, INK, TextAlign::CENTER_RIGHT, "Malen");
  frame(it, 24, 130, 492, 560, 18, 3, INK, PAPER);
  demo::canvas_draw(it, CANVAS_TOP, CANVAS_BOTTOM);
  text(it, a.r32, 24, 706, 40, INK, TextAlign::TOP_LEFT, "Mit dem Finger malen. Das Bild geht an die Bewohner.", 492, 2);
  frame(it, 24, 810, 238, 110, 18, 3, INK, PAPER);
  it.print(56, 865, a.i48, INK, TextAlign::CENTER_LEFT, icon::ERASER);
  it.print(116, 865, a.m32, INK, TextAlign::CENTER_LEFT, "Löschen");
  hit(24, 810, 238, 110, CLEAR);
  fill_round(it, 278, 810, 238, 110, 18, INK);
  it.print(318, 865, a.i48, PAPER, TextAlign::CENTER_LEFT, icon::SEND);
  it.print(378, 865, a.m32, PAPER, TextAlign::CENTER_LEFT, "Senden");
  hit(278, 810, 238, 110, SEND_DRAWING);
}

inline void draw_friends(Display &it) {
  back_button(it);
  it.print(24, 134, a.b48, INK, TextAlign::TOP_LEFT, "Für Freunde");
  const int n = text(it, a.r32, 24, 204, 42, INK, TextAlign::TOP_LEFT,
                     "Sie haben eine Einladung? Code mit dem Handy scannen und Ihre Geheimzahl eingeben. "
                     "Dann läutet Ihr eigener Klingelton.",
                     492, 5);
  if (a.friends != nullptr) {
    const int m = a.friends->get_size(), s = std::max(1, std::min(10, 280 / m));
    const int qy = 204 + n * 42 + 40;
    it.qr_code(270 - m * s / 2, qy, a.friends, INK, s);
    it.print(270, qy + m * s + 40, a.r32, MID, TextAlign::TOP_CENTER, "[Link zur Freundesseite]");
  }
}

inline void draw(Display &it) {
  if (!full_needed && view == DRAW) {  // a stroke: the canvas only gains ink, the rest of the picture stays
    demo::canvas_draw(it, CANVAS_TOP, CANVAS_BOTTOM);
    return;
  }
  full_needed = false;
  n_hits = 0;
  it.fill(PAPER);
  switch (view) {
    case START:
    case RINGING: draw_home(it); break;
    case CALL: draw_call(it); break;
    case PICK: draw_pick(it); break;
    case MESSAGE: draw_message(it); break;
    case RECORDING: draw_recording(it); break;
    case SENT: draw_sent(it); break;
    case DRAW: draw_drawing(it); break;
    case FRIENDS: draw_friends(it); break;
  }
}

// ---------------------------------------------------------------------------------------------- touch
inline void act(int action, int arg, uint32_t now) {
  switch (action) {
    case GO_PICK: go(PICK, now); break;
    case GO_MESSAGE: go(MESSAGE, now); break;
    case GO_DRAW: go(DRAW, now); break;
    case GO_FRIENDS: go(FRIENDS, now); break;
    case GO_BACK:
    case CANCEL: go(START, now); break;
    case TARGET:  // Stage 1 via HA (not wired yet): the page shows whom it rings
      ring_target = arg == 0 ? "allen im Haus" : targets[arg];
      ring_ms = now;
      waited = false;
      ESP_LOGI("ui", "targeted ring: %s", ring_target.c_str());
      go(RINGING, now);
      break;
    case RECORD:
      rec_ms = now;
      rec_step = -1;
      go(RECORDING, now);
      break;
    case SEND:
      sent_drawing = false;
      go(SENT, now);
      break;
    case SEND_DRAWING:
      sent_drawing = true;
      demo::canvas_clear();
      go(SENT, now);
      break;
    case CLEAR:  // erasing large content is practically a new page: the short flash
      demo::canvas_clear();
      want_page = true;
      break;
    case SPEAK:  // the visitor's one-time "Sprechen": straight to the talk computer, the call page at once
      speak_request = true;
      speak_ms = now | 1;
      chat_first = newest_page_first();
      chat_latest = true;
      ESP_LOGI("ui", "Sprechen");
      go(CALL, now);
      break;
    case OLDER:  // paging moves everything: a page change
      chat_first = older_page_first(chat_first);
      chat_latest = false;
      go(CALL, now, true);
      break;
    case NEWEST:
      chat_first = newest_page_first();
      chat_latest = true;
      go(CALL, now, true);
      break;
    default: break;
  }
}

inline void touch(int x, int y, uint32_t now) {
  last_touch_ms = now;
  if (view == DRAW && y > CANVAS_TOP + 4 && y < CANVAS_BOTTOM - 4 && x > 30 && x < 510) {
    demo::canvas_dot(x, y, 3, CANVAS_TOP, CANVAS_BOTTOM);
    stroke = true;
    last_x = x;
    last_y = y;
    want_partial = true;  // ink only: no full redraw
    return;
  }
  for (int k = n_hits - 1; k >= 0; k--) {
    const Hit &h = hits[k];
    if (x >= h.x && x < h.x + h.w && y >= h.y && y < h.y + h.h) {
      act(h.action, h.arg, now);
      return;
    }
  }
}

inline void move(int x, int y) {
  if (view != DRAW || !stroke || (x == last_x && y == last_y))
    return;
  demo::canvas_line(last_x, last_y, x, y, 3, CANVAS_TOP, CANVAS_BOTTOM);
  last_x = x;
  last_y = y;
  want_partial = true;  // ink only: no full redraw
}

inline void release() { stroke = false; }

// ---------------------------------------------------------------------------------------------- time
inline void tick(uint32_t now) {
  call_active = (direct_ms != 0 && now - direct_ms < DIRECT_FRESH_MS) ? direct_call : ha_call;
  // a call at the door (a key held, or the visitor tapped "Sprechen"): the call page; its end: back to the start
  if (call_active && !seen_call) {
    seen_call = true;
    if (view != CALL) {
      chat_first = newest_page_first();
      chat_latest = true;
      go(CALL, now);
    }
  } else if (!call_active) {
    seen_call = false;
    if (view == CALL && (speak_ms == 0 || now - speak_ms >= SPEAK_GRACE_MS)) {
      speak_ms = 0;
      go(START, now);
    }
  }
  if (call_active)
    speak_ms = 0;  // the talk computer took over
  // the chat changed: a line that fits below the last one only adds ink; anything else is a new page
  if (aikos_call::chat_version != seen_chat) {
    seen_chat = aikos_call::chat_version;
    // R27: the oldest may fall out of the window; the page keeps its messages if they are all still there
    const int d = aikos_call::appended ? aikos_call::dropped : 0;
    const int first = chat_first - d;
    const bool same_top = first >= 0 && (first > 0) == (chat_first > 0);  // "Ältere" stays as it is
    if (view == CALL && chat_latest) {
      if (aikos_call::appended && same_top && chat_fits(first, true)) {
        chat_first = first;
        changed();
      } else {
        chat_first = newest_page_first();
        go(CALL, now, true);
      }
    } else if (view == CALL) {  // reading older messages: stay on them unless they fell out
      if (aikos_call::appended && same_top) {
        chat_first = first;
      } else {
        chat_first = std::max(0, std::min(first, aikos_call::n_msgs - 1));
        if (aikos_call::n_msgs == 0)
          chat_latest = true;  // an emptied chat (R22): the next message is shown as it comes
        go(CALL, now, true);
      }
    }
  }
  // who speaks / who listens: the text in place; the message button vanishing: a page change
  if (aikos_call::status_version != seen_status) {
    seen_status = aikos_call::status_version;
    if (view == CALL) {
      if (aikos_call::answered != shown_answered)
        go(CALL, now, true);
      else
        changed();
    }
  }
  switch (view) {
    case RINGING:
      if (!waited && now - ring_ms >= WAIT_MS) {
        waited = true;
        changed();
      }
      if (now - ring_ms >= RING_SHOW_MS)
        go(START, now);
      break;
    case RECORDING: {
      const int step = (int) ((now - rec_ms) / 5000);
      if (now - rec_ms >= REC_MAX_MS) {
        sent_drawing = false;
        go(SENT, now);
      } else if (step != rec_step) {
        rec_step = step;
        changed();
      }
      break;
    }
    case SENT:
      if (now - view_ms >= SENT_SHOW_MS)
        go(START, now);
      break;
    case CALL:  // paged back and left alone: back to the newest lines
      if (!chat_latest && now - std::max(view_ms, last_touch_ms) >= 20000) {
        chat_first = newest_page_first();
        chat_latest = true;
        go(CALL, now, true);
      }
      break;
    case PICK:
    case MESSAGE:
    case DRAW:
    case FRIENDS:
      if (now - std::max(view_ms, last_touch_ms) >= SUBPAGE_IDLE_MS)
        go(START, now);
      break;
    default: break;
  }
  if (want_partial || want_page)
    last_change_ms = now;
  // invisible clean-up: one flash once things have rested for 2 min (nobody is looking)
  if (partials_since_flash > 0 && view == START && now - last_change_ms >= CLEANUP_MS &&
      now - last_touch_ms >= CLEANUP_MS) {
    ESP_LOGI("ui", "clean-up flash after %u partial updates", (unsigned) partials_since_flash);
    want_page = true;
  }
}

// the glue calls these after it asked the panel for a picture
inline void picture_sent(bool page) {
  if (page)
    partials_since_flash = 0;
  else
    partials_since_flash++;
}

}  // namespace door_ui
