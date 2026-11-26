"""Generate /research/design-experiments/NN-name/{index.html,style.css}.

Each experiment reconstructs one technique found in the visual research,
built from scratch with the shared design tokens and The Breez Hotel's own
photographs. Run: python3 tools/build_experiments.py
"""
import json, os, html as H

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "research", "design-experiments")
A = "../../../assets/images/breez/"
IMG = {
    "courtyard": "gardens/cottage-courtyard-swing-1600.webp",
    "fountain": "gardens/courtyard-fountain-gazebos-1600.webp",
    "fountain2": "gardens/courtyard-lawn-fountain-1600.webp",
    "gazebo": "gardens/gazebo-cypress-1600.webp",
    "gazebo2": "gardens/gazebo-flowerbeds-1600.webp",
    "building": "exterior/building-palms-pool-court-1600.webp",
    "building2": "exterior/building-palms-umbrellas-1600.webp",
    "facade": "exterior/main-building-facade-1600.webp",
    "tower": "exterior/tower-and-terrace-1600.webp",
    "sign": "exterior/sign-the-breeze-hotel-karibu-1600.webp",
    "gate": "exterior/entrance-gate-1600.webp",
    "pool": "pools/pool-umbrellas-above-1600.webp",
    "pool2": "pools/pool-terrace-kids-pool-1600.webp",
    "poolaerial": "pools/pool-aerial-1600.webp",
    "poolside": "pools/poolside-tables-1600.webp",
    "loungers": "pools/pool-loungers-1600.webp",
    "lanes": "pools/pool-lanes-1600.webp",
    "room": "rooms/room-four-poster-window-1600.webp",
    "room2": "rooms/room-grey-bedding-1600.webp",
    "room3": "rooms/room-fridge-tv-1600.webp",
    "room4": "rooms/room-desk-armchair-1600.webp",
    "roomp": "rooms/room-portrait-1600.webp",
    "bath": "rooms/bathroom-shower-1600.webp",
    "bed": "rooms/bed-detail-1600.webp",
    "conf": "conference/hall-classroom-setup-1600.webp",
    "conf2": "conference/hall-banquet-red-1600.webp",
    "conf3": "conference/hall-gold-cloths-1600.webp",
    "dine": "dining/poolside-meal-juice-1600.webp",
    "rest": "dining/restaurant-interior-blue-1600.webp",
    "bar": "dining/bar-counter-stools-1600.webp",
    "buffet": "dining/buffet-samosa-chapati-1600.webp",
    "event": "events/tent-wedding-setup-1600.webp",
    "event2": "events/garden-party-setup-1600.webp",
    "lounge": "interiors/lounge-rattan-sofas-1600.webp",
    "veranda": "interiors/veranda-corridor-1600.webp",
}

def img(key, alt, cls="", eager=False):
    return f'<img src="{A}{IMG[key]}" alt="{H.escape(alt)}" class="{cls}" {"" if eager else "loading=\"lazy\""} decoding="async">'

XP = []
def xp(slug, title, inspired, body, css):
    XP.append(dict(slug=slug, title=title, inspired=inspired, body=body, css=css))

# 01 ------------------------------------------------------------------------
xp("01-editorial-margin-layout", "Editorial margin layout",
   "Broadsheet-style sites on Pinterest (\"The Wordsmith\") and Aman's generous white space",
   f"""
<main class="page">
  <aside class="margin-note label">Nº 01 — The courtyard</aside>
  <article class="col">
    <p class="label">Busia, Kenya</p>
    <h1 class="display">A garden of cottages, a pool among the palms.</h1>
    <p class="lead">Text sits in a narrow measure inside wide page margins; notes live in the margin, not in the copy.</p>
    <figure class="wide ph ratio-land">{img('courtyard','The cottage courtyard at The Breez Hotel with lawn, paths and a hanging swing chair', eager=True)}</figure>
    <p>Margins do the work that boxes usually do. The reading column never exceeds about 62 characters, while photographs break out to the full content width — the rhythm of a magazine spread rather than a template.</p>
  </article>
  <aside class="margin-note margin-note--right">Photograph: hotel courtyard, The Breez Hotel (Facebook).</aside>
</main>""",
"""
.page{display:grid;grid-template-columns:minmax(var(--page-margin),1fr) minmax(0,62ch) minmax(var(--page-margin),1fr);gap:0 var(--gutter);padding:var(--section-gap) 0}
.col{grid-column:2;display:grid;gap:24px}
.wide{margin:16px calc(-1 * min(18vw,240px));}
.margin-note{grid-column:1;justify-self:end;align-self:start;position:sticky;top:24px;max-width:160px;text-align:right}
.margin-note--right{grid-column:3;justify-self:start;text-align:left;font:italic 15px/1.4 var(--font-display);color:var(--ink-soft);align-self:end}
@media(max-width:860px){.page{grid-template-columns:1fr;padding:48px 20px}.col,.margin-note,.margin-note--right{grid-column:1;justify-self:start;text-align:left;position:static;max-width:none}.wide{margin:16px -20px}}
""")

# 02 ------------------------------------------------------------------------
xp("02-framed-page-layout", "Framed page layout (inset double frame)",
   "Hotel du Tasso's white page floating inside a coloured mat",
   f"""
<div class="mat">
  <div class="sheet">
    <header class="top"><span class="label">Rooms</span><strong class="logo">The Breez</strong><a class="btn btn--framed" href="#">Book</a></header>
    <section class="hero">
      <h1 class="display">Karibu.<br>Stay a while.</h1>
      <figure class="ph ratio-port a">{img('room','A four-poster bed with mosquito net and dark wood frame in a Breez Hotel room', eager=True)}</figure>
      <figure class="ph ratio-port b">{img('pool2','The main pool and kids pool on the stone terrace')}</figure>
    </section>
  </div>
</div>""",
"""
body{background:var(--palm)}
.mat{padding:var(--page-margin);min-height:100vh}
.sheet{background:var(--sand);min-height:calc(100vh - 2*var(--page-margin));outline:1px solid var(--ochre);outline-offset:-10px;padding:clamp(20px,4vw,56px)}
.top{display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap}
.logo{font:600 28px var(--font-display)}
.hero{display:grid;grid-template-columns:1.2fr .8fr .8fr;gap:var(--grid-gap);align-items:end;margin-top:clamp(40px,8vw,120px)}
.hero .a{margin-bottom:60px}
@media(max-width:760px){.hero{grid-template-columns:1fr 1fr}.hero h1{grid-column:1/-1}.hero .a{margin:0}}
""")

# 03 ------------------------------------------------------------------------
xp("03-asymmetric-hotel-gallery", "Asymmetric hotel gallery",
   "Travel-magazine spreads on Pinterest; Behance resort case studies",
   f"""
<main class="wrap">
  <h1 class="h2">The hotel, unhurried</h1>
  <div class="asym" data-lightbox>
    <a class="ph i1" href="{A}{IMG['courtyard']}" data-caption="Cottage courtyard">{img('courtyard','Cottage courtyard with lawn and paths', eager=True)}</a>
    <a class="ph i2" href="{A}{IMG['pool']}" data-caption="Main pool and terrace">{img('pool','Main pool with blue parasols from above')}</a>
    <a class="ph i3" href="{A}{IMG['sign']}" data-caption="The hotel sign: Karibu">{img('sign','Wooden sign reading The Breeze Hotel Karibu')}</a>
    <a class="ph i4" href="{A}{IMG['room']}" data-caption="Four-poster room">{img('room','Room with four-poster bed')}</a>
    <a class="ph i5" href="{A}{IMG['dine']}" data-caption="Lunch by the pool">{img('dine','Juice and fries served beside the pool')}</a>
  </div>
</main>""",
"""
.wrap{max-width:var(--content-width);margin:0 auto;padding:var(--section-gap) var(--gutter)}
.asym{display:grid;grid-template-columns:repeat(12,minmax(0,1fr));grid-auto-rows:clamp(60px,7vw,100px);gap:var(--grid-gap);margin-top:32px}
.asym a{display:block}.asym img{transition:transform var(--transition-slow)}.asym a:hover img{transform:scale(1.04)}
.i1{grid-column:1/8;grid-row:1/6}.i2{grid-column:8/13;grid-row:2/5}.i3{grid-column:9/12;grid-row:5/9}.i4{grid-column:2/6;grid-row:6/10}.i5{grid-column:6/9;grid-row:7/11}
@media(max-width:700px){.asym{grid-template-columns:repeat(6,minmax(0,1fr));grid-auto-rows:70px}.i1{grid-column:1/7;grid-row:1/5}.i2{grid-column:1/4;grid-row:5/8}.i3{grid-column:4/7;grid-row:5/9}.i4{grid-column:1/4;grid-row:8/12}.i5{grid-column:4/7;grid-row:9/12}}
""")

# 04 ------------------------------------------------------------------------
xp("04-overlapping-photo-composition", "Overlapping photo composition",
   "Terreno Barrio Hotel's tilted, layered images; architecture portfolios on Pinterest",
   f"""
<main class="ov">
  <div class="stack">
    <figure class="ph back ratio-land">{img('building','Hotel building with palms, parasols and pool court', eager=True)}</figure>
    <figure class="ph front ratio-port">{img('room4','Room with desk and armchair by the window')}</figure>
    <span class="tag label">Overlap · 18% · offset shadow</span>
  </div>
  <div class="txt"><p class="label">Stay</p><h1 class="h2">Rooms that open onto the gardens</h1><p class="lead">Two photographs, one composition: the front image breaks the edge of the back image, so the eye reads them as one story — place, then room.</p></div>
</main>""",
"""
.ov{display:grid;grid-template-columns:1.3fr 1fr;gap:var(--gutter);align-items:center;max-width:var(--content-width);margin:0 auto;padding:var(--section-gap) var(--gutter)}
.stack{position:relative;padding-bottom:18%}
.back{width:88%}
.front{position:absolute;width:42%;right:0;bottom:0;box-shadow:var(--shadow-lift);border:8px solid var(--sand)}
.tag{position:absolute;left:0;bottom:-8px}
@media(max-width:760px){.ov{grid-template-columns:1fr}}
""")

# 05 ------------------------------------------------------------------------
xp("05-double-border-sections", "Double-border sections",
   "Hotel du Tasso's double-framed buttons; Grand Hotel Vesuvio's ruled navigation",
   f"""
<main class="wrap">
  <section class="db"><p class="label">01 · Accommodation</p><h2 class="h2">Rooms</h2><p>Single, double, deluxe, superior and king rooms are listed by booking platforms — categories awaiting the hotel's confirmation.</p></section>
  <section class="db db--ochre"><p class="label">02 · Leisure</p><h2 class="h2">Pools</h2><p>A main pool and a children's pool sit beside the terrace.</p></section>
  <section class="db db--palm"><p class="label">03 · Meetings</p><h2 class="h2">Conference halls</h2><p>Classroom, banquet and theatre set-ups, as shown in the hotel's photos.</p></section>
</main>""",
"""
.wrap{max-width:var(--content-width);margin:0 auto;padding:var(--section-gap) var(--gutter);display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:var(--grid-gap)}
.db{position:relative;padding:40px 32px;border:1px solid var(--ink);display:grid;gap:12px}
.db::before{content:"";position:absolute;inset:6px;border:1px solid var(--ink);pointer-events:none}
.db--ochre{border-color:var(--ochre-deep)}.db--ochre::before{border-color:var(--ochre-deep)}
.db--palm{background:var(--palm);color:var(--sand);border-color:var(--sand)}.db--palm::before{border-color:var(--ochre)}.db--palm .label{color:var(--pool-light)}
.db p{margin:0}
""")

# 06 ------------------------------------------------------------------------
xp("06-vertical-side-navigation", "Vertical side navigation",
   "Fashion and architecture portfolios with edge navigation (Pinterest: \"vertical typography website side labels\")",
   f"""
<div class="shell">
  <nav class="side" aria-label="Main">
    <strong class="logo">B</strong>
    <ul><li><a href="#">Stay</a></li><li><a href="#">Pools</a></li><li><a href="#">Dine</a></li><li><a href="#">Meet</a></li><li><a href="#">Gallery</a></li></ul>
    <span class="vert label">Karibu · Busia</span>
  </nav>
  <main class="ph hero">{img('fountain2','The courtyard fountain and gazebos on the lawn', eager=True)}<h1 class="display">The Breez</h1></main>
</div>""",
"""
.shell{display:grid;grid-template-columns:96px 1fr;min-height:100vh}
.side{position:sticky;top:0;height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:space-between;padding:24px 0;border-right:var(--border-subtle);background:var(--sand)}
.logo{font:600 36px var(--font-display);color:var(--palm)}
.side ul{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:28px}
.side a{writing-mode:vertical-rl;transform:rotate(180deg);text-decoration:none;font:600 13px var(--font-body);letter-spacing:.18em;text-transform:uppercase}
.side a:hover{color:var(--ochre-deep)}
.vert{writing-mode:vertical-rl;transform:rotate(180deg)}
.hero{min-height:100vh;display:flex;align-items:flex-end}.hero img{position:absolute;inset:0}.hero h1{position:relative;color:#fff;padding:32px;text-shadow:0 2px 30px rgba(0,0,0,.5)}
@media(max-width:700px){.shell{grid-template-columns:1fr}.side{position:sticky;height:auto;flex-direction:row;padding:10px 14px;z-index:2;border-right:0;border-bottom:var(--border-subtle)}.side ul{flex-direction:row;gap:14px}.side a{writing-mode:horizontal-tb;transform:none;font-size:11px}.vert{display:none}.hero{min-height:70vh}}
""")

# 07 ------------------------------------------------------------------------
xp("07-floating-booking-bar", "Floating booking bar",
   "The Hoxton's in-hero booking bar; Sarova's docked widget; Ace Hotel's header booking strip",
   f"""
<header class="ph hero">{img('building2','The hotel building with palms and striped parasols', eager=True)}<h1 class="display">Your stay. Your comfort.<br>Your Breez.</h1></header>
<form class="bar" data-booking aria-label="Request a booking">
  <label>Check-in<input type="date" name="checkin" required></label>
  <label>Check-out<input type="date" name="checkout" required></label>
  <label>Guests<select name="guests"><option>1 adult</option><option selected>2 adults</option><option>2 adults + 1 child</option><option>Family (4)</option></select></label>
  <button class="btn btn--book" type="submit">Request to book</button>
  <p class="note" data-nights aria-live="polite"></p>
</form>
<main class="filler"><p class="lead">Scroll: the bar docks to the top of the screen (position: sticky) and stays one tap away.</p></main>""",
"""
.hero{min-height:78vh;display:flex;align-items:flex-end}.hero img{position:absolute;inset:0}.hero::after{content:"";position:absolute;inset:0;background:linear-gradient(transparent 40%,rgba(20,15,10,.65))}.hero h1{position:relative;z-index:1;color:#fff;padding:0 var(--gutter) 120px}
.bar{position:sticky;top:12px;z-index:5;margin:-72px var(--gutter) 0;background:var(--paper);box-shadow:var(--shadow-lift);display:grid;grid-template-columns:repeat(3,minmax(0,1fr)) auto;gap:12px;padding:16px;align-items:end}
.bar label{display:grid;gap:6px;font:700 12px var(--font-body);letter-spacing:.1em;text-transform:uppercase;color:var(--ink-soft)}
.bar input,.bar select{font:16px var(--font-body);min-height:48px;padding:0 12px;border:1px solid var(--sand-deep);background:#fff;color:var(--ink)}
.note{grid-column:1/-1;margin:0;font-size:14px;color:var(--ink-soft)}
.filler{min-height:120vh;padding:80px var(--gutter)}
@media(max-width:760px){.bar{grid-template-columns:1fr 1fr;margin:-40px 12px 0}.bar button{grid-column:1/-1}}
""")

# 08 ------------------------------------------------------------------------
xp("08-oversized-editorial-headings", "Oversized editorial headings",
   "Tengile Malamala and the Terreno wordmark: type that fills the screen",
   f"""
<main class="big">
  <h1 class="giant"><span>Karibu</span><span class="it">to Busia</span></h1>
  <figure class="ph strip ratio-pano">{img('courtyard','Courtyard of cottages and gazebos', eager=True)}</figure>
  <p class="lead">The word on the hotel's own sign, set at the size of the place it welcomes you to.</p>
</main>""",
"""
.big{padding:var(--section-gap) var(--gutter);display:grid;gap:32px}
.giant{margin:0;font:500 clamp(4rem,17vw,17rem)/.82 var(--font-display);letter-spacing:-.03em;color:var(--palm);display:grid}
.giant .it{font-style:italic;color:var(--ochre-deep);padding-left:12vw}
.strip{margin-top:-4vw}
""")

# 09 ------------------------------------------------------------------------
xp("09-cinematic-image-hero", "Cinematic image hero (crossfade slideshow)",
   "Hemingways' aerial video hero; Serena's three-word line",
   f"""
<header class="cine" aria-roledescription="carousel">
  <div class="slides">
    <figure class="ph s is-on">{img('pool','Pool with parasols', eager=True)}</figure>
    <figure class="ph s">{img('courtyard','Cottage courtyard')}</figure>
    <figure class="ph s">{img('building','Hotel building and palms')}</figure>
  </div>
  <div class="copy"><p class="label">The Breez Hotel · Busia</p><h1 class="display">Class. Comfort.<br>Serenity.</h1></div>
  <div class="dots" role="tablist"><button aria-label="Slide 1" aria-selected="true"></button><button aria-label="Slide 2"></button><button aria-label="Slide 3"></button></div>
</header>
<script>{{const s=[...document.querySelectorAll('.s')],d=[...document.querySelectorAll('.dots button')];let i=0;const go=n=>{{s[i].classList.remove('is-on');d[i].setAttribute('aria-selected','false');i=(n+s.length)%s.length;s[i].classList.add('is-on');d[i].setAttribute('aria-selected','true')}};d.forEach((b,k)=>b.onclick=()=>go(k));if(!matchMedia('(prefers-reduced-motion: reduce)').matches)setInterval(()=>go(i+1),5000)}}</script>""",
"""
.cine{position:relative;height:100svh;min-height:520px;color:#fff;overflow:hidden}
.slides,.s{position:absolute;inset:0}.s{opacity:0;transition:opacity 1.4s ease,transform 7s linear;transform:scale(1.08)}.s.is-on{opacity:1;transform:scale(1)}
.cine::after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(15,20,15,.7),transparent 70%)}
.copy{position:absolute;z-index:2;left:var(--gutter);bottom:18%;display:grid;gap:12px}.copy .label{color:#f3d9a8}
.dots{position:absolute;z-index:2;right:var(--gutter);bottom:32px;display:flex;gap:10px}.dots button{width:44px;height:44px;background:none;border:0;cursor:pointer;position:relative}.dots button::after{content:"";position:absolute;left:8px;right:8px;top:21px;height:2px;background:rgba(255,255,255,.45)}.dots [aria-selected=true]::after{background:#fff}
""")

# 10 ------------------------------------------------------------------------
cards = [("courtyard","exterior","Courtyard"),("pool","pools","Main pool"),("room","rooms","Four-poster room"),("conf","meet","Conference hall"),("sign","exterior","The sign"),("dine","dine","Poolside lunch"),("gazebo","exterior","Gazebo"),("room2","rooms","Double room"),("lanes","pools","Pool lanes"),("conf2","meet","Banquet set-up"),("bar","dine","Bar"),("event","events","Tent wedding set-up"),("fountain2","exterior","Fountain lawn"),("bath","rooms","Shower room")]
masonry = "".join(f'<a href="{A}{IMG[k]}" data-cat="{c}" data-caption="{t}" class="m">{img(k,t)}<span>{t}</span></a>' for k,c,t in cards)
xp("10-masonry-gallery", "Masonry gallery with filters and lightbox",
   "Dribbble hotel galleries; CSS columns masonry from photography portfolios",
   f"""
<main class="wrap">
  <h1 class="h2">Gallery</h1>
  <div class="filters" data-filters="grid" role="group" aria-label="Filter photos">
    <button data-filter="all" aria-pressed="true">All</button><button data-filter="exterior" aria-pressed="false">The hotel</button><button data-filter="rooms" aria-pressed="false">Rooms</button><button data-filter="pools" aria-pressed="false">Pools</button><button data-filter="dine" aria-pressed="false">Dining</button><button data-filter="meet" aria-pressed="false">Meetings</button><button data-filter="events" aria-pressed="false">Events</button>
  </div>
  <div id="grid" class="masonry" data-lightbox>{masonry}</div>
</main>""",
"""
.wrap{max-width:var(--content-width);margin:0 auto;padding:var(--section-gap) var(--gutter)}
.filters{display:flex;flex-wrap:wrap;gap:8px;margin:24px 0}
.filters button{min-height:44px;padding:0 16px;border:1px solid var(--ink);background:none;font:600 14px var(--font-body);cursor:pointer;border-radius:var(--pill)}
.filters [aria-pressed=true]{background:var(--ink);color:var(--sand)}
.masonry{columns:3 260px;column-gap:var(--grid-gap)}
.m{display:block;break-inside:avoid;margin-bottom:var(--grid-gap);position:relative;overflow:hidden}
.m img{transition:transform var(--transition-slow)}.m:hover img{transform:scale(1.05)}
.m span{position:absolute;left:0;bottom:0;padding:8px 12px;font:600 13px var(--font-body);color:#fff;background:linear-gradient(transparent,rgba(0,0,0,.6));width:100%;opacity:0;transition:opacity var(--transition-fast)}.m:hover span,.m:focus span{opacity:1}
""")

# 11 ------------------------------------------------------------------------
xp("11-split-screen-introduction", "Split-screen introduction",
   "Tribe's \"Tribe is a philosophy\" split; Aman's calm halves",
   f"""
<main class="split">
  <figure class="ph left">{img('sign','The hotel sign reading The Breeze Hotel Karibu', eager=True)}</figure>
  <section class="right"><p class="label">About the hotel</p><h1 class="h2">Along the Kisumu–Busia road, in a calm residential corner of town.</h1><p class="lead">Thirty-seven rooms, two pools, a restaurant and bar, conference halls and a garden of cottages — minutes from the border crossing.</p><p class="small">Room count from public listings; to be confirmed by management.</p><a class="link-arrow" href="#">Our story</a></section>
</main>""",
"""
.split{display:grid;grid-template-columns:1fr 1fr;min-height:100vh}
.left{min-height:60vh}.right{display:grid;align-content:center;gap:20px;padding:var(--gutter);max-width:640px}
.small{font-size:13px;color:var(--ink-soft);margin:0}
@media(max-width:760px){.split{grid-template-columns:1fr}}
""")

# 12 ------------------------------------------------------------------------
xp("12-architectural-grid", "Architectural grid (visible hairline grid)",
   "Architecture studio sites on Pinterest; Awwwards' ruled grids",
   f"""
<main class="ag">
  <div class="cell c1"><p class="label">Rooms</p><span class="numeral">37</span><p>rooms listed</p></div>
  <div class="cell c2 ph">{img('facade','The main building façade', eager=True)}</div>
  <div class="cell c3"><p class="label">Pools</p><span class="numeral">2</span><p>main + children's</p></div>
  <div class="cell c4 ph">{img('pool','Pool from above')}</div>
  <div class="cell c5"><h1 class="h2">Built around a courtyard.</h1></div>
  <div class="cell c6"><p class="label">Border</p><p>Minutes from the Kenya–Uganda crossing</p></div>
</main>""",
"""
.ag{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));border-top:var(--border-strong);border-left:var(--border-strong);margin:var(--page-margin)}
.cell{border-right:var(--border-strong);border-bottom:var(--border-strong);padding:24px;min-height:220px;display:grid;align-content:space-between;gap:8px}.cell p{margin:0}
.cell.ph{padding:0}.c2{grid-column:span 2;grid-row:span 2}.c4{grid-column:span 2}.c5{grid-column:span 2}
@media(max-width:700px){.ag{grid-template-columns:1fr 1fr}.c2,.c4,.c5{grid-column:1/-1}.c2{grid-row:auto;min-height:300px}}
""")

# 13 ------------------------------------------------------------------------
xp("13-image-mask-transitions", "Image mask transitions (clip-path reveal)",
   "Awwwards nominees' wipe reveals on scroll",
   f"""
<main class="wrap">
  <p class="label">Scroll</p>
  <figure class="ph ratio-land reveal-mask m1">{img('pool2','Main and kids pool', eager=True)}</figure>
  <figure class="ph ratio-land reveal-mask m2">{img('room','Four-poster room')}</figure>
  <figure class="ph ratio-land reveal-mask m3 arch">{img('gazebo','A gazebo between cypress trees')}</figure>
</main>""",
"""
.wrap{max-width:900px;margin:0 auto;padding:40vh var(--gutter);display:grid;gap:30vh}
.m2{transition-delay:.1s}.arch{border-radius:50% 50% 0 0/40% 40% 0 0}
.reveal-mask img{transform:scale(1.15);transition:transform 1.4s var(--ease-out)}.reveal-mask.is-in img{transform:scale(1)}
""")

# 14 ------------------------------------------------------------------------
xp("14-animated-section-dividers", "Animated section dividers",
   "Fine-rule separators on editorial sites; travelling borders on Awwwards",
   """
<main>
  <section class="s"><h2 class="h2">Stay</h2></section>
  <div class="divider reveal"><span class="line"></span><span class="mark">✦ Karibu ✦</span><span class="line"></span></div>
  <section class="s"><h2 class="h2">Dine</h2></section>
  <div class="divider divider--wave reveal" aria-hidden="true"><svg viewBox="0 0 1200 40" preserveAspectRatio="none"><path d="M0 20 Q 75 0 150 20 T 300 20 T 450 20 T 600 20 T 750 20 T 900 20 T 1050 20 T 1200 20"/></svg></div>
  <section class="s"><h2 class="h2">Swim</h2></section>
  <div class="divider divider--travel"></div>
  <section class="s"><h2 class="h2">Meet</h2></section>
</main>""",
"""
.s{padding:18vh var(--gutter)}
.divider{display:flex;align-items:center;gap:20px;padding:0 var(--gutter)}
.divider .line{flex:1;height:1px;background:var(--ink);transform:scaleX(0);transition:transform 1.2s var(--ease-out)}
.divider .line:first-child{transform-origin:right}.divider .line:last-child{transform-origin:left}
.divider.is-in .line{transform:scaleX(1)}
.divider .mark{font:italic 20px var(--font-display);color:var(--ochre-deep);white-space:nowrap}
.divider--wave svg{width:100%;height:40px}.divider--wave path{fill:none;stroke:var(--pool);stroke-width:2;stroke-dasharray:1400;stroke-dashoffset:1400;transition:stroke-dashoffset 2s var(--ease-out)}.divider--wave.is-in path{stroke-dashoffset:0}
.divider--travel{height:1px;margin:0 var(--gutter);background:linear-gradient(90deg,var(--sand-deep),var(--ochre),var(--sand-deep));background-size:200% 100%;animation:trav 4s linear infinite}
@keyframes trav{to{background-position:-200% 0}}
""")

# 15 ------------------------------------------------------------------------
xp("15-creative-footer-layout", "Creative footer layout",
   "Hotel footers with oversized wordmarks (Terreno, Casa Momo)",
   f"""
<main style="min-height:40vh"></main>
<footer class="ft">
  <div class="cols">
    <div><p class="label">Find us</p><p>Kisumu–Busia Road, Busia, Kenya<br>Plus Code F44C+HJ</p></div>
    <div><p class="label">Reservations</p><p>Call, SMS or WhatsApp<br><a href="tel:+254707461665">0707 461 665</a><br><a href="mailto:thebreezhotel@gmail.com">thebreezhotel@gmail.com</a></p></div>
    <div><p class="label">Follow</p><p><a href="https://web.facebook.com/TheBreezhotelofficial">Facebook</a><br><a href="https://www.tiktok.com/@thebreezhotelbusia">TikTok</a></p></div>
    <div class="stamp" aria-hidden="true"><svg viewBox="0 0 120 120"><defs><path id="c" d="M60 60 m-44 0 a44 44 0 1 1 88 0 a44 44 0 1 1 -88 0"/></defs><text><textPath href="#c">BOOK YOUR STAY · KARIBU · BOOK YOUR STAY · KARIBU ·</textPath></text></svg></div>
  </div>
  <p class="word">The Breez</p>
  <p class="fine">Contact details as published on the hotel's TikTok and Facebook.</p>
</footer>""",
"""
.ft{background:var(--palm);color:var(--sand);padding:72px var(--gutter) 24px;overflow:hidden}
.ft a{color:var(--sand)}.ft .label{color:var(--pool-light)}
.cols{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:32px;align-items:start}
.word{font:500 clamp(4rem,19vw,18rem)/.8 var(--font-display);margin:48px 0 0;letter-spacing:-.04em;color:var(--ochre);white-space:nowrap}
.fine{font-size:13px;opacity:.75;margin:16px 0 0}
.stamp{width:120px;justify-self:end;animation:spin 18s linear infinite}.stamp text{font:600 10px var(--font-body);letter-spacing:.2em;fill:var(--sand)}
@keyframes spin{to{transform:rotate(360deg)}}
""")

# 16 ------------------------------------------------------------------------
xp("16-fullscreen-navigation", "Fullscreen navigation",
   "Grand Hotel Vesuvio and Hemingways' full-screen MENU overlays",
   f"""
<header class="nav"><strong class="logo">The Breez</strong><button class="burger" data-menu-toggle aria-controls="fs" aria-expanded="false">Menu</button></header>
<nav id="fs" class="fs" aria-label="Main">
  <ul>
    <li><a href="#">Stay<small>Rooms</small></a></li><li><a href="#">Swim<small>Two pools</small></a></li><li><a href="#">Dine<small>Restaurant &amp; bar</small></a></li><li><a href="#">Meet<small>Conferences &amp; events</small></a></li><li><a href="#">Gallery<small>The hotel in pictures</small></a></li><li><a href="#">Contact<small>0707 461 665</small></a></li>
  </ul>
  <figure class="ph">{img('courtyard','Hotel courtyard')}</figure>
</nav>
<main class="ph hero">{img('building','The hotel building', eager=True)}</main>""",
"""
.nav{position:fixed;inset:0 0 auto 0;z-index:20;display:flex;justify-content:space-between;align-items:center;padding:16px var(--gutter);color:#fff;mix-blend-mode:difference}
.logo{font:600 26px var(--font-display)}
.burger{min-height:44px;padding:0 18px;background:none;border:1px solid #fff;color:#fff;font:600 13px var(--font-body);letter-spacing:.2em;text-transform:uppercase;cursor:pointer}
.fs{position:fixed;inset:0;z-index:15;background:var(--palm);color:var(--sand);display:grid;grid-template-columns:1.2fr 1fr;clip-path:circle(0 at calc(100% - 60px) 36px);transition:clip-path .8s var(--ease-out);visibility:hidden}
.fs[data-open]{clip-path:circle(150% at calc(100% - 60px) 36px);visibility:visible}
.fs ul{list-style:none;margin:0;padding:96px var(--gutter);display:grid;align-content:center;gap:4px}
.fs a{display:flex;align-items:baseline;gap:16px;text-decoration:none;font:500 clamp(2.4rem,6vw,5rem)/1.05 var(--font-display)}
.fs a:hover{color:var(--ochre)}.fs small{font:500 13px var(--font-body);letter-spacing:.1em;opacity:.7}
.hero{height:100svh}
@media(max-width:760px){.fs{grid-template-columns:1fr}.fs figure{display:none}}
""")

# 17 ------------------------------------------------------------------------
xp("17-floating-image-cards", "Floating image cards",
   "Dribbble resort UI cards with lift-on-hover; Behance Luvora Hotels",
   f"""
<main class="wrap">
  <h1 class="h2">Moments at The Breez</h1>
  <div class="float">
    <article class="fc"><figure class="ph ratio-port">{img('pool','Pool')}</figure><h2 class="h3">A swim before supper</h2><p>Main pool · children's pool</p></article>
    <article class="fc up"><figure class="ph ratio-port">{img('dine','Poolside lunch')}</figure><h2 class="h3">Lunch by the water</h2><p>Restaurant &amp; bar</p></article>
    <article class="fc"><figure class="ph ratio-port">{img('gazebo','Gazebo')}</figure><h2 class="h3">Shade in the gazebos</h2><p>Garden courtyard</p></article>
  </div>
</main>""",
"""
.wrap{max-width:var(--content-width);margin:0 auto;padding:var(--section-gap) var(--gutter)}
.float{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:clamp(16px,3vw,40px);margin-top:40px;align-items:start}
.fc{background:var(--paper);padding:14px 14px 22px;box-shadow:var(--shadow-soft);border-radius:var(--image-radius-soft);transition:transform var(--transition-standard),box-shadow var(--transition-standard)}
.fc .ph{border-radius:14px}.fc h2{margin:16px 6px 4px}.fc p{margin:0 6px;color:var(--ink-soft);font-size:14px}
.fc:hover{transform:translateY(-10px) rotate(-.6deg);box-shadow:var(--shadow-lift)}
.up{margin-top:-30px}
@media(max-width:800px){.up{margin-top:0}}
""")

# 18 ------------------------------------------------------------------------
strip = "".join(f'<li class="hs"><figure class="ph">{img(k,t)}</figure><p class="label">{n:02d}</p><h3 class="h3">{t}</h3></li>' for n,(k,t) in enumerate([("gate","Arrive at the gate"),("sign","Karibu"),("courtyard","Into the courtyard"),("pool","Swim"),("dine","Eat by the pool"),("room","Rest"),("conf","Work"),("event","Celebrate")],1))
xp("18-horizontal-experience-gallery", "Horizontal experience gallery",
   "Horizontal storytelling sections on Awwwards; native scroll-snap",
   f"""
<main>
  <header class="hd"><h1 class="h2">A day at The Breez</h1><div class="ctl"><button class="prev" aria-label="Previous">←</button><button class="next" aria-label="Next">→</button></div></header>
  <ol class="hscroll" tabindex="0" aria-label="A day at the hotel, scroll sideways">{strip}</ol>
</main>
<script>{{const r=document.querySelector('.hscroll'),w=()=>r.querySelector('li').getBoundingClientRect().width+24;document.querySelector('.next').onclick=()=>r.scrollBy({{left:w(),behavior:'smooth'}});document.querySelector('.prev').onclick=()=>r.scrollBy({{left:-w(),behavior:'smooth'}});}}</script>""",
"""
.hd{display:flex;justify-content:space-between;align-items:end;padding:var(--section-gap) var(--gutter) 24px;gap:16px;flex-wrap:wrap}
.ctl{display:flex;gap:8px}.ctl button{width:52px;height:52px;border:1px solid var(--ink);background:none;font-size:20px;cursor:pointer;border-radius:50%}
.hscroll{list-style:none;margin:0;padding:0 var(--gutter) 60px;display:flex;gap:24px;overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:thin}
.hs{flex:0 0 clamp(240px,32vw,420px);scroll-snap-align:start}.hs:nth-child(even){margin-top:60px}
.hs .ph{aspect-ratio:3/4}.hs .label{margin:14px 0 4px;color:var(--ochre-deep)}
""")

# 19 ------------------------------------------------------------------------
rooms = [("room","Double Room","1 double bed · 2 guests"),("room2","Deluxe Room","1 double bed · 2 guests"),("room3","Superior Double","1 large double · 2 guests"),("room4","King Room","1 large double · 2 guests")]
rc = "".join(f'<article class="oc oc{i}"><figure class="ph ratio-land">{img(k,n+" — photo from the hotel")}</figure><div class="info"><p class="label">0{i}</p><h2 class="h3">{n}</h2><p>{m}</p><a class="link-arrow" href="#">Enquire</a></div></article>' for i,(k,n,m) in enumerate(rooms,1))
xp("19-offset-accommodation-cards", "Offset accommodation cards",
   "Staggered room lists on boutique hotel sites (Hotel du Tasso, Casa Momo)",
   f"""<main class="wrap"><h1 class="h2">Rooms</h1><p class="note">Room names from booking platforms; photos are of real Breez rooms but not yet matched to categories — management to confirm.</p><div class="offset">{rc}</div></main>""",
"""
.wrap{max-width:var(--content-width);margin:0 auto;padding:var(--section-gap) var(--gutter)}
.note{font-size:14px;color:var(--ink-soft)}
.offset{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:var(--grid-gap) clamp(20px,5vw,80px);margin-top:32px}
.oc:nth-child(even){transform:translateY(clamp(40px,8vw,120px))}
.info{display:grid;gap:6px;padding:16px 4px;border-bottom:var(--border-subtle)}.info p,.info h2{margin:0}
.oc .ph img{transition:transform var(--transition-slow)}.oc:hover .ph img{transform:scale(1.04)}
@media(max-width:640px){.offset{grid-template-columns:1fr}.oc:nth-child(even){transform:none}}
""")

# 20 ------------------------------------------------------------------------
xp("20-editorial-numbered-sections", "Editorial numbered sections",
   "Pinterest: website with oversized numeral on the left edge; architectural brochures",
   f"""
<main class="wrap">
  <section class="ns"><span class="n">01</span><div><p class="label">Stay</p><h2 class="h2">Rooms around a garden</h2><p>Four-poster beds, balconies and garden views.</p></div><figure class="ph ratio-land">{img('room','Room')}</figure></section>
  <section class="ns"><span class="n">02</span><div><p class="label">Swim</p><h2 class="h2">Two pools</h2><p>The main pool and a shallow pool for children.</p></div><figure class="ph ratio-land">{img('pool2','Pools')}</figure></section>
  <section class="ns"><span class="n">03</span><div><p class="label">Meet</p><h2 class="h2">Halls for every set-up</h2><p>Classroom, banquet and theatre layouts.</p></div><figure class="ph ratio-land">{img('conf','Conference hall')}</figure></section>
</main>""",
"""
.wrap{max-width:var(--content-width);margin:0 auto;padding:var(--section-gap) var(--gutter);display:grid;gap:clamp(48px,8vw,120px)}
.ns{display:grid;grid-template-columns:auto 1fr 1.2fr;gap:var(--gutter);align-items:start;border-top:var(--border-strong);padding-top:20px}
.n{font:400 clamp(4rem,10vw,9rem)/.8 var(--font-display);color:var(--ochre)}
.ns p{margin:8px 0 0}
@media(max-width:760px){.ns{grid-template-columns:auto 1fr}.ns figure{grid-column:1/-1}}
""")

# 21 ------------------------------------------------------------------------
xp("21-image-and-typography-overlap", "Image and typography overlap",
   "The Terreno \"Terra cotta\" wordmark crossing its photograph (Pinterest)",
   f"""
<main class="io">
  <figure class="ph pic">{img('poolaerial','The pool seen from above', eager=True)}</figure>
  <h1 class="word"><span class="a">Swim</span><span class="b">&amp; stay</span></h1>
</main>""",
"""
.io{position:relative;padding:var(--section-gap) var(--gutter);min-height:100vh;display:grid;place-items:center}
.pic{width:min(70vw,720px);aspect-ratio:4/5}
.word{position:absolute;inset:auto 0 18% 0;margin:0;text-align:center;font:500 clamp(4rem,15vw,14rem)/.85 var(--font-display);color:var(--palm);display:grid;pointer-events:none}
.word .a{mix-blend-mode:multiply}.word .b{font-style:italic;color:var(--ochre-deep);transform:translateX(8vw)}
""")

# 22 ------------------------------------------------------------------------
xp("22-vertical-labels-and-side-notes", "Vertical labels and side notes",
   "Fashion editorial sites with rotated captions; Hotel du Tasso's side cues",
   f"""
<main class="wrap">
  <section class="vl"><span class="side">Nº 2 — Swimming &amp; leisure</span><figure class="ph ratio-land">{img('pool','Pool', eager=True)}</figure><p class="note">Photograph: the main pool, The Breez Hotel.<br>Parasols, terrace and the children's pool.</p></section>
  <section class="vl"><span class="side">Nº 3 — Dining</span><figure class="ph ratio-land">{img('dine','Poolside lunch')}</figure><p class="note">Fresh juice and lunch on the pool terrace.</p></section>
</main>""",
"""
.wrap{max-width:var(--content-width);margin:0 auto;padding:var(--section-gap) var(--gutter);display:grid;gap:80px}
.vl{display:grid;grid-template-columns:40px 1fr 220px;gap:24px;align-items:end}
.side{writing-mode:vertical-rl;transform:rotate(180deg);font:600 12px var(--font-body);letter-spacing:.2em;text-transform:uppercase;color:var(--ochre-deep);align-self:start}
.note{font:italic 17px/1.4 var(--font-display);color:var(--ink-soft);border-left:1px solid var(--ochre);padding-left:14px;margin:0}
@media(max-width:760px){.vl{grid-template-columns:28px 1fr}.note{grid-column:2}}
""")

# 23 ------------------------------------------------------------------------
xp("23-layered-image-frames", "Layered image frames",
   "Gallery and museum sites: passe-partout mats and offset outlines",
   f"""
<main class="wrap">
  <figure class="lf f1"><div class="ph ratio-port">{img('roomp','Room, portrait view')}</div><figcaption>Passe-partout</figcaption></figure>
  <figure class="lf f2"><div class="ph ratio-port offset-outline">{img('gazebo2','Gazebo and flowerbeds')}</div><figcaption>Offset outline</figcaption></figure>
  <figure class="lf f3"><div class="ph ratio-port ticks">{img('sign','Hotel sign')}</div><figcaption>Corner ticks</figcaption></figure>
  <figure class="lf f4"><div class="ph ratio-port arch">{img('fountain2','Fountain lawn')}</div><figcaption>Arch mask</figcaption></figure>
</main>""",
"""
.wrap{max-width:var(--content-width);margin:0 auto;padding:var(--section-gap) var(--gutter);display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:48px}
.lf{margin:0;display:grid;gap:14px}.lf figcaption{font:600 12px var(--font-body);letter-spacing:.14em;text-transform:uppercase;color:var(--ink-soft)}
.f1 .ph{border:18px solid var(--paper);outline:1px solid var(--sand-deep);box-shadow:var(--shadow-soft)}
.f2 .ph{overflow:visible}.f2 img{position:relative;z-index:1}
.f3 .ph{overflow:visible}
.arch{border-radius:999px 999px 0 0}
""")

# 24 ------------------------------------------------------------------------
xp("24-creative-booking-panel", "Creative booking panel",
   "Terreno's circular BOOK NOW stamp; Hoxton's friendly booking copy",
   f"""
<main class="bp">
  <figure class="ph">{img('room','Room with four-poster bed', eager=True)}</figure>
  <form class="panel" data-booking aria-label="Booking request">
    <p class="label">Booking request</p>
    <h1 class="h2">When would you like to stay?</h1>
    <div class="row"><label>Arriving<input type="date" name="checkin" required></label><label>Leaving<input type="date" name="checkout" required></label></div>
    <fieldset><legend>Guests</legend><label><input type="radio" name="g" checked> Just me</label><label><input type="radio" name="g"> Two of us</label><label><input type="radio" name="g"> Family</label><label><input type="radio" name="g"> Group / company</label></fieldset>
    <label>Room preference<select><option>No preference</option><option>Single</option><option>Double</option><option>Deluxe</option><option>Superior</option><option>King</option></select></label>
    <p class="nights" data-nights aria-live="polite"></p>
    <div class="actions"><button class="btn btn--book" type="submit">Send request</button><a class="btn" href="https://wa.me/254707461665">WhatsApp us</a></div>
  </form>
</main>""",
"""
.bp{display:grid;grid-template-columns:1fr 1fr;min-height:100vh}
.bp > figure{min-height:50vh}
.panel{padding:clamp(24px,5vw,72px);display:grid;gap:18px;align-content:center;background:var(--paper)}
.row{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.panel label{display:grid;gap:6px;font:600 13px var(--font-body);color:var(--ink-soft)}
.panel input[type=date],.panel select{min-height:48px;font:16px var(--font-body);padding:0 12px;border:0;border-bottom:1px solid var(--ink);background:transparent;color:var(--ink)}
fieldset{border:0;padding:0;margin:0;display:flex;flex-wrap:wrap;gap:8px}legend{font:600 13px var(--font-body);color:var(--ink-soft);margin-bottom:8px}
fieldset label{display:inline-flex;align-items:center;gap:8px;min-height:44px;padding:0 14px;border:1px solid var(--sand-deep);border-radius:var(--pill);color:var(--ink);cursor:pointer}
fieldset label:has(input:checked){background:var(--palm);color:var(--sand);border-color:var(--palm)}
fieldset input{accent-color:var(--ochre)}
.nights{margin:0;font-size:14px;color:var(--ink-soft)}.actions{display:flex;flex-wrap:wrap;gap:10px}
@media(max-width:800px){.bp{grid-template-columns:1fr}}
""")

# 25 ------------------------------------------------------------------------
xp("25-asymmetric-section-margins", "Asymmetric section margins",
   "Alternating narrow and wide sections on Aman and editorial portfolios",
   f"""
<main>
  <section class="as as--left"><figure class="ph ratio-land">{img('courtyard','Courtyard', eager=True)}</figure><div><p class="label">Wide left</p><h2 class="h2">The courtyard</h2></div></section>
  <section class="as as--right"><div><p class="label">Narrow right</p><h2 class="h2">The pools</h2></div><figure class="ph ratio-port">{img('pool','Pool')}</figure></section>
  <section class="as as--center"><figure class="ph ratio-pano">{img('building','Building and palms')}</figure></section>
</main>""",
"""
.as{display:grid;gap:var(--gutter);align-items:end;margin-bottom:var(--section-gap)}
.as--left{grid-template-columns:2fr 1fr;padding-right:var(--gutter)}
.as--right{grid-template-columns:1fr 1fr;padding-left:22vw;padding-right:var(--gutter)}
.as--center{padding:0 12vw}
@media(max-width:760px){.as--left,.as--right{grid-template-columns:1fr;padding:0 20px}.as--center{padding:0}}
""")

# 26 (extra) -----------------------------------------------------------------
xp("26-karibu-stamp-and-ticker", "Karibu stamp and welcome ticker (discovered)",
   "Terreno's rotating stamp + the hotel's own sign word 'Karibu' and its English/Swahili captions on TikTok",
   """
<main class="kt">
  <div class="ticker" aria-hidden="true"><span>Karibu · Welcome · Karibuni sana · Class · Comfort · Ambience · Serenity · Karibu · Welcome · Karibuni sana · Class · Comfort · Ambience · Serenity ·</span></div>
  <a class="stamp" href="#" aria-label="Book your stay"><svg viewBox="0 0 160 160" aria-hidden="true"><defs><path id="r" d="M80 80 m-60 0 a60 60 0 1 1 120 0 a60 60 0 1 1 -120 0"/></defs><text><textPath href="#r">BOOK YOUR STAY · KARIBU · BOOK YOUR STAY · KARIBU ·</textPath></text></svg><span>B</span></a>
</main>""",
"""
.kt{min-height:100vh;display:grid;place-items:center;gap:40px;overflow:hidden;background:var(--palm)}
.ticker{width:100%;white-space:nowrap;border-block:1px solid var(--ochre);padding:16px 0;color:var(--sand);font:italic 500 clamp(1.6rem,4vw,3rem) var(--font-display)}
.ticker span{display:inline-block;animation:tick 30s linear infinite}
@keyframes tick{to{transform:translateX(-50%)}}
.stamp{position:relative;width:180px;height:180px;display:grid;place-items:center;text-decoration:none;border-radius:50%;background:var(--ochre)}
.stamp svg{position:absolute;inset:0;animation:spin 20s linear infinite}.stamp text{font:700 12px var(--font-body);letter-spacing:.22em;fill:#1E140A}
.stamp span{font:600 64px var(--font-display);color:#1E140A}
.stamp:hover svg{animation-duration:6s}
@keyframes spin{to{transform:rotate(360deg)}}
""")

PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{n} · {title} — Breez design experiment</title>
<link rel="stylesheet" href="../../../assets/css/base.css"><link rel="stylesheet" href="style.css"></head>
<body>
<div class="xp-bar"><span>Experiment {n} — {title}</span><span>Inspired by: {inspired}</span><a href="../../../design-laboratory/index.html">← Design laboratory</a></div>
{body}
<script src="../../../assets/js/site.js"></script>
</body></html>
"""

def main():
    os.makedirs(OUT, exist_ok=True)
    idx = []
    for x in XP:
        d = os.path.join(OUT, x["slug"]); os.makedirs(d, exist_ok=True)
        n = x["slug"][:2]
        open(os.path.join(d, "index.html"), "w").write(PAGE.format(n=n, title=H.escape(x["title"]), inspired=H.escape(x["inspired"]), body=x["body"]))
        open(os.path.join(d, "style.css"), "w").write("/* " + x["title"] + " */\n" + x["css"].strip() + "\n")
        idx.append(dict(n=n, slug=x["slug"], title=x["title"], inspired=x["inspired"]))
    json.dump(idx, open(os.path.join(OUT, "experiments.json"), "w"), indent=1)
    print(len(idx), "experiments written")

if __name__ == "__main__":
    main()
