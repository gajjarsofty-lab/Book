"""Read Overture Maps GeoParquet directly from the public S3 bucket over HTTPS
range requests (no AWS SDK, no DuckDB extensions -- both are unavailable here).

Overture's transportation/water/land_use layers are derived from OpenStreetMap;
building footprints are OSM plus openly licensed ML-derived sources.
"""
import io, re, os, json, time, concurrent.futures as cf
import requests
import pyarrow.parquet as pq

BUCKET = "https://overturemaps-us-west-2.s3.amazonaws.com/"
RELEASE = "release/2026-08-19.0"

_session = requests.Session()
_session.headers["User-Agent"] = "surat-book/1.0"


def list_keys(prefix):
    keys, tok = [], None
    while True:
        u = f"{BUCKET}?list-type=2&prefix={prefix}&max-keys=1000"
        if tok:
            u += "&continuation-token=" + requests.utils.quote(tok, safe="")
        s = _session.get(u, timeout=90).text
        keys += re.findall(r"<Key>(.*?)</Key>", s)
        m = re.search(r"<NextContinuationToken>(.*?)</NextContinuationToken>", s)
        if not m:
            break
        tok = m.group(1)
    return [k for k in keys if k.endswith(".parquet")]


class RangeFile(io.RawIOBase):
    """Minimal seekable read-only file over an HTTP object with Range support."""

    def __init__(self, url, size=None):
        self.url = url
        self.pos = 0
        self._size = size if size is not None else self._head()
        self._tail = None          # cached trailing bytes (parquet footer)
        self._tail_off = None

    def _head(self):
        for attempt in range(6):
            try:
                r = _session.head(self.url, timeout=60)
                r.raise_for_status()
                return int(r.headers["Content-Length"])
            except Exception:
                if attempt == 5:
                    raise
                time.sleep(2 ** attempt)
        raise RuntimeError

    def prefetch_tail(self, n=8 << 20):
        n = min(n, self._size)
        self._tail_off = self._size - n
        self._tail = self._get(self._tail_off, self._size - 1)

    def _get(self, start, end):
        for attempt in range(5):
            try:
                r = _session.get(self.url, headers={"Range": f"bytes={start}-{end}"}, timeout=180)
                r.raise_for_status()
                return r.content
            except Exception:
                if attempt == 4:
                    raise
                time.sleep(2 ** attempt)
        raise RuntimeError

    # --- file protocol -------------------------------------------------
    def seekable(self): return True
    def readable(self): return True
    def writable(self): return False
    def tell(self): return self.pos

    def seek(self, off, whence=0):
        if whence == 0: self.pos = off
        elif whence == 1: self.pos += off
        else: self.pos = self._size + off
        return self.pos

    def size(self): return self._size

    def read(self, n=-1):
        if n is None or n < 0:
            n = self._size - self.pos
        if n == 0 or self.pos >= self._size:
            return b""
        end = min(self.pos + n, self._size) - 1
        if self._tail is not None and self.pos >= self._tail_off:
            a = self.pos - self._tail_off
            b = end - self._tail_off + 1
            data = self._tail[a:b]
        else:
            data = self._get(self.pos, end)
        self.pos += len(data)
        return data

    def readall(self): return self.read(-1)


def _stats_range(rg, prefix):
    """Return (min, max) for column path `prefix` in a row group, or None."""
    for i in range(rg.num_columns):
        col = rg.column(i)
        if col.path_in_schema == prefix and col.is_stats_set:
            st = col.statistics
            if st.has_min_max:
                return st.min, st.max
    return None


def scan(theme_type, bbox, columns=None, filt=None, max_workers=8, verbose=True):
    """bbox = (xmin, ymin, xmax, ymax). Returns list of pyarrow Tables."""
    xmin, ymin, xmax, ymax = bbox
    prefix = f"{RELEASE}/{theme_type}/"
    keys = list_keys(prefix)

    def probe(key):
        url = BUCKET + key
        f = RangeFile(url)
        f.prefetch_tail()
        pf = pq.ParquetFile(f)
        hits = []
        md = pf.metadata
        for g in range(md.num_row_groups):
            rg = md.row_group(g)
            sx = _stats_range(rg, "bbox.xmin")
            sX = _stats_range(rg, "bbox.xmax")
            sy = _stats_range(rg, "bbox.ymin")
            sY = _stats_range(rg, "bbox.ymax")
            if not (sx and sX and sy and sY):
                hits.append(g)
                continue
            if sx[0] > xmax or sX[1] < xmin or sy[0] > ymax or sY[1] < ymin:
                continue
            hits.append(g)
        return key, hits, pf, f

    tables = []
    with cf.ThreadPoolExecutor(max_workers) as ex:
        for key, hits, pf, f in ex.map(probe, keys):
            if not hits:
                continue
            if verbose:
                print(f"  {key.split('/')[-1][:20]} -> row groups {hits}", flush=True)
            t = pf.read_row_groups(hits, columns=columns)
            tables.append(t)
    return tables
