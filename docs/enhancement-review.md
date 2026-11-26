# Enhancement round: deployed 26 Nov 2026

Approved and merged from `about-redesign` into `main` (merge commit f3f98d2). Published through `gh-pages` (83aa88a); the GitHub Pages run "pages-build-deployment #2" succeeded.

- Live site: https://baswet.github.io/the-breez-hotel/
- Motion lab: https://baswet.github.io/the-breez-hotel/lab/ (noindex, disallowed in robots.txt, not in the sitemap)
- Rollback: branch `rollback-live-2026-11-26` holds the previous published site (c0b7707). To restore it, force-push that branch to `gh-pages`. The `backup-2026-11-26` branch is also preserved.

This round combines four briefs: the About page redesign, the hero family, the image-composition and gallery enhancement, the scroll and motion pass, and the dining photography.

## What was preserved

- **Identity:** ivory, stone, palm green and one sandstone accent; Cormorant Garamond with Karla; the double-ruled frames; numbered kickers; the "Karibu" welcome.
- **Header, footer and mobile dock:** the Call, WhatsApp and Book dock is unchanged.
- **Every form and its behaviour:** WhatsApp and email hand-off with a reference number, date validation and a summary of nights.
- **Page structures:** Rooms spreads and the comparison table; Pools sticky story and collage; Dining menu card and bar section; Meetings spec table, layouts, events and enquiry form; the Gallery archive with filters and lightbox; Contact directions and the message form.
- **Facts on the pages:** the same verified facts. Rates, capacities, menus and hours still say "on request". Room categories are still labelled "as listed on Booking.com".

## What was improved

| Page | Change |
| --- | --- |
| Home | The full-screen hero stays. The headline now animates letter by letter, the text drifts gently on scroll, and a dates strip runs along the bottom edge. Added a marquee (Karibu · Stay · Swim · Dine · Meet · Celebrate) and an animated intro headline with the sign photo in an arch. A one-sentence statement fills in word by word as you scroll. The three separate Stay, Pools and Dining sections are replaced by **one pinned story**, "One day, five moments": an arched photo holds in place while five steps change and the background tone shifts. |
| About | Rebuilt as six short sections: hero, story, experience, property in pictures, people, closing. Uses an arched gate tag, a left-wipe and scale reveal, a water ripple on the pools panel and a circular dining panel. An arched property image opens the lightbox. The team photo sharpens from blur as it enters. |
| Rooms | The hero room photo is in an arch with a fine outline, plus a parallax detail photo and an image index (hover a category to change the photo). Added an **expanding frame**: an arched room photo grows to full width while "Rest." fades. Added a **room slideshow** with directional mask transitions, dots, arrows, keyboard and swipe. Spreads now reveal from the left. |
| Pools | Capsule-shaped photo rail with a water ripple on hover, a cool ambient glow, and the "Pools" title animating letter by letter. |
| Dining | New stock food hero with a circular juice detail, a thin ring and a warm glow. The mood strip now uses curated food photography, labelled illustrative. Added a layered **"Photographed at The Breez"** section with the hotel's own food photos. |
| Meetings | The ruled grid draws its lines in on load. The banquet layer has parallax. The title is revealed line by line through a mask. |
| Gallery | Hero mosaic with an arch and a circle, and photos that drift with the cursor. Added a **cinematic sequence with liquid displacement (WebGL)**, a **draggable film strip** ("A day, frame by frame"), a **layered garden collage** (arch, circle and rectangle) and the archive. The full-screen viewer now slides in the direction you navigate, with swipe. |
| Contact | Headline animates word by word, location lines enter one after another, and the carved sign sits in a circle with a ring. |
| Site-wide | Page-to-page fade transitions (where the browser supports them), a fill sweep on buttons and a press response. |
| New: `lab/` | Motion lab with 15 working experiments. It is set to noindex, blocked in robots.txt and left out of the sitemap. |

## Effect rules

- **Liquid displacement:** only in the gallery sequence. It is about 90 lines of vanilla WebGL and falls back to a crossfade.
- **Water ripple:** pool images only, with a desktop pointer. It does not run on touch.
- **Parallax:** one layer per composition, using transforms only.
- **Pinned sections:** two in total (Home story, Pools story), both plain CSS `position: sticky`. Scrolling is never taken over.
- **Reduced motion:** with `prefers-reduced-motion` set, everything appears in its final state. The marquee stops, the expanding frame shows full-size and the slideshow cuts rather than wipes.
- **Without JavaScript:** all text and images remain visible. Start states only apply after the script prepares an element.
- **Dependencies:** none added.

## Files

**New:**
- `src/css/heroes.css`, `src/css/motion.css`, `src/js/effects.js`
- `tools/make_motion_lab.py`, `src/lab.html`
- 20 food WebP files in `assets/images/stock/`
- `research/hero-redesign-research.md`
- `design-review/hero-directions/` (three directions, with screenshots)
- `backups/about-2026-11-26.html`

**Changed:**
- `tools/build_site.py` (heroes, About, gallery, story, slideshow, food, registry)
- `src/css/site.css` (old About rules removed)
- `src/js/site.js` (lightbox transitions and swipe; rooms image index)
- `tools/check_pages.py` (8 widths, local server)
- `docs/visual-assets-register.md`

## Testing (local server, Chromium)

- **Overflow:** none on 12 pages at 1920, 1440, 1024, 768, 430, 390, 375 and 360 px.
- **Forms:** the quick dates strip → booking page (2 nights carried over), the booking request (reference and room in the WhatsApp message), the event enquiry and the contact message all work.
- **Interactive pieces:** the mobile menu opens and closes with Escape. The room slideshow advances 01 → 02. The liquid sequence runs in WebGL mode and advances 01 → 02. The gallery filter shows 14 pool photos. The lightbox opens at "1 / 14".
- **Links:** every internal link on all pages returns 200.
- **Errors:** no JavaScript errors on any page.
- **Photo mix:** 87 hotel photos and 12 stock photos. Every stock photo is labelled "Illustrative, not The Breez" and credited.
