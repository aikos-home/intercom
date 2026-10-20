"""USB-Feld v3: wie v1 (Einsatz von unten mit 3 USB-C-Breakouts + Abdeckung mit Sicherheitsschrauben). Neu ist nur der
groessere Ausschnitt der Abdeckung fuer die teilbare M20-Verschraubung (v3). Masse aus v3_params.py, Kasten aus v3_kasten.

    exec(open(r"hardware\\v3\\cad\\v3_usb.py", encoding="utf-8").read())
    check_usb()

Ablauf (Bauherr): Litzen an V-frei/D-/D+/G loeten, Breakouts von unten in die Schlitze der Einsatzplatte stecken (Blende
liegt aussen auf, ein Ring Silikon darunter, damit kein Harz durchlaeuft), Becher auf dem Tisch vergiessen. Danach den
Einsatz mit Silikon von unten in die Bodenoeffnung setzen; die Abdeckung (2 x M3 Torx-Pin in Einsaetze im Kastenboden)
drueckt ihn an und deckt die Buchsen ab.
"""
import os as _os
# Paths (public copy): everything relative to this folder, outputs into out/ (gitignored).
V3_DIR = globals().get("V3_DIR") or _os.environ.get("KLINGELBOX_V3_DIR") or _os.path.dirname(_os.path.abspath(__file__))
_os.environ.setdefault("KLINGELBOX_V3_DIR", V3_DIR)
for _d in ("out", _os.path.join("out", "print", "metall")):
    _os.makedirs(_os.path.join(V3_DIR, _d), exist_ok=True)
exec(open(_os.path.join(V3_DIR, "v3_kasten.py"), encoding="utf-8").read())

USB_DIR = _os.path.join(V3_DIR, "out", "print")
U, UB = P.USB_FIELD, P.USB_BREAKOUT
Y_BOT = B["y1"]                                  # Aussenseite des Kastenbodens
Y_PL = Y_BOT + U["plate_t"]                      # Unterseite der Einsatzplatte = Rueckseite der Blenden
Y_FL = Y_PL + UB["flange_t"]                     # Vorderseite der Blenden = Buchsenoeffnung
Y_CO = Y_FL + 0.3 + U["cover_t"]                 # Unterseite der Abdeckung
GLAND_R = P.GLAND["body_d"] / 2                  # v3: teilbare M20-Verschraubung aussen, SW30 ueber Eck 33.5


def breakouts():
    """Die 3 Breakouts als Koerper: Blende (aussen), Buchse, Platine (senkrecht nach oben in den Becher)."""
    out = []
    d0 = U["d_c"]
    for xc in P.USB_XS:
        fl = rbox(xc - UB["flange_h"] / 2, Y_PL, xc + UB["flange_h"] / 2, Y_FL, d0 - UB["flange_l"] / 2,
                  d0 + UB["flange_l"] / 2)
        port = rbox(xc - P.USB_PORT_T / 2, Y_FL - UB["port_l"], xc + P.USB_PORT_T / 2, Y_FL,
                    d0 - UB["port_w"] / 2, d0 + UB["port_w"] / 2)
        pcb = rbox(xc - P.USB_PORT_T / 2 - UB["pcb_t"], Y_PL - UB["pcb_l"], xc - P.USB_PORT_T / 2, Y_PL,
                   d0 - UB["pcb_w"] / 2, d0 + UB["pcb_w"] / 2)
        out.append(fl.fuse([port, pcb]).removeSplitter())
    return out


def _gland_cut(y0, y1):
    return ycyl(P.GLAND["c"][0], P.GLAND["c"][1], y0, y1, 2 * U["gland_r"])


def usb_insert():
    """Einsatzplatte (aussen am Boden) + Vergussbecher (durch die Bodenoeffnung nach innen) + 3 Schlitze."""
    px0, px1, pd0, pd1 = P.USB_PLATE
    cx0, cx1, cd0, cd1, ytop = P.USB_CUP
    w = U["wall"]
    plate = rbox(px0, Y_BOT, px1, Y_PL, pd0, pd1).cut(_gland_cut(Y_BOT - 1.0, Y_PL + 1.0))
    cup = rbox(cx0, ytop, cx1, Y_BOT + 0.01, cd0, cd1).cut(
        rbox(cx0 + w, ytop - 1.0, cx1 - w, Y_BOT + 0.02, cd0 + w, cd1 - w))
    s = plate.fuse(cup)
    slots = []
    for xc in P.USB_XS:
        slots.append(rbox(xc - P.USB_PORT_T / 2 - UB["pcb_t"] - U["play"], Y_BOT - 0.5, xc + P.USB_PORT_T / 2 + U["play"],
                          Y_PL + 0.5, U["d_c"] - UB["pcb_w"] / 2 - U["play"], U["d_c"] + UB["pcb_w"] / 2 + U["play"]))
    return s.cut(slots).removeSplitter()


def usb_cover():
    """Abdeckung: liegt links/hinten am Kastenboden an, umfasst die Einsatzplatte und deckt die Buchsen ab."""
    px0, px1, pd0, pd1 = P.USB_PLATE
    c = rbox(U["cover_x0"], Y_BOT, px1, Y_CO, pd0, U["cover_d1"]).cut(_gland_cut(Y_BOT - 1.0, Y_CO + 1.0))
    cuts = [rbox(px0 - 0.2, Y_BOT - 1.0, px1 + 1.0, Y_PL, pd0 - 1.0, pd1 + 0.2)]            # Platz fuer die Platte
    for xc in P.USB_XS:                                                                    # Tasche fuer die Blenden
        cuts.append(rbox(xc - UB["flange_h"] / 2 - 0.3, Y_PL - 0.1, xc + UB["flange_h"] / 2 + 0.3, Y_FL + 0.3,
                         U["d_c"] - UB["flange_l"] / 2 - 0.3, U["d_c"] + UB["flange_l"] / 2 + 0.3))
    for (x, d) in U["screws"]:                                                             # Schraube + Kopfsenkung
        cuts.append(ycyl(x, d, Y_BOT - 1.0, Y_CO + 1.0, 3.4))
        cuts.append(ycyl(x, d, Y_CO - 2.0, Y_CO + 1.0, 6.4))
    # Ablauf unter jeder Buchse: Die Plattentasche ist rechts und vorn zum Rand offen (Spalte 0.2), dort kann Wasser
    # hineinkriechen. Ohne Loch bliebe es in der Blendentasche stehen, direkt an der Buchse.
    for xc in P.USB_XS:
        cuts.append(ycyl(xc, U["d_c"], Y_FL, Y_CO + 1.0, U["drain_d"]))
    return c.cut(cuts).removeSplitter()


def check_usb():
    box = Part.Shape(); box.importBrep(BREP_BOX)
    ins, cov, bos = usb_insert(), usb_cover(), breakouts()
    comps, wires = component_solids(), [("LAN-Kabel", 8, lan_cable())]     # v3: Leitungen nur noch als Gassen
    keep = {k: rbox(v[0], v[2], v[1], v[3], v[4], v[5]) for k, v in P.KEEP_OUT.items()}
    gland = ycyl(P.GLAND["c"][0], P.GLAND["c"][1], Y_BOT, Y_BOT + 30.0, 2 * GLAND_R)
    bad = 0
    print("\n--- USB-Feld v3 ---")

    def line(name, pairs):
        nonlocal bad
        hits = [(n, v) for n, v in pairs if v > 0.01]
        print("  %-30s %s" % (name, ", ".join("%s %.2f" % h for h in hits) if hits else "frei"))
        bad += bool(hits)

    usb_wires = {wn for wn, n, w in wires if wn.startswith("USB")}
    for name, s in (("Einsatz", ins), ("Abdeckung", cov)):
        pairs = [("Kasten", s.common(box).Volume)]
        pairs += [(n, s.common(c).Volume) for n, c in comps.items() if not n.startswith("USB")]
        pairs += [("Leitung " + wn, s.common(w).Volume) for wn, n, w in wires if wn not in usb_wires]
        pairs += [("Freiraum " + k, s.common(v).Volume) for k, v in keep.items()]
        pairs += [("Verschraubung aussen", s.common(gland).Volume)]
        line(name, pairs)
    for i, b in enumerate(bos):
        pairs = [("Kasten", b.common(box).Volume), ("Einsatz", b.common(ins).Volume), ("Abdeckung", b.common(cov).Volume)]
        pairs += [(n, b.common(c).Volume) for n, c in comps.items() if not n.startswith("USB")]
        line("Breakout %d (x %.1f)" % (i + 1, P.USB_XS[i]), pairs)
    line("Einsatz gegen Abdeckung", [("Abdeckung", ins.common(cov).Volume)])
    # Anlage: Platte liegt am Kastenboden an, Abdeckung am Kastenboden und an der Platte
    for name, s, v_ in (("Platte am Kastenboden", ins, V(0, 0, 0.15)), ("Abdeckung am Kastenboden", cov, V(0, 0, 0.15))):
        m = s.copy(); m.translate(v_)
        v = m.common(box).Volume
        print("  %-30s %s" % (name, "liegt an" if v > 0.01 else "LUFT <<<")); bad += v <= 0.01
    m = cov.copy(); m.translate(V(0, 0, 0.15))
    v = m.common(ins).Volume
    print("  %-30s %s" % ("Abdeckung drueckt die Platte", "ja" if v > 0.01 else "LUFT <<<")); bad += v <= 0.01
    # Harz: jede Platine steckt mit >= 1 mm Harz rundum im Becher (Becherinneres minus Platinen)
    cx0, cx1, cd0, cd1, ytop = P.USB_CUP
    inner = rbox(cx0 + U["wall"], ytop, cx1 - U["wall"], Y_BOT, cd0 + U["wall"], cd1 - U["wall"])
    for i, b in enumerate(bos):
        pcb_in = b.common(rbox(0, ytop - 5.0, 100, Y_BOT, 0, 60))
        q = pcb_in.common(inner).Volume / pcb_in.Volume
        print("  %-30s %5.1f%% im Becher, Becherrand %.1f ueber der Platine %s"
              % ("Platine %d im Verguss" % (i + 1), 100 * q, (Y_PL - UB["pcb_l"]) - ytop, "" if q > 0.999 else "<<<"))
        bad += q <= 0.999
    for (x, d) in U["screws"]:                                # Kopfsenkung rundum mit >= 1 mm Rand in der Abdeckung
        ann = ycyl(x, d, Y_CO - 1.9, Y_CO - 0.1, 8.4).cut(ycyl(x, d, Y_CO - 2.0, Y_CO, 6.4))
        q = cov.common(ann).Volume / ann.Volume
        print("  %-30s %5.1f%% Material im 1-mm-Ring %s" % ("Senkung (%.1f|%.1f)" % (x, d), 100 * q,
                                                            "" if q > 0.995 else "<<< RAND"))
        bad += q <= 0.995
    for i, xc in enumerate(P.USB_XS):                         # Ablauf: freier Weg vom Taschenboden nach aussen
        probe = ycyl(xc, U["d_c"], Y_FL + 0.35, Y_CO + 0.5, U["drain_d"] - 0.4)
        v = cov.common(probe).Volume
        print("  %-30s %s" % ("Ablauf unter Buchse %d" % (i + 1), "frei" if v < 0.001 else "ZU <<<"))
        bad += v >= 0.001
    print("USB-PRUEFUNG: %s" % ("BESTANDEN" if bad == 0 else "%d FEHLER" % bad))
    return bad


def export_usb(dev=0.02):
    import Mesh
    os.makedirs(USB_DIR, exist_ok=True)
    out = []
    for name, s in (("U1_usb_einsatz.stl", usb_insert()), ("U2_usb_abdeckung.stl", usb_cover())):
        r = s.copy()                                               # CAD-Z = -y: Aussenseite liegt schon unten (Bett)
        bb = r.BoundBox; r.translate(V(-bb.XMin, -bb.YMin, -bb.ZMin))
        Mesh.Mesh(r.tessellate(dev)).write(os.path.join(USB_DIR, name))
        bb = r.BoundBox
        print("  %-24s %5.1f x %5.1f x %5.1f mm | %.1f g | valid %s" % (name, bb.XLength, bb.YLength, bb.ZLength,
                                                                       r.Volume * 1.27e-3, r.isValid()))
        out.append(name)
    return out
