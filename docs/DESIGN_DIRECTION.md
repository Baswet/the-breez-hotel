# Design direction

## Brand character

Welcoming, calm and well run. The hotel describes itself with four words — class, comfort, ambience, serenity — and the design should earn them without overselling: a confident mid-range town hotel with a pool among the palms, not a safari lodge or an international resort.

## Palette

Taken from the building and its grounds: ochre stone cladding, cream columns, dark-stained wood, palm fronds and pool water.

| Token | Hex | Use |
| --- | --- | --- |
| `sand` | `#F7F1E6` | Page ground |
| `sand-deep` | `#EFE3CC` | Alternate bands |
| `palm` | `#23402F` | Primary text accents, primary buttons, dark bands |
| `ochre` | `#C98A2E` | Booking calls to action |
| `terracotta` | `#A8562F` | Secondary accent |
| `pool` | `#1F7F98` | Small details, links on dark |
| `ink` | `#2A2118` | Body text |
| `wood` | `#1D150D` | Footer |

Text colours are chosen to meet WCAG AA contrast (4.5:1 for body text).

## Typography

- Headings: an editorial serif (Cormorant Garamond in Concept A).
- Body and interface: a clean sans-serif (Karla in Concept A), 16–17 px, line length under 70 characters.

## Three concepts under review

| Concept | Idea | Feel |
| --- | --- | --- |
| A — Ochre & Palm | Editorial: serif headlines, full-bleed hero, booking bar overlapping the hero, green and ochre bands | Calm, classic, warm |
| B — Poolside Modern | The pool as the hero: bright, geometric sans-serif, image-led cards | Fresh, friendly, leisure-led |
| C — Karibu Busia | Evening palette, Swahili welcome, emphasis on business travel, conferences and the border | Confident, corporate, local |

Ideas adapted from the reference research: a booking bar inside the hero (The Hoxton, Sarova), a top bar with call and WhatsApp (Tribe), a short brand line (Serena), a Swahili greeting (The Social House), and calm editorial pacing (Aman). Nothing is copied from any site.

## Interface rules

- Booking actions always in ochre; one primary action per section.
- Touch targets at least 44 px; visible focus states; real buttons, links and labelled inputs.
- Respect `prefers-reduced-motion`; motion limited to gentle fades and the hero slideshow.
- Any content awaiting confirmation is marked on the page, never presented as fact.
