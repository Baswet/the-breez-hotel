"""Write src/lab.html: the motion lab (15 working experiments from the site's own components)."""
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
I = '../images/breez/'
def im(p, alt=''): return f'<img src="{I}{p}-1600.webp" alt="{alt}" loading="lazy">'
slides = ''.join('<figure class="sl-slide%s">%s</figure>' % (' on' if i == 0 else '', im(k)) for i, k in enumerate(['rooms/room-grey-bedding', 'rooms/room-desk-armchair', 'rooms/bathroom-shower']))
slideshow = ('<div class="sl" data-slides tabindex="0"><div class="sl-stage">' + slides + '</div><div class="sl-bar"><div class="sl-dots">'
             '<button type="button" data-dot aria-current="true" aria-label="Photo 1"></button><button type="button" data-dot aria-label="Photo 2"></button><button type="button" data-dot aria-label="Photo 3"></button></div>'
             '<div class="sl-ctl"><span class="sl-count" data-count>01 / 03</span><button type="button" data-prev aria-label="Previous">←</button><button type="button" data-next aria-label="Next">→</button></div></div></div>')
stag = ''.join(f'<figure class="hx-ph">{im(k)}</figure>' for k in ['gardens/gazebo-cypress', 'pools/kids-pool-umbrellas', 'gardens/garden-gazebo-roof', 'exterior/entrance-gate'])
demos = [
 ('01', 'Word-by-word headline', '<h2 class="lab-h" data-split="words">Stay. Unwind. Discover.</h2>'),
 ('02', 'Character-by-character', '<h2 class="lab-h" data-split="chars">Karibu</h2>'),
 ('03', 'Line-by-line mask', '<h2 class="lab-h" data-split="lines" style="max-width:12ch">Your next stay starts at the gate.</h2>'),
 ('04', 'Circular image reveal', f'<figure class="hx-ph lab-img" data-reveal="circle">{im("gardens/fountain-lawn-swing")}</figure>'),
 ('05', 'Organic (arch) reveal', f'<figure class="hx-ph lab-img mask-arch" data-reveal="arch">{im("exterior/tower-and-terrace-tall")}</figure>'),
 ('06', 'Cinematic entrance: blur to sharp', f'<figure class="hx-ph lab-img" data-reveal="blur">{im("pools/pool-lawn-view")}</figure>'),
 ('07', 'Layered parallax', f'<div class="lab-layer"><figure class="hx-ph a">{im("exterior/main-building-facade")}</figure><figure class="hx-ph b mask-arch" data-parallax="0.12">{im("exterior/sign-the-breeze-hotel-karibu")}</figure></div>'),
 ('08', 'Pinned image and text', '<p class="lab-note">On the homepage, “One day, five moments”: the photo holds while five statements change and the background tone shifts.</p><a class="link" href="../index.html#story-h">Open on the homepage</a>'),
 ('09', 'Expanding composition', '<p class="lab-note">On the Rooms page: an arched room photo grows to full width as you scroll.</p><a class="link" href="../rooms.html#xp-h">Open on Rooms</a>'),
 ('10', 'Marquee typography', '<div class="mq" data-marquee><div class="mq-track"><span>Karibu</span><span>Stay</span><span>Swim</span><span>Dine</span><span>Meet</span><span>Celebrate</span></div></div>'),
 ('11', 'Scroll-tinted statement', '<p class="lab-tint" data-tint>A garden hotel on the Kisumu–Busia Road, where guests come to stay the night, to swim, to meet and to celebrate.</p>'),
 ('12', 'Staggered gallery reveal', f'<div class="lab-stag" data-stagger>{stag}</div>'),
 ('13', 'Image-to-image: directional slide mask', slideshow),
 ('14', 'Cinematic slideshow: liquid displacement', '<p class="lab-note">On the Gallery page, “Six moments at The Breez”: a WebGL displacement transition, with a crossfade fallback.</p><a class="link" href="../gallery.html#lq-h">Open the Gallery</a>'),
 ('15', 'Animated geometric framing', f'<div class="lab-ring"><figure class="hx-ph mask-circle ring">{im("gardens/fountain-seating")}</figure></div>'),
]
body = ''.join(f'<section class="lab-demo"><header><span class="hx-k">{n}</span><h3>{t}</h3></header><div class="lab-stage">{d}</div></section>' for n, t, d in demos)
css = """.lab{width:min(100% - 2*var(--pad),1200px);margin:0 auto;padding:48px 0 120px}.lab>h1{font:500 clamp(3rem,2rem + 4vw,6rem)/.9 var(--f-display);margin:10px 0 12px}
.lab-demo{border-top:1px solid var(--rule-strong);padding:40px 0 64px;display:grid;grid-template-columns:260px minmax(0,1fr);gap:32px}.lab-demo h3{font:500 1.6rem var(--f-display);margin:8px 0 0}
.lab-h{font:500 clamp(2.6rem,1.6rem + 4vw,5.6rem)/.95 var(--f-display);margin:0;color:var(--green)}.lab-img{aspect-ratio:16/9}.lab-img.mask-arch{aspect-ratio:3/4;max-width:420px}
.lab-layer{position:relative;padding:0 0 12% 0}.lab-layer .a{aspect-ratio:16/9;width:80%}.lab-layer .b{position:absolute;right:4%;bottom:0;width:30%;aspect-ratio:3/4;border:8px solid var(--ivory)}
.lab-tint{font:500 clamp(1.8rem,1rem + 2.4vw,3.2rem)/1.2 var(--f-display);margin:0}.lab-stag{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}.lab-stag figure{aspect-ratio:3/4}
.lab-ring{max-width:320px;padding:40px}.lab-note{color:var(--ink-2);margin:0 0 10px}@media(max-width:760px){.lab-demo{grid-template-columns:1fr}.lab-stag{grid-template-columns:1fr 1fr}}"""
html = f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>Motion lab · The Breez Hotel</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;1,500&family=Karla:wght@400;700&display=swap">
<link rel="stylesheet" href="../assets/site.css"><link rel="stylesheet" href="../assets/heroes.css"><link rel="stylesheet" href="../assets/motion.css"><style>{css}</style></head>
<body><main class="lab"><span class="hx-k">The Breez Hotel</span><h1>Motion lab</h1>{body}</main>
<script>document.documentElement.classList.add('js')</script><script src="../assets/effects.js"></script></body></html>'''
(ROOT / 'src/lab.html').write_text(html, encoding='utf-8')
print('lab written')
