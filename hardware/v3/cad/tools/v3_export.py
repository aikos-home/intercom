"""Druckdateien Intercom v3 -> cad/druck/v3/ (alle Teile in EINEM Ordner, Bauherr: "alles beieinander"), in Drucklage.
    "C:/Program Files/FreeCAD 1.1/bin/freecadcmd.exe" hardware/v3/cad/tools/v3_export.py
Vorher muessen die BREPs aktuell sein (v3_kasten: build_box/build_plate, v3_stahl: build_steel, v3_messing:
build_shape, v3_diffusor: build) und alle Pruefungen bestanden haben. Schreibt auch die Metall-Vorlagen nach metall/.
"""
import os as _os
# Paths (public copy): everything relative to this folder, outputs into out/ (gitignored).
V3_DIR = globals().get("V3_DIR") or _os.environ.get("KLINGELBOX_V3_DIR") or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
_os.environ.setdefault("KLINGELBOX_V3_DIR", V3_DIR)
for _d in ("out", _os.path.join("out", "print", "metall")):
    _os.makedirs(_os.path.join(V3_DIR, _d), exist_ok=True)
import os
import sys

exec(open(_os.path.join(V3_DIR, "v3_teile.py"), encoding="utf-8").read())
import Mesh

DRUCK = _os.path.join(V3_DIR, "out", "print")
os.makedirs(DRUCK, exist_ok=True)
DENS = {"PETG": 1.27e-3, "PLA": 1.24e-3}
LOG = []


def place(s):
    bb = s.BoundBox
    s.translate(V(-bb.XMin, -bb.YMin, -bb.ZMin))
    return s


def rot_x(s, deg):
    s = s.copy()
    s.rotate(V(0, 0, 0), V(1, 0, 0), deg)
    return place(s)


back_down = lambda s: rot_x(s, -90.0)      # groesstes d (Rueckseite) aufs Bett
front_down = lambda s: rot_x(s, 90.0)      # kleinstes d (Vorderseite) aufs Bett


def write(s, name, mat="PETG", dev=0.02):
    Mesh.Mesh(s.tessellate(dev)).write(os.path.join(DRUCK, name))
    bb = s.BoundBox
    line = "%-44s %6.1f x %6.1f x %5.1f mm | %5.1f g %s | Solids %d | valid %s" % (
        name, bb.XLength, bb.YLength, bb.ZLength, s.Volume * DENS[mat], mat, len(s.Solids), s.isValid())
    LOG.append(line)
    print("EXPORT " + line)


box = Part.Shape(); box.importBrep(BREP_BOX)
plate = Part.Shape(); plate.importBrep(BREP_PLATE)
write(back_down(box), "01_kasten.stl", dev=0.03)
write(front_down(plate), "02_display_traegerplatte.stl")
write(back_down(carrier()), "03_computer_traeger.stl")
write(back_down(spk_clamp()), "04_lautsprecher_klemmring.stl")
write(front_down(radar_frame(0)), "05_radar_rahmen.stl")    # v3.2: Stufe aufs Bett, ihre Auflageflaeche oben
write(place(amp_frames_print()), "06_verstaerker_rahmen_3_staerken.stl")    # v3.5: Ø2,5/2,6/2,7, Zahl unten
write(place(dowels_print()), "06b_zapfen_4x_abknipsen.stl")
write(place(knobs_print()), "06c_rastknoepfe_3_hoehen.stl")      # v3.3: Rastknopf fuer den Computer-Traeger (geklebt)
write(back_down(vert_socket()), "07_verteiler_sockel.stl")
write(place(sht_lids_print()), "08_sht31_kammerdeckel_3_staerken.stl")      # v3.5: Ø3,0/3,1/3,2, Zahl aussen
write(place(plate_rests_print()), "17_plattenstuetzen_links_rechts.stl")    # v3.6: Klebeflaeche aufs Bett
write(place(spacers_print()), "18_display_abstandsstuecke_3_staerken.stl")   # v3.7: Kaemme 2,6/2,7/2,8
for _old in ("06_verstaerker_rahmen.stl", "08_sht31_kammerdeckel.stl"):          # bis v3.4 einzeln, nicht liegen lassen
    if os.path.exists(os.path.join(DRUCK, _old)):
        os.remove(os.path.join(DRUCK, _old))
write(place(pins_print()), "09_display_druckstifte_4_laengen.stl")
write(bars_print(), "10_gegenleisten_ersatz_fuer_druckpause.stl")

gu = {"__name__": "usb"}
exec(open(_os.path.join(V3_DIR, "v3_usb.py"), encoding="utf-8").read(), gu)
write(place(gu["usb_insert"]().copy()), "11_usb_einsatz.stl")
write(place(gu["usb_cover"]().copy()), "12_usb_abdeckung.stl")

gs = {"__name__": "stahl"}
exec(open(_os.path.join(V3_DIR, "v3_stahl.py"), encoding="utf-8").read(), gs)
st = Part.Shape(); st.importBrep(gs["BREP_STEEL"])
PETG_HOLE = 4.3      # Zapfenloch im PETG-Ersatz (Stahl 4.1 gelasert; gedruckt +0.1 je Seite), wie v2
(xl, yl), (xr, yr) = P.SPIGOTS
s_ = P.SPIGOT["slot"]
st = st.cut([cyl(xl, yl, -1.0, P.STEEL["t"] + 1.0, PETG_HOLE),
             cyl(xr - s_, yr, -1.0, P.STEEL["t"] + 1.0, PETG_HOLE).fuse(
                 [cyl(xr + s_, yr, -1.0, P.STEEL["t"] + 1.0, PETG_HOLE),
                  rbox(xr - s_, yr - PETG_HOLE / 2, xr + s_, yr + PETG_HOLE / 2, -1.0, P.STEEL["t"] + 1.0)])])
write(back_down(st), "13_stahlblech_ersatz.stl")

gm = {"__name__": "messing"}
exec(open(_os.path.join(V3_DIR, "v3_messing.py"), encoding="utf-8").read(), gm)
unten, oben = gm["split_for_print"]()
write(rot_x(unten, -90.0), "14_messing_ersatz_unten.stl")       # Rueckseite aufs Bett
write(rot_x(oben, 175.0), "15_messing_ersatz_oben.stl")         # Dach aufs Bett

gd = {"__name__": "diffusor"}
exec(open(_os.path.join(V3_DIR, "v3_diffusor.py"), encoding="utf-8").read(), gd)
df = Part.Shape(); df.importBrep(gd["BREP"])
write(rot_x(df, 180.0 - (90.0 - gd["CAP_ANGLE"])), "16_diffusor_weiss.stl", mat="PLA")

# Metall-Vorlagen (NICHT bestellen, Vorbesprechung abwarten)
gs["export_steel"]()
br = Part.Shape(); br.importBrep(gm["BREP"])
br.exportStep(os.path.join(DRUCK, "metall", "messing_v3.step"))
df.exportStep(os.path.join(DRUCK, "metall", "diffusor_v3.step"))
open(os.path.join(DRUCK, "_export.log"), "w", encoding="utf-8").write("\n".join(LOG) + "\n")
print("EXPORT fertig: %s" % DRUCK)
