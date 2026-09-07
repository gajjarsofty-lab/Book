# Surat — A Personal City Book

`SURAT_PRIVATE_EDITION.pdf` — twelve pages, US Letter portrait, built to be
printed at home on an HP DeskJet 2700-series.

Everything in the book is real. The maps are OpenStreetMap geometry for Surat,
the typefaces are licensed OFL fonts, the numbers are sourced and the
straight-line distances are computed from coordinates. The whole file is
vector: live PDF text plus vector map artwork, with zero raster images.

**There is no photography in this edition.** The build machine's network policy
blocks every source of real, licensed, print-resolution photographs of Surat —
Wikimedia Commons, Unsplash, Pexels, Flickr, government media. Rather than
fabricate or upscale, the layout was changed and the book is set as a small
atlas. The full list of blocked hosts, and what was tried, is in `SOURCES.txt`.

## Contents

| Page | |
|---|---|
| 1 | Cover — the municipal area at 1:145 000 |
| 2 | The Tapi |
| 3 | Layers of history — Surat Castle |
| 4 | Diamond city — the Surat Diamond Bourse at Khajod |
| 5 | The textile city — the Ring Road market blocks |
| 6 | **Bangle** — home, 21.1990335 N 72.7901332 E, 1 km radius at 1:12 000 |
| 7 | Surti flavours — aloopuri, locho, khavsa, cheese angoori |
| 8 | Dumas |
| 9 | Surat today |
| 10 | Everyday Surat — four quarters at one scale |
| 11 | Closing |
| 12 | Colophon and sources |

## Files

```
SURAT_PRIVATE_EDITION.pdf   the book
SOURCES.txt                 sources, licences, attribution, asset manifest
assets/                     every map as vector PDF + 300 dpi PNG (+ SVG
                            where the file is small enough to be useful),
                            each with a .json sidecar giving its projected
                            extent in EPSG:32643
  BANGLE_map.pdf/.svg/.png  the home map
data/bangle_*.gpkg          the OSM-derived geometry behind page 6
fonts/                      Cormorant Garamond, Inter, Noto Serif Gujarati
src/overture.py             reads Overture GeoParquet straight off public S3
                            over HTTPS range requests
src/fetch_map_data.py       pulls the map layers into data/*.gpkg
src/render_maps.py          renders every map as vector PDF/SVG/PNG
src/build_book.py           lays out and writes the PDF
```

## Rebuilding

```bash
pip install reportlab pillow requests pyarrow geopandas shapely pyproj \
            matplotlib pdfrw pymupdf
python3 src/fetch_map_data.py bangle      # and the other tiles, see SOURCES.txt §6
python3 src/render_maps.py                # all maps
python3 src/build_book.py                 # the PDF
```

## Printing

Print at **actual size / 100 %**, not "fit to page". Nothing sits closer than
0.42 in to the trim, inside the printer's unprintable border.
