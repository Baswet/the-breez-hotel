# Visual design system

Source of truth: [`assets/css/tokens.css`](../assets/css/tokens.css) and [`assets/css/base.css`](../assets/css/base.css). Signature: **the courtyard frame** — an inset page frame of fine double rules, ochre corner ticks, numbered sections and a vertical "Karibu" side label.

## Layout

| Token | Value | Use |
| --- | --- | --- |
| `--page-margin` | `clamp(12px, 3.2vw, 56px)` | Frame inset around the page |
| `--gutter` | `clamp(18px, 4vw, 72px)` | Inner padding, column gaps |
| `--content-width` | `1240px` | Max content width |
| `--text-width` | `62ch` | Reading measure |
| `--section-gap` | `clamp(64px, 10vw, 160px)` | Vertical rhythm between sections |
| `--grid-gap` | `clamp(12px, 1.6vw, 24px)` | Image grids |
| Grid | 12 columns (A, C), 4 visible columns (B) | |

Margins collapse on phones: the frame inset drops to 8–12 px, asymmetric offsets become a single column, and desktop margin notes move inline.

## Lines, frames and radii

| Token | Value |
| --- | --- |
| `--border-subtle` | 1px ink at 16% |
| `--border-strong` | 1px ink |
| `--border-double` | 3px double |
| `--frame-gap` | 6px between double lines |
| `--tick` | 14px corner ticks |
| `--image-radius` | 2px (A, B) |
| `--image-radius-soft` | 22px (C) |

Reusable classes: `.frame-double`, `.ticks`, `.offset-outline`, `.rule`, `.btn--framed`.

## Colour

Sand `#F5EEE1` · Sand deep `#EADCC3` · Ochre `#C98A2E` (booking actions) · Ochre text `#9C6517` · Terracotta `#A8562F` · Cocoa `#4A3222` · Palm `#23402F` · Pool `#1C7F98` · Ink `#231B14`. Body text contrast ≥ 4.5:1 on sand.

## Typography

| Step | Size | Use |
| --- | --- | --- |
| `--step--1` | 12.8–14px | Labels (uppercase, +16% tracking) |
| `--step-0` | 16–17px | Body (line-height 1.6) |
| `--step-1` | 19–23px | Lead |
| `--step-2` | 26–38px | H3 |
| `--step-3` | 35–64px | H2 |
| `--step-4` | 45–120px | Display |

Concept pairs: A Cormorant Garamond + Karla · B Marcellus + Jost · C Fraunces + Plus Jakarta Sans.

## Images

Ratios: hero 16:9, landscape 3:2, portrait 4:5, tall 2:3, square, panorama 21:9. Treatments: full-bleed, framed (passe-partout), overlapping, offset outline, arch mask. All images lazy-load below the fold; the hero uses `fetchpriority="high"`; WebP at 800 and 1600 px.

## Buttons and links

`.btn` outline · `.btn--book` ochre (only for booking) · `.btn--framed` double outline · `.link-arrow` underlined with moving arrow. Minimum touch target 44–48 px.

## Motion

`--transition-fast` 160ms · `--transition-standard` 420ms · `--transition-slow` 900ms, all `cubic-bezier(.22,1,.36,1)`. Patterns: fade-up reveal, clip-path mask reveal, crossfade hero, drawn dividers, rotating stamp. All disabled under `prefers-reduced-motion`.

## Responsive rules

Tested at 1920, 1440, 1024, 768, 390 and 360 px with no horizontal overflow (`tools/check_pages.py`). On phones every concept adds a fixed booking/WhatsApp bar.
