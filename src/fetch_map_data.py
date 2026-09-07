"""Download the real OpenStreetMap-derived geometry used by the book's maps.

Source: Overture Maps Foundation open data on AWS S3 (public bucket), release
2026-08-19.0.  Transportation, water and land-use features carry OSM record ids
and the ODbL-1.0 licence; building footprints are OSM plus openly licensed
ML-derived footprints.  Written out as GeoPackage layers under data/.
"""
import os, sys, json
sys.path.insert(0, os.path.dirname(__file__))
import overture
import pyarrow as pa
import numpy as np
import geopandas as gpd
import shapely

OUT = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(OUT, exist_ok=True)

HOME = (21.1990335, 72.7901332)


def bbox_around(lat, lon, metres):
    dlat = metres / 111_320.0
    dlon = metres / (111_320.0 * np.cos(np.radians(lat)))
    return (lon - dlon, lat - dlat, lon + dlon, lat + dlat)


def fetch(theme_type, bbox, columns, name):
    path = os.path.join(OUT, name + ".gpkg")
    if os.path.exists(path):
        print("skip", name)
        return gpd.read_file(path)
    print(f"[{name}] scanning {theme_type} ...", flush=True)
    tables = overture.scan(theme_type, bbox, columns=columns, verbose=False)
    if not tables:
        print("  no data")
        return None
    t = pa.concat_tables(tables)
    b = t.column("bbox").combine_chunks()
    xs = b.field("xmin").to_numpy(); Xs = b.field("xmax").to_numpy()
    ys = b.field("ymin").to_numpy(); Ys = b.field("ymax").to_numpy()
    m = (xs <= bbox[2]) & (Xs >= bbox[0]) & (ys <= bbox[3]) & (Ys >= bbox[1])
    t = t.filter(pa.array(m))
    geom = shapely.from_wkb(t.column("geometry").to_pylist())
    cols = {}
    for c in columns:
        if c in ("geometry", "bbox"):
            continue
        vals = t.column(c).to_pylist()
        if c == "names":
            vals = [(v or {}).get("primary") for v in vals]
        elif c == "sources":
            vals = [json.dumps(v)[:900] if v else None for v in vals]
        cols[c] = vals
    gdf = gpd.GeoDataFrame(cols, geometry=gpd.GeoSeries(geom, crs=4326))
    gdf.to_file(path, driver="GPKG")
    print(f"  {len(gdf)} features -> {path}", flush=True)
    return gdf


def _main():
    what = sys.argv[1] if len(sys.argv) > 1 else "bangle"
    if what == "tile":
        tile(sys.argv[2], float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5]),
             sys.argv[6].split(",") if len(sys.argv) > 6 else ("roads","buildings","water","landuse"))
        return

    if what == "bangle":
        bb = bbox_around(*HOME, 1300)
        fetch("theme=transportation/type=segment", bb,
              ["id", "subtype", "class", "names", "geometry", "bbox"], "bangle_roads")
        fetch("theme=buildings/type=building", bb,
              ["id", "subtype", "class", "height", "geometry", "bbox"], "bangle_buildings")
        fetch("theme=base/type=water", bb,
              ["id", "subtype", "class", "names", "geometry", "bbox"], "bangle_water")
        fetch("theme=base/type=land_use", bb,
              ["id", "subtype", "class", "names", "geometry", "bbox"], "bangle_landuse")

    elif what == "city":
        bb = (72.66, 21.04, 72.96, 21.30)
        fetch("theme=transportation/type=segment", bb,
              ["id", "subtype", "class", "names", "geometry", "bbox"], "city_roads")
        fetch("theme=base/type=water", bb,
              ["id", "subtype", "class", "names", "geometry", "bbox"], "city_water")

    elif what == "places":
        bb = (72.60, 21.00, 72.95, 21.28)
        fetch("theme=places/type=place", bb,
              ["id", "names", "categories", "confidence", "geometry", "bbox"], "city_places")

    elif what == "coast":
        bb = (72.55, 20.98, 73.00, 21.32)
        fetch("theme=base/type=water", bb,
              ["id", "subtype", "class", "names", "geometry", "bbox"], "coast_water")
        fetch("theme=base/type=land", bb,
              ["id", "subtype", "class", "names", "geometry", "bbox"], "coast_land")
        fetch("theme=transportation/type=segment", bb,
              ["id", "subtype", "class", "names", "geometry", "bbox"], "coast_roads")


# --- generic tile fetch ------------------------------------------------
def tile(name, lat, lon, radius_m, layers=("roads", "buildings", "water", "landuse")):
    bb = bbox_around(lat, lon, radius_m)
    spec = {
        "roads":     ("theme=transportation/type=segment",
                      ["id", "subtype", "class", "names", "geometry", "bbox"]),
        "buildings": ("theme=buildings/type=building",
                      ["id", "subtype", "class", "height", "geometry", "bbox"]),
        "water":     ("theme=base/type=water",
                      ["id", "subtype", "class", "names", "geometry", "bbox"]),
        "landuse":   ("theme=base/type=land_use",
                      ["id", "subtype", "class", "names", "geometry", "bbox"]),
        "land":      ("theme=base/type=land",
                      ["id", "subtype", "class", "names", "geometry", "bbox"]),
    }
    for lyr in layers:
        tt, cols = spec[lyr]
        fetch(tt, bb, cols, f"{name}_{lyr}")


if __name__ == "__main__":
    _main()
