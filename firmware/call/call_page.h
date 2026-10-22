// aikos Intercom Screen: the call as the door screen shows it (voice v2, R17; aikos features/sprechen.md §4b).
//
// Sources (all through Home Assistant except the visitor's "Sprechen", which goes straight to the talk computer):
//   sensor.aikos_call_log        attribute messages_json: the chat of the running call, the one source (no merging here)
//   sensor.aikos_people          attribute keys_json: node -> {name, room, host}; the screen maps a key's last octet
//   talk computer                floor_key (who speaks, last octet), "Call member keys" ("144,110"), answered
// the owner's decisions (2026-10-01): "Sprechen" right after the ring; the visitor's own words under the role aikos
// recognised ("Paketdienst · DHL"); "Max und Erika hören zu"; "Nachricht hinterlassen" only until someone answers.
// Placeholder copy: the owner writes the wording.
#pragma once

#include <cstdint>
#include <cstdlib>
#include <cstring>
#include <map>
#include <string>

namespace aikos_call {

struct Msg {
  std::string id, side, who, text;  // side "door" = the visitor, "room" = someone inside
  bool operator==(const Msg &o) const { return id == o.id && side == o.side && who == o.who && text == o.text; }
};
// R27 (the owner, 2026-10-02): a device keeps only the newest messages, for a while; the full log lives on the server.
// The call log sends the newest 10 (aikos PR #27).
static const int MAX_MSGS = 10;

inline Msg msgs[MAX_MSGS];
inline int n_msgs = 0;
inline uint32_t chat_version = 0;  // +1 on every change of the chat
inline bool appended = true;       // the last change only added messages at the end (ink only on the screen)
inline int dropped = 0;            // with appended: how many of the oldest fell out of the window (R27)
inline uint32_t status_version = 0;  // +1 when who speaks / who listens changes
inline bool answered = false;
inline int floor_octet = 0;
inline std::string member_octets;
inline std::map<int, std::string> names;  // last octet -> name ("Max", or the room for shared rooms)

// the list the screen shows (oldest first); the screen decides how to draw the difference
inline void show_list(const Msg *list, int n) {
  if (n > MAX_MSGS) {  // the newest
    list += n - MAX_MSGS;
    n = MAX_MSGS;
  }
  if (n == n_msgs) {
    bool same = true;
    for (int i = 0; i < n && same; i++)
      same = msgs[i] == list[i];
    if (same)
      return;
  }
  // appended: the old list, minus some of its oldest (the window of R27), is the start of the new one, and more follows
  int shift = -1;
  for (int d = 0; d <= n_msgs && shift < 0; d++) {
    const int keep = n_msgs - d;
    if (n <= keep)
      continue;
    bool same = true;
    for (int i = 0; i < keep && same; i++)
      same = msgs[d + i] == list[i];
    if (same)
      shift = d;
  }
  if (n_msgs > 0 && shift == n_msgs)
    shift = -1;  // nothing of the old list is left: a new chat, not an addition
  for (int i = 0; i < n; i++)
    msgs[i] = list[i];
  n_msgs = n;
  appended = shift >= 0;
  dropped = shift > 0 ? shift : 0;
  chat_version++;
}

// R22 (the owner, 2026-10-01): the last call's chat never shows at the next call, not even briefly. Two guards:
// 1. the log's messages are shown only while the log says its call is on (`active`). The list is kept while it isn't,
//    because HA may deliver messages_json before active.
// 2. the moment the talk computer announces another call id (a new call, or 0 = the end; its broadcast is faster than
//    HA), the chat is forgotten. HA sends the whole list again with the next message.
inline Msg log_msgs[MAX_MSGS];
inline int log_n = 0;
inline bool log_active = false;
inline uint32_t door_call_id = 0;
inline bool door_call_known = false;

inline void show_log() {
  if (log_active)
    show_list(log_msgs, log_n);
  else
    show_list(nullptr, 0);
}
// the whole list from the call log (oldest first)
inline void set_messages(const Msg *list, int n) {
  if (n > MAX_MSGS) {  // the newest
    list += n - MAX_MSGS;
    n = MAX_MSGS;
  }
  for (int i = 0; i < n; i++)
    log_msgs[i] = list[i];
  log_n = n;
  show_log();
}
inline void set_log_active(bool on) {
  log_active = on;
  show_log();
}
inline void forget_chat() {
  log_n = 0;
  show_log();
}
// the call id from the talk computer's broadcast (every second; 0 = no call)
inline void set_door_call(uint32_t id) {
  if (!door_call_known) {  // the first one after boot: nothing of an earlier call is on this screen yet
    door_call_known = true;
    door_call_id = id;
    return;
  }
  if (id != door_call_id) {
    door_call_id = id;
    forget_chat();
  }
}

inline void clear_people() { names.clear(); }
inline void add_person(const char *host, const char *name) {
  const char *dot = strrchr(host, '.');
  if (dot != nullptr && name != nullptr && name[0] != '\0')
    names[atoi(dot + 1)] = name;
}
inline std::string name_of(int octet) {
  auto it = names.find(octet);
  return it != names.end() ? it->second : std::string("Jemand");
}

inline void set_floor(int octet) {
  if (octet != floor_octet) {
    floor_octet = octet;
    status_version++;
  }
}
inline void set_members(const std::string &octets) {
  if (octets != member_octets) {
    member_octets = octets;
    status_version++;
  }
}
inline void set_answered(bool on) {
  if (on != answered) {
    answered = on;
    status_version++;
  }
}

// "Max spricht gerade", or empty when nobody inside holds
inline std::string speaking() { return floor_octet > 0 ? name_of(floor_octet) + " spricht gerade" : std::string(); }

// "Max hört zu" / "Max und Erika hören zu" / "Max, Erika und Anna hören zu", or empty
inline std::string listeners() {
  std::string list[8];
  int n = 0;
  size_t pos = 0;
  while (pos < member_octets.size() && n < 8) {
    size_t comma = member_octets.find(',', pos);
    if (comma == std::string::npos)
      comma = member_octets.size();
    const int octet = atoi(member_octets.substr(pos, comma - pos).c_str());
    if (octet > 0) {
      const std::string name = name_of(octet);
      bool dup = false;
      for (int i = 0; i < n; i++)
        dup |= list[i] == name;
      if (!dup)
        list[n++] = name;
    }
    pos = comma + 1;
  }
  if (n == 0)
    return std::string();
  std::string out = list[0];
  for (int i = 1; i < n; i++)
    out += (i == n - 1 ? " und " : ", ") + list[i];
  return out + (n == 1 ? " hört zu" : " hören zu");
}

// the label above a message: the room's speaker, or the visitor as aikos recognised them
inline std::string label(const Msg &m) {
  if (!m.who.empty())
    return m.who;
  return m.side == "door" ? std::string("Besucher") : std::string("Drinnen");
}

}  // namespace aikos_call
