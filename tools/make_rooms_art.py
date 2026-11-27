#!/usr/bin/env python3
"""Artwork for the Rooms hero: torn paper, watercolour washes and paper grain.

Everything here is a shape or a texture, not a colour. The page colours each
wash through CSS (background-color seen through the mask), so the colours can
change smoothly from slide to slide. Also written:

  ambient-<key>.webp  a heavily blurred copy of each slide's photograph; the
                      light around the slideshow comes from the photo on screen
  palette.json        per-slide wash colours: measured from each photograph,
                      then blended towards that slide's art direction

All original work, generated procedurally. Run:  python3 tools/make_rooms_art.py
"""
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'assets/images/rooms-art'
RNG = np.random.default_rng(7)

# photo key -> art direction (green-family wash, gold wash, rose/earth wash, ambient light)
SLIDES = {
    'bed-detail':              ('#5E7A5A', '#DDB36A', '#DDB3A0', '#EAD6B4'),   # champagne, ivory, muted sand
    'room-four-poster-window': ('#3E6A4C', '#CFB062', '#C2B37A', '#DDE0C2'),   # botanical green, olive
    'room-grey-bedding':       ('#52705F', '#D9A86E', '#CC8C82', '#EED3C4'),   # terracotta, champagne, dusty rose
    'room-fridge-tv':          ('#24503C', '#B98444', '#C28A66', '#E5D3BB'),   # deep forest, bronze
    'bedroom-sunlit-linen':    ('#5C7C5E', '#E0B45C', '#DDBCA0', '#F2E6D2'),   # warm white, natural beige
    'nightstand-honey-wood':   ('#46684F', '#D2984F', '#D2A07C', '#ECD9C0'),   # honey wood, warm sand
}


def photo_path(key):
    for p in (ROOT / 'assets/images/stock' / f'{key}-800.webp',
              *(ROOT / 'site/images/breez').glob(f'*/{key}-800.webp'),
              *(ROOT / 'assets/images/breez').glob(f'*/{key}-800.webp')):
        if p.exists():
            return p
    raise FileNotFoundError(key)


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


def save_mask(alpha, name):
    a = (np.clip(alpha, 0, 1) * 255).astype(np.uint8)
    rgba = np.dstack([np.full_like(a, 255)] * 3 + [a])
    Image.fromarray(rgba, 'RGBA').save(OUT / f'{name}.webp', 'WEBP', quality=90, method=6)
    print(f'  {name}.webp  {a.shape[1]}x{a.shape[0]}  {(OUT / f"{name}.webp").stat().st_size // 1024} KB')


def rounded_rect_sd(w, h, inset, radius):
    """Signed distance, positive inside, to a rounded rectangle inset from the canvas edge."""
    y, x = np.mgrid[0:h, 0:w].astype(np.float32)
    cx, cy = (w - 1) / 2, (h - 1) / 2
    hx, hy = w / 2 - inset - radius, h / 2 - inset - radius
    qx, qy = np.abs(x - cx) - hx, np.abs(y - cy) - hy
    out = np.hypot(np.maximum(qx, 0), np.maximum(qy, 0)) + np.minimum(np.maximum(qx, qy), 0) - radius
    return -out


def torn(sd, h, w, big, fine, rim=False):
    """Tear an edge: wobble the boundary at two scales, add loose fibres outside it."""
    d = sd + (fbm(h, w, (90, 34), (.7, .3)) - .5) * 2 * big + (fbm(h, w, (6, 3), (.6, .4)) - .5) * 2 * fine
    core = smoothstep(-.7, .7, d)
    fib = fibres(h, w)
    halo = ((d > -4) & (d < 0)) * fib * .55 * smoothstep(-4, 0, d)
    alpha = np.maximum(core, halo)
    if rim:   # torn paper shows a paler, fibrous core along the tear
        band = smoothstep(-.7, .7, d) * (1 - smoothstep(2.5, 8, d))
        return alpha, band * (.45 + .55 * fib)
    return alpha


def blob_field(h, w, n, rng, spread=.32, size=(.16, .3)):
    y, x = np.mgrid[0:h, 0:w].astype(np.float32)
    f = np.zeros((h, w), np.float32)
    for _ in range(n):
        cx, cy = rng.uniform(.5 - spread, .5 + spread) * w, rng.uniform(.5 - spread, .5 + spread) * h
        rx, ry = rng.uniform(*size) * w, rng.uniform(*size) * h
        f += np.exp(-(((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2))
    return f / f.max()


def torn_wash(h, w, seed):
    """Torn painted paper: a hard torn outline, a dense textured interior."""
    rng = np.random.default_rng(seed)
    f = blob_field(h, w, 12, rng, spread=.36, size=(.11, .25)) + (fbm(h, w, (120, 40), (.7, .3), rng) - .5) * .55
    f += (fbm(h, w, (5, 2), (.6, .4), rng) - .5) * .06                    # fine tear on the threshold
    t = .3
    inside = smoothstep(t, t + .015, f)
    streak = np.asarray(Image.fromarray((noise(h, w, 3, rng) * 255).astype(np.uint8)).resize((w // 6, h)).resize((w, h), Image.BICUBIC), np.float32) / 255
    tex = .86 + .1 * (fbm(h, w, (60, 14), (.6, .4), rng) - .5) * 2 + .07 * (streak - .5) * 2   # brushed paint
    edge_pale = 1 - .4 * (smoothstep(t, t + .015, f) - smoothstep(t + .015, t + .05, f))     # white paper core at the tear
    return inside * np.clip(tex, 0, 1) * edge_pale


def soft_wash(h, w, seed):
    """Watercolour: pigment pools darker at the edges, granulates, and blooms."""
    rng = np.random.default_rng(seed)
    f = blob_field(h, w, 13, rng, spread=.35, size=(.11, .24)) + (fbm(h, w, (140, 50, 16), (.6, .3, .1), rng) - .5) * .6
    t = .3
    body = smoothstep(t, t + .05, f)
    ring = np.exp(-((f - t - .02) / .025) ** 2)                          # pigment pooled at the drying edge
    bloom = smoothstep(.42, .8, fbm(h, w, (70, 25), (.7, .3), rng))       # back-runs
    gran = (noise(h, w, 2, rng) - .5) * .2 + (noise(h, w, 4, rng) - .5) * .12
    a = body * (.5 + .2 * bloom + gran) + .42 * ring * smoothstep(t - .02, t + .01, f)
    soft = np.asarray(Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(.8)), np.float32) / 255
    return soft


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


# ---- the frame: one composition of torn and painted paper around the photograph -------------------
# Drawn on the box the CSS calls .rh-art (the photograph plus the artwork around it). Each layer is a
# shape only; the page paints it in the slide's colours. Boxes are fractions of that box (x0, y0, x1, y1),
# laid out after the supplied reference: deep green torn paper at the upper left and down the right,
# ochre and peach watercolour over the left, lower and upper-right edges, scraps of ivory paper between.
FW, FH = 1330, 916


def place(canvas, piece, box):
    h, w = canvas.shape
    x0, y0, x1, y1 = (int(round(v)) for v in (box[0] * w, box[1] * h, box[2] * w, box[3] * h))
    im = Image.fromarray((np.clip(piece, 0, 1) * 255).astype(np.uint8), 'L').resize((x1 - x0, y1 - y0), Image.BICUBIC)
    a = np.asarray(im, np.float32) / 255
    cx0, cy0, cx1, cy1 = max(x0, 0), max(y0, 0), min(x1, w), min(y1, h)
    if cx1 <= cx0 or cy1 <= cy0:
        return
    sub = a[cy0 - y0:cy1 - y0, cx0 - x0:cx1 - x0]
    canvas[cy0:cy1, cx0:cx1] = np.maximum(canvas[cy0:cy1, cx0:cx1], sub)


def box_sd(w, h, x0, y0, x1, y1):
    y, x = np.mgrid[0:h, 0:w].astype(np.float32)
    return -np.maximum(np.maximum(x0 - x, x - x1), np.maximum(y0 - y, y - y1))


def scrap(h, w, seed, big=10, fine=2.4):
    """A torn scrap of paper: a slightly skewed rectangle with a fibrous tear."""
    rng = np.random.default_rng(seed)
    sd = box_sd(w, h, w * .08, h * .1, w * .92, h * .9)
    y, x = np.mgrid[0:h, 0:w].astype(np.float32)
    sd = sd + (x - w / 2) * rng.uniform(-.06, .06) + (y - h / 2) * rng.uniform(-.06, .06)
    return torn(sd, h, w, big=big, fine=fine)


def field(blobs, seed, rough=.55):
    """A painted mass: soft ellipses (cx, cy, rx, ry as fractions of the frame) roughened by noise."""
    rng = np.random.default_rng(seed)
    y, x = np.mgrid[0:FH, 0:FW].astype(np.float32)
    f = np.zeros((FH, FW), np.float32)
    for cx, cy, rx, ry in blobs:
        f = np.maximum(f, np.exp(-(((x / FW - cx) / rx) ** 2 + ((y / FH - cy) / ry) ** 2)))
    d = np.minimum(np.minimum(x / FW, 1 - x / FW) * FW / FH, np.minimum(y / FH, 1 - y / FH))   # distance to the box edge
    f = f - (1 - smoothstep(.0, .06, d)) * .9                         # so every shape tears before the edge, never cut by it
    return f + (fbm(FH, FW, (150, 56, 18), (.55, .3, .15), rng) - .5) * rough, rng


def torn_mass(blobs, seed, t=.42):
    f, rng = field(blobs, seed)
    f += (fbm(FH, FW, (5, 2), (.6, .4), rng) - .5) * .05
    inside = smoothstep(t, t + .012, f)
    streak = np.asarray(Image.fromarray((noise(FH, FW, 3, rng) * 255).astype(np.uint8)).resize((FW // 7, FH)).resize((FW, FH), Image.BICUBIC), np.float32) / 255
    tex = .88 + .14 * (fbm(FH, FW, (70, 16), (.6, .4), rng) - .5) * 2 + .07 * (streak - .5) * 2
    pale = 1 - .45 * (smoothstep(t, t + .012, f) - smoothstep(t + .012, t + .04, f))   # white paper core along the tear
    return inside * np.clip(tex, 0, 1) * pale


def wash_mass(blobs, seed, t=.4, body=.62):
    f, rng = field(blobs, seed, rough=.6)
    inside = smoothstep(t, t + .04, f)
    ring = np.exp(-((f - t - .02) / .03) ** 2) * smoothstep(t - .02, t + .01, f)
    bloom = smoothstep(.42, .8, fbm(FH, FW, (80, 26), (.7, .3), rng))
    gran = (noise(FH, FW, 2, rng) - .5) * .18 + (noise(FH, FW, 5, rng) - .5) * .12
    a = inside * (body + .22 * bloom + gran) + .35 * ring
    return np.asarray(Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(.8)), np.float32) / 255


def frame():
    lay = {
        # pale sage bloom behind the photograph: upper left, and outside the right edge
        'sage': wash_mass([(.14, .0, .26, .16), (1.0, .42, .06, .4), (.40, .0, .12, .06)], 31, body=.75),
        # ochre pooled over the lower left edge, along the bottom, and across the top towards the right
        'gold': wash_mass([(.10, .62, .13, .3), (.18, .95, .17, .12), (.42, 1.0, .2, .08), (.62, .03, .19, .1),
                           (.82, .1, .1, .15), (.38, .02, .1, .07), (.02, .82, .06, .12)], 41, body=.7),
        # peach and dusty rose: the upper right corner, the lower left
        'rose': wash_mass([(.93, .07, .13, .2), (.99, .32, .05, .12), (.26, 1.0, .1, .08), (.06, .99, .07, .09)], 51, body=.7),
        # deep green torn paper: the upper left corner, down the right, the lower right
        'green': torn_mass([(.07, .17, .12, .33), (.17, .03, .12, .11), (.02, .5, .05, .2), (.99, .52, .065, .33),
                            (.97, .86, .09, .17), (.80, 1.0, .18, .085), (.94, .03, .04, .06)], 71),
    }
    lay['paper'] = torn_mass([(.42, .0, .1, .065), (.56, -.01, .07, .05), (.0, .64, .03, .1), (.55, 1.0, .09, .045), (.86, .2, .025, .06)], 61)
    for k, a in lay.items():
        save_mask(a, f'frame-{k}')
    sd = box_sd(FW, FH, FW * .075, FH * .035, FW * .93, FH * .965)
    save_mask(torn(sd, FH, FW, big=13, fine=3), 'frame-hole')

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    print('masks')
    sd = rounded_rect_sd(860, 1000, 22, 10)
    panel, rim = torn(sd, 1000, 860, big=7, fine=2.2, rim=True)
    save_mask(panel, 'mask-panel'); save_mask(rim, 'mask-rim')
    save_mask(torn_wash(640, 860, 13), 'wash-left')        # behind the panel's left edge
    frame()
    paper_tile()

    print('ambient light and palette')
    palette = {}
    for key, (g, au, ro, amb) in SLIDES.items():
        img = Image.open(photo_path(key))
        a = img.convert('RGB').resize((96, 60), Image.LANCZOS).filter(ImageFilter.GaussianBlur(7))
        a.save(OUT / f'ambient-{key}.webp', 'WEBP', quality=80)
        mean, accent = photo_tones(img)
        k = .16                                       # how far the photograph pulls each colour
        palette[key] = {
            'green': rgbhex(hexrgb(g) * (1 - k) + accent * k),
            'gold': rgbhex(hexrgb(au) * (1 - k) + accent * k),
            'rose': rgbhex(hexrgb(ro) * (1 - k) + accent * k),
            'amb': rgbhex(hexrgb(amb) * .8 + (mean * .5 + 255 * .5) * .2),
        }
        print(f'  {key:24s} {palette[key]}')
    (OUT / 'palette.json').write_text(json.dumps(palette, indent=2) + '\n')


if __name__ == '__main__':
    main()
