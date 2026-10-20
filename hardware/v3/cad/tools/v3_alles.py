"""Intercom v3 komplett bauen, pruefen und exportieren - in dieser Reihenfolge, Abbruch beim ersten Fehler.
    "C:/Program Files/FreeCAD 1.1/bin/freecadcmd.exe" hardware/v3/cad/tools/v3_alles.py
Ergebnis: tools/_v3_alles.log (jede Pruefung mit Zahlen), BREPs in cad/v3/, Druckdateien in cad/druck/v3/.
"""
import os as _os
# Paths (public copy): everything relative to this folder, outputs into out/ (gitignored).
V3_DIR = globals().get("V3_DIR") or _os.environ.get("KLINGELBOX_V3_DIR") or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
_os.environ.setdefault("KLINGELBOX_V3_DIR", V3_DIR)
for _d in ("out", _os.path.join("out", "print", "metall")):
    _os.makedirs(_os.path.join(V3_DIR, _d), exist_ok=True)
import contextlib
import io
import sys

ALLES_LOG = _os.path.join(V3_DIR, "out", "_v3_alles.log")   # nicht LOG: v3_export.py (exec) setzt LOG = []
buf = io.StringIO()


class Tee:
    def write(self, s):
        buf.write(s)
        sys.__stdout__.write(s)

    def flush(self):
        sys.__stdout__.flush()


ok = True
with contextlib.redirect_stdout(Tee()):
    sys.path.insert(0, V3_DIR)
    import v3_params as _VP
    errs, warns = _VP.validate(verbose=False)
    print("validate(): %d Fehler, %d Warnungen" % (len(errs), len(warns)))
    for e in errs:
        print("  FEHLER  " + e)
    ok = not errs
    if ok:
        exec(open(_os.path.join(V3_DIR, "v3_teile.py"), encoding="utf-8").read())
        build_box()
        build_plate()
        ok = check_cad() == 0
    if ok:
        ok = check_teile() == 0
    if ok:
        gm = {"__name__": "messing"}
        exec(open(_os.path.join(V3_DIR, "v3_messing.py"), encoding="utf-8").read(), gm)
        gm["build_shape"]()
        ok = gm["check"]() == 0
    if ok:
        gs = {"__name__": "stahl"}
        exec(open(_os.path.join(V3_DIR, "v3_stahl.py"), encoding="utf-8").read(), gs)
        gs["build_steel"]()
        ok = gs["check_steel"]() == 0
    if ok:
        gd = {"__name__": "diffusor"}
        exec(open(_os.path.join(V3_DIR, "v3_diffusor.py"), encoding="utf-8").read(), gd)
        gd["build"]()
        ok = gd["check"]() == 0
    if ok:
        gu = {"__name__": "usb"}
        exec(open(_os.path.join(V3_DIR, "v3_usb.py"), encoding="utf-8").read(), gu)
        ok = gu["check_usb"]() == 0
    if ok:
        br = Part.Shape(); br.importBrep(gm["BREP"])
        st = Part.Shape(); st.importBrep(gs["BREP_STEEL"])
        bx = Part.Shape(); bx.importBrep(BREP_BOX)
        dfs = Part.Shape(); dfs.importBrep(gd["BREP"])
        v = [br.common(st).Volume, br.common(bx).Volume, dfs.common(br).Volume, dfs.common(st).Volume]
        print("Messing/Stahl %.2f | Messing/Kasten %.2f | Diffusor/Messing %.2f | Diffusor/Stahl %.2f mm3" % tuple(v))
        ok = max(v) < 0.01
    if ok:
        exec(open(_os.path.join(V3_DIR, "tools", "v3_export.py"), encoding="utf-8").read())
    print("\nV3 GESAMT: %s" % ("ALLES BESTANDEN, EXPORTIERT" if ok else "ABGEBROCHEN (siehe oben)"))
open(ALLES_LOG, "w", encoding="utf-8").write(buf.getvalue())
