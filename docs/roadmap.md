# Roadmap

State: 2026-10-20. Generated from `explorer/skeleton.json` and `explorer/texts.json`;
the interactive version is the roadmap section of the [explorer](../explorer/).

`[x]` done · `[~]` under way · `[ ]` to do · `◆` a decision that must be locked in

## Must-lock-ins

- ◆ Lock in: which extra audio features (voice messages, push-to-talk into the house) (M3)

## M0 · Concept and architecture

**Done** · 4 of 4 tasks done

Decide what the device is before buying and printing: the front design, the parts and how they connect.

- [x] Front design v5: one bent brass sheet, 100 × 260 mm, light band under the roof
- [x] Architecture: one PoE cable, three computers (doorbell, talk, screen)
- [x] Parts chosen and drawn with their dimensions
- [x] This map and the public repository

*Done when:* Every part, wire and open decision is on the map.

## M1 · All hardware on the table

**Now** · 3 of 4 tasks done

Nothing can be measured, fitted or programmed for real until every part of the final build is here.

Needs: M0 Concept and architecture

- [x] Power path: the doorbell computer's PoE module feeds the box (heater load test passed, 9.37 W)
- [x] In hand: all three computers, microphone, amplifier, speaker, both climate sensors, radar, heater pad, thermal fuses, level shifter
- [x] Bench checks on arrival: touch chip GT911, real BME280, heater on PoE
- [ ] Still to buy: a logic-level MOSFET, the COB LED strip, the outdoor cable

*Done when:* Every part of the final build is here and identified.

## M2 · Measure and alpha print

**Done** · 5 of 5 tasks done

Find out whether everything fits before designing the real box: first the parts alone, then with every cable.

Needs: M1 All hardware on the table

- [x] Measure what makers don't publish: display, doorbell computer, talk computer, microphone, amplifier, SHT31, radar
- [x] Count the cables entering the box: one network cable; service USB through the bottom
- [x] Alpha print v2: all parts in place, surface-mounted on the door frame (12–13 Oct)
- [x] Box v3 (v3.0–v3.7): every part and every cable fits, with reserve
- [x] Box size locked: 92 × 252 × 60 mm, on the wall (the door frame)

*Done when:* Every part and every cable fits in a printed box, and the number of cables entering it is final.

## M3 · Bench build and software

**Now** · 5 of 9 tasks done

Wire everything together and build the software until the experience at the door and in the house is release quality.

Needs: M1 All hardware on the table

- [x] Doorbell: all three line states; storm ringing 20 of 20 at the bell, in Home Assistant and on the screen
- [x] Screen pages change on a ring; Wi-Fi in the box (−29 dBm from the doorbell computer's own access point)
- [x] Talk between the door and a room key, with transcripts on the screen
- [x] Duplex settled: the door arbitrates, its microphone is muted toward the keys while its speaker plays
- [x] One cable and the power rail: 4.82 W in the box, 9.37 W with the heater on the bench
- [~] Climate sensors in the firmware (written), the heater control and its switch
- [ ] Radar in the screen firmware; light under the roof
- [ ] ◆ Lock in: which extra audio features (voice messages, push-to-talk into the house)
- [~] UX until release quality: screen pages, light, sounds

*Done when:* The device does everything at release quality, and the measured power stays within 802.3af.

## M4 · Watertightness proof of concept

**Now** · 3 of 5 tasks done

Prove that the printed box, the steel sheet and the brass can be sealed. Runs alongside everything else.

Needs: M0 Concept and architecture

- [x] Mounting locked: surface-mounted on the solid wooden door frame
- [x] Box material locked: PETG (prints well on an open printer)
- [x] The steel sheet as the water plane, the brass on top; printed stand-ins in v3
- [~] Seals: silicone bead, O-ring at every screw, button O-ring, mic membrane, split cable gland
- [ ] Water test of the sealed box: hose or shower, dry inside afterwards

*Done when:* The box stays dry inside in a repeatable water test, and the sealing recipe is written down.

## M5 · Beta box on the desk

**Now** · 2 of 4 tasks done

The complete device in its real box, running on the desk over the one cable. Not watertight yet.

Needs: M2 Measure and alpha print, M3 Bench build and software, M4 Watertightness proof of concept (bracket and dummy plate)

- [x] Print the box from what the alpha prints showed (v3.7)
- [x] All inside wiring soldered, with reserve; first power-on in the box (20 Oct)
- [ ] Fit the steel and brass stand-ins with everything running
- [ ] Two weeks on the desk: scripted rings and calls, 20 PoE power cycles, no unexpected reboot

*Done when:* The whole device runs in its box for two weeks without a surprise.

## M6 · Pre-release box

**Later** · 0 of 5 tasks done

Bring the lessons of v3 and the water test into the final box and order the real metal front.

Needs: M5 Beta box on the desk, M4 Watertightness proof of concept

- [ ] Apply the findings of v3 and the water test: the v4 box, without glued parts
- [ ] Order the steel and brass front from a metal shop (cut, bent, engraved)
- [ ] Final print
- [ ] Water test of the complete device
- [ ] Freezer cold start: heater, screen and PoE module come up in frost

*Done when:* The finished device passes the water test and the cold start.

## M7 · At the door

**Later** · 0 of 4 tasks done

Install the finished device at the front door and switch it on for good.

Needs: M6 Pre-release box

- [ ] Electrician: earth the surge protector, remove the old bell transformer
- [ ] Cable route through the wall
- [ ] Mount the box and seal the joint to the facade
- [ ] Go live with the watchdogs on (stuck button, cut wire, offline)

*Done when:* A ring at the real door reaches the phone.
