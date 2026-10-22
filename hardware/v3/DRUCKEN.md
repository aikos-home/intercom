# Intercom v3.7: drucken und einbauen

> Öffentliche Fassung der Druck- und Einbauanleitung des Prototyps (Deutsch; englische Kurzfassung: [README.md](README.md)). Die Druckdateien liegen in [`print/`](print/), die Metall-Vorlagen in [`metal/`](metal/), die Bilder in [`images/`](images/), die Generatoren in [`cad/`](cad/). Die fertig geslicten Bambu-Dateien (3MF) und die FreeCAD-Gesamtansicht sind nicht veröffentlicht; die Tabellen unten nennen trotzdem ihre Platten, Zeiten und Mengen.

Stand 2026-10-17, v3.7.

**Neu in v3.7 gegenüber v3.6:** **Abstandsstücke 18** für den Spalt zwischen E-Ink-Panel und Displayplatine (Befund
V3-07).
- Drückt man auf das Display, gab es nach, weil im Spalt (2,7 mm) nur Heizpad und Schaumklebefolie liegen.
- Drei Kämme mit Stücken in 2,6, 2,7 und 2,8 mm Dicke, je 11 Stück von 3 bis 30 mm lang und 3 mm breit. Die Dicke steht
  auf dem Rücken des Kamms (Bild [`bild_v3_abstandsstuecke.png`](images/bild_v3_abstandsstuecke.png)).
- Abbrechen, an freien Stellen in den Spalt schieben und festkleben, siehe Zusammenbau Schritt 12.
- Druckt als **Platte L**, nur die Kämme. Auf B ist kein Platz mehr, deshalb gehört L auch bei einem kompletten
  Neudruck dazu.
- Geklärt (2026-10-17): Verstärker-Rahmen **Ø 2,6** und SHT31-Deckel **Ø 3,2** sitzen straff.
- Kasten und alle anderen Teile sind bytegleich mit v3.6.

**Neu in v3.6 gegenüber v3.5:** zwei **Plattenstützen 17** (Befund V3-05).
- Wenn man das Display oben drückte, bog die Display-Trägerplatte oben nach hinten durch. Oben hielten sie nur die
  Haken am Klemmring.
- Die zwei Stützen kommen links und rechts an die Seitenwände, neben den oberen Teil der Platte. Die Platte liegt
  hinten auf ihren Zungen auf, geschraubt wird nichts.
- Jede Stütze liegt an drei Flächen an: an der Seitenwand, vorn am Leistenkanal und oben am Gitterblock. So sitzt sie
  beim Kleben von selbst richtig (Bild [`bild_v3_plattenstuetzen.png`](images/bild_v3_plattenstuetzen.png)).
- Platte J enthält jetzt auch die Stützen. Wer J aus v3.5 schon gedruckt hat, druckt **Platte K**, nur die Stützen.
- Kasten und alle anderen Teile sind bytegleich mit v3.5.

**Neu in v3.5 gegenüber v3.4:** Verstärker-Rahmen 06 und SHT31-Kammerdeckel 08 gibt es jetzt als **Satz in drei
Stiftstärken** (Befund V3-04).
- Die alten Stifte waren gedruckt zu dünn, beide Platinen saßen lose.
- Die Stifte sitzen jetzt mittig in den Platinenlöchern und haben vorn eine kleine Fase.
- Verstärker: Ø 2,5 / 2,6 / 2,7. SHT31: Ø 3,0 / 3,1 / 3,2. Die Zahl ist eingraviert: beim Rahmen auf der Unterseite,
  beim Deckel außen (Bild [`bild_v3_stiftsaetze_unten.png`](images/bild_v3_stiftsaetze_unten.png)).
- Du steckst die Platine auf und nimmst das Teil, auf dem sie **straff** sitzt. Erwartet wird die mittlere Stärke.
  Die anderen zwei bleiben übrig.
- Wer B schon gedruckt hat, druckt **Platte J** (beide Sätze). Platte G entfällt, der Deckel steckt in J.
- Sofort, ohne neuen Druck: die Verstärker-Stifte mit dem Lötkolben vernieten oder je ein Tropfen Heißkleber; auf den
  SHT31-Stift ein Tropfen Sekundenkleber.
- Kasten und alle anderen Teile sind bytegleich mit v3.4.

**Neu in v3.4 gegenüber v3.3:** Der Radar-Rahmen 05 wird **eingeklebt** statt eingedrückt (Befund V3-02, Nachtrag).
- Hinter dem Gitterblock ließ er sich nicht eindrücken. Die Tasche ist nur 2,1 mm tief, die Quetschrippen hatten
  Übermaß, und vorn saß der Wulst der ersten Lage.
- Der neue Rahmen hat keine Rippen, rundum 0,3 mm Luft und vorn eine Fase. Er fällt ohne Kraft in die Tasche.
- Festgeklebt wird er mit Heißkleber, unten und an der Seite zur Kastenwand (Bild [`bild_v3_radar_kleben.png`](images/bild_v3_radar_kleben.png)).
- Das Radar sitzt darin wie in v3.2.
- Kasten und alle anderen Teile sind bytegleich mit v3.3.
- Wer B schon gedruckt hat, druckt **Platte H** (nur der Rahmen, 16 min). Es geht auch ohne Druck: am alten Rahmen die
  6 Rippen außen mit dem Cutter abschneiden.
- Die Display-Druckstifte **−1,5** passen (2026-10-16, P3-03): Das Display ist bündig mit dem Stahl-Ersatz.

**Neu in v3.3 gegenüber v3.2:** Der Computer-Träger 03 rastet ein (Befund V3-03). Bisher hielt ihn erst der Anschlag der
Display-Trägerplatte; ohne Platte fiel er nach unten heraus.
- Auf die Rückwand kommt ein kleiner **Rastknopf** (Teil 06c, geklebt). Der Träger hat hinten eine Gasse, in der der
  Knopf beim Hochschieben läuft, und am Ende ein Loch, in das er einrastet.
- Heraus geht es so: unten 1–2 mm anheben und nach unten ziehen.
- Den Knopf gibt es in drei Höhen (0,4 / 0,6 / 0,8 mm), damit du die Rastkraft ausprobieren kannst.
- Kasten und alle anderen Teile sind bytegleich mit v3.2.
- Wer B schon gedruckt hat, druckt **Platte I** (neuer Träger und die Knöpfe).

**Neu in v3.2 gegenüber v3.1:** Der Radar-Rahmen 05 ist jetzt ein Abstandsrahmen (Befund V3-02).
- Die Stiftleiste des Radars liegt an einer Langseite der Platine, nicht wie angenommen an einer Kurzseite. Ihre
  Lötstellen treffen deshalb keine Nut im Taschenboden.
- Der neue Rahmen hält die Platine auf einer Stufe 1,9 mm vor dem Taschenboden. Hinten halten sie Lippen, so kann sie
  nicht mehr herausfallen.
- Alle anderen Teile sind bytegleich mit v3.1, auch der Kasten.
- Wer Platte B schon gedruckt hat, druckt nur **Platte H**, den neuen Rahmen.

**Neu in v3.1 gegenüber v3:** Der SHT31-Kammerdeckel 08 hat einen Stift für die gemessene SHT31-Platine
(13,22 × 10,5, Loch Ø 3) und eine Rippe, die sie gegen Verdrehen hält. Wer Platte B aus v3 gedruckt hat, druckte dafür
Platte G; seit v3.5 steckt der Deckel als Satz in **Platte J**.

**Zweck:** v3 wird gedruckt und ganz eingebaut, bevor das Metall bei einem Metallbetrieb bestellt wird. Stahl und Messing sind darin gedruckte
Ersatzteile in gleicher Form (13–15). v3 ist die Grundlage für die CNC-Aufträge, aber nicht der endgültige Kasten für
prod. Was sich gegenüber v2 geändert hat und warum, steht in der Befundliste des Projekts (Befunde B-01 bis B-13, Wünsche W-01 bis W-06; nicht veröffentlicht,
die Kurzfassung steht in [README.md](README.md)).

**Herkunft:** `cad/tools/v3_alles.py` baut, prüft und exportiert alles aus `cad/v3_params.py` (Ausgabe in
`cad/out/`). Alle Prüfungen sind bestanden (Protokoll `cad/out/_v3_alles.log`):
- `validate()`: 0 Fehler, 0 Warnungen.
- `check_cad()` misst am fertigen Kasten nach. `check_teile()` prüft alle Druckteile, dazu die Einbauwege: Leisten in der
  Druckpause, Träger einsetzen und hochschieben, Platte einsetzen.
- Messing, Stahl, Diffusor und USB-Feld haben je eine eigene Prüfung.
- 18 von 18 absichtlich eingebauten Fehlern werden erkannt (`v3_mutationen.py`, Protokoll `_mutationen.log`), darunter
  die zu dünnen Stifte aus V3-04, eine Plattenstütze in der Bahn des Computer-Trägers und Abstandsstücke in falscher
  Dicke.
- Jede Bambu-Datei hat genau eine Druckplatte. Passt etwas nicht mehr auf eine Platte, bricht `v3_bambu.py` ab, statt
  still eine zweite anzulegen.

Die Bambu-Dateien erzeugt ein eigenes Skript aus einer Vorlage des Druckers; beides ist nicht veröffentlicht.

**Gesamtansicht:** Die FreeCAD-Datei `intercom-v3.7_ansicht.FCStd` (nicht veröffentlicht) enthält das ganze Intercom in 9 farbigen
Gruppen: Kasten, Front, Taster, Display-Trägerplatte, Computer-Träger, Lautsprecher und Radar, Verteiler mit Sensoren und
Mikrofon, USB-Feld und der Platz für Leitungen. Bilder davon in [`images/`](images/):
[`bild_v3_innen_von_hinten.png`](images/bild_v3_innen_von_hinten.png), [`bild_v3_innen_von_vorn_ohne_platte.png`](images/bild_v3_innen_von_vorn_ohne_platte.png), dazu:
- `bild_v3_sht31_deckel.png`: der Kammerdeckel mit der SHT31-Platine auf dem Stift, von innen gesehen
- [`bild_v3_radar_rahmen.png`](images/bild_v3_radar_rahmen.png): der Radar-Rahmen mit dem Radar, von hinten
- [`bild_v3_radar_kleben.png`](images/bild_v3_radar_kleben.png): der Rahmen in der Tasche am Gitterblock, gelb die zwei Heißkleber-Nähte. Der Blick geht
  von hinten unten, deshalb liegt die Seite zur Kastenwand im Bild rechts.
- [`bild_v3_traeger_rueckseite.png`](images/bild_v3_traeger_rueckseite.png): der Computer-Träger von hinten, mit Gasse und Rastknopf
- [`bild_v3_lautsprecher_schnitt.png`](images/bild_v3_lautsprecher_schnitt.png) und [`bild_v3_lautsprecher_explosion.png`](images/bild_v3_lautsprecher_explosion.png): der Lautsprecher-Einbau
- [`bild_v3_stiftsaetze_unten.png`](images/bild_v3_stiftsaetze_unten.png): die zwei Stiftsätze wie gedruckt, von unten mit den Zahlen. Oben die drei
  Verstärker-Rahmen, unten die drei Kammerdeckel.
- [`bild_v3_plattenstuetzen.png`](images/bild_v3_plattenstuetzen.png): die zwei Plattenstützen an den Seitenwänden, von hinten oben gesehen. Die Platte
  liegt mit ihren Rändern hinten auf den Zungen auf.
- [`bild_v3_abstandsstuecke.png`](images/bild_v3_abstandsstuecke.png): die drei Kämme mit den Abstandsstücken, wie gedruckt.

## Was neu ist

| | v2 | v3 | Grund |
|---|---|---|---|
| Gegenleisten | von oben eingeschoben, Kanäle voller Stützen | in einer **Druckpause** in offene Rinnen gelegt, der Kragen wird darüber gedruckt; O-Ring an jeder Schraube | B-02 |
| Lautsprecher | Einsätze hinten im Gitterblock, kaum erreichbar | 2 Schrauben **von vorn** in einen Klemmring (04), Moosgummi-Dichtung | B-04 |
| Druckausgleichsventil | Loch im Gitterblock | ruht, kein Loch | B-03 |
| Radar | Träger mit Rückplatte, Schacht zu eng | Abstandsrahmen (05), Schacht 0,5 breiter, Platine 1,9 vor dem Taschenboden; seit v3.4 eingeklebt | B-06, V3-02 |
| Sprech- und Klingelrechner | Schlitten mit Schienen, Klingelrechner an der Platte | **ein Computer-Träger** (03) in Schienen an der Rückwand, nach unten herausziehbar | W-03, B-07–B-09, B-11 |
| Display-Trägerplatte | 4 Schrauben, trägt den Klingelrechner | hängt oben mit 2 Zungen am Klemmring, 2 Schrauben unten; trägt Druckstifte und Verstärker | W-03 |
| Druckstifte | Spitze 1,0, eine Länge | Spitze 1,75, **4 Längen** (−0,5 bis −2,0 gegen v2), beschriftet; **−1,5 passt** | B-12, B-13, P3-03 |
| Verstärker-Rahmen | Stifte klemmen nicht | Stifte mittig in den Löchern (Lochabstand 12,5), Satz in 3 Stärken Ø 2,5 / 2,6 / 2,7 | B-10, V3-04 |
| Verteiler | Träger für 25 × 70 | ganze Platine 30 × 70 auf einem geklebten Klips-Sockel (07) | W-04 |
| LAN | Loch M20, keine Verschraubung | teilbare M20-Verschraubung, der Stecker passt durchs Loch; 5 Kabelbinder-Ösen in S-Kurve | B-01, W-05 |
| Temperatur und Feuchte | BME280 im Halter H2 | SHT31-D in eigener **Außenkammer** unten rechts, auf einem Stift am Deckel (Satz in 3 Stärken Ø 3,0 / 3,1 / 3,2); der BME280 kann auf den Verteiler | W-02, V3-04 |
| LEDs | 2 Fenster im Kragen | COB-Streifen im Diffusor unter dem Dach, ein Kabelloch | W-06 |
| Holzschrauben | Linsenkopf mit Scheibe | **Senkkopf**, bündig, weil der Träger darüber gleitet | – |
| Kämme und Halter | Kämme, Klebehalter | keine Kämme; freie Kabelgassen und 5 Wand-Ösen | – |

## Fertig geslict für die A1

Im Ordner `bambu/`: Bambu A1, 0,4-mm-Düse, Textured PEI, 0,20 mm. Der Kasten hat 4 Wände und 25 % Gyroid-Füllung, die
übrigen Teile 3 Wände, der Diffusor 2.

| Reihenfolge | Datei | Inhalt | Zeit laut Slicer | Filament |
|---|---|---|---|---|
| 1 | `intercom-v3.7_B-teile_petg.gcode.3mf` | Teile 02–12 und 17, **darin die Leisten 10 für die Pause** | 4 h 21 min | 85 g PETG |
| 2 | `intercom-v3.7_A-kasten_petg.gcode.3mf` | Kasten 01, **mit Druckpause** | 11 h 24 min + Pause | 271 g PETG |
| 3 | `intercom-v3.7_C-stahlblech-ersatz_petg.gcode.3mf` | Stahl-Ersatz 13 | 1 h 6 min | 25 g PETG |
| 4 | `intercom-v3.7_D-messing-ersatz-unten_petg.gcode.3mf` | Messing-Ersatz unten 14 | 1 h 26 min | 36 g PETG |
| 5 | `intercom-v3.7_E-messing-ersatz-oben_petg.gcode.3mf` | Messing-Ersatz oben 15 | 53 min | 18 g PETG |
| 6 | `intercom-v3.7_F-diffusor_weiss_pla.gcode.3mf` | Diffusor 16 | 24 min | 4 g PLA, **weiß** |
| (H) | `intercom-v3.7_H-radar-rahmen_petg.gcode.3mf` | nur der Radar-Rahmen 05 (neu seit v3.4: zum Kleben) | 16 min | 1,5 g PETG |
| (I) | `intercom-v3.7_I-computer-traeger_petg.gcode.3mf` | nur Computer-Träger 03 und Rastknöpfe 06c (neu seit v3.3) | 56 min | 16 g PETG |
| (J) | `intercom-v3.7_J-stiftsaetze-plattenstuetzen_petg.gcode.3mf` | Verstärker-Rahmen 06 und Kammerdeckel 08 je in 3 Stiftstärken (seit v3.5), dazu die Plattenstützen 17 (neu in v3.6) | 52 min | 15 g PETG |
| (K) | `intercom-v3.7_K-plattenstuetzen_petg.gcode.3mf` | nur die zwei Plattenstützen 17 (neu in v3.6) | 26 min | 6 g PETG |
| L | `intercom-v3.7_L-display-abstandsstuecke_petg.gcode.3mf` | Abstandsstücke 18, drei Kämme (neu in v3.7); passt nicht mehr auf B und gehört deshalb immer dazu | 24 min | 5 g PETG |

- **B vor A:** In B stecken die zwei Leisten, die in der Pause von A in den Kasten kommen.
- C bis F gehen in beliebiger Reihenfolge.
- L braucht jeder. H bis K braucht nur, wer B aus einem älteren Stand gedruckt hat:
  - H, wenn B aus v3 bis v3.3 stammt
  - I, wenn B aus v3 bis v3.2 stammt
  - J, wenn B aus v3 bis v3.5 stammt
  - K statt J, wenn J aus v3.5 schon gedruckt ist
- Platte G (nur der Kammerdeckel, seit v3.1) gibt es nicht mehr, der Deckel steckt jetzt als Satz in J.
- Die Kasten-Datei A ist dieselbe wie in v3. Ein schon laufender oder fertiger Kasten aus v3 passt zu allen Ständen bis
  v3.7.
- Den Kasten gibt es in v3 nur ganz aus PETG. Die Variante mit PLA-Kontaktschichten aus v2 entfällt: Mit ihr setzt der
  Slicer trotz Blocker ein paar Stützen in zwei Kabelbinder-Ösen. Die PETG-Datei ist im G-Code nachgeprüft: keine Stütze
  in den Leistenrinnen, keine in den Kanälen der Ösen.
- Der Kasten liegt mit der Rückwand nach unten, um 45° gedreht, mittig auf dem Bett.
- Beim Start das Filament dem AMS-Fach zuordnen.

## Druckpause beim Kasten

> ⚠️ **Die Kasten-Datei A nicht aus Bambu Studio drucken** (Befund V3-01, 2026-10-16). Bambu Studio öffnet sie als
> Projekt und slict beim Senden neu, dabei geht die Pause verloren. Die Datei direkt am Drucker starten: per FTPS auf
> den Drucker laden und am Display starten.

Die Pause ist in der Datei schon eingebaut. Der Drucker hält bei **88 %**, nach rund 10 Stunden, auf 54,0 mm Höhe. Er
fährt die Düse 25 mm hoch und den Kopf ganz nach links, dann wartet er. Danach druckt er noch etwa 1 h 15 min.

1. Die zwei Leisten aus Teil 10 bereitlegen: **231 mm** und **191 mm** lang. Steht ein Elefantenfuß über, ihn mit einer
   Klinge abziehen. Die Leisten müssen sich ohne Kraft in die Rinnen legen lassen.
2. Die Rinnen sind die zwei schmalen, oben offenen Kanäle an den Längsseiten des Kastens. Die **lange Leiste kommt in die
   lange Rinne**, die kurze in die kurze.
   - Die kurze Rinne endet 50 mm vor dem Kastenende mit USB-Öffnung und Verschraubungsloch, die lange 10 mm davor.
   - Vertauschen geht nicht, denn die lange Leiste passt nicht in die kurze Rinne.
   - Die Richtung ist egal, die Löcher liegen symmetrisch.
3. Beide Leisten ganz hinunterdrücken. Sie liegen dann 0,5 mm unter der Rinnenkante, nichts darf überstehen.
4. Hängt ein Faden an der Düse, ihn mit einer Pinzette abnehmen. Vorsicht, die Düse ist heiß.
5. Am Drucker oder in der App fortsetzen. Jetzt wird der Kragen über die Leisten gedruckt.

**Die Leisten bleiben für immer im Kasten.** Ein Kasten mit Edelstahlleisten wird neu gedruckt, mit derselben Datei. In
der Pause kommen dann die Edelstahlleisten hinein.

## Alle Teile

Alle Dateien liegen oben in diesem Ordner, schon in Drucklage. Alles ist PETG, nur der Diffusor 16 ist weißes PLA.

| Nr | Datei | Wofür | Platte | Hinweis |
|---|---|---|---|---|
| 01 | `01_kasten.stl` | Kasten 92 × 252 × 60 | A | Rückwand unten, mit Druckpause |
| 02 | `02_display_traegerplatte.stl` | Display-Trägerplatte: vorn die Druckstifte, hinten der Verstärker | B | Die 2 Gewindeeinsätze sitzen im Kasten, nicht in der Platte. |
| 03 | `03_computer_traeger.stl` | Computer-Träger für Sprech- und Klingelrechner | B, I | Seit v3.3 mit Gasse und Rastloch hinten. |
| 04 | `04_lautsprecher_klemmring.stl` | Klemmring hinter dem Lautsprecher | B | 2 Gewindeeinsätze, am Tisch einschmelzen |
| 05 | `05_radar_rahmen.stl` | Radar-Rahmen, Abstandsrahmen (seit v3.2), ohne Rippen (seit v3.4) | B, H | wird mit Heißkleber **geklebt**, nicht gedrückt. Druckt mit der Stufe nach unten. |
| 06 | `06_verstaerker_rahmen_3_staerken.stl` | Verstärker-Rahmen, Satz mit Stiften Ø 2,5 / 2,6 / 2,7 (neu in v3.5) | B, J | Den nehmen, auf dem der Verstärker straff sitzt (Zahl unten), und auf die Plattenrückseite kleben. |
| 06b | `06b_zapfen_4x_abknipsen.stl` | Zapfen Ø 3 für den Verstärker-Rahmen | B | 2 werden gebraucht, 2 sind Reserve. Vom Steg abknipsen. |
| 06c | `06c_rastknoepfe_3_hoehen.stl` | Rastknöpfe Ø 3 für den Computer-Träger (neu in v3.3) | B, I | 0,4 / 0,6 / 0,8 hoch, der flachste neben dem Fähnchen. Abknipsen, einen davon auf die Rückwand kleben. |
| 07 | `07_verteiler_sockel.stl` | Sockel für die Verteilerplatine | B | in den Sitz an der Rückwand kleben |
| 08 | `08_sht31_kammerdeckel_3_staerken.stl` | Deckel der SHT31-Kammer mit Stift und Rippe, Satz mit Stiften Ø 3,0 / 3,1 / 3,2 (neu in v3.5) | B, J | Den nehmen, auf dem die Platine straff sitzt (Zahl außen); geklebt. |
| 09 | `09_display_druckstifte_4_laengen.stl` | 4 Leisten mit je 5 Druckstiften | B | beschriftet −0,5, −1,0, −1,5 und −2,0 |
| 10 | `10_gegenleisten_ersatz_fuer_druckpause.stl` | Gegenleisten, 231 und 191 lang | B | **für die Pause von A** |
| 11 | `11_usb_einsatz.stl` | USB-Einsatz | B | |
| 12 | `12_usb_abdeckung.stl` | USB-Abdeckung | B | Ausschnitt für die Verschraubung größer als in v2 |
| 13 | `13_stahlblech_ersatz.stl` | Ersatz für das Stahlblech | C | Zapfenlöcher Ø 4,3 statt 4,1, sonst wie der Stahl |
| 14 | `14_messing_ersatz_unten.stl` | Messing-Ersatz unten | D | |
| 15 | `15_messing_ersatz_oben.stl` | Messing-Ersatz oben, mit Dach | E | |
| 16 | `16_diffusor_weiss.stl` | Diffusor unter dem Dach | F | weißes PLA |
| 17 | `17_plattenstuetzen_links_rechts.stl` | Zwei Stützen für die Display-Trägerplatte, links und rechts (neu in v3.6) | B, J, K | An die Seitenwände geklebt. Die Zunge zeigt zur Kastenmitte. Druckt mit der Klebefläche auf dem Bett. |
| 18 | `18_display_abstandsstuecke_3_staerken.stl` | Abstandsstücke zwischen E-Ink-Panel und Displayplatine, drei Kämme 2,6 / 2,7 / 2,8 (neu in v3.7) | L | Abbrechen und einkleben, siehe Schritt 12. |

## Kasten: Stützen

Diese Einstellungen stecken schon in der Datei:
- Typ Baum (automatisch), Schwellenwinkel 30°.
- „Nur auf der Druckplatte“ ist aus.
- Brücken bis 10 mm druckt der Slicer ohne Stütze.
- 12 Stützenblocker: über den 2 Leistenrinnen und in den 10 Kabelbinder-Kanälen.

Wo Stützen entstehen, aus dem G-Code zurückgerechnet:

**Innen**, alles von vorn durch die offene Front erreichbar:
1. hinter dem Gitterblock oben, an der Fläche für den Lautsprecher
2. **in der Radartasche**, auch in den Nuten. Die Decke ist 23 mm breit, das ist für eine Brücke zu weit. Die Tasche
   gründlich ausräumen, sonst liegt der Radar-Rahmen nicht flach auf dem Taschenboden.
3. an beiden Seiten über die ganze Länge, unter den Leistenkanälen (wie in v2)
4. unten um Taster und Mikrofon
5. unter den 2 Plattenauflagern
6. unter den 5 Wand-Ösen. Die Kanäle der Ösen selbst bleiben frei.

**Außen**, vom Bett aus:
7. **in den 4 Löchern für die Holzschrauben.** Die Stützen wachsen vom Bett durch die Rückwand nach innen. Von außen
   herausdrücken.
8. vor dem Kastenboden, unter dem Loch der Kabelverschraubung und unter der USB-Öffnung

**Nach dem Druck prüfen:**
- Eine 4er-Holzschraube geht durch jedes der 4 Löcher, und der Kopf liegt bündig in der Senkung.
- Ein Kabelbinder 3,6 mm geht durch alle 10 Ösen.
- Eine M3 × 10 lässt sich in jedes der 18 Löcher im Kragen bis in die Leiste drehen. In PETG schneidet sie das Gewinde
  selbst.
- Radartasche und Nut sind frei, der Radar-Rahmen fällt in beiden Lagen ohne Kraft hinein.
- Der USB-Einsatz 11 geht von unten in die Bodenöffnung.

## Einkaufen und bereitlegen

**8 × M3-Gewindeeinsatz** (Loch Ø 4,0 × 6, die 5,7 mm langen wie bisher):
- 2 in den Klemmring 04, am Tisch
- 2 in die Plattenauflager im Kasten
- 2 in die Tasterscheibe im Kasten
- 2 in die Dome der USB-Abdeckung, von außen im Kastenboden

| Wofür | Schraube oder Teil | Anzahl |
|---|---|---|
| Kasten an die Zarge | **neu:** Holzschraube 4,0 × 30–35 mit **Senkkopf** (Kopf Ø 8, 90°) | 4 |
| Kabeleinführung | **neu:** teilbare Verschraubung M20 für Kabel 6–8 mm: OBO V-TEC TB20 06-08 (Satz mit teilbarer Gegenmutter) oder PFLITSCH USG 22053 PC + Gegenmutter 1420/220 GGM + Dichteinsatz UFE 53p8 | 1 |
| Lautsprecher | **neu:** M3 × 14 Linsenkopf ISO 7380, unter jedem Kopf ein O-Ring 3 × 1,5 | 2 + 2 |
| Display-Trägerplatte | M3 × 8 Linsen- oder Zylinderkopf, Kopf höchstens Ø 6 × 3 | 2 |
| Taster | wie bisher | 2 |
| Stahl-Ersatz in die Leisten | M3 × 10 Senkkopf ISO 14581 (Torx), dazu **neu** je ein O-Ring 3 × 1 NBR | 18 + 18 (10 links, 8 rechts) |
| Messing-Ersatz in den Stahl-Ersatz | M3 × 4 Senkkopf (× 5 geht, × 6 ist zu lang) | 4 |
| USB-Abdeckung | M3 × 8 Linsenkopf ISO 7380, Sicherheits-Torx (Torx-Pin) | 2 |

Dazu:
- **neu:** Moosgummi 2 mm, geschlossenzellig, für die Lautsprecher-Dichtung: 40 × 40, Loch Ø 35 in der Mitte, 4 Löcher
  Ø 3,6 im Lochbild 32,4
- **neu:** Schaumstoff 2 mm, nicht leitend, doppelseitig klebend, unter den Klingelrechner
- **neu:** COB-Streifen, 5 V, adressierbar (WS2812B), 10 mm breit, zum Beispiel BTF-LIGHTING FCOB. Man schneidet alle
  11 mm, 5 Abschnitte ergeben 55 mm. Dazu Schutzlack.
  - Die 5 mm breite Ausführung passt auch: 5 Abschnitte, 62,5 mm.
  - Die RGBW-Ausführung (WS2814, 12 V, ein Abschnitt 62 mm) passt nicht.
- Kabelbinder 3,6 mm breit, mindestens 10 (5 LAN-Ösen, 5 Wand-Ösen)
- O-Ring 26 × 2 für die Tasterbohrung
- fürs Mikrofon: ePTFE-Membran Ø 12 und 2 Dichtringe 10/13 × 1
- Vergussharz fürs USB-Feld
- neutral vernetzendes Silikon
- Sekundenkleber
- **neu:** Heißklebepistole mit Heißkleber, für den Radar-Rahmen

## Zusammenbau

Die Reihenfolge hat Gründe:
- Der Klemmring hält oben die Display-Trägerplatte, darum kommt er vorher.
- Der Computer-Träger gleitet über die Holzschrauben, darum hängt der Kasten vorher an der Zarge.
- Die Platte hält den Träger von unten, darum kommt sie nach dem Träger.

1. **Einsätze:** die 8 Gewindeeinsätze einschmelzen.
2. **Sockel, Stützen und Kammer kleben:**
   - Den Verteiler-Sockel 07 in seinen Sitz unten links an der Rückwand kleben. Ein 1-mm-Rand gibt die Lage vor.
   - **Plattenstützen 17** (neu in v3.6, Bild [`bild_v3_plattenstuetzen.png`](images/bild_v3_plattenstuetzen.png)): Die zwei Stützen sind spiegelgleich.
     Die Zunge zeigt immer zur Kastenmitte. Die abgeschrägte Kante kommt vorn in die Ecke zwischen Wand und
     Leistenkanal.
     - Sekundenkleber auf die Klebefläche, das ist die raue Seite vom Druckbett.
     - Die Stütze durch die Front hinter den Leistenkanal schieben und an die Seitenwand drücken.
     - Dabei nach vorn an den Leistenkanal und nach oben an die Unterseite des Gitterblocks schieben. Dann sitzt sie
       richtig.
     - Ist die Display-Trägerplatte schon drin, vorher die 2 Schrauben lösen und die Platte herausnehmen.
   - **SHT31-D auf den Deckel 08** (Bild `bild_v3_sht31_deckel.png`):
     - Den Deckel wählen: Die Platine nacheinander auf die drei Deckel aus dem Satz stecken (Zahl außen: 3,0 / 3,1 /
       3,2) und den nehmen, auf dem sie **straff** sitzt. Am Prototyp passt **3,2** (2026-10-17).
     - Die Litzen an die 4 Lötlöcher am linken Rand löten (VIN, GND, SCL, SDA).
     - Die Platine mit der **beschrifteten Seite zum Deckel** auf den Stift stecken, bis sie auf dem Bund liegt. Das
       Loch sitzt rechts oben, die Lötlöcher links, direkt hinter dem Kabelloch des Deckels.
     - Unter ihrer Unterkante liegt eine Rippe. Beim Aufstecken die Unterkante darauf legen, dann sitzt sie gerade.
     - Nur wenn keiner der drei Stifte straff sitzt: das Stiftende mit einem Tropfen Sekundenkleber sichern.
   - Die Litzen durch das Kabelloch im Deckel führen. Den Deckel unten rechts gerade auf die Kammerwände setzen und
     kleben, die Platine zeigt dabei in die Kammer. Das Kabelloch mit Silikon dichten.
   - Die 3 kleinen Löcher der Kammer nach außen bleiben offen: zwei unten im Boden, eines schräg in der rechten Wand.
3. **USB-Feld** wie in v2:
   - Litzen an die 3 Breakouts löten.
   - Die Breakouts von unten in die Schlitze des Einsatzes 11 stecken, die Blende liegt außen auf. Ein Ring Silikon
     darunter, damit kein Harz durchläuft.
   - Den Becher auf dem Tisch vergießen.
   - Den Einsatz mit Silikon von unten in die Bodenöffnung setzen.
   - Die Abdeckung 12 mit 2 × M3 × 8 Torx-Pin festschrauben.
4. **Lautsprecher**, solange die Front offen ist:
   - Lautsprecher und Moosgummi-Dichtung von innen an die Rückseite des Gitterblocks halten, Membran nach vorn, den
     Klemmring 04 dahinter.
   - Von vorn, aus dem Gitterhohlraum, 2 × M3 × 14 durch die Wand und die oberen Rahmenlöcher in den Klemmring drehen.
     Unter jeden Kopf einen O-Ring 3 × 1,5.
   - Unten gibt es keine Schrauben. Dort drücken zwei Flächen des Klemmrings auf die Rahmenecken, und sein Fuß stützt
     sich unter dem Lautsprecher am Gitterblock ab.
5. **Radar**, seit v3.4 eingeklebt (Bild [`bild_v3_radar_kleben.png`](images/bild_v3_radar_kleben.png), gelb ist der Kleber):
   - Am Tisch das Kabel auf die Stiftleiste stecken.
   - Das Radar von der **offenen Seite** in den Rahmen 05 schieben: zwischen die Stufen vorn und die Lippen hinten,
     Antenne nach vorn, Bauteile und Stiftleiste nach hinten. Die Stiftleiste läuft dabei an einer Seitenleiste
     entlang; welche der beiden, ist egal.
   - Die Tasche hinten am Gitterblock muss frei von Stützenresten sein.
   - Den Rahmen in die quadratische Tasche setzen, bis er auf dem Taschenboden aufliegt. Er hat rundum 0,3 mm Luft und
     braucht keine Kraft.
   - Den Rahmen mit einem Finger halten und mit Heißkleber festkleben:
     - eine Naht **unten**, wo der Rahmen aus der Tasche kommt
     - eine Naht an der **Seite zur Kastenwand**
     - Der Kleber kommt jeweils auf die Rückseite des Gitterblocks und an den Rahmen. Auf der Lautsprecherseite ist kein
       Platz, und in die Mitte kommt kein Kleber, dort ist die Antenne.
   - Die Platine liegt dann 1,9 mm vor dem Taschenboden, die Lötstellen schweben frei darüber. Die alten Nuten im
     Taschenboden bleiben leer, sie stören nicht.
   - Das geht in zwei Lagen, 0° und 90°. Welche besser durch das Gitter sieht, zeigt erst der Drehtest mit echtem Metall.
     Heißkleber lässt sich dafür wieder lösen.
   - Sekundenkleber hält auch, dann sitzt der Rahmen aber fest. Für die andere Lage braucht es dann einen neuen Rahmen
     (Platte H, 16 min).
   - Wer den Rahmen aus v3.2 schon hat: die 6 Rippen außen mit dem Cutter abschneiden, dann geht er auch. Er hat aber
     nur 0,1 mm Luft und keine Fase. Klemmt er noch, Platte H drucken.
6. **Kasten an die Zarge** (nur an der Tür, auf dem Tisch entfällt das):
   - Den LAN-Stecker von unten durch das Loch Ø 20,5 in den Kasten führen.
   - Die teilbare Verschraubung um das Kabel legen und von innen mit der Gegenmutter festziehen. Dafür gilt die Anleitung
     des Herstellers.
   - Den Kasten mit 4 Senkkopf-Holzschrauben festschrauben. Die Köpfe müssen bündig liegen.
7. **Computer-Träger 03:**
   - Am Tisch einsetzen:
     - Den Sprechrechner in seinen Platz stecken, Modulseite zum Träger, Stifte nach vorn, Antenne oben, USB-C unten. Er
       rastet oben hinter zwei Haken ein. Unter der USB-C-Buchse bleiben 25 mm frei, für einen Stecker oder für Litzen.
     - Den Klingelrechner auf 2 mm Schaumstoff kleben, PoE-Seite zum Träger, RJ45 nach unten. Er liegt oben an den
       Anschlägen und unten auf dem Sockel unter der Buchse.
   - **Einmalig den Rastknopf setzen** (der Kasten v3 hat ihn noch nicht), am besten mit dem leeren Träger und mit dem
     Kasten auf dem Rücken:
     1. Den Träger einsetzen wie unten beschrieben und ganz hochschieben.
     2. Einen Rastknopf aus 06c abknipsen, zum Anfang den mittleren (0,6). Auf seine flache Seite kommt ein
        **winziger** Tropfen Sekundenkleber.
     3. Den Knopf von vorn durch das Rastloch im Träger stecken (unten rechts, unter der RJ45-Buchse) und mit einem
        Zahnstocher auf die Rückwand drücken. Der Träger ist dabei die Lehre.
     4. Kurz warten, dann den Träger unten anheben und herausziehen. Der Knopf bleibt auf der Rückwand.
     5. Nicht zu viel Kleber nehmen, sonst klebt der Träger mit fest.
   - Den Träger etwa 40 mm unterhalb seiner Endlage von vorn an die Rückwand setzen. Die Zungen stehen dann in den Lücken
     zwischen den Schienenlippen. Der Rastknopf liegt dabei in der Gasse auf der Trägerrückseite.
   - Den Träger hochschieben bis zum Anschlag. Auf den letzten Millimetern rastet er hörbar ein.
   - **Heraus:** den Träger unten 1–2 mm anheben und nach unten ziehen.
   - Hält er zu fest oder zu locker, einen anderen Knopf nehmen: Den alten mit einer Klinge abheben, einen niedrigeren
     oder höheren aufkleben.
   - Den LAN-Stecker von unten in die Buchse stecken. Das Kabel entlang der S-Kurve mit 5 Kabelbindern an die Ösen ziehen.
8. **Verteiler:** Die Platine auf die 4 Stifte des Sockels drücken, bis die 2 Rastfinger rechts über die Kante schnappen.
   Die Bauteile zeigen nach vorn.
9. **Display-Trägerplatte 02** vorbereiten:
   - Den Rahmen wählen: Den Verstärker nacheinander auf die drei Rahmen aus dem Satz drücken (Zahl unten: 2,5 / 2,6 /
     2,7) und den nehmen, auf dem er **straff** sitzt. Am Prototyp passt **2,6** (2026-10-17).
   - Diesen Rahmen mit 2 Zapfen 06b auf die Plattenrückseite stecken und kleben.
   - Den Verstärker auf die 2 Stifte des Rahmens drücken, Bauteile nach hinten.
   - Hält er auf keinem straff: die Stiftspitzen, die 2 mm über die Platine stehen, mit dem Lötkolben zu einem kleinen
     Nietkopf drücken, oder je ein Tropfen Heißkleber.
   - 4 Druckstifte **einer** Länge in die 4 Mulden vorn auf der Platte stecken.
     - **−1,5 nehmen.** Damit ist das Display bündig mit dem Stahl-Ersatz (2026-10-16).
     - Erst kleben, wenn die Länge passt.
10. **Display-Trägerplatte einsetzen:**
    - Die Platte etwa 3,5 mm unterhalb ihrer Endlage von vorn einsetzen. Ihre Ränder liegen dabei hinten an den Zungen
      der Plattenstützen an.
    - Hochschieben: Die 2 Zungen oben gehen zwischen Gitterblock und die Haken des Klemmrings.
    - Unten mit 2 × M3 × 8 festschrauben.
    - Der Zapfen hinten auf der Platte stützt jetzt den Computer-Träger von unten.
    - Probe: Das Display oben kräftig drücken, die Platte darf hinten nicht mehr nachgeben.
11. **Mikrofon und Taster** wie in v2: Membran und Dichtringe in die Mikrofontasche, Taster mit O-Ring 26 × 2 und
    2 Schrauben.
12. **Display** vorbereiten und aufsetzen:
    - Zuerst die **Abstandsstücke 18** in den Spalt zwischen E-Ink-Panel und Displayplatine setzen (neu in v3.7):
      - Mit 2,7 anfangen. Klemmt ein Stück, 2,6 nehmen; wackelt es noch, 2,8.
      - Nur an freie Stellen: nicht auf Bauteile, nicht auf das Flachbandkabel des Panels, nicht auf die Litzen des
        Heizpads.
      - Mehrere Stücke rundum verteilen, vor allem dort, wo man drückt.
      - Mit einem Tropfen Sekundenkleber nur auf der Platinenseite festkleben. Das Panel liegt dann nur auf.
    - Das Display auf die Stifte setzen, das Glas nach vorn, das USB-Ende nach unten.
    - Probe: Drückt man auf das Glas, darf es nicht mehr nachgeben.
13. **LED-Streifen:**
    - Den COB-Streifen unter das Dach des Messing-Ersatzes 15 kleben und lackieren.
    - Die 3 Adern durch das Loch oben bei x 62 führen: erst durch 15, dann durch den Stahl-Ersatz 13, dann durch den
      Kragen in den Kasten.
14. **Stahl-Ersatz 13:**
    - In jede Nut um die 18 Schraublöcher einen O-Ring 3 × 1 legen.
    - Den Stahl-Ersatz aufsetzen: Die 2 Zapfen am Kasten gehen in seine Löcher, das Displayglas liegt im Fenster.
    - Die 18 × M3 × 10 in die Leisten schrauben, in PETG nur handfest.
    - Die Köpfe müssen bündig sitzen, sonst liegt der Messing-Ersatz nicht auf.
15. **Messing-Ersatz und Diffusor:**
    - Erst 14 (unten) aufsetzen, dann 15 (oben) mit dem Falz.
    - 4 × M3 × 4 in die Ecken des Stahl-Ersatzes schrauben.
    - Den Diffusor 16 mit seinen 2 Laschen in die Schlitze unter dem Dach drücken.
    - Im Probeaufbau reichen die klemmenden Laschen. Endgültig hält Silikon in der Rille am Diffusorrand.

**Dicht ist der Aufbau nur mit Raupe.** Für einen Test bei Regen die Silikonraupe wie im Endaufbau in die Rinne um die
Front ziehen.

**Ausbau**, wie festgelegt:
1. Messing abschrauben.
2. Die Silikonfuge schneiden.
3. Den Stahl abschrauben. Das Display geht mit.
4. Die Display-Trägerplatte abschrauben, 2 Schrauben.
5. Den LAN-Stecker abziehen.
6. Den Computer-Träger unten etwas anheben, 40 mm nach unten schieben und nach vorn herausnehmen.

## Vor dem Einbau klären oder messen

1. **COB-Streifen:** Welcher wird es? Unter dem Dach ist Platz für 10 mm Breite bis 57 mm Länge, für 5 mm Breite bis
   66 mm.
2. **Verteiler:** Rechts liegt ein 1,7 mm breiter Rand hinter dem Taster. Dort nur Bauteile bis 5 mm Höhe, sonst bis
   10 mm.
3. **Lautsprecher:** Gebaut ist mit dem gemessenen Lochbild 32,4, das Datenblatt sagt 32. Beides geht, die M3-Schrauben haben in
   den Löchern Luft.
4. **Druckstifte:** Erledigt 2026-10-16: −1,5 passt (P3-03).
5. **SHT31-D:** Erledigt in v3.1, die Platine ist gemessen. Offen ist nur, auf welcher Seite ihre Bauteile stehen.
   Vorgesehen sind auf beiden Seiten bis 1,7 mm. Am Stift liegt die Platine auf einem Bund Ø 3,8; stünde dort auf der
   beschrifteten Seite ein Bauteil näher als 1,9 mm an der Lochmitte, sag Bescheid.
6. **Stiftstärken:** Erledigt 2026-10-17: Verstärker-Rahmen 2,6 und Kammerdeckel 3,2 sitzen straff. Der nächste Kasten
   bekommt genau diese Maße.
7. **Stopper für den Computer-Träger** (am Prototyp eine geklebte Leiste): Maße A–E aus dem Messblatt stehen noch aus. Sie
   kommen in den v4-Kasten.

## Was der Aufbau zeigen soll

- Die Leisten sitzen nach der Pause richtig: alle 18 Schrauben greifen, der Stahl-Ersatz liegt plan.
- Der Lautsprecher ist dicht und klingt sauber: Dichtung, Klemmring, die 2 Schrauben von vorn.
- Der Computer-Träger gleitet sauber hinein und heraus und sitzt fest, wenn Platte und Anschlag ihn halten.
- Die Platte hängt sicher an den 2 Zungen, die 2 Schrauben unten sind erreichbar.
- Display: Sitz im Fenster, Touch durch die Front, gibt beim Drücken nicht nach (Abstandsstücke 18). Die Stiftlänge ist
  geklärt (−1,5).
- Radar in beiden Lagen, Rahmen geklebt; Verteiler auf dem Sockel, SHT31-D in der Kammer.
- Das LAN-Kabel hat freie Bahn, die Zugentlastung über die Ösen hält.
- Die LED leuchtet gleichmäßig durch den Diffusor.
- Taster, Mikrofon und Flashen über die Unterseite gehen.

Passt etwas nicht, ändert sich `v3_params.py`, und alles wird neu erzeugt, auch die Unterlagen für das Metall.

## Metall: noch nicht bestellen

Im Ordner [`metal/`](metal/) liegen die Vorlagen für die Vorbesprechung mit einem Metallbetrieb:
- `STAHL_VORLAGE.md`: Stahlblech und Gegenleisten mit allen Maßen
- `stahlblech_v3.step` und `stahlblech_v3_kontur.dxf`
- `gegenleisten_v3.dxf`
- `messing_v3.step`
- `diffusor_v3.step`

**Nicht bestellen.** Sie werden neu erzeugt, sobald die Regeln des Betriebs bekannt sind. 
