"""Build SURAT_PRIVATE_EDITION.pdf.

Twelve pages, US Letter portrait, pure white, live PDF text throughout; the
maps are placed as vector PDF form XObjects produced by src/render_maps.py from
real OpenStreetMap-derived geometry.  No page is a flattened raster.
"""
import os, json, math
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pdfrw import PdfReader
from pdfrw.buildxobj import pagexobj
from pdfrw.toreportlab import makerl
from pyproj import Geod

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ASSETS = os.path.join(ROOT, "assets")
FONTS = os.path.join(ROOT, "fonts")
OUTPDF = os.path.join(ROOT, "SURAT_PRIVATE_EDITION.pdf")

PW, PH = letter                      # 612 x 792 pt
ML = MR = 54.0                       # 0.75 in text margin
MT = 54.0
MB = 54.0
COLW = PW - ML - MR                  # 504 pt

INK    = (0x11 / 255, 0x11 / 255, 0x11 / 255)
GREY   = (0x55 / 255, 0x55 / 255, 0x55 / 255)
RULE   = (0xD8 / 255, 0xD8 / 255, 0xD8 / 255)
ACCENT = (0xC4 / 255, 0x55 / 255, 0x1F / 255)

GEOD = Geod(ellps="WGS84")


# --------------------------------------------------------------- fonts
def register_fonts():
    faces = {
        "Cormorant-Light":    "CormorantGaramond-300.ttf",
        "Cormorant-Regular":  "CormorantGaramond-400.ttf",
        "Cormorant-Medium":   "CormorantGaramond-500.ttf",
        "Cormorant-SemiBold": "CormorantGaramond-600.ttf",
        "Inter-Light":        "Inter-300.ttf",
        "Inter-Regular":      "Inter-400.ttf",
        "Inter-Medium":       "Inter-500.ttf",
        "Inter-SemiBold":     "Inter-600.ttf",
        "Gujarati-Regular":   "NotoSerifGujarati-400.ttf",
        "Gujarati-SemiBold":  "NotoSerifGujarati-600.ttf",
    }
    for name, fn in faces.items():
        pdfmetrics.registerFont(TTFont(name, os.path.join(FONTS, fn)))


# ------------------------------------------------------------- drawing
def set_fill(c, rgb):
    c.setFillColorRGB(*rgb)


def swidth(s, font, size, track=0.0):
    return pdfmetrics.stringWidth(s, font, size) + track * max(len(s) - 1, 0)


def text(c, x, y, s, font="Inter-Light", size=8.6, color=INK, track=0.0):
    to = c.beginText()
    to.setTextOrigin(x, y)
    to.setFont(font, size)
    to.setFillColorRGB(*color)
    to.setCharSpace(track)          # always emit Tc: it is text state and persists
    to.textOut(s)
    c.drawText(to)


def text_right(c, x, y, s, font="Inter-Light", size=8.6, color=INK, track=0.0):
    text(c, x - swidth(s, font, size, track), y, s, font, size, color, track)


def text_center(c, x, y, s, font="Inter-Light", size=8.6, color=INK, track=0.0):
    text(c, x - swidth(s, font, size, track) / 2, y, s, font, size, color, track)


def label(c, x, y, s, size=6.4, track=1.9, color=GREY, font="Inter-Medium"):
    text(c, x, y, s.upper(), font, size, color, track)


def label_center(c, x, y, s, size=6.4, track=1.9, color=GREY, font="Inter-Medium"):
    text_center(c, x, y, s.upper(), font, size, color, track)


def headline(c, x, y, lines, size=62, leading=None, font="Cormorant-Light",
             color=INK, track=0.0):
    """y is the baseline of the first line; returns baseline of the last."""
    leading = leading or size * 0.86
    for i, ln in enumerate(lines):
        text(c, x, y - i * leading, ln, font, size, color, track)
    return y - (len(lines) - 1) * leading


def rule(c, x, y, w, color=RULE, lw=0.4):
    c.saveState()
    c.setStrokeColorRGB(*color)
    c.setLineWidth(lw)
    c.line(x, y, x + w, y)
    c.restoreState()


def wrap(s, font, size, width, track=0.0):
    words, lines, cur = s.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        tw = swidth(trial, font, size, track)
        if tw <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(c, x, y, w, s, font="Inter-Light", size=8.6, leading=13.4, color=INK,
         track=0.0):
    """y is the baseline of the first line; returns the baseline after the last."""
    for i, ln in enumerate(wrap(s, font, size, w, track)):
        text(c, x, y - i * leading, ln, font, size, color, track)
    return y - len(wrap(s, font, size, w, track)) * leading


def folio(c, n):
    text_center(c, PW / 2, MB - 22, f"{n:02d}", "Inter-Light", 6.4, GREY, 1.4)


# --------------------------------------------------------- map placement
_XOBJ = {}


def _xobj(stem):
    if stem not in _XOBJ:
        page = PdfReader(os.path.join(ASSETS, stem + ".pdf")).pages[0]
        _XOBJ[stem] = pagexobj(page)
    return _XOBJ[stem]


def place_map(c, stem, x, y, w, h=None):
    """Place a vector map PDF. The map is scaled uniformly -- never stretched --
    and centred in the box if the box aspect differs."""
    xo = _xobj(stem)
    bw = float(xo.BBox[2]) - float(xo.BBox[0])
    bh = float(xo.BBox[3]) - float(xo.BBox[1])
    if h is None:
        h = w * bh / bw
    s = min(w / bw, h / bh)
    dx = x + (w - bw * s) / 2
    dy = y + (h - bh * s) / 2
    c.saveState()
    c.translate(dx, dy)
    c.scale(s, s)
    c.doForm(makerl(c, xo))
    c.restoreState()
    return s, bw * s, bh * s


def map_scale(stem, drawn_w_pt):
    """Representative fraction of a placed map, from its real projected width."""
    j = json.load(open(os.path.join(ASSETS, stem + ".json")))
    e = j["extent"]
    metres = e[1] - e[0]
    inches = drawn_w_pt / 72.0
    return metres / (inches * 0.0254)


def rf(stem, drawn_w_pt):
    d = map_scale(stem, drawn_w_pt)
    step = 500 if d < 20000 else 5000
    d = int(round(d / step) * step)
    return f"1:{d:,}".replace(",", " ")


def km(a, b):
    return GEOD.inv(a[1], a[0], b[1], b[0])[2] / 1000.0


# ------------------------------------------------------------- geography
HOME = (21.1990335, 72.7901332)
CASTLE = (21.19619, 72.81776)
DUMAS = (21.07903, 72.71520)
BOURSE = (21.11000, 72.79505)
AIRPORT = (21.11349, 72.73417)
STATION = (21.20462, 72.84076)

OSM_LINE = "Map data © OpenStreetMap contributors, ODbL 1.0"
OVERTURE_LINE = "Geometry via Overture Maps Foundation, release 2026-08-19.0"


# =====================================================================
# pages
# =====================================================================
def page_cover(c):
    y = headline(c, ML, 470, ["SURAT"], size=136, font="Cormorant-Light")
    rule(c, ML, 440, 150)
    label(c, ML, 420, "Gujarat      India", size=8.2, track=5.4, color=INK)
    label(c, ML, 398, "A personal city book", size=6.8, track=2.6, color=GREY)

    # bottom band: the municipal area as OpenStreetMap holds it
    s, w, h = place_map(c, "map_cover", 36, 66, PW - 72, 222)
    label(c, 36, 50, "Surat municipal area · " + rf("map_cover", w),
          size=5.6, track=1.6)
    text_right(c, PW - 36, 50, OSM_LINE, "Inter-Light", 5.6, GREY, 0.4)


def page_tapi(c):
    label(c, ML, PH - MT - 6, "01 · The river")
    rule(c, ML, PH - MT - 18, COLW)
    headline(c, ML, PH - MT - 84, ["THE", "TAPI"], size=64)

    body = ("The Tapi rises near Multai, in Betul district, Madhya Pradesh, and "
            "runs about 724 km west to the Gulf of Khambhat. Surat stands on both "
            "banks, roughly 20 km upstream of the mouth. Below is the river as "
            "OpenStreetMap records it: channel, sandbanks, and the crossings that "
            "tie Adajan and Pal to the old city.")
    para(c, ML + 264, PH - MT - 84, 240, body, size=8.6, leading=13.6)

    s, w, h = place_map(c, "map_tapi", ML, MB + 42, COLW, 430)
    label(c, ML, MB + 26, "The Tapi through Surat · " + rf("map_tapi", w),
          size=5.8, track=1.6)
    text_right(c, PW - MR, MB + 26, OSM_LINE, "Inter-Light", 5.8, GREY, 0.4)
    folio(c, 2)


def page_history(c):
    label(c, ML, PH - MT - 6, "02 · The castle")
    rule(c, ML, PH - MT - 18, COLW)
    headline(c, ML, PH - MT - 84, ["LAYERS", "OF HISTORY"], size=58)

    body = ("Surat Castle was built between 1540 and 1546 by Khudawand Khan for "
            "Sultan Mahmud Shah III, to hold the river against Portuguese raids. "
            "It is a roughly square work of about an acre, with 12.2 m corner "
            "bastions and curtain walls 4.1 m thick.")
    para(c, ML, PH - MT - 190, 232, body)

    dates = [("1540–46", "Castle built for Sultan Mahmud Shah III"),
             ("1613", "English East India Company opens its first Indian factory"),
             ("1687", "The Company moves its headquarters to Bombay"),
             ("2015", "Conservation passes to the municipal corporation"),
             ("2022", "The castle reopens to the public in September")]
    y = PH - MT - 190
    for d, t in dates:
        text(c, ML + 264, y, d, "Inter-Medium", 7.0, INK, 0.8)
        lines = wrap(t, "Inter-Light", 7.6, 176)
        for i, ln in enumerate(lines):
            text(c, ML + 318, y - i * 10.4, ln, "Inter-Light", 7.6, GREY)
        y -= 12 + 10.4 * len(lines)
        rule(c, ML + 264, y + 10, 240)

    place_map(c, "map_castle", (PW - 300) / 2, MB + 46, 300, 300)
    label_center(c, PW / 2, MB + 30,
                 "Surat Castle and the old city · " + rf("map_castle", 300),
                 size=5.8, track=1.6)
    text_center(c, PW / 2, MB + 18, OSM_LINE, "Inter-Light", 5.8, GREY, 0.4)
    folio(c, 3)


def page_diamond(c):
    label(c, ML, PH - MT - 6, "03 · Khajod")
    rule(c, ML, PH - MT - 18, COLW)
    headline(c, ML, PH - MT - 84, ["DIAMOND", "CITY"], size=62)

    body = ("Rough stones arrive from Antwerp and Dubai and leave Surat cut and "
            "polished. The workshops are concentrated in Varachha, Katargam and "
            "Mahidharpura; the trade's usual estimate is that nine in ten of the "
            "world's diamonds pass through them. The Surat Diamond Bourse at "
            "Khajod opened on 17 December 2023 with about 4,500 offices in nine "
            "linked spines.")
    para(c, ML + 264, PH - MT - 194, 240, body)

    facts = [("21.1100° N   72.7951° E", "Bourse"),
             (f"{km(HOME, BOURSE):.1f} km", "Direct from Bangle"),
             ("17 . 12 . 2023", "Opened")]
    y = PH - MT - 194
    for v, k in facts:
        text(c, ML, y, v, "Inter-Light", 14, INK, 0.5)
        label(c, ML, y - 14, k, size=5.8, track=1.6)
        y -= 44
        rule(c, ML, y + 18, 232)

    place_map(c, "map_bourse", (PW - 320) / 2, MB + 44, 320, 320)
    label_center(c, PW / 2, MB + 28,
                 "Surat Diamond Bourse, Khajod · " + rf("map_bourse", 320),
                 size=5.8, track=1.6)
    text_center(c, PW / 2, MB + 16, OSM_LINE, "Inter-Light", 5.8, GREY, 0.4)
    folio(c, 4)


def page_textile(c):
    label(c, ML, PH - MT - 6, "04 · Ring Road")
    rule(c, ML, PH - MT - 18, COLW)
    headline(c, ML, PH - MT - 84, ["THE", "TEXTILE", "CITY"], size=54)

    body = ("Surat weaves, dyes and prints man-made fibre — polyester and "
            "viscose — on several hundred thousand power looms, then sells it "
            "wholesale from market buildings packed along Ring Road. Industry "
            "bodies put the city's daily output in the tens of millions of metres.")
    para(c, ML + 264, PH - MT - 84, 240, body)

    markets = ["India", "Millennium", "Raghukul", "Bombay", "Shalimar",
               "Universal", "Silk City", "Abhinandan", "Reshamwala", "Swadesi",
               "Someshwar", "New Textile Market"]
    y = PH - MT - 186
    label(c, ML + 264, y, "Market buildings on the Ring Road", size=5.8, track=1.6)
    y -= 14
    for i, m in enumerate(markets):
        col = i % 2
        row = i // 2
        text(c, ML + 264 + col * 122, y - row * 11.4, m,
             "Inter-Light", 7.4, INK)

    s, w, h = place_map(c, "map_textile", ML, MB + 44, 340, 340)
    label(c, ML, MB + 28, "Ring Road market blocks · " + rf("map_textile", w),
          size=5.8, track=1.6)
    text_right(c, PW - MR, MB + 28, OSM_LINE, "Inter-Light", 5.8, GREY, 0.4)
    folio(c, 5)


def page_bangle(c):
    label_center(c, PW / 2, PH - MT - 8, "05 · Home")
    headline(c, 0, 0, [])                       # no-op, keeps the API honest

    t = "BANGLE"
    tw = swidth(t, "Cormorant-Light", 60)
    text(c, (PW - tw) / 2, PH - MT - 74, t, "Cormorant-Light", 60, INK)
    label_center(c, PW / 2, PH - MT - 92, "Home in Surat", size=7.0, track=3.4)

    size = 468
    s, w, h = place_map(c, "BANGLE_map", (PW - size) / 2, MB + 108, size, size)

    y = MB + 84
    text_center(c, PW / 2, y, "21.1990° N", "Inter-Light", 13, INK, 1.1)
    text_center(c, PW / 2, y - 17, "72.7901° E", "Inter-Light", 13, INK, 1.1)
    label_center(c, PW / 2, y - 34, "Surat, Gujarat, India", size=6.4, track=2.6)

    rule(c, ML + 120, MB + 30, COLW - 240)
    text_center(c, PW / 2, MB + 18,
                f"1 km radius · {rf('BANGLE_map', w)} · {OSM_LINE}",
                "Inter-Light", 5.8, GREY, 0.4)
    text_center(c, PW / 2, MB + 8,
                "Rendered from OpenStreetMap geometry in the prettymaps manner",
                "Inter-Light", 5.8, GREY, 0.4)
    folio(c, 6)


DISHES = [
    ("01", "ALOOPURI",
     "Small fried puris under white-pea ragda, potato, sev and green and "
     "kokum chutney."),
    ("02", "LOCHO",
     "Steamed gram-flour batter left deliberately soft, scooped hot with "
     "butter, sev, onion and chutney."),
    ("03", "KHAVSA",
     "Surat's reading of Burmese khow suey: noodles in coconut-milk gravy, "
     "finished with crushed papdi, garlic and lime."),
    ("04", "CHEESE ANGOORI",
     "Grape-sized cheese balls in a creamy onion and tomato gravy, eaten "
     "with pav."),
]


def page_food(c):
    label(c, ML, PH - MT - 6, "06 · Street food")
    rule(c, ML, PH - MT - 18, COLW)
    headline(c, ML, PH - MT - 84, ["SURTI", "FLAVOURS"], size=60)

    intro = ("Four dishes ordered by name in Surat and almost nowhere else. "
             "Each is described from the plate rather than from a story about "
             "its origin.")
    para(c, ML + 264, PH - MT - 196, 240, intro)

    cw = (COLW - 40) / 2
    top = 440
    for i, (num, name, desc) in enumerate(DISHES):
        col, row = i % 2, i // 2
        x = ML + col * (cw + 40)
        y = top - row * 150
        rule(c, x, y + 16, cw)
        text(c, x, y - 6, num, "Inter-Medium", 6.4, GREY, 1.9)
        nsize = 28.0
        while swidth(name, "Cormorant-Regular", nsize) > cw and nsize > 16:
            nsize -= 0.5
        text(c, x, y - 42, name, "Cormorant-Regular", nsize, INK)
        para(c, x, y - 64, cw, desc, size=8.0, leading=12.6, color=GREY)

    rule(c, ML, MB + 76, COLW)
    label(c, ML, MB + 62,
          "Businesses in Surat carrying the dish in their name, OpenStreetMap",
          size=5.8, track=1.6)
    counts = [("21", "locho"), ("11", "aloopuri"), ("2", "khavsa / khausa"),
              ("1", "cheese angoori")]
    for i, (n, nm) in enumerate(counts):
        x = ML + i * (COLW / 4)
        text(c, x, MB + 40, n, "Inter-Light", 15, INK, 0.4)
        label(c, x, MB + 28, nm, size=5.8, track=1.6)
    text(c, ML, MB + 10,
         "This edition carries no photography — see the colophon.",
         "Inter-Light", 6.2, GREY, 0.3)
    folio(c, 7)


def page_dumas(c):
    label(c, ML, PH - MT - 6, "07 · The coast")
    rule(c, ML, PH - MT - 18, COLW)
    headline(c, ML, PH - MT - 84, ["DUMAS"], size=72)

    body = ("Dumas lies on the Arabian Sea about 21 km south-west of Surat by "
            "road, on the south side of the Tapi's mouth. The sand is dark, "
            "usually attributed to iron-bearing sediment. Surat airport lies "
            "about 5 km inland; the city itself is out of sight.")
    para(c, ML + 264, PH - MT - 84, 240, body)

    s, w, h = place_map(c, "map_coast", ML, MB + 176, COLW, 300)
    label(c, ML, MB + 160, "Surat to Dumas · " + rf("map_coast", w),
          size=5.8, track=1.6)
    text_right(c, PW - MR, MB + 160, OSM_LINE, "Inter-Light", 5.8, GREY, 0.4)

    y = MB + 108
    rule(c, ML, y + 22, COLW)
    label(c, ML, y + 8, "Straight-line distances, computed from coordinates",
          size=5.8, track=1.6)
    rows = [("Surat Castle", CASTLE), ("Surat Airport", AIRPORT),
            ("Surat Junction", STATION), ("Bangle", HOME)]
    for i, (nm, p) in enumerate(rows):
        x = ML + i * (COLW / 4)
        text(c, x, y - 22, f"{km(p, DUMAS):.1f} km", "Inter-Light", 15, INK, 0.4)
        label(c, x, y - 36, nm, size=5.8, track=1.6)
    rule(c, ML, y - 50, COLW)
    text(c, ML, y - 62,
         "Published road distances: about 21 km from the city, 7 km from the "
         "airport, 22 km from Surat Junction.",
         "Inter-Light", 6.6, GREY)
    folio(c, 8)


def page_today(c):
    label(c, ML, PH - MT - 6, "08 · The city")
    rule(c, ML, PH - MT - 18, COLW)
    headline(c, ML, PH - MT - 84, ["SURAT", "TODAY"], size=64)

    rule(c, ML, 566, COLW)
    facts = [("4,467,797", "Population, 2011 census"),
             ("462.1 km²", "Municipal area, after the 2020 extension"),
             ("724 km", "The Tapi, source to sea"),
             ("2 lines", "Metro under construction")]
    for i, (v, k) in enumerate(facts):
        x = ML + i * (COLW / 4)
        text(c, x, 548, v, "Inter-Light", 15, INK, 0.4)
        for j, ln in enumerate(wrap(k, "Inter-Light", 6.8, COLW / 4 - 12)):
            text(c, x, 534 - j * 9.4, ln, "Inter-Light", 6.8, GREY)
    rule(c, ML, 508, COLW)

    place_map(c, "map_city", (PW - 420) / 2, MB + 18, 420, 436)
    label(c, ML, MB + 2, "Surat street network · " + rf("map_city", 420),
          size=5.8, track=1.6)
    text_right(c, PW - MR, MB + 2, OSM_LINE, "Inter-Light", 5.8, GREY, 0.4)
    folio(c, 9)


QUARTERS = [("q_oldcity", "Old city", "Chowk and the castle"),
            ("q_ringroad", "Ring Road", "Textile market blocks"),
            ("q_pal", "Adajan", "Bangle, off Anand Mahal Road"),
            ("q_dumas", "Dumas", "The coast road")]


def page_quarters(c):
    label(c, ML, PH - MT - 6, "09 · Everyday Surat")
    rule(c, ML, PH - MT - 18, COLW)
    headline(c, ML, PH - MT - 76, ["EVERYDAY", "SURAT"], size=52)

    intro = ("Four quarters at one scale, 900 metres across. Same city, four "
             "grains: the packed lanes behind the castle, the market blocks on "
             "Ring Road, the plotted streets of Adajan, the thin edge at Dumas.")
    para(c, ML + 264, PH - MT - 76, 240, intro, size=8.2, leading=13.0)
    cap_y = PH - MT - 76 - 4 * 13.0 - 6
    text(c, ML + 264, cap_y, "Each tile 900 × 900 m · " + rf("q_pal", 200),
         "Inter-Light", 5.8, GREY, 0.4)
    text(c, ML + 264, cap_y - 10, OSM_LINE, "Inter-Light", 5.8, GREY, 0.4)

    tile = 200
    gap = COLW - 2 * tile
    for i, (stem, name, sub) in enumerate(QUARTERS):
        col, row = i % 2, i // 2
        x = ML + col * (tile + gap)
        y = 352 - row * 256
        place_map(c, stem, x, y, tile, tile)
        rule(c, x, y - 12, tile)
        text(c, x, y - 26, name, "Cormorant-Regular", 17, INK)
        text(c, x, y - 38, sub, "Inter-Light", 7.0, GREY)
    folio(c, 10)


def page_closing(c):
    t = "SURAT"
    tw = swidth(t, "Cormorant-Light", 116)
    text(c, (PW - tw) / 2, 470, t, "Cormorant-Light", 116, INK)

    g = "સુરત"
    gw = swidth(g, "Gujarati-Regular", 38)
    text(c, (PW - gw) / 2, 414, g, "Gujarati-Regular", 38, INK)

    rule(c, PW / 2 - 40, 384, 80)
    text_center(c, PW / 2, 362, "21.1990° N", "Inter-Light", 8.0, GREY, 1.2)
    text_center(c, PW / 2, 348, "72.7901° E", "Inter-Light", 8.0, GREY, 1.2)
    folio(c, 11)


def page_colophon(c):
    label(c, ML, PH - MT - 6, "Colophon and sources")
    rule(c, ML, PH - MT - 18, COLW)

    y = PH - MT - 56
    blocks = [
        ("Cartography",
         "Every map in this book is drawn from real OpenStreetMap geometry, "
         "read from the Overture Maps Foundation's open data release "
         "2026-08-19.0 (transportation, water and land-use themes carry OSM "
         "record ids and the ODbL 1.0 licence; building footprints are OSM plus "
         "openly licensed machine-derived footprints). Layers were clipped, "
         "projected to UTM zone 43N and rendered as vector PDF in the "
         "prettymaps manner: white ground, pale grey footprints, graded road "
         "hierarchy, one warm marker. No street, building or coastline on these "
         "pages was drawn by hand."),
        ("Map attribution",
         "Map data © OpenStreetMap contributors, licensed ODbL 1.0. "
         "Geometry distributed by the Overture Maps Foundation. Rendered with "
         "GeoPandas and Matplotlib in the manner of prettymaps "
         "(github.com/marceloprates/prettymaps); prettymaps itself queries the "
         "Overpass API, which was unreachable from the machine that built this "
         "book, so its rendering approach was reproduced against the same "
         "underlying OpenStreetMap data."),
        ("Photography",
         "This edition carries no photographs. The build environment's network "
         "policy blocked every source of genuinely licensed, print-resolution "
         "photography of Surat — Wikimedia Commons, Unsplash, Pexels and "
         "government media among them. Rather than fill the pages with "
         "synthesised or low-resolution imagery, the layout was changed: the "
         "book is set as an atlas, and the city supplies its own pictures in "
         "the form of its street geometry."),
        ("Typography",
         "Cormorant Garamond and Inter, both under the SIL Open Font Licence "
         "1.1, with Noto Serif Gujarati for the Gujarati title on the closing "
         "page. Numerals are set in Inter throughout: Cormorant Garamond ships "
         "old-style figures, which read badly in data. Set in live PDF text at "
         "8.5 × 11 in, with a 0.75 in type margin and nothing closer than "
         "0.42 in to the trim."),
    ]
    for title, body in blocks:
        label(c, ML, y, title, size=6.2, track=1.9, color=INK)
        y = para(c, ML, y - 16, COLW, body, size=7.4, leading=11.4, color=GREY)
        y -= 16

    rule(c, ML, y + 4, COLW)
    y -= 12
    label(c, ML, y, "Factual sources", size=6.2, track=1.9, color=INK)
    y -= 14
    srcs = [
        "Surat Castle dates, dimensions and 2022 reopening — Surat Municipal "
        "Corporation, suratmunicipal.gov.in; Wikipedia, Surat Castle.",
        "Trading history, 1613 factory and the 1687 move to Bombay — "
        "Government of Gujarat NRI division; Wikipedia, Surat Presidency.",
        "Diamond industry share and Surat Diamond Bourse, opened 17 December "
        "2023 — Wikipedia, Surat Diamond Bourse; trade press.",
        "Textile output and man-made-fibre share — Fibre2Fashion; Ministry of "
        "Textiles, txcindia.gov.in.",
        "Tapi length and source — India-WRIS; Wikipedia, Tapti River.",
        "Dumas distances — Gujarat Tourism and surat.nic.in; straight-line "
        "figures computed from coordinates in this book.",
        "Population and municipal area — Surat Municipal Corporation, "
        "Census of India 2011.",
        "Full URLs, licences and the asset manifest are in SOURCES.txt.",
    ]
    for s in srcs:
        for i, ln in enumerate(wrap("· " + s, "Inter-Light", 7.0, COLW)):
            text(c, ML + (0 if i == 0 else 8), y, ln, "Inter-Light", 7.0, GREY)
            y -= 10.2
        y -= 2

    rule(c, ML, MB + 26, COLW)
    text(c, ML, MB + 12, "Surat · A Personal City Book · Private edition",
         "Inter-Light", 6.4, GREY, 0.8)
    text_right(c, PW - MR, MB + 12, "Printed at 8.5 × 11 in",
               "Inter-Light", 6.4, GREY, 0.8)
    folio(c, 12)


PAGES = [page_cover, page_tapi, page_history, page_diamond, page_textile,
         page_bangle, page_food, page_dumas, page_today, page_quarters,
         page_closing, page_colophon]


def build():
    register_fonts()
    c = canvas.Canvas(OUTPDF, pagesize=letter)
    c.setTitle("Surat — A Personal City Book")
    c.setAuthor("Private edition")
    c.setSubject("Surat, Gujarat, India")
    for fn in PAGES:
        c.setFillColorRGB(1, 1, 1)
        c.rect(0, 0, PW, PH, stroke=0, fill=1)
        fn(c)
        c.showPage()
    c.save()
    print("wrote", OUTPDF)


if __name__ == "__main__":
    build()
