# Archive: the first box (September 2026)

The first design: a box set flush into 14 cm of facade insulation, a carrier plate for the electronics, the v5 front
sheet (2 mm brass, folded, with two LED windows in the bend) and the first quarter-round diffuser. It was printed as a
test and is **superseded** by the [v3 box](../../v3/). Kept for the record; do not print it for a build.

| Folder | What |
|---|---|
| `cad/` | `kasten_v3_params.py` (the dimensions of this early box, which was called "v3" at the time; unrelated to today's v3), `make_kasten_v3.py`, `make_sheet_v5.py`, `make_diffusor_v1.py`, `build_front_sheet.py` |
| `models/` | the exported STL and STEP files of that state |

The scripts read the front layout from [`../../front-sheet/`](../../front-sheet/) and write into `cad/out/`.
