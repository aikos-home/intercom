// aikos Intercom Screen: first Wi-Fi setup, drawn instead of the normal pages (portrait, 540 x 960).
//
// Until the screen has joined a network once, it shows a Wi-Fi QR code for its own setup network. The phone joins
// it, the captive portal opens by itself, the home Wi-Fi is picked there, and the screen shows "Verbunden".
// Once a connection has worked, the code never shows again by itself: the screen hangs at a front door, and a
// stranger must not be offered the setup network. Reset from Home Assistant to set it up anew.
#pragma once

#include <algorithm>
#include <cstdint>
#include "esphome/components/display/display.h"
#include "esphome/components/font/font.h"
#include "esphome/components/network/ip_address.h"
#include "esphome/components/qr_code/qr_code.h"
#include "esphome/components/wifi/wifi_component.h"

namespace aikos_setup {

enum State : int { NORMAL = 0, SETUP = 1, CONNECTING = 2, CONNECTED = 3, RETRY = 4 };

static const uint32_t TRY_MS = 40000;   // no connection this long after the credentials: they were wrong
static const uint32_t SHOW_OK_MS = 10000;  // "Verbunden" stays this long, then the normal pages

struct Assets {
  esphome::font::Font *title = nullptr;  // 48 px
  esphome::font::Font *text = nullptr;   // 32 px, the visitor minimum
  esphome::font::Font *icon = nullptr;   // Material Symbols, 96 px
  esphome::qr_code::QrCode *join = nullptr;    // WIFI:... for the setup network
  esphome::qr_code::QrCode *portal = nullptr;  // http://192.168.4.1
};
inline Assets assets;
inline int state = NORMAL;

// Called often (every 20 ms). proven is a restored global: true once any connection has worked.
// Returns true when the state changed, i.e. a new page is due.
inline bool update(bool &proven, uint32_t now) {
  static uint32_t creds_ms = 0, joined_ms = 0;
  auto *w = esphome::wifi::global_wifi_component;
  const bool connected = w->is_connected();
  const bool has_creds = w->has_sta();
  if (connected && !proven) {
    proven = true;
    joined_ms = now | 1;
  }
  if (joined_ms != 0 && now - joined_ms >= SHOW_OK_MS)
    joined_ms = 0;
  if (!has_creds)
    creds_ms = 0;
  else if (creds_ms == 0)
    creds_ms = now | 1;

  int s;
  if (connected)
    s = joined_ms != 0 ? CONNECTED : NORMAL;
  else if (proven)
    s = NORMAL;  // lost the network later: never offer the setup network at the door
  else if (!has_creds)
    s = SETUP;
  else
    s = now - creds_ms < TRY_MS ? CONNECTING : RETRY;  // the setup network stays up until a connection works
  if (s == state)
    return false;
  state = s;
  return true;
}

// Draws the whole page and returns true, or returns false in NORMAL (then the normal pages draw).
inline bool draw(esphome::display::Display &it) {
  using esphome::display::COLOR_OFF;
  using esphome::display::COLOR_ON;
  using esphome::display::TextAlign;
  const Assets &a = assets;
  if (state == NORMAL || a.text == nullptr)
    return false;
  it.fill(COLOR_OFF);

  if (state == SETUP || state == RETRY) {
    it.print(24, 22, a.icon, COLOR_ON, TextAlign::TOP_LEFT, "\U0000e63e");  // wifi
    it.print(132, 70, a.title, COLOR_ON, TextAlign::CENTER_LEFT, "WLAN einrichten");
    it.print(24, 132, a.text, COLOR_ON, TextAlign::TOP_LEFT,
             state == SETUP ? "Mit der Handy-Kamera scannen:" : "Hat nicht geklappt. Nochmal:");

    const int n = a.join->get_size();
    const int s = std::min(11, 330 / n);
    const int qy = 210;  // 4 modules of white above: the scanner needs its quiet zone
    it.qr_code((540 - n * s) / 2, qy, a.join, COLOR_ON, s);

    static const char *const STEPS[4][2] = {{"1", "Code scannen, beitreten"},
                                            {"2", "Heimnetz wählen und"},
                                            {"", "Passwort eingeben"},
                                            {"3", "Auf Verbunden warten"}};
    int y = qy + n * s + 40;
    for (auto &st : STEPS) {
      it.print(24, y, a.text, COLOR_ON, TextAlign::TOP_LEFT, st[0]);
      it.print(64, y, a.text, COLOR_ON, TextAlign::TOP_LEFT, st[1]);
      y += 42;
    }

    const int m = a.portal->get_size();
    const int ps = std::min(5, 125 / m);
    const int py = 928 - m * ps;  // quiet zone clear of the glass print (hides 7-9 px)
    it.line(24, py - 24, 516, py - 24, COLOR_ON);
    it.line(24, py - 23, 516, py - 23, COLOR_ON);
    it.qr_code(34, py, a.portal, COLOR_ON, ps);
    const int tx = 34 + m * ps + 24;
    it.print(tx, py - 2, a.text, COLOR_ON, TextAlign::TOP_LEFT, "Seite geht nicht auf?");
    it.print(tx, py + 40, a.text, COLOR_ON, TextAlign::TOP_LEFT, "Diesen Code scannen");
    it.print(tx, py + 82, a.text, COLOR_ON, TextAlign::TOP_LEFT, "oder 192.168.4.1");

  } else if (state == CONNECTING) {
    it.print(270, 330, a.icon, COLOR_ON, TextAlign::CENTER, "\U0000e63e");  // wifi
    it.print(270, 450, a.title, COLOR_ON, TextAlign::CENTER, "Verbinde ...");
    it.print(270, 530, a.text, COLOR_ON, TextAlign::CENTER, "mit dem Heimnetz,");
    it.print(270, 572, a.text, COLOR_ON, TextAlign::CENTER, "einen Moment");

  } else {  // CONNECTED
    it.print(270, 330, a.icon, COLOR_ON, TextAlign::CENTER, "\U0000e86c");  // check_circle
    it.print(270, 450, a.title, COLOR_ON, TextAlign::CENTER, "Verbunden");
    char ip[esphome::network::IP_ADDRESS_BUFFER_SIZE] = "";
    for (auto &addr : esphome::wifi::global_wifi_component->get_ip_addresses()) {
      if (addr.is_set() && addr.is_ip4()) {
        addr.str_to(ip);
        break;
      }
    }
    if (ip[0] != '\0')
      it.printf(270, 530, a.text, COLOR_ON, TextAlign::CENTER, "IP %s", ip);
    it.print(270, 610, a.text, COLOR_ON, TextAlign::CENTER, "Home Assistant findet");
    it.print(270, 652, a.text, COLOR_ON, TextAlign::CENTER, "den Bildschirm jetzt selbst");
  }
  return true;
}

}  // namespace aikos_setup
