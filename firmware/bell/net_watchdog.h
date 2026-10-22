// aikos Intercom Bell: network watchdog.
//
// Seen 2026-10-01 00:17 on the bench: the Ethernet link stayed "connected" but every send failed (sendto() error -1,
// HA lost the bell, ping dead) until a manual reset. Most likely the W5500 reset on a USB power dip while the ESP ran
// on, so the driver never noticed. A doorbell must come back by itself: while the link is up, send one tiny UDP
// packet to the gateway every check; if sending fails for FAIL_LIMIT checks in a row, restart. With the cable pulled
// the link is down and nothing restarts (no boot loop).
#pragma once

#include <cstdint>
#include <lwip/sockets.h>
#include <esp_netif.h>
#include "esphome/core/log.h"

namespace net_watchdog {

static const int FAIL_LIMIT = 6;  // x 5 s = 30 s of a dead network with the link up
inline int fails = 0;
inline int sock = -1;

// true = restart now
inline bool check(bool link_up) {
  if (!link_up) {
    fails = 0;
    return false;
  }
  esp_netif_t *netif = esp_netif_get_default_netif();
  esp_netif_ip_info_t info{};
  if (netif == nullptr || esp_netif_get_ip_info(netif, &info) != ESP_OK || info.gw.addr == 0) {
    fails = 0;  // no address yet: DHCP is still working on it
    return false;
  }
  if (sock < 0)
    sock = ::socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);  // ::, esphome has a socket namespace
  bool ok = false;
  if (sock >= 0) {
    sockaddr_in to{};
    to.sin_family = AF_INET;
    to.sin_addr.s_addr = info.gw.addr;
    to.sin_port = htons(9);  // discard
    const uint8_t probe = 0;
    ok = sendto(sock, &probe, 1, 0, (const sockaddr *) &to, sizeof to) == 1;
  }
  if (ok) {
    if (fails > 0)
      ESP_LOGI("netdog", "network sends again after %d failed checks", fails);
    fails = 0;
    return false;
  }
  fails++;
  ESP_LOGW("netdog", "cannot send with the link up (%d of %d)", fails, FAIL_LIMIT);
  return fails >= FAIL_LIMIT;
}

}  // namespace net_watchdog
