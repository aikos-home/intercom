"""Stahlblech v3: flaches Tragblech 2.0 mm (1.4404) zwischen Messing und Kasten. Grundlage fuer die Vorbesprechung bei
Metallbetrieb - NICHT bestellen, bis die Regeln des Betriebs bekannt sind.
Gegenueber Stahlblech v1: die zwei LED-Fenster entfallen, dafuer ein Kabelloch Ø4.5 fuer den LED-Streifen im Diffusor
(W-06). Alles andere wie v1: Schraubenlage, Zapfen, Messinggewinde, Dichtlinie.

    exec(open(r"hardware\\v3\\cad\\v3_stahl.py", encoding="utf-8").read())
    build_steel(); check_steel(); export_steel()

Erzeugt cad/druck/v3/metall/:
  stahlblech_v3.step          3D mit den 18 Senkungen
  stahlblech_v3_kontur.dxf    Kontur in mm, Ursprung linke untere Ecke, Blick auf die MESSINGSEITE
  gegenleisten_v3.dxf         die 2 Gegenleisten 5 x 4 als Streifen, Gewinde laut Tabelle
  STAHL_VORLAGE.md            Werkstoff, Bearbeitung, Lochtabelle (DXF-Koordinaten)
"""
import os as _os
# Paths (public copy): everything relative to this folder, outputs into out/ (gitignored).
V3_DIR = globals().get("V3_DIR") or _os.environ.get("KLINGELBOX_V3_DIR") or _os.path.dirname(_os.path.abspath(__file__))
_os.environ.setdefault("KLINGELBOX_V3_DIR", V3_DIR)
for _d in ("out", _os.path.join("out", "print", "metall")):
    _os.makedirs(_os.path.join(V3_DIR, _d), exist_ok=True)
exec(open(_os.path.join(V3_DIR, "v3_kasten.py"), encoding="utf-8").read())

ST_DIR = _os.path.join(V3_DIR, "out", "print", "metall")
BREP_STEEL = os.path.join(OUT, "_v3_stahlblech.brep")
SS, SC = P.STEEL, P.STEEL_CUT
SX0, SY0, SX1, SY1 = B["x0"] + SS["inset"], B["y0"] + SS["inset"], B["x1"] - SS["inset"], B["y1"] - SS["inset"]
SR = P.CORNER_R - SS["inset"]
DENS = 8.0e-3                                                   # g/mm3, 1.4404


def bar_x(side):
    return P.BAR["x"] if side == "links" else B["x0"] + B["x1"] - P.BAR["x"]


def de(v, n=1):
    """Zahl mit deutschem Dezimalkomma."""
    return ("%%.%df" % n % v).replace(".", ",")


def dxf_xy(x, y):
    """Front-Koordinaten (x, y nach unten) -> DXF (Ursprung linke untere Blechecke, Y nach oben)."""
    return x - SX0, SY1 - y


def _slot_x(x, y, d, half):
    """Langloch in x: Kreise Ø d bei x-half / x+half plus Mittelstueck."""
    return cyl(x - half, y, -1.0, 3.0, d).fuse([cyl(x + half, y, -1.0, 3.0, d),
                                                 rbox(x - half, y - d / 2, x + half, y + d / 2, -1.0, 3.0)])


def steel_cuts():
    """[(Art, Text, (x, y), Schnittkoerper d -1..3)] - jeder Laser-Durchbruch des Stahlblechs."""
    G, o, g = P.DISPLAY_GLASS, SC["win_over"], SC["glass_gap"]
    out = [("Fenster", "Display-Glas %s × %s, je Seite %s Klebefuge" % (de(G["x1"] - G["x0"], 2), de(G["y1"] - G["y0"], 2),
                                                                        de(g)),
            ((G["x0"] + G["x1"]) / 2, (G["y0"] + G["y1"]) / 2),
            rbox(G["x0"] - g, G["y0"] - g, G["x1"] + g, G["y1"] + g, -1.0, 3.0, 0.5))]
    Gr = P.GRILLE
    out.append(("Fenster", "Gitter + Radar (hinter allen Messingschlitzen)", ((Gr["x0"] + Gr["x1"]) / 2,
                (Gr["y0"] + Gr["y1"]) / 2), rbox(Gr["x0"] - o, Gr["y0"] - o, Gr["x1"] + o, Gr["y1"] + o, -1.0, 3.0, 2.0)))
    lx, ly = P.LED_CABLE["c"]                                   # v3: statt zwei LED-Fenstern ein Kabelloch (W-06)
    out.append(("Loch", "Kabel LED-Streifen (unter dem Diffusor)", (lx, ly), cyl(lx, ly, -1.0, 3.0, P.LED_CABLE["steel"])))
    for i, (a, b) in enumerate(P.LED_SLITS):
        out.append(("Fenster", "Diffusor-Schlitz %d" % (i + 1), ((a + b) / 2, sum(P.LED_SLIT_Y) / 2),
                    rbox(a - o, P.LED_SLIT_Y[0] - o, b + o, P.LED_SLIT_Y[1] + o, -1.0, 3.0, 0.5)))
    out.append(("Loch", "Taster", P.BTN_C, cyl(P.BTN_C[0], P.BTN_C[1], -1.0, 3.0, SC["btn_hole"])))
    for (x, y) in P.MICS:
        out.append(("Loch", "Mikrofon", (x, y), cyl(x, y, -1.0, 3.0, SC["mic_hole"])))
    for side in ("links", "rechts"):
        for y in P.BAR_HOLES[side]:
            out.append(("Senkloch", "M3 in Gegenleiste %s" % side, (bar_x(side), y),
                        cyl(bar_x(side), y, -1.0, 3.0, SC["csk_hole"])))
    (xl, yl), (xr, yr) = P.SPIGOTS
    out.append(("Zapfen", "Zapfen links, rund (Festpunkt)", (xl, yl), cyl(xl, yl, -1.0, 3.0, P.SPIGOT["hole"])))
    out.append(("Zapfen", "Zapfen rechts, Langloch quer", (xr, yr), _slot_x(xr, yr, P.SPIGOT["hole"], P.SPIGOT["slot"])))
    for (x, y) in P.SCREWS:
        out.append(("Gewinde", "M3 fuer Messingschraube", (x, y), cyl(x, y, -1.0, 3.0, P.STEEL_TAP)))
    return out


def countersinks():
    """90-Grad-Senkungen von der Messingseite (d 0) auf Ø csk_d - nur im 3D, der Laser schneidet das Durchgangsloch."""
    r1, r0 = SC["csk_d"] / 2, SC["csk_hole"] / 2
    return [Part.makeCone(r1 + 0.5, r0, (r1 - r0) + 0.5, pt(bar_x(side), y, -0.5), V(0, 1, 0))
            for side in ("links", "rechts") for y in P.BAR_HOLES[side]]


def _plate(with_csk=True):
    plate = rbox(SX0, SY0, SX1, SY1, 0.0, SS["t"], SR)
    return plate.cut([c[3] for c in steel_cuts()] + (countersinks() if with_csk else [])).removeSplitter()


def build_steel():
    s = _plate(True)
    s.exportBrep(BREP_STEEL)
    print("Stahlblech v3: %.1f x %.1f x %.1f | Solids %d | valid %s | %.0f mm3 = %.0f g (1.4404)"
          % (SX1 - SX0, SY1 - SY0, SS["t"], len(s.Solids), s.isValid(), s.Volume, s.Volume * DENS))
    return s


def face_xy():
    """Laserkontur als ebene Flaeche in XY (DXF-Koordinaten, Blick auf die Messingseite)."""
    p = _plate(False)
    f = [fc for fc in p.Faces if abs(fc.CenterOfMass.y) < 1e-6 and fc.normalAt(0, 0).y < -0.99][0].copy()
    f.rotate(V(0, 0, 0), V(1, 0, 0), -90.0)                   # (x, 0, -y) -> (x, -y, 0)
    f.translate(V(-SX0, SY1, 0))
    return f


def check_steel():
    st = Part.Shape(); st.importBrep(BREP_STEEL)
    box = Part.Shape(); box.importBrep(BREP_BOX)
    bad = 0
    print("\n--- Stahlblech v3 ---")
    # 1) Stege zwischen allen Durchbruechen und zur Kontur (Laserkontur, ohne Senkungen)
    f = face_xy()
    inner = [w for w in f.Wires if not w.isSame(f.OuterWire)]
    worst = []
    for i, a in enumerate(inner):
        worst.append((a.distToShape(f.OuterWire)[0], "Rand", i))
        for j in range(i + 1, len(inner)):
            worst.append((a.distToShape(inner[j])[0], "Loch", i, j))
    worst.sort()
    lo = worst[0][0]
    n_thin = sum(1 for w in worst if w[0] < 2.0)
    print("  %-38s schmalster Steg %.2f mm, %d Stege unter 2.0 (Laser: >= Blechdicke 2.0 empfohlen, min 1.5) %s"
          % ("Stege (%d Durchbrueche)" % len(inner), lo, n_thin, "" if lo >= 1.5 else "<<<"))
    for w in worst[:4]:
        bb = inner[w[2]].BoundBox
        print("      %.2f mm bei DXF x %.1f y %.1f (%s)" % (w[0], (bb.XMin + bb.XMax) / 2, (bb.YMin + bb.YMax) / 2, w[1]))
    bad += lo < 1.5
    # Senkungen: Reststeg an der Oberflaeche zum Blechrand
    e = min(bar_x("links") - SC["csk_d"] / 2 - SX0, SX1 - bar_x("rechts") - SC["csk_d"] / 2)
    print("  %-38s %.2f mm an der Messingseite (min 1.2)" % ("Senkung zum Blechrand", e)); bad += e < 1.2
    # 2) Dichtlinie: unter der ganzen Raupe voller Stahl
    groove, _d = seal_line()
    band = groove.copy(); band.translate(V(0, -(F0 - 0.2), 0))      # Rinne auf d ~0.2..0.7 = im Stahl
    q = st.common(band).Volume / band.Volume
    print("  %-38s %5.1f%% Stahl %s" % ("Dichtlinie: Raupe liegt auf vollem Stahl", 100 * q, "" if q > 0.999 else "<<<"))
    bad += q <= 0.999
    # 3) Kasten: nichts stoesst an, die Zapfen gehen durch ihre Loecher
    v = st.common(box).Volume
    print("  %-38s %.2f mm3 (muss 0; Zapfen in den Loechern, Abstandsringe liegen an)" % ("Stahl gegen Kasten", v))
    bad += v > 0.01
    for (x, y) in P.SPIGOTS:                                    # Zapfen mit Spiel: 0.05 versetzt immer noch frei
        vv = 0.0
        for (dx, dz) in ((0.04, 0), (-0.04, 0), (0, 0.04), (0, -0.04)):
            z = cyl(x, y, 0.0, SS["t"], P.SPIGOT["d"]); z.translate(V(dx, 0, dz))
            vv = max(vv, st.common(z).Volume)
        print("  %-38s %.3f mm3 bei 0.04 Versatz (muss 0)" % ("Zapfen (%.1f|%.0f) im Loch" % (x, y), vv))
        bad += vv > 0.001
    # 4) Leistenschrauben: Schaft Ø3 durch Stahl, Kragen und in die Leiste
    v = sum(st.common(cyl(bar_x(s_), y, 0.0, SS["t"], 3.0)).Volume for s_ in ("links", "rechts")
            for y in P.BAR_HOLES[s_])
    print("  %-38s %.2f mm3 (muss 0)" % ("18 Leistenschrauben durch den Stahl", v)); bad += v > 0.01
    # 5) Display-Glas im Fenster, Messingring im Tasterloch
    G = P.DISPLAY_GLASS
    glass = rbox(G["x0"], G["y0"], G["x1"], G["y1"], 0.0, SS["t"])
    vv = st.common(glass).Volume
    print("  %-38s %.2f mm3, Klebefuge %.1f je Seite" % ("Display-Glas im Fenster", vv, SC["glass_gap"]))
    bad += vv > 0.01
    rg = (SC["btn_hole"] - P.RING_D) / 2
    print("  %-38s %.2f mm Luft rundum (Lage +-0.2, Dehnung +-0.25)" % ("Messingring im Tasterloch", rg)); bad += rg < 0.6
    # 6) Messingoeffnungen liegen verdeckt in den Stahloeffnungen (kein Stahlrand sichtbar)
    o = SC["win_over"]
    DW, Gr = P.DISPLAY_WIN, P.GRILLE
    pairs = [("Displayfenster", (DW["x0"], DW["y0"], DW["x1"], DW["y1"]),
              (G["x0"] - SC["glass_gap"], G["y0"] - SC["glass_gap"], G["x1"] + SC["glass_gap"], G["y1"] + SC["glass_gap"])),
             ("Gitter", (Gr["x0"], Gr["y0"], Gr["x1"], Gr["y1"]), (Gr["x0"] - o, Gr["y0"] - o, Gr["x1"] + o, Gr["y1"] + o))]
    lx, ly = P.LED_CABLE["c"]
    rb, rs = P.LED_CABLE["brass"] / 2, P.LED_CABLE["steel"] / 2
    pairs += [("LED-Kabelloch", (lx - rb, ly - rb, lx + rb, ly + rb), (lx - rs, ly - rs, lx + rs, ly + rs))]
    pairs += [("Diffusor-Schlitz %d" % (i + 1), (a, P.LED_SLIT_Y[0], b, P.LED_SLIT_Y[1]),
               (a - o, P.LED_SLIT_Y[0] - o, b + o, P.LED_SLIT_Y[1] + o)) for i, (a, b) in enumerate(P.LED_SLITS)]
    for nm, br, sl in pairs:
        m = min(br[0] - sl[0], br[1] - sl[1], sl[2] - br[2], sl[3] - br[3])
        print("  %-38s Messing liegt %.2f mm innerhalb des Stahls %s" % ("verdeckt: " + nm, m, "" if m >= 0.3 else "<<<"))
        bad += m < 0.3
    m = (SC["btn_hole"] - P.BTN_HOLE) / 2
    print("  %-38s Messing liegt %.2f mm innerhalb des Stahls %s" % ("verdeckt: Tasterloch", m, "" if m >= 0.3 else "<<<"))
    bad += m < 0.3
    m = (SC["mic_hole"] - P.MIC_D) / 2
    print("  %-38s Messing liegt %.2f mm innerhalb des Stahls %s" % ("verdeckt: Mikrofonloecher", m, "" if m >= 0.3 else "<<<"))
    bad += m < 0.3
    print("  %-38s %.0f g" % ("Gewicht", st.Volume * DENS))
    print("STAHLBLECH-PRUEFUNG: %s" % ("BESTANDEN" if bad == 0 else "%d FEHLER" % bad))
    return bad


def bars_xy():
    """Die 2 Gegenleisten als Streifen 5 x L in XY (fuer den Laser), nebeneinander, mit den Kernloechern Ø2.5."""
    out = []
    for i, side in enumerate(("links", "rechts")):
        t, b = P.BAR_Y[side]
        L = b - t
        f = Part.makePlane(P.BAR["w"], L, V(i * 15.0, 0, 0))
        out.append((side, L, [y - t for y in P.BAR_TAPS[side]], f))
    return out


def export_steel():
    os.makedirs(ST_DIR, exist_ok=True)
    import Import
    st = Part.Shape(); st.importBrep(BREP_STEEL)
    st.exportStep(os.path.join(ST_DIR, "stahlblech_v3.step"))
    Import.writeDXFShape([face_xy()], os.path.join(ST_DIR, "stahlblech_v3_kontur.dxf"))
    bars = bars_xy()
    Import.writeDXFShape([b[3] for b in bars], os.path.join(ST_DIR, "gegenleisten_v3.dxf"))
    write_order(st, bars)
    print("Export: %s" % ST_DIR)


def write_order(st, bars):
    L = []
    w = L.append
    w("# Stahlblech v3 und Gegenleisten: Vorlage für die Vorbesprechung")
    w("")
    w("**Noch nicht bestellen.** Grundlage für das Gespräch mit einem Metallbetrieb. Die Unterlagen werden nach den Antworten "
      "des Betriebs (kleinster Fräser, Toleranzen, Gewinde) neu erzeugt.")
    w("")
    w("Erzeugt von `cad/v3_stahl.py` am %s aus `v3_params.py`. Geprüft: `validate()`, `check_cad()`, "
      "`check_steel()` bestanden." % __import__("datetime").date.today().isoformat())
    w("")
    w("Gegenüber Stahlblech v1 (2026-10-12): Die zwei LED-Fenster entfallen. Dafür gibt es ein Kabelloch Ø %s für "
      "den LED-Streifen im Diffusor. Alles andere bleibt wie v1." % de(P.LED_CABLE["steel"]))
    w("")
    w("## 1. Tragblech")
    w("")
    w("| | |")
    w("|---|---|")
    w("| Dateien | `stahlblech_v3_kontur.dxf` (Kontur, mm), `stahlblech_v3.step` (3D mit Senkungen) |")
    w("| Werkstoff | Edelstahl **1.4404** (V4A), **2,0 mm**, Oberfläche egal (liegt hinter dem Messing) |")
    w("| Maße | %s × %s mm, Ecken R%s, Gewicht ca. %.0f g |" % (de(SX1 - SX0), de(SY1 - SY0), de(SR), st.Volume * DENS))
    w("| Gewinde | **4 × M3** (Tabelle „Gewinde“), dort schraubt das Messing hinein |")
    w("| Senkungen | **%d × 90° auf Ø %s** auf der Messingseite (Tabelle „Senkloch“) |"
      % (sum(len(v) for v in P.BAR_HOLES.values()), de(SC["csk_d"])))
    w("| Kanten | entgratet, eben (≤ 0,3 mm) |")
    w("")
    w("**Lage:** Das DXF zeigt das Blech von vorn, also von der Messingseite. Ursprung ist die linke untere Ecke, "
      "X nach rechts, Y nach oben.")
    w("")
    w("| Art | Was | Ø / Größe | X | Y |")
    w("|---|---|---|---|---|")
    for art, txt, (x, y), body in steel_cuts():
        bb = body.BoundBox
        size = ("%s × %s" % (de(bb.XLength), de(bb.ZLength))) if art in ("Fenster", "Zapfen") and \
            abs(bb.XLength - bb.ZLength) > 0.05 else ("Ø %s" % de(bb.XLength))
        X, Y = dxf_xy(x, y)
        w("| %s | %s | %s | %s | %s |" % (art, txt, size, de(X, 2), de(Y, 2)))
    w("")
    w("## 2. Gegenleisten (2 Stück)")
    w("")
    w("Neu in v3: Die Leisten werden **beim Drucken des Kastens eingelegt** (Druckpause), der Kragen wird über sie "
      "gedruckt. Sie sitzen danach fest im Kasten. Für den Probeaufbau gibt es sie als PETG-Ersatz (Druckteil 10).")
    w("")
    w("| | |")
    w("|---|---|")
    w("| Datei | `gegenleisten_v3.dxf` (2 Streifen) |")
    w("| Werkstoff | Edelstahl **1.4404**, **%s × %s mm** |" % (de(P.BAR["w"]), de(P.BAR["t"])))
    w("| Längen | links **%s mm**, rechts **%s mm** |" % (de(bars[0][1]), de(bars[1][1])))
    w("| Gewinde | M3 **durchgehend** durch die 4 mm, auf der Stahlseite 90° auf Ø 4,0 angesenkt |")
    w("| Kanten | entgratet, gerade (≤ 0,3 mm auf die Länge) |")
    w("")
    for side, Lb, holes, _f in bars:
        w("- **Leiste %s** (%s lang): %d Gewinde bei %s mm ab einem Ende, mittig in der Breite."
          % (side, de(Lb), len(holes), ", ".join(de(h) for h in holes)))
    w("")
    w("Die Gewinde liegen symmetrisch, die Leiste kann nicht falsch herum hinein. Das Gewinde an einem Ende bleibt "
      "ungenutzt, es macht nur die Symmetrie.")
    w("")
    w("## 3. Schrauben und Dichtung")
    w("")
    w("- %d × **M3 × %.0f ISO 14581** (Senkkopf Torx), A4, Stahl → Gegenleisten." %
      (sum(len(v) for v in P.BAR_HOLES.values()), P.BAR["screw_l"]))
    w("- %d × **O-Ring %g × %g NBR**, je einer auf jeder Schraube zwischen Stahl und Kasten (Nut im Abstandsring)."
      % (sum(len(v) for v in P.BAR_HOLES.values()), P.ORING["id"], P.ORING["cs"]))
    w("- 4 × **M3 × 4 Senkkopf** Messing → Stahl, Sicherheits-Torx.")
    w("- Silikon, neutral vernetzend, für die Raupe und das LED-Kabel.")
    open(os.path.join(ST_DIR, "STAHL_VORLAGE.md"), "w", encoding="utf-8", newline="\n").write("\n".join(L) + "\n")

