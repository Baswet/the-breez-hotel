"""Generate /design-laboratory/index.html — side-by-side variations of each technique."""
import json, os, html as H
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = "../assets/images/breez/"
P = {
 "court": A+"gardens/cottage-courtyard-swing-1600.webp", "pool": A+"pools/pool-umbrellas-above-1600.webp",
 "pool2": A+"pools/pool-terrace-kids-pool-1600.webp", "room": A+"rooms/room-four-poster-window-1600.webp",
 "room2": A+"rooms/room-grey-bedding-1600.webp", "sign": A+"exterior/sign-the-breeze-hotel-karibu-1600.webp",
 "bld": A+"exterior/building-palms-umbrellas-1600.webp", "dine": A+"dining/poolside-meal-juice-1600.webp",
 "conf": A+"conference/hall-classroom-setup-1600.webp", "gaz": A+"gardens/gazebo-cypress-1600.webp",
 "fount": A+"gardens/courtyard-lawn-fountain-1600.webp", "bar": A+"dining/bar-counter-stools-1600.webp",
}
xps = json.load(open(os.path.join(ROOT, "research/design-experiments/experiments.json")))
def im(k, alt=""): return f'<img src="{P[k]}" alt="{H.escape(alt)}" loading="lazy">'
def card(name, demo, note): return f'<figure class="v"><div class="demo">{demo}</div><figcaption><strong>{name}</strong><span>{note}</span></figcaption></figure>'
def iframe(slug, name, note): return f'<figure class="v v--frame"><div class="demo"><iframe src="../research/design-experiments/{slug}/index.html" title="{H.escape(name)}" loading="lazy"></iframe></div><figcaption><strong>{name}</strong><span>{note} · <a href="../research/design-experiments/{slug}/index.html">open full size</a></span></figcaption></figure>'

labs = []
labs.append(("layout","Layout lab","Six page structures. The courtyard-frame family (inset, editorial, asymmetric) is the signature; full-bleed is reserved for heroes.",[
  iframe("01-editorial-margin-layout","Editorial margins","Narrow measure, notes in the margin"),
  iframe("12-architectural-grid","Architectural grid","Visible hairline cells"),
  iframe("11-split-screen-introduction","Split screen","Photo half, text half"),
  iframe("25-asymmetric-section-margins","Asymmetric sections","Alternating wide/narrow"),
  iframe("03-asymmetric-hotel-gallery","Asymmetric mosaic","12-column offset grid"),
  iframe("18-horizontal-experience-gallery","Horizontal story","Scroll-snap sideways"),
]))
labs.append(("margins","Margin lab","Same content, six margin systems. Watch how the photograph's relationship to the page edge changes the mood.",[
  card("Full-bleed", f'<div class="m m-full">{im("court")}</div>', "0 px — immersive, for heroes"),
  card("Wide inset", f'<div class="m m-wide">{im("court")}</div>', "page-margin ≈ 3vw"),
  card("Narrow editorial", f'<div class="m m-narrow">{im("court")}<p>Reading column with generous margins.</p></div>', "62ch column, 20% margins"),
  card("Asymmetric", f'<div class="m m-asym">{im("court")}</div>', "left 30% · right 6%"),
  card("Double-framed", f'<div class="m m-double"><div>{im("court")}</div></div>', "mat + double rule (signature)"),
  card("Floating", f'<div class="m m-float">{im("court")}</div>', "small object in big space"),
]))
labs.append(("borders","Border lab","Fine lines are the house ornament: they reference the cream columns and window bands of the building.",[
  card("Single hairline", f'<div class="b b-1">{im("room")}</div>', "1px ink at 16%"),
  card("Double rule", f'<div class="b b-2">{im("room")}</div>', "1px + 6px gap + 1px"),
  card("Offset outline", f'<div class="b b-3">{im("room")}</div>', "ochre outline shifted 14px"),
  card("Rounded frame", f'<div class="b b-4">{im("room")}</div>', "22px radius, paper mat"),
  card("Architectural corners", f'<div class="b b-5">{im("room")}<i></i><i></i><i></i><i></i></div>', "ticks at four corners"),
  card("Animated edge", f'<div class="b b-6">{im("room")}</div>', "travelling ochre border on hover"),
]))
labs.append(("type","Typography lab","One hierarchy, three voices. A uses Cormorant + Karla; B Marcellus + Jost; C Fraunces + Plus Jakarta Sans.",[
  card("Oversized serif", '<p class="t t-over">Karibu</p>', "Cormorant 500, −3% tracking"),
  card("Split-line headline", '<p class="t t-split"><span>Your stay.</span><span>Your comfort.</span><em>Your Breez.</em></p>', "indent + italic third line"),
  card("Small caps label + serif", '<p class="t t-label"><span class="label">Nº 02 · Swim</span>Two pools among the palms</p>', "label 12px, +16% tracking"),
  card("Architectural caps", '<p class="t t-arch">THE BREEZ<br><small>HOTEL · BUSIA</small></p>', "Marcellus, wide tracking (concept B)"),
  card("Contemporary", '<p class="t t-mod">Good days start<br>by the pool.</p>', "Fraunces 700 (concept C)"),
  card("Oversized numeral", '<p class="t t-num"><span>37</span>rooms listed</p>', "numerals as section markers"),
]))
labs.append(("images","Image composition lab","All compositions use the hotel's own photographs.",[
  card("Full-bleed", f'<div class="ic ic-full">{im("pool")}</div>', "one image, edge to edge"),
  card("Overlapping", f'<div class="ic ic-over">{im("bld")}{im("room")}</div>', "front image breaks the edge"),
  card("Offset pair", f'<div class="ic ic-off">{im("pool2")}{im("dine")}</div>', "staggered baselines"),
  card("Mosaic", f'<div class="ic ic-mos">{im("court")}{im("pool")}{im("room")}{im("sign")}</div>', "2×2 with one tall"),
  card("Editorial collage", f'<div class="ic ic-col">{im("gaz")}{im("sign")}{im("fount")}</div>', "three sizes, tilted note"),
  card("Arch mask", f'<div class="ic ic-arch">{im("fount")}</div>', "echoes the gazebo roofs"),
]))
labs.append(("nav","Navigation lab","",[
  iframe("16-fullscreen-navigation","Fullscreen menu","Circle-reveal overlay"),
  iframe("06-vertical-side-navigation","Vertical side nav","Rotated labels"),
  card("Centred logo, split links", '<nav class="n n-split"><span>Stay</span><span>Swim</span><b>The Breez</b><span>Dine</span><span>Meet</span></nav>', "symmetry of the courtyard"),
  card("Ruled bar (B)", '<nav class="n n-ruled"><span>Menu</span><b>THE BREEZ</b><span>Book</span></nav>', "cells divided by rules"),
  card("Floating pill (C)", '<nav class="n n-pill"><b>Breez</b><span>Stay</span><span>Swim</span><span>Dine</span><em>Book</em></nav>', "detached, rounded, sticky"),
  card("Mobile bottom bar", '<nav class="n n-bottom"><span>Call</span><span>WhatsApp</span><em>Book</em></nav>', "thumb-reach actions on phones"),
]))
labs.append(("motion","Animation lab","Motion is slow and purposeful; everything respects reduced-motion settings.",[
  iframe("13-image-mask-transitions","Mask reveal","clip-path wipe on scroll"),
  iframe("14-animated-section-dividers","Section dividers","drawn rules and waves"),
  iframe("09-cinematic-image-hero","Crossfade hero","Ken Burns + fade"),
  iframe("26-karibu-stamp-and-ticker","Karibu stamp","rotating booking seal + ticker"),
]))
labs.append(("cards","Accommodation card lab","Room names from booking platforms; categories await management confirmation.",[
  card("Editorial (A)", f'<div class="rc rc-a">{im("room")}<p class="label">01</p><b>Double Room</b><span>1 double bed · 2 guests</span></div>', "hairline under, numeral"),
  card("Framed (B)", f'<div class="rc rc-b">{im("room2")}<b>DELUXE</b><span>1 double · 2 guests</span></div>', "double frame, caps"),
  card("Floating (C)", f'<div class="rc rc-c">{im("room")}<b>King Room</b><span>Large double · pool view listed</span><em>Enquire</em></div>', "rounded, lifted"),
  iframe("19-offset-accommodation-cards","Offset grid","staggered pairs"),
]))
labs.append(("gallery","Gallery lab","",[
  iframe("10-masonry-gallery","Masonry + filters + lightbox","categories with real photos only"),
  iframe("03-asymmetric-hotel-gallery","Asymmetric spread","magazine rhythm"),
  iframe("18-horizontal-experience-gallery","Horizontal story","a day at the hotel"),
]))
labs.append(("booking","Booking interface lab","Every booking control sends a request — nothing claims live availability.",[
  iframe("07-floating-booking-bar","Floating bar","overlaps hero, then sticks"),
  iframe("24-creative-booking-panel","Conversational panel","pills, WhatsApp fallback"),
  card("Sticky mobile CTA", '<div class="bk"><span>Busia · Kisumu–Busia Rd</span><em>Request to book</em></div>', "always visible on phones"),
]))
labs.append(("footer","Footer lab","",[
  iframe("15-creative-footer-layout","Wordmark footer","oversized name + stamp"),
  card("Ruled columns (B)", '<div class="ft ft-b"><span>Find us</span><span>Reserve</span><span>Follow</span></div>', "architectural cells"),
  card("Card footer (C)", '<div class="ft ft-c"><b>Plan your stay</b><em>WhatsApp 0707 461 665</em></div>', "rounded call-to-action"),
]))

nav = "".join(f'<a href="#{k}">{t.replace(" lab","")}</a>' for k,t,_,_ in labs)
secs = "".join(f'<section id="{k}" class="lab"><header><p class="label">Lab {i:02d}</p><h2 class="h2">{t}</h2>{f"<p class=lead>{d}</p>" if d else ""}</header><div class="grid">{"".join(items)}</div></section>' for i,(k,t,d,items) in enumerate(labs,1))
xlist = "".join(f'<li><a href="../research/design-experiments/{x["slug"]}/index.html"><span>{x["n"]}</span>{H.escape(x["title"])}</a><small>{H.escape(x["inspired"])}</small></li>' for x in xps)

page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Design laboratory — The Breez Hotel</title>
<link rel="stylesheet" href="../assets/css/base.css"><link rel="stylesheet" href="lab.css"></head>
<body>
<header class="top">
  <div><p class="label">The Breez Hotel · Busia</p><h1 class="display">Design laboratory</h1><p class="lead">Every technique harvested from the research, rebuilt from scratch with the hotel's own photographs, shown side by side so variations can be compared.</p></div>
  <a class="btn btn--framed" href="../design-review/index.html">Open design review →</a>
</header>
<nav class="labnav" aria-label="Labs">{nav}<a href="#experiments">All experiments</a></nav>
{secs}
<section id="experiments" class="lab"><header><p class="label">Index</p><h2 class="h2">All {len(xps)} experiments</h2></header><ol class="xlist">{xlist}</ol></section>
<footer class="labfoot"><p>Photographs: The Breez Hotel (official Facebook page), used with the hotel's permission for this prototype. Not for public release until written permission is on file.</p></footer>
<script src="../assets/js/site.js"></script>
</body></html>"""
open(os.path.join(ROOT, "design-laboratory/index.html"), "w").write(page)
print("lab written:", len(labs), "labs")
