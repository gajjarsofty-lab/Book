"""Render every map in the book from the downloaded OpenStreetMap-derived data.

Nothing here is drawn by hand or invented: each layer is the real geometry read
back out of data/*.gpkg (Overture Maps' OSM-sourced transportation, water and
land-use themes plus building footprints).  Each map is written as a vector PDF
for placement in the book, an SVG, and a 300 dpi PNG, together with a small
JSON sidecar giving the projected extent so the book can place labels on top of
the map in real page coordinates.
"""
import os, sys, json, math
import numpy as np
import geopandas as gpd
import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["pdf.fonttype"] = 42
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
from shapely.geometry import Point, box

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA = os.path.join(ROOT, "data")
OUT = os.path.join(ROOT, "assets")
os.makedirs(OUT, exist_ok=True)

HOME_LAT, HOME_LON = 21.1990335, 72.7901332
CRS_M = "EPSG:32643"                       # UTM 43N, metres

INK        = "#111111"
GREY_DARK  = "#5E5E5E"
GREY_MID   = "#8A8A8A"
GREY_LIGHT = "#C7C7C7"
BUILDING   = "#E3E3E3"
BUILD_EDGE = "#CFCFCF"
WATER      = "#E4EBEF"
GREEN      = "#EEF1EB"
ACCENT     = "#C4551F"
RULE       = "#D8D8D8"

MAJOR = {"motorway", "trunk", "primary", "secondary"}
MID   = {"tertiary"}
GREENCLASSES = ["park", "meadow", "playground", "grass", "forest", "garden",
                "recreation_ground", "village_green", "nature_reserve"]


def load(name):
    p = os.path.join(DATA, name + ".gpkg")
    if not os.path.exists(p):
        return None
    g = gpd.read_file(p)
    if not len(g):
        return None
    return g.to_crs(CRS_M)


def drop_huge(g, max_km2):
    """Remove continent-scale polygons (ocean, ocean-wide reserves) that share a
    bounding box with the tile but would swamp it once clipped."""
    if g is None:
        return None
    ok = g.geometry.area <= max_km2 * 1e6
    g = g[ok]
    return g if len(g) else None


def to_m(lat, lon):
    return gpd.GeoSeries([Point(lon, lat)], crs=4326).to_crs(CRS_M).iloc[0]


def fit_extent(x0, y0, x1, y1, target_aspect):
    """Grow the projected bounds so their width/height matches the page frame
    exactly -- the map is then placed at native scale, never stretched."""
    w, h = x1 - x0, y1 - y0
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    if w / h < target_aspect:
        w = h * target_aspect
    else:
        h = w / target_aspect
    return cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2


def _save(fig, stem, extent):
    for ext in ("pdf", "svg", "png"):
        fig.savefig(os.path.join(OUT, f"{stem}.{ext}"), dpi=300,
                    facecolor="#FFFFFF", transparent=False)
    json.dump({"extent": extent, "crs": CRS_M},
              open(os.path.join(OUT, f"{stem}.json"), "w"))
    plt.close(fig)


# ---------------------------------------------------------------- tiles
def neighbourhood(prefix, stem, lat, lon, radius_m, shape="circle",
                  size=8.0, marker=None, lw_scale=1.0, frame=True,
                  show_green=True, aspect=1.0):
    """`size` is the figure width in inches; the tile is square unless a
    rectangular `aspect` (width/height) is given."""
    c = to_m(lat, lon)
    if shape == "circle":
        clip = c.buffer(radius_m)
        halfx = halfy = radius_m
    else:
        halfx, halfy = radius_m, radius_m / aspect
        clip = box(c.x - halfx, c.y - halfy, c.x + halfx, c.y + halfy)

    roads = load(prefix + "_roads")
    bldg  = load(prefix + "_buildings")
    water = drop_huge(load(prefix + "_water"), 5_000_000)
    land  = drop_huge(load(prefix + "_landuse"), 40)

    roads = gpd.clip(roads, clip) if roads is not None else None
    bldg  = gpd.clip(bldg, clip) if bldg is not None else None
    water = gpd.clip(water, clip) if water is not None else None
    land  = gpd.clip(land, clip) if land is not None else None

    fig, ax = plt.subplots(figsize=(size, size / aspect), dpi=300)
    fig.patch.set_facecolor("#FFFFFF"); ax.set_facecolor("#FFFFFF")

    if show_green and land is not None:
        parks = land[land["class"].isin(GREENCLASSES)]
        if len(parks):
            parks.plot(ax=ax, color=GREEN, linewidth=0, zorder=1)
    if water is not None and len(water):
        water.plot(ax=ax, color=WATER, linewidth=0, zorder=2)
    if bldg is not None and len(bldg):
        bldg.plot(ax=ax, color=BUILDING, linewidth=0.05 * lw_scale,
                  edgecolor=BUILD_EDGE, zorder=3)
    if roads is not None and len(roads):
        minor = roads[~roads["class"].isin(MAJOR | MID)]
        mid   = roads[roads["class"].isin(MID)]
        major = roads[roads["class"].isin(MAJOR)]
        if len(minor): minor.plot(ax=ax, color=GREY_LIGHT, linewidth=0.5 * lw_scale, zorder=4, capstyle="round")
        if len(mid):   mid.plot(ax=ax, color=GREY_MID, linewidth=1.1 * lw_scale, zorder=5, capstyle="round")
        if len(major): major.plot(ax=ax, color=INK, linewidth=1.9 * lw_scale, zorder=6, capstyle="round")

    if marker:
        mx = to_m(*marker)
        r = radius_m * 0.016
        ax.add_patch(Circle((mx.x, mx.y), r, facecolor=ACCENT, edgecolor="none", zorder=9))
        ax.add_patch(Circle((mx.x, mx.y), r * 2.8, facecolor="none",
                            edgecolor=ACCENT, linewidth=0.7, zorder=9))
    if frame and shape == "circle":
        ax.add_patch(Circle((c.x, c.y), radius_m, facecolor="none",
                            edgecolor=RULE, linewidth=0.8, zorder=10))

    pad = 1.005
    ext = [c.x - halfx * pad, c.x + halfx * pad, c.y - halfy * pad, c.y + halfy * pad]
    ax.set_xlim(ext[0], ext[1]); ax.set_ylim(ext[2], ext[3])
    ax.set_aspect("equal"); ax.set_axis_off()
    fig.subplots_adjust(0, 0, 1, 1)
    _save(fig, stem, ext)
    n_r = 0 if roads is None else len(roads)
    n_b = 0 if bldg is None else len(bldg)
    print(f"{stem}: {n_r} road segments, {n_b} building footprints")
    return ext


def city_plan(stem, bbox_ll, figsize=(7.0, 7.0), water_only=False,
              minor=True, marks=(), lw_scale=1.0):
    """bbox_ll = (lon_min, lat_min, lon_max, lat_max)."""
    ll0 = gpd.GeoSeries([box(*bbox_ll)], crs=4326).to_crs(CRS_M).iloc[0]
    ll = box(*fit_extent(*ll0.bounds, figsize[0] / figsize[1]))
    clip = ll
    roads = load("city_roads")
    water = drop_huge(load("city_water"), 6000)
    roads = gpd.clip(roads, clip) if roads is not None else None
    water = gpd.clip(water, clip) if water is not None else None

    fig, ax = plt.subplots(figsize=figsize, dpi=300)
    fig.patch.set_facecolor("#FFFFFF"); ax.set_facecolor("#FFFFFF")

    if water is not None and len(water):
        water.plot(ax=ax, color=WATER, linewidth=0, zorder=2)
    if roads is not None and not water_only:
        mn = roads[~roads["class"].isin(MAJOR | MID)]
        md = roads[roads["class"].isin(MID)]
        mj = roads[roads["class"].isin(MAJOR)]
        if minor and len(mn): mn.plot(ax=ax, color="#DCDCDC", linewidth=0.16 * lw_scale, zorder=3)
        if len(md): md.plot(ax=ax, color=GREY_LIGHT, linewidth=0.32 * lw_scale, zorder=4)
        if len(mj): mj.plot(ax=ax, color=GREY_DARK, linewidth=0.75 * lw_scale, zorder=5)

    for lat, lon in marks:
        p = to_m(lat, lon)
        ax.add_patch(Circle((p.x, p.y), (ll.bounds[2] - ll.bounds[0]) * 0.006,
                            facecolor=ACCENT, edgecolor="none", zorder=9))

    x0, y0, x1, y1 = ll.bounds
    ax.set_xlim(x0, x1); ax.set_ylim(y0, y1)
    ax.set_aspect("equal"); ax.set_axis_off()
    fig.subplots_adjust(0, 0, 1, 1)
    _save(fig, stem, [x0, x1, y0, y1])
    print(f"{stem}: city plan")
    return [x0, x1, y0, y1]


def coast_plan(stem, bbox_ll, figsize=(7.0, 7.0), marks=()):
    ll0 = gpd.GeoSeries([box(*bbox_ll)], crs=4326).to_crs(CRS_M).iloc[0]
    ll = box(*fit_extent(*ll0.bounds, figsize[0] / figsize[1]))
    water = load("coast_water")
    roads = load("coast_roads")
    water = gpd.clip(water, ll) if water is not None else None
    roads = gpd.clip(roads, ll) if roads is not None else None

    fig, ax = plt.subplots(figsize=figsize, dpi=300)
    fig.patch.set_facecolor("#FFFFFF"); ax.set_facecolor("#FFFFFF")
    if water is not None and len(water):
        water.plot(ax=ax, color=WATER, linewidth=0, zorder=1)
    if roads is not None and len(roads):
        mj = roads[roads["class"].isin(MAJOR)]
        md = roads[roads["class"].isin(MID)]
        if len(md): md.plot(ax=ax, color=GREY_LIGHT, linewidth=0.35, zorder=3)
        if len(mj): mj.plot(ax=ax, color=GREY_DARK, linewidth=0.8, zorder=4)
    for lat, lon in marks:
        p = to_m(lat, lon)
        ax.add_patch(Circle((p.x, p.y), (ll.bounds[2] - ll.bounds[0]) * 0.005,
                            facecolor=ACCENT, edgecolor="none", zorder=9))
    x0, y0, x1, y1 = ll.bounds
    ax.set_xlim(x0, x1); ax.set_ylim(y0, y1)
    ax.set_aspect("equal"); ax.set_axis_off()
    fig.subplots_adjust(0, 0, 1, 1)
    _save(fig, stem, [x0, x1, y0, y1])
    print(f"{stem}: coast plan")
    return [x0, x1, y0, y1]


SPEC = {
    # stem: callable rendering it at exactly the size its page frame needs
    "BANGLE_map":  lambda: neighbourhood("bangle", "BANGLE_map", HOME_LAT, HOME_LON,
                                         1000, marker=(HOME_LAT, HOME_LON), size=6.500),
    "map_castle":  lambda: neighbourhood("castle", "map_castle", 21.19619, 72.81776,
                                         700, marker=(21.19619, 72.81776), size=4.1667),
    "map_bourse":  lambda: neighbourhood("bourse", "map_bourse", 21.11000, 72.79505,
                                         450, marker=(21.11000, 72.79505), size=4.4444),
    "map_textile": lambda: neighbourhood("textilemkt", "map_textile", 21.18900,
                                         72.84200, 750, size=4.7222),
    "map_tapi":    lambda: city_plan("map_tapi", (72.700, 21.105, 72.905, 21.265),
                                     figsize=(7.00, 5.97)),
    "map_city":    lambda: city_plan("map_city", (72.690, 21.060, 72.925, 21.280),
                                     figsize=(5.8333, 6.0556), marks=[(HOME_LAT, HOME_LON)]),
    "map_cover":   lambda: city_plan("map_cover", (72.715, 21.135, 72.895, 21.235),
                                     figsize=(7.50, 3.08), lw_scale=0.85),
    "map_coast":   lambda: coast_plan("map_coast", (72.630, 21.040, 72.895, 21.225),
                                      figsize=(7.00, 4.17),
                                      marks=[(21.19619, 72.81776), (21.07903, 72.71520)]),
    "q_oldcity":   lambda: neighbourhood("castle", "q_oldcity", 21.19619, 72.81776, 450,
                                         shape="rect", size=2.7778, lw_scale=0.9, frame=False),
    "q_ringroad":  lambda: neighbourhood("textilemkt", "q_ringroad", 21.18900, 72.84200, 450,
                                         shape="rect", size=2.7778, lw_scale=0.9, frame=False),
    "q_pal":       lambda: neighbourhood("bangle", "q_pal", HOME_LAT, HOME_LON, 450,
                                         shape="rect", size=2.7778, lw_scale=0.9, frame=False),
    "q_dumas":     lambda: neighbourhood("dumas", "q_dumas", 21.07950, 72.71350, 450,
                                         shape="rect", size=2.7778, lw_scale=0.9, frame=False),
}


if __name__ == "__main__":
    want = sys.argv[1:] or list(SPEC)
    for k in want:
        SPEC[k]()
