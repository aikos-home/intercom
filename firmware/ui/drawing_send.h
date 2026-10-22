// The visitor's drawing for the residents (screen 0.7.15): "Malen -> Senden" used to only clear the canvas.
// The canvas rows [y0, y1) go to Home Assistant as one event (esphome.aikos_door_drawing): per row the run lengths
// white, ink, white, ... (each an unsigned LEB128 varint, a row's runs add up to the width, a row starting with ink
// begins with a white run of 0), base64. Chalk lines on white compress to a few kB. A very full drawing is halved in
// both directions (a 2 x 2 block is ink if any pixel is) so the event stays well below the API's frame size.
// Decoder: ha-dev/save_drawing.py (Klingelbox repo).
#pragma once
#include <cstdint>
#include <string>
#include "esphome/core/helpers.h"
#if __has_include("esphome/core/alloc_helpers.h")
#include "esphome/core/alloc_helpers.h"  // base64_encode lives here since ESPHome 2026.x
#endif

namespace aikos_drawing {

static const size_t MAX_RAW = 30000;  // bytes before base64: ~40 kB in the event

inline bool ink_at(const uint8_t *canvas, int stride, int x, int y) { return canvas[y * stride + (x >> 3)] & (1 << (x & 7)); }

// scale 1: every pixel; scale 2: 2 x 2 blocks. Returns false when the result would be too big.
inline bool encode_raw(const uint8_t *canvas, int stride, int width, int y0, int y1, int scale, std::string &raw) {
  raw.clear();
  auto put = [&](uint32_t v) {
    do {
      uint8_t b = v & 0x7F;
      v >>= 7;
      if (v)
        b |= 0x80;
      raw.push_back((char) b);
    } while (v);
  };
  const int w = width / scale;
  for (int y = y0; y + scale <= y1; y += scale) {
    bool ink = false;
    uint32_t run = 0;
    for (int x = 0; x < w; x++) {
      bool b = false;
      for (int dy = 0; dy < scale && !b; dy++)
        for (int dx = 0; dx < scale && !b; dx++)
          b = ink_at(canvas, stride, x * scale + dx, y + dy);
      if (b != ink) {
        put(run);
        run = 0;
        ink = b;
      }
      run++;
    }
    put(run);
    if (raw.size() > MAX_RAW)
      return false;
  }
  return true;
}

// The event's fields; empty rle = nothing to send (an empty canvas or far too much ink).
struct Drawing {
  int width = 0, height = 0, scale = 1;
  std::string rle;
};

inline Drawing encode(const uint8_t *canvas, int stride, int width, int y0, int y1) {
  Drawing d;
  if (canvas == nullptr)
    return d;
  bool any = false;
  for (int y = y0; y < y1 && !any; y++)
    for (int i = 0; i < (width + 7) / 8 && !any; i++)
      any = canvas[y * stride + i] != 0;
  if (!any)
    return d;
  std::string raw;
  for (int scale = 1; scale <= 2; scale++) {
    if (encode_raw(canvas, stride, width, y0, y1, scale, raw)) {
      d.width = width / scale;
      d.height = (y1 - y0) / scale;
      d.scale = scale;
      d.rle = esphome::base64_encode(reinterpret_cast<const uint8_t *>(raw.data()), raw.size());
      return d;
    }
  }
  return d;
}

}  // namespace aikos_drawing
