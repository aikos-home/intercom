// aikos Intercom Talk: walkie-talkie between the door and the room key that answered (aikos vertraege.md §4).
//
// Wire format: RTP L16 big-endian, PT 96, 16 kHz mono, 20 ms (320 samples), UDP 5004, unicast.
// - Door -> key: only while the visitor holds the talk button on the door screen, only during a call, only to the
//   key that answered. A copy goes to the transcriber (Mac Studio :5008) whenever the visitor holds.
// - Key -> door: played ONLY while the answering key reports its button held (talk_start .. talk_stop, forwarded by HA:
//   the owner's rule "speaking only while the RoomKey button is pressed"). Audio that arrived at most 0.3 s before
//   talk_start is played when it arrives, so the HA hop (~0.1 s) doesn't cut the first syllable; nothing older. Everything else from the key is dropped
//   unheard (counted). Never while the visitor holds (half-duplex).
// - Call start: one silent 20 ms frame to the key so it latches the door as its peer.
// - Release: flush the last samples, then one comfort-noise packet (PT 13, RFC 3389, 1 byte): end of speech.
#pragma once

#include <algorithm>
#include <atomic>
#include <cmath>
#include <cstdint>
#include <cstring>
#include <mutex>
#include <string>
#include <vector>
#include <lwip/sockets.h>
#include <esp_random.h>
#include "esphome/core/hal.h"
#include "esphome/core/log.h"
#include "esphome/components/microphone/microphone_source.h"
#include "esphome/components/speaker/speaker.h"

namespace door_talk {

static const char *const TAG = "talk";
static const int FRAME = 320;            // samples per packet: 20 ms at 16 kHz
static const uint16_t PORT = 5004;
static const uint8_t PT_L16 = 96, PT_CN = 13;
static const uint32_t CALL_IDLE_MS = 120000;  // no audio either way for this long: the conversation is over

inline int sock = -1;
inline std::atomic<bool> in_call{false}, talking{false};
inline std::atomic<uint32_t> peer_ip{0};      // network byte order
inline std::atomic<uint16_t> peer_port{0};    // network byte order
inline uint32_t copy_ip = 0;                  // transcriber, network byte order (0 = none)
inline uint16_t copy_port = 0;
inline uint16_t seq = 0;
inline uint32_t ts = 0, ssrc = 0;
inline bool spurt_start = true;
inline int16_t frame[FRAME];
inline int fill = 0;
inline std::atomic<int> gain{4};
inline std::atomic<uint32_t> tx_packets{0}, rx_packets{0};
inline std::atomic<uint32_t> last_audio_ms{0};
inline std::atomic<bool> peer_talking{false};  // the answering key's button is held
inline uint32_t peer_talk_ms = 0;
static const uint32_t PEER_TALK_MAX_MS = 90000;  // a lost talk_stop can't leave the door open
static const int PRE = 25;                       // room for 0.5 s; only the last PRE_MS of it is ever played
static const uint32_t PRE_MS = 300;
inline int16_t pre[PRE][FRAME];
inline int pre_len[PRE];
inline uint32_t pre_ms[PRE];
inline uint32_t pre_ip[PRE];
inline int pre_head = 0, pre_count = 0;
inline std::atomic<uint32_t> held_back{0};       // packets from the key that were not played
inline uint32_t call_ms = 0;
inline int latch_left = 0;  // the first packet to a new address is often lost while ARP resolves: repeat the silent frame
inline esphome::speaker::Speaker *spk = nullptr;
inline esphome::microphone::MicrophoneSource *mic = nullptr;
inline std::mutex tx_lock;  // the mic task and the main loop both send: one packet at a time, one frame buffer

inline void send_to(uint32_t ip, uint16_t port, const uint8_t *pkt, size_t len) {
  if (sock < 0 || ip == 0 || port == 0)
    return;
  sockaddr_in to{};
  to.sin_family = AF_INET;
  to.sin_addr.s_addr = ip;
  to.sin_port = port;
  sendto(sock, pkt, len, 0, (const sockaddr *) &to, sizeof to);
}

// one RTP packet to the peer (during a call) and the transcriber copy
inline void send_rtp(uint8_t pt, bool marker, const uint8_t *payload, size_t n, uint32_t samples, bool to_peer,
                     bool to_copy) {
  uint8_t pkt[12 + 2 * FRAME];
  if (n > sizeof pkt - 12)
    return;
  pkt[0] = 0x80;
  pkt[1] = (uint8_t) ((marker ? 0x80 : 0) | pt);
  pkt[2] = seq >> 8;
  pkt[3] = seq & 0xFF;
  pkt[4] = ts >> 24;
  pkt[5] = (ts >> 16) & 0xFF;
  pkt[6] = (ts >> 8) & 0xFF;
  pkt[7] = ts & 0xFF;
  pkt[8] = ssrc >> 24;
  pkt[9] = (ssrc >> 16) & 0xFF;
  pkt[10] = (ssrc >> 8) & 0xFF;
  pkt[11] = ssrc & 0xFF;
  memcpy(pkt + 12, payload, n);
  if (to_peer && in_call)
    send_to(peer_ip, peer_port, pkt, 12 + n);
  if (to_copy)
    send_to(copy_ip, copy_port, pkt, 12 + n);
  seq++;
  ts += samples;
  tx_packets++;
}

inline void send_frame(int samples) {
  uint8_t be[2 * FRAME];
  for (int i = 0; i < samples; i++) {
    be[2 * i] = (uint8_t) ((uint16_t) frame[i] >> 8);
    be[2 * i + 1] = (uint8_t) ((uint16_t) frame[i] & 0xFF);
  }
  send_rtp(PT_L16, spurt_start, be, 2 * samples, samples, true, true);
  spurt_start = false;
}

// microphone task: 16-bit little-endian mono samples
inline void on_mic(const std::vector<uint8_t> &data) {
  if (!talking)
    return;
  std::lock_guard<std::mutex> guard(tx_lock);
  const int g = gain;
  const size_t n = data.size() / 2;
  for (size_t i = 0; i < n; i++) {
    const int16_t s = (int16_t) (data[2 * i] | (data[2 * i + 1] << 8));
    // gain with a soft knee above ~73 % instead of hard clipping
    float y = (float) s * g;
    const float a = fabsf(y), knee = 24000.0f;
    if (a > knee)
      y = copysignf(std::min(32767.0f, knee + (a - knee) * 0.15f), y);
    frame[fill++] = (int16_t) y;
    if (fill == FRAME) {
      send_frame(FRAME);
      fill = 0;
    }
  }
  last_audio_ms = esphome::millis();
}

inline bool parse_host_port(const std::string &s, uint32_t &ip, uint16_t &port) {
  const size_t colon = s.find(':');
  const std::string host = s.substr(0, colon);
  if (host.empty())
    return false;
  in_addr a{};
  if (inet_aton(host.c_str(), &a) == 0)
    return false;
  ip = a.s_addr;
  port = htons(colon == std::string::npos ? PORT : (uint16_t) atoi(s.c_str() + colon + 1));
  return true;
}

inline void set_transcriber(const std::string &host_port) {
  uint32_t ip = 0;
  uint16_t port = 0;
  if (parse_host_port(host_port, ip, port)) {
    copy_ip = ip;
    copy_port = port;
    ESP_LOGI(TAG, "transcriber copy to %s", host_port.c_str());
  } else {
    copy_ip = 0;
    copy_port = 0;
    ESP_LOGI(TAG, "no transcriber copy");
  }
}

inline void setup(esphome::speaker::Speaker *speaker, esphome::microphone::Microphone *microphone) {
  spk = speaker;
  ssrc = esp_random();
  seq = (uint16_t) esp_random();
  ts = esp_random();
  mic = new esphome::microphone::MicrophoneSource(microphone, 16, 1, false);
  mic->add_channel(0);
  mic->add_data_callback([](const std::vector<uint8_t> &data) { on_mic(data); });
  sock = ::socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);  // ::, esphome has a socket namespace
  if (sock < 0) {
    ESP_LOGE(TAG, "no UDP socket");
    return;
  }
  sockaddr_in me{};
  me.sin_family = AF_INET;
  me.sin_addr.s_addr = htonl(INADDR_ANY);
  me.sin_port = htons(PORT);
  if (bind(sock, (const sockaddr *) &me, sizeof me) != 0)
    ESP_LOGE(TAG, "cannot bind UDP %u", PORT);
  fcntl(sock, F_SETFL, fcntl(sock, F_GETFL, 0) | O_NONBLOCK);
  ESP_LOGI(TAG, "RTP on UDP %u", PORT);
}

inline void talk_start() {
  if (talking)
    return;
  fill = 0;
  spurt_start = true;
  talking = true;
  if (mic != nullptr)
    mic->start();
  ESP_LOGI(TAG, "visitor talks%s", in_call ? "" : " (no call: transcriber copy only)");
}

inline void talk_stop() {
  if (!talking)
    return;
  std::lock_guard<std::mutex> guard(tx_lock);
  talking = false;
  if (fill > 0)
    send_frame(fill);  // the last few samples
  fill = 0;
  const uint8_t noise = 127;  // comfort noise = end of speech: the transcriber closes the utterance at once
  send_rtp(PT_CN, false, &noise, 1, 0, true, true);
  if (mic != nullptr)
    mic->stop();
  ESP_LOGI(TAG, "visitor released (%u packets sent so far)", (unsigned) tx_packets.load());
}

inline void call_start(const std::string &host, int port) {
  uint32_t ip = 0;
  uint16_t p = 0;
  if (!parse_host_port(host + ":" + std::to_string(port > 0 ? port : PORT), ip, p)) {
    ESP_LOGW(TAG, "call_start: bad peer '%s'", host.c_str());
    return;
  }
  peer_ip = ip;
  peer_port = p;
  in_call = true;
  last_audio_ms = esphome::millis();
  if (spk != nullptr)
    spk->start();
  uint8_t silence[2 * FRAME] = {0};  // lets the key latch the door as its peer
  {
    std::lock_guard<std::mutex> guard(tx_lock);
    send_rtp(PT_L16, true, silence, sizeof silence, FRAME, true, false);
  }
  call_ms = esphome::millis();
  latch_left = 2;  // again after 0.1 s and 0.4 s
  ESP_LOGI(TAG, "call with %s:%d", host.c_str(), port);
}

inline void play_frame(const int16_t *le, int n) {
  if (spk == nullptr)
    return;
  if (!spk->is_running())
    spk->start();
  spk->play((const uint8_t *) le, (size_t) n * 2, 0);
}

// HA forwards a key's talk_start / talk_stop with the key's address (the owner: hold = speak, no answer, no hang-up).
// The first talk_start makes that key the door's partner (visitor replies go to it); the conversation ends after
// CALL_IDLE_MS without audio.
inline void set_peer_talk(bool held, const std::string &host) {
  const uint32_t now = esphome::millis();
  if (held) {
    uint32_t ip = 0;
    uint16_t p = 0;
    if (!host.empty() && parse_host_port(host, ip, p) && (!in_call || ip != peer_ip))
      call_start(host, PORT);
    if (!in_call) {
      ESP_LOGW(TAG, "talk_start without a key address: ignored");
      return;
    }
    peer_talking = true;
    peer_talk_ms = now;
    last_audio_ms = now;
    // what this key sent just before its talk_start got through (the HA hop), nothing older, nothing from others
    int played = 0;
    for (int k = 0; k < pre_count; k++) {
      const int i = (pre_head - pre_count + k + PRE) % PRE;
      if (pre_ip[i] == peer_ip && now - pre_ms[i] <= PRE_MS) {
        play_frame(pre[i], pre_len[i]);
        played++;
      } else {
        held_back++;
      }
    }
    ESP_LOGI(TAG, "key talks (%d frames from just before talk_start played)", played);
  } else {
    if (peer_talking)
      ESP_LOGI(TAG, "key released");
    peer_talking = false;
    held_back += pre_count;
    last_audio_ms = now;
  }
  pre_count = 0;
}

inline void call_end() {
  if (!in_call)
    return;
  if (talking)
    talk_stop();
  in_call = false;
  peer_talking = false;
  held_back += pre_count;
  pre_count = 0;
  peer_ip = 0;
  peer_port = 0;
  if (spk != nullptr)
    spk->stop();
  ESP_LOGI(TAG, "call ended");
}

// main loop: play what the peer sends; end an idle call
inline void poll(uint32_t now) {
  if (sock < 0)
    return;
  uint8_t buf[1500];
  for (int k = 0; k < 16; k++) {
    sockaddr_in from{};
    socklen_t fl = sizeof from;
    const int len = recvfrom(sock, buf, sizeof buf, 0, (sockaddr *) &from, &fl);
    if (len <= 0)
      break;
    if (len <= 12 || (buf[1] & 0x7F) != PT_L16 || talking)
      continue;  // keepalive, comfort noise, or the visitor holds (half-duplex)
    const int n = (len - 12) / 2;
    const int m = std::min(n, FRAME);
    int16_t le[FRAME];
    for (int i = 0; i < m; i++)
      le[i] = (int16_t) ((buf[12 + 2 * i] << 8) | buf[13 + 2 * i]);
    if (in_call && peer_talking && from.sin_addr.s_addr == peer_ip) {
      play_frame(le, m);
      rx_packets++;
      last_audio_ms = now;
    } else {  // no button held for this sender: keep it briefly, unheard (played only if its talk_start follows)
      memcpy(pre[pre_head], le, (size_t) m * 2);
      pre_len[pre_head] = m;
      pre_ms[pre_head] = now;
      pre_ip[pre_head] = from.sin_addr.s_addr;
      pre_head = (pre_head + 1) % PRE;
      if (pre_count < PRE)
        pre_count++;
      else
        held_back++;  // the oldest frame falls out without ever being played
    }  // unheard packets don't keep the conversation alive
  }
  if (peer_talking && now - peer_talk_ms > PEER_TALK_MAX_MS) {
    ESP_LOGW(TAG, "no talk_stop after %u s: closing", (unsigned) (PEER_TALK_MAX_MS / 1000));
    set_peer_talk(false, "");
  }
  if (in_call && latch_left > 0 && now - call_ms >= (latch_left == 2 ? 100u : 400u)) {
    uint8_t silence[2 * FRAME] = {0};
    std::lock_guard<std::mutex> guard(tx_lock);
    send_rtp(PT_L16, false, silence, sizeof silence, FRAME, true, false);
    latch_left--;
  }
  if (in_call && !talking && now - last_audio_ms > CALL_IDLE_MS) {
    ESP_LOGI(TAG, "no audio for %u s", (unsigned) (CALL_IDLE_MS / 1000));
    call_end();
  }
}

}  // namespace door_talk
