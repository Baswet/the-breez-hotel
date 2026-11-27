#!/usr/bin/env python3
"""Render the botanical leaf compositions for the homepage highlights band.

Original artwork, rendered procedurally: banana and canna leaves, two plants
common in Busia gardens. No photographs or third-party material are used, so
the images carry no licence obligations (see docs/ASSETS_AND_LICENSING.md).

Each leaf is shaded from a simple surface model: a midrib that bends, blade
halves that fall away from it, pleats running along the veins, banana's
vein-line splits, a glossy highlight, cast shadows and depth of field on the
leaves further back. Two compositions are written as transparent WebP:

  leaves-side   tall cluster emerging from the left edge (wide screens)
  leaves-corner low sprig across the band's top edge (tablet and phone)

Run:  python3 tools/make_botanical.py
"""
import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'assets/images/botanical'
SS = 2                                     # supersampling factor

LIGHT = np.array([0.46, -0.60, 0.66], np.float32); LIGHT /= np.linalg.norm(LIGHT)   # warm light, upper right
HALF = LIGHT + np.array([0, 0, 1], np.float32); HALF /= np.linalg.norm(HALF)


def smoothstep(a, b, x):
    t = np.clip((x - a) / (b - a), 0, 1)
    return t * t * (3 - 2 * t)


def value_noise(h, w, cell, rng):
    g = rng.random((max(2, h // cell + 2), max(2, w // cell + 2)))
    im = Image.fromarray((g * 255).astype(np.uint8), 'L').resize((w, h), Image.BICUBIC)
    return np.asarray(im, np.float32) / 255.0


def fbm(h, w, rng, cells=(90, 34, 12, 4), amps=(.5, .27, .15, .08)):
    n = sum(a * value_noise(h, w, max(1, c * SS // 2), rng) for c, a in zip(cells, amps))
    return n / sum(amps)


# Blade outlines as half-width (0..1) along the midrib, u = 0 at the base, 1 at the tip.
def banana_shape(u):
    u = np.clip(u, 0, 1)
    return np.clip(np.sin(np.pi * u), 0, 1) ** .32 * (1 - .22 * u) * (.25 + .75 * smoothstep(0, .22, u))


def canna_shape(u):
    u = np.clip(u, 0, 1)
    return np.clip(np.sin(np.pi * u ** .78), 0, 1) ** .85


# pleat: fine vein ridges; wave: the broad folds every few veins that catch the light
SPECIES = {
    'banana': dict(shape=banana_shape, vein=76, spacing=1 / 110, pleat=.035, wave=.07, wave_every=7,
                   rib=(196, 200, 140), rib_w=.07, margin=.022,
                   dark=(30, 62, 38), mid=(66, 112, 60), light=(132, 162, 84), shin=36, spec=.32),
    'canna': dict(shape=canna_shape, vein=58, spacing=1 / 46, pleat=.07, wave=.08, wave_every=3,
                  rib=(160, 176, 104), rib_w=.045, margin=.0,
                  dark=(24, 56, 34), mid=(54, 102, 56), light=(112, 152, 74), shin=44, spec=.5),
}


def render_leaf(H, W, p):
    """Return (y0, y1, x0, x1, premultiplied rgb, alpha) for one leaf on an H x W canvas."""
    rng = np.random.default_rng(p['seed'])
    sp = SPECIES[p['kind']]
    bx, by = p['base'][0] * SS, p['base'][1] * SS
    L, wmax = p['L'] * SS, p['w'] * SS
    a = math.radians(p['angle']); ca, sa = math.cos(a), math.sin(a)
    bend = p.get('bend', 0.0)

    us = np.linspace(0, 1, 80)
    xs, ys = [bx], [by]
    for sg in (-1.15, 1.15):
        lx = us * L; ly = bend * L * us ** 2 + sg * wmax
        xs += list(bx + lx * ca - ly * sa); ys += list(by + lx * sa + ly * ca)
    x0, x1 = int(max(0, min(xs) - 6)), int(min(W, max(xs) + 6))
    y0, y1 = int(max(0, min(ys) - 6)), int(min(H, max(ys) + 6))
    if x1 <= x0 or y1 <= y0:
        return None

    yy, xx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
    dx, dy = xx - bx, yy - by
    lx = dx * ca + dy * sa
    ly = -dx * sa + dy * ca
    u = lx / L
    slope = 2 * bend * u
    s = (ly - bend * L * u ** 2) / np.sqrt(1 + slope ** 2)
    side = np.where(s >= 0, 1.0, -1.0).astype(np.float32)
    ph1, ph2 = rng.uniform(0, 2 * np.pi, 2)
    wavy = 1 + sp['margin'] * (np.sin(2 * np.pi * 5.5 * u + ph1) + .6 * np.sin(2 * np.pi * 13 * u + ph2 + side))
    w = np.maximum(wmax * sp['shape'](np.clip(u, 0, 1)) * (1 + p.get('asym', .07) * side) * wavy, 1e-3)
    v = s / w
    inside = (u >= 0) & (u <= 1) & (np.abs(v) <= 1)

    # veins run out from the midrib and forward towards the tip
    tan_t = math.tan(math.radians(sp['vein']))
    spacing = L * sp['spacing']
    phi = (u * L - np.abs(s) / tan_t) / spacing

    # banana: splits that follow a vein in from the edge
    torn = np.zeros_like(inside)
    for _ in range(p.get('tears', 0)):
        pk = rng.uniform(.12, .92) * L / spacing
        sd = rng.choice([-1.0, 1.0])
        depth = rng.uniform(.22, .9)
        t = (np.abs(v) - (1 - depth)) / depth
        gap = .04 + rng.uniform(.5, 1.1) * np.clip(t, 0, 1) ** 1.6
        cut = (side == sd) & (t > 0) & (np.abs(phi - pk) < gap)
        torn |= (side == sd) & (t > 0) & (np.abs(np.abs(phi - pk) - gap) < .6)
        inside &= ~cut

    # ---- surface slopes in the leaf's own frame
    cph = np.cos(2 * np.pi * phi)
    cwv = np.cos(2 * np.pi * phi / sp['wave_every'])
    ridge = sp['pleat'] * cph + sp['wave'] * cwv
    fold, droop, arch = p.get('fold', .3), p.get('droop', .42), p.get('arch', .4)
    mw = np.maximum(sp['rib_w'] * wmax * (1 - .75 * np.clip(u, 0, 1)), 1.5 * SS)
    rib = np.exp(-(s / mw) ** 2)
    hx = arch * (1 - 2 * u) + ridge
    hy = -(fold + 3 * droop * v * v) * side - ridge * side / tan_t - .7 * (2 * s / mw) * rib
    gx, gy = hx * ca - hy * sa, hx * sa + hy * ca
    n = np.stack([-gx, -gy, np.ones_like(gx)], -1)
    n /= np.linalg.norm(n, axis=-1, keepdims=True)
    diff = np.clip(n @ LIGHT, 0, 1)
    spec = np.clip(n @ HALF, 0, 1) ** sp['shin']

    # ---- albedo
    hh, ww = yy.shape
    nz = fbm(hh, ww, rng)
    # gloss runs in streaks along the veins: it varies across them, not along them
    q1, q2 = rng.uniform(0, 2 * np.pi, 2)
    sheen = smoothstep(.15, .95, .5 + .32 * np.sin(2 * np.pi * phi / 17 + q1) + .22 * np.sin(2 * np.pi * phi / 6.3 + q2))
    sheen *= .65 + .35 * nz
    dark, mid, light = (np.array(sp[k], np.float32) for k in ('dark', 'mid', 'light'))
    uu = np.clip(u, 0, 1)
    tone = np.clip(.36 + .28 * (nz - .5) + .22 * smoothstep(.05, .7, uu) - .1 * np.abs(v), 0, 1)[..., None]
    alb = np.where(tone < .5, dark + (mid - dark) * (tone / .5), mid + (light - mid) * ((tone - .5) / .5))
    alb *= (1 + .04 * (.5 + .5 * cph) ** 8)[..., None]                                # fine veins
    alb = alb + (np.array(sp['rib'], np.float32) - alb) * (.8 * rib)[..., None]       # pale midrib
    edge = smoothstep(.84, 1, np.abs(v))[..., None]
    alb = alb + (alb * np.array([1.14, 1.12, .84], np.float32) - alb) * (.5 * edge)    # thin, yellower margin
    alb = alb + (np.array([168, 170, 104], np.float32) - alb) * (.45 * torn)[..., None]  # pale tissue at splits

    # ---- light
    col = alb * (.34 + .8 * diff[..., None])
    col += alb * np.array([.10, .22, .04], np.float32) * (.25 + .75 * edge)           # light through thin tissue
    col += sp['spec'] * (spec * (.35 + .65 * sheen))[..., None] * np.array([255, 246, 214], np.float32)
    col *= (.62 + .38 * smoothstep(0, .16, np.clip(u, 0, 1)))[..., None]              # shade at the base
    d = p.get('depth', 0.0)
    band = np.array([20, 46, 34], np.float32)
    grey = col.mean(-1, keepdims=True)
    col = col + (grey - col) * (.12 + .3 * d)                                          # natural, not candy green
    col = col * (.93 - .5 * d) + band * (.07 + .32 * d)                                # sit in the band's light
    col = np.clip(col, 0, 255)

    alpha = inside.astype(np.float32)
    return y0, y1, x0, x1, col * alpha[..., None], alpha


def to_rgba_img(rgb, a):
    arr = np.nan_to_num(np.dstack([rgb, a * 255])).clip(0, 255).astype(np.uint8)
    return Image.fromarray(arr, 'RGBa')


def over(canvas, y0, x0, rgb, a):
    h, w = a.shape
    dst = canvas[y0:y0 + h, x0:x0 + w]
    dst[..., :3] = rgb + dst[..., :3] * (1 - a[..., None])
    dst[..., 3] = a + dst[..., 3] * (1 - a)


def compose(W, H, leaves):
    Hs, Ws = H * SS, W * SS
    canvas = np.zeros((Hs, Ws, 4), np.float32)
    for p in leaves:
        r = render_leaf(Hs, Ws, p)
        if r is None:
            continue
        y0, y1, x0, x1, rgb, a = r
        # soft shadow, cast down and to the right, onto whatever lies beneath
        sig = p.get('shadow_blur', 16) * SS
        pad = int(3 * sig)
        ox, oy = int(p.get('shadow_dx', 10) * SS), int(p.get('shadow_dy', 18) * SS)
        m = Image.fromarray((a * 255).astype(np.uint8), 'L')
        big = Image.new('L', (m.width + 2 * pad, m.height + 2 * pad)); big.paste(m, (pad, pad))
        sh = np.asarray(big.filter(ImageFilter.GaussianBlur(sig)), np.float32) / 255 * p.get('shadow', .34)
        sy0, sx0 = y0 - pad + oy, x0 - pad + ox
        cy0, cx0 = max(0, sy0), max(0, sx0)
        cy1, cx1 = min(Hs, sy0 + sh.shape[0]), min(Ws, sx0 + sh.shape[1])
        if cy1 > cy0 and cx1 > cx0:
            part = sh[cy0 - sy0:cy1 - sy0, cx0 - sx0:cx1 - sx0]
            over(canvas, cy0, cx0, np.zeros(part.shape + (3,), np.float32), part)
        # depth of field on the leaves further back
        if p.get('blur'):
            im = to_rgba_img(rgb, a).filter(ImageFilter.GaussianBlur(p['blur'] * SS))
            arr = np.asarray(im, np.float32)
            rgb, a = arr[..., :3], arr[..., 3] / 255
        over(canvas, y0, x0, rgb, a)
    # supersampled -> output size, averaging in premultiplied space
    c = canvas.reshape(H, SS, W, SS, 4).mean((1, 3))
    return to_rgba_img(c[..., :3], c[..., 3]).convert('RGBA')


# Canvas units are the 2x asset's pixels. Bases sit off the left edge so the
# leaves emerge from beyond the viewport.
# The band is drawn to sit between y = 105 and 895 here (CSS pins the image so); the top
# canna crosses its upper edge and the lower canna its bottom edge, into the ivory.
SIDE = (760, 1000, [
    dict(kind='banana', base=(-120, 670), angle=-31, L=820, w=112, bend=.09, depth=.82, blur=2.4, tears=3, seed=11, shadow=.2),
    dict(kind='canna', base=(-40, 580), angle=-60, L=620, w=98, bend=.10, depth=.18, seed=14, fold=.28),
    dict(kind='banana', base=(-170, 732), angle=-9, L=780, w=116, bend=.06, depth=.04, tears=4, seed=13, fold=.34),
    dict(kind='canna', base=(-60, 750), angle=22, L=500, w=86, bend=.04, depth=.36, blur=.8, seed=12, shadow=.26, shadow_blur=12),
])

CORNER = (640, 400, [
    dict(kind='banana', base=(-90, 365), angle=-27, L=560, w=78, bend=.08, depth=.5, blur=.7, tears=3, seed=21, shadow=.2),
    dict(kind='canna', base=(-40, 335), angle=-48, L=360, w=66, bend=.10, depth=.05, seed=22, fold=.28),
    dict(kind='banana', base=(-120, 338), angle=-10, L=520, w=80, bend=.05, tears=3, seed=23, fold=.34),
])


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, (W, H, leaves) in (('leaves-side', SIDE), ('leaves-corner', CORNER)):
        im = compose(W, H, leaves)
        for scale, tag in ((1, W), (2, W // 2)):
            out = im if scale == 1 else im.convert('RGBa').resize((W // 2, H // 2), Image.LANCZOS).convert('RGBA')
            path = OUT / f'{name}-{tag}.webp'
            out.save(path, 'WEBP', quality=84, method=6)
            print(f'{path.relative_to(ROOT)}  {out.width}x{out.height}  {path.stat().st_size // 1024} KB')


if __name__ == '__main__':
    main()
