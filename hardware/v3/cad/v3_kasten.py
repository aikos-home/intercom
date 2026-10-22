"""Intercom v3 - Kasten und Display-Traegerplatte. Geometrie AUSSCHLIESSLICH aus v3_params.py.

    exec(open(r"hardware\\v3\\cad\\v3_kasten.py", encoding="utf-8").read())
    build_box(); build_plate(); check_cad()

Abgeleitet von cad/make_kasten_v3.py (= v2, eingefroren). check_cad() misst am FERTIGEN Koerper nach, nicht an den
Parametern - die zweite Pruefstufe nach P.validate().
"""
import os as _os
# Paths (public copy): everything relative to this folder, outputs into out/ (gitignored).
V3_DIR = globals().get("V3_DIR") or _os.environ.get("KLINGELBOX_V3_DIR") or _os.path.dirname(_os.path.abspath(__file__))
_os.environ.setdefault("KLINGELBOX_V3_DIR", V3_DIR)
for _d in ("out", _os.path.join("out", "print", "metall")):
    _os.makedirs(_os.path.join(V3_DIR, _d), exist_ok=True)
import math
import os
import sys

V3 = V3_DIR
sys.path.insert(0, V3)
import v3_params as P

import FreeCAD as App
import Part
from FreeCAD import Vector as V

OUT = _os.path.join(V3, "out")
BREP_BOX = os.path.join(OUT, "_v3_kasten.brep")
BREP_PLATE = os.path.join(OUT, "_v3_displayplatte.brep")

B, DEPTH, WALL, BACK = P.BOX, P.DEPTH, P.WALL, P.BACK
FW, FT = P.FLANGE_W, P.FLANGE_T
F0 = P.FRAME_T                       # Kastenstirn d 3.0
DB = P.D_BACK_IN                     # Rueckwand innen d 57
pt = lambda x, y, d: V(x, d, -y)


# ------------------------------------------------------------------ Helfer
def rbox(x0, y0, x1, y1, d0, d1, r=0.0):
    s = Part.makeBox(x1 - x0, d1 - d0, y1 - y0, pt(x0, y1, d0))
    if r > 0:
        edges = [e for e in s.Edges
                 if abs(abs((e.Vertexes[1].Point - e.Vertexes[0].Point).normalize().y) - 1.0) < 1e-6]
        s = s.makeFillet(r, edges)
    return s


def cyl(x, y, d0, d1, dia):
    return Part.makeCylinder(dia / 2, d1 - d0, pt(x, y, d0), V(0, 1, 0))


def ycyl(x, d, y0, y1, dia):
    """Zylinder mit Achse in y (senkrecht), von y0 (oben) bis y1 (unten)."""
    return Part.makeCylinder(dia / 2, y1 - y0, pt(x, y1, d), V(0, 0, 1))


def xcyl(x0, x1, y, d, dia):
    return Part.makeCylinder(dia / 2, x1 - x0, pt(x0, y, d), V(1, 0, 0))


def prism_dy(pts, x0, x1):
    """Profil [(d, y)] in der Ebene x = x0, in x bis x1 extrudiert."""
    w = Part.makePolygon([pt(x0, y, d) for (d, y) in pts] + [pt(x0, pts[0][1], pts[0][0])])
    return Part.Face(w).extrude(V(x1 - x0, 0, 0))


def prism_xd(pts, y0, y1):
    """Profil [(x, d)] in der Ebene y = y0, in y bis y1 extrudiert."""
    w = Part.makePolygon([pt(x, y0, d) for (x, d) in pts] + [pt(pts[0][0], y0, pts[0][1])])
    return Part.Face(w).extrude(V(0, 0, -(y1 - y0)))


# ------------------------------------------------------------------ Schale (wie v2)
def box_shell():
    outer = rbox(B["x0"], B["y0"], B["x1"], B["y1"], F0, DEPTH, P.CORNER_R)
    cav = rbox(B["x0"] + WALL, B["y0"] + WALL, B["x1"] - WALL, B["y1"] - WALL, F0 + FT, DB, max(P.CORNER_R - WALL, 0.5))
    mouth = rbox(B["x0"] + FW, B["y0"] + FW, B["x1"] - FW, B["y1"] - FW, F0 - 1.0, F0 + FT + 0.001,
                 max(P.CORNER_R - FW, 0.5))
    return outer.cut([cav, mouth])


def flange_ramps():
    """45-Grad-Rampen unter der Kragennase (wie v2)."""
    xi0, yi0, xi1, yi1 = B["x0"] + WALL, B["y0"] + WALL, B["x1"] - WALL, B["y1"] - WALL
    xf0, yf0, xf1, yf1 = B["x0"] + FW, B["y0"] + FW, B["x1"] - FW, B["y1"] - FW
    r = FW - WALL
    d = F0 + FT
    out = []
    for xi, xf in ((xi0, xf0), (xi1, xf1)):
        w = Part.makePolygon([V(xf, d, -yi0), V(xi, d, -yi0), V(xi, d + r, -yi0), V(xf, d, -yi0)])
        out.append(Part.Face(w).extrude(V(0, 0, -(yi1 - yi0))))
    for yi, yf in ((yi0, yf0), (yi1, yf1)):
        w = Part.makePolygon([pt(xi0, yf, d), pt(xi0, yi, d), pt(xi0, yi, d + r), pt(xi0, yf, d)])
        out.append(Part.Face(w).extrude(V(xi1 - xi0, 0, 0)))
    return out


def flange_passes():
    """v3 (W-06): nur noch die blinden Taschen hinter den zwei Laschenschlitzen des Diffusors und EIN Kabelloch fuer den
    LED-Streifen bei (62|11) durch Kragen und Rampe ins Innere (mit Silikon um das Kabel gedichtet). Die LED-Fenster und
    ihre Taschen sind weg."""
    out = [rbox(a - 1.5, P.LED_SLIT_Y[0] - 1.5, b + 1.5, P.LED_SLIT_Y[1] + 1.5, -1.0, F0 + FT) for (a, b) in P.LED_SLITS]
    lx, ly = P.LED_CABLE["c"]
    out.append(cyl(lx, ly, F0 - 1.0, F0 + FT + (FW - WALL) + 4.0, P.LED_CABLE["collar"]))
    return out


# ------------------------------------------------------------------ Gitterhohlraum, Lautsprecher, Radar
def grille_module():
    """Gitterblock wie v2, aber (v3): keine Einsatzloecher und Sockel fuer den Lautsprecher, kein Ventilloch. Neu: zwei
    Kopftaschen oben im Hohlraum mit Durchgangsloch (Schrauben von vorn in den Klemmring) und die Nuten fuer die
    Loetstellen der Radar-Stiftleiste im Taschenboden."""
    BL, C, S = P.BLOCK, P.CAV, P.SPK
    block = rbox(BL["x0"], BL["y0"], BL["x1"], BL["y1"], F0, C["d"] + P.SPK_WALL)
    slope = (C["y_back"] - C["y_front"]) / (C["d"] - F0)
    prof = [(-1.0, C["y0"]), (C["d"], C["y0"]), (C["d"], C["y_back"]), (-1.0, C["y_front"] - slope * (F0 + 1.0))]
    cuts = [prism_dy(prof, C["x0"], C["x1"])]
    SS = P.SPK_SCREW
    for (x, y) in P.SPK_SCREWS:
        cuts.append(cyl(x, y, -1.0, C["d"], SS["pocket_d"]))                       # Kopftasche, nach vorn offen
        cuts.append(cyl(x, y, C["d"] - 0.5, C["d"] + P.SPK_WALL + 0.5, SS["hole"]))  # Durchgang zum Klemmring
    cuts.append(cyl(S["c"][0], S["c"][1], C["d"] - 0.5, C["d"] + P.SPK_WALL + 0.5, S["port_d"]))
    R = P.RADAR_POCKET
    cuts.append(rbox(R["x0"], R["y0"], R["x1"], R["y1"], R["d0"], C["d"] + P.SPK_WALL + 0.5))
    cuts += radar_grooves()
    return block, cuts


def radar_grooves():
    """Nuten im Radar-Taschenboden unter der Stiftleiste (B-06): Lage 0 Grad (Leiste unten) und 90 Grad (Leiste links)."""
    cx, cy = P.RADAR["c"]
    R, G = P.RADAR_POCKET, P.RADAR_GROOVE
    d1, d0 = R["d0"] + 0.01, R["d0"] - G["d"]
    return [rbox(cx - G["l"] / 2, R["y1"] - G["w"], cx + G["l"] / 2, R["y1"], d0, d1),
            rbox(R["x0"], cy - G["l"] / 2, R["x0"] + G["w"], cy + G["l"] / 2, d0, d1)]


# ------------------------------------------------------------------ Taster (eingefroren, wie v2)
def button_mount():
    d0, d1 = P.RING_T - P.SHEET["t"], P.RING_T - P.SHEET["t"] + P.BTN_PLATE_T
    bore = P.BTN_CYL_D + 0.6
    ay0, ay1 = P.BTN_ARM_Y
    da = max(d0, F0)
    solid = cyl(P.BTN_C[0], P.BTN_C[1], d0, d1, P.RING_D - 1.0).fuse([
        rbox(B["x0"] + WALL, ay0, P.BTN_C[0], ay1, da, d1),
        rbox(P.BTN_C[0], ay0, B["x1"] - WALL, ay1, da, d1),
        cyl(P.BTN_C[0], P.BTN_C[1], d0, d0 + 20.0, bore + 5.0)])
    cuts = [cyl(P.BTN_C[0], P.BTN_C[1], d0 - 1.0, d0 + 21.0, bore),
            rbox(P.BTN_C[0] - 6.0, P.BTN_C[1] - bore, P.BTN_C[0] + 6.0, P.BTN_C[1], d1 + 0.5, d0 + 21.0)]
    for s in (-1, 1):
        cuts.append(cyl(P.BTN_C[0] + s * P.BTN_SCREW_CC / 2, P.BTN_C[1], d0, d0 + P.INS["l"], P.INS["d"]))
    O = P.BTN_ORING
    cuts.append(cyl(P.BTN_C[0], P.BTN_C[1], d0 - 0.001, d0 + O["d"], O["mean"] + O["w"])
                .cut(cyl(P.BTN_C[0], P.BTN_C[1], d0 - 0.002, d0 + O["d"] + 0.1, O["mean"] - O["w"])))
    return solid.cut(cuts)


def mic_pocket():
    M, (x, y) = P.MIC_POCKET, P.MIC_C
    z = P.STEEL["t"]
    boss = cyl(x, y, z + M["membrane_t"], z + M["boss_l"], M["boss_d"])
    cuts = [cyl(x, y, z - 1.0, z + M["depth"], M["bore"]),
            cyl(x, y, z + M["depth"] - 0.01, z + M["boss_l"] + 1.0, M["opening"])]
    return boss, cuts


def plate_bosses():
    """v3: nur noch die 2 unteren Auflager (oben haengt die Platte am Klemmring)."""
    add, cut = [], []
    for (x, y) in P.PLATE_BOSSES:
        left = x < (B["x0"] + B["x1"]) / 2
        x0 = B["x0"] + WALL if left else x - 5.0
        x1 = x + 5.0 if left else B["x1"] - WALL
        add.append(rbox(x0, y - 5.0, x1, y + 5.0, P.PLATE_Z, P.PLATE_Z + 10.0))
        cut.append(cyl(x, y, P.PLATE_Z - 0.5, P.PLATE_Z + P.INS["l"], P.INS["d"]))
    return add, cut


# ------------------------------------------------------------------ Stahl-Aufnahmen (B-02 v3)
def bar_axes():
    return [("links", P.BAR["x"], P.BAR["stop_l"]), ("rechts", B["x0"] + B["x1"] - P.BAR["x"], P.BAR["stop_r"])]


def steel_mounts(oring=True):
    """Gegenleisten-Kanaele wie v2, aber OBEN ZU (v3): die Leiste wird in der Druckpause bei z 54.0 eingelegt und vom
    Kragen ueberdruckt. Unten Boden + Ablaufloch nach aussen. Abstandsringe mit O-Ring-Nut, 2 Zapfen."""
    Bp, S, O = P.BAR, P.STEEL, P.ORING
    d0 = P._BAR_D0
    d1 = d0 + Bp["t"] + 2 * Bp["play_d"]
    cw = Bp["w"] / 2 + Bp["play_x"]
    add, cut = [], []
    for side, ax, stop in bar_axes():
        sgn = -1 if side == "links" else 1
        x_wall = B["x0"] + WALL if sgn < 0 else B["x1"] - WALL
        x_in = ax - sgn * (cw + Bp["inner"])
        add.append(rbox(min(x_wall, x_in), B["y0"] + WALL, max(x_wall, x_in), stop + Bp["back"], d0 - 0.01,
                        d1 + Bp["back"]))
        cut.append(rbox(ax - cw, P.BAR_TOP_END, ax + cw, stop, d0, d1))              # Kanal, oben ZU (v3)
        x_out = B["x0"] - 1.0 if sgn < 0 else B["x1"] + 1.0
        cut.append(xcyl(min(x_out, ax), max(x_out, ax), stop - 1.2, (d0 + d1) / 2, 2.0))   # Ablauf
        for y in P.BAR_HOLES[side]:
            add.append(cyl(ax, y, F0 - S["glue"], F0 + 0.01, P.STANDOFF_D))           # Abstandsring = Fugendicke
            cut.append(cyl(ax, y - Bp["slot"], F0 - S["glue"] - 0.5, d0 + 0.5, Bp["hole"]).fuse(
                [cyl(ax, y + Bp["slot"], F0 - S["glue"] - 0.5, d0 + 0.5, Bp["hole"]),
                 rbox(ax - Bp["hole"] / 2, y - Bp["slot"], ax + Bp["hole"] / 2, y + Bp["slot"],
                      F0 - S["glue"] - 0.5, d0 + 0.5)]))                                # Langloch +-0.5 in y
            z0 = F0 - S["glue"]
            if oring:
                cut.append(cyl(ax, y, z0 - 0.5, z0 + O["groove_d"], O["groove_od"]))   # O-Ring-Nut (v3)
    for (x, y) in P.SPIGOTS:
        add.append(cyl(x, y, P.SPIGOT["tip"], F0 + 0.01, P.SPIGOT["d"]))
    for (x, y) in P.SCREWS:
        cut.append(cyl(x, y, F0 - 0.01, F0 + 1.0, 4.0))
    return add, cut


def seal_line():
    """Dichtlinie Variante A (wie v2)."""
    S = P.SEAL
    w2 = S["w"] / 2
    xl, xr, ys, ya = S["x_l"], S["x_r"], S["y_sill"], S["y_arm"]
    xa, xb = P.SEAL_ARC_X
    cx, cy = P.BTN_C
    g0, g1 = F0 - 0.01, F0 + S["d"]
    segs = [rbox(xl - w2, ys - w2, xr + w2, ys + w2, g0, g1), rbox(xl - w2, ys - w2, xl + w2, ya + w2, g0, g1),
            rbox(xr - w2, ys - w2, xr + w2, ya + w2, g0, g1), rbox(xl - w2, ya - w2, xa, ya + w2, g0, g1),
            rbox(xb, ya - w2, xr + w2, ya + w2, g0, g1)]
    ring = cyl(cx, cy, g0, g1, 2 * (S["r_arc"] + w2)).cut(cyl(cx, cy, g0 - 0.1, g1 + 0.1, 2 * (S["r_arc"] - w2)))
    arc = ring.common(rbox(cx - 40.0, cy - 40.0, cx + 40.0, ya, g0 - 0.1, g1 + 0.1))
    groove = segs[0].fuse(segs[1:] + [arc]).removeSplitter()
    e = w2 + S["land"]
    dt = F0 + S["deck_t"]
    mouth = rbox(B["x0"] + FW, B["y0"] + FW, B["x1"] - FW, B["y1"] - FW, F0, dt, max(P.CORNER_R - FW, 0.5))
    wet = rbox(B["x0"], ya - e, B["x1"], B["y1"], F0, dt).fuse(cyl(cx, cy, F0, dt, 2 * (S["r_arc"] + e)))
    deck = mouth.common(wet).cut(cyl(cx, cy, F0 - 1.0, dt + 1.0, P.RING_D - 1.0 - 0.3))
    return groove, deck.removeSplitter()


def gland_hole():
    """v3: teilbare M20-Verschraubung, Wandloch Ø20.5 im 3-mm-Boden (der RJ45-Stecker passt hindurch)."""
    G = P.GLAND
    gx, gd = G["c"]
    return ycyl(gx, gd, B["y1"] - WALL - 1.0, B["y1"] + 1.0, G["hole_d"])


def usb_mount():
    U, (ox0, ox1, od0, od1) = P.USB_FIELD, P.USB_OPEN
    y_in = B["y1"] - WALL
    add = [ycyl(x, d, y_in - P.INS["l"], y_in + 0.01, U["boss_d"]) for (x, d) in U["screws"]]
    cut = [rbox(ox0, P.USB_CUP[4] - 1.0, ox1, B["y1"] + 1.0, od0, od1)]
    cut += [ycyl(x, d, B["y1"] - P.INS["l"], B["y1"] + 1.0, P.INS["d"]) for (x, d) in U["screws"]]
    return add, cut


def anchors():
    """Holzschrauben mit Senkkopf (v3): 90-Grad-Senkung von innen, Kopf buendig mit der Rueckwand."""
    out = []
    r1, r0 = P.ANCHOR_HEAD_D / 2, P.ANCHOR_D / 2
    for (x, y) in P.ANCHORS:
        out.append(cyl(x, y, DB - 0.5, DEPTH + 0.5, P.ANCHOR_D))
        out.append(Part.makeCone(r1 + 0.5, r0, (r1 - r0) + 0.5, pt(x, y, DB - 0.5), V(0, 1, 0)))
    return out


# ------------------------------------------------------------------ Computer-Traeger: Schienen (W-03 v3)
def rail_lips():
    """Kurze Lippen auf der Rueckwand, je eine pro Traegerzunge. Die 45-Grad-Unterseite der Lippe liegt mit 0.3 Spiel VOR
    der Fase der Zunge (druckt ohne Stuetzen, Rueckwand liegt auf dem Bett). Nur die oberste Lippe hat einen Anschlag:
    beim Hochschieben laufen die unteren Zungen unter den oberen Lippen hindurch."""
    out = []
    for side, (y0, y1), stop, prof in rail_profiles():
        out.append(prism_xd(prof, y0, y1))
        if stop:
            xs = [p_[0] for p_ in prof]
            out.append(rbox(min(xs), y0 - P.CARRIER["stop"], max(xs), y0, P.CARRIER["ridge_d"], DB + 0.01))
    return out


def rail_profiles():
    """[(Seite, (y0, y1), Anschlag?, Profil [(x, d)])] - eine Quelle fuer Kasten, Pruefung und Bilder."""
    C = P.CARRIER
    pl, bv, rd = C["play"], C["bevel"], C["ridge_d"]
    xt_l, xt_r = C["x0"] - C["tab_out"], C["x1"] + C["tab_out"]      # Zungenkante an der Rueckseite (d 57)
    out = []
    for i, (a, b) in enumerate(C["tabs"]):
        xl57, xl54 = xt_l - pl, xt_l - pl + bv                         # Lippenflaeche 0.3 links (vor) der Zungenfase
        out.append(("links", (a, b), i == 0, [(xl57 - C["ridge_w"], DB + 0.01), (xl57, DB + 0.01), (xl54, DB - bv),
                                               (xl54, rd), (xl57 - C["ridge_w"], rd)]))
        xr57, xr54 = xt_r + pl, xt_r + pl - bv
        out.append(("rechts", (a, b), i == 0, [(xr54, rd), (xr54, DB - bv), (xr57, DB + 0.01),
                                                (xr57 + C["ridge_w"], DB + 0.01), (xr57 + C["ridge_w"], rd)]))
    return out


# ------------------------------------------------------------------ Kabelbinder-Oesen (W-05 v3)
def eyelet_back(x, y, ang):
    """Oese auf der Rueckwand: Block mit Spitzbogen-Kanal (45 Grad, druckt ohne Stuetzen), Binder laeuft in Richtung
    ang (Grad, 0 = x, 90 = y)."""
    E = P.EYELET
    hb, pk, w, L = E["base"] / 2, E["peak"], E["wall"], E["depth"]
    H = pk + w
    blk = Part.makeBox(L, H, 2 * (hb + w), V(-L / 2, DB - H, -(hb + w)))
    tri = Part.makePolygon([V(-L / 2 - 1, DB + 0.01, -hb), V(-L / 2 - 1, DB + 0.01, hb), V(-L / 2 - 1, DB - pk, 0),
                            V(-L / 2 - 1, DB + 0.01, -hb)])
    ch = Part.Face(tri).extrude(V(L + 2, 0, 0))
    s = blk.cut(ch)
    s.rotate(V(0, 0, 0), V(0, 1, 0), ang)
    s.translate(V(x, 0, -y))
    return s


def eyelet_channel(x, y, ang, grow=0.0):
    """Nur der Kanal (fuer die Pruefung)."""
    E = P.EYELET
    hb, pk, L = E["base"] / 2 + grow, E["peak"] + grow, E["depth"]
    tri = Part.makePolygon([V(-L / 2 - 1, DB, -hb), V(-L / 2 - 1, DB, hb), V(-L / 2 - 1, DB - pk, 0), V(-L / 2 - 1, DB, -hb)])
    ch = Part.Face(tri).extrude(V(L + 2, 0, 0))
    ch.rotate(V(0, 0, 0), V(0, 1, 0), ang)
    ch.translate(V(x, 0, -y))
    return ch


def eyelet_wall(side, y, d):
    """Oese an der Seitenwand: Buegel mit Kanal fuer den Binder, der Binder laeuft in y."""
    E = P.EYELET
    g, h, w, L = E["side_gap"], E["side_h"], 2.0, E["depth"]
    xw = B["x0"] + WALL if side == "links" else B["x1"] - WALL
    sg = 1 if side == "links" else -1
    xa, xb = sorted((xw - sg * 0.5, xw + sg * (g + w)))
    blk = rbox(xa, y - L / 2, xb, y + L / 2, d - h / 2 - w, d + h / 2 + w)
    ca, cb = sorted((xw - sg * 0.5, xw + sg * g))
    return blk.cut(rbox(ca, y - L / 2 - 1, cb, y + L / 2 + 1, d - h / 2, d + h / 2))


def eyelets():
    out = [eyelet_back(x, y, a) for (x, y, a) in P.LAN_EYELETS]
    out += [eyelet_wall(s, y, d) for (s, y, d) in P.WALL_EYELETS]
    return out


# ------------------------------------------------------------------ SHT31-D-Aussenkammer (W-02 v3)
def sht_chamber():
    """Zwei Waende (links, oben) von der Rueckwand bis zum Deckel; rechts und unten schliessen Kastenwand und Boden.
    2 Zuluftloecher nach unten, 1 Abluft oben rechts schraeg nach unten durch die Seitenwand."""
    S = P.SHT
    dl = S["d0"] + S["lid_t"]                                   # Vorderkante der Waende = Deckelrueckseite
    add = [rbox(S["x0"], S["y0"], S["x0"] + S["wall"], B["y1"] - WALL + 0.01, dl, DB + 0.01),
           rbox(S["x0"], S["y0"], B["x1"] - WALL + 0.01, S["y0"] + S["wall"], dl, DB + 0.01)]
    cut = [ycyl(x, d, B["y1"] - WALL - 1.0, B["y1"] + 1.0, S["hole_d"]) for (x, d) in S["holes"]]
    a = pt(B["x1"] - WALL - 1.5, S["vent_y"] - 1.5, (dl + DB) / 2)
    cut.append(Part.makeCylinder(S["vent_d"] / 2, 9.0, a, V(1, 0, -1).normalize()))
    return add, cut


def sht_lid_seat():
    """Innenraum der Kammer (fuer Pruefungen)."""
    S = P.SHT
    return rbox(S["x0"] + S["wall"], S["y0"] + S["wall"], B["x1"] - WALL, B["y1"] - WALL, S["d0"] + S["lid_t"], DB)


# ------------------------------------------------------------------ Verteiler-Sitz (W-04 v3)
def vert_seat():
    """1-mm-Rand auf der Rueckwand um den Sockelboden: legt die Klebestelle fest."""
    Vt, K = P.VERTEILER, P.VERT_SOCKET
    i = K["inset"] - K["seat_play"]
    x0, x1 = Vt["x0"] + i, Vt["x0"] + Vt["w"] - i
    y0, y1 = Vt["y0"] + i, Vt["y0"] + Vt["h"] - i
    r = K["seat_rim"]
    ring = rbox(x0 - r, y0 - r, x1 + r, y1 + r, DB - r, DB + 0.01).cut(rbox(x0, y0, x1, y1, DB - r - 1.0, DB + 1.0))
    return ring.cut(rbox(x1 - 0.5, y0 + 2.0, x1 + r + 1.0, y1 - 2.0, DB - r - 1.0, DB + 1.0))   # rechts frei (Rastfinger)


# ------------------------------------------------------------------ Bauen
def build_box():
    block, block_cuts = grille_module()
    p_add, p_cut = plate_bosses()
    m_add, m_cut = mic_pocket()
    s_add, s_cut = steel_mounts()
    seal_groove, deck = seal_line()
    u_add, u_cut = usb_mount()
    h_add, h_cut = sht_chamber()
    shape = box_shell().fuse([block, button_mount(), m_add, deck, vert_seat()] + flange_ramps() + p_add + s_add
                             + u_add + h_add + rail_lips() + eyelets())
    shape = shape.cut([gland_hole(), seal_groove] + m_cut + flange_passes() + block_cuts + p_cut + s_cut + u_cut
                      + h_cut + [cyl(P.BTN_C[0], P.BTN_C[1], -1.0, P.RING_T - P.SHEET["t"] + 0.3, P.BTN_HOLE)]
                      + anchors()).removeSplitter()
    shape.exportBrep(BREP_BOX)
    print("Kasten v3: Solids %d | valid %s | %.0f mm3 (PETG 1.27 = %.0f g)"
          % (len(shape.Solids), shape.isValid(), shape.Volume, shape.Volume * 1.27e-3))
    return shape


# ------------------------------------------------------------------ Display-Traegerplatte (v3)
def plate_body():
    PL, PT = P.PLATE, P.PLATE_TONGUE
    d0, d1 = P.PLATE_Z - PL["t"], P.PLATE_Z
    p = rbox(PL["x0"], PL["y0"], PL["x1"], PL["y1"], d0, d1, 4.0)
    p = p.fuse([rbox(a, PT["y0"], b, PL["y0"] + 2.0, d0, d1) for (a, b) in PT["xs"]])     # Zungen oben (in der Dicke)
    return p


def build_plate():
    PL, DP = P.PLATE, P.DISPLAY_PIN
    d0, d1 = P.PLATE_Z - PL["t"], P.PLATE_Z
    p = plate_body()
    sx, sy = P.PLATE_STOP["c"]
    p = p.fuse(cyl(sx, sy, d1 - 0.01, P.PLATE_STOP["d1"], P.PLATE_STOP["d"]).fuse(
        Part.makeCone(P.PLATE_STOP["d"] / 2 + 2.0, P.PLATE_STOP["d"] / 2, 2.0, pt(sx, sy, d1 - 0.01), V(0, 1, 0))))
    wx0, wy0, wx1, wy1 = P.PLATE_WINDOW
    cuts = [rbox(wx0, wy0, wx1, wy1, d0 - 1.0, d1 + 1.0, 2.0)]                            # Fenster hinter den Leisten
    cuts += [cyl(x, y, d0 - 0.5, d1 + 0.5, P.PLATE_HOLE) for (x, y) in P.PLATE_BOSSES]
    cuts += [cyl(x, y, d0 - 0.5, d0 + DP["socket"], DP["d"] + 2 * P.FIT["pocket"]) for (x, y) in P.DISPLAY_PINS]
    cuts += [cyl(x, y, d1 - 2.0, d1 + 0.5, P.FIT["peg_hole"]) for (x, y) in P.AMP_PEGS]
    p = p.cut(cuts).removeSplitter()
    p.exportBrep(BREP_PLATE)
    print("Display-Traegerplatte v3: Solids %d | valid %s | %.0f mm3 (%.0f g PETG)" % (len(p.Solids), p.isValid(), p.Volume,
                                                                                        p.Volume * 1.27e-3))
    return p


# ------------------------------------------------------------------ Belegung als Koerper
def component_solids():
    out = {}
    for nm, (e, src, zone) in P.LAYOUT.items():
        if nm == "Klingelrechner":
            parts = [rbox(q[0], q[2], q[1], q[3], q[4], q[5]) for q in P.BELL_PARTS.values()]
            out[nm] = parts[0].fuse(parts[1:])
        elif nm in P.ROUND:
            out[nm] = cyl((e[0] + e[1]) / 2, (e[2] + e[3]) / 2, e[4], e[5], P.ROUND[nm])
        else:
            out[nm] = rbox(e[0], e[2], e[1], e[3], e[4], e[5])
    return out


def lan_cable(r=None):
    """LAN-Kabel als Schlauch entlang P.LAN_PATH."""
    r = P.LAN["cable_d"] / 2 if r is None else r
    pts = [pt(*p) for p in P.LAN_PATH]
    segs = [Part.makeCylinder(r, (b - a).Length, a, (b - a).normalize()) for a, b in zip(pts, pts[1:])]
    segs += [Part.makeSphere(r, p) for p in pts[1:-1]]
    return segs[0].fuse(segs[1:])


# ------------------------------------------------------------------ Zweite Pruefstufe: am Koerper
def check_cad():
    sh = Part.Shape(); sh.importBrep(BREP_BOX)
    plate = Part.Shape(); plate.importBrep(BREP_PLATE)
    print("\n--- Kasten v3: am fertigen Koerper nachgemessen ---")
    bad = 0

    def frac(probe):
        return sh.common(probe).Volume / probe.Volume

    def line(name, ok, txt):
        nonlocal bad
        print("  %-44s %s%s" % (name, txt, "" if ok else "   <<<"))
        bad += not ok

    def ring_test(name, x, y, d0, d1, hole_d, need):
        ann = cyl(x, y, d0, d1, hole_d + 2 * need).cut(cyl(x, y, d0 - 0.1, d1 + 0.1, hole_d))
        q = frac(ann)
        line(name, q > 0.995, "%5.1f%% Material im %.1f-mm-Ring" % (100 * q, need))

    # Stahl-Aufnahmen
    slab = rbox(B["x0"] - 5.0, B["y0"] - 5.0, B["x1"] + 5.0, B["y1"] + 5.0, -5.0, P.STEEL["t"])
    v = sh.common(slab).Volume
    want = len(P.SPIGOTS) * math.pi * (P.SPIGOT["d"] / 2) ** 2 * (P.STEEL["t"] - P.SPIGOT["tip"])
    line("Kasten vor der Stahlrueckseite", abs(v - want) < 0.5, "%.1f mm3 (nur die Zapfen: %.1f)" % (v, want))
    cw = P.BAR["w"] / 2 + P.BAR["play_x"]
    d0, d1 = P._BAR_D0, P._BAR_D0 + P.BAR["t"] + 2 * P.BAR["play_d"]
    for side, ax, stop in bar_axes():
        sgn = -1 if side == "links" else 1
        y0, y1 = P.BAR_TOP_END + 2.0, stop - 2.5
        for wn, w in (("aussen", rbox(min(ax + sgn * (cw + 0.05), ax + sgn * (cw + P.BAR["skin"] - 0.05)), y0,
                                       max(ax + sgn * (cw + 0.05), ax + sgn * (cw + P.BAR["skin"] - 0.05)), y1, d0, d1)),
                      ("innen", rbox(min(ax - sgn * (cw + 0.05), ax - sgn * (cw + P.BAR["inner"] - 0.05)), y0,
                                     max(ax - sgn * (cw + 0.05), ax - sgn * (cw + P.BAR["inner"] - 0.05)), y1, d0, d1)),
                      ("hinten", rbox(ax - cw, y0, ax + cw, y1, d1 + 0.05, d1 + P.BAR["back"] - 0.05)),
                      ("oben ZU", rbox(ax - cw, P.BAR_TOP_END - 4.0, ax + cw, P.BAR_TOP_END - 0.05, d0, d1)),
                      ("Kragen ueber der Leiste", rbox(ax - cw, y0, ax + cw, y1, F0 + 0.05, d0 - 0.05).cut(
                          [cyl(ax, y, F0 - 1, d0 + 1, P.BAR["hole"] + 2 * P.BAR["slot"] + 0.2)
                           for y in P.BAR_HOLES[side]]))):
            q = frac(w)
            line("Kanal %s, %s" % (side, wn), q > 0.995, "%5.1f%% Material" % (100 * q))
    comps = component_solids()
    for side in ("links", "rechts"):                            # Druckpause: Leiste von oben (vorn) einlegen
        bar = comps["Gegenleiste " + side]
        pre = sh.common(rbox(B["x0"] - 5, B["y0"] - 5, B["x1"] + 5, B["y1"] + 5, P._BAR_D0 + 0.001, DEPTH + 1))
        worst = 0.0
        for k in range(0, 9):
            m = bar.copy(); m.translate(V(0, -(8 - k) * 1.0, 0))     # aus d -8 bis Endlage
            worst = max(worst, pre.common(m).Volume)
        rest = sh.common(bar).Volume
        line("Leiste %s in der Druckpause einlegen" % side, worst < 0.01 and rest < 0.01,
             "Weg %.2f mm3 | Endlage %.2f mm3 (muss 0)" % (worst, rest))
    O = P.ORING
    for side, ax, stop in bar_axes():
        for y in P.BAR_HOLES[side][:1] + P.BAR_HOLES[side][-1:]:
            z0 = F0 - P.STEEL["glue"]
            groove = cyl(ax, y, z0 + 0.05, z0 + O["groove_d"] - 0.05, O["groove_od"] - 0.1).cut(
                cyl(ax, y, z0, z0 + 1, O["groove_id"] + 0.1))
            rim = cyl(ax, y, z0 + 0.05, F0 - 0.05, P.STANDOFF_D - 0.1).cut(cyl(ax, y, z0, F0, O["groove_od"] + 0.1))
            line("O-Ring-Nut %s y %.0f" % (side, y), sh.common(groove).Volume < 0.01 and frac(rim) > 0.99,
                 "Nut frei %.2f mm3 | Rand %.1f%%" % (sh.common(groove).Volume, 100 * frac(rim)))
    # Dichtlinie + Bodenwand (wie v2)
    S = P.SEAL
    groove, _deck = seal_line()
    under = groove.copy(); under.translate(V(0, S["d"] + 0.05, 0))
    q = frac(under)
    line("Dichtlinie: Auflage unter der Rinne", q > 0.995, "%5.1f%% Material" % (100 * q))
    cx, cy = P.BTN_C
    w2 = S["w"] / 2
    mouth = rbox(B["x0"] + FW, B["y0"] + FW, B["x1"] - FW, B["y1"] - FW, F0 + 1.4, F0 + 1.9, max(P.CORNER_R - FW, 0.5))
    wet = rbox(B["x0"], S["y_arm"] + w2, B["x1"], B["y1"], F0 + 1.4, F0 + 1.9).fuse(
        cyl(cx, cy, F0 + 1.4, F0 + 1.9, 2 * (S["r_arc"] - w2)))
    holes = [cyl(cx, cy, F0, F0 + 3.0, P.BTN_CYL_D + 0.6)]
    holes += [cyl(cx + sg * P.BTN_SCREW_CC / 2, cy, F0, F0 + 3.0, P.INS["d"]) for sg in (-1, 1)]
    holes.append(cyl(P.MIC_C[0], P.MIC_C[1], F0, F0 + 3.0, P.MIC_POCKET["bore"]))
    q = frac(mouth.common(wet).cut(holes))
    line("Bodenwand: nasse Bucht zu", q > 0.995, "%5.1f%% Material" % (100 * q))
    for i, (a, b) in enumerate([(29.0, 47.0), (53.0, 71.0)]):          # v2-LED-Fenster: Kragen jetzt voll (bis aufs Kabelloch)
        probe = rbox(a, 8.0, b, 14.0, F0 + 0.05, F0 + FT - 0.05)
        if i == 1:
            probe = probe.cut(cyl(*P.LED_CABLE["c"], F0 - 1, F0 + 5, P.LED_CABLE["collar"] + 0.2))
        q = frac(probe)
        line("Kragen am alten LED-Fenster %d voll" % (i + 1), q > 0.995, "%5.1f%% Material" % (100 * q))
    lx, ly = P.LED_CABLE["c"]
    v = sh.common(cyl(lx, ly, F0 - 1.0, F0 + FT + (FW - WALL) + 3.0, P.LED_CABLE["collar"] - 0.2)).Volume
    line("LED-Kabelloch frei bis ins Innere", v < 0.01, "%.2f mm3" % v)
    fl = []
    for d in (F0 + 0.5, P.CAV["d"] - 0.5):
        y = next((48.0 + i * 0.05 for i in range(300) if sh.isInside(pt(50.0, 48.0 + i * 0.05, d), 0.001, True)), None)
        fl.append(y)
    ok = fl[0] is not None and fl[1] is not None and fl[1] < fl[0] - 0.5 and fl[0] <= P.GRILLE["y1"] - 0.2
    line("Hohlraumboden faellt nach vorn", ok, "vorn y %.2f / hinten y %.2f" % (fl[0] or -1, fl[1] or -1))
    v = sum(sh.common(cyl(ax, y, 0.0, P.BAR["screw_l"], 3.0)).Volume for side, ax, stop in bar_axes()
            for y in P.BAR_HOLES[side])
    line("Leistenschrauben M3x%.0f frei" % P.BAR["screw_l"], v < 0.01, "%.2f mm3" % v)
    for s in (-1, 1):
        x = P.BTN_C[0] + s * P.BTN_SCREW_CC / 2
        d0b = P.RING_T - P.SHEET["t"]
        ring_test("Tasterschraube (%.2f)" % x, x, P.BTN_C[1], d0b + P.BTN_ORING["d"] + 0.3, d0b + P.INS["l"] - 0.5,
                  P.INS["d"], P.MIN_WALL)
    G = P.GLAND
    gx, gd = G["c"]
    y0, y1 = B["y1"] - WALL + 0.3, B["y1"] - 0.3
    v = sh.common(ycyl(gx, gd, y0 - 1, y1 + 1, G["hole_d"] - 0.2)).Volume
    ann = ycyl(gx, gd, y0, y1, G["hole_d"] + 4.0).cut(ycyl(gx, gd, y0 - 0.1, y1 + 0.1, G["hole_d"]))
    line("Einfuehrung M20: Loch frei, Boden rundum", v < 0.01 and frac(ann) > 0.995,
         "frei %.2f mm3 | %5.1f%% im 2-mm-Ring" % (v, 100 * frac(ann)))
    nut = ycyl(gx, gd, B["y1"] - WALL - G["nut_t"], B["y1"] - WALL - 0.05, G["nut_d"])
    v = sh.common(nut).Volume
    line("Einfuehrung: Gegenmutter Ø%.0f hat Platz" % G["nut_d"], v < 0.01, "%.2f mm3" % v)
    for (x, d) in P.USB_FIELD["screws"]:
        y0, y1 = B["y1"] - P.INS["l"] + 0.5, B["y1"] - 0.5
        ann = ycyl(x, d, y0, y1, P.INS["d"] + 2 * P.MIN_WALL).cut(ycyl(x, d, y0 - 0.1, y1 + 0.1, P.INS["d"]))
        q = frac(ann)
        line("USB-Abdeckung Einsatz (%.1f,%.1f)" % (x, d), q > 0.995, "%5.1f%% Material" % (100 * q))
    for (x, y) in P.PLATE_BOSSES:
        ring_test("Plattenauflager (%.1f,%.0f)" % (x, y), x, y, P.PLATE_Z + 0.3, P.PLATE_Z + P.INS["l"] - 0.5,
                  P.INS["d"], P.MIN_WALL)
    # Lautsprecher (B-04 v3): Durchgang + Kopftasche frei, Wand ueber der Tasche, keine alten Einsatzloecher/Sockel
    SS, C = P.SPK_SCREW, P.CAV
    for (x, y) in P.SPK_SCREWS:
        v1 = sh.common(cyl(x, y, C["d"] + 0.1, C["d"] + P.SPK_WALL - 0.1, SS["hole"] - 0.2)).Volume
        v2 = sh.common(cyl(x, y, C["d"] - 2.5, C["d"] - 0.05, SS["pocket_d"] - 0.2)).Volume
        top = rbox(x - 2.0, P.BLOCK["y0"] + 0.05, x + 2.0, y - SS["pocket_d"] / 2 - 0.05, F0 + 0.1, C["d"] - 0.1)
        line("Lautsprecherschraube (%.1f|%.1f)" % (x, y), v1 < 0.01 and v2 < 0.01 and frac(top) > 0.99,
             "Loch %.2f | Kopftasche %.2f mm3 | Wand darueber %5.1f%%" % (v1, v2, 100 * frac(top)))
    for (x, y) in P.SPK_HOLES:
        if (x, y) in P.SPK_SCREWS:
            continue
        v = sh.common(cyl(x, y, C["d"] + 0.5, C["d"] + P.SPK_WALL - 0.5, P.INS["d"] - 0.2)).Volume
        line("Unteres Rahmenloch (%.1f|%.1f): Wand voll (kein Einsatz)" % (x, y), v > 0.9 * math.pi * 1.9 ** 2 * 5,
             "%.1f mm3 Material" % v)
    ring_test("Mikrofontasche", P.MIC_C[0], P.MIC_C[1], P.STEEL["t"] + P.MIC_POCKET["membrane_t"] + 0.1,
              P.STEEL["t"] + P.MIC_POCKET["depth"] - 0.1, P.MIC_POCKET["bore"], P.MIN_WALL - 0.05)
    need = (P.RING_T - P.SHEET["t"]) + P.BTN_CYL_L + P.BTN_FREE
    v = sh.common(cyl(P.BTN_C[0], P.BTN_C[1], P.RING_T - P.SHEET["t"] + 20.0, need, P.BTN_CYL_D + P.BTN_FREE)).Volume
    line("Taster-Freiraumsaeule", v < 0.5, "%.1f mm3" % v)
    G = P.DISPLAY_GLASS
    v = sh.common(rbox(G["x0"], G["y0"], G["x1"], G["y1"], 0.0, P.DISPLAY["stack"])).Volume
    line("Displayraum frei", v < 0.5, "%.1f mm3" % v)
    v = sh.common(cyl(P.SPK["c"][0], P.SPK["c"][1], P.CAV["d"] + 0.5, P.CAV["d"] + P.SPK_WALL - 0.5,
                      P.SPK["port_d"])).Volume
    line("Schalloeffnung frei", v < 0.5, "%.1f mm3" % v)
    # Radar-Nuten (B-06): frei, darunter >= 1.85 Wand
    R, Gr = P.RADAR_POCKET, P.RADAR_GROOVE
    for g in radar_grooves():
        bb = g.BoundBox
        x0_, x1_, y0_, y1_ = bb.XMin, bb.XMax, -bb.ZMax, -bb.ZMin
        free = sh.common(rbox(x0_ + 0.05, y0_ + 0.05, x1_ - 0.05, y1_ - 0.05, R["d0"] - Gr["d"] + 0.05,
                              R["d0"] - 0.05)).Volume
        wall = frac(rbox(x0_ + 0.05, y0_ + 0.05, x1_ - 0.05, y1_ - 0.05, P.CAV["d"] + 0.05, R["d0"] - Gr["d"] - 0.05))
        line("Radar-Nut x %.1f..%.1f y %.1f..%.1f" % (x0_, x1_, y0_, y1_), free < 0.01 and wall > 0.995,
             "frei %.2f mm3 | Wand darunter %5.1f%%" % (free, 100 * wall))
    # Schienenlippen (Traeger-Pruefung in v3_teile), Holzschrauben buendig, Kammer, Verteiler-Sitz, Oesen
    for (x, y) in P.ANCHORS:
        head = Part.makeCone(P.ANCHOR_HEAD_D / 2 - 0.1, P.ANCHOR_D / 2 - 0.1, (P.ANCHOR_HEAD_D - P.ANCHOR_D) / 2,
                             pt(x, y, DB), V(0, 1, 0))
        above = cyl(x, y, DB - 6.0, DB - 0.05, P.ANCHOR_HEAD_D + 1.0)
        v1, v2 = sh.common(head).Volume, sh.common(above).Volume
        line("Holzschraube (%.0f|%.0f) Senkkopf buendig" % (x, y), v1 < 0.01 and v2 < 0.01,
             "Kopf %.2f | darueber %.2f mm3" % (v1, v2))
    Sh = P.SHT
    inner = sht_lid_seat()
    rc = P.CORNER_R - WALL                                                # gerundete Innenecke unten rechts
    corner = rbox(B["x1"] - WALL - rc, B["y1"] - WALL - rc, B["x1"], B["y1"], 0, DEPTH).cut(
        cyl(B["x1"] - WALL - rc, B["y1"] - WALL - rc, -1, DEPTH + 1, 2 * rc))
    inner_probe = rbox(Sh["x0"] + Sh["wall"] + 0.1, Sh["y0"] + Sh["wall"] + 0.1, B["x1"] - WALL - 0.1,
                       B["y1"] - WALL - 0.1, Sh["d0"] + Sh["lid_t"] + 0.1, DB - 0.1).cut(corner)
    vi = sh.common(inner_probe).Volume
    wl = frac(rbox(Sh["x0"] + 0.05, Sh["y0"] + Sh["wall"] + 1, Sh["x0"] + Sh["wall"] - 0.05, B["y1"] - WALL - 1,
                   Sh["d0"] + Sh["lid_t"] + 0.05, DB - 0.05))
    wt = frac(rbox(Sh["x0"] + Sh["wall"] + 1, Sh["y0"] + 0.05, B["x1"] - WALL - 1, Sh["y0"] + Sh["wall"] - 0.05,
                   Sh["d0"] + Sh["lid_t"] + 0.05, DB - 0.05))
    vh = sum(sh.common(ycyl(x, d, B["y1"] - WALL - 0.5, B["y1"] + 0.5, Sh["hole_d"] - 0.2)).Volume for (x, d) in Sh["holes"])
    line("SHT31-Kammer: Waende, Zuluft", vi < 0.5 and wl > 0.995 and wt > 0.995 and vh < 0.01,
         "innen frei %.1f mm3 | Waende %5.1f/%5.1f%% | Loecher %.2f mm3" % (vi, 100 * wl, 100 * wt, vh))
    seat = vert_seat()
    q = frac(seat.common(rbox(B["x0"] + WALL + 0.1, 0, B["x1"], 300, DB - 0.95, DB - 0.05)).removeSplitter())
    line("Verteiler-Sitz (1-mm-Rand)", q > 0.99, "%5.1f%% Material" % (100 * q))
    for (x, y, a) in P.LAN_EYELETS:
        tie = Part.makeBox(P.EYELET["depth"] + 2.0, P.LAN["tie_t"], P.LAN["tie_w"],
                           V(-(P.EYELET["depth"] + 2.0) / 2, DB - P.LAN["tie_t"] - 0.05, -P.LAN["tie_w"] / 2))
        tie.rotate(V(0, 0, 0), V(0, 1, 0), a)
        tie.translate(V(x, 0, -y))
        v = sh.common(tie).Volume
        line("LAN-Oese (%.0f|%.0f): Binder 3.6 x 1.3 geht durch" % (x, y), v < 0.01, "%.2f mm3" % v)
    cab = lan_cable()
    v = sh.common(cab).Volume
    line("LAN-Kabel Ø7: Weg frei vom Stecker zur Einfuehrung", v < 0.5, "%.2f mm3" % v)
    # Belegung gegen Kasten und Platte
    print("\n  Belegung gegen Kasten und Display-Traegerplatte (mm3, muss je 0 sein):")
    for nm, sol in comps.items():
        vb, vp = sh.common(sol).Volume, plate.common(sol).Volume
        ok = vb < 0.5 and vp < 0.5
        bad += not ok
        print("    %-30s Kasten %6.1f | Platte %6.1f %s" % (nm, vb, vp, "" if ok else "<<<"))
    vb = sh.common(plate).Volume
    line("Display-Traegerplatte gegen Kasten", vb < 0.01, "%.2f mm3" % vb)
    m = plate.copy(); m.translate(V(0, -0.15, 0))                   # Zungen liegen an der Blockrueckseite an
    vz = sh.common(m).Volume
    line("Plattenzungen liegen am Gitterblock an", vz > 0.01, "%.2f mm3 bei 0.15 nach vorn" % vz)
    bb = sh.BoundBox
    print("  %-44s %.1f x %.1f x %.1f mm" % ("BoundBox", bb.XLength, bb.YLength, bb.ZLength))
    print("\n%s" % ("ALLE CAD-PRUEFUNGEN BESTANDEN" if bad == 0 else "%d CAD-PRUEFUNGEN FEHLGESCHLAGEN" % bad))
    return bad


if __name__ == "__main__":
    build_box()
    build_plate()
    check_cad()
