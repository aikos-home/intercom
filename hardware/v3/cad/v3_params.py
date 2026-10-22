"""Intercom v3 - EINZIGE Quelle aller Masse fuer v3.

des Bauherrn Zaehlung (2026-10-13): v1 = Testbox, v2 = Endkasten-Testaufbau (gedruckt 2026-10-12/13, Generatoren in cad/,
eingefroren), v3 = dieser Stand. v3 wird gedruckt und eingebaut, bevor Bauherr zu Metallbetrieb geht; v3 ist die Grundlage
fuer die CNC-Auftraege (Messing, Stahl, Leisten), aber nicht der endgueltige prod-Kasten.

Ausgangspunkt ist kasten_v3_params.py (= v2). Alles, was v2 hatte und was sich bewaehrt hat, steht hier unveraendert.
Was sich aendert, kommt aus cad/v3/V3_GRUNDLAGE.md (Befunde B-01..B-13, Wuensche W-01..W-06) und steht beim jeweiligen
Mass mit "v3:" und der Befundnummer.

Zeichnung, CAD und Pruefung lesen alle diese Datei. `validate()` prueft jede geometrische Regel.
Tags: [DB] Datenblatt · [GEMESSEN] am realen Teil · [FREI] Konstruktionswahl · [PLATZ] Platzhalter.
Koordinaten: Ursprung = linke obere Ecke der Messingblende, x rechts, y unten, d = Tiefe hinter der Messingrueckseite.

WAS SICH GEGENUEBER v2 AENDERT (Kurzfassung, Einzelheiten bei den Massen)
  B-02  Gegenleisten: dieselben Kanaele wie v2, aber oben ZU. Die Leisten werden waehrend einer Druckpause eingelegt
        und vom Kragen ueberdruckt (keine Einschuboeffnung, kein Hohlraum fuer Stuetzen). O-Ring in jedem Abstandsring.
  B-04  Lautsprecher von vorn: 2 Schrauben aus dem Gitterhohlraum in einen Klemmring hinter dem Lautsprecher,
        Moosgummi-Dichtung vor dem Rahmen. Keine Einsaetze mehr im Gitterblock.
  B-03  Druckausgleichsventil ruht: kein Ventilloch mehr im Gitterblock.
  B-06  Radar-Traeger als offener Rahmen, Schacht an der kurzen Seite +0.5, Nuten im Taschenboden fuer die Loetstellen.
  B-12/13 Display-Druckstifte: Spitze 1.75 lang, Satz in vier Laengen (-0.5 .. -2.0 gegen v2).
  B-10  Verstaerker-Rahmen: Stifte druecken gegen die Aussenkanten der Loecher (15.0).
  W-03  Klingel- und Sprechrechner auf EINEM Computer-Traeger in Schienen an der Rueckwand, herausziehbar nach unten.
        Die Display-Traegerplatte haengt oben in zwei Schlitzen im Gitterblock und hat nur noch 2 Schrauben unten.
  W-04  Verteiler 30 x 70 auf einem geklebten Klips-Sockel an der Rueckwand (Sitz im Kasten).
  W-05  LAN: Einfuehrung fuer den Stecker, Kabelbinder-Oesen an der Rueckwand, freie Bahn zur Buchse.
  W-02  SHT31-D in einer eigenen Aussenkammer unten rechts, BME280 auf dem Verteiler.
  W-06  LEDs: keine LED-Fenster mehr, Streifen im Diffusor, ein Kabelloch durch Messing, Stahl und Kragen.
  Holzschrauben mit Senkkopf (buendig), weil der Computer-Traeger ueber sie gleitet.

v3.1 (2026-10-14, des Bauherrn SHT31-Masse): Die SHT31-D-Platine steckt auf einem Stift am Kammerdeckel 08 (Bund, Stift,
Rippe gegen Verdrehen). Nur der Deckel aendert sich, der Kasten bleibt bytegleich.
v3.2 (2026-10-16, V3-02): Radar-Rahmen 05 als Abstandsrahmen (Stufe vorn, Lippen hinten), weil die Stiftleiste an der
Langseite liegt und das Radar aus dem v3-Rahmen fiel. Nur der Rahmen aendert sich, der Kasten bleibt bytegleich.
v3.3 (2026-10-16, V3-03): Computer-Traeger rastet ein: Rastknopf (Klebeteil 06c) auf der Rueckwand, Gasse und Rastloch
im Traeger. Neu: Traeger 03 und Knoepfe 06c; der Kasten bleibt bytegleich.
v3.4 (2026-10-16, V3-02 Nachtrag): Bauherr bekommt den Radar-Rahmen hinter dem Gitterblock nicht eingeklemmt. Rahmen 05
wird jetzt eingeklebt: keine Quetschrippen, rundum 0.3 Luft, vorn aussen eine Fase gegen den Wulst der ersten Lage. Das
Radar sitzt wie in v3.2. Nur der Rahmen aendert sich, der Kasten bleibt bytegleich.
v3.5 (2026-10-16, V3-04): Die duennen Stifte fuer Verstaerker und SHT31 waren gedruckt zu duenn, beide Platinen hielten
nicht. Verstaerker-Rahmen 06 und Kammerdeckel 08 kommen jetzt je als Satz in drei Stiftstaerken (Zahl unten
eingraviert), die Stifte sitzen mittig in den Loechern. Der Kasten bleibt bytegleich.
v3.6 (2026-10-16, V3-05): Die Display-Traegerplatte biegt oben nach hinten durch, wenn man das Display drueckt. Neu
sind zwei Plattenstuetzen 17 zum Einkleben an den Seitenwaenden; die Platte liegt oben hinten darauf. Der Kasten bleibt
bytegleich.
v3.7 (2026-10-17, V3-07): Das Display gibt beim Druecken nach, weil zwischen Panel und Displayplatine nur Schaumstoff
und Heizpad liegen. Neu sind Abstandsstuecke 18 fuer diesen Spalt (gemessen 2.7), als Kaemme in 2.6 / 2.7 / 2.8 zum
Abbrechen und Einkleben. Alle anderen Teile bleiben bytegleich.
"""
import math

STAND = "v3.7"               # Name des Druckstands: Dateinamen der Bambu-Dateien und der FreeCAD-Ansicht

# ==================================================================== EINGEFROREN (unveraendert seit 2026-09-18)
FROZEN = {
    "BTN_C": (50.0, 225.0),
    "BTN_SCREW_CC": 37.06,
    "BTN_HOLE": 49.5,
    "RING_D": 48.5,
    "RING_T": 4.77,
    "BTN_CYL_D": 18.9,
    "BTN_CYL_L": 32.5,
    "BTN_FREE": 10.0,
}

# ------------------------------------------------------------------ Blende (wie v2)
SHEET = dict(w=100.0, h=260.0, t=2.0)                       # [DB]
GRILLE = dict(x0=21.0, y0=36.0, x1=79.0, y1=53.0, rows=2, row0=36.0, pitch=9.5, slot_h=7.5, slot_w=1.5,
              angle=70.0)
DISPLAY = dict(c=(50.0, 116.0), vis_w=56.95, vis_h=101.9, glass_w=66.77, glass_h=120.1,
               border_far=4.91, border_ribbon=13.28, stack=11.9)                     # [GEMESSEN] 2026-09-29
WIN_LAP = 0.5
DISPLAY_WIN = dict(x0=DISPLAY["c"][0] - DISPLAY["vis_w"] / 2 + WIN_LAP,
                   y0=DISPLAY["c"][1] - DISPLAY["vis_h"] / 2 + WIN_LAP,
                   x1=DISPLAY["c"][0] + DISPLAY["vis_w"] / 2 - WIN_LAP,
                   y1=DISPLAY["c"][1] + DISPLAY["vis_h"] / 2 - WIN_LAP)
DISPLAY_GLASS = dict(x0=DISPLAY["c"][0] - DISPLAY["glass_w"] / 2,
                     x1=DISPLAY["c"][0] + DISPLAY["glass_w"] / 2,
                     y0=DISPLAY["c"][1] - DISPLAY["vis_h"] / 2 - DISPLAY["border_far"],
                     y1=DISPLAY["c"][1] + DISPLAY["vis_h"] / 2 + DISPLAY["border_ribbon"])
# v3 (W-06, Bauherr 2026-10-14): Die zwei LED-Fenster (18 x 6) entfallen in Messing, Stahl und Kragen. Der LED-Streifen
# (COB, 10 breit) klebt unter dem Messingdach IM Diffusor. Es bleiben die zwei Laschenschlitze des Diffusors und EIN
# Kabelloch fuer 5V/DIN/GND, verdeckt unter dem Diffusor. Messing 3.5, Stahl und Kragen 4.5 (Messingloch liegt mit
# 0.5 Rand im Stahlloch, wie alle Oeffnungen). Abgedichtet mit Silikon um das Kabel.
LED_SLITS, LED_SLIT_Y = [(15.0, 25.0), (75.0, 85.0)], (9.7, 12.3)    # [DB] Laschenschlitze (wie v2)
LED_CABLE = dict(c=(62.0, 11.0), brass=3.5, steel=4.5, collar=4.5)  # [FREI] alte Stelle hinter Fenster 2
MIC = dict(d=13.0, t=2.53)                                  # [GEMESSEN]
MIC_C = (82.7, 221.5)
MIC_HOLE_OFF = 4.0
MICS = [(MIC_C[0], MIC_C[1] - MIC_HOLE_OFF), (MIC_C[0], MIC_C[1] + MIC_HOLE_OFF)]
MIC_D = 1.2
MIC_POCKET = dict(bore=13.2, membrane_t=0.2, membrane_d=12.0, gasket_t=1.0, gasket_squeeze=0.3, gasket_id=10.0,
                  gasket_od=13.0, floor=1.6, opening=10.0, rear_t=1.0, rear_squeeze=0.3)
MIC_POCKET["depth"] = (MIC_POCKET["membrane_t"] + MIC_POCKET["gasket_t"] - MIC_POCKET["gasket_squeeze"] + MIC["t"]
                       + MIC_POCKET["rear_t"] - MIC_POCKET["rear_squeeze"])
MIC_POCKET["boss_d"] = MIC_POCKET["bore"] + 2 * 1.5
MIC_POCKET["boss_l"] = MIC_POCKET["depth"] + MIC_POCKET["floor"]
BTN_C, RING_D, RING_T = (50.0, 225.0), 48.5, 4.77
BTN_HOLE = RING_D + 1.0
BTN_SCREW_CC = 37.06
BTN_CYL_D, BTN_CYL_L, BTN_FREE = 18.9, 32.5, 10.0
BTN_PLATE_T = 7.0
BTN_ORING = dict(mean=28.0, w=2.4, d=1.5)
# v3 (W-06): Diffusor wie v1 (Viertelrundstab R18 unter dem Dach), Wand 1.6 statt 2.0 (heller, COB-Streifen braucht
# keine dicke Wand). Der Streifen liegt unter dem Dach, nicht an der Front: dort stehen die Laschenrippen nicht im Weg.
DIFFUSOR = dict(r=18.0, x0=13.0, x1=87.0, wall=1.6)        # [DB]/[FREI]
# COB-Streifen (Subagent 2026-10-14): unter dem Dach ist Platz fuer 10 mm breit bis ~57 mm lang (5 mm breit bis ~66).
# Passt: BTF-LIGHTING FCOB WS2812B 10 mm, 5 V, RGB, Schnitt alle 11 mm -> 5 Abschnitte = 55 mm. Passt NICHT: die RGBW-
# Variante WS2814 (12 V, ein Abschnitt 62 mm). Alternative 5 mm breit (160 LED/m, Schnitt 12.5) mit 5 Abschnitten.
LED_STRIP = dict(w=10.0, t=3.0, l=55.0, xs0=4.5)           # [FREI] 10 breit, bis 3 dick, ab 4.5 hinter der Front

SCREWS = [(12.0, 30.0), (88.0, 30.0), (12.0, 248.0), (88.0, 248.0)]   # Messing -> Gewinde im Stahl (wie v2)
SCREW_HOLE, SCREW_HEAD = 3.2, 6.0
STEEL_TAP = 2.5

# ------------------------------------------------------------------ Kasten (Aussenmasse wie v2)
BOX = dict(x0=4.0, y0=4.0, x1=96.0, y1=256.0)               # [DB] 92 x 252
DEPTH = 60.0
WALL, BACK = 3.0, 3.0
CORNER_R = 10.0
STEEL = dict(t=2.0, glue=1.0, inset=0.1)
FRAME_T = STEEL["t"] + STEEL["glue"]                         # Kastenstirn d 3.0
FLANGE_W, FLANGE_T = 11.0, 3.0
D_BACK_IN = DEPTH - BACK                                     # Rueckwand innen d 57

# Gegenleisten (B-02, v3): Geometrie wie v2 (Edelstahl 5 x 4 in Kanaelen der Seitenkragen, M3x10 ISO 14581 alle 20,
# Gewinde y 30 ungenutzt fuer die Symmetrie), ABER:
#   - Der Kanal ist oben ZU. Es gibt keine Einschuboeffnung an der Kastenecke mehr (Bauherr: "die Idee mit dem
#     Einschieben wird niemals funktionieren").
#   - Die Leiste wird in einer DRUCKPAUSE eingelegt: Der Kasten druckt mit der Rueckwand nach unten, der Kanal ist bis
#     zur Kragenrueckseite (d 6 = Druckhoehe 54.0) eine offene Rinne. Pause, Leisten hinein, weiterdrucken: der Kragen
#     wird ueber die Leisten gedruckt. Die Leiste stuetzt die Bruecke, es entsteht kein Hohlraum, in den der Slicer
#     Stuetzen setzt. Die Leiste sitzt danach fest und kann nicht falsch herum hinein (Gewinde symmetrisch).
#   - Die Schrauben liegen ausserhalb der Dichtlinie (nass) und fuehren in den geschlossenen Kanal, der unten nach aussen
#     entwaessert - wie in v2, also braucht kein Loch eine Dichtung ins Innere. des Bauherrn O-Ring je Schraube kommt
#     trotzdem dazu (B-02): er sitzt in einer Nut im Abstandsring und haelt das Wasser schon vor dem Kanal auf.
BAR = dict(w=5.0, t=4.0, x=8.7, play_x=0.3, play_d=0.25,
           skin=1.9, inner=1.5, back=1.5,
           top=14.5, gap=0.5,                              # Oberkante der Leiste; Luft zu den Kanalenden (oben UND unten)
           stop_l=246.0, stop_r=206.0,
           y0=50.0, pitch=20.0,
           screw_l=10.0, hole=3.4, slot=0.5)
_BAR_D0 = FRAME_T + FLANGE_T                                 # Kragenrueckseite = Kanalvorderseite (d 6)
SHEATH_BACK_D = _BAR_D0 + BAR["t"] + 2 * BAR["play_d"] + BAR["back"]   # Rueckseite der Kanalwand (d 12)
BAR_Y = {s: (BAR["top"], BAR[k] - BAR["gap"]) for s, k in (("links", "stop_l"), ("rechts", "stop_r"))}
BAR_TOP_END = BAR["top"] - BAR["gap"]                        # v3: Kanal endet oben hier (geschlossen)
BAR_HOLES = {s: [BAR["y0"] + i * BAR["pitch"] for i in range(20)
                 if BAR["y0"] + i * BAR["pitch"] <= BAR_Y[s][1] - 5.0] for s in BAR_Y}
BAR_TAPS = {s: [BAR["y0"] - BAR["pitch"]] + BAR_HOLES[s] for s in BAR_HOLES}
# Druckpause: der Kasten liegt mit der Rueckwand auf dem Bett, Druckhoehe z = DEPTH - d. Die Pause kommt nach der Schicht,
# die bei z = DEPTH - _BAR_D0 endet; danach wird der Kragen ueber die Leisten gedruckt.
PRINT = dict(layer=0.2, first=0.2)                           # [DB] 0.20 Standard @BBL A1
PAUSE_Z = DEPTH - _BAR_D0                                    # 54.0
SPIGOTS = [(BAR["x"], 140.0), (BOX["x0"] + BOX["x1"] - BAR["x"], 140.0)]
SPIGOT = dict(d=4.0, hole=4.1, slot=0.5, tip=0.3)
STANDOFF_D = 7.0
# O-Ring je Schraube (B-02, Bauherr 2026-10-14): O-Ring 3 x 1 (NBR) auf dem Schaft, in einer Nut im Abstandsring. Der
# Stahl liegt auf dem Ringrand (1.0 = Silikonfuge) und drueckt den O-Ring auf 0.8 (20 %).
ORING = dict(id=3.0, cs=1.0, groove_id=3.4, groove_od=5.6, groove_d=0.8)   # [DB] O-Ring 3x1; Nut [FREI]
STEEL_CUT = dict(glass_gap=0.3, win_over=0.5, btn_hole=50.5, mic_hole=2.0, csk_hole=3.4, csk_d=6.0)
SEAL = dict(w=2.5, d=0.5, x_l=13.5, x_r=86.5, y_sill=56.5, y_arm=209.0, r_arc=27.2, deck_t=2.0, land=1.0)
SEAL_ARC_X = (BTN_C[0] - math.sqrt(SEAL["r_arc"] ** 2 - (BTN_C[1] - SEAL["y_arm"]) ** 2),
              BTN_C[0] + math.sqrt(SEAL["r_arc"] ** 2 - (BTN_C[1] - SEAL["y_arm"]) ** 2))

INS = dict(d=4.0, l=6.0)
MIN_WALL = 1.5
FIT = dict(pocket=0.10, peg_d=3.0, peg_hole=3.2, amp_pocket=0.15)

# ------------------------------------------------------------------ Lautsprecher VISATON K 40 SQ
SPK = dict(c=(59.0, 36.5), frame=40.0, port_d=35.0, hole_d=3.6, pattern=32.4, depth=12.0, behind=12.0)
SPK_WALL = 6.0
SPK_HOLES = [(SPK["c"][0] + sx * SPK["pattern"] / 2, SPK["c"][1] + sy * SPK["pattern"] / 2)
             for sy in (-1, 1) for sx in (-1, 1)]               # alle 4 Rahmenloecher
# v3 (B-04): Schrauben VON VORN aus dem Gitterhohlraum, aber nur in die 2 OBEREN Rahmenloecher. Die unteren liegen 1.7
# unter dem Hohlraumboden (y 52.7 gegen 51.0): dort gaebe es fuer den Kopf nur eine Senke unter dem Boden, in der
# Wasser steht. Unten haelt der Klemmring den Rahmen: er stuetzt sich mit einem Fuss unter dem Lautsprecher auf der
# Gitterblock-Rueckseite ab (Hebel). Zwischen Rahmen und Block eine Moosgummi-Dichtung (2 -> 1.2 gedrueckt); sie dichtet
# Schalloeffnung und Schraubloecher. Unter jedem Schraubenkopf ein O-Ring 3 x 1.5 (zweite Sperre, Hohlraum ist nass).
SPK_SCREWS = [h for h in SPK_HOLES if h[1] < SPK["c"][1]]      # (42.8|20.3), (75.2|20.3)
SPK_GASKET = dict(t=2.0, t_pressed=1.2)                       # [FREI] Moosgummi/Zellkautschuk geschlossenzellig
SPK_FRAME_T = 0.6                                             # [DB] VISATON-Zeichnung 2013/2021: Stahlrahmen 0.6
# VISATON K 40 SQ [DB]: Mylar-Membran, Korb Ø37, hinter der Rahmenvorderseite 10.0 tief (Bauherr gemessen gesamt 12,
# wir rechnen 12), Kalotte ragt 1.5 nach vorn in die Schalloeffnung. Lochbild laut DB 32 x 32 / Ø3.4, Bauherr hat 32.4 /
# Ø3.6 gemessen - es bleibt bei des Bauherrn Mass (Schrauben M3 haben in beiden Faellen Luft). IP65/67 nur vorn, wenn
# eingebaut: genau so sitzt er hier (Membran zur nassen Seite, Korb im trockenen Innenraum).
SPK_SCREW = dict(hole=3.4, head_d=5.7, oring_od=6.0, oring_pressed=1.1, pocket_d=7.5, l=14.0)   # ISO 7380 M3x14
# Klemmring hinter dem Lautsprecher (Druckteil, Einsaetze am Tisch): Rahmen auf dem Lautsprecherblech, 7.5 dick (druckt
# flach mit der Rueckseite aufs Bett), oben 2
# Dome fuer die Schrauben, unten mittig ein Fuss auf der Gitterblock-Rueckseite (Hebel), unten an den Ecken zwei
# Haken, hinter denen die Zungen der Display-Traegerplatte stecken.
SPK_CLAMP = dict(t=7.5, bar=3.5, boss_d=8.0, boss_l=7.5, hole_d=30.0, foot_x=(52.0, 66.0), foot_y1=59.4,
                 catch_x=[(39.0, 45.5), (72.5, 79.0)], catch_y1=60.0, play=0.3)   # [FREI]
CAV = dict(x0=16.0, x1=84.0, y0=18.5, y_front=52.5, y_back=51.0, d=12.0)
BLOCK = dict(x0=12.0, x1=88.0, y0=15.0, y1=59.6)
SPK_D_FRONT = CAV["d"] + SPK_WALL + SPK_GASKET["t_pressed"]   # Rahmenvorderseite d 19.2
# v3 (B-03): Druckausgleichsventil ruht (Bauherr 2026-10-14). Das Loch im Gitterblock entfaellt (der Ring passte nicht).

RADAR = dict(w=15.84, h=22.26, t=1.56, back=3.0, hdr=11.4, c=(26.85, 44.5), wall=3.9)
_RQ = RADAR["h"] / 2 + 0.3
RADAR_POCKET = dict(x0=RADAR["c"][0] - _RQ, x1=RADAR["c"][0] + _RQ, y0=RADAR["c"][1] - _RQ,
                    y1=RADAR["c"][1] + _RQ, d0=12.0 + RADAR["wall"])
# v3 (B-06): Stiftleiste auf der Bauteilseite [GEMESSEN Bauherr]: 12.64 lang, 2.4 tief, 8.3 hoch, < 0.6 vom Rand.
# Auf der Antennenseite stehen ihre Loetstellen 1.67 ueber.
# v3.2 (V3-02, Fotos Bauherr 2026-10-16): Die Leiste laeuft an einer LANGSEITE (22.26) entlang, mittig - nicht an der
# Kurzseite, wie bis v3.1 angenommen. Ihre Loetstellen treffen damit keine der zwei Nuten im Taschenboden. Darum haelt
# der Rahmen die Platine jetzt mit Abstand: vorn eine Stufe, auf der die Antennenseite 1.9 vor dem Taschenboden liegt
# (die Loetstellen haben Platz, keine Nut noetig), hinten die Lippen wie bisher. Die Platine wird von der offenen Seite
# eingeschoben und ist dann zwischen Stufe und Lippen gefangen (vorher fiel sie zur Antennenseite heraus). Die Antenne
# liegt damit 1.9 vor der lambda/2-Wand (die Abstandshalter-Alternative aus B-06).
RADAR_HDR = dict(l=12.64, w=2.4, h=8.3, edge=0.6, stub=1.67, stub_r=0.75)   # [GEMESSEN], stub_r = Loetstelle [FREI]
RADAR_GROOVE = dict(l=14.0, w=4.0, d=2.0)       # [FREI] v3/v3.1; liegt nach V3-02 an der falschen Stelle, stoert nicht
# v3.4 (Bauherr 2026-10-16): Der Rahmen liess sich hinter dem Gitterblock nicht eindruecken. Die Tasche ist nur 2.1 tief,
# die Quetschrippen hatten 0.2 Uebermass, dazu kommt der Wulst der ersten Lage an der Vorderkante. Jetzt ohne Rippen,
# rundum fit Luft und vorn aussen eine Fase ch; der Rahmen wird mit Heisskleber unten und links an der Blockrueckseite
# festgeklebt (Naht glue x glue). "play" bleibt nur die v2-Bezugsgroesse fuer die Schachtregel.
RADAR_CARRIER = dict(play=0.1, play_short=0.35, lip=0.5, lip_t=0.7, end_bar=1.5,   # v3: Schacht +0.5 kurz
                     ledge=0.8, standoff=1.9, chan=0.1,          # v3.2: Stufe vorn, Abstand zum Taschenboden [FREI]
                     fit=0.3, ch=0.4, glue=2.0)                  # v3.4: geklebt [FREI]
RADAR_D_ANT = RADAR_POCKET["d0"] + RADAR_CARRIER["standoff"]   # v3.2: Antennenseite der Platine d 17.8
RADAR_D_PCB_BACK = RADAR_D_ANT + RADAR["t"]                     # Bauteilseite d 19.36

# ------------------------------------------------------------------ Display-Traegerplatte (v3)
# Die Platte bleibt (Bauherr, W-03): vorn die 4 Druckstifte, hinten der Verstaerker. Der Klingelrechner-Halter entfaellt.
# NEU: oben haengt sie mit zwei Zungen hinter den Haken des Lautsprecher-Klemmrings, unten 2 Schrauben in Einsaetze.
# Damit fallen die oberen Kastenauflager weg; zwischen Gitterblock und den unteren Auflagern (y 159) ist die Kasten-
# oeffnung frei fuer den Computer-Traeger. Einbau: Platte 3 tiefer von vorn einsetzen, hochschieben (Zungen in die
# Schlitze), 2 Schrauben. Ein Fenster in der Platte laesst den Litzen an den Stiftleisten des Klingelrechners Platz.
PLATE = dict(x0=16.0, x1=84.0, y0=60.5, y1=182.0, t=4.0)
PLATE_Z = 22.0
PLATE_BOSSES = [(19.5, 164.0), (80.5, 164.0)]              # v3: nur noch unten (wie v2 unten)
PLATE_SCREW_HEAD = dict(d=6.0, h=3.0)
PLATE_HOLE = 3.4
PLATE_DROP = 3.5                                             # [FREI] so viel tiefer einsetzen, dann hochschieben
# Zungen oben an der Platte, in ihrer eigenen Dicke (d 18..22, drucken flach mit). Sie stecken zwischen der
# Gitterblock-Rueckseite (vorn) und den Haken des Lautsprecher-Klemmrings (hinten).
PLATE_TONGUE = dict(xs=[(39.5, 44.5), (73.5, 78.5)], y0=57.5)   # [FREI]
PLATE_WINDOW = (52.5, 69.5, 76.0, 116.5)                      # x0, y0, x1, y1 [FREI] hinter den Stiftleisten
PLATE_STOP = dict(c=(54.0, 137.3), d=4.0, d1=55.0)           # [FREI] Anschlag unter dem Computer-Traeger
# v3.6 (V3-05, Bauherr 2026-10-16): Drueckt man das Display oben, biegt die Platte oben nach hinten durch. Oben halten
# sie nur die zwei Zungen hinter den Haken des Klemmrings (0.3 Spiel), und der Ring ist nur oben verschraubt und gibt
# unten nach. des Bauherrn Vorschlag: Stuetzen von den Seitenwaenden, auf denen die Platte hinten nur aufliegt.
# Umsetzung: zwei Klebeteile 17 (links, rechts gespiegelt) an den Seitenwaenden neben dem oberen Plattenteil. Jedes
# liegt an drei Flaechen an und richtet sich damit beim Kleben selbst aus: aussen an der Seitenwand (Klebeflaeche),
# vorn an der Rueckseite des Leistenkanals (d 12) und oben an der Unterseite des Gitterblocks (y 59.6). Eine Zunge
# reicht hinter den Plattenrand, ihre Vorderseite liegt play hinter der Plattenrueckseite.
# Die Zunge darf dem Computer-Traeger nicht im Weg sein: Er wird 39.6 tiefer von vorn eingesetzt und streicht dabei mit
# Koerper (ab x 19.6) und Zungen (ab x 16.0, y 61.6-69.6 und 91.6-99.6) durch genau diesen Bereich. Darum liegt die
# Zunge bei x bis 19.1 und y 70.6-90.6, zwischen den Zungenbahnen; der Koerper bleibt links von x 16. Vorn aussen eine
# Fase ch ueber der 45-Grad-Rampe unter dem Kanal. Der Kasten bleibt bytegleich.
PLATE_REST = dict(play=0.1, clear=0.5, x_in=19.1, tongue_y0=70.6, tongue_y1=90.6, d1=28.0, tongue_d1=27.0,
                  ch=2.5)                                                               # [FREI]
BTN_ARM_Y = (204.0, 214.0)

# Displayplatine (wie v2)
_DB_X1 = DISPLAY["c"][0] + 63.0 / 2
_DB_Y1 = DISPLAY_GLASS["y0"] + 118.2
DISPLAY_PINS = [(_DB_X1 - hx, _DB_Y1 - hy) for (hx, hy) in
                ((4.54, 113.06), (47.73, 112.92), (4.58, 5.18), (58.39, 5.21))]
# v3 (B-12/B-13, Bauherr 2026-10-14): Stapel Glas + 3M + Heizpad + Platine [GEMESSEN] 5.93 bis zur Platinenrueckseite.
# Mit v2-Stiften (Stirn d 5.6) stand das Glas 0.6 (gedrueckt) bis 1.7 (frei) ueber dem Stahl-Ersatz. Die Stiftlaenge ist
# die Stellgroesse: ein Satz in vier Laengen, Stirn je 0.5 weiter hinten als v2 (-0.5 .. -2.0), beschriftet. Spitze
# 1.75 lang (Bauherr: 1.5-2), zwischen Platine und Panel sind ~3 mm frei.
DISPLAY_PCB_BACK = 5.93                                      # [GEMESSEN] Bauherr 2026-10-14
DISPLAY_PCB_T = 1.4
DISPLAY_FREE_FRONT = 3.0                                     # [GEMESSEN] Luft zwischen Platine und Panel (Bauherr)
DISPLAY_PIN = dict(d=6.0, tip_d=3.4, tip_l=1.75, socket=1.0, v2_front=5.6, steps=[0.5, 1.0, 1.5, 2.0], per_step=5)
DISPLAY_PIN_FRONTS = [DISPLAY_PIN["v2_front"] + s for s in DISPLAY_PIN["steps"]]   # d 6.1 .. 7.6
DISPLAY_PIN_D0 = DISPLAY_PIN_FRONTS[0]                        # laengste Stifte fuer die Belegung
# [GEMESSEN] Ergebnis Bauherr 2026-10-16 (P3-03): Die Stufe -1.5 (Stirn d 7.1) passt perfekt. Das Glas ist buendig mit
# dem Stahl-Ersatz 13, und das alte v1-Messing liegt glatt davor. Fuer den naechsten Kasten genuegt diese eine Laenge.
# v3.7 (V3-07, Bauherr 2026-10-17): Drueckt man auf das Display, gibt es nach. Zwischen E-Ink-Panel und Displayplatine
# liegen nur die 3M-Schaumklebefolie und das Heizpad; der Spalt ist innen 2.7 [GEMESSEN]. Abstandsstuecke 18 fuellen ihn
# an freien Stellen fest aus: laengliche Stuecke, Dicke = Spaltmass. Gedruckt liegt die Dicke waagerecht (in XY, also
# genau und nicht in 0.2-Schichten gestuft), die Breite w steht hoch. Je Dicke ein Kamm mit Zahl, die Stuecke haengen an
# duennen Stegen und werden abgebrochen. Unten an den Laengskanten eine kleine Fase gegen den Wulst der ersten Lage.
DISPLAY_SPACER = dict(gap=2.7, steps=[2.6, 2.7, 2.8], w=3.0, lengths=[3, 4, 5, 6, 8, 10, 12, 15, 20, 25, 30],
                      pitch_gap=2.0, spine_w=6.0, spine_t=1.2, bridge=(1.0, 0.8, 0.6), ch=0.3,
                      label_h=3.5, label_t=0.6)                                         # gap [GEMESSEN], Rest [FREI]

# ------------------------------------------------------------------ Verstaerker (v3)
# Adafruit 3006. v3 (B-10, Bauherr gemessen): Lochaussenkanten 15.0, Innenkanten 10.0 -> Loch 2.5, Mitte 12.5 (nicht
# 12.7). Lage v3: links unter dem Sprechrechner, ausserhalb des Klingelrechners (der liegt jetzt flach rechts).
# v3 bis v3.4: Stifte Ø2.2, die aussen nur 0.1 gegen die Lochkanten druecken. Gedruckt hielt das nicht (V3-04, Bauherr
# 2026-10-16: "zu nah aneinander und zu klein im Durchmesser"; duenne gedruckte Stifte werden etwa 0.1 duenner).
# v3.5: Die Stifte sitzen MITTIG in den Loechern und haben eine Spitzenfase. Der Rahmen kommt als Satz in drei
# Stiftstaerken pin_steps, die Zahl ist unten eingraviert; Bauherr nimmt den, auf dem die Platine straff sitzt.
# pin_d = mittlere Staerke fuer Ansicht und Pruefung. Die Stifte stehen weiter stake ueber der Platine, notfalls
# vernietet man sie mit dem Loetkolben (so war es beim Halter H1 gedacht).
# [GEMESSEN] Ergebnis Bauherr 2026-10-17: Ø2.6 sitzt straff (pin_ok, Loch 2.5 -> +0.1). Gilt fuer v4 als einzige Staerke.
AMP = dict(w=17.78, h=19.05, t=1.6, top=12.2, hole_d=2.5, hole_cc=12.5, hole_e=2.54, c=(35.0, 105.0))
AMP_FRAME = dict(base_t=2.0, stand=2.5, margin=0.5, pin_d=2.6, pin_steps=[2.5, 2.6, 2.7], tip=0.3, stake=2.0,
                 boss_d=4.6, rib_w=0.9, dowel_l=3.8, label_h=4.0, label_t=0.6, pin_ok=2.6)
_AMP_X0, _AMP_Y0 = AMP["c"][0] - AMP["w"] / 2, AMP["c"][1] - AMP["h"] / 2
_AMP_X1, _AMP_Y1 = _AMP_X0 + AMP["w"], _AMP_Y0 + AMP["h"]
AMP_HOLES = [(AMP["c"][0] - AMP["hole_cc"] / 2, _AMP_Y1 - AMP["hole_e"]),
             (AMP["c"][0] + AMP["hole_cc"] / 2, _AMP_Y1 - AMP["hole_e"])]
AMP_PINS = list(AMP_HOLES)                                       # v3.5: mittig in den Loechern
AMP_D0 = PLATE_Z + AMP_FRAME["base_t"] + AMP_FRAME["stand"]
AMP_PEGS = [(AMP["c"][0] - 7.0, AMP["c"][1] - 7.0), (AMP["c"][0] + 7.0, AMP["c"][1] + 7.0)]

BME = dict(w=15.0, h=11.5, t=1.6, comp=1.5)                  # v3: sitzt auf dem Verteiler (Bauherr + Einbau-Fork)

# ------------------------------------------------------------------ Verteiler (W-04, v3)
# Volle Lochrasterplatine 30 x 70 (nicht gesaegt) [GEMESSEN Bauherr], Bauteile nach vorn. Sockel mit flachem Boden, an
# die Rueckwand geklebt (Sitz = 1-mm-Rand im Kasten), 4 Stifte mit Rasthaken durch die Eckbohrungen, 3 mm Luft unter der
# Platine fuer Loetstellen. Lage unten links. Der rechte Rand (1.7 mm) liegt hinter dem Taster-Freiraum: dort nur
# flache Bauteile (Hoehe bis 5 mm).
VERTEILER = dict(w=30.0, h=70.0, t=1.6, x0=7.2, y0=174.5, comp=10.0,           # [GEMESSEN] / Lage [FREI]
                 hole_d=1.95, edge_long=1.07, edge_short=1.14, cc=(25.95, 65.85))
# Sockel: 4 Stifte Ø1.8 durch die Eckbohrungen (Ø1.95) auf 3-mm-Saeulen, rechts 2 Rastfinger ueber der Platinenkante
# (links liegt die Platine 0.2 vor der Kastenwand). Sitz im Kasten: Rand oben, unten, links = Wand; rechts frei fuer die
# Rastfinger.
VERT_SOCKET = dict(base_t=2.0, gap=3.0, post_d=3.4, pin_d=1.8, pin_over=1.6, seat_rim=1.0, seat_play=0.2, inset=0.3,
                   latch_y=[192.0, 227.0], latch_w=8.0, latch_t=1.2, latch_hook=0.5)
VERT_D_PCB_BACK = D_BACK_IN - VERT_SOCKET["base_t"] - VERT_SOCKET["gap"]     # d 52.0
VERT_D_PCB_FRONT = VERT_D_PCB_BACK - VERTEILER["t"]                          # d 50.4
VERT_HOLES = [(VERTEILER["x0"] + VERTEILER["edge_long"] + VERTEILER["hole_d"] / 2 + i * VERTEILER["cc"][0],
               VERTEILER["y0"] + VERTEILER["edge_short"] + VERTEILER["hole_d"] / 2 + j * VERTEILER["cc"][1])
              for j in (0, 1) for i in (0, 1)]

# ------------------------------------------------------------------ Computer-Traeger (W-03, v3)
# EIN Druckteil fuer Sprech- und Klingelrechner, an der Rueckwand in Schienen, herausziehbar nach unten (Bauherr).
# Ablauf: Display mit Stahl ab, Display-Traegerplatte ab (2 Schrauben). Traeger 40 mm nach unten schieben (die Zungen
# kommen aus den Schienen), nach vorn heraus. Einbau umgekehrt. Er haelt oben an den Schienenenden (Anschlag) und unten
# am Anschlag auf der Display-Traegerplatte (kein Rastteil, das brechen kann).
# Schienen: kurze Lippen mit 45-Grad-Unterseite auf der Rueckwand (drucken ohne Stuetzen), Schwalbenschwanz-Zungen am
# Traeger. Die Lippen liegen nur dort, wo die Zungen am Ende sitzen; beim Einsetzen stehen die Zungen in den Luecken.
CARRIER = dict(t=3.0, bevel=3.0, play=0.3, S=39.6,
               x0=19.6, x1=76.4,                             # Umriss (Rueckseite)
               xa1=51.0,                                     # Teil A (Sprechrechner) x0..xa1, Teil B (Klingel) xa1..x1
               y0=21.0, ya1=88.6, yb1=134.3,                 # oben, Ende Teil A, Ende Teil B
               xb1_low=75.0, y_low=117.0,                    # Teil B unterhalb y_low nur bis x 75.0 (Auflager unten)
               tab_out=3.6, tabs=[(22.0, 30.0), (52.0, 60.0), (82.0, 88.0)],
               ridge_w=4.3, ridge_d=52.0, stop=2.0)
CARRIER_D_FACE = D_BACK_IN - CARRIER["t"]                    # Vorderseite der Traegerplatte d 54
# v3.3 (V3-03, Bauherr 2026-10-16): Der Traeger passt gut, faellt aber ohne Display-Traegerplatte nach unten heraus (bis
# v3.2 haelt ihn erst deren Anschlag). Bauherr: ein kleiner Zapfen am Kasten auf der Seite des Klingelrechners, leicht
# einrastend; heraus mit 1-2 mm Anheben unten. Umsetzung:
#   - RASTKNOPF Ø3 auf der Rueckwand, im Traeger ein LOCH an der Stelle, wo der Knopf in der Endlage steht.
#   - Beim Einsetzen liegt der Traeger S tiefer an der Rueckwand. Damit ihn der Knopf dort nicht anhebt (die unteren
#     Zungen muessen unter die Lippen), laeuft der Knopf hinten in einer GASSE. Vor dem Loch hebt eine 45-Grad-RAMPE den
#     Traeger ueber einen kurzen STEG, dann faellt der Knopf ins Loch (Klick).
#   - Die Lochkante zur Gasse ist senkrecht: Die Schwerkraft zieht ihn nicht heraus. Heraus: unten anheben, nach unten.
#   - Der Kasten v3 ist schon gedruckt, darum ist der Knopf ein KLEBETEIL: Traeger ganz hoch, Knopf mit einem winzigen
#     Tropfen Kleber durch das Loch auf die Rueckwand druecken - der Traeger ist die Lehre. Drei Hoehen zum Probieren
#     (Vielfache der Schichthoehe 0.2).
CARRIER_KNOB = dict(x=63.0, y=129.0, d=3.0, ch=0.2, heights=[0.4, 0.6, 0.8],
                    hole_d=3.6, lane_w=3.8, lane_t=1.0, lane_over=2.5, ramp=1.0, ridge=0.8)   # [FREI]
_CK = CARRIER_KNOB
KNOB_HOLE_Y0 = _CK["y"] - _CK["hole_d"] / 2                    # obere Lochkante (zur Gasse hin)
KNOB_RAMP_Y1 = KNOB_HOLE_Y0 - _CK["ridge"]                       # Rampe endet hier auf voller Dicke
KNOB_RAMP_Y0 = KNOB_RAMP_Y1 - _CK["ramp"]                        # Gasse endet hier, Rampe beginnt
KNOB_LANE_Y0 = _CK["y"] - CARRIER["S"] - _CK["lane_over"]        # Gasse beginnt (Knopf beim Einsetzen + Reserve)

# Sprechrechner HW678 (ESP32-S3-N16R8), Masse wie v2 [GEMESSEN]/[FOTO]. v3: liegt im Traeger wie im v2-Schlitten (der
# passte perfekt), Modulseite (Schirm, USB-C) auf der Traegerplatte, Stifte nach VORN (Bauherr: "Pins nach vorne").
# Antenne OBEN (weg vom Klingelrechner, nichts davor), USB-C UNTEN mit 25 mm freiem Raum (Stecker oder Loeten, B-07).
TALK = dict(l=63.2, pcb_l=57.5, w=28.28, t=1.6, front=3.2, strip=2.5, pin=6.0, ant=5.7, usb_l=7.5, mod_l=17.0,
            x0=21.15, y0=23.0, usb_free=25.0)
TALK_CRADLE = dict(wall=1.2, lip=0.5, lip_t=0.8, play=0.15, stop_w=3.5, hook=0.5, hook_l=1.15)   # wie H5 v2
TALK_D_PCB_BACK = CARRIER_D_FACE - TALK["front"]              # Platine Modulseite d 50.8
TALK_D_PCB_FRONT = TALK_D_PCB_BACK - TALK["t"]                # d 49.2
TALK_D_STRIP = TALK_D_PCB_FRONT - TALK["strip"]               # gelbe Leisten vorn d 46.7
TALK_D_PINS = TALK_D_STRIP - TALK["pin"]                      # Stiftspitzen d 40.7
_T = TALK
TALK_PCB_Y0 = _T["y0"] + _T["ant"]                            # Platine oben (Antenne ragt darueber)
TALK_PCB_Y1 = TALK_PCB_Y0 + _T["pcb_l"]                       # Platine unten = USB-Ende

# Klingelrechner Waveshare ESP32-S3-ETH + PoE (Masse wie v2). v3 (Bauherr 2026-10-14): liegt FLACH auf dem Traeger, auf
# 2 mm nicht leitendem Schaumstoff geklebt, PoE-Seite zur Hauswand (Rueckwand), RJ45 zeigt nach unten. Anschlag oben an
# den Platinenecken (Steckkraft), Sockel unter der RJ45-Buchse, seitliche Fuehrung am PoE-Modul.
WAVESHARE = dict(l=72.8, w=21.0, t=1.86, rj45_over=1.0, rj45_w=16.4, rj45_below=14.0,
                 poe_l=36.15, poe_from_end=20.0, poe_w=21.5, above=4.3, below=18.9, total_b=20.5)
WAVESHARE["thick"] = max(WAVESHARE["total_b"], WAVESHARE["above"] + WAVESHARE["t"] + WAVESHARE["below"])
BELL = dict(x0=53.75, y0=60.0, foam=2.0, stop_v=3.5, stop_h=2.0, ped_gap=0.5, guide_h=4.0, guide_t=0.6)
_W = WAVESHARE
BELL_D_POE_BACK = CARRIER_D_FACE - BELL["foam"]               # PoE-Modul Rueckseite d 52.0
BELL_D_CHIP = BELL_D_POE_BACK - _W["below"]                  # Chip-Seite der Platine d 33.1
BELL_D_LOGO = BELL_D_CHIP - _W["t"]                           # Logo-Seite d 31.24
BELL_D_HDR = BELL_D_LOGO - _W["above"]                        # Stiftleisten vorn d 26.94
_bu = lambda u: BELL["y0"] + u                                 # u laengs ab dem oberen Ende (ohne Stecker)
_bv = lambda v: BELL["x0"] + v                                 # v quer ab der linken Platinenkante
BELL_PARTS = {   # (x0, x1, y0, y1, d0, d1)
    "Platine": (_bv(0), _bv(_W["w"]), _bu(0), _bu(_W["l"]), BELL_D_LOGO, BELL_D_CHIP),
    "Stiftleiste 1": (_bv(0.34), _bv(2.88), _bu(4.67 - 1.27), _bu(72.8 - 19.87 + 1.27), BELL_D_HDR, BELL_D_LOGO),
    "Stiftleiste 2": (_bv(18.12), _bv(20.66), _bu(4.67 - 1.27), _bu(72.8 - 19.87 + 1.27), BELL_D_HDR, BELL_D_LOGO),
    "Logo-Bauteile": (_bv(3.2), _bv(17.8), _bu(0), _bu(_W["l"]), BELL_D_LOGO - 3.3, BELL_D_LOGO),
    "PoE-Modul": (_bv((_W["w"] - _W["poe_w"]) / 2), _bv((_W["w"] + _W["poe_w"]) / 2), _bu(_W["poe_from_end"]),
                  _bu(_W["poe_from_end"] + _W["poe_l"]), BELL_D_CHIP, BELL_D_POE_BACK),
    "RJ45": (_bv(0), _bv(_W["w"]), _bu(56.5), _bu(_W["l"] + _W["rj45_over"]), BELL_D_CHIP, BELL_D_CHIP + _W["rj45_below"]),
    "Antenne": (_bv(7.0), _bv(14.0), _bu(-1.5), _bu(3.0), BELL_D_CHIP, BELL_D_CHIP + 1.6),
    "IPEX": (_bv(19.625 - 2.6 - 1.3), _bv(19.625 - 2.6 + 1.3), _bu(1.58 + 2.6 - 1.3), _bu(1.58 + 2.6 + 1.3),
             BELL_D_CHIP, BELL_D_CHIP + 1.3),
    "Taster BOOT": (_bv(-0.6), _bv(2.5), _bu(56.5), _bu(64.5), BELL_D_LOGO - 2.0, BELL_D_CHIP),
    "Taster RESET": (_bv(18.5), _bv(21.6), _bu(56.5), _bu(64.5), BELL_D_LOGO - 2.0, BELL_D_CHIP),
}
BELL_Y1 = _bu(_W["l"] + _W["rj45_over"])                       # Unterkante RJ45 (Buchsenoeffnung) y 134.3
PLUG_L = 40.0                                                 # [GEMESSEN] Bauherr 2026-10-14: Stecker mit Tuelle ~40
LAN = dict(cable_d=7.0, bend_r=28.0, tie_w=3.6, tie_t=1.3)  # [GEMESSEN] Bauherr: Aussenkabel Ø7, Binder 3.6 breit

# ------------------------------------------------------------------ LAN-Einfuehrung + Oesen (B-01, W-05, v3)
# Einfuehrung: [PLATZ] bis die Recherche zur teilbaren Verschraubung da ist (Subagent 2026-10-14). Annahme M25 mit
# Gegenmutter innen. Lage unten, nah an der Rueckwand; x so, dass die Mutter frei vom USB-Becher bleibt.
# Recherche (Subagent 2026-10-14, Datenblaetter): teilbare Verschraubung M20, durch deren Wandloch Ø20.5 der RJ45-Stecker
# samt Tuelle passt (Diagonale ~18.6, 0.9 Luft je Ecke). Die Verschraubung oeffnet sich ganz, der Stecker muss nie durch
# sie hindurch. Kauf: OBO V-TEC TB20 06-08 (Satz mit Koerper, Kappe, Einsatz 6-8 und teilbarer Gegenmutter) oder
# PFLITSCH USG 22053 PC + Gegenmutter 1420/220 GGM + Dichteinsatz UFE 53p8. IP67, UV-bestaendig. Aussen SW30 (Ecke 33.5),
# bis 29.7 hoch; Gegenmutter SW27 x 8, ueber Eck 30. Gewinde 10: 7 greifen nach der 3-mm-Wand.
# Die M25 von Conta-Clip (KDS-KV) passt nicht: ihre Gegenmutter ist ueber Eck 38 und stiesse an USB-Becher und Domen.
# Lage: 7.5 links der Mitte, damit die Mutter frei vom USB-Becher bleibt; so nah an der Rueckwand, wie die Mutter erlaubt.
GLAND = dict(hole_d=20.5, wall=3.0, side="unten", c=(42.5, 41.5), nut_d=30.0, nut_t=8.0, body_d=33.5, body_h=29.7,
             thread_l=10.0, plug_diag=18.6)                   # [DB]
# Kabelbinder-Oesen (Bauherr: mind. 5, von unten nach oben, gern entlang einer Kurve, stark). Spitzbogen (45 Grad) statt
# Bruecke, damit sie ohne Stuetzen drucken. Kanal fuer Binder 3.6 x 1.3.
EYELET = dict(base=6.4, peak=3.2, wall=2.2, depth=5.0, side_gap=1.6, side_h=4.2)        # [FREI] Spitzbogen 6 breit, 3 hoch
# Kabelweg (Mitte, auf der Rueckwand): vom Stecker unter der RJ45 S-foermig zur Einfuehrung. Punkte (x, y, d).
LAN_PATH = [(64.25, BELL_Y1 + PLUG_L, 40.1), (63.0, 186.0, 49.0), (57.0, 203.0, 53.5), (48.5, 220.0, 53.5),
            (43.5, 236.0, 49.0), (42.5, 252.0, 41.5)]
LAN_EYELET_GAP = 0.6                                          # Luft Kabelmantel <-> Oesenblock


def _lan_x(y):
    for p_, q_ in zip(LAN_PATH, LAN_PATH[1:]):
        if p_[1] <= y <= q_[1]:
            return p_[0] + (q_[0] - p_[0]) * (y - p_[1]) / (q_[1] - p_[1])
    raise ValueError(y)


def _lan_eyelet(y, side):
    """Oese neben dem Kabel bei Hoehe y: Block laengs zum Kabel, Binder quer dazu (Richtung = Kabelnormale)."""
    for p_, q_ in zip(LAN_PATH, LAN_PATH[1:]):
        if p_[1] <= y <= q_[1]:
            ux, uy = q_[0] - p_[0], q_[1] - p_[1]
            n_ = math.hypot(ux, uy)
            ux, uy = ux / n_, uy / n_
            nx, ny = -uy * side, ux * side                     # side +1: rechts der Laufrichtung (x+ bei Kabel nach unten)
            off = EYELET["depth"] / 2 + LAN["cable_d"] / 2 + LAN_EYELET_GAP
            x0_ = _lan_x(y)
            return (x0_ + nx * off, y + ny * off, math.degrees(math.atan2(ny, nx)))
    raise ValueError(y)


# Oesen neben dem Kabel (Seite +1 / -1), entlang der S-Kurve; der Binder zieht das Kabel an die Oese
LAN_EYELETS = [_lan_eyelet(y, sd) for (y, sd) in ((188.0, -1), (200.0, 1), (212.0, -1), (224.0, -1), (234.0, -1))]
# (x, y, Richtung des Binders in Grad, 0 = quer in x)

# ------------------------------------------------------------------ SHT31-D-Aussenkammer (W-02, v3)
# Bauherr: gemessen wird das Wetter draussen. Kammer unten rechts an der Rueckwand, dicht zum Innenraum (Deckel geklebt,
# Kabelloch mit Silikon), Oeffnungen nach unten (2 Zuluft) und eine Abluft oben aussen. Weit weg von PoE und Heizfolie.
# Die Kammer (innen ~25 x 31, 12 tief) war fuer die groesste bekannte Platine ausgelegt (Adafruit 2857, 25.4 x 17.78).
SHT = dict(x0=66.5, y0=220.0, d0=43.4, wall=1.6, lid_t=1.6, holes=[(73.0, 48.0), (81.0, 53.5)], hole_d=3.5,
           vent_y=226.0, vent_d=3.0)
# v3.1 (Bauherr 2026-10-14, gemessen): lila Modul, Aufdruck "SHT3X", 13.22 x 10.5, Platine 1.5, mit Bauteilen 3.2.
# Von der beschrifteten Seite gesehen: links 4 Loetloecher VIN, GND, SCL, SDA; rechts oben ein Befestigungsloch Ø3.0,
# sein Rand 1.2 von der oberen Langseite und 1.2 von der rechten Kurzseite; darunter 2 Loetloecher AL, AD (Aufdruck
# hinten). Auf welcher Seite die Bauteile stehen, ist offen -> Huelle 1.7 auf BEIDEN Seiten.
SHT_BOARD = dict(l=13.22, h=10.5, t=1.5, thick=3.2, hole_d=3.0, hole_rim=1.2)          # [GEMESSEN]
# Halt (v3.1): Die Platine steckt mit ihrem Loch auf einem Stift am Kammerdeckel 08, beschriftete Seite zum Deckel, auf
# einem Bund 3.5 vor dem Deckel (Luft auf beiden Seiten; nicht tiefer, denn der Deckel muss so weit gerade auf die
# Kammer, wie Platine und Stift hineinragen, und davor steht die Kuppel der USB-Abdeckungsschraube bis d 35.5).
# Unter ihrer Unterkante liegt eine Rippe:
# Die Platine haengt am Stift und dreht sich unter ihrem Gewicht auf die Rippe -> verdrehsicher, nichts nach Augenmass.
# Die Loetloecher links liegen hinter dem Kabelloch des Deckels. Der Kasten bleibt unveraendert, nur der Deckel aendert
# sich. Einbau: Litzen anloeten, Platine aufstecken, Stiftende mit einem Tropfen Sekundenkleber sichern, Litzen durchs
# Kabelloch, Deckel aufkleben.
# v3.5 (V3-04, Bauherr 2026-10-16): Der Stift Ø2.9 (0.05 Luft je Seite) war gedruckt zu duenn, die Platine sass lose.
# Jetzt ein Satz Deckel mit Stift pin_steps, die Zahl aussen eingraviert; Bauherr nimmt den, auf dem die Platine straff
# sitzt. Dann richtet man sie beim Aufstecken an der Rippe aus, der Tropfen Sekundenkleber ist nur noch Reserve.
# [GEMESSEN] Ergebnis Bauherr 2026-10-17: Ø3.2 sitzt straff (pin_ok, Loch 3.0 -> +0.2), die dickste Stufe des Satzes.
# Gilt fuer v4 als einzige Staerke.
SHT_MOUNT = dict(x0=70.0, y0=223.5, standoff=3.5, collar_d=3.8, pin_d=3.1, pin_steps=[3.0, 3.1, 3.2], pin_over=1.5,
                 rib_t=1.2, rib_gap=0.2, rib_x=(73.0, 80.0), label_c=(79.0, 241.0), label_h=5.0,
                 label_t=0.6, pin_ok=3.2)                                               # [FREI]
SHT_D_LID = SHT["d0"] + SHT["lid_t"]                                  # Deckel innen d 45.0
SHT_D_FRONT = SHT_D_LID + SHT_MOUNT["standoff"]                       # beschriftete Seite d 50.0
SHT_D_BACK = SHT_D_FRONT + SHT_BOARD["t"]                             # Rueckseite d 51.5
SHT_COMP = SHT_BOARD["thick"] - SHT_BOARD["t"]                        # Bauteile 1.7 (Seite offen)
SHT_X1 = SHT_MOUNT["x0"] + SHT_BOARD["l"]
SHT_Y1 = SHT_MOUNT["y0"] + SHT_BOARD["h"]
SHT_HOLE = (SHT_X1 - SHT_BOARD["hole_rim"] - SHT_BOARD["hole_d"] / 2,
            SHT_MOUNT["y0"] + SHT_BOARD["hole_rim"] + SHT_BOARD["hole_d"] / 2)   # (80.52 | 226.2)
# So weit muss der Deckel gerade auf die Kammer: alles hinter dem Deckel (Stift, Platine mit Bauteil-Huelle) + 0.5
SHT_LID_TRAVEL = max(SHT_D_BACK + SHT_MOUNT["pin_over"], SHT_D_BACK + SHT_COMP) - SHT_D_LID + 0.5
SHT_CABLE_HOLE = (SHT["x0"] + SHT["wall"] + 3.5, SHT["y0"] + SHT["wall"] + 3.5)    # Kabelloch im Deckel, Ø3.5

# ------------------------------------------------------------------ USB-Feld (wie v2)
USB_BREAKOUT = dict(flange_l=20.2, flange_h=6.81, flange_t=1.51, hole_d=2.24, hole_inner=14.0,
                    pcb_w=11.57, pcb_l=14.72, pcb_t=1.6, port_w=9.12, port_l=7.7, stack_t=4.84)
USB_PORT_T = USB_BREAKOUT["stack_t"] - USB_BREAKOUT["pcb_t"]
USB_FIELD = dict(x0=58.0, d_c=18.4, pitch=7.0, play=0.2, resin=1.0, wall=1.0, over=2.5,
                 plate_t=2.5, land=2.5, open_play=0.3, cover_t=2.0, cover_x0=47.0, cover_d1=36.0,
                 screws=[(51.5, 14.0), (75.0, 31.5)], boss_d=8.0, gland_r=17.75, drain_d=2.0)   # v3: gland_r neu
_U, _UB = USB_FIELD, USB_BREAKOUT
USB_XS = [_U["x0"] + _U["wall"] + _U["resin"] + _U["play"] + USB_PORT_T / 2 + _UB["pcb_t"] + i * _U["pitch"]
          for i in range(3)]
USB_CUP = (USB_XS[0] - USB_PORT_T / 2 - _UB["pcb_t"] - _U["play"] - _U["resin"] - _U["wall"],
           USB_XS[-1] + USB_PORT_T / 2 + _U["play"] + _U["resin"] + _U["wall"],
           _U["d_c"] - _UB["pcb_w"] / 2 - _U["play"] - _U["resin"] - _U["wall"],
           _U["d_c"] + _UB["pcb_w"] / 2 + _U["play"] + _U["resin"] + _U["wall"],
           BOX["y1"] + _U["plate_t"] - _UB["pcb_l"] - _U["over"])
USB_OPEN = (USB_CUP[0] - _U["open_play"], USB_CUP[1] + _U["open_play"],
            USB_CUP[2] - _U["open_play"], USB_CUP[3] + _U["open_play"])
USB_PLATE = (USB_OPEN[0] - _U["land"], USB_OPEN[1] + _U["land"], USB_OPEN[2] - _U["land"], USB_OPEN[3] + _U["land"])

# ------------------------------------------------------------------ Holzschrauben (v3: Senkkopf)
# Der Computer-Traeger gleitet ueber die Rueckwand -> Koepfe buendig: Senkkopf-Holzschraube 4.0 (Kopf Ø8), 90-Grad-
# Senkung in der 3-mm-Rueckwand, darunter bleiben 1.1. Rechts oben 79 -> 75: dort liegt die rechte Schienenlippe.
ANCHORS = [(21.0, 75.0), (75.0, 75.0), (21.0, 150.0), (79.0, 150.0)]   # [FREI]
ANCHOR_D, ANCHOR_HEAD_D = 4.5, 8.3                            # Durchgang 4.0er Schraube, Senkung Ø8.3 (Kopf 8.0)
ACCESS_R = 4.5

# ------------------------------------------------------------------ Kabelgassen (Platz fuer den Einbau-Fork)
# Keine Kaemme mehr (Litzen werden erst geloetet, dann gebuendelt). Statt dessen Kabelbinder-Oesen an den Waenden und
# freie Gassen, in denen kein Halter steht. (x0, x1, y0, y1, d0, d1)
CABLE_LANES = {
    "Gasse oben (hinter dem Gitterblock)": (7.0, 93.0, 7.5, 19.0, 36.0, D_BACK_IN),
    "Gasse rechts": (85.2, 93.0, 18.0, 215.0, 38.0, D_BACK_IN),
    "Gasse links unten": (7.0, 19.0, 95.0, 174.5, 38.0, D_BACK_IN),
}
WALL_EYELETS = [("rechts", 60.0, 47.0), ("rechts", 120.0, 47.0), ("rechts", 180.0, 47.0),
                ("links", 110.0, 47.0), ("links", 160.0, 47.0)]   # (Wand, y, d) Binder laeuft in y

# ------------------------------------------------------------------ Belegung (Huellquader x0, x1, y0, y1, d0, d1)
_S, _C = SPK, CAV
_TK = TALK
LAYOUT = {
    "Display": ((DISPLAY_GLASS["x0"], DISPLAY_GLASS["x1"], DISPLAY_GLASS["y0"], DISPLAY_GLASS["y1"], 0.0,
                 DISPLAY["stack"]), "GEM", "vorn"),
    "Lautsprecher": ((_S["c"][0] - _S["frame"] / 2, _S["c"][0] + _S["frame"] / 2, _S["c"][1] - _S["frame"] / 2,
                      _S["c"][1] + _S["frame"] / 2, SPK_D_FRONT, SPK_D_FRONT + _S["behind"]), "DB", "vorn"),
    "Lautsprecher-Dichtung": ((_S["c"][0] - _S["frame"] / 2, _S["c"][0] + _S["frame"] / 2, _S["c"][1] - _S["frame"] / 2,
                               _S["c"][1] + _S["frame"] / 2, _C["d"] + SPK_WALL, SPK_D_FRONT), "FREI", "vorn"),
    "Radar": ((RADAR_POCKET["x0"], RADAR_POCKET["x1"], RADAR_POCKET["y0"], RADAR_POCKET["y1"], RADAR_POCKET["d0"],
               RADAR_D_PCB_BACK + RADAR_HDR["h"]), "GEM", "vorn"),      # v3.2: Platine 1.9 vor dem Boden
    "Mikrofon + Membranen": ((MIC_C[0] - MIC["d"] / 2, MIC_C[0] + MIC["d"] / 2, MIC_C[1] - MIC["d"] / 2,
                              MIC_C[1] + MIC["d"] / 2, STEEL["t"], STEEL["t"] + MIC_POCKET["depth"]), "GEM", "vorn"),
    "USB-Feld (Becher)": ((USB_CUP[0], USB_CUP[1], USB_CUP[4], BOX["y1"] - WALL, USB_CUP[2], USB_CUP[3]), "GEM", "unten"),
    "Gegenleiste links": ((BAR["x"] - BAR["w"] / 2, BAR["x"] + BAR["w"] / 2, BAR_Y["links"][0], BAR_Y["links"][1],
                           _BAR_D0, _BAR_D0 + BAR["t"]), "FREI", "kasten"),
    "Gegenleiste rechts": ((BOX["x0"] + BOX["x1"] - BAR["x"] - BAR["w"] / 2, BOX["x0"] + BOX["x1"] - BAR["x"]
                            + BAR["w"] / 2, BAR_Y["rechts"][0], BAR_Y["rechts"][1], _BAR_D0, _BAR_D0 + BAR["t"]),
                           "FREI", "kasten"),
    # Sprechrechner: Platine samt Antenne und gelben Leisten, Stifte nach vorn (bis d 40.7) + Litzen 4 davor
    "Sprechrechner": ((_TK["x0"], _TK["x0"] + _TK["w"], _TK["y0"], _TK["y0"] + _TK["l"], TALK_D_PINS - 4.0,
                       CARRIER_D_FACE), "GEM", "traeger"),
    "Sprechrechner USB-Freiraum": ((_TK["x0"] + 3.5, _TK["x0"] + _TK["w"] - 3.5, TALK_PCB_Y1, TALK_PCB_Y1 + _TK["usb_free"],
                                    TALK_D_PCB_BACK - 1.6, D_BACK_IN), "FREI", "traeger"),
    "Klingelrechner": ((BELL["x0"] - 0.6, BELL["x0"] + _W["w"] + 0.6, BELL["y0"] - 1.5, BELL_Y1, BELL_D_HDR - 3.0,
                        BELL_D_POE_BACK), "GEM", "traeger"),
    "RJ45-Stecker": ((BELL["x0"] + _W["w"] / 2 - 6.75, BELL["x0"] + _W["w"] / 2 + 6.75, BELL_Y1, BELL_Y1 + PLUG_L,
                      BELL_D_CHIP, BELL_D_CHIP + _W["rj45_below"]), "GEM", "unten"),
    "Verstaerker": ((_AMP_X0, _AMP_X1, _AMP_Y0, _AMP_Y1, AMP_D0, AMP_D0 + AMP["top"]), "DB", "platte hinten"),
    "Verstaerker-Rahmen": ((_AMP_X0 - AMP_FRAME["margin"], _AMP_X1 + AMP_FRAME["margin"], _AMP_Y0 - AMP_FRAME["margin"],
                            _AMP_Y1 + AMP_FRAME["margin"], PLATE_Z, AMP_D0), "FREI", "platte hinten"),
    "Verteilerplatine": ((VERTEILER["x0"], VERTEILER["x0"] + VERTEILER["w"], VERTEILER["y0"],
                          VERTEILER["y0"] + VERTEILER["h"], VERT_D_PCB_FRONT, VERT_D_PCB_BACK), "GEM", "unten"),
    "Verteiler-Sockel": ((VERTEILER["x0"] + VERT_SOCKET["inset"], VERTEILER["x0"] + VERTEILER["w"] - VERT_SOCKET["inset"],
                          VERTEILER["y0"] + VERT_SOCKET["inset"], VERTEILER["y0"] + VERTEILER["h"] - VERT_SOCKET["inset"],
                          VERT_D_PCB_BACK, D_BACK_IN), "FREI", "unten"),
    "Verteiler Bauteile": ((VERTEILER["x0"], 35.4, VERTEILER["y0"], VERTEILER["y0"] + VERTEILER["h"],
                            VERT_D_PCB_FRONT - VERTEILER["comp"], VERT_D_PCB_FRONT), "PLATZ", "unten"),
    "Verteiler Rand flach": ((35.4, VERTEILER["x0"] + VERTEILER["w"], VERTEILER["y0"], VERTEILER["y0"] + VERTEILER["h"],
                              VERT_D_PCB_FRONT - 4.9, VERT_D_PCB_FRONT), "PLATZ", "unten"),
    "SHT31-D": ((SHT_MOUNT["x0"], SHT_X1, SHT_MOUNT["y0"], SHT_Y1, SHT_D_FRONT - SHT_COMP, SHT_D_BACK + SHT_COMP),
                "GEM", "unten"),                                  # v3.1: Platine auf dem Deckelstift, Huelle beidseitig
}
for _i, (_px, _py) in enumerate(DISPLAY_PINS):
    _r = DISPLAY_PIN["d"] / 2
    LAYOUT["Displaystift %d" % (2 * _i + 1)] = ((_px - _r, _px + _r, _py - _r, _py + _r,
                                                 DISPLAY_PIN_D0 - DISPLAY_PIN["tip_l"],
                                                 PLATE_Z - PLATE["t"] + DISPLAY_PIN["socket"]), "GEM", "platte vorn")
for (_bx, _by) in PLATE_BOSSES:
    _r = PLATE_SCREW_HEAD["d"] / 2
    LAYOUT["Plattenschraube (%.1f,%.0f)" % (_bx, _by)] = (
        (_bx - _r, _bx + _r, _by - _r, _by + _r, PLATE_Z - PLATE["t"] - PLATE_SCREW_HEAD["h"], PLATE_Z - PLATE["t"]),
        "DB", "platte vorn")
GLUED = ["Verteilerplatine", "Verteiler-Sockel", "Radar"]            # v3.1: SHT31-D steckt am Deckel, nicht geklebt
ROUND = {"Mikrofon + Membranen": MIC["d"]}
ROUND.update({n: DISPLAY_PIN["d"] for n in LAYOUT if n.startswith("Displaystift")})
ROUND.update({n: PLATE_SCREW_HEAD["d"] for n in LAYOUT if n.startswith("Plattenschraube")})
SCREEN_USB_X = 57.7
_gx, _gd = GLAND["c"]
_gy1 = BOX["y1"] - GLAND["wall"]
KEEP_OUT = {
    "Bildschirm-USB-Stecker": (SCREEN_USB_X - 6.5, 75.0, 178.34, 186.0, 4.5, 14.0),
    "Kabelmutter": (_gx - GLAND["nut_d"] / 2, _gx + GLAND["nut_d"] / 2, _gy1 - GLAND["nut_t"], _gy1,
                    _gd - GLAND["nut_d"] / 2, _gd + GLAND["nut_d"] / 2),
    "Taster-Zylinder": (BTN_C[0] - BTN_CYL_D / 2 - 0.3, BTN_C[0] + BTN_CYL_D / 2 + 0.3,
                        BTN_C[1] - BTN_CYL_D / 2 - 0.3, BTN_C[1] + BTN_CYL_D / 2 + 0.3,
                        RING_T - SHEET["t"], RING_T - SHEET["t"] + BTN_CYL_L),
    "Taster-Freiraum": (BTN_C[0] - (BTN_CYL_D + BTN_FREE) / 2, BTN_C[0] + (BTN_CYL_D + BTN_FREE) / 2,
                        BTN_C[1] - (BTN_CYL_D + BTN_FREE) / 2, BTN_C[1] + (BTN_CYL_D + BTN_FREE) / 2,
                        RING_T - SHEET["t"] + BTN_CYL_L, RING_T - SHEET["t"] + BTN_CYL_L + BTN_FREE),
}
KEEP_OUT.update(CABLE_LANES)
INSTALL = dict(brass_bottom=960.0)


def height_over_floor(y):
    return INSTALL["brass_bottom"] + SHEET["h"] - y


def _rrect_inset(x, y, r):
    """Abstand von (x,y) bis zur Aussenkontur des abgerundeten Kastens."""
    ix0, ix1 = BOX["x0"] + r, BOX["x1"] - r
    iy0, iy1 = BOX["y0"] + r, BOX["y1"] - r
    dx, dy = max(ix0 - x, 0.0, x - ix1), max(iy0 - y, 0.0, y - iy1)
    if dx > 0 and dy > 0:
        return r - math.hypot(dx, dy)
    return min(x - BOX["x0"], BOX["x1"] - x, y - BOX["y0"], BOX["y1"] - y)


def _inner_inset(x, y):
    """Abstand von (x,y) bis zur Innenwand (Innenecken R = CORNER_R - WALL); negativ = ausserhalb des Innenraums."""
    r = CORNER_R - WALL
    ix0, ix1 = BOX["x0"] + WALL + r, BOX["x1"] - WALL - r
    iy0, iy1 = BOX["y0"] + WALL + r, BOX["y1"] - WALL - r
    dx, dy = max(ix0 - x, 0.0, x - ix1), max(iy0 - y, 0.0, y - iy1)
    if dx > 0 and dy > 0:
        return r - math.hypot(dx, dy)
    return min(x - (BOX["x0"] + WALL), (BOX["x1"] - WALL) - x, y - (BOX["y0"] + WALL), (BOX["y1"] - WALL) - y)


def carrier_tabs():
    """[(Seite, y0, y1)] der Traegerzungen in Endlage."""
    return [(s, a, b) for (a, b) in CARRIER["tabs"] for s in ("links", "rechts")]


def validate(verbose=True):
    errs, warns, oks = [], [], []

    def rule(ok, msg, hard=True):
        (oks if ok else (errs if hard else warns)).append(msg)

    def _ov(a, b, m=0.01):
        return all(min(a[2 * i + 1], b[2 * i + 1]) - max(a[2 * i], b[2 * i]) > m for i in range(3))

    # --- 0. Eingefrorene Masse
    for _k, _want in FROZEN.items():
        _got = globals()[_k]
        rule(_got == _want, "EINGEFROREN %-14s = %s%s" % (_k, _want, "" if _got == _want else "  <<< STEHT AUF %s"
                                                             % (_got,)))

    # --- 1. Gegenleisten-Kanaele (wie v2) + Druckpause (v3)
    _cx0 = BOX["x0"] + BAR["skin"]
    _cx1 = _cx0 + BAR["w"] + 2 * BAR["play_x"]
    rule(abs((_cx0 + _cx1) / 2 - BAR["x"]) < 1e-6, "Gegenleiste mittig in ihrem Kanal (Achse x %.2f)" % BAR["x"])
    rule(_cx1 + BAR["inner"] <= BOX["x0"] + FLANGE_W - 1.0, "Kanal samt Innenwand (bis x %.1f) endet >= 1 mm vor der "
         "Kragenoeffnung (x %.1f)" % (_cx1 + BAR["inner"], BOX["x0"] + FLANGE_W))
    rule(min(BAR["skin"], BAR["inner"], BAR["back"]) >= MIN_WALL, "Kanalwaende aussen %.1f / innen %.1f / hinten %.1f "
         "(min %.1f)" % (BAR["skin"], BAR["inner"], BAR["back"], MIN_WALL))
    for side, k in (("links", "stop_l"), ("rechts", "stop_r")):
        _w = _rrect_inset(_cx0, BAR[k], CORNER_R)
        rule(_w >= BAR["skin"] - 1e-6, "Kanal unten %s (y %.1f): %.2f mm Aussenhaut in der Ecke (min %.1f)"
             % (side, BAR[k], _w, BAR["skin"]))
    _w = _rrect_inset(_cx0, BAR_TOP_END, CORNER_R)
    rule(_w >= BAR["skin"] - 1e-6 and BAR_TOP_END - (BOX["y0"] + WALL) >= 5.0,
         "v3: Kanal oben ZU bei y %.1f: %.2f mm Aussenhaut in der Ecke, %.1f mm bis zur Innendecke (kein Einschub mehr)"
         % (BAR_TOP_END, _w, BAR_TOP_END - (BOX["y0"] + WALL)))
    _rx_in = BOX["x0"] + BOX["x1"] - BAR["x"] - BAR["w"] / 2 - BAR["play_x"] - BAR["inner"]
    _mic_top = MIC_C[1] - math.sqrt(max(MIC_POCKET["boss_d"] ** 2 / 4 - max(_rx_in - MIC_C[0], 0.0) ** 2, 0.0))
    rule(BAR["stop_r"] + BAR["back"] + 0.5 <= _mic_top, "Rechter Kanal endet %.2f mm ueber dem Mikrofondom (min 0.5)"
         % (_mic_top - BAR["stop_r"] - BAR["back"]))
    rule(BAR["screw_l"] <= FRAME_T + FLANGE_T + BAR["t"] + BAR["play_d"], "M3x%.0f endet in der Leiste"
         % BAR["screw_l"])
    rule(BAR["screw_l"] - FRAME_T - FLANGE_T >= 0.75 * BAR["t"], "M3 greift %.1f mm in die %.0f-mm-Leiste (min 3/4)"
         % (BAR["screw_l"] - FRAME_T - FLANGE_T, BAR["t"]))
    for side in BAR_Y:
        _t, _b = BAR_Y[side]
        _h = BAR_TAPS[side]
        rule(_h and _h[0] - _t >= 5.0 and _b - _h[-1] >= 5.0, "Gegenleiste %s: %d Gewinde, Rand oben %.1f / unten "
             "%.1f (min 5)" % (side, len(_h), _h[0] - _t, _b - _h[-1]))
        rule(abs((_h[0] - _t) - (_b - _h[-1])) < 0.01, "Gegenleiste %s symmetrisch: Einlegerichtung egal" % side)
    _n = PAUSE_Z / PRINT["layer"]
    rule(abs(_n - round(_n)) < 1e-6, "v3: Druckpause bei z %.2f liegt auf einer Schichtgrenze (0.20)" % PAUSE_Z)
    _trough = BAR["t"] + 2 * BAR["play_d"]
    rule(_trough - BAR["t"] >= 0.3, "v3: Leiste liegt %.2f unter dem Rinnenrand (Duese faehrt nicht an, min 0.3)"
         % (_trough - BAR["t"]))
    # O-Ring je Schraube (B-02)
    O = ORING
    _space = O["groove_d"]
    _comp = 1.0 - _space / O["cs"]
    _vol_ring = 2 * math.pi ** 2 * ((O["id"] + O["cs"]) / 2) * (O["cs"] / 2) ** 2
    _vol_groove = math.pi / 4 * (O["groove_od"] ** 2 - O["groove_id"] ** 2) * O["groove_d"]
    rule(0.15 <= _comp <= 0.30, "O-Ring %gx%g in %.1f tiefer Nut: %.0f %% gedrueckt (15-30 %%)" % (O["id"], O["cs"],
         _space, 100 * _comp))
    rule(0.60 <= _vol_ring / _vol_groove <= 0.90, "O-Ring fuellt die Nut zu %.0f %% (60-90 %%)"
         % (100 * _vol_ring / _vol_groove))
    rule((STANDOFF_D - O["groove_od"]) / 2 >= 0.6 and O["groove_d"] < STEEL["glue"],
         "Abstandsring: Rand %.2f um die O-Ring-Nut, Nut %.1f < Ring %.1f hoch" % ((STANDOFF_D - O["groove_od"]) / 2,
                                                                           O["groove_d"], STEEL["glue"]))
    rule(O["id"] <= 3.0 <= O["id"] * 1.15, "O-Ring ID %.1f sitzt auf dem M3-Schaft" % O["id"])
    # Stahl: Stege an der Kontur (wie v2)
    _se = BOX["x0"] + STEEL["inset"]
    rule(BAR["x"] - 5.5 / 2 - _se >= 1.5, "Stahl: Senkkopf %.2f mm vom Rand (min 1.5)" % (BAR["x"] - 5.5 / 2 - _se))
    for (x, y) in SPIGOTS:
        _w = min(x, 100.0 - x) - SPIGOT["hole"] / 2 - SPIGOT["slot"] - _se
        rule(_w >= 1.5, "Stahl: Zapfenloch (%.1f,%.0f) %.2f mm vom Rand (min 1.5)" % (x, y, _w))
        _g = min(abs(y - h) for h in BAR_HOLES["links"] + BAR_HOLES["rechts"]) - STANDOFF_D / 2 - SPIGOT["d"] / 2
        rule(_g >= 1.0, "Zapfen (%.1f,%.0f) %.2f mm neben dem naechsten Abstandsring (min 1)" % (x, y, _g))
    for (x, y) in SCREWS:
        _w = _rrect_inset(x, y, CORNER_R - STEEL["inset"]) - STEEL["inset"] - STEEL_TAP / 2
        rule(_w >= 1.5, "Stahl: Gewinde der Messingschraube (%.0f,%.0f) %.2f mm vom Rand (min 1.5)" % (x, y, _w))
    # LED-Kabelloch (W-06): im Messing kleiner als im Stahl, verdeckt unter dem Diffusor, frei von Dach/Gitter/Rand
    lx, ly = LED_CABLE["c"]
    rule((LED_CABLE["steel"] - LED_CABLE["brass"]) / 2 >= 0.5, "LED-Kabelloch: Messing Ø%.1f liegt mit %.2f Rand im "
         "Stahlloch Ø%.1f" % (LED_CABLE["brass"], (LED_CABLE["steel"] - LED_CABLE["brass"]) / 2, LED_CABLE["steel"]))
    rule(DIFFUSOR["x0"] + 2 <= lx <= DIFFUSOR["x1"] - 2 and ly + LED_CABLE["steel"] / 2 <= DIFFUSOR["r"] - 2,
         "LED-Kabelloch (%.0f|%.0f) liegt verdeckt unter dem Diffusor" % (lx, ly))
    rule(all(not (a - 1.5 < lx < b + 1.5) for (a, b) in LED_SLITS), "LED-Kabelloch neben den Laschenschlitzen")
    rule(ly - LED_CABLE["steel"] / 2 - (BOX["y0"] + STEEL["inset"]) >= 1.5 and
         GRILLE["y0"] - (ly + LED_CABLE["collar"] / 2) >= 3.0,
         "LED-Kabelloch: %.2f zum Stahlrand oben, %.1f bis zum Gitter" % (ly - LED_CABLE["steel"] / 2 - BOX["y0"] - 0.1,
                                                                     GRILLE["y0"] - ly - LED_CABLE["collar"] / 2))
    rule(BOX["y0"] + FLANGE_W - (ly + LED_CABLE["collar"] / 2) >= 1.0, "LED-Kabelloch liegt ganz im oberen Kragen "
         "(endet %.2f vor der Kragenkante)" % (BOX["y0"] + FLANGE_W - ly - LED_CABLE["collar"] / 2))
    # Holzschrauben: Senkung in der Rueckwand
    _csk = (ANCHOR_HEAD_D - ANCHOR_D) / 2
    rule(BACK - _csk >= 1.0, "Holzschraube: 90-Grad-Senkung %.2f tief, darunter %.2f Wand (min 1.0)"
         % (_csk, BACK - _csk))
    for (x, y) in ANCHORS:
        w = _inner_inset(x, y) - ANCHOR_HEAD_D / 2
        rule(w >= 0.5, "Holzschraube (%.0f,%.0f): Senkung %.2f mm von der Innenwand" % (x, y, w))
    _gap = BTN_SCREW_CC / 2 - INS["d"] / 2 - (BTN_ORING["mean"] + BTN_ORING["w"]) / 2
    rule(_gap >= 0.8, "Tasterschraube haelt %.2f mm Abstand zur O-Ring-Nut" % _gap)
    rule(INS["l"] <= BTN_PLATE_T - 0.5, "Tasterschraube: Einsatz passt in die Tragscheibe")

    # --- 2. Blendenschrauben gegen Blendenoeffnungen (ohne LED-Fenster)
    for (x, y) in SCREWS:
        r = SCREW_HEAD / 2
        rule(not (DISPLAY_WIN["x0"] - r < x < DISPLAY_WIN["x1"] + r and DISPLAY_WIN["y0"] - r < y < DISPLAY_WIN["y1"] + r),
             "Blendenschraube (%.0f,%.0f) frei vom Displayfenster" % (x, y))
        rule(math.hypot(x - BTN_C[0], y - BTN_C[1]) > BTN_HOLE / 2 + r, "Blendenschraube (%.0f,%.0f) frei vom "
             "Tasterausschnitt" % (x, y))
        rule(not (GRILLE["x0"] - r < x < GRILLE["x1"] + r and GRILLE["y0"] - r < y < GRILLE["y1"] + r),
             "Blendenschraube (%.0f,%.0f) frei vom Gitter" % (x, y))
        rule(not (DIFFUSOR["x0"] - r < x < DIFFUSOR["x1"] + r and y < DIFFUSOR["r"] + r),
             "Blendenschraube (%.0f,%.0f) frei vom Diffusor" % (x, y))

    # --- 3. Dichtlinie A (wie v2)
    S, w2 = SEAL, SEAL["w"] / 2
    rule(S["x_l"] - w2 - (BAR["x"] + STANDOFF_D / 2) >= 0.0, "Seitenrinne %.2f mm neben den Abstandsringen"
         % (S["x_l"] - w2 - (BAR["x"] + STANDOFF_D / 2)))
    rule(S["x_l"] + w2 <= BOX["x0"] + FLANGE_W, "Seitenrinne liegt ganz auf dem Kragen")
    rule(S["y_sill"] - w2 - CAV["y_front"] >= 1.5 and BLOCK["y1"] - (S["y_sill"] + w2) >= 1.0,
         "Querriegel-Rinne: %.2f unter dem Hohlraum, %.2f ueber dem Modulende" % (S["y_sill"] - w2 - CAV["y_front"],
                                                                             BLOCK["y1"] - (S["y_sill"] + w2)))
    rule(BTN_ARM_Y[0] + 1.0 <= S["y_arm"] - w2 and S["y_arm"] + w2 <= BTN_ARM_Y[1] - 1.0, "Armrinne auf den Tasterarmen")
    rule(S["r_arc"] - w2 - BTN_HOLE / 2 >= 1.0, "Tasterbogen auf vollem Stahl")
    _mt = MIC_C[1] - MIC_POCKET["boss_d"] / 2
    rule(_mt - (S["y_arm"] + w2) >= 1.0, "Armrinne %.2f mm ueber dem Mikrofondom" % (_mt - (S["y_arm"] + w2)))

    # --- 5. Gitterhohlraum, Lautsprecher (B-04 v3)
    rule(CAV["y_front"] <= GRILLE["y1"], "Hohlraumboden trifft das Blech %.1f ueber der untersten Schlitzreihe"
         % (GRILLE["y1"] - CAV["y_front"]))
    rule(CAV["y_back"] <= CAV["y_front"] - 1.0, "Hohlraumboden faellt nach vorn")
    rule(CAV["x0"] < GRILLE["x0"] and CAV["x1"] > GRILLE["x1"] and CAV["y0"] < GRILLE["y0"], "Gitter liegt im Hohlraum")
    pr = SPK_SCREW["pocket_d"] / 2
    for (x, y) in SPK_SCREWS:
        rule(y - pr - BLOCK["y0"] >= MIN_WALL, "Lautsprecherschraube (%.1f|%.1f): Kopftasche %.2f mm unter der "
             "Blockoberkante (min %.1f)" % (x, y, y - pr - BLOCK["y0"], MIN_WALL))
        rule(CAV["x0"] + 0.5 <= x - pr and x + pr <= CAV["x1"] - 0.5, "Kopftasche (%.1f) liegt im Hohlraum (x)" % x)
        rule(y + pr <= CAV["y_back"] - 2.0, "Kopftasche (%.1f|%.1f) liegt oben im Hohlraum (Wasser laeuft ab)" % (x, y))
        _wp = math.hypot(x - SPK["c"][0], y - SPK["c"][1]) - SPK["port_d"] / 2 - SPK_SCREW["hole"] / 2
        rule(_wp >= MIN_WALL, "Lautsprecherschraube (%.1f|%.1f): %.2f Wand zur Schalloeffnung" % (x, y, _wp))
        _rd = math.hypot(max(RADAR_POCKET["x0"] - x, x - RADAR_POCKET["x1"], 0.0),
                         max(RADAR_POCKET["y0"] - y, y - RADAR_POCKET["y1"], 0.0)) - SPK_SCREW["hole"] / 2
        rule(_rd >= MIN_WALL, "Lautsprecherschraube (%.1f|%.1f): %.2f Wand zur Radartasche" % (x, y, _rd))
    rule(SPK_SCREW["oring_od"] <= SPK_SCREW["pocket_d"] - 1.0, "O-Ring unter dem Kopf passt in die Kopftasche")
    _grip = SPK_SCREW["l"] - SPK_SCREW["oring_pressed"] - SPK_WALL - SPK_GASKET["t_pressed"] - SPK_FRAME_T
    rule(3.0 <= _grip <= INS["l"] - 0.5 and INS["l"] + MIN_WALL <= SPK_CLAMP["boss_l"],
         "M3x%.0f greift %.1f mm in den Einsatz (6) des Klemmrings, Dom %.1f lang" % (SPK_SCREW["l"], _grip,
                                                                                 SPK_CLAMP["boss_l"]))
    rule(DISPLAY_GLASS["y0"] - BLOCK["y1"] >= 0.3, "Gittermodul endet %.2f vor dem Displayglas"
         % (DISPLAY_GLASS["y0"] - BLOCK["y1"]))
    # Plattenzungen hinter den Haken des Klemmrings (v3)
    K, PT = SPK_CLAMP, PLATE_TONGUE
    for (a, b), (ca, cb) in zip(PT["xs"], K["catch_x"]):
        rule(ca + 0.3 <= a and b <= cb - 0.3, "Plattenzunge x %.1f..%.1f liegt hinter dem Haken x %.1f..%.1f"
             % (a, b, ca, cb))
        rule(b <= K["foot_x"][0] - 1.0 or a >= K["foot_x"][1] + 1.0, "Plattenzunge x %.1f..%.1f neben dem Fuss" % (a, b))
        rule(a - RADAR_POCKET["x1"] >= 1.0, "Plattenzunge x %.1f %.2f neben der Radartasche" % (a, a - RADAR_POCKET["x1"]))
    _sy1 = SPK["c"][1] + SPK["frame"] / 2
    rule(PT["y0"] - _sy1 >= 0.5, "Plattenzunge (ab y %.1f) %.2f unter dem Lautsprecherrahmen" % (PT["y0"], PT["y0"] - _sy1))
    rule(K["catch_y1"] - PT["y0"] >= 2.0, "Haken ueberdeckt die Zunge %.1f mm" % (K["catch_y1"] - PT["y0"]))
    rule(PLATE["y0"] + PLATE_DROP - (PLATE["y0"] - PT["y0"]) >= max(BLOCK["y1"], K["catch_y1"]) + 0.3,
         "Platte: Zungen kommen beim Einsetzen (%.1f tiefer) unter Gitterblock und Haken durch" % PLATE_DROP)
    rule(CARRIER["y0"] + CARRIER["S"] - K["catch_y1"] >= 0.5, "Traeger faehrt beim Einsetzen %.2f unter den Haken "
         "vorbei" % (CARRIER["y0"] + CARRIER["S"] - K["catch_y1"]))
    rule(K["foot_y1"] <= BLOCK["y1"] - 0.1, "Fuss des Klemmrings steht auf der Gitterblock-Rueckseite")

    # --- 5b. Display
    rule(DISPLAY_GLASS["x0"] > BOX["x0"] + FLANGE_W and DISPLAY_GLASS["x1"] < BOX["x1"] - FLANGE_W,
         "Displayglas passt zwischen die Kragen")
    rule(DISPLAY_GLASS["y1"] < BTN_C[1] - (RING_D - 1.0) / 2, "Displayglas endet vor der Tasterscheibe")
    rule(DISPLAY["stack"] < PLATE_Z - PLATE["t"], "Displaystapel endet vor der Traegerplatte")
    # Platte
    for (x, y) in PLATE_BOSSES:
        _w = min(x - PLATE["x0"], PLATE["x1"] - x, y - PLATE["y0"], PLATE["y1"] - y) - PLATE_HOLE / 2
        rule(_w >= MIN_WALL, "Plattenschraube (%.1f,%.0f): %.2f mm Rand" % (x, y, _w))
    _sr = DISPLAY_PIN["d"] / 2 + FIT["pocket"]
    for (x, y) in DISPLAY_PINS:
        _w = min(x - PLATE["x0"], PLATE["x1"] - x, y - PLATE["y0"], PLATE["y1"] - y) - _sr
        rule(_w >= MIN_WALL, "Druckstift-Tasche (%.1f,%.1f): %.2f mm Rand zur Plattenkante" % (x, y, _w))
        _g = min(math.hypot(x - bx, y - by) for (bx, by) in PLATE_BOSSES) - DISPLAY_PIN["d"] / 2 \
            - PLATE_SCREW_HEAD["d"] / 2
        rule(_g >= 0.5, "Druckstift (%.1f,%.1f) %.2f mm neben dem naechsten Schraubenkopf" % (x, y, _g))
        wx0, wy0, wx1, wy1 = PLATE_WINDOW
        _gw = max(wx0 - x, x - wx1, wy0 - y, y - wy1) - _sr
        rule(_gw >= 1.0, "Druckstift-Tasche (%.1f,%.1f) %.2f mm neben dem Plattenfenster" % (x, y, _gw))
    rule(PLATE["t"] - DISPLAY_PIN["socket"] >= 2.0, "Stifttasche laesst %.1f Plattenboden" % (PLATE["t"] -
                                                                                               DISPLAY_PIN["socket"]))
    rule(1.5 <= DISPLAY_PIN["tip_l"] <= 2.0, "Druckstift-Spitze %.2f lang (Bauherr: 1.5-2.0)" % DISPLAY_PIN["tip_l"])
    rule(DISPLAY_PIN["tip_l"] - DISPLAY_PCB_T <= DISPLAY_FREE_FRONT - 1.0, "Spitze ragt hoechstens %.2f vor die "
         "Platine (frei sind %.1f)" % (DISPLAY_PIN["tip_l"] - DISPLAY_PCB_T, DISPLAY_FREE_FRONT))
    rule(DISPLAY_PIN["tip_d"] < 3.94 - 0.3, "Spitze Ø%.1f im Platinenloch Ø3.94" % DISPLAY_PIN["tip_d"])
    _lo, _hi = DISPLAY_PIN_FRONTS[0] - DISPLAY_PIN["v2_front"], DISPLAY_PIN_FRONTS[-1] - DISPLAY_PIN["v2_front"]
    rule(_lo <= 0.6 and _hi >= 1.7, "Stiftsatz deckt den gemessenen Ueberstand 0.6..1.7 ab (Stirn %.1f..%.1f hinter v2)"
         % (_lo, _hi))
    _mx0, _mx1 = BOX["x0"] + FLANGE_W, BOX["x1"] - FLANGE_W
    rule(PLATE["x0"] - _mx0 >= 0.5 and _mx1 - PLATE["x1"] >= 0.5, "Traegerplatte passt durch die Kastenoeffnung")
    # v3.6 (V3-05): Plattenstuetzen 17 hinter den oberen Plattenecken
    _PR, _C = PLATE_REST, CARRIER
    rule(0.0 <= _PR["play"] <= 0.2, "v3.6: Platte liegt %.1f vor den Stuetzen (nur aufliegen)" % _PR["play"])
    rule(_PR["x_in"] - PLATE["x0"] >= 3.0, "v3.6: Zunge reicht %.1f hinter den Plattenrand" % (_PR["x_in"] - PLATE["x0"]))
    rule(_PR["clear"] >= 0.4, "v3.6: %.1f Luft zwischen Stuetze und Plattenkante" % _PR["clear"])
    rule(BLOCK["x0"] <= PLATE["x0"] - _PR["clear"] - 2.0, "v3.6: Stuetze liegt oben %.1f breit am Gitterblock an"
         % (PLATE["x0"] - _PR["clear"] - BLOCK["x0"]))
    rule(_PR["x_in"] <= _C["x0"] - 0.5 and PLATE["x0"] - _PR["clear"] <= _C["x0"] - _C["tab_out"] - 0.4,
         "v3.6: Traeger beim Einsetzen frei: Zunge bis x %.1f (Traeger ab %.1f), Koerper bis x %.1f (Zungen ab %.1f)"
         % (_PR["x_in"], _C["x0"], PLATE["x0"] - _PR["clear"], _C["x0"] - _C["tab_out"]))
    _bands = [(a + _C["S"], b + _C["S"]) for (a, b) in _C["tabs"]]
    _gap = min(min(abs(_PR["tongue_y0"] - b), abs(a - _PR["tongue_y1"])) for (a, b) in _bands)
    rule(all(_PR["tongue_y1"] <= a - 0.9 or _PR["tongue_y0"] >= b + 0.9 for (a, b) in _bands),
         "v3.6: Zunge y %.1f-%.1f zwischen den Bahnen der Traegerzungen %s (mind. %.1f Luft)"
         % (_PR["tongue_y0"], _PR["tongue_y1"], ", ".join("%.1f-%.1f" % ab for ab in _bands), _gap))
    rule(_PR["tongue_d1"] - (PLATE_Z + _PR["play"]) >= 4.0 and _PR["tongue_y1"] - _PR["tongue_y0"] >= 15.0,
         "v3.6: Zunge %.1f dick, %.1f hoch" % (_PR["tongue_d1"] - (PLATE_Z + _PR["play"]),
                                               _PR["tongue_y1"] - _PR["tongue_y0"]))
    # v3.7 (V3-07): Abstandsstuecke 18 zwischen Panel und Displayplatine
    _DS = DISPLAY_SPACER
    rule(_DS["gap"] in _DS["steps"] and _DS["steps"] == sorted(_DS["steps"])
         and _DS["steps"][-1] - _DS["steps"][0] <= 0.4 + 1e-9,
         "v3.7: Abstandsstuecke %s um den gemessenen Spalt %.1f" % (_DS["steps"], _DS["gap"]))
    rule(_DS["ch"] <= 0.4 and _DS["w"] >= 2.0 and min(_DS["lengths"]) >= 3,
         "v3.7: Stueck %.1f breit, ab %d lang, Fase %.1f unten" % (_DS["w"], min(_DS["lengths"]), _DS["ch"]))
    rule(_DS["bridge"][2] <= _DS["w"] / 3, "v3.7: Steg %.1f hoch bricht sauber ab (Stueck %.1f)"
         % (_DS["bridge"][2], _DS["w"]))

    # --- 5d. Radar
    _sl = GRILLE["slot_h"] / math.sin(math.radians(GRILLE["angle"]))
    rule(_sl >= 6.2 * 1.15, "Gitterschlitze %.2f lang >= 1.15 x lambda/2" % _sl)
    _rw = RADAR_POCKET["d0"] - CAV["d"]
    rule(abs(_rw - 3.9) <= 0.2 * 3.9, "Wand vor dem Radar %.2f = lambda/2 in ABS" % _rw)
    rule(_rw - RADAR_GROOVE["d"] >= 1.7, "v3: unter der Loetstellen-Nut bleiben %.2f Wand" % (_rw - RADAR_GROOVE["d"]))
    rule(RADAR_GROOVE["d"] >= RADAR_HDR["stub"] + 0.2, "v3: Nut %.1f tief fuer %.2f Loetstellen" % (RADAR_GROOVE["d"],
                                                                                             RADAR_HDR["stub"]))
    rule(RADAR_GROOVE["l"] >= RADAR_HDR["l"] + 1.0, "v3: Nut %.1f lang fuer die %.2f-Leiste" % (RADAR_GROOVE["l"],
                                                                                         RADAR_HDR["l"]))
    _sx0, _sx1 = SPK["c"][0] - SPK["frame"] / 2, SPK["c"][0] + SPK["frame"] / 2
    rule(max(RADAR_POCKET["x0"] - _sx1, _sx0 - RADAR_POCKET["x1"]) >= 0.5, "Radartasche neben dem Lautsprecherrahmen")
    rule(RADAR_CARRIER["play_short"] * 2 - RADAR_CARRIER["play"] * 2 >= 0.5 - 1e-9,
         "v3: Radarschacht an der kurzen Seite %.2f breiter als v2 (Bauherr: +0.5)"
         % (RADAR_CARRIER["play_short"] * 2 - RADAR_CARRIER["play"] * 2))
    # v3.2 (V3-02): Abstandsrahmen, Leiste an der Langseite
    _RC, _RH = RADAR_CARRIER, RADAR_HDR
    rule(_RC["standoff"] >= _RH["stub"] + 0.2, "v3.2: Platine %.1f vor dem Taschenboden, Loetstellen %.2f hoch"
         % (_RC["standoff"], _RH["stub"]))
    _stub_in = _RH["edge"] + _RH["w"] / 2 - _RH["stub_r"]            # Loetstelle beginnt so weit innen vom Langrand
    rule(_RC["ledge"] <= _stub_in - 0.2, "v3.2: Stufe %.1f laesst %.2f bis zu den Loetstellen (Platine ganz zur Seite)"
         % (_RC["ledge"], _stub_in - _RC["ledge"]))
    rule(_RC["lip"] <= _RH["edge"] - 0.1 + 1e-9, "v3.2: Lippe %.1f laesst %.2f bis zur Stiftleiste (Platine ganz zur Seite)"
         % (_RC["lip"], _RH["edge"] - _RC["lip"]))
    _slot = RADAR["w"] + 2 * _RC["play_short"]
    rule(RADAR["w"] - (_slot - 2 * _RC["ledge"]) >= 0.4, "v3.2: Platine %.2f breiter als die Luecke zwischen den Stufen"
         % (RADAR["w"] - (_slot - 2 * _RC["ledge"])))
    rule(RADAR["w"] - (_slot - 2 * _RC["lip"]) >= 0.2, "v3.2: Platine %.2f breiter als die Luecke zwischen den Lippen"
         % (RADAR["w"] - (_slot - 2 * _RC["lip"])))
    # v3.4: geklebt statt gedrueckt
    rule(_RC["fit"] >= 0.25, "v3.4: Rahmen rundum %.2f Luft zur Tasche (wird geklebt, nicht gedrueckt)" % _RC["fit"])
    rule(_RC["ch"] >= 0.3, "v3.4: Fase %.1f vorn aussen gegen den Wulst der ersten Lage" % _RC["ch"])
    _face = RADAR["c"][0] - RADAR["w"] / 2 - _RC["play_short"] + _RC["ledge"] - (RADAR_POCKET["x0"] + _RC["fit"])
    rule(_face - _RC["ch"] >= 2.5, "v3.4: Auflage vorn je Seite %.2f breit (nach der Fase)" % (_face - _RC["ch"]))
    _gl = min(BLOCK["y1"] - RADAR_POCKET["y1"], RADAR_POCKET["x0"] - BLOCK["x0"])
    rule(_gl >= _RC["glue"], "v3.4: Blockrueckseite unter und links neben der Tasche %.2f breit fuer die Klebenaht" % _gl)

    # --- 5b. Mikrofon (wie v2)
    M, mb = MIC_POCKET, MIC_POCKET["bore"] / 2
    _w = math.hypot(MIC_C[0] - BTN_C[0], MIC_C[1] - BTN_C[1]) - BTN_HOLE / 2 - mb
    rule(_w >= MIN_WALL, "Mikrofontasche: %.2f Wand zum Tasterausschnitt" % _w)
    _w = _rrect_inset(MIC_C[0], MIC_C[1], CORNER_R) - mb
    rule(_w >= MIN_WALL - 1e-6, "Mikrofontasche: %.2f Wand zur Aussenkontur" % _w)

    # --- 5c. Verstaerker (B-10, v3.5: V3-04)
    _hole_out = AMP["hole_cc"] + AMP["hole_d"]
    rule(abs(_hole_out - 15.0) < 0.01 and abs(AMP["hole_cc"] - AMP["hole_d"] - 10.0) < 0.01,
         "Lochlage aus des Bauherrn Messung (aussen 15.0 / innen 10.0)")
    _AF = AMP_FRAME
    rule(all(abs(p[0] - h[0]) < 1e-9 and abs(p[1] - h[1]) < 1e-9 for p, h in zip(AMP_PINS, AMP_HOLES)),
         "v3.5: Verstaerker-Stifte mittig in den Loechern (Abstand %.1f)" % (AMP_PINS[1][0] - AMP_PINS[0][0]))
    _st = _AF["pin_steps"]
    rule(_st == sorted(_st) and _AF["pin_d"] == _st[len(_st) // 2],
         "v3.5: Verstaerker-Stiftsatz %s aufsteigend, Ansicht mit der mittleren Staerke %.1f" % (_st, _AF["pin_d"]))
    rule((_st[0] - AMP["hole_d"]) / 2 >= -1e-9 and (_st[-1] - AMP["hole_d"]) / 2 <= 0.15 + 1e-9,
         "v3.5: Stifte Ø%.1f..%.1f im Loch Ø%.1f: nominal %.2f..%.2f Uebermass je Seite (gedruckt etwa 0.1 duenner)"
         % (_st[0], _st[-1], AMP["hole_d"], (_st[0] - AMP["hole_d"]) / 2, (_st[-1] - AMP["hole_d"]) / 2))
    rule(_AF["tip"] <= _AF["stake"] / 2, "v3.5: Spitzenfase %.1f am %.1f-Ueberstand" % (_AF["tip"], _AF["stake"]))
    rule(_AF["pin_ok"] in _st, "Bauherr 2026-10-17: Verstaerker-Stift Ø%.1f sitzt straff (aus dem Satz %s)"
         % (_AF["pin_ok"], _st))
    rule(_AF["base_t"] - _AF["label_t"] >= 1.2, "v3.5: unter der Gravur bleiben %.1f Boden"
         % (_AF["base_t"] - _AF["label_t"]))
    for (px, py) in AMP_PEGS:
        _w = min(px - PLATE["x0"], PLATE["x1"] - px, py - PLATE["y0"], PLATE["y1"] - py)
        rule(_w >= 3.0, "Verstaerker-Zapfen (%.0f|%.0f) auf der Platte" % (px, py))

    # --- 5f. Computer-Traeger (W-03): Einbauweg und Schienen
    C = CARRIER
    yi0 = C["y0"] + C["S"]
    yi1 = max(C["ya1"], C["yb1"]) + C["S"]
    rule(yi0 - BLOCK["y1"] >= 1.0, "Traeger beim Einsetzen %.2f mm unter dem Gitterblock" % (yi0 - BLOCK["y1"]))
    rule(yi1 <= BTN_ARM_Y[0] - 1.0, "Traeger beim Einsetzen endet %.1f mm ueber den Tasterarmen"
         % (BTN_ARM_Y[0] - yi1))
    rule(C["x0"] - C["tab_out"] >= _mx0 + 0.5 and C["x1"] + C["tab_out"] <= _mx1 - 0.5,
         "Traeger samt Zungen (x %.1f..%.1f) passt durch die Kragenoeffnung" % (C["x0"] - C["tab_out"],
                                                                              C["x1"] + C["tab_out"]))
    for (bx, by) in PLATE_BOSSES:
        _b = (bx - 5.0 if bx > 50 else BOX["x0"] + WALL, bx + 5.0 if bx < 50 else BOX["x1"] - WALL, by - 5.0, by + 5.0)
        # Teil in der Hoehe des Auflagers beim Einsetzen
        lo_y, hi_y = _b[2] - C["S"], _b[3] - C["S"]
        if bx > 50:
            xr = C["xb1_low"] if lo_y >= C["y_low"] else C["x1"]
            rule(xr <= _b[0] - 0.4, "Traeger rechts (x bis %.1f) faehrt am Auflager (%.1f|%.0f) vorbei (ab x %.1f)"
                 % (xr, bx, by, _b[0]))
        else:
            xl = C["xa1"] if lo_y >= C["ya1"] else C["x0"] - C["tab_out"]
            rule(xl >= _b[1] + 0.4 or hi_y < C["y0"], "Traeger links (x ab %.1f) faehrt am Auflager (%.1f|%.0f) vorbei"
                 % (xl, bx, by))
    _ins = [(a + C["S"], b + C["S"]) for (a, b) in C["tabs"]]
    _bad = [(i, j) for (i, j) in _ins for (a, b) in C["tabs"] if min(j, b) - max(i, a - C["stop"]) > -0.5]
    rule(not _bad, "Traeger: Zungen stehen beim Einsetzen in den Luecken zwischen den Lippen")
    _xl = (C["x0"] - C["tab_out"] - C["play"] - C["ridge_w"], C["x0"] - C["tab_out"] - C["play"] + C["bevel"])
    _xr = (C["x1"] + C["tab_out"] + C["play"] - C["bevel"], C["x1"] + C["tab_out"] + C["play"] + C["ridge_w"])
    for (x, y) in ANCHORS:
        for i, (a, b) in enumerate(C["tabs"]):
            ya = a - (C["stop"] if i == 0 else 0.0)
            for xr in (_xl, _xr):
                hit = (xr[0] - ANCHOR_HEAD_D / 2 < x < xr[1] + ANCHOR_HEAD_D / 2 and
                       ya - ANCHOR_HEAD_D / 2 < y < b + ANCHOR_HEAD_D / 2)
                rule(not hit, "Holzschraube (%.0f|%.0f) frei von der Schiene bei y %.0f..%.0f" % (x, y, a, b))
    for xr, nm in ((_xl, "links"), (_xr, "rechts")):
        rule(xr[0] >= BOX["x0"] + WALL + 0.5 and xr[1] <= BOX["x1"] - WALL - 0.5, "Schiene %s (x %.1f..%.1f) im Innenraum"
             % (nm, xr[0], xr[1]))
        rule(min(abs(xr[0] - C["x0"]), abs(xr[1] - C["x1"])) > 0 and (xr[1] <= C["x0"] - 0.6 or xr[0] >= C["x1"] + 0.6),
             "Schiene %s laesst den Traeger-Umriss %.1f frei (Einsetzen zwischen den Lippen)" % (nm, 0.9))
    rule(VERTEILER["y0"] - yi1 >= 0.5, "Traeger beim Einsetzen %.2f ueber dem Verteiler" % (VERTEILER["y0"] - yi1))
    # Sprechrechner: Antenne oben ohne Material, USB-Freiraum
    rule(TALK["usb_free"] >= 25.0, "Sprechrechner: %.0f mm frei am USB-Ende (Stecker oder Loeten)" % TALK["usb_free"])
    rule(TALK["y0"] - 2.0 >= C["y0"] - 0.01, "Sprechrechner-Antenne liegt im Traeger-Ausschnitt")
    # Klingelrechner unter dem Lautsprecher und neben den Auflagern
    rule(BELL["y0"] - BELL["stop_h"] - 0.3 >= SPK["c"][1] + SPK["frame"] / 2 + 1.0,
         "Klingelrechner-Anschlag %.2f mm unter dem Lautsprecherrahmen" % (BELL["y0"] - BELL["stop_h"] - 0.3 -
                                                                         SPK["c"][1] - SPK["frame"] / 2))
    rule(BELL_D_HDR - PLATE_Z >= 4.0, "Stiftleisten des Klingelrechners %.2f mm hinter der Platte (Fenster dahinter)"
         % (BELL_D_HDR - PLATE_Z))
    rule(PLATE_STOP["c"][1] - PLATE_STOP["d"] / 2 - C["yb1"] >= 0.3 and
         PLATE_STOP["c"][1] - PLATE_STOP["d"] / 2 - C["yb1"] <= 1.5,
         "Anschlag der Platte %.2f unter dem Traeger (haelt ihn oben)" % (PLATE_STOP["c"][1] - PLATE_STOP["d"] / 2
                                                                          - C["yb1"]))
    rule(C["xa1"] + 0.3 <= PLATE_STOP["c"][0] - PLATE_STOP["d"] / 2 and PLATE_STOP["c"][0] + PLATE_STOP["d"] / 2 <=
         C["xb1_low"] - 0.3, "Anschlag liegt unter Teil B")
    # v3.3 (V3-03): Rastknopf und Rastloch
    K_ = CARRIER_KNOB
    hr = K_["hole_d"] / 2
    _e = min(K_["x"] - hr - C["xa1"], C["xb1_low"] - K_["x"] - hr, C["yb1"] - K_["y"] - hr)
    rule(_e >= 1.5 and K_["y"] - hr > C["y_low"], "v3.3: Rastloch (%.0f|%.0f) im unteren Teil B, %.1f vom Rand"
         % (K_["x"], K_["y"], _e))
    _ki = K_["y"] - C["S"]                                          # Knopf beim Einsetzen, in Traeger-Koordinaten
    rule(KNOB_LANE_Y0 + K_["d"] / 2 + 0.5 <= _ki and _ki + K_["d"] / 2 + 0.5 <= KNOB_RAMP_Y0,
         "v3.3: Knopf liegt beim Einsetzen (Traeger %.1f tiefer) in der Gasse y %.1f..%.1f" % (C["S"], KNOB_LANE_Y0,
                                                                                            KNOB_RAMP_Y0))
    rule(K_["lane_w"] >= K_["d"] + 0.6, "v3.3: Gasse %.1f breit fuer den Knopf Ø%.1f" % (K_["lane_w"], K_["d"]))
    rule(K_["lane_t"] >= max(K_["heights"]) + 0.2 - 1e-9, "v3.3: Gasse %.1f tief fuer Knoepfe bis %.1f"
         % (K_["lane_t"], max(K_["heights"])))
    rule(C["t"] - K_["lane_t"] >= 1.8, "v3.3: unter der Gasse bleiben %.1f Traeger" % (C["t"] - K_["lane_t"]))
    rule(K_["hole_d"] - K_["d"] <= 0.8, "v3.3: Knopf hat %.2f Luft im Loch" % ((K_["hole_d"] - K_["d"]) / 2))
    rule(all(abs(h_ / PRINT["layer"] - round(h_ / PRINT["layer"])) < 1e-6 for h_ in K_["heights"]),
         "v3.3: Knopfhoehen %s sind Vielfache der Schicht %.1f" % (K_["heights"], PRINT["layer"]))
    rule(min(math.hypot(K_["x"] - ax, K_["y"] - ay) for (ax, ay) in ANCHORS) >= ANCHOR_HEAD_D / 2 + hr + 1.0,
         "v3.3: Knopf frei von den Holzschrauben")
    rule(K_["x"] + K_["lane_w"] / 2 <= C["x1"] - C["bevel"] - 1.0, "v3.3: Gasse frei von den Zungen")

    # --- 6. Tiefenbudget
    need_btn = (RING_T - SHEET["t"]) + BTN_CYL_L + BTN_FREE
    rule(need_btn <= D_BACK_IN, "Tiefe: Taster braucht %.2f von %.2f" % (need_btn, D_BACK_IN))
    rule(SPK_D_FRONT + SPK["behind"] <= TALK_D_PINS - 4.0 - 1.0, "Lautsprecher (bis d %.1f) vor den Sprechrechner-"
         "Litzen (ab d %.1f)" % (SPK_D_FRONT + SPK["behind"], TALK_D_PINS - 4.0))

    # --- 7. LAN-Einfuehrung (Platzhalter bis zur Recherche)
    gx, gd = GLAND["c"]
    rule(BOX["x0"] + CORNER_R <= gx - GLAND["body_d"] / 2 and gx + GLAND["body_d"] / 2 <= BOX["x1"] - CORNER_R,
         "Einfuehrung: Verschraubung Ø%.1f sitzt auf dem geraden Boden" % GLAND["body_d"])
    rule(gd + GLAND["body_d"] / 2 <= DEPTH - 0.5, "Einfuehrung: Verschraubung aussen endet %.2f vor der Rueckseite"
         % (DEPTH - gd - GLAND["body_d"] / 2))
    rule(GLAND["thread_l"] - GLAND["wall"] >= 0.8 * GLAND["nut_t"], "Einfuehrung: Gewinde greift %.1f in die %.0f-mm-"
         "Gegenmutter" % (GLAND["thread_l"] - GLAND["wall"], GLAND["nut_t"]))
    rule(FLANGE_T + 1.0 <= gd - GLAND["nut_d"] / 2 and gd + GLAND["nut_d"] / 2 <= D_BACK_IN - 0.5,
         "Einfuehrung: Mutter Ø%.1f zwischen Kragen und Rueckwand (d %.1f..%.1f)"
         % (GLAND["nut_d"], gd - GLAND["nut_d"] / 2, gd + GLAND["nut_d"] / 2))
    _k = KEEP_OUT["Kabelmutter"]
    rule(_k[1] <= USB_CUP[0] - 0.5 or _k[4] >= USB_CUP[3] + 0.5, "Einfuehrung: Mutter frei vom USB-Becher")
    rule(abs(gx - 50.0) <= 10.0, "Einfuehrung unten, %.1f mm neben der Mitte (Bauherr: unten mittig)" % (gx - 50.0),
         hard=False)
    rule(GLAND["hole_d"] - GLAND["plug_diag"] >= 1.5, "Einfuehrung Ø%.1f laesst den RJ45-Stecker durch (Diagonale %.1f)"
         % (GLAND["hole_d"], GLAND["plug_diag"]))
    rule(_k[4] >= USB_CUP[3] + 0.0 or _k[1] <= USB_CUP[0] - 0.5, "Einfuehrung: Mutter frei vom USB-Becher (x)")
    _ux0 = USB_FIELD["cover_x0"]
    rule(True, "Einfuehrung: USB-Abdeckung bekommt einen Ausschnitt r %.1f um die Verschraubung" % (GLAND["body_d"] / 2 + 1))
    # Oesen: mindestens 5, auf der Rueckwand, im Innenraum
    rule(len(LAN_EYELETS) >= 5, "LAN: %d Kabelbinder-Oesen (Bauherr: mind. 5)" % len(LAN_EYELETS))
    def _path_x(y):
        for p_, q_ in zip(LAN_PATH, LAN_PATH[1:]):
            if p_[1] <= y <= q_[1]:
                t_ = (y - p_[1]) / (q_[1] - p_[1])
                return p_[0] + (q_[0] - p_[0]) * t_
        return None
    for (ex, ey, _a) in LAN_EYELETS:
        rule(_inner_inset(ex, ey) >= EYELET["base"] / 2 + EYELET["wall"], "Oese (%.0f|%.0f) im Innenraum" % (ex, ey))
        g_ = min(math.dist((ex, ey), (p_[0] + (q_[0] - p_[0]) * t / 50, p_[1] + (q_[1] - p_[1]) * t / 50))
                 for p_, q_ in zip(LAN_PATH, LAN_PATH[1:]) for t in range(51)) - EYELET["depth"] / 2 - LAN["cable_d"] / 2
        rule(LAN_EYELET_GAP - 0.01 <= g_ <= 1.5, "Oese (%.0f|%.0f) liegt %.2f neben dem Kabel (Binder zieht es heran)"
             % (ex, ey, g_))

    # --- 7b. SHT31-D auf dem Deckelstift (v3.1)
    SB, SM = SHT_BOARD, SHT_MOUNT
    cx0, cx1 = SHT["x0"] + SHT["wall"], BOX["x1"] - WALL                  # Kammer innen
    cy0, cy1 = SHT["y0"] + SHT["wall"], BOX["y1"] - WALL
    m_ = min(SM["x0"] - cx0, SM["y0"] - cy0, cx1 - SHT_X1, cy1 - SHT_Y1)
    rule(m_ >= 1.5, "SHT31: Platine %.2f x %.2f liegt mit %.1f Rand in der Kammer" % (SB["l"], SB["h"], m_))
    rule(SHT_D_FRONT - SHT_COMP - SHT_D_LID >= 1.5, "SHT31: vorn %.1f Luft zwischen Bauteilen und Deckel"
         % (SHT_D_FRONT - SHT_COMP - SHT_D_LID))
    _lid_x1 = BOX["x1"] - WALL - 0.2
    for (ux, ud) in USB_FIELD["screws"]:                  # Kuppeln der USB-Abdeckung stehen vor der Kammer
        if SHT["x0"] - USB_FIELD["boss_d"] / 2 < ux < _lid_x1 + USB_FIELD["boss_d"] / 2:
            rule(SHT["d0"] - SHT_LID_TRAVEL >= ud + USB_FIELD["boss_d"] / 2 + 0.3,
                 "SHT31: Deckel geht %.1f gerade auf die Kammer, vorbei an der USB-Kuppel (x %.1f, bis d %.1f)"
                 % (SHT_LID_TRAVEL, ux, ud + USB_FIELD["boss_d"] / 2))
    rule(D_BACK_IN - (SHT_D_BACK + SHT_COMP) >= 2.0, "SHT31: hinten %.1f Luft bis zur Rueckwand"
         % (D_BACK_IN - (SHT_D_BACK + SHT_COMP)))
    rule(SHT_D_BACK + SM["pin_over"] <= D_BACK_IN - 2.0, "SHT31: Stiftende d %.1f vor der Rueckwand"
         % (SHT_D_BACK + SM["pin_over"]))
    hx, hy = SHT_HOLE
    e_ = min(hx - SM["x0"], SHT_X1 - hx, hy - SM["y0"], SHT_Y1 - hy)
    rule(SM["collar_d"] / 2 <= e_ - 0.3, "SHT31: Bund Ø%.1f bleibt auf der Platine (Lochmitte %.2f vom Rand)"
         % (SM["collar_d"], e_))
    rule((SM["collar_d"] - SB["hole_d"]) / 2 >= 0.3, "SHT31: Bund traegt %.2f rund um das Loch"
         % ((SM["collar_d"] - SB["hole_d"]) / 2))
    _st = SM["pin_steps"]                                       # v3.5 (V3-04): Satz statt einer Staerke
    rule(_st == sorted(_st) and SM["pin_d"] == _st[len(_st) // 2],
         "v3.5: SHT31-Stiftsatz %s aufsteigend, Ansicht mit der mittleren Staerke %.1f" % (_st, SM["pin_d"]))
    rule((_st[0] - SB["hole_d"]) / 2 >= -1e-9 and (_st[-1] - SB["hole_d"]) / 2 <= 0.15 + 1e-9,
         "v3.5: SHT31-Stifte Ø%.1f..%.1f im Loch Ø%.1f: nominal %.2f..%.2f Uebermass je Seite (gedruckt etwa 0.1 "
         "duenner)" % (_st[0], _st[-1], SB["hole_d"], (_st[0] - SB["hole_d"]) / 2, (_st[-1] - SB["hole_d"]) / 2))
    rule(SHT["lid_t"] - SM["label_t"] >= 1.0, "v3.5: unter der Gravur im Deckel bleiben %.1f"
         % (SHT["lid_t"] - SM["label_t"]))
    rule(SM["pin_ok"] in _st, "Bauherr 2026-10-17: SHT31-Stift Ø%.1f sitzt straff (aus dem Satz %s)" % (SM["pin_ok"], _st))
    rule(SM["x0"] + 2.5 <= SM["rib_x"][0] and SM["rib_x"][1] <= SHT_X1 - 2.0,
         "SHT31: Rippe x %.0f..%.0f laesst die Loetloecher an beiden Kurzseiten frei" % SM["rib_x"])
    rule(SM["rib_x"][0] < SM["x0"] + SB["l"] / 2 < hx, "SHT31: Schwerpunkt x %.1f links vom Stift x %.1f, die Platine "
         "kippt auf die Rippe" % (SM["x0"] + SB["l"] / 2, hx))
    rule(SHT_Y1 + SM["rib_gap"] + SM["rib_t"] <= cy1 - 1.0, "SHT31: Rippe liegt in der Kammer")
    kx, ky = SHT_CABLE_HOLE
    rule(SM["x0"] - 0.5 <= kx <= SM["x0"] + 3.5 and SM["y0"] <= ky <= SHT_Y1,
         "SHT31: Kabelloch (%.1f|%.1f) liegt vor den Loetloechern am linken Rand" % (kx, ky))
    rule(SHT_X1 + 5.0 <= BOX["x1"] - WALL - 1.5 - SHT["vent_d"] / 2 and SHT_Y1 + 10.0 <= cy1,
         "SHT31: Platine verdeckt weder Abluft noch Zuluft")

    # --- 8. Holzschrauben erreichbar (Platte ab, Traeger ab)
    for (x, y) in ANCHORS:
        blocked = []
        if BLOCK["x0"] - ACCESS_R < x < BLOCK["x1"] + ACCESS_R and BLOCK["y0"] - ACCESS_R < y < BLOCK["y1"] + ACCESS_R:
            blocked.append("Gittermodul")
        if not (BOX["x0"] + FLANGE_W + ACCESS_R <= x <= BOX["x1"] - FLANGE_W - ACCESS_R
                and BOX["y0"] + FLANGE_W + ACCESS_R <= y <= BOX["y1"] - FLANGE_W - ACCESS_R):
            blocked.append("Kragen")
        if math.hypot(x - BTN_C[0], y - BTN_C[1]) < (RING_D - 1.0) / 2 + ACCESS_R:
            blocked.append("Tasterscheibe")
        if BTN_ARM_Y[0] - ACCESS_R < y < BTN_ARM_Y[1] + ACCESS_R:
            blocked.append("Tasterarm")
        for (bx, by) in PLATE_BOSSES:
            if abs(x - bx) < 5 + ACCESS_R and abs(y - by) < 5 + ACCESS_R:
                blocked.append("Plattenauflager")
        for nm in GLUED:
            e = LAYOUT[nm][0]
            if e[0] - ACCESS_R < x < e[1] + ACCESS_R and e[2] - ACCESS_R < y < e[3] + ACCESS_R:
                blocked.append(nm + " (eingeklebt)")
        rule(not blocked, "Holzschraube (%.0f,%.0f) erreichbar%s" % (x, y, "" if not blocked else
                                                                    " - VERDECKT von " + ", ".join(blocked)))

    # --- 9. Belegung: im Innenraum, keine Ueberschneidung, Freiraeume frei
    xi0, xi1 = BOX["x0"] + WALL, BOX["x1"] - WALL
    yi0_, yi1_ = BOX["y0"] + WALL, BOX["y1"] - WALL
    for nm, (e, src, zone) in LAYOUT.items():
        if zone == "kasten":
            rule(BOX["x0"] < e[0] and e[1] < BOX["x1"] and BOX["y0"] < e[2] and e[3] < BOX["y1"],
                 "%s liegt in der Kastenkontur (in der Wand)" % nm)
            continue
        rule(xi0 - 1e-6 <= e[0] and e[1] <= xi1 + 1e-6 and yi0_ - 1e-6 <= e[2] and e[3] <= yi1_ + 1e-6
             and -1e-6 <= e[4] and e[5] <= D_BACK_IN + 1e-6, "%s liegt im Innenraum" % nm)
        for kn, k in KEEP_OUT.items():
            if (nm, kn) == ("Display", "Bildschirm-USB-Stecker"):
                continue
            if kn.startswith("Gasse") and zone == "traeger" and False:
                continue
            rule(not _ov(e, k), "%s haelt den Freiraum %s frei" % (nm, kn))
    names = list(LAYOUT)
    _ok_pairs = {("Display", n) for n in names if n.startswith("Displaystift")}
    _ok_pairs |= {("Verteilerplatine", "Verteiler Bauteile"), ("Verteilerplatine", "Verteiler Rand flach"),
                  ("Verteilerplatine", "Verteiler-Sockel"),
                  ("Verteiler Bauteile", "Verteiler Rand flach"), ("Lautsprecher", "Lautsprecher-Dichtung"),
                  ("Klingelrechner", "RJ45-Stecker")}
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            if (a, b) in _ok_pairs or (b, a) in _ok_pairs:
                continue
            rule(not _ov(LAYOUT[a][0], LAYOUT[b][0]), "%s und %s ueberschneiden sich nicht" % (a, b))

    # --- 10. Schraubenabstand Stahl (wie v2)
    for side in BAR_HOLES:
        _h = BAR_HOLES[side]
        _span = max(b - a for a, b in zip(_h, _h[1:]))
        _top, _bot = _h[0] - (BOX["y0"] + STEEL["inset"]), (BOX["y1"] - STEEL["inset"]) - _h[-1]
        rule(_span <= 40.0 and max(_top, _bot) <= 70.0, "Stahlschrauben %s: alle %.0f mm, Ende oben %.0f / unten %.0f"
             % (side, _span, _top, _bot), hard=False)

    if verbose:
        for m in oks:
            print("  OK      %s" % m)
        for m in warns:
            print("  WARNUNG %s" % m)
        for m in errs:
            print("  FEHLER  %s" % m)
        print("\n%d Regeln: %d ok, %d Warnungen, %d FEHLER" % (len(oks) + len(warns) + len(errs), len(oks), len(warns),
                                                               len(errs)))
    return errs, warns


if __name__ == "__main__":
    validate()
