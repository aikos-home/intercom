"""Intercom v3 - Druckteile ausser Kasten und Display-Traegerplatte. Masse aus v3_params.py, Bausteine aus v3_kasten.py.

    exec(open(r"hardware\\v3\\cad\\v3_teile.py", encoding="utf-8").read())
    check_teile()

Teile:
  T1 Computer-Traeger (Sprech- + Klingelrechner, Schienen an der Rueckwand)      W-03
  T2 Lautsprecher-Klemmring (Einsaetze am Tisch, Schrauben von vorn)              B-04
  T3 Radar-Rahmen (offen, Schacht +0.5)                                           B-06
  T4 Verstaerker-Rahmen + Zapfen                                                  B-10
  T5 Verteiler-Sockel (4 Stifte, 2 Rastfinger)                                    W-04
  T6 Deckel der SHT31-Kammer                                                      W-02
  T7 Display-Druckstifte in vier Laengen                                          B-12/B-13
  T8 Gegenleisten-Ersatz (PETG, fuer die Druckpause)                              B-02
  T9 Plattenstuetzen links/rechts (Klebeteile, v3.6)                              V3-05
  T10 Abstandsstuecke zwischen Display-Panel und Displayplatine (v3.7)            V3-07
"""
import os as _os
# Paths (public copy): everything relative to this folder, outputs into out/ (gitignored).
V3_DIR = globals().get("V3_DIR") or _os.environ.get("KLINGELBOX_V3_DIR") or _os.path.dirname(_os.path.abspath(__file__))
_os.environ.setdefault("KLINGELBOX_V3_DIR", V3_DIR)
for _d in ("out", _os.path.join("out", "print", "metall")):
    _os.makedirs(_os.path.join(V3_DIR, _d), exist_ok=True)
exec(open(_os.path.join(V3_DIR, "v3_kasten.py"), encoding="utf-8").read())

DF = P.CARRIER_D_FACE


# ------------------------------------------------------------------ T1 Computer-Traeger
def carrier_plate():
    C = P.CARRIER
    A = rbox(C["x0"], C["y0"], C["xa1"], C["ya1"], DF, DB)
    Bt = rbox(C["xa1"] - 0.01, C["y0"], C["x1"], C["y_low"], DF, DB)
    Bl = rbox(C["xa1"] - 0.01, C["y_low"] - 0.01, C["xb1_low"], C["yb1"], DF, DB)
    s = A.fuse([Bt, Bl])
    tabs = []
    for (a, b) in C["tabs"]:
        xl = C["x0"] - C["tab_out"]
        tabs.append(prism_xd([(xl, DB), (C["x0"] + 0.01, DB), (C["x0"] + 0.01, DF), (xl + C["bevel"], DF)], a, b))
        xr = C["x1"] + C["tab_out"]
        tabs.append(prism_xd([(C["x1"] - 0.01, DB), (xr, DB), (xr - C["bevel"], DF), (C["x1"] - 0.01, DF)], a, b))
    s = s.fuse(tabs)
    T = P.TALK
    s = s.cut(rbox(T["x0"] + 3.5, C["y0"] - 1.0, T["x0"] + T["w"] - 3.5, P.TALK_PCB_Y0 + 2.0, DF - 1.0, DB + 1.0))
    s = s.cut(rbox(T["x0"] + 3.5, P.TALK_PCB_Y1 - 0.2, T["x0"] + T["w"] - 3.5, C["ya1"] + 1.0, DF - 1.0, DB + 1.0))  # USB
    return s


def talk_cradle():
    """Wie der v2-Schlitten H5 (passte perfekt): Laengswaende mit 0.5-Lippen ueber den gelben Leisten, oben Rasthaken
    hinter dem Platinenende (Antennenseite), unten Anschlaege nur an den Ecken - die USB-C-Buchsen bleiben frei (B-07)."""
    T, K = P.TALK, P.TALK_CRADLE
    tx0, tx1 = T["x0"], T["x0"] + T["w"]
    pl, w = K["play"], K["wall"]
    ya_, yb_ = P.TALK_PCB_Y0 - 1.7, P.TALK_PCB_Y1 + 2.3
    dl = P.TALK_D_STRIP - K["lip_t"]
    parts = [rbox(tx0 - pl - w, ya_, tx0 - pl, yb_, dl, DF + 0.01), rbox(tx1 + pl, ya_, tx1 + pl + w, yb_, dl, DF + 0.01),
             rbox(tx0 - pl - 0.01, P.TALK_PCB_Y0, tx0 - pl + K["lip"], P.TALK_PCB_Y1, dl, P.TALK_D_STRIP),
             rbox(tx1 + pl - K["lip"], P.TALK_PCB_Y0, tx1 + pl + 0.01, P.TALK_PCB_Y1, dl, P.TALK_D_STRIP),
             rbox(tx0 - pl - 0.01, P.TALK_PCB_Y0 - K["hook_l"] - 0.05, tx0 - pl + K["hook"], P.TALK_PCB_Y0 - 0.05,
                  P.TALK_D_PCB_FRONT, P.TALK_D_PCB_BACK),
             rbox(tx1 + pl - K["hook"], P.TALK_PCB_Y0 - K["hook_l"] - 0.05, tx1 + pl + 0.01, P.TALK_PCB_Y0 - 0.05,
                  P.TALK_D_PCB_FRONT, P.TALK_D_PCB_BACK),
             rbox(tx0 - pl - 0.01, P.TALK_PCB_Y1 + 0.15, tx0 + K["stop_w"], yb_, P.TALK_D_PCB_FRONT - 0.2, DF + 0.01),
             rbox(tx1 - K["stop_w"], P.TALK_PCB_Y1 + 0.15, tx1 + pl + 0.01, yb_, P.TALK_D_PCB_FRONT - 0.2, DF + 0.01)]
    return parts[0].fuse(parts[1:])


def bell_mount():
    """Klingelrechner flach, PoE-Seite zur Rueckwand auf 2 mm Schaumstoff (Bauherr): seitliche Fuehrung am PoE-Modul,
    Sockel unter der RJ45-Buchse, Anschlaege oben an den Platinenecken (nehmen die Steckkraft des LAN-Steckers)."""
    BL, W = P.BELL, P.WAVESHARE
    bx0, bx1 = BL["x0"], BL["x0"] + W["w"]
    px0, px1 = bx0 + (W["w"] - W["poe_w"]) / 2, bx0 + (W["w"] + W["poe_w"]) / 2
    pu0, pu1 = BL["y0"] + W["poe_from_end"], BL["y0"] + W["poe_from_end"] + W["poe_l"]
    gt = 1.2
    parts = [rbox(px0 - 0.2 - gt, pu0 + 1.0, px0 - 0.2, pu1 - 1.0, DF - BL["guide_h"], DF + 0.01),
             rbox(px1 + 0.2, pu0 + 1.0, min(px1 + 0.2 + gt, P.CARRIER["x1"]), pu1 - 1.0, DF - BL["guide_h"], DF + 0.01),
             rbox(bx0 + 0.5, BL["y0"] + 57.5, bx1 - 0.5, P.BELL_Y1 - 0.3, P.BELL_D_CHIP + W["rj45_below"] + BL["ped_gap"],
                  DF + 0.01)]
    for (v0, v1) in ((0.0, BL["stop_v"]), (W["w"] - BL["stop_v"], W["w"])):
        parts.append(rbox(bx0 + v0, BL["y0"] - BL["stop_h"] - 0.3, bx0 + v1, BL["y0"] - 0.3, P.BELL_D_LOGO - 0.5, DF + 0.01))
        parts.append(rbox(bx0 + v0, BL["y0"] - 5.0, bx0 + v1, BL["y0"] - 0.3, 36.0, DF + 0.01))
    return parts[0].fuse(parts[1:])


def carrier():
    return carrier_plate().fuse([talk_cradle(), bell_mount()]).cut(knob_cuts()).removeSplitter()


def knob_cuts():
    """v3.3 (V3-03): hinten eine Gasse, in der der Rastknopf beim Einsetzen und Hochschieben laeuft, an ihrem Ende eine
    45-Grad-Rampe, dann ein kurzer Steg und das Rastloch (durch den ganzen Traeger, damit man den Klebeknopf durchsteckt).
    Masse direkt aus CARRIER_KNOB (nicht aus abgeleiteten Konstanten), damit Mutationstests wirken."""
    K = P.CARRIER_KNOB
    x0, x1 = K["x"] - K["lane_w"] / 2, K["x"] + K["lane_w"] / 2
    hole_y0 = K["y"] - K["hole_d"] / 2
    ramp_y1 = hole_y0 - K["ridge"]
    ramp_y0 = ramp_y1 - K["ramp"]
    lane_y0 = K["y"] - P.CARRIER["S"] - K["lane_over"]
    lane = rbox(x0, lane_y0, x1, ramp_y0 + 0.01, DB - K["lane_t"], DB + 1.0)
    k = K["lane_t"] / K["ramp"]                                 # Steigung der Rampe (1 = 45 Grad)
    ramp = prism_dy([(DB - K["lane_t"], ramp_y0), (DB + 1.0, ramp_y1 + 1.0 / k), (DB + 1.0, ramp_y0 - 0.01)], x0, x1)
    hole = cyl(K["x"], K["y"], DF - 10.0, DB + 1.0, K["hole_d"])
    return [lane, ramp, hole]


def knob_solid(h=None):
    """Rastknopf auf der Rueckwand (Klebeteil), Hoehe h, oben gefast."""
    K = P.CARRIER_KNOB
    h = K["heights"][1] if h is None else h
    r, ch = K["d"] / 2, K["ch"]
    body = cyl(K["x"], K["y"], DB - h + ch - 0.01, DB + 0.01, K["d"])
    top = Part.makeCone(r - ch, r, ch, pt(K["x"], K["y"], DB - h), V(0, 1, 0))
    return body.fuse(top).removeSplitter()


def knobs_print():
    """Die drei Rastknoepfe zum Ausprobieren, Klebeseite unten, mit duennen Stegen verbunden; neben dem flachsten
    (erste Hoehe) ein Faehnchen als Merkmal."""
    K = P.CARRIER_KNOB
    r, ch = K["d"] / 2, K["ch"]
    parts = []
    for i, h in enumerate(K["heights"]):
        x = 6.0 * i
        parts.append(Part.makeCylinder(r, h - ch, V(x, 0, 0)).fuse(Part.makeCone(r, r - ch, ch, V(x, 0, h - ch))))
    parts += [Part.makeBox(6.0 - 2 * r + 0.6, 0.8, 0.2, V(6.0 * i + r - 0.3, -0.4, 0)) for i in range(len(K["heights"]) - 1)]
    parts.append(Part.makeBox(2.5, 2.5, 0.2, V(-r - 3.0, -1.25, 0)))                          # Faehnchen
    parts.append(Part.makeBox(1.0 + 0.3, 0.8, 0.2, V(-r - 0.6 - 0.2, -0.4, 0)))               # Steg zum Faehnchen
    return parts[0].fuse(parts[1:]).removeSplitter()


def talk_board():
    """Sprechrechner (v3-Lage) als Koerper: Platine, gelbe Leisten, Stifte, USB-C, Modul mit Antenne."""
    T = P.TALK
    x0, x1 = T["x0"], T["x0"] + T["w"]
    y0p, y1p = P.TALK_PCB_Y0, P.TALK_PCB_Y1
    pcb = rbox(x0, y0p, x1, y1p, P.TALK_D_PCB_FRONT, P.TALK_D_PCB_BACK)
    strips = rbox(x0, y0p, x0 + 2.54, y1p, P.TALK_D_STRIP, P.TALK_D_PCB_FRONT).fuse(
        rbox(x1 - 2.54, y0p, x1, y1p, P.TALK_D_STRIP, P.TALK_D_PCB_FRONT))
    pins = rbox(x0 + 1.27 - 0.4, y0p, x0 + 1.27 + 0.4, y1p, P.TALK_D_PINS, P.TALK_D_STRIP).fuse(
        rbox(x1 - 1.27 - 0.4, y0p, x1 - 1.27 + 0.4, y1p, P.TALK_D_PINS, P.TALK_D_STRIP))
    usb = rbox(x0 + 4.0, y1p - T["usb_l"], x1 - 4.0, y1p + 0.5, P.TALK_D_PCB_BACK, P.TALK_D_PCB_BACK + T["front"])
    mod = rbox(x0 + 5.0, T["y0"], x1 - 5.0, y0p + T["mod_l"], P.TALK_D_PCB_BACK, P.TALK_D_PCB_BACK + 3.1)
    return {"Platine": pcb, "gelbe Leisten": strips, "lange Stifte": pins, "USB-C": usb, "Modul + Antenne": mod}


def bell_board():
    parts = [rbox(q[0], q[2], q[1], q[3], q[4], q[5]) for q in P.BELL_PARTS.values()]
    return parts[0].fuse(parts[1:])


# ------------------------------------------------------------------ T2 Lautsprecher-Klemmring
def spk_clamp():
    """Rahmen hinter dem Lautsprecher, links offen (dort sitzt der Radar-Rahmen). Oben 2 Dome mit Gewindeeinsatz in den
    oberen Rahmenloechern, unten 2 Druckflaechen auf den unteren Rahmenecken, ein Fuss auf der Gitterblock-Rueckseite
    (Hebel) und zwei Haken, hinter denen die Zungen der Display-Traegerplatte stecken."""
    K, S = P.SPK_CLAMP, P.SPK
    cx, cy = S["c"]
    fx0, fx1, fy0, fy1 = cx - S["frame"] / 2, cx + S["frame"] / 2, cy - S["frame"] / 2, cy + S["frame"] / 2
    d0 = P.SPK_D_FRONT + P.SPK_FRAME_T                          # Rueckseite des Lautsprecherrahmens
    d1 = d0 + K["t"]
    pads = []
    for (x, y) in P.SPK_HOLES:
        pads.append(cyl(x, y, d0, d1, K["boss_d"]))
    top = rbox(fx0 + 0.2, fy0 - 4.0, fx1 + 4.0, fy0 + 0.6, d0, d1)
    right = rbox(fx1 - 0.6, fy0 - 4.0, fx1 + 4.0, fy1 + 0.6, d0, d1)
    bottom = rbox(fx0 + 0.2, fy1 - 0.6, fx1 + 4.0, fy1 + K["bar"], d0, d1)
    bosses = [cyl(x, y, d0, d0 + K["boss_l"], K["boss_d"]) for (x, y) in P.SPK_SCREWS]
    foot = rbox(K["foot_x"][0], fy1 + 0.2, K["foot_x"][1], K["foot_y1"], P.CAV["d"] + P.SPK_WALL, d0 + 0.01)
    s = top.fuse([right, bottom, foot] + pads + bosses)
    pd = P.PLATE_Z + K["play"]                                  # Haken hinter den Plattenzungen
    for (a, b) in K["catch_x"]:
        s = s.cut(rbox(a, fy1 - 1.0, b, fy1 + K["bar"] + 1.0, d0 - 1.0, pd))            # Platz fuer die Zunge
        s = s.fuse(rbox(a, fy1 - 0.6, b, K["catch_y1"], pd, pd + 2.0))
    basket = cyl(cx, cy, d0 - 0.5, d1 + 10.0, 38.0)
    s = s.cut(basket)
    s = s.cut([cyl(x, y, d0 - 0.5, d0 + P.INS["l"], P.INS["d"]) for (x, y) in P.SPK_SCREWS])
    return s.removeSplitter()


def speaker_solids():
    """Lautsprecher als Rahmenblech 40 x 40 x 0.6 + Korb Ø37 + Dichtung."""
    S = P.SPK
    cx, cy = S["c"]
    fr = rbox(cx - 20, cy - 20, cx + 20, cy + 20, P.SPK_D_FRONT, P.SPK_D_FRONT + P.SPK_FRAME_T)
    fr = fr.cut([cyl(x, y, P.SPK_D_FRONT - 1, P.SPK_D_FRONT + 2, S["hole_d"]) for (x, y) in P.SPK_HOLES])
    body = cyl(cx, cy, P.SPK_D_FRONT + P.SPK_FRAME_T - 0.01, P.SPK_D_FRONT + 10.0, 37.0).fuse(
        cyl(cx, cy, P.SPK_D_FRONT + 9.9, P.SPK_D_FRONT + S["behind"], 20.0))
    gasket = rbox(cx - 20, cy - 20, cx + 20, cy + 20, P.CAV["d"] + P.SPK_WALL, P.SPK_D_FRONT).cut(
        [cyl(cx, cy, 0, 40, S["port_d"])] + [cyl(x, y, 0, 40, S["hole_d"]) for (x, y) in P.SPK_HOLES])
    return fr, body, gasket


# ------------------------------------------------------------------ T3 Radar-Rahmen (v3.2: Abstandsrahmen, v3.4 geklebt)
def _front_chamfer(X0, Y0, X1, Y1, d0, ch, m=0.5):
    """4 Dreiecksprismen fuer cut(): 45-Grad-Fase ch an den Aussenkanten der Vorderseite (d0). Nur ebene Flaechen,
    damit die BoundBox exakt bleibt (front_down legt das Teil danach aufs Bett)."""
    def prism(p1, p2, p3, vec):
        return Part.Face(Part.makePolygon([p1, p2, p3, p1])).extrude(vec)
    out = []
    for xe, s in ((X0, 1), (X1, -1)):                           # links/rechts: Dreieck in (x, d), entlang y
        out.append(prism(pt(xe - s * m, Y0 - m, d0 - m), pt(xe + s * (ch + m), Y0 - m, d0 - m),
                         pt(xe - s * m, Y0 - m, d0 + ch + m), V(0, 0, -(Y1 - Y0 + 2 * m))))
    for ye, s in ((Y0, 1), (Y1, -1)):                           # oben/unten: Dreieck in (y, d), entlang x
        out.append(prism(pt(X0 - m, ye - s * m, d0 - m), pt(X0 - m, ye + s * (ch + m), d0 - m),
                         pt(X0 - m, ye - s * m, d0 + ch + m), V(X1 - X0 + 2 * m, 0, 0)))
    return out


def radar_frame(rot=0):
    """v3.2 (V3-02): zwei Seitenleisten an den Langseiten der Platine, vorn je eine Stufe (die Antennenseite liegt 1.9
    vor dem Taschenboden, die Loetstellen der Stiftleiste haben Platz), hinten je eine Lippe; die Platine wird von der
    offenen Seite (y gross) eingeschoben und ist dann gefangen. Oben hinten eine Querverbindung.
    v3.4: keine Quetschrippen mehr, rundum fit Luft zur Tasche, vorn aussen die Fase ch; der Rahmen wird eingeklebt.
    Schacht an der kurzen Seite 0.5 breiter als v2 (B-06). rot=90: derselbe Rahmen gedreht (Drehtest)."""
    if rot == 90:
        cx, cy = P.RADAR["c"]
        s = radar_frame(0).copy()
        s.rotate(V(cx, 0, -cy), V(0, 1, 0), 90.0)
        return s
    R, C = P.RADAR_POCKET, P.RADAR_CARRIER
    cx, cy = P.RADAR["c"]
    X0, X1, Y0, Y1 = R["x0"] + C["fit"], R["x1"] - C["fit"], R["y0"] + C["fit"], R["y1"] - C["fit"]
    d0, d_ant, d_pcb = R["d0"], P.RADAR_D_ANT, P.RADAR_D_PCB_BACK
    d_back = d_pcb + P.RADAR["back"] + 0.15
    bx0, bx1 = cx - P.RADAR["w"] / 2 - C["play_short"], cx + P.RADAR["w"] / 2 + C["play_short"]
    dl0, dl1 = d_pcb + C["chan"], d_pcb + C["chan"] + C["lip_t"]
    parts = [rbox(X0, Y0, bx0, Y1, d0, d_back + C["end_bar"]), rbox(bx1, Y0, X1, Y1, d0, d_back + C["end_bar"]),
             rbox(bx0 - 0.01, Y0, bx0 + C["ledge"], Y1, d0, d_ant),                       # Stufe vorn
             rbox(bx1 - C["ledge"], Y0, bx1 + 0.01, Y1, d0, d_ant),
             rbox(bx0 - 0.01, Y0, bx0 + C["lip"], Y1, dl0, dl1),                          # Lippe hinten
             rbox(bx1 - C["lip"], Y0, bx1 + 0.01, Y1, dl0, dl1),
             rbox(X0, Y0, X1, Y0 + 3.0, d_back, d_back + C["end_bar"])]                     # Querverbindung oben hinten
    s = parts[0].fuse(parts[1:]).removeSplitter()
    return s.cut(_front_chamfer(X0, Y0, X1, Y1, d0, C["ch"])).removeSplitter()


def radar_glue():
    """v3.4: Heisskleber-Naht unten und links, wo der Rahmen aus der Tasche kommt: glue x glue auf der
    Blockrueckseite, am Rahmen anliegend. In beiden Drehlagen gleich. Fuer Bild und Pruefung."""
    R, C = P.RADAR_POCKET, P.RADAR_CARRIER
    g, d1 = C["glue"], P.CAV["d"] + P.SPK_WALL
    X0, X1, Y0, Y1 = R["x0"] + C["fit"], R["x1"] - C["fit"], R["y0"] + C["fit"], R["y1"] - C["fit"]
    bottom = rbox(R["x0"] - g, Y1, X1, R["y1"] + g, d1, d1 + g)
    left = rbox(R["x0"] - g, Y0, X0, Y1 + 0.01, d1, d1 + g)
    return bottom.fuse(left).removeSplitter()


def radar_board(rot=0, side=-1):
    """LD2410C auf der Stufe des Rahmens (v3.2). Stiftleiste auf der Bauteilseite an einer LANGSEITE, mittig (Fotos
    Bauherr 2026-10-16); side -1: an der Langseite bei x klein, +1: bei x gross (Lage 0 Grad). Loetstellen der Leiste
    auf der Antennenseite. Lage rot."""
    H = P.RADAR_HDR
    cx, cy = P.RADAR["c"]
    w, h = P.RADAR["w"], P.RADAR["h"]
    da, db = P.RADAR_D_ANT, P.RADAR_D_PCB_BACK
    pcb = rbox(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2, da, db)
    e = P.RADAR_CARRIER["lip"] + 0.2
    comp = rbox(cx - w / 2 + e, cy - h / 2, cx + w / 2 - e, cy + h / 2, db, db + P.RADAR["back"])
    hx0 = cx - w / 2 + H["edge"] if side < 0 else cx + w / 2 - H["edge"] - H["w"]
    hdr = rbox(hx0, cy - H["l"] / 2, hx0 + H["w"], cy + H["l"] / 2, db, db + H["h"])
    pc = hx0 + H["w"] / 2                                       # Mitte der Stifte
    stub = rbox(pc - H["stub_r"], cy - H["l"] / 2 + 0.5, pc + H["stub_r"], cy + H["l"] / 2 - 0.5, da - H["stub"], da)
    out = {"Platine": pcb, "Bauteile": comp, "Stiftleiste": hdr, "Loetstellen": stub}
    if rot == 90:
        for k in out:
            out[k] = out[k].copy()
            out[k].rotate(V(cx, 0, -cy), V(0, 1, 0), 90.0)
    return out


# ------------------------------------------------------------------ T4 Verstaerker-Rahmen
def engrave(text, x, y, d_face, size, depth):
    """Schrift zum Ausschneiden aus der Flaeche bei d_face: von vorn (-d) lesbar, depth tief nach hinten (+d)."""
    t = label_solid(text, size, depth + 0.1)                   # in XY, z 0..h
    t.rotate(V(0, 0, 0), V(1, 0, 0), 90.0)                     # XY -> XZ, Leseseite nach -Y (vorn)
    bb = t.BoundBox
    t.translate(V(x - (bb.XMin + bb.XMax) / 2, d_face - 0.1 - bb.YMin, -y - (bb.ZMin + bb.ZMax) / 2))
    return t


def step_label(s_):
    return ("%.1f" % s_).replace(".", ",")


def print_row(shapes, gap=4.0):
    """Teile mit der Vorderseite (kleinstes d) aufs Bett drehen und nebeneinander legen (ein STL, mehrere Koerper)."""
    out, x = [], 0.0
    for s in shapes:
        s = s.copy()
        s.rotate(V(0, 0, 0), V(1, 0, 0), 90.0)
        bb = s.BoundBox
        s.translate(V(x - bb.XMin, -bb.YMin, -bb.ZMin))
        out.append(s)
        x += bb.XLength + gap
    return Part.makeCompound(out)


def amp_frame(pin_d=None, label=None):
    """Rahmen fuer den Verstaerker auf der Plattenrueckseite (2 Zapfen 06b). v3.5 (V3-04): Stifte mittig in den
    Loechern, Staerke pin_d (Satz AMP_FRAME pin_steps), mit Spitzenfase; label = Stiftstaerke, unten eingraviert."""
    F = P.AMP_FRAME
    pd = F["pin_d"] if pin_d is None else pin_d
    m = F["margin"]
    base = rbox(P._AMP_X0 - m, P._AMP_Y0 - m, P._AMP_X1 + m, P._AMP_Y1 + m, P.PLATE_Z, P.PLATE_Z + F["base_t"], 1.0)
    d_b = P.PLATE_Z + F["base_t"]
    top = P.AMP_D0 + P.AMP["t"] + F["stake"]
    add = []
    for (hx, hy) in P.AMP_HOLES:
        add.append(cyl(hx, hy, d_b - 0.01, P.AMP_D0, F["boss_d"]))
    for (px, py) in P.AMP_PINS:
        add.append(cyl(px, py, P.AMP_D0 - 0.01, top - F["tip"], pd))
        add.append(Part.makeCone(pd / 2, pd / 2 - F["tip"], F["tip"], pt(px, py, top - F["tip"] - 0.01), V(0, 1, 0)))
    for x0 in (P._AMP_X0, P._AMP_X1 - F["rib_w"]):
        add.append(rbox(x0, P._AMP_Y0 + 4.0, x0 + F["rib_w"], P._AMP_Y1 - 5.5, d_b - 0.01, P.AMP_D0))
    s = base.fuse(add)
    s = s.cut([cyl(x, y, P.PLATE_Z - 0.5, P.PLATE_Z + F["dowel_l"] - 2.0, P.FIT["peg_hole"]) for (x, y) in P.AMP_PEGS])
    if label:
        s = s.cut(engrave(label, P.AMP["c"][0], P.AMP["c"][1], P.PLATE_Z, F["label_h"], F["label_t"]))
    return s.removeSplitter()


def amp_frames_print():
    """v3.5: Satz aus drei Rahmen, einer je Stiftstaerke, Zahl unten eingraviert."""
    return print_row([amp_frame(s_, step_label(s_)) for s_ in P.AMP_FRAME["pin_steps"]])


# ------------------------------------------------------------------ T9 Plattenstuetzen (v3.6, V3-05)
def plate_rests():
    """Zwei Klebeteile [links, rechts] an den Seitenwaenden: Die Display-Traegerplatte liegt hinten auf ihren Zungen auf.
    Koerper von der Seitenwand (Klebeflaeche) bis kurz vor die Plattenkante, vorn an der Rueckseite des Leistenkanals,
    oben an der Unterseite des Gitterblocks; vorn aussen eine Fase ueber der 45-Grad-Rampe am Kanal. Die Zunge reicht
    hinter den Plattenrand, zwischen den Bahnen der Traegerzungen. Rechts = links gespiegelt (Kasten symmetrisch)."""
    R, PL = P.PLATE_REST, P.PLATE
    xw, xb = B["x0"] + WALL, PL["x0"] - R["clear"]
    d0, ytop = P.SHEATH_BACK_D, P.BLOCK["y1"]
    body = rbox(xw, ytop, xb, R["tongue_y1"], d0, R["d1"])
    tongue = rbox(xb - 0.01, R["tongue_y0"], R["x_in"], R["tongue_y1"], P.PLATE_Z + R["play"], R["tongue_d1"])
    ch, m = R["ch"], 0.5
    fase = Part.Face(Part.makePolygon([pt(xw - m, ytop - 1.0, d0 - m), pt(xw + ch + m, ytop - 1.0, d0 - m),
                                       pt(xw - m, ytop - 1.0, d0 + ch + m), pt(xw - m, ytop - 1.0, d0 - m)]))
    left = body.fuse(tongue).cut(fase.extrude(V(0, 0, -(R["tongue_y1"] - ytop + 2.0)))).removeSplitter()
    right = left.mirror(V((B["x0"] + B["x1"]) / 2, 0, 0), V(1, 0, 0))
    return [left, right]


def spacer_comb(t):
    """v3.7 (V3-07): ein Kamm in Drucklage (z oben). Ruecken mit der Dicke als Zahl, daran die Abstandsstuecke der Dicke
    t an duennen Stegen zum Abbrechen. Die Dicke liegt in x (waagerecht, also genau), die Breite w steht in z, die Laenge
    laeuft in y. Gibt (Kamm, [Stuecke]) zurueck."""
    S = P.DISPLAY_SPACER
    w, g, ch = S["w"], S["pitch_gap"], S["ch"]
    bl, bx, bz = S["bridge"][1], S["bridge"][0], S["bridge"][2]     # Steg: Laenge in y, Breite in x, Hoehe in z
    n = len(S["lengths"])
    span = n * t + (n - 1) * g
    parts = [Part.makeBox(span, S["spine_w"], S["spine_t"], V(0, -S["spine_w"], 0))]
    teeth = []
    for i, L in enumerate(S["lengths"]):
        x0 = i * (t + g)
        tooth = Part.makeBox(t, L, w, V(x0, bl, 0))
        for xe, s in ((x0, 1.0), (x0 + t, -1.0)):             # Fase unten an beiden Laengskanten
            tri = Part.Face(Part.makePolygon([V(xe - s * 0.5, bl - 1.0, -0.5), V(xe + s * (ch + 0.5), bl - 1.0, -0.5),
                                              V(xe - s * 0.5, bl - 1.0, ch + 0.5), V(xe - s * 0.5, bl - 1.0, -0.5)]))
            tooth = tooth.cut(tri.extrude(V(0, L + 2.0, 0)))
        teeth.append(tooth.removeSplitter())
        parts.append(Part.makeBox(bx, bl + 0.02, bz, V(x0 + (t - bx) / 2, -0.01, 0)))
    lab = label_solid(step_label(t), S["label_h"], S["label_t"] + 0.01)
    bb = lab.BoundBox
    lab.translate(V(span / 2 - (bb.XMin + bb.XMax) / 2, -S["spine_w"] / 2 - (bb.YMin + bb.YMax) / 2,
                    S["spine_t"] - 0.01))
    return parts[0].fuse(parts[1:] + teeth + [lab]).removeSplitter(), teeth


def spacers_print():
    """v3.7: die drei Kaemme (Dicken DISPLAY_SPACER steps) nebeneinander."""
    out, x = [], 0.0
    for t in P.DISPLAY_SPACER["steps"]:
        c = spacer_comb(t)[0]
        bb = c.BoundBox
        c.translate(V(x - bb.XMin, -bb.YMin, -bb.ZMin))
        out.append(c)
        x += bb.XLength + 6.0
    return Part.makeCompound(out)


def plate_rests_print():
    """Beide Stuetzen mit der Klebeflaeche (Seitenwand) aufs Bett, nebeneinander."""
    lf, rt = plate_rests()
    lf, rt = lf.copy(), rt.copy()
    lf.rotate(V(0, 0, 0), V(0, 1, 0), -90.0)                   # Flaeche bei x klein (Normale -x) nach unten
    rt.rotate(V(0, 0, 0), V(0, 1, 0), 90.0)                    # Flaeche bei x gross (Normale +x) nach unten
    out, x = [], 0.0
    for s in (lf, rt):
        bb = s.BoundBox
        s.translate(V(x - bb.XMin, -bb.YMin, -bb.ZMin))
        out.append(s)
        x += bb.XLength + 4.0
    return Part.makeCompound(out)


def dowels_print(n=4):
    L = P.AMP_FRAME["dowel_l"]
    strip = Part.makeBox(4.0 + 8.0 * n, 6.0, 1.0)
    pegs = [Part.makeCylinder(P.FIT["peg_d"] / 2, L, V(6.0 + 8.0 * i, 3.0, 1.0)) for i in range(n)]
    return strip.fuse(pegs).removeSplitter()


def amp_board():
    pcb = rbox(P._AMP_X0, P._AMP_Y0, P._AMP_X1, P._AMP_Y1, P.AMP_D0, P.AMP_D0 + P.AMP["t"])
    return pcb.cut([cyl(x, y, P.AMP_D0 - 1, P.AMP_D0 + 3, P.AMP["hole_d"]) for (x, y) in P.AMP_HOLES])


# ------------------------------------------------------------------ T5 Verteiler-Sockel
def vert_socket():
    Vt, K = P.VERTEILER, P.VERT_SOCKET
    i = K["inset"]
    x0, x1, y0, y1 = Vt["x0"] + i, Vt["x0"] + Vt["w"] - i, Vt["y0"] + i, Vt["y0"] + Vt["h"] - i
    db_, dp = DB - K["base_t"], P.VERT_D_PCB_BACK
    s = rbox(x0, y0, x1, y1, db_, DB, 1.0)
    s = s.cut(rbox(x0 + 4.0, y0 + 6.0, x1 - 4.0, y1 - 6.0, db_ - 1, DB + 1, 2.0))            # Rahmen statt Vollplatte
    add = []
    for (hx, hy) in P.VERT_HOLES:
        add.append(cyl(hx, hy, dp, db_ + 0.01, K["post_d"]))
        add.append(cyl(hx, hy, dp - Vt["t"] - K["pin_over"], dp + 0.01, K["pin_d"]))
        add.append(rbox(min(hx, x0 + 2.0) - 0.01, hy - 2.25, max(hx, x1 - 2.0) + 0.01, hy + 2.25, db_, DB)
                   .common(rbox(x0, y0, x1, y1, db_ - 1, DB + 1)))
    xe = Vt["x0"] + Vt["w"]                                    # rechte Platinenkante
    for yl in K["latch_y"]:
        a, b = yl - K["latch_w"] / 2, yl + K["latch_w"] / 2
        add.append(rbox(x1 - 3.0, a, xe + 0.2 + K["latch_t"], b, db_, DB))                    # Fuss
        add.append(rbox(xe + 0.2, a, xe + 0.2 + K["latch_t"], b, P.VERT_D_PCB_FRONT - 1.0, db_ + 0.01))   # Finger
        hook = prism_xd([(xe + 0.2 + 0.01, P.VERT_D_PCB_FRONT - 0.05), (xe - K["latch_hook"], P.VERT_D_PCB_FRONT - 0.05),
                         (xe + 0.2 + 0.01, P.VERT_D_PCB_FRONT - 1.0)], a, b)                 # 45-Grad-Einfuehrung
        add.append(hook)
    return s.fuse(add).removeSplitter()


def vert_board():
    Vt = P.VERTEILER
    pcb = rbox(Vt["x0"], Vt["y0"], Vt["x0"] + Vt["w"], Vt["y0"] + Vt["h"], P.VERT_D_PCB_FRONT, P.VERT_D_PCB_BACK)
    return pcb.cut([cyl(x, y, P.VERT_D_PCB_FRONT - 1, P.VERT_D_PCB_BACK + 1, Vt["hole_d"]) for (x, y) in P.VERT_HOLES])


# ------------------------------------------------------------------ T6 SHT31-Kammerdeckel
def sht_lid(pin_d=None, label=None):
    """v3.1: Deckel mit Halter fuer die gemessene SHT31-Platine (Bund, Stift, Rippe). v3.5 (V3-04): Stiftstaerke
    pin_d (Satz SHT_MOUNT pin_steps), label = Stiftstaerke, aussen eingraviert."""
    s = sht_lid_plate().fuse(sht_mount(pin_d)).removeSplitter()
    if label:
        SM = P.SHT_MOUNT
        s = s.cut(engrave(label, SM["label_c"][0], SM["label_c"][1], P.SHT["d0"], SM["label_h"],
                          SM["label_t"])).removeSplitter()
    return s


def sht_lids_print():
    """v3.5: Satz aus drei Deckeln, einer je Stiftstaerke, Zahl aussen eingraviert."""
    return print_row([sht_lid(s_, step_label(s_)) for s_ in P.SHT_MOUNT["pin_steps"]])


def sht_mount(pin_d=None):
    """Bund + Stift fuer das Befestigungsloch der Platine und die Rippe unter ihrer Unterkante (verdrehsicher)."""
    SM = P.SHT_MOUNT
    pd = SM["pin_d"] if pin_d is None else pin_d
    hx, hy = P.SHT_HOLE
    dl, tip = P.SHT_D_LID, P.SHT_D_BACK + SM["pin_over"]
    collar = cyl(hx, hy, dl - 0.01, P.SHT_D_FRONT, SM["collar_d"])
    pin = cyl(hx, hy, P.SHT_D_FRONT - 0.01, tip - 0.3, pd)
    cone = Part.makeCone(pd / 2, pd / 2 - 0.3, 0.3, pt(hx, hy, tip - 0.3 - 0.01), V(0, 1, 0))
    return collar.fuse([pin, cone, sht_rib()])


def sht_rib():
    SM = P.SHT_MOUNT
    y0 = P.SHT_Y1 + SM["rib_gap"]
    return rbox(SM["rib_x"][0], y0, SM["rib_x"][1], y0 + SM["rib_t"], P.SHT_D_LID - 0.01, P.SHT_D_BACK)


def sht_board():
    """SHT31-D-Platine (gemessen) mit Befestigungsloch, ohne Bauteile (deren Huelle steht in LAYOUT)."""
    SM = P.SHT_MOUNT
    hx, hy = P.SHT_HOLE
    pcb = rbox(SM["x0"], SM["y0"], P.SHT_X1, P.SHT_Y1, P.SHT_D_FRONT, P.SHT_D_BACK)
    return pcb.cut(cyl(hx, hy, P.SHT_D_FRONT - 1.0, P.SHT_D_BACK + 1.0, P.SHT_BOARD["hole_d"]))


def sht_lid_plate():
    """Deckel wie v3: Platte auf den Kammerwaenden, Zentrierrand, Kabelloch."""
    S = P.SHT
    d0, d1 = S["d0"], S["d0"] + S["lid_t"]
    s = rbox(S["x0"], S["y0"], B["x1"] - WALL - 0.2, B["y1"] - WALL - 0.2, d0, d1)
    rc = P.CORNER_R - WALL
    cxr, cyr = B["x1"] - WALL - rc, B["y1"] - WALL - rc
    corner = rbox(cxr, cyr, B["x1"], B["y1"], d0 - 1, d1 + 1).cut(cyl(cxr, cyr, d0 - 2, d1 + 2, 2 * rc - 0.4))
    s = s.cut(corner)
    lip = rbox(S["x0"] + S["wall"] + 0.2, S["y0"] + S["wall"] + 0.2, S["x0"] + S["wall"] + 1.4, B["y1"] - WALL - 1.0,
               d1 - 0.01, d1 + 1.0).fuse(rbox(S["x0"] + S["wall"] + 0.2, S["y0"] + S["wall"] + 0.2, B["x1"] - WALL - 1.0,
                                              S["y0"] + S["wall"] + 1.4, d1 - 0.01, d1 + 1.0))
    s = s.fuse(lip).cut(cyl(S["x0"] + S["wall"] + 3.5, S["y0"] + S["wall"] + 3.5, d0 - 1, d1 + 2, 3.5))   # Kabelloch
    return s.removeSplitter()


# ------------------------------------------------------------------ T7 Display-Druckstifte (vier Laengen)
def pin_local(front_d):
    """Ein Stift, Achse z, Fuss (Plattenseite) bei z 0, Spitze oben. front_d = d der Stirn im Einbau."""
    DP = P.DISPLAY_PIN
    foot_d = P.PLATE_Z - P.PLATE["t"] + DP["socket"]
    L = foot_d - front_d
    r, ch = DP["d"] / 2, 0.4
    post = Part.makeCone(r - ch, r, ch, V(0, 0, 0)).fuse(Part.makeCylinder(r, L - ch, V(0, 0, ch)))
    tr, tch = DP["tip_d"] / 2, 0.3
    tip = Part.makeCylinder(tr, DP["tip_l"] - tch, V(0, 0, L)).fuse(Part.makeCone(tr, tr - tch, tch,
                                                                                    V(0, 0, L + DP["tip_l"] - tch)))
    return post.fuse(tip).removeSplitter()


def display_pins(front_d):
    out = []
    foot_d = P.PLATE_Z - P.PLATE["t"] + P.DISPLAY_PIN["socket"]
    for (x, y) in P.DISPLAY_PINS:
        s = pin_local(front_d).copy()
        s.rotate(V(0, 0, 0), V(1, 0, 0), 90.0)
        s.translate(pt(x, y, foot_d))
        out.append(s)
    return out


def label_solid(text, size=4.0, h=0.6):
    wires = Part.makeWireString(text, "C:/Windows/Fonts/arialbd.ttf", size, 0)
    faces = [Part.makeFace(ws, "Part::FaceMakerBullseye") for ws in wires if ws]
    txt = faces[0] if len(faces) == 1 else faces[0].fuse(faces[1:])
    return txt.extrude(V(0, 0, h))


def pins_print():
    """Vier Leisten mit je 5 Stiften, stehend, Fuss unten; jede Leiste traegt ihre Stufe (gegen v2) als Schrift."""
    DP = P.DISPLAY_PIN
    parts = []
    for row, step in enumerate(DP["steps"]):
        y = row * 14.0
        bar = Part.makeBox(10.0 * DP["per_step"] + 22.0, 4.0, 0.8, V(-4.0, y - 2.0, 0.0))
        pins = []
        for i in range(DP["per_step"]):
            s = pin_local(DP["v2_front"] + step).copy()
            s.translate(V(5.0 + 10.0 * i, y, 0.0))
            pins.append(s)
        lab = label_solid(("-%.1f" % step).replace(".", ","))
        bb = lab.BoundBox
        lab.translate(V(10.0 * DP["per_step"] + 3.0 - bb.XMin, y - bb.YLength / 2 - bb.YMin, 0.8))
        parts.append(bar.fuse(pins + [lab]).removeSplitter())
    return parts[0].fuse(parts[1:])


# ------------------------------------------------------------------ T8 Gegenleisten-Ersatz (Druckpause)
def bars_print():
    out = []
    for i, side in enumerate(("links", "rechts")):
        t, b = P.BAR_Y[side]
        bx = 10.0 * i
        s = rbox(bx, t, bx + P.BAR["w"], b, 0.0, P.BAR["t"])
        s = s.cut([cyl(bx + P.BAR["w"] / 2, y, -1.0, P.BAR["t"] + 1.0, 2.5) for y in P.BAR_TAPS[side]])
        out.append(s)
    s = out[0].fuse(out[1])
    s.rotate(V(0, 0, 0), V(1, 0, 0), -90.0)
    bb = s.BoundBox
    s.translate(V(-bb.XMin, -bb.YMin, -bb.ZMin))
    return s


# ------------------------------------------------------------------ Pruefen
def _load(brep):
    s = Part.Shape(); s.importBrep(brep); return s


def pin_fit(holder, board, holes, hole_d, pin_d, shift=0.03):
    """v3.5 (V3-04): Platine ohne Spiel auf den Stiften (um shift verschoben stoesst sie in alle 4 Richtungen an) und
    Stift mittig im Loch (Schwerpunkt der Ueberdeckung auf der Lochachse). Gibt (ok, Text) zurueck."""
    out, ok = [], True
    for (hx, hy) in holes:
        near = holder.common(cyl(hx, hy, -10.0, 90.0, hole_d + 1.0))
        hit = []
        for vec in (V(shift, 0, 0), V(-shift, 0, 0), V(0, 0, shift), V(0, 0, -shift)):
            m = board.copy(); m.translate(vec)
            hit.append(m.common(near).Volume)
        free = min(hit) <= 0.01
        ok = ok and not free
        txt = "Spiel %s" % ("JA" if free else "keins")
        if pin_d > hole_d + 1e-6:
            ov = board.common(near).Solids
            tot = sum(s.Volume for s in ov)
            if tot > 0:
                cx_ = sum(s.CenterOfMass.x * s.Volume for s in ov) / tot
                cz_ = sum(s.CenterOfMass.z * s.Volume for s in ov) / tot
                off = math.hypot(cx_ - hx, -cz_ - hy)
            else:
                off = 99.0
            ok = ok and off < 0.02
            txt += ", Mitte %.3f" % off
        out.append(txt)
    return ok, " | ".join(out)


def engraving_inside(plain, labelled, text_solid, d_face, depth):
    """v3.5: Die Gravur liegt ganz in der Flaeche (nicht ueber einem Rand oder Loch): weggenommen = Schrift im Teil."""
    removed = plain.Volume - labelled.Volume
    bb = text_solid.BoundBox
    inside = text_solid.common(Part.makeBox(bb.XLength + 2, depth, bb.ZLength + 2,
                                            V(bb.XMin - 1, d_face, bb.ZMin - 1))).Volume
    return abs(removed - inside) < 0.03 and inside > 1.0, removed, inside


def check_teile():
    box, plate = _load(BREP_BOX), _load(BREP_PLATE)
    comps = component_solids()
    keep = {k: rbox(v[0], v[2], v[1], v[3], v[4], v[5]) for k, v in P.KEEP_OUT.items()}
    bad = 0

    def line(name, ok, txt):
        nonlocal bad
        print("  %-46s %s%s" % (name, txt, "" if ok else "   <<<"))
        bad += not ok

    def hits(s, skip=(), skipk=()):
        h = [(n, s.common(c).Volume) for n, c in comps.items() if n not in skip and s.BoundBox.intersect(c.BoundBox)]
        h += [("Freiraum " + k, s.common(v).Volume) for k, v in keep.items() if k not in skipk
              and s.BoundBox.intersect(v.BoundBox)]
        return [(n, v) for n, v in h if v > 0.01]

    print("\n--- v3 Druckteile gegen Kasten, Platte, Bauteile, Freiraeume ---")
    car, tb, bb_ = carrier(), talk_board(), bell_board()
    clamp = spk_clamp()
    sp_fr, sp_body, sp_gas = speaker_solids()
    h3 = {0: radar_frame(0), 90: radar_frame(90)}
    amp, sock, lid = amp_frame(), vert_socket(), sht_lid()
    rests = plate_rests()                                       # v3.6 (V3-05)
    own = {"T1 Computer-Traeger": {"Sprechrechner", "Sprechrechner USB-Freiraum", "Klingelrechner", "RJ45-Stecker"},
           "T2 Klemmring": {"Lautsprecher", "Lautsprecher-Dichtung"}, "T3 Radar-Rahmen 0": {"Radar"},
           "T3 Radar-Rahmen 90": {"Radar"}, "T4 Verstaerker-Rahmen": {"Verstaerker", "Verstaerker-Rahmen"},
           "T5 Verteiler-Sockel": {"Verteilerplatine", "Verteiler-Sockel", "Verteiler Bauteile", "Verteiler Rand flach"},
           "T6 Kammerdeckel": {"SHT31-D"}}
    allow = {}                                                  # v3.4: Radar-Rahmen ohne Quetschrippen, also 0
    skipk = {"T1 Computer-Traeger": {"Gasse oben (hinter dem Gitterblock)"}}
    for name, s in (("T1 Computer-Traeger", car), ("T2 Klemmring", clamp), ("T3 Radar-Rahmen 0", h3[0]),
                    ("T3 Radar-Rahmen 90", h3[90]), ("T4 Verstaerker-Rahmen", amp), ("T5 Verteiler-Sockel", sock),
                    ("T6 Kammerdeckel", lid), ("T9 Plattenstuetze links", rests[0]),
                    ("T9 Plattenstuetze rechts", rests[1])):
        vb, vp = s.common(box).Volume, s.common(plate).Volume
        h = hits(s, own.get(name, ()), skipk.get(name, ()))
        ok = vb <= allow.get(name, 0.0) + 0.01 and vp < 0.01 and not h
        line(name, ok, "Kasten %.2f%s | Platte %.2f | %s" % (vb, " (Rippen)" if name in allow else "", vp,
                                                              ", ".join("%s %.2f" % x for x in h) if h else "frei"))
    # --- T1: Boards im Traeger, Antenne frei, USB frei, Schienen
    for nm, body in tb.items():
        v = car.common(body).Volume
        line("T1 Sprechrechner: %s" % nm, v < 0.01, "%.2f mm3 im Traeger (muss 0)" % v)
    T = P.TALK
    ant_zone = rbox(T["x0"] + 3.5, T["y0"] - 2.0, T["x0"] + T["w"] - 3.5, P.TALK_PCB_Y0, P.TALK_D_PCB_BACK - 2.0, DB)
    v = car.common(ant_zone).Volume
    line("T1 Antenne Sprechrechner: 2 mm frei", v < 0.01, "%.2f mm3" % v)
    v = car.common(comps["Sprechrechner USB-Freiraum"]).Volume
    line("T1 USB-C Sprechrechner: 25 mm frei", v < 0.01, "%.2f mm3" % v)
    v = car.common(bb_).Volume
    line("T1 Klingelrechner im Traeger", v < 0.01, "%.2f mm3 (muss 0)" % v)
    for dn, vec, what in (("vor", V(0, -0.4, 0), "Lippen halten nach vorn"), ("hoch", V(0, 0, 0.4), "Anschlag oben")):
        m = car.copy(); m.translate(vec)
        v = m.common(box).Volume
        line("T1 Schiene: %s" % what, v > 0.01, "%.2f mm3 bei 0.4 %s" % (v, dn))
    stop = cyl(*P.PLATE_STOP["c"], P.PLATE_Z, P.PLATE_STOP["d1"], P.PLATE_STOP["d"])
    m = car.copy(); m.translate(V(0, 0, -1.2))
    line("T1 Anschlag der Platte haelt den Traeger oben", m.common(plate).Volume > 0.01 and car.common(plate).Volume < 0.01,
         "Endlage %.2f | 1.2 tiefer %.2f mm3" % (car.common(plate).Volume, m.common(plate).Volume))
    # Ein- und Ausbauweg: erst 40 tiefer von vorn bis an die Rueckwand, dann 40 hoch. Mit Boards, gegen Kasten, Klemmring,
    # Lautsprecher, Radar-Rahmen und -Platine, Verteiler, Kammerdeckel. Platte und Display sind dabei ab.
    unit = car.fuse([tb["Platine"], tb["gelbe Leisten"], tb["lange Stifte"], tb["USB-C"], tb["Modul + Antenne"], bb_])
    glue = radar_glue()
    fixed = [("Kasten", box), ("Klemmring", clamp), ("Lautsprecher", sp_body.fuse(sp_fr)), ("Radar-Rahmen 0", h3[0]),
             ("Radar-Rahmen 90", h3[90]), ("Radar-Klebenaht", glue), ("Verteiler-Sockel", sock), ("Kammerdeckel", lid),
             ("Plattenstuetze links", rests[0]), ("Plattenstuetze rechts", rests[1])]
    fixed += [(n, c) for n, c in comps.items() if n in ("Radar", "Verteilerplatine", "Verteiler Bauteile",
                                                        "Verteiler Rand flach", "SHT31-D", "Mikrofon + Membranen",
                                                        "USB-Feld (Becher)", "Lautsprecher")]
    S_ = P.CARRIER["S"]
    for label, path in (("von vorn einsetzen", [(S_, -k) for k in range(int(P.D_BACK_IN) + 6, -1, -1)]),
                        ("hochschieben", [(S_ - k, 0.0) for k in range(0, int(S_) + 1)] + [(0.0, 0.0)])):
        worst = {}
        for (dy, dd) in path:
            m = unit.copy(); m.translate(V(0, dd, -dy))
            for n, f in fixed:
                if m.BoundBox.intersect(f.BoundBox):
                    v = m.common(f).Volume
                    if v > worst.get(n, 0.0):
                        worst[n] = v
        w = [(n, v) for n, v in worst.items() if v > 0.01]
        line("T1 Weg: %s (%d Lagen)" % (label, len(path)), not w, ", ".join("%s %.2f" % x for x in w) if w else "frei")
    # --- T1 v3.3 (V3-03): Rastknopf. Endlage: Knopf frei im Loch; 0.5 tiefer stoesst er an die steile Lochkante (haelt
    # gegen die Schwerkraft). Beim Einsetzen (S tiefer, von vorn) und beim Hochschieben laeuft er frei in der Gasse; erst
    # auf den letzten Millimetern hebt ihn die Rampe ueber den Steg (Klick).
    K_ = P.CARRIER_KNOB
    for hk in K_["heights"]:
        kn = knob_solid(hk)
        v0 = car.common(kn).Volume
        m = car.copy(); m.translate(V(0, 0, -0.5))
        v1 = m.common(kn).Volume
        line("T1 Rastknopf %.1f: frei im Loch, 0.5 tiefer haelt er" % hk, v0 < 0.01 and v1 > 0.01,
             "Endlage %.2f | 0.5 tiefer %.2f mm3" % (v0, v1))
    kn = knob_solid(max(K_["heights"]))
    w_in = 0.0
    for k in range(0, int(P.D_BACK_IN) + 7):
        m = car.copy(); m.translate(V(0, -k, -P.CARRIER["S"]))
        w_in = max(w_in, m.common(kn).Volume)
    w_up, w_click, dy = 0.0, 0.0, P.CARRIER["S"]
    dy_free = K_["y"] + K_["d"] / 2 - (P.KNOB_RAMP_Y0 + (K_["lane_t"] - max(K_["heights"])) * K_["ramp"] / K_["lane_t"])
    while dy > 0.0:
        m = car.copy(); m.translate(V(0, 0, -dy))
        v = m.common(kn).Volume
        if dy >= dy_free + 0.1:
            w_up = max(w_up, v)
        else:
            w_click = max(w_click, v)
        dy = round(dy - 0.5, 3)
    line("T1 Rastknopf: Gasse frei beim Einsetzen und Hochschieben", w_in < 0.01 and w_up < 0.01,
         "einsetzen %.2f | hochschieben bis %.1f vor Endlage %.2f mm3" % (w_in, dy_free + 0.1, w_up))
    line("T1 Rastknopf: Rampe und Steg heben den Traeger (Klick)", w_click > 0.01, "%.2f mm3 auf den letzten %.1f mm"
         % (w_click, dy_free + 0.1))
    # --- T2 Klemmring: Fuss liegt an, Druckflaechen liegen auf dem Rahmen, Haken halten die Platte
    v = clamp.common(sp_fr).Volume + clamp.common(sp_body).Volume
    line("T2 Klemmring frei von Lautsprecher", v < 0.01, "%.2f mm3" % v)
    for what, vec, other in (("Fuss auf der Blockrueckseite", V(0, -0.15, 0), box),
                             ("Druckflaechen auf dem Rahmenblech", V(0, -0.15, 0), sp_fr)):
        m = clamp.copy(); m.translate(vec)
        v = m.common(other).Volume
        line("T2 %s" % what, v > 0.01, "%.2f mm3 bei 0.15 nach vorn" % v)
    m = plate.copy(); m.translate(V(0, 0.4, 0))
    v = m.common(clamp).Volume
    line("T2 Haken halten die Plattenzungen", v > 0.01 and plate.common(clamp).Volume < 0.01,
         "Endlage %.2f | 0.4 nach hinten %.2f mm3" % (plate.common(clamp).Volume, v))
    for (x, y) in P.SPK_SCREWS:
        sc = cyl(x, y, P.CAV["d"] - P.SPK_SCREW["oring_pressed"], P.CAV["d"] - P.SPK_SCREW["oring_pressed"]
                 + P.SPK_SCREW["l"], 2.9)
        v1 = sc.common(box).Volume
        ins = cyl(x, y, P.SPK_D_FRONT + P.SPK_FRAME_T, P.SPK_D_FRONT + P.SPK_FRAME_T + P.INS["l"], 2.9)
        grip = sc.common(ins).Volume / (math.pi * 1.45 ** 2)
        line("T2 Schraube M3x%.0f (%.1f|%.1f)" % (P.SPK_SCREW["l"], x, y), v1 < 0.01 and grip >= 3.0,
             "Kasten %.2f | greift %.1f mm im Einsatz" % (v1, grip))
    # Einbau der Platte: 3.5 tiefer von vorn, dann hoch - Zungen unter Gitterblock und Haken durch (v3.6: vorbei an den
    # Plattenstuetzen, auf deren Zungen sie dabei hinten entlanggleitet)
    worst = 0.0
    for k in range(0, 23):
        m = plate.copy(); m.translate(V(0, -(22 - k), -P.PLATE_DROP))
        worst = max(worst, m.common(box).Volume + m.common(clamp).Volume + m.common(car).Volume
                    + sum(m.common(r).Volume for r in rests))
    for k in range(0, 8):
        m = plate.copy(); m.translate(V(0, 0, -P.PLATE_DROP + k * P.PLATE_DROP / 7))
        worst = max(worst, m.common(box).Volume + m.common(clamp).Volume + m.common(car).Volume
                    + sum(m.common(r).Volume for r in rests))
    line("Platte einsetzen (vorn rein, %.1f hoch)" % P.PLATE_DROP, worst < 0.01, "%.2f mm3" % worst)
    # --- T9 Plattenstuetzen (v3.6, V3-05): liegen an Wand, Kanal und Gitterblock an; die Platte liegt hinten darauf
    for nm, r, sx in (("links", rests[0], -1.0), ("rechts", rests[1], 1.0)):
        a = []
        for vec in (V(0.15 * sx, 0, 0), V(0, -0.15, 0), V(0, 0, 0.15)):      # zur Wand, nach vorn, nach oben
            m = r.copy(); m.translate(vec)
            a.append(m.common(box).Volume)
        v0 = r.common(box).Volume
        line("T9 Stuetze %s liegt an Wand, Kanal und Gitterblock an" % nm, v0 < 0.01 and min(a) > 0.01,
             "Endlage %.2f | Wand %.2f | Kanal %.2f | Gitterblock %.2f mm3" % (v0, a[0], a[1], a[2]))
        m = plate.copy(); m.translate(V(0, 0.2, 0))
        vp, vb = r.common(plate).Volume, m.common(r).Volume
        line("T9 Platte liegt hinten auf der Stuetze %s" % nm, vp < 0.01 and vb > 0.01,
             "Endlage %.2f | Platte 0.2 nach hinten %.2f mm3" % (vp, vb))
        oth = [("Klemmring", clamp), ("Traeger", car), ("Verstaerker-Rahmen", amp), ("Radar-Rahmen 0", h3[0]),
               ("Radar-Rahmen 90", h3[90]), ("Radar-Klebenaht", glue)]
        hv = [(n, r.common(s).Volume) for n, s in oth]
        hv = [(n, v) for n, v in hv if v > 0.01]
        line("T9 Stuetze %s frei von Klemmring, Traeger und Nachbarteilen" % nm, not hv,
             ", ".join("%s %.2f" % x for x in hv) if hv else "frei")
    # --- T10 Abstandsstuecke (v3.7, V3-07): Dicke, Laenge und Breite je Stueck; der gemessene Spalt liegt im Satz
    S_ = P.DISPLAY_SPACER
    th = []
    for t in S_["steps"]:
        comb, teeth = spacer_comb(t)
        bad_ = []
        for L, tooth in zip(S_["lengths"], teeth):
            bb = tooth.BoundBox
            th.append(bb.XLength)
            if abs(bb.XLength - t) > 0.005 or abs(bb.YLength - L) > 0.005 or abs(bb.ZLength - S_["w"]) > 0.005:
                bad_.append("%d mm: %.2f x %.2f x %.2f" % (L, bb.XLength, bb.YLength, bb.ZLength))
        ok = comb.isValid() and len(comb.Solids) == 1 and not bad_
        line("T10 Kamm %s: %d Stuecke %.1f dick, Laengen wie Liste" % (step_label(t), len(teeth), t), ok,
             "ein Koerper, gueltig" if ok else (", ".join(bad_) or "Koerper %d, gueltig %s"
                                                % (len(comb.Solids), comb.isValid())))
    line("T10 Spalt %.1f liegt im Satz der Dicken" % S_["gap"], min(th) - 1e-6 <= S_["gap"] <= max(th) + 1e-6,
         "Dicken %.2f..%.2f" % (min(th), max(th)))
    # --- T3 Radar-Rahmen (v3.2: Abstandsrahmen, Stiftleiste an einer Langseite, beide Seiten und beide Drehlagen)
    for rot in (0, 90):
        f = h3[rot]
        for side in (-1, 1):
            rb = radar_board(rot, side)
            nm = "T3 Radar %d Grad, Leiste %s" % (rot, "Seite A" if side < 0 else "Seite B")
            v = {k: f.common(s).Volume for k, s in rb.items()}
            line("%s: alles frei im Rahmen" % nm, max(v.values()) < 0.01, " | ".join("%s %.2f" % kv for kv in v.items()))
            vb = sum(box.common(s).Volume for s in rb.values())
            line("%s: frei vom Kasten (Loetstellen ueber dem Boden)" % nm, vb < 0.01, "%.2f mm3" % vb)
        pcb = radar_board(rot, -1)["Platine"]
        m1 = pcb.copy(); m1.translate(V(0, -0.3, 0))           # zum Taschenboden hin -> Stufe
        m2 = pcb.copy(); m2.translate(V(0, 0.3, 0))            # nach hinten -> Lippen
        v1, v2 = m1.common(f).Volume, m2.common(f).Volume
        line("T3 Radar %d Grad: Platine gefangen (Stufe vorn, Lippen hinten)" % rot, v1 > 0.01 and v2 > 0.01,
             "0.3 nach vorn %.2f | 0.3 nach hinten %.2f mm3" % (v1, v2))
        unit = radar_board(rot, -1)
        unit = unit["Platine"].fuse([unit["Bauteile"], unit["Stiftleiste"], unit["Loetstellen"]])
        go = V(0, 0, -1) if rot == 0 else V(-1, 0, 0)          # Richtung zur offenen Seite (y gross bei 0 Grad)
        worst = 0.0
        for k in range(0, 49):
            m = unit.copy(); m.translate(go * (0.5 * k))
            worst = max(worst, m.common(f).Volume)
        line("T3 Radar %d Grad: von der offenen Seite einschieben (24 mm)" % rot, worst < 0.01, "%.2f mm3" % worst)
        v = f.common(clamp).Volume
        line("T3 Radar-Rahmen %d frei vom Klemmring" % rot, v < 0.01, "%.2f mm3" % v)
        # v3.4: geklebt - geht ohne Kraft in die Tasche, liegt auf dem Taschenboden, die Klebenaht liegt an
        worst = 0.0
        for vec in (V(0.2, 0, 0), V(-0.2, 0, 0), V(0, 0, 0.2), V(0, 0, -0.2)):
            m = f.copy(); m.translate(vec)
            worst = max(worst, m.common(box).Volume)
        v = f.common(box).Volume
        line("T3 Radar-Rahmen %d: ohne Kraft in die Tasche (0.2 Luft rundum)" % rot, v < 0.01 and worst < 0.01,
             "Endlage %.2f | 0.2 verschoben %.2f mm3" % (v, worst))
        m = f.copy(); m.translate(V(0, -0.15, 0))
        v = m.common(box).Volume
        line("T3 Radar-Rahmen %d liegt auf dem Taschenboden" % rot, v > 0.01, "%.2f mm3 bei 0.15 nach vorn" % v)
        m1 = glue.copy(); m1.translate(V(0.15, 0, 0))            # linke Naht in den Rahmen
        m2 = glue.copy(); m2.translate(V(0, 0, 0.15))            # untere Naht nach oben in den Rahmen
        v1, v2 = m1.common(f).Volume, m2.common(f).Volume
        line("T3 Klebenaht liegt links und unten am Rahmen %d" % rot, v1 > 0.01 and v2 > 0.01,
             "links %.2f | unten %.2f mm3 bei 0.15" % (v1, v2))
    # v3.4: Platz fuer die Klebenaht - frei von allem ausser Kasten und Rahmen, an denen sie nur anliegt
    others = [("Kasten", box), ("Klemmring", clamp), ("Lautsprecher", sp_body.fuse(sp_fr)), ("Platte", plate),
              ("Traeger", car), ("Radar-Rahmen 0", h3[0]), ("Radar-Rahmen 90", h3[90])]
    others += [("Radar %d %s" % (r, k), s) for r in (0, 90) for side in (-1, 1) for k, s in radar_board(r, side).items()]
    hv = [(n, glue.common(s).Volume) for n, s in others]
    hv = [(n, v) for n, v in hv if v > 0.01] + hits(glue, ("Radar",))
    m = glue.copy(); m.translate(V(0, -0.15, 0))
    vb = m.common(box).Volume
    line("T3 Klebenaht %.0f x %.0f unten und links: Platz frei, liegt auf der Blockrueckseite" % (
        P.RADAR_CARRIER["glue"], P.RADAR_CARRIER["glue"]), not hv and vb > 0.01,
         "%s | Block %.2f mm3 bei 0.15 nach vorn" % (", ".join("%s %.2f" % x for x in hv) if hv else "frei", vb))
    # --- T4 Verstaerker (v3.5, V3-04): Stifte mittig in den Loechern, Satz in drei Staerken, Platine ohne Spiel
    ab, AF = amp_board(), P.AMP_FRAME
    for s_ in AF["pin_steps"]:
        ok, txt = pin_fit(amp_frame(s_), ab, P.AMP_HOLES, P.AMP["hole_d"], s_)
        line("T4 Rahmen Ø%.1f: Stifte mittig, Platine ohne Spiel (%.2f je Seite)" % (s_, (s_ - P.AMP["hole_d"]) / 2),
             ok, txt)
        t_ = engrave(step_label(s_), P.AMP["c"][0], P.AMP["c"][1], P.PLATE_Z, AF["label_h"], AF["label_t"])
        ok, rem, ins = engraving_inside(amp_frame(s_), amp_frame(s_, step_label(s_)), t_, P.PLATE_Z, AF["label_t"])
        line("T4 Rahmen Ø%.1f: Zahl ganz im Boden eingraviert" % s_, ok, "weg %.2f | Schrift %.2f mm3" % (rem, ins))
    m = ab.copy(); m.translate(V(0, -0.15, 0))
    v = m.common(amp_frame(P.AMP["hole_d"] - 0.3)).Volume
    line("T4 Platine liegt auf den Domen", v > 0.01, "%.2f mm3 bei 0.15 zum Rahmen" % v)
    m = amp.copy(); m.translate(V(0, -0.15, 0))
    line("T4 Rahmen liegt auf der Platte", m.common(plate).Volume > 0.01, "%.2f mm3" % m.common(plate).Volume)
    # --- T5 Verteiler-Sockel
    vb_ = vert_board()
    v = sock.common(vb_).Volume
    line("T5 Platine auf dem Sockel (Stifte in den Loechern)", v < 0.01, "%.2f mm3" % v)
    for what, vec in (("liegt auf den Saeulen", V(0, 0.15, 0)), ("Rastfinger halten", V(0, -0.3, 0))):
        m = vb_.copy(); m.translate(vec)
        v = m.common(sock).Volume
        line("T5 Platine %s" % what, v > 0.01, "%.2f mm3" % v)
    m = sock.copy(); m.translate(V(0, 0.15, 0))
    line("T5 Sockel liegt auf der Rueckwand", m.common(box).Volume > 0.01, "%.2f mm3" % m.common(box).Volume)
    v = sock.common(box).Volume
    line("T5 Sockel im Sitz", v < 0.01, "%.2f mm3" % v)
    # --- T6 Deckel, v3.1 mit der SHT31-Platine auf dem Stift
    m = lid.copy(); m.translate(V(0, 0.15, 0))
    line("T6 Deckel liegt auf den Kammerwaenden", m.common(box).Volume > 0.01, "%.2f mm3" % m.common(box).Volume)
    sb, SM_ = sht_board(), P.SHT_MOUNT
    for s_ in SM_["pin_steps"]:                                 # v3.5 (V3-04): Satz in drei Stiftstaerken
        ok, txt = pin_fit(sht_lid(s_), sb, [P.SHT_HOLE], P.SHT_BOARD["hole_d"], s_)
        line("T6 Deckel Ø%.1f: Stift mittig, Platine ohne Spiel (%.2f je Seite)"
             % (s_, (s_ - P.SHT_BOARD["hole_d"]) / 2), ok, txt)
        t_ = engrave(step_label(s_), SM_["label_c"][0], SM_["label_c"][1], P.SHT["d0"], SM_["label_h"], SM_["label_t"])
        ok, rem, ins = engraving_inside(sht_lid(s_), sht_lid(s_, step_label(s_)), t_, P.SHT["d0"], SM_["label_t"])
        line("T6 Deckel Ø%.1f: Zahl ganz in der Aussenseite eingraviert" % s_, ok, "weg %.2f | Schrift %.2f mm3"
             % (rem, ins))
    m = sb.copy(); m.translate(V(0, -0.15, 0))
    v = m.common(sht_lid(P.SHT_BOARD["hole_d"] - 0.3)).Volume
    line("T6 SHT31-Platine liegt auf dem Bund", v > 0.01, "%.2f mm3 bei 0.15 zum Deckel" % v)
    hx, hy = P.SHT_HOLE
    tilt = []
    for a in (3.0, -3.0):                                       # die Richtung, in der die Platine unter ihrem Gewicht kippt
        m = sb.copy(); m.rotate(pt(hx, hy, 0.0), V(0, 1, 0), a)
        tilt.append((m.BoundBox.ZMin, a, m))
    _, a, m = min(tilt, key=lambda t: t[0])                     # tiefster Punkt sinkt (Z = -y)
    v = m.common(sht_rib()).Volume
    line("T6 Rippe haelt die Platine gegen Verdrehen", v > 0.01, "%.2f mm3 bei %.0f Grad gekippt" % (v, abs(a)))
    plain = sht_lid_plate().fuse(sht_rib())
    env = comps["SHT31-D"]
    v1, v2 = env.common(box).Volume, env.common(plain).Volume
    line("T6 Bauteil-Huelle (1.7 beidseitig) frei", v1 < 0.01 and v2 < 0.01, "Kasten %.2f | Deckel %.2f mm3" % (v1, v2))
    unit = lid.fuse([sb, env])                                  # mit der Bauteil-Huelle, beidseitig
    worst, n = 0.0, int(math.ceil(P.SHT_LID_TRAVEL / 0.5))
    for k in range(0, n + 1):
        m = unit.copy(); m.translate(V(0, -P.SHT_LID_TRAVEL * k / n, 0))
        worst = max(worst, m.common(box).Volume)
    line("T6 Deckel mit Platine gerade auf die Kammer", worst < 0.01, "%.2f mm3 auf den letzten %.1f mm"
         % (worst, P.SHT_LID_TRAVEL))
    # --- T7 Druckstifte: in der Tasche der Platte, Spitze geht durch das Platinenloch
    pcb = rbox(P.DISPLAY_GLASS["x0"], P.DISPLAY_GLASS["y0"], P.DISPLAY_GLASS["x1"], P.DISPLAY_GLASS["y1"],
               P.DISPLAY_PCB_BACK - P.DISPLAY_PCB_T, P.DISPLAY_PCB_BACK).cut(
        [cyl(x, y, 0, 10, 3.94) for (x, y) in P.DISPLAY_PINS])
    for fd in P.DISPLAY_PIN_FRONTS:
        ps = display_pins(fd)
        vp = sum(p_.common(plate).Volume for p_ in ps)
        vb2 = sum(p_.common(box).Volume for p_ in ps)
        vpc = sum(p_.common(pcb).Volume for p_ in ps)
        line("T7 Stifte Stirn d %.1f (%s)" % (fd, ("-%.1f" % (fd - P.DISPLAY_PIN["v2_front"])).replace(".", ",")),
             vp < 0.01 and vb2 < 0.01 and vpc < 0.01, "Platte %.2f | Kasten %.2f | Platine %.2f mm3" % (vp, vb2, vpc))
    print("TEILE-PRUEFUNG v3: %s" % ("BESTANDEN" if bad == 0 else "%d FEHLER" % bad))
    return bad
