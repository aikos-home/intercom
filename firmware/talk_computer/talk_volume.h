// Speaker level of the talk computer (owner 2026-10-04: full level only for the gong, never for speech).
// ESPHome's software volume v in [0, 1] is a reduction of 49 dB x (1 - v). "Speaker volume" 0-100 % is speech only and
// tops out at -6 dB (a quarter of the amp's full power); the chime script sets 1.0 for the gong and restores this after.
#pragma once
#include <algorithm>

static constexpr float SPEECH_VOLUME_MAX = 0.878f;  // 49 dB x (1 - 0.878) = 6 dB below full level

inline float speech_volume(float percent) { return std::clamp(percent, 0.0f, 100.0f) / 100.0f * SPEECH_VOLUME_MAX; }
