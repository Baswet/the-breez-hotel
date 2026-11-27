#!/usr/bin/env python3
"""Artwork for the Rooms hero: painted leaves, watercolour washes and torn paper around the photographs.

One composition on the hero's stage (1600 x 900, the 16:9 box the CSS calls .rh-stage), after the supplied
reference: an organic opening for the slideshow edged with torn white paper; a band of painted leaves round it
(deep forest green at the upper left and lower right, olive and pale sage along the top and the right, ochre and
peach over the lower left, the bottom and the upper right); palm fronds hugging the left edge and a small palm
at the foot of the text; soft washes over the paper.

Nothing here has a fixed colour. Each leaf family is one image: its alpha is the shape and its grey is the
painting (0.5 = the family's own colour, darker where pigment pooled, lighter along the veins). The page fills
each family with the slide's colour and lays the painting over it (hard-light), so the leaves change colour with
the photographs. Washes are alpha masks the page fills the same way. Written to assets/images/rooms-art/:

  stage-hole.webp    the opening (alpha)          stage-rim.webp     its torn white paper edge (alpha)
  leaves-<family>    deep, olive, amber, peach    wash-<name>        amber, peach, sage, page
  paper.webp         paper grain                  palette.json       each slide's colours

All original work, generated procedurally (no photographs or third-party material). Run:
    python3 tools/make_rooms_art.py
"""
import json
import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'assets/images/rooms-art'
RNG = np.random.default_rng(7)
CW, CH = 1600, 900                         # the stage
HOLE = (.355, .118, .968, .886)            # the opening's box, fractions of the stage (the CSS places the photographs to match)
FAMILIES = ('deep', 'olive', 'amber', 'peach')

# photo key -> art direction: deep green, ochre, peach, the light on the paper. The same families on every
# slide, moved gently towards each photograph's mood (warm interior, garden green, sunlit, evening).
SLIDES = {
    'bed-detail':              ('#4E6E4C', '#D8A752', '#E3A684', '#F1DDBF'),   # champagne, caramel, warm ivory
    'room-four-poster-window': ('#3E6544', '#CFA24E', '#DDA37E', '#E9E2C6'),   # forest green, olive, botanical cream
    'room-grey-bedding':       ('#4F6A55', '#D29C5E', '#E39A85', '#F2D9C8'),   # peach, sand, muted amber
    'room-fridge-tv':          ('#2F4F37', '#BE8641', '#CF9068', '#E8D5BB'),   # deep olive, warm brown, subdued champagne
    'bedroom-sunlit-linen':    ('#587A57', '#E0B055', '#EEB08C', '#F5E7CF'),   # sunlit: peach, sand, amber
    'nightstand-honey-wood':   ('#435F45', '#CB9046', '#D99D74', '#EEDABE'),   # honey wood, caramel
}


def photo_path(key):
    for p in (ROOT / 'assets/images/stock' / f'{key}-800.webp',
              *(ROOT / 'site/images/breez').glob(f'*/{key}-800.webp'),
              *(ROOT / 'assets/images/breez').glob(f'*/{key}-800.webp')):
        if p.exists():
            return p
    raise FileNotFoundError(key)


# ---- noise ---------------------------------------------------------------------------------------------
def smoothstep(a, b, x):
    t = np.clip((x - a) / (b - a), 0, 1)
    return t * t * (3 - 2 * t)


def noise(h, w, cell, rng=RNG):
    g = rng.random((max(2, h // cell + 3), max(2, w // cell + 3)))
    im = Image.fromarray((g * 255).astype(np.uint8), 'L').resize((w + 2 * cell, h + 2 * cell), Image.BICUBIC)
    return np.asarray(im, np.float32)[cell:cell + h, cell:cell + w] / 255.0


def fbm(h, w, cells, amps, rng=RNG):
    return sum(a * noise(h, w, c, rng) for c, a in zip(cells, amps)) / sum(amps)


def fibres(h, w, rng=RNG):
    """Short paper fibres: thin streaks of noise stretched in two directions."""
    a = np.asarray(Image.fromarray((noise(h, w, 2, rng) * 255).astype(np.uint8)).filter(ImageFilter.BoxBlur(1)), np.float32) / 255
    return np.clip((a - .45) * 3, 0, 1)


def curve1d(n, cells, rng):
    """A smooth random curve of n samples, about -1..1."""
    out = np.zeros(n, np.float32)
    for c, a in cells:
        k = max(2, n // c + 3)
        out += a * np.interp(np.arange(n) / c + 1, np.arange(k), rng.uniform(-1, 1, k))
    return out


# ---- a painted leaf ------------------------------------------------------------------------------------
PROFILES = {   # half-width along the leaf, stem (0) to tip (1)
    'ovate': lambda t: np.clip(np.sin(np.pi * t ** .8), 0, 1) ** .75,
    'lance': lambda t: np.clip(np.sin(np.pi * t ** .72), 0, 1) ** 1.05,
    'broad': lambda t: np.clip(np.sin(np.pi * t), 0, 1) ** .55,
    'blade': lambda t: np.clip(1 - t, 0, 1) ** .9 * np.minimum(1, t * 7) ** .6,      # a palm leaflet
}


def leaf(length, width, rng, kind='ovate', bow=0., rough=.05, tear=0., veins=10, glaze=1., light=-1):
    """One watercolour leaf, stem at the bottom. Returns (alpha, paint): paint is about 0.5 for the family's
    colour, darker where the pigment pooled at the drying edge and towards the stem, lighter along the veins."""
    pad = int(width * .35) + 6
    L = int(length)
    H, W = L + 2 * pad, int(width * 1.1 + abs(bow) * width) + 2 * pad
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    t = 1 - (yy - pad) / L
    tc = np.clip(t, 0, 1)
    with np.errstate(invalid='ignore'):
        hw = width / 2 * np.nan_to_num(PROFILES[kind](tc))
    row = np.clip((yy[:, 0] - pad).astype(int), 0, L - 1)
    edge = lambda: curve1d(L, [(L // 5 + 2, .6), (L // 14 + 2, .3), (6, .1)], rng)[row][:, None]
    wl, wr = 1 + rough * edge(), 1 + rough * edge()
    if tear:   # a torn rather than a cut edge
        wl = wl + tear * curve1d(L, [(3, .7), (2, .3)], rng)[row][:, None]
        wr = wr + tear * curve1d(L, [(3, .7), (2, .3)], rng)[row][:, None]
    axis = W / 2 - bow * width * 4 * (tc ** 2 - tc)
    dx = xx - axis
    half = np.where(dx < 0, hw * wl, hw * wr)
    e = half - np.abs(dx)                                  # px to the edge, positive inside
    alpha = smoothstep(-.9, .9, e) * ((t > 0) & (t < 1))
    alpha = np.maximum(alpha, ((t <= 0) & (t > -.06) & (np.abs(dx) < max(1.2, width * .018))) * .9)   # the stem
    s = dx / np.maximum(half, 1)
    d = np.clip(e, 0, None)
    sh = (fbm(H, W, (max(10, int(width * .9)), max(5, int(width * .35)), 6), (.5, .32, .18), rng) - .5) * .28   # mottled pigment
    sh += -.2 * np.exp(-d / 2.6) + .06 * np.exp(-d / 12)  # pooled at the drying edge
    sh += .11 * light * s                                  # one half in shade
    sh += -.08 * (1 - tc) + .04 * tc                       # deeper towards the stem
    sh += .1 * np.exp(-(dx ** 2) / (2 * max(1., width * .012) ** 2)) * (1 - tc * .8)   # pale midrib, lifted out
    if veins:
        ph = tc * veins - np.abs(s) * 1.1                 # side veins sweeping up to the edge
        vd = np.abs(ph - np.round(ph)) * (L / veins)
        sh += .03 * np.exp(-(vd ** 2) / 1.6) * (np.abs(s) < .92) * (np.abs(s) > .04)
    sh += (noise(H, W, 2, rng) - .5) * .09                  # granulation
    for _ in range(rng.integers(0, 3)):                    # a back-run bloom
        cx, cy, r = rng.uniform(.3, .7) * W, rng.uniform(.25, .75) * H, rng.uniform(.12, .3) * width
        rr = np.hypot(xx - cx, yy - cy)
        sh += .05 * smoothstep(r, r * .2, rr) - .035 * np.exp(-((rr - r) / 2.5) ** 2)
    return alpha * glaze, np.clip(.5 + sh, .08, .95)


def frond(length, rng, n=26, leaflet=(.42, .055), droop=.25):
    """A palm frond: leaflets either side of a curved rachis, stem at the bottom centre."""
    W, H = int(length * 1.3), int(length * 1.15)
    A = np.zeros((H, W), np.float32); S = np.full((H, W), .5, np.float32)
    p0 = np.array([W / 2, H - 8.]); p1 = np.array([W / 2 - length * .08, H - 8 - length * .55])
    p2 = np.array([W / 2 + length * .25, H - 8 - length * .95])
    at = lambda u: (1 - u) ** 2 * p0 + 2 * (1 - u) * u * p1 + u ** 2 * p2
    for i in range(n):
        u = .1 + .9 * i / (n - 1)
        p, q = at(u), at(min(1, u + .01))
        ang = math.degrees(math.atan2(q[0] - p[0], -(q[1] - p[1])))
        size = math.sin(math.pi * (.15 + .8 * u)) ** .7
        for side in (-1, 1):
            a, s = leaf(length * leaflet[0] * size * rng.uniform(.85, 1.1), length * leaflet[1] * (.8 + .4 * size) * rng.uniform(.85, 1.15),
                        rng, 'blade', bow=side * rng.uniform(.04, .12), rough=.04, veins=0, light=side)
            paste(A, S, a, s, p[0], p[1], ang + side * (40 - 14 * u + droop * 30 * (1 - u)) + rng.uniform(-6, 6), 'stem')
    for k in range(200):                                    # the rachis
        p = at(k / 199); r = max(1., length * .006 * (1 - k / 199 * .7))
        y0, x0 = int(p[1]), int(p[0])
        A[max(0, y0 - 2):y0 + 2, max(0, x0 - int(r)):x0 + int(r) + 1] = .95
        S[max(0, y0 - 2):y0 + 2, max(0, x0 - int(r)):x0 + int(r) + 1] = .42
    return A, S


def rotate(arr, deg, fill):
    return np.asarray(Image.fromarray(arr.astype(np.float32), 'F').rotate(deg, resample=Image.BICUBIC, expand=True, fillcolor=fill), np.float32)


def paste(A, S, a, s, x, y, deg=0., anchor='centre'):
    """Paint a leaf onto a family (A alpha, S paint) at (x, y), turned deg clockwise; 'stem' puts the stem there."""
    h, w = a.shape
    vx, vy = (0., h * .44) if anchor == 'stem' else (0., 0.)
    ra, rs = rotate(a, -deg, 0.), rotate(s, -deg, .5)
    th = math.radians(deg)
    cx, cy = x - (vx * math.cos(th) - vy * math.sin(th)), y - (vx * math.sin(th) + vy * math.cos(th))
    H, W = A.shape; rh, rw = ra.shape
    x0, y0 = int(round(cx - rw / 2)), int(round(cy - rh / 2))
    cx0, cy0, cx1, cy1 = max(x0, 0), max(y0, 0), min(x0 + rw, W), min(y0 + rh, H)
    if cx1 <= cx0 or cy1 <= cy0:
        return None
    sa = np.clip(ra[cy0 - y0:cy1 - y0, cx0 - x0:cx1 - x0], 0, 1); ss = rs[cy0 - y0:cy1 - y0, cx0 - x0:cx1 - x0]
    ao, so = A[cy0:cy1, cx0:cx1], S[cy0:cy1, cx0:cx1]
    an = sa + ao * (1 - sa)
    S[cy0:cy1, cx0:cx1] = np.where(an > 1e-4, (ss * sa + so * ao * (1 - sa)) / np.maximum(an, 1e-4), so)
    A[cy0:cy1, cx0:cx1] = an
    return cx0, cy0, cx1, cy1, sa


class Leaves:
    """The four leaf families on the stage. A leaf painted later covers the ones beneath it, whatever their family."""
    GLAZE = {'deep': 1.0, 'olive': 1.0, 'sage': .94, 'amber': .96, 'peach': .95}
    LIFT = {'deep': .03, 'olive': .04, 'sage': .22, 'amber': .1, 'peach': .1}   # amber and peach painted lighter, sage is pale olive

    def __init__(self):
        self.A = {f: np.zeros((CH, CW), np.float32) for f in FAMILIES}
        self.S = {f: np.full((CH, CW), .5, np.float32) for f in FAMILIES}

    def put(self, fam, a, s, x, y, deg, anchor='centre', lift=0.):
        f = 'olive' if fam == 'sage' else fam
        box = paste(self.A[f], self.S[f], a, np.clip(s + self.LIFT[fam] + lift, .05, .97), x, y, deg, anchor)
        if box:
            cx0, cy0, cx1, cy1, sa = box
            for o in FAMILIES:
                if o != f:
                    self.A[o][cy0:cy1, cx0:cx1] *= (1 - sa)


# ---- the composition ------------------------------------------------------------------------------------
def opening(rng):
    """Signed distance to the opening (positive inside): a squarish oval, unevenly drawn."""
    y, x = np.mgrid[0:CH, 0:CW].astype(np.float32)
    x0, y0, x1, y1 = HOLE[0] * CW, HOLE[1] * CH, HOLE[2] * CW, HOLE[3] * CH
    cx, cy, rx, ry = (x0 + x1) / 2, (y0 + y1) / 2, (x1 - x0) / 2, (y1 - y0) / 2
    r = (np.abs((x - cx) / rx) ** 3.4 + np.abs((y - cy) / ry) ** 3.4) ** (1 / 3.4)
    return (1 - r) * min(rx, ry) + (fbm(CH, CW, (260, 110, 40), (.55, .3, .15), rng) - .5) * 52


def edge_points(sd, n, rng):
    """Points on the opening's edge, walking round it, with the outward direction."""
    cx, cy = (HOLE[0] + HOLE[2]) / 2 * CW, (HOLE[1] + HOLE[3]) / 2 * CH
    out = []
    for i in range(n):
        th = 2 * math.pi * (i + rng.uniform(-.35, .35)) / n
        for k in range(0, 1200, 2):
            px, py = cx + math.cos(th) * k, cy + math.sin(th) * k
            if not (0 <= px < CW and 0 <= py < CH):
                break
            if sd[int(py), int(px)] < 0:
                out.append((px, py, th)); break
    return out


def family_at(fx, fy, rng):
    """Colour family by place round the opening, after the reference."""
    r = rng.random()
    if fy < .38 and fx < .52: return 'deep' if r < .72 else 'olive'                                  # upper left: forest green
    if fy < .22 and fx < .76: return 'olive' if r < .6 else ('amber' if r < .85 else 'sage')         # along the top
    if fy < .4:               return 'peach' if r < .6 else 'amber'                                  # upper right: peach, amber
    if fx > .86 and fy < .78: return 'olive' if r < .45 else 'deep'                                  # down the right
    if fx > .7 and fy >= .78: return 'deep' if r < .65 else 'olive'                                  # lower right
    if fy > .8 and fx > .52:  return 'amber' if r < .45 else ('peach' if r < .75 else 'deep')        # along the bottom
    if fy > .62:              return 'amber' if r < .5 else 'peach'                                  # lower left
    return 'olive' if r < .55 else ('amber' if r < .8 else 'deep')                                   # the left edge


def edge_leaves(lv, sd, rng):
    for x, y, th in edge_points(sd, 14, rng):              # sprigs of palm among the leaves
        fx, fy = x / CW, y / CH
        if (.3 < fy < .7 and fx > .5) or (fx < .42 and fy < .8):
            continue
        f = family_at(fx, fy, rng)
        f = 'deep' if f in ('amber', 'peach') and rng.random() < .5 else f
        a, s = frond(rng.uniform(150, 230), rng, n=16, leaflet=(.45, .05), droop=.2)
        lv.put(f, a, s, x + math.cos(th) * 60, y + math.sin(th) * 60, math.degrees(th) + 90 + rng.uniform(-50, 50), 'stem')
    pts = edge_points(sd, 64, rng) + [p for p in edge_points(sd, 56, rng) if (p[0] / CW < .55 and p[1] / CH < .45) or p[0] / CW > .9]
    for i in rng.permutation(len(pts)):
        x, y, th = pts[i]
        f = family_at(x / CW, y / CH, rng)
        kind = rng.choice(['ovate', 'ovate', 'broad', 'lance', 'lance'])
        left = x / CW < .42                                 # the side facing the words: a slimmer band
        foot = y / CH > .8 and .44 < x / CW < .76           # and under the photograph, where the motto runs
        if foot and rng.random() < .45:
            continue
        L = (rng.uniform(65, 105) if rng.random() < .3 else rng.uniform(100, 185)) * (1.1 if f == 'deep' else 1) * (1.2 if kind == 'lance' else 1) * (.8 if left else 1) * (.75 if foot else 1)
        w = L * {'ovate': .52, 'broad': .68, 'lance': .32}[kind] * rng.uniform(.85, 1.15)
        a, s = leaf(L, w, rng, kind, bow=rng.uniform(-.14, .14), rough=.07, tear=rng.choice([0, .02, .04]),
                    veins=int(rng.integers(7, 12)), light=rng.choice([-1, 1]), glaze=Leaves.GLAZE[f])
        turn = math.degrees(th) + 90 + (rng.uniform(-30, 30) if (left or rng.random() > .3) else 90 * rng.choice([-1, 1]) * rng.uniform(.5, .9))
        off = (rng.uniform(.18, .42) if rng.random() < .82 else rng.uniform(.04, .16)) * L * (.7 if left or foot else 1)   # mostly outside the edge
        lv.put(f, a, s, x + math.cos(th) * off, y + math.sin(th) * off, turn)


def outer_leaves(lv, rng):
    for x, y, deg, L, f in [(-40, 330, 14, 300, 'deep'), (-50, 640, 10, 330, 'olive'), (-70, 1000, 14, 300, 'deep'), (-30, 40, 150, 220, 'olive')]:
        a, s = frond(L, rng, n=28, leaflet=(.4, .034), droop=.35)             # palm fronds hugging the left edge
        lv.put(f, a, s, x, y, deg, 'stem')
    a, s = leaf(210, 88, rng, 'ovate', bow=.1, rough=.05, veins=11)
    lv.put('deep', a, s, 20, 935, 14, 'stem')
    a, s = frond(230, rng, n=20, leaflet=(.48, .045), droop=.2)                # a small palm at the foot of the text
    lv.put('olive', a, s, 590, 905, -24, 'stem')
    a, s = frond(180, rng, n=16, leaflet=(.48, .045), droop=.2)
    lv.put('olive', a, s, 620, 905, 22, 'stem', lift=.08)
    for x, y, deg, L in [(520, 50, 70, 150), (650, 22, 112, 130)]:            # pale leaves along the top
        a, s = leaf(L, L * .46, rng, 'ovate', bow=.08, rough=.05, glaze=.7)
        lv.put('sage', a, s, x, y, deg)
    for x, y, deg, L in [(1560, 905, -55, 230), (1610, 840, -95, 200)]:       # deep green off the lower right corner
        a, s = leaf(L, L * .44, rng, 'ovate', bow=.1, rough=.05, veins=11)
        lv.put('deep', a, s, x, y, deg, 'stem')
    a, s = leaf(200, 100, rng, 'ovate', bow=.1, glaze=.85)                    # a peach leaf at the right edge
    lv.put('peach', a, s, 1612, 250, -70, 'stem')


def wash(blobs, rng, rough=.55, t=.38):
    """Watercolour: soft masses (cx, cy, rx, ry in stage fractions) with a pooled edge, blooms and granulation."""
    y, x = np.mgrid[0:CH, 0:CW].astype(np.float32)
    f = np.zeros((CH, CW), np.float32)
    for cx, cy, rx, ry in blobs:
        f = np.maximum(f, np.exp(-(((x / CW - cx) / rx) ** 2 + ((y / CH - cy) / ry) ** 2)))
    f = f + (fbm(CH, CW, (170, 60, 20), (.55, .3, .15), rng) - .5) * rough
    inside = smoothstep(t, t + .05, f)
    ring = np.exp(-((f - t - .02) / .03) ** 2) * smoothstep(t - .02, t + .01, f)
    bloom = smoothstep(.42, .8, fbm(CH, CW, (90, 30), (.7, .3), rng))
    gran = (noise(CH, CW, 2, rng) - .5) * .14 + (noise(CH, CW, 5, rng) - .5) * .1
    a = inside * (.5 + .22 * bloom + gran) + .3 * ring
    return np.asarray(Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1)), np.float32) / 255


def save_alpha(a, name):
    a8 = (np.clip(a, 0, 1) * 255).astype(np.uint8)
    Image.fromarray(np.dstack([np.full_like(a8, 255)] * 3 + [a8]), 'RGBA').save(OUT / f'{name}.webp', 'WEBP', quality=82, method=6)
    print(f'  {name}.webp  {(OUT / f"{name}.webp").stat().st_size // 1024} KB')


def save_painted(a, s, name):
    a8 = (np.clip(a, 0, 1) * 255).astype(np.uint8)
    g8 = (np.clip(s, 0, 1) * 255).astype(np.uint8)
    Image.fromarray(np.dstack([g8, g8, g8, a8]), 'RGBA').save(OUT / f'{name}.webp', 'WEBP', quality=80, method=6)
    print(f'  {name}.webp  {(OUT / f"{name}.webp").stat().st_size // 1024} KB')


def stage():
    rng = np.random.default_rng(11)
    sd = opening(rng)
    d = sd + (fbm(CH, CW, (30, 9), (.7, .3), rng) - .5) * 10 + (fbm(CH, CW, (4, 2), (.6, .4), rng) - .5) * 4.4   # torn, not cut
    save_alpha(smoothstep(-.8, .8, d), 'stage-hole')
    fib = fibres(CH, CW, rng)
    rim = smoothstep(-18, -13, d) * (1 - smoothstep(-.8, .8, d)) * (.75 + .25 * fib)
    save_alpha(np.maximum(rim, ((d > -22) & (d < -16)) * fib * .5), 'stage-rim')
    lv = Leaves()
    outer_leaves(lv, rng)
    edge_leaves(lv, sd, rng)
    for f in FAMILIES:
        save_painted(lv.A[f], lv.S[f], f'leaves-{f}')
    for name, blobs, kw in [
        ('amber', [(.36, .7, .07, .2), (.5, .93, .14, .07), (.66, .1, .12, .07), (.08, .95, .12, .1), (.92, .12, .07, .08)], {}),
        ('peach', [(.9, .14, .11, .15), (.98, .4, .04, .12), (.42, .92, .07, .07), (.3, .82, .05, .06), (1.0, .0, .12, .1)], {}),
        ('sage', [(.42, .12, .12, .1), (.99, .62, .04, .2), (.25, .02, .1, .05)], {}),
        ('page', [(.12, .06, .2, .14), (.86, .04, .2, .1), (.16, .97, .22, .1), (.02, .55, .06, .26)], {'rough': .6, 't': .34}),
    ]:
        save_alpha(wash(blobs, rng, **kw), f'wash-{name}')


# ---- paper and palette ----------------------------------------------------------------------------------
def paper_tile(n=512):
    """Tileable warm paper grain, near white: it is multiplied over colour, so white means 'no change'."""
    rng = np.random.default_rng(3)
    base = np.zeros((n, n), np.float32)
    for cell, amp in ((64, .35), (16, .3), (4, .2), (2, .15)):
        g = rng.random((n // cell, n // cell))
        g = np.tile(g, (3, 3))
        im = Image.fromarray((g * 255).astype(np.uint8), 'L').resize((n * 3, n * 3), Image.BICUBIC)
        base += amp * np.asarray(im, np.float32)[n:2 * n, n:2 * n] / 255
    fib = np.tile(fibres(n, n, rng), (1, 1))
    v = .955 + (base - .5) * .09 - fib * .05
    rgb = np.dstack([v * 255, v * 252, v * 245])
    Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8), 'RGB').save(OUT / 'paper.webp', 'WEBP', quality=86, method=6)
    print(f'  paper.webp  {n}x{n}  {(OUT / "paper.webp").stat().st_size // 1024} KB')


def hexrgb(h):
    return np.array([int(h[i:i + 2], 16) for i in (1, 3, 5)], np.float32)


def rgbhex(c):
    return '#' + ''.join(f'{int(round(v)):02X}' for v in np.clip(c, 0, 255))


def photo_tones(img):
    """The photograph's mean colour and its most saturated mid-tone."""
    small = img.convert('RGB').resize((64, 40), Image.LANCZOS)
    px = np.asarray(small, np.float32).reshape(-1, 3)
    mean = px.mean(0)
    mx, mn = px.max(1), px.min(1)
    sat = (mx - mn) / np.maximum(mx, 1)
    lum = px @ np.array([.299, .587, .114], np.float32)
    mid = (lum > 50) & (lum < 215)
    accent = px[mid][np.argsort(sat[mid])[-max(1, mid.sum() // 12):]].mean(0) if mid.any() else mean
    return mean, accent


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    print('stage')
    stage()
    paper_tile()
    print('palette')
    palette = {}
    for key, (g, au, ro, amb) in SLIDES.items():
        mean, accent = photo_tones(Image.open(photo_path(key)))
        k = .1                                        # how far each photograph pulls its colours
        palette[key] = {
            'green': rgbhex(hexrgb(g) * (1 - k) + accent * k),
            'gold': rgbhex(hexrgb(au) * (1 - k) + accent * k),
            'rose': rgbhex(hexrgb(ro) * (1 - k) + accent * k),
            'amb': rgbhex(hexrgb(amb) * .85 + (mean * .5 + 255 * .5) * .15),
        }
        print(f'  {key:24s} {palette[key]}')
    (OUT / 'palette.json').write_text(json.dumps(palette, indent=2) + '\n')


if __name__ == '__main__':
    main()
