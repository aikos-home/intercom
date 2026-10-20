# Stahlblech v3 und Gegenleisten: Vorlage für die Vorbesprechung

**Noch nicht bestellen.** Grundlage für das Gespräch mit einem Metallbetrieb. Die Unterlagen werden nach den Antworten des Betriebs (kleinster Fräser, Toleranzen, Gewinde) neu erzeugt.

Erzeugt von `cad/v3_stahl.py` am 2026-10-20 aus `v3_params.py`. Geprüft: `validate()`, `check_cad()`, `check_steel()` bestanden.

Gegenüber Stahlblech v1 (2026-10-12): Die zwei LED-Fenster entfallen. Dafür gibt es ein Kabelloch Ø 4,5 für den LED-Streifen im Diffusor. Alles andere bleibt wie v1.

## 1. Tragblech

| | |
|---|---|
| Dateien | `stahlblech_v3_kontur.dxf` (Kontur, mm), `stahlblech_v3.step` (3D mit Senkungen) |
| Werkstoff | Edelstahl **1.4404** (V4A), **2,0 mm**, Oberfläche egal (liegt hinter dem Messing) |
| Maße | 91,8 × 251,8 mm, Ecken R9,9, Gewicht ca. 183 g |
| Gewinde | **4 × M3** (Tabelle „Gewinde“), dort schraubt das Messing hinein |
| Senkungen | **18 × 90° auf Ø 6,0** auf der Messingseite (Tabelle „Senkloch“) |
| Kanten | entgratet, eben (≤ 0,3 mm) |

**Lage:** Das DXF zeigt das Blech von vorn, also von der Messingseite. Ursprung ist die linke untere Ecke, X nach rechts, Y nach oben.

| Art | Was | Ø / Größe | X | Y |
|---|---|---|---|---|
| Fenster | Display-Glas 66,77 × 120,09, je Seite 0,3 Klebefuge | 67,4 × 120,7 | 45,90 | 135,72 |
| Fenster | Gitter + Radar (hinter allen Messingschlitzen) | 59,0 × 18,0 | 45,90 | 211,40 |
| Loch | Kabel LED-Streifen (unter dem Diffusor) | Ø 4,5 | 57,90 | 244,90 |
| Fenster | Diffusor-Schlitz 1 | 11,0 × 3,6 | 15,90 | 244,90 |
| Fenster | Diffusor-Schlitz 2 | 11,0 × 3,6 | 75,90 | 244,90 |
| Loch | Taster | Ø 50,5 | 45,90 | 30,90 |
| Loch | Mikrofon | Ø 2,0 | 78,60 | 38,40 |
| Loch | Mikrofon | Ø 2,0 | 78,60 | 30,40 |
| Senkloch | M3 in Gegenleiste links | Ø 3,4 | 4,60 | 205,90 |
| Senkloch | M3 in Gegenleiste links | Ø 3,4 | 4,60 | 185,90 |
| Senkloch | M3 in Gegenleiste links | Ø 3,4 | 4,60 | 165,90 |
| Senkloch | M3 in Gegenleiste links | Ø 3,4 | 4,60 | 145,90 |
| Senkloch | M3 in Gegenleiste links | Ø 3,4 | 4,60 | 125,90 |
| Senkloch | M3 in Gegenleiste links | Ø 3,4 | 4,60 | 105,90 |
| Senkloch | M3 in Gegenleiste links | Ø 3,4 | 4,60 | 85,90 |
| Senkloch | M3 in Gegenleiste links | Ø 3,4 | 4,60 | 65,90 |
| Senkloch | M3 in Gegenleiste links | Ø 3,4 | 4,60 | 45,90 |
| Senkloch | M3 in Gegenleiste links | Ø 3,4 | 4,60 | 25,90 |
| Senkloch | M3 in Gegenleiste rechts | Ø 3,4 | 87,20 | 205,90 |
| Senkloch | M3 in Gegenleiste rechts | Ø 3,4 | 87,20 | 185,90 |
| Senkloch | M3 in Gegenleiste rechts | Ø 3,4 | 87,20 | 165,90 |
| Senkloch | M3 in Gegenleiste rechts | Ø 3,4 | 87,20 | 145,90 |
| Senkloch | M3 in Gegenleiste rechts | Ø 3,4 | 87,20 | 125,90 |
| Senkloch | M3 in Gegenleiste rechts | Ø 3,4 | 87,20 | 105,90 |
| Senkloch | M3 in Gegenleiste rechts | Ø 3,4 | 87,20 | 85,90 |
| Senkloch | M3 in Gegenleiste rechts | Ø 3,4 | 87,20 | 65,90 |
| Zapfen | Zapfen links, rund (Festpunkt) | Ø 4,1 | 4,60 | 115,90 |
| Zapfen | Zapfen rechts, Langloch quer | 5,1 × 4,1 | 87,20 | 115,90 |
| Gewinde | M3 fuer Messingschraube | Ø 2,5 | 7,90 | 225,90 |
| Gewinde | M3 fuer Messingschraube | Ø 2,5 | 83,90 | 225,90 |
| Gewinde | M3 fuer Messingschraube | Ø 2,5 | 7,90 | 7,90 |
| Gewinde | M3 fuer Messingschraube | Ø 2,5 | 83,90 | 7,90 |

## 2. Gegenleisten (2 Stück)

Neu in v3: Die Leisten werden **beim Drucken des Kastens eingelegt** (Druckpause), der Kragen wird über sie gedruckt. Sie sitzen danach fest im Kasten. Für den Probeaufbau gibt es sie als PETG-Ersatz (Druckteil 10).

| | |
|---|---|
| Datei | `gegenleisten_v3.dxf` (2 Streifen) |
| Werkstoff | Edelstahl **1.4404**, **5,0 × 4,0 mm** |
| Längen | links **231,0 mm**, rechts **191,0 mm** |
| Gewinde | M3 **durchgehend** durch die 4 mm, auf der Stahlseite 90° auf Ø 4,0 angesenkt |
| Kanten | entgratet, gerade (≤ 0,3 mm auf die Länge) |

- **Leiste links** (231,0 lang): 11 Gewinde bei 15,5, 35,5, 55,5, 75,5, 95,5, 115,5, 135,5, 155,5, 175,5, 195,5, 215,5 mm ab einem Ende, mittig in der Breite.
- **Leiste rechts** (191,0 lang): 9 Gewinde bei 15,5, 35,5, 55,5, 75,5, 95,5, 115,5, 135,5, 155,5, 175,5 mm ab einem Ende, mittig in der Breite.

Die Gewinde liegen symmetrisch, die Leiste kann nicht falsch herum hinein. Das Gewinde an einem Ende bleibt ungenutzt, es macht nur die Symmetrie.

## 3. Schrauben und Dichtung

- 18 × **M3 × 10 ISO 14581** (Senkkopf Torx), A4, Stahl → Gegenleisten.
- 18 × **O-Ring 3 × 1 NBR**, je einer auf jeder Schraube zwischen Stahl und Kasten (Nut im Abstandsring).
- 4 × **M3 × 4 Senkkopf** Messing → Stahl, Sicherheits-Torx.
- Silikon, neutral vernetzend, für die Raupe und das LED-Kabel.
