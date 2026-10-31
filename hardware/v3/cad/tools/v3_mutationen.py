"""Mutationstests v3: Jede neue Pruefung muss anschlagen, wenn man das Teil absichtlich falsch baut.
    "C:/Program Files/FreeCAD 1.1/bin/freecadcmd.exe" hardware/v3/cad/tools/v3_mutationen.py
Baut in einen Temp-Ordner (die echten BREPs bleiben unberuehrt) und schreibt das Ergebnis nach tools/_mutationen.log.
"""
import os as _os
# Paths (public copy): everything relative to this folder, outputs into out/ (gitignored).
V3_DIR = globals().get("V3_DIR") or _os.environ.get("KLINGELBOX_V3_DIR") or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
_os.environ.setdefault("KLINGELBOX_V3_DIR", V3_DIR)
for _d in ("out", _os.path.join("out", "print", "metall")):
    _os.makedirs(_os.path.join(V3_DIR, _d), exist_ok=True)
import contextlib
import io
import os
import tempfile

LOG = _os.path.join(V3_DIR, "out", "_mutationen.log")
exec(open(_os.path.join(V3_DIR, "v3_teile.py"), encoding="utf-8").read())
TMP = tempfile.mkdtemp(prefix="v3mut_")
REAL_BOX, REAL_PLATE = BREP_BOX, BREP_PLATE
out = []


def run(name, patch, unpatch, checker, needle):
    """patch() aendert etwas, checker() laeuft, needle muss in einer FEHLER-Zeile (<<<) stehen."""
    global BREP_BOX, BREP_PLATE
    BREP_BOX, BREP_PLATE = os.path.join(TMP, "box.brep"), os.path.join(TMP, "plate.brep")
    patch()
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            build_box()
            build_plate()
            checker()
    finally:
        unpatch()
        BREP_BOX, BREP_PLATE = REAL_BOX, REAL_PLATE
    hit = [ln for ln in buf.getvalue().splitlines() if "<<<" in ln and needle in ln]
    out.append("%-55s %s" % (name, ("SCHLAEGT AN: " + hit[0].strip()[:90]) if hit else "NICHT ERKANNT <<<"))


def setp(key, sub, val):
    old = P.__dict__[key][sub] if sub is not None else P.__dict__[key]
    def patch():
        if sub is None:
            P.__dict__[key] = val
        else:
            P.__dict__[key][sub] = val
    def unpatch():
        if sub is None:
            P.__dict__[key] = old
        else:
            P.__dict__[key][sub] = old
    return patch, unpatch


# 1 Druckpause: Kanal zu flach -> Leiste stuende ueber dem Rinnenrand (Kragen wuerde auf ihr gedruckt, Leiste klemmt)
_o = (P.BAR["play_d"],)
run("Druckpause: Kanal 0.4 zu flach", *setp("BAR", "play_d", -0.2), check_cad, "Druckpause")
# 2 O-Ring-Nut fehlt
_sm = steel_mounts
def _no_groove():
    globals()["steel_mounts"] = lambda: _sm(oring=False)
def _groove_back():
    globals()["steel_mounts"] = _sm
run("O-Ring-Nut fehlt", _no_groove, _groove_back, check_cad, "O-Ring-Nut")
# 3 v3.2: Radar-Rahmen ohne Stufe vorn -> die Platine faellt zur Antennenseite heraus (wie in v3)
run("Radar-Rahmen ohne Stufe", *setp("RADAR_CARRIER", "ledge", 0.0), check_teile, "gefangen")
# 3b v3.2: Loetstellen hoeher als der Abstand -> sie stehen auf dem Taschenboden
run("Radar-Loetstellen 2.2 hoch", *setp("RADAR_HDR", "stub", 2.2), check_teile, "frei vom Kasten")
# 3e v3.4: Rahmen ohne Luft zur Tasche -> er klemmt wieder (wie mit den Quetschrippen aus v3.2)
run("Radar-Rahmen ohne Luft zur Tasche", *setp("RADAR_CARRIER", "fit", 0.0), check_teile, "ohne Kraft")
# 3c v3.3: Gasse zu kurz -> der Rastknopf liegt beim Einsetzen unter dem Traeger und hebt ihn an
run("Traeger-Gasse 8 mm zu kurz", *setp("CARRIER_KNOB", "lane_over", -6.0), check_teile, "Gasse frei")
# 3d v3.3: Rastloch kleiner als der Knopf -> der Traeger steht in der Endlage auf dem Knopf
run("Rastloch 2.8 statt 3.6", *setp("CARRIER_KNOB", "hole_d", 2.8), check_teile, "frei im Loch")
# 4 Anschlag der Platte 3 mm zu tief -> Traeger kann herunterrutschen
_c = P.PLATE_STOP["c"]
run("Plattenanschlag 3 mm tiefer", *setp("PLATE_STOP", "c", (_c[0], _c[1] + 3.0)), check_teile, "Anschlag der Platte")
# 5 Haken des Klemmrings 1 mm weiter hinten -> Platte nicht gehalten
run("Klemmring-Haken 1.5 mm Spiel", *setp("SPK_CLAMP", "play", 1.5), check_teile, "Haken halten")
# 6 Traeger 1 mm weniger Hub -> Zungen stossen beim Einsetzen auf die Lippen
run("Traeger-Hub 30 statt 39.6", *setp("CARRIER", "S", 30.0), check_teile, "Weg")
# 7 Verteiler-Rastfinger ohne Haken
run("Verteiler-Rastfinger ohne Haken", *setp("VERT_SOCKET", "latch_hook", -0.6), check_teile, "Rastfinger")
# 8 v3.5 (V3-04): SHT31-Stifte wieder zu duenn (wie v3.1 bis v3.4) -> die Platine hat Spiel
run("SHT31-Stifte 2,7/2,8/2,9 statt 3,0/3,1/3,2", *setp("SHT_MOUNT", "pin_steps", [2.7, 2.8, 2.9]), check_teile,
    "Stift mittig, Platine ohne Spiel")
# 8b v3.5 (V3-04): Verstaerker-Stifte zu duenn (wie v3 bis v3.4) -> die Platine hat Spiel
run("Verstaerker-Stifte 2,1/2,2/2,3", *setp("AMP_FRAME", "pin_steps", [2.1, 2.2, 2.3]), check_teile,
    "Stifte mittig, Platine ohne Spiel")
# 8c v3.5: Verstaerker-Stifte 0,3 nach aussen versetzt (das Prinzip bis v3.4) -> nicht mittig
_ap = P.AMP_PINS
run("Verstaerker-Stifte 0,3 nach aussen", *setp("AMP_PINS", None, [(_ap[0][0] - 0.3, _ap[0][1]),
                                                                   (_ap[1][0] + 0.3, _ap[1][1])]), check_teile,
    "Stifte mittig")
# 8d v3.6 (V3-05): Plattenstuetze mit 0,6 Luft -> die Platte biegt wieder durch, bevor sie aufliegt
run("Plattenstuetze 0,6 hinter der Platte", *setp("PLATE_REST", "play", 0.6), check_teile, "Platte liegt hinten auf")
# 8e v3.6: Zunge der Stuetze bis x 21 -> sie steht dem Computer-Traeger beim Einsetzen im Weg
run("Plattenstuetze bis x 21 (Traegerbahn)", *setp("PLATE_REST", "x_in", 21.0), check_teile, "Weg")
# 8f v3.7 (V3-07): Abstandsstuecke an der falschen Dicke -> der gemessene Spalt 2,7 liegt nicht im Satz
run("Abstandsstuecke 2,9/3,0/3,1", *setp("DISPLAY_SPACER", "steps", [2.9, 3.0, 3.1]), check_teile, "Spalt")
# 9 v3.1: Rippe zu weit unter der Platine -> sie haelt nicht gegen Verdrehen
run("SHT31-Rippe 1.2 unter der Platine", *setp("SHT_MOUNT", "rib_gap", 1.2), check_teile, "Rippe haelt")

open(LOG, "w", encoding="utf-8").write("\n".join(out) + "\n")
print("\n".join(out))
