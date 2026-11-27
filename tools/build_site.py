#!/usr/bin/env python3
"""Build the production website for The Breez Hotel into ./site.

Static HTML, one shared stylesheet (src/css/site.css) and script (src/js/site.js).
Facts used on the pages are limited to what the hotel's own channels confirm
(see docs/final-design-recommendation.md). Room categories and features are shown
"as listed on Booking.com"; rates, capacities, menus and hours are "on request".

Run:  python3 tools/build_site.py
"""
import html, json, shutil, datetime
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'site'
BASE_URL = 'https://baswet.github.io/the-breez-hotel/'
TODAY = datetime.date.today().isoformat()

PHONE_DISPLAY = '0707 461 665'
TEL = 'tel:+254707461665'
WA = 'https://wa.me/254707461665'
EMAIL = 'thebreezhotel@gmail.com'
FB = 'https://www.facebook.com/TheBreezhotelofficial'
TT = 'https://www.tiktok.com/@thebreezhotelbusia'
ADDRESS = 'Kisumu–Busia Road, Busia, Kenya'
# Verified 26 Nov 2026 against the Google Maps place 'The Breez Hotel, Busia' (Kisumu–Busia Road)
GEO = (0.4564723, 34.1215845)
MAP_EMBED = 'https://maps.google.com/maps?q=0.4564723,34.1215845&z=16&output=embed'
MAP_PLACE = 'https://www.google.com/maps/place/The+Breez+Hotel+,+Busia/@0.4564723,34.1215845,17z'
MAP_LINK = 'https://www.google.com/maps/search/?api=1&query=The+Breez+Hotel+Busia+Kenya'

# Photos not published: identifiable guests without recorded consent, and seasonal decor.
EXCLUDE = {'guests-lunch-garden-terrace', 'wedding-party-courtyard', 'wedding-marquee-guests',
           'reception-christmas', 'lobby-christmas', 'bed-towel-art', 'building-palms-umbrellas', 'grilled-chicken'}

STOCK = {  # key: (photographer, unsplash photo id or page)
    'woman-swimming-pool': ('Leilani Angel', 'Unsplash'),
    'pool-reading-lifestyle': ('Abby Thompson', 'Unsplash'),
    'kenya-lake-sunset': ('Tony Samuel Gachie', 'Unsplash'),
    'food-table-shared': ('Annie Spratt', 'Unsplash'),
    'rice-chicken-plate': ('Takashi Miyazaki', 'Unsplash'),
    'group-dinner': ('Jim Nyamao', 'Unsplash'),
    'waiter-serving': ('Kate Townsend', 'Unsplash'),
    'long-table-gathering': ('Lisa Marie Theck', 'Unsplash'),
    'friends-lunch': ('Sweet Life', 'Unsplash'),
    'food-salmon-plate': ('Casey Lee', 'Unsplash'),
    'food-sauce-pour': ('Urban Gyllström', 'Unsplash'),
    'food-grilled-board': ('Mark DeYoung', 'Unsplash'),
    'food-chicken-woodboard': ('Bayu Syaits', 'Unsplash'),
    'drink-mango-juice': ('Sam Hojati', 'Unsplash'),
    'drink-three-juices': ('Dhiren Maru', 'Unsplash'),
    'food-breakfast-bowls': ('Monaz Hastam', 'Unsplash'),
    'food-table-evening': ('Jay Wennington', 'Unsplash'),
    'food-table-set': ('Kamilla Isalieva', 'Unsplash'),
    'food-overhead-plate': ('Jametlene Reskp', 'Unsplash'),
    'food-fries-golden': ('Pixzolo Photography', 'Unsplash'),
    'food-burger-fries': ('Mike', 'Unsplash'),
    'linen-coffee-eucalyptus': ('Madison Inouye', 'Pexels'),
    'drink-mocktails-sunlit': ('Anastase Maragos', 'Unsplash'),
    'food-lunch-by-water': ('Hameen Reynolds', 'Unsplash'),
}

LICENSES = {'Unsplash': 'https://unsplash.com/license', 'Pexels': 'https://www.pexels.com/license/'}

ALT = {
    'building-palms-pool-court': 'The Breez Hotel building rising behind palms and the pool court',
    'building-palms-umbrellas': 'Hotel building with palms and poolside umbrellas',
    'main-building-facade': 'Main building facade of The Breez Hotel',
    'tower-and-terrace': 'The hotel tower above the terrace',
    'tower-and-terrace-tall': 'The hotel tower above the terrace',
    'wing-and-garden': 'Guest wing beside the garden',
    'entrance-gate': 'Entrance gate of the hotel on the Kisumu–Busia Road',
    'sign-the-breeze-hotel-karibu': 'Carved stone sign at the hotel reading “The Breeze Hotel — Karibu”',
    'gate-sign-crop': 'Hotel name sign at the gate',
    'i-love-the-breez-sign': '“I love The Breez” sign at the hotel',
    'wall-sign-i-love-the-breez': '“I love The Breez” wall sign',
    'vip-lounge-tower-kids-pool': 'VIP lounge and tower beside the kids’ pool',
    'cottage-courtyard-swing': 'Garden swing in the cottage courtyard',
    'courtyard-fountain-gazebos': 'Courtyard fountain with gazebos',
    'courtyard-fountain-tent': 'Courtyard fountain with an events tent',
    'courtyard-lawn-fountain': 'Lawn and fountain in the courtyard',
    'gazebo-flowerbeds': 'Gazebo among flowerbeds',
    'gazebo-cypress': 'Gazebo framed by cypress trees',
    'gazebo-cypress-2': 'Gazebo and cypress trees in the garden',
    'cottages-lawn': 'Cottages facing the lawn',
    'gazebo-garden': 'Garden gazebo',
    'fountain-seating': 'Seating beside the fountain',
    'gazebo-steps': 'Steps up to a garden gazebo',
    'garden-gazebo-roof': 'Thatched gazebo roof in the garden',
    'walkway-cottages': 'Walkway between the cottages',
    'fountain-lawn-swing': 'Fountain, lawn and swing',
    'cypress-cottage': 'Cottage behind cypress trees',
    'pool-umbrellas-above': 'Pool and umbrellas seen from above',
    'pool-terrace-kids-pool': 'Pool terrace with the kids’ pool',
    'pool-aerial': 'Aerial view of the swimming pool',
    'poolside-tables': 'Tables beside the pool',
    'pool-garden-view': 'Pool with garden view',
    'pool-lawn-view': 'Pool beside the lawn',
    'pool-top-down': 'Pool water seen from above',
    'pool-lanes': 'Pool lanes in sunlight',
    'pool-lanes-2': 'Pool lanes',
    'pool-lanes-3': 'Pool lanes and deck',
    'pool-loungers': 'Loungers along the pool',
    'pool-fence-umbrellas': 'Pool fence and umbrellas',
    'kids-pool-umbrellas': 'Kids’ pool with umbrellas',
    'kids-pool-building': 'Kids’ pool in front of the building',
    'room-four-poster-window': 'Guest room with four-poster bed by the window',
    'room-four-poster-2': 'Guest room with four-poster bed',
    'room-fridge-tv': 'Guest room with fridge and TV',
    'room-grey-bedding': 'Guest room with grey bedding',
    'room-desk-armchair': 'Guest room with desk and armchair',
    'room-portrait': 'Guest room',
    'room-net-portrait': 'Bed with mosquito net',
    'room-vanity': 'Room vanity and mirror',
    'room-tv-fridge': 'TV and fridge in a guest room',
    'single-room': 'Single guest room',
    'room-desk': 'Writing desk in a guest room',
    'room-double': 'Double guest room',
    'bed-detail': 'Made bed detail',
    'bed-towel-art': 'Towel art on a made bed',
    'bed-towel-art-2': 'Towel art welcome on the bed',
    'bathroom-toilet-basin': 'En-suite bathroom basin',
    'bathroom-shower': 'En-suite shower',
    'lounge-rattan-sofas': 'Lounge with rattan sofas',
    'lounge-rattan-2': 'Rattan lounge seating',
    'veranda-corridor': 'Veranda corridor',
    'entrance-lobby': 'Hotel entrance lobby',
    'hall-classroom-setup': 'Meeting hall in classroom set-up',
    'hall-gold-cloths': 'Hall dressed with gold cloths',
    'hall-red-skirting': 'Hall with red table skirting',
    'hall-classroom-2': 'Meeting hall, classroom layout',
    'hall-banquet-gold': 'Banquet set-up in gold',
    'hall-banquet-red': 'Banquet set-up in red',
    'hall-projector': 'Meeting hall with projector',
    'hall-theatre-grey': 'Hall in theatre set-up',
    'hall-banquet-2': 'Banquet set-up',
    'hall-screen': 'Hall with projection screen',
    'poolside-meal-juice': 'Meal and fresh juice served by the pool',
    'restaurant-interior-blue': 'Restaurant interior',
    'bar-counter-stools': 'Bar counter and stools',
    'bar-ice-buckets': 'Bar with ice buckets',
    'bar-shelves': 'Bar shelves',
    'buffet-samosa-chapati': 'Buffet table',
    'roast-meat': 'Roast meat from the kitchen',
    'stew-plate': 'Plate from the kitchen',
    'grilled-chicken': 'Grilled chicken from the kitchen',
    'buffet-decor': 'Decorated buffet',
    'tent-wedding-setup': 'Wedding tent set-up on the grounds',
    'tent-buffet-line': 'Buffet line inside an events tent',
    'marquee-lawn': 'Marquee on the lawn',
    'garden-party-setup': 'Garden party set-up',
    'garden-party-balloons': 'Garden party with balloons',
    'tent-red-white': 'Red and white events tent',
    'staff-team-welcome': 'The Breez Hotel team',
    'woman-swimming-pool': 'A swimmer floating in a pool',
    'pool-reading-lifestyle': 'Reading by a pool',
    'kenya-lake-sunset': 'Sunset over a Kenyan lake',
    'food-table-shared': 'A shared table of dishes',
    'rice-chicken-plate': 'A plate of rice and chicken',
    'group-dinner': 'Friends laughing over dinner',
    'waiter-serving': 'A waiter carrying drinks',
    'long-table-gathering': 'A long table gathering',
    'friends-lunch': 'Friends sharing lunch',
    'food-salmon-plate': 'A plated fish dish with fresh vegetables',
    'food-sauce-pour': 'A chef finishing a plated dish with sauce',
    'food-grilled-board': 'Grilled chicken and vegetables on a wooden board',
    'food-chicken-woodboard': 'Grilled chicken served on a wooden platter',
    'drink-mango-juice': 'Fresh mango juice with lime',
    'drink-three-juices': 'Three fresh fruit juices',
    'food-breakfast-bowls': 'A breakfast table seen from above',
    'food-table-evening': 'Plates and glasses on an evening dinner table',
    'food-table-set': 'A dinner table set with plates and glasses',
    'food-overhead-plate': 'A plated dish seen from above',
    'food-fries-golden': 'Golden fries with a dipping sauce',
    'food-burger-fries': 'A burger with fries in a steel cup',
    'linen-coffee-eucalyptus': 'A cup of black coffee and a sprig of eucalyptus on white bed linen',
    'drink-mocktails-sunlit': 'Fruit mocktails in afternoon sunlight',
    'food-lunch-by-water': 'Lunch and a cold drink on a ledge by the water',
}

CAT_LABEL = {'exterior': 'Building', 'gardens': 'Gardens', 'pools': 'Pools', 'rooms': 'Rooms',
             'interiors': 'Interiors', 'conference': 'Meetings', 'dining': 'Dining', 'events': 'Events', 'people': 'People'}

# ---------------------------------------------------------------------------- images
IMAGES = {}   # key -> dict(path800, path1600, w, h, stock, cat)
def scan():
    for p in sorted((ROOT / 'assets/images/breez').glob('*/*-1600.webp')):
        key = p.name[:-10]
        if key in EXCLUDE: continue
        with Image.open(p) as im: w, h = im.size
        IMAGES[key] = dict(cat=p.parent.name, stock=False, w=w, h=h, rel=f'images/breez/{p.parent.name}/{key}')
    for p in sorted((ROOT / 'assets/images/stock').glob('*-1600.webp')):
        key = p.name[:-10]
        if key not in STOCK: continue
        with Image.open(p) as im: w, h = im.size
        IMAGES[key] = dict(cat='stock', stock=True, w=w, h=h, rel=f'images/stock/{key}')
USED = set()

def img(key, sizes='(max-width:760px) 100vw, 50vw', eager=False, alt=None):
    m = IMAGES[key]; USED.add(key)
    a = html.escape(alt if alt is not None else ALT.get(key, ''), quote=True)
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    w1600 = 1600 if m['w'] >= 1600 else m['w']
    return (f'<img src="{m["rel"]}-1600.webp" srcset="{m["rel"]}-800.webp 800w, {m["rel"]}-1600.webp {w1600}w" '
            f'sizes="{sizes}" width="{m["w"]}" height="{m["h"]}" alt="{a}" {load} decoding="async">')

def ph(key, cls='', sizes='(max-width:760px) 100vw, 50vw', eager=False, cap=True, alt=None, extra=''):
    m = IMAGES[key]
    c = ''   # stock credits are kept on the photo-credits page and in docs/, not on the image
    return f'<figure class="ph {cls}"{extra}>{img(key, sizes, eager, alt)}{c}</figure>'


def hx(key, cls='', sizes='(max-width:760px) 100vw, 50vw', eager=False, alt=None, num=None, extra=''):
    n = f'<figcaption class="hx-no">{num}</figcaption>' if num else ''
    return f'<figure class="hx-ph {cls}"{extra}>{img(key, sizes, eager, alt)}{n}</figure>'

def crumb(label):
    return f'<nav class="crumb" aria-label="Breadcrumb"><a href="index.html">Home</a><span>/</span><span>{label}</span></nav>'

# ---------------------------------------------------------------------------- chrome
ICON = {
  'phone': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 5a2 2 0 0 1 2-2"/></svg>',
  'wa': '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.3-.4.7-1.4.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6a2.7 2.7 0 0 0 1.8-1.3 2.2 2.2 0 0 0 .2-1.3c-.1-.1-.3-.2-.5-.3Z"/></svg>',
  'cal': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><rect x="3" y="5" width="18" height="16" rx="1"/><path d="M3 10h18M8 3v4M16 3v4"/></svg>',
  'mail': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="1"/><path d="m3 7 9 6 9-6"/></svg>',
}
import hashlib as _hl
_SRC = {'site.css': 'src/css/site.css', 'heroes.css': 'src/css/heroes.css', 'motion.css': 'src/css/motion.css', 'site.js': 'src/js/site.js', 'effects.js': 'src/js/effects.js'}
# cache-busting: version each asset by its content, so every deploy that changes a file changes its URL
ASSET_V = {k: _hl.sha1((ROOT / v).read_bytes()).hexdigest()[:10] for k, v in _SRC.items()}

NAV = [('rooms', 'Stay'), ('pools', 'Pools'), ('dining', 'Dining'), ('meetings', 'Meetings & Events'),
       ('gallery', 'Gallery'), ('about', 'About'), ('contact', 'Contact')]

def href(slug): return 'index.html' if slug == 'index' else f'{slug}.html'
def cur(slug, s): return ' aria-current="page"' if slug == s else ''

def header(slug):
    left = ''.join(f'<a href="{href(s)}"{cur(slug, s)}>{t}</a>' for s, t in NAV[:4])
    right = ''.join(f'<a href="{href(s)}"{cur(slug, s)}>{t}</a>' for s, t in NAV[4:])
    ov = ''.join(f'<li><a href="{href(s)}"{cur(slug, s)}>{t}</a></li>' for s, t in [('index', 'Home')] + NAV + [('book', 'Book a stay')])
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="hdr{' hdr--over' if slug == 'index' else ''}">
  <div class="hdr-in">
    <nav class="nav" aria-label="Primary">{left}</nav>
    <a class="mark" href="index.html" aria-label="The Breez Hotel, home"><b>The Breez</b><span>Hotel · Busia</span></a>
    <nav class="nav nav--r" aria-label="Secondary">{right}<a class="btn btn--book" href="book.html"{cur(slug, 'book')}>Book</a></nav>
    <button class="menu-btn" type="button" data-open-menu aria-controls="menu" aria-expanded="false"><i></i>Menu</button>
  </div>
</header>
<div class="overlay" id="menu" aria-hidden="true" role="dialog" aria-modal="true" aria-label="Menu">
  <div class="ov-top"><a class="mark" href="index.html"><b>The Breez</b><span>Hotel · Busia</span></a><button class="ov-close" type="button">Close</button></div>
  <ul class="ov-nav">{ov}</ul>
  <div class="ov-foot"><a class="btn btn--wa" href="{WA}" target="_blank" rel="noopener">{ICON['wa']} WhatsApp {PHONE_DISPLAY}</a><a class="btn btn--light" href="{TEL}">{ICON['phone']} Call reception</a></div>
</div>'''

def footer():
    g1 = [('index', 'Home'), ('about', 'About'), ('rooms', 'Rooms'), ('pools', 'Pools'), ('dining', 'Dining')]
    g2 = [('meetings', 'Meetings &amp; Events'), ('gallery', 'Gallery'), ('contact', 'Contact'), ('book', 'Book a stay')]
    ul = lambda g: ''.join(f'<li><a href="{href(s)}">{t}</a></li>' for s, t in g)
    return f'''<footer class="ftr">
  <svg class="ftr-edge" viewBox="0 0 1440 120" preserveAspectRatio="none" aria-hidden="true"><path d="M0 120V78L330 104L640 40L800 82L1010 58L1440 96V120Z"/></svg>
  <div class="wrap ftr-body">
    <p class="ftr-word" aria-hidden="true">The Breez</p>
    <div class="ftr-grid">
      <div class="ftr-brand"><a class="mark" href="index.html" aria-label="The Breez Hotel, home"><b>The Breez</b><span>Hotel · Busia</span></a><p>Karibu. We look forward to welcoming you.</p></div>
      <nav class="ftr-nav" aria-label="Footer"><span class="label">Explore</span><ul>{ul(g1)}</ul></nav>
      <nav class="ftr-nav" aria-label="Footer, more"><span class="label">&nbsp;</span><ul>{ul(g2)}</ul></nav>
      <div class="ftr-contact"><span class="label">Contact</span><ul><li><a href="{TEL}">{PHONE_DISPLAY}</a></li><li><a href="mailto:{EMAIL}">{EMAIL}</a></li><li>{ADDRESS}</li></ul>
        <div class="ftr-social"><a href="{FB}" target="_blank" rel="noopener" aria-label="The Breez Hotel on Facebook">{SOCIAL_ICON['fb']}</a><a href="{TT}" target="_blank" rel="noopener" aria-label="The Breez Hotel on TikTok">{SOCIAL_ICON['tt']}</a><a href="{WA}" target="_blank" rel="noopener" aria-label="WhatsApp reception">{ICON['wa']}</a></div></div>
    </div>
    <div class="ftr-base"><span>&copy; <span data-year>2026</span> The Breez Hotel, Busia, Kenya</span><span><a href="credits.html">Photo credits</a> &middot; Bookings are requests until confirmed by the hotel.</span><a class="ftr-top" href="#main">Back to top <span aria-hidden="true">&uarr;</span></a></div>
  </div>
</footer>
<nav class="dock" aria-label="Quick actions"><a href="{TEL}">{ICON['phone']} Call</a><a href="{WA}" target="_blank" rel="noopener">{ICON['wa']} WhatsApp</a><a href="book.html">{ICON['cal']} Book</a></nav>'''

def jsonld():
    d = {"@context": "https://schema.org", "@type": "Hotel", "name": "The Breez Hotel", "url": BASE_URL,
         "image": BASE_URL + "images/og-image.jpg", "telephone": "+254707461665", "email": EMAIL,
         "address": {"@type": "PostalAddress", "streetAddress": "Kisumu–Busia Road", "addressLocality": "Busia", "addressCountry": "KE"},
         "sameAs": [FB, TT],
         "amenityFeature": [{"@type": "LocationFeatureSpecification", "name": n, "value": True} for n in
                            ["Swimming pools", "Kids' pool", "Restaurant", "Bar", "Meeting rooms", "Free Wi-Fi", "Secure parking", "Gardens"]]}
    return f'<script type="application/ld+json">{json.dumps(d, ensure_ascii=False)}</script>'

def page(slug, title, desc, body, og_img='images/og-image.jpg'):
    url = BASE_URL + ('' if slug == 'index' else f'{slug}.html')
    full = title if slug == 'index' else f'{title} · The Breez Hotel, Busia'
    BASE_TAG = '\n<base href="/the-breez-hotel/">' if slug == '404' else ''
    ld = jsonld() if slug in ('index', 'contact') else ''
    doc = f'''<!DOCTYPE html>
<html lang="en-KE">
<head>
<meta charset="utf-8">{BASE_TAG}
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(full)}</title>
<meta name="description" content="{html.escape(desc, quote=True)}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#20392B">
<meta property="og:type" content="website"><meta property="og:site_name" content="The Breez Hotel">
<meta property="og:title" content="{html.escape(full, quote=True)}"><meta property="og:description" content="{html.escape(desc, quote=True)}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{BASE_URL}{og_img}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:locale" content="en_KE"><meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="images/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;1,300;1,400;1,500&family=Karla:wght@400;500;700&display=swap">
<link rel="stylesheet" href="assets/site.css?v={ASSET_V["site.css"]}">
<link rel="stylesheet" href="assets/heroes.css?v={ASSET_V["heroes.css"]}">
<link rel="stylesheet" href="assets/motion.css?v={ASSET_V["motion.css"]}">
{ld}
</head>
<body class="p-{slug}">
{header(slug)}
<main id="main">
{body}
</main>
{footer()}
<script src="assets/site.js?v={ASSET_V["site.js"]}" defer></script>
<script src="assets/effects.js?v={ASSET_V["effects.js"]}" defer></script>
</body>
</html>
'''
    (OUT / href(slug)).write_text(doc, encoding='utf-8')

def head(label, title, extra='', light=False, tag='h2'):
    return f'<div class="head{" head--light" if light else ""} rv"><div><span class="label{" label--light" if light else ""}">{label}</span><{tag} class="h-l">{title}</{tag}></div><div>{extra}</div></div>'

# ---------------------------------------------------------------------------- pages
ROOMS = {
    'single': {'Room': 'Standard Single', 'Bed': '1 single bed', 'Sleeps': '1 guest', 'Balcony': 'Listed', 'Air conditioning': 'Not listed', 'View': 'Pool view', 'Breakfast': 'Included as listed', 'Rate': 'On request'},
    'double': {'Room': 'Double Room', 'Bed': '1 double bed', 'Sleeps': '2 guests', 'Balcony': 'Listed', 'Air conditioning': 'Not listed', 'View': 'Pool view', 'Breakfast': 'Included as listed', 'Rate': 'On request'},
    'deluxe': {'Room': 'Deluxe Room', 'Bed': '1 double bed', 'Sleeps': '2 guests', 'Balcony': 'Listed', 'Air conditioning': 'Listed', 'View': 'City view', 'Breakfast': 'Included as listed', 'Rate': 'On request'},
    'king':   {'Room': 'King Room', 'Bed': '1 large double bed', 'Sleeps': '2 guests', 'Balcony': 'Listed', 'Air conditioning': 'Listed', 'View': 'Pool view', 'Breakfast': 'Included as listed', 'Rate': 'On request'},
}

STORY = [
    ('entrance-gate', 'Arrive', 'Through the gate.', 'The stone sign says Karibu. Secure parking waits inside.', 'contact.html', 'Find us', 'stone'),
    ('room-four-poster-window', 'Stay', 'A room by the garden.', 'Single, Double, Deluxe and King rooms, with Wi-Fi and housekeeping.', 'rooms.html', 'See the rooms', 'warm'),
    ('pool-umbrellas-above', 'Swim', 'Two pools in the palm court.', 'A main pool, a kids’ pool, loungers and shade.', 'pools.html', 'Visit the pools', 'pool'),
    ('poolside-meal-juice', 'Dine', 'Lunch at the water’s edge.', 'Restaurant, bar and poolside service. Breakfast with stays, as listed.', 'dining.html', 'Restaurant &amp; bar', 'warm'),
    ('courtyard-fountain-gazebos', 'Celebrate', 'Evenings on the lawn.', 'Gazebos, a fountain and marquees for weddings, ruracio and parties.', 'meetings.html', 'Plan an event', 'green'),
]
STORY_IMGS = [x[0] for x in STORY]


MOOD_POS = {'gazebo-cypress': '45% 50%', 'pool-terrace-kids-pool': '58% 60%', 'garden-party-setup': '50% 60%', 'room-four-poster-window': '55% 50%'}

MOOD_LAYOUT = {  # main photo, supporting photo, composition
    '01': ('garden-gazebo-roof', None, 'square'),
    '02': ('pool-umbrellas-above', 'pool-lanes-2', 'wide'),
    '03': ('tent-wedding-setup', 'garden-party-setup', 'tall'),
    '04': ('room-four-poster-2', None, 'portrait'),
}
PLACE_WORDS = ['unwind', 'gather', 'celebrate', 'discover', 'belong']

MOODS = [
    ('01', 'The quiet of morning', 'Let the day begin <em>gently</em>.', 'gazebo-cypress',
     'Early light on the lawns, the gazebos still in shade, and breakfast with your stay where the room rate includes it.',
     'dining.html', 'Discover dining', 'wide'),
    ('02', 'The brightness of afternoon', 'Where the afternoon <em>slows down</em>.', 'pool-terrace-kids-pool',
     'Sun on the water, shade under the blue umbrellas, a lounger by the pool and a fresh juice brought to the table.',
     'pools.html', 'Discover the pools', 'tall'),
    ('03', 'The art of coming together', 'Good moments are <em>better shared</em>.', 'garden-party-setup',
     'Round tables on the lawn, a marquee for the wedding, a hall set for the workshop. There is room for everyone who matters.',
     'meetings.html', 'Discover meetings &amp; celebrations', 'cine'),
    ('04', 'The beauty of evening', 'As the day settles, <em>stay a little longer</em>.', 'room-four-poster-window',
     'The garden goes quiet, the lights come on along the veranda, and a four-poster bed with fresh linen is waiting.',
     'rooms.html', 'Discover the rooms', 'side'),
]

HIGHLIGHTS = [
    ('leaf', '01', 'A place to unwind', 'Palms, lawns, gazebos and a fountain in the courtyard: quiet corners to sit, read and let the afternoon pass.', 'about.html', 'The hotel and its grounds'),
    ('wave', '02', 'Moments by the pool', 'A swimming pool and a children&rsquo;s pool, with loungers, blue umbrellas and a fresh juice brought to the table.', 'pools.html', 'See the pools'),
    ('star', '03', 'Room to come together', 'Halls, lawns and marquees for conferences, weddings, ruracio and birthdays.', 'meetings.html', 'Plan an event'),
    ('bed', '04', 'A stay to remember', 'Four room categories, with free Wi-Fi, daily housekeeping, secure parking and access to both pools.', 'rooms.html', 'See the rooms'),
]
LOWER_ICONS = {'leaf': '<path d="M20.5 3.5C11 3.6 4.6 8.4 4.2 15.6c-.1 1.2 0 2.4.4 3.5L2.8 21l1.4 1.4 1.9-1.9c1 .4 2.2.5 3.4.4 7.2-.5 11-6.9 11-17.4zM8.9 18.1l6.7-6.7-1.4-1.4-6.7 6.7c-.2-.7-.2-1.4-.1-2.1.3-4.9 4.3-8.4 10.8-8.9-.5 6.5-3.6 11-8.6 11.4-.3 0-.5 0-.7 0z"/>',
    'bed': '<path d="M3 5h2.6v6.2H8V9.4C8 8.1 9 7 10.4 7h7.8C20.3 7 22 8.7 22 10.8V19h-2.6v-2.6H5.6V19H3zm2.6 8.8h13.8v-2.6H5.6z"/>'}
SOCIAL_ICON = {
    'fb': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M13.5 21v-7.6h2.6l.4-3h-3V8.5c0-.9.3-1.5 1.5-1.5h1.6V4.3c-.3 0-1.2-.1-2.3-.1-2.3 0-3.9 1.4-3.9 4v2.2H7.8v3h2.6V21z"/></svg>',
    'tt': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M16.6 3c.3 2.2 1.6 3.6 3.9 3.8v2.6c-1.4.1-2.6-.3-3.9-1.1v5.6c0 6.9-7.6 9.1-10.6 4.1-2-3.2-.8-8.9 5.6-9.1v2.7c-.5.1-1 .2-1.5.4-1.4.5-2.2 1.4-2 3 .4 3.1 6 4 5.6-2V3z"/></svg>',
}

def lower_home():
    hl = ''.join(
        f'<div class="bx-f rv"><svg class="bx-i" viewBox="0 0 24 24" aria-hidden="true">{({**EXP_ICONS, **LOWER_ICONS})[ic]}</svg>'
        f'<div><span class="lw-no">{n}</span><h3>{h}</h3><p>{t} <a href="{u}">{lt}</a></p></div></div>' for ic, n, h, t, u, lt in HIGHLIGHTS)
    return f'''<section class="lw-rev" aria-labelledby="rev-h">
  <div class="lw-rev-ph">{img('linen-coffee-eucalyptus', '100vw')}</div>
  <div class="lw-rev-in wrap">
    <div class="lw-rev-panel rv">
      <span class="ed-kick">Guest reviews</span>
      <h2 id="rev-h">What our guests say</h2>
      <p>The best way to know a place is to hear it from the people who stayed. Guests share their time at The Breez in their own words on Google and on Facebook.</p>
      <div class="lw-rev-links"><a class="ed-mood-link" href="{MAP_PLACE}" target="_blank" rel="noopener">Read reviews on Google<span aria-hidden="true"> &rarr;</span></a><a class="ed-mood-link" href="{FB}" target="_blank" rel="noopener">Visit us on Facebook<span aria-hidden="true"> &rarr;</span></a></div>
    </div>
    <div class="lw-book rv">
      <p class="lw-book-line">Karibu. <em>Your room is waiting.</em></p>
      <div class="lw-book-act"><a class="hb-btn hb-btn--gold" href="book.html">Book your stay</a><a class="lw-wa" href="{WA}" target="_blank" rel="noopener">or ask us on WhatsApp</a></div>
    </div>
  </div>
</section>

<section class="lw-hl" aria-labelledby="hl-h">
  <div class="bx-wrap"><h2 class="sr-only" id="hl-h">Why guests choose The Breez</h2><div class="bx-fgrid">{hl}</div></div>
</section>

<section class="lw-loc" aria-labelledby="loc-h">
  <div class="wrap lw-loc-grid">
    <div class="lw-loc-text">
      <span class="ed-kick rv">Find us</span>
      <h2 class="lw-loc-title rv" id="loc-h">We are <em>here.</em></h2>
      <p class="lw-loc-line rv">A little place to find your own moment.</p>
      <p class="lw-loc-intro rv">On the Kisumu&ndash;Busia Road in Busia, western Kenya, close to the Uganda border, with secure parking on site.</p>
      <dl class="lw-loc-dl rv">
        <div><dt>Address</dt><dd>{ADDRESS}</dd></div>
        <div><dt>Call</dt><dd><a href="{TEL}">{PHONE_DISPLAY}</a></dd></div>
        <div><dt>Email</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd></div>
      </dl>
      <div class="lw-loc-links rv"><a class="ed-mood-link" href="{MAP_PLACE}" target="_blank" rel="noopener">Open in Google Maps<span aria-hidden="true"> &rarr;</span></a><a class="ed-mood-link" href="contact.html">Directions and contact<span aria-hidden="true"> &rarr;</span></a></div>
    </div>
    <div class="lw-map rv" data-map>
      <iframe src="{MAP_EMBED}" title="Map showing The Breez Hotel on the Kisumu&ndash;Busia Road, Busia" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
      <div class="lw-pin" aria-hidden="true"><span class="lw-pin-label">The Breez Hotel</span><svg viewBox="0 0 24 32"><path d="M12 0C5.4 0 0 5.2 0 11.7 0 20.4 12 32 12 32s12-11.6 12-20.3C24 5.2 18.6 0 12 0z"/><circle cx="12" cy="11.5" r="4.3"/></svg></div>
      <span class="lw-map-coord" aria-hidden="true">0.4565&deg; N &middot; 34.1216&deg; E</span>
    </div>
  </div>
</section>'''

def editorial():
    karibu = f'''<section class="ed-karibu" aria-labelledby="kar-h">
  <div class="ed-k-panel">
    <span class="ed-kick rv">Karibu</span>
    <h2 class="ed-k-title rv" id="kar-h">The art of <em>welcome</em></h2>
    <p class="ed-k-essay rv">In Swahili, <em>karibu</em> is a welcome and an invitation to come closer. At The Breez it begins at the gate and carries on along the shaded veranda, past the fountain and the gazebos, to a cool drink by the pool and a quiet room at the end of the day.</p>
    <a class="ed-discover rv" href="about.html" aria-label="Discover the hotel and its grounds">Discover</a>
    <a class="ed-k-ph rv" href="about.html" tabindex="-1" aria-hidden="true">{ph('entrance-lobby', '', '(max-width:760px) 86vw, 36vw')}</a>
  </div>
  <div class="ed-k-side" aria-hidden="true">
    <div class="ed-xp" data-arrive>
      <div class="ed-arch"><div class="ed-arch-in">
        <figure class="ed-xp-a">{img('building-palms-pool-court', '(max-width:760px) 86vw, 560px', eager=True).replace('fetchpriority="high"', 'loading="eager" fetchpriority="low"')}</figure>
        <figure class="ed-xp-b">{img('entrance-lobby', '(max-width:760px) 86vw, 560px', eager=True).replace('fetchpriority="high"', 'loading="eager" fetchpriority="low"')}</figure>
      </div></div>
      <div class="ed-xp-prog"><span class="on">The exterior</span><i><b></b></i><span>The arrival</span></div>
    </div>
  </div>
</section>'''
    def mood(n, lab, h, k, t, u, lt, lay):
        main, support, cls = MOOD_LAYOUT[n]
        sup = f'<figure class="ed-c-sup" data-reveal="up">{img(support, "(max-width:760px) 46vw, 18vw")}</figure>' if support else ''
        return (f'<article class="ed-c ed-c--{cls}">'
                f'<a class="ed-c-media" href="{u}" tabindex="-1" aria-hidden="true"><figure class="ed-c-main" data-reveal="up">{img(main, "(max-width:760px) 100vw, 46vw")}</figure>{sup}</a>'
                f'<div class="ed-c-text rv"><span class="ed-c-no">{n}</span><span class="ed-kick">{lab}</span><h3>{h}</h3><p>{t}</p>'
                f'<a class="ed-mood-link" href="{u}">{lt}<span aria-hidden="true"> &rarr;</span></a></div></article>')
    cards = ''.join(mood(*m) for m in MOODS)
    words = ''.join(('<span class="on">' if i == 0 else '<span>') + w + '</span>' for i, w in enumerate(PLACE_WORDS))
    story_sec = f'''<section class="ed-moods2" aria-labelledby="moods-h">
  <div class="wrap">
    <div class="ed-spine" aria-hidden="true"><span>experience</span></div>
    <header class="ed-intro">
      <span class="ed-kick rv">The Breez experience</span>
      <h2 class="ed-intro-h rv" id="moods-h"><span class="ed-i1">The many moods</span> <span class="ed-i2">of The Breez</span></h2>
      <p class="ed-intro-sub rv">The best time to visit? <em>Every hour of the day.</em></p>
    </header>
    <div class="ed-coll">{cards}</div>
    <div class="ed-taste">
      <figure class="ed-taste-ph" data-reveal="up">{img('pool-garden-view', '(max-width:760px) 100vw, 58vw')}</figure>
      <div class="ed-taste-text rv">
        <p class="ed-taste-lead">The Breez is a place to</p>
        <p class="ed-taste-word" data-words aria-label="The Breez is a place to unwind, gather, celebrate, discover and belong">{words}</p>
        <p class="ed-taste-copy">Some places are made for slowing down. At The Breez, discover the pleasure of peaceful mornings, refreshing afternoons, meaningful gatherings and evenings worth remembering.</p>
      </div>
    </div>
  </div>
</section>'''
    return karibu + '\n' + story_sec

EXP_TILES = ['building-palms-pool-court', 'room-four-poster-window', 'pool-aerial', 'room-grey-bedding', 'bar-counter-stools', 'buffet-samosa-chapati',
             'poolside-meal-juice', 'room-desk-armchair', 'restaurant-interior-blue', 'courtyard-fountain-gazebos', 'stew-plate', 'bed-detail']
EXP_SPANS = [5, 3, 4, 3, 4, 5, 4, 5, 3, 5, 3, 4]          # 12-column rhythm of the reference mosaic
EXP_ICONS = {
    'pin': '<path d="M12 2a7 7 0 0 0-7 7c0 5.3 7 13 7 13s7-7.7 7-13a7 7 0 0 0-7-7zm0 9.6A2.6 2.6 0 1 1 12 6.4a2.6 2.6 0 0 1 0 5.2z"/>',
    'wave': '<path d="M1 7.6c2 0 3-1.6 5.5-1.6S9.8 7.6 12 7.6 15 6 17.5 6 21 7.6 23 7.6v3c-2 0-3-1.6-5.5-1.6S14.2 10.6 12 10.6 9 9 6.5 9 3 10.6 1 10.6zm0 6.4c2 0 3-1.6 5.5-1.6s3.3 1.6 5.5 1.6 3-1.6 5.5-1.6S21 14 23 14v3c-2 0-3-1.6-5.5-1.6S14.2 17 12 17s-3-1.6-5.5-1.6S3 17 1 17z"/>',
    'cup': '<path d="M3 8h14v5a6 6 0 0 1-6 6H9a6 6 0 0 1-6-6zm14 1.5h1.5a3 3 0 0 1 0 6H17v-2.4h1.5a.6.6 0 0 0 0-1.2H17zM2 20.5h17V23H2zM7 1.5c1 1 1 2.2 0 3.3s-1 2 0 2.7H5c-1-1-1-2 0-3s1-2 0-3zm4.5 0c1 1 1 2.2 0 3.3s-1 2 0 2.7h-2c-1-1-1-2 0-3s1-2 0-3z"/>',
    'star': '<path d="M12 1.8l3.1 6.6 7.2.9-5.3 5 1.4 7.1L12 17.9l-6.4 3.5L7 14.3l-5.3-5 7.2-.9z"/>',
}
EXP_FEATS = [
    ('pin', 'On the Kisumu–Busia Road', 'A garden hotel in Busia, easy to reach by road and with secure parking for your stay.', 'contact.html', 'Find us'),
    ('wave', 'Pools and gardens', 'A swimming pool and a children&rsquo;s pool, with umbrellas, loungers and green lawns all around.', 'pools.html', 'See the pools'),
    ('cup', 'Food and drink', 'Kenyan and international dishes, a full bar, and meals with fresh juice served at the pool.', 'dining.html', 'Eat and drink'),
    ('star', 'Meetings and celebrations', 'Halls, lawns and marquees for conferences, weddings, ruracio and birthdays.', 'meetings.html', 'Plan an event'),
]

def experiences():
    tiles = ''.join(
        f'<a class="bx-t" style="--s:{EXP_SPANS[i]}" href="{IMAGES[k]["rel"]}-1600.webp" data-alt="{html.escape(ALT[k], quote=True)}" data-caption="{html.escape(ALT[k], quote=True)}">'
        f'{img(k, "(max-width:760px) 50vw, 40vw")}</a>' for i, k in enumerate(EXP_TILES))
    feats = ''.join(
        f'<div class="bx-f rv"><svg class="bx-i" viewBox="0 0 24 24" aria-hidden="true">{EXP_ICONS[ic]}</svg>'
        f'<div><h3>{h}</h3><p>{t} <a href="{u}">{lt}</a></p></div></div>' for ic, h, t, u, lt in EXP_FEATS)
    return f'''<section class="bx" aria-labelledby="bx-h">
  <h2 class="sr-only" id="bx-h">Your stay at The Breez</h2>
  <div class="bx-band"><div class="bx-wrap bx-grid" data-lightbox>{tiles}</div></div>
</section>'''

def home():
    stay = f'''<section class="sec" aria-labelledby="stay-h">
  <div class="wrap">
    {head('01 · Stay', '<span id="stay-h">Rooms that open onto the garden and the pool</span>', '<p class="lead">Four room categories, from a single for the solo traveller to a King room for two. Every stay includes Wi-Fi, housekeeping and secure parking.</p>')}
    <div class="stay-spread">
      <a class="stay-card sc1 rv" href="rooms.html#double">{ph('room-four-poster-window', 'ph--zoom', '(max-width:760px) 100vw, 40vw')}<span class="meta">Double · King</span><h3>Four-poster calm</h3><p>Rooms with a four-poster bed, desk and en-suite bathroom.</p></a>
      <a class="stay-card sc2 rv" href="rooms.html#deluxe">{ph('room-grey-bedding', 'ph--zoom', '(max-width:760px) 100vw, 50vw')}<span class="meta">Deluxe</span><h3>Room to settle in</h3><p>Air conditioning and a balcony, as listed for this category.</p></a>
      <div class="stay-cta rv"><p class="lead">Rates depend on dates and room. Send a request and reception replies with availability.</p><div class="btn-row"><a class="btn btn--solid" href="rooms.html">See the rooms</a><a class="btn" href="book.html">Request a booking</a></div></div>
      <a class="stay-card sc3 rv" href="rooms.html#single">{ph('bed-detail', 'ph--zoom', '30vw')}<span class="meta">Standard Single</span><h3>For one</h3></a>
    </div>
  </div>
</section>'''
    return f'''<section class="hx-home hb" aria-label="Welcome to The Breez Hotel">
  {hx('pool-loungers', 'hb-ph', '100vw', eager=True)}
  <div class="hb-in">
    <span class="hb-k hb-a1">Karibu &middot; Busia, Kenya</span>
    <h1 class="hb-title hb-a2">The Breez</h1>
    <p class="hb-line hb-a3">Where the garden meets <em>the pool</em>.</p>
    <div class="hb-actions hb-a4"><a class="hb-btn hb-btn--gold" href="book.html">Book your stay</a><a class="hb-btn hb-btn--light" href="about.html">Explore the hotel</a></div>
  </div>
  <dl class="hb-facts hb-a5">
    <div><dt>2</dt><dd>swimming pools, one for children</dd></div>
    <div><dt>4</dt><dd>room categories</dd></div>
    <div><dt>Busia</dt><dd>on the Kisumu&ndash;Busia Road</dd></div>
  </dl>
</section>
<div class="mq" data-marquee aria-label="Karibu. Stay, swim, dine, meet and celebrate at The Breez."><div class="mq-track"><span>Karibu</span><span>Stay</span><span>Swim</span><span>Dine</span><span>Meet</span><span>Celebrate</span></div></div>

{editorial()}

{experiences()}

<section class="sec sec--stone" aria-labelledby="meet-h">
  <div class="wrap">
    {head('04 · Meetings &amp; events', '<span id="meet-h">Halls for the workshop, lawns for the wedding</span>')}
    <div class="meet-grid rv">
      <div class="mg-text"><p class="lead">Meeting halls come with a projector and screen, Wi-Fi and a full set-up. Packages are flexible and include food and drinks. The lawns and marquees host weddings, ruracio, birthdays and garden parties.</p><div class="btn-row"><a class="btn btn--solid" href="meetings.html">Plan an event</a></div></div>
      {ph('hall-classroom-setup', 'mg-img tall', '(max-width:760px) 100vw, 25vw')}
      {ph('tent-wedding-setup', 'mg-img tall', '(max-width:760px) 100vw, 25vw')}
      <div class="mg-list"><span class="label">Meetings</span><b>Conferences</b><b>Training</b><b>Workshops</b></div>
      <div class="mg-list"><span class="label">Celebrations</span><b>Weddings</b><b>Ruracio</b><b>Garden parties</b></div>
    </div>
  </div>
</section>

<section class="sec" aria-labelledby="gal-h">
  <div class="wrap">
    {head('05 · Gallery', '<span id="gal-h">Around the hotel</span>', '<a class="link" href="gallery.html">All photographs</a>')}
    <div class="mosaic" data-lightbox data-stagger data-drift>
      {''.join(f'<a class="{c}" href="{IMAGES[k]["rel"]}-1600.webp" data-alt="{html.escape(ALT[k], quote=True)}" data-caption="{html.escape(ALT[k], quote=True)}">{img(k, "(max-width:760px) 50vw, 33vw")}</a>' for c, k in [('m1', 'courtyard-fountain-gazebos'), ('m2', 'pool-aerial'), ('m3', 'gazebo-cypress'), ('m4', 'lounge-rattan-sofas'), ('m5', 'tower-and-terrace'), ('m6', 'bar-counter-stools')])}
    </div>
  </div>
</section>

{lower_home()}'''

def about():
    exp = f"""<section class="ab-sec" aria-labelledby="exp-h">
  <div class="wrap">
    <div class="ab-exp-head rv"><div><span class="ab-n">03</span><h2 class="ab-h" id="exp-h" style="margin-top:12px" data-split="words">The Breez experience</h2></div><p class="hx-sub">Four reasons guests come through the gate.</p></div>
    <div class="ab-exp">
      <a class="ab-x ab-x1 rv" href="rooms.html">{hx('room-four-poster-window', '', '(max-width:760px) 100vw, 58vw')}<div class="ab-x-cap"><div><h3>Accommodation</h3><p>Single, Double, Deluxe and King rooms.</p></div><span class="go">Rooms</span></div></a>
      <a class="ab-x ab-x2 rv" href="pools.html">{hx('pool-umbrellas-above', 'fx-ripple', '(max-width:760px) 50vw, 40vw')}<div class="ab-x-cap"><div><h3>Swimming pools</h3><p>A main pool and a kids’ pool.</p></div><span class="go">Pools</span></div></a>
      <a class="ab-x ab-x3 rv" href="dining.html">{hx('poolside-meal-juice', 'mask-circle', '(max-width:760px) 50vw, 33vw')}<div class="ab-x-cap"><div><h3>Dining</h3><p>Restaurant, bar and poolside.</p></div><span class="go">Dining</span></div></a>
      <a class="ab-x ab-x4 rv" href="meetings.html">{hx('hall-classroom-setup', '', '100vw')}<div class="ab-x4-over"><span class="ab-n">Meetings &amp; events</span><h3>Halls, lawns and marquees</h3><p>Projector, Wi-Fi and catering packages.</p><span class="link" style="justify-self:start">Plan an event</span></div></a>
    </div>
  </div>
</section>"""
    props = [('ab-p1', 'cottage-courtyard-swing', 'Courtyard and gazebos', '(max-width:760px) 100vw, 58vw'),
             ('ab-p2', 'fountain-lawn-swing', 'The fountain lawn', '(max-width:760px) 50vw, 40vw'),
             ('ab-p3', 'garden-gazebo-roof', 'A garden gazebo', '(max-width:760px) 50vw, 40vw'),
             ('ab-p4', 'pool-garden-view', 'Pool, garden and the guest wing', '100vw')]
    pr = ''.join(f'<a class="{c}{" mask-arch" if c == "ab-p1" else ""}" data-reveal="{"arch" if c == "ab-p1" else ("circle" if c == "ab-p3" else "up")}" href="{IMAGES[k]["rel"]}-1600.webp" data-alt="{html.escape(ALT[k], quote=True)}" data-caption="{t}"><figure style="margin:0;height:100%">{img(k, sz)}<figcaption><b>0{i+1}</b>{t}</figcaption></figure></a>' for i, (c, k, t, sz) in enumerate(props))
    return f"""<section class="ab-hero" aria-labelledby="ab-h1">
  <div class="ab-hero-rail" aria-hidden="true"><span class="hx-v">01 · About The Breez</span></div>
  <div class="ab-hero-text">
    <div>{crumb('About')}<span class="hx-k hx-a1">Busia, Kenya</span>
      <h1 id="ab-h1" data-split="words">More than <em>a place</em> to stay.</h1></div>
    <div class="ab-hero-foot hx-a3"><p class="hx-sub">Discover a welcoming hotel in Busia, where relaxation, hospitality and memorable moments come together.</p><a class="hx-scroll" href="#story"><i></i>Scroll</a></div>
  </div>
  <div class="ab-hero-media">
    {hx('tower-and-terrace-tall', 'main', '(max-width:760px) 100vw, 50vw', eager=True)}
    {hx('gate-sign-crop', 'tag mask-arch', '230px')}
    <span class="loc">Kisumu–Busia Road</span>
  </div>
</section>

<section class="ab-sec" id="story" aria-labelledby="story-h">
  <div class="wrap ab-story">
    <span class="hx-v" aria-hidden="true">Our story</span>
    {hx('main-building-facade', 'ab-story-main', '(max-width:760px) 100vw, 55vw', extra=' data-reveal="left"')}
    {hx('sign-the-breeze-hotel-karibu', 'ab-story-sign', '(max-width:760px) 60vw, 25vw', extra=' data-reveal="scale" data-parallax="0.05"')}
    <div class="ab-story-text rv"><span class="ab-n">02 · Our story</span><h2 class="ab-h" id="story-h" data-split="words">Karibu, carved at the gate.</h2>
      <p>The Breez Hotel stands on the Kisumu–Busia Road, close to the Kenya–Uganda border. Behind the carved Karibu sign are guest rooms, a main pool and a kids’ pool, a restaurant and bar, meeting halls, and gardens with gazebos and a fountain. Guests come to stay the night, to swim, to meet and to celebrate.</p></div>
  </div>
</section>

{exp}

<section class="ab-sec sec--stone" aria-labelledby="prop-h">
  <div class="wrap">
    <div class="ab-prop-head rv"><div><span class="ab-n">04</span><h2 class="ab-h" id="prop-h" style="margin-top:12px">The property in pictures</h2></div><a class="link" href="gallery.html">All photographs</a></div>
    <div class="ab-prop" data-lightbox data-drift>{pr}</div>
  </div>
</section>

<section class="ab-sec" aria-labelledby="people-h">
  <div class="wrap ab-people">
    {hx('staff-team-welcome', '', '(max-width:760px) 100vw, 640px', extra=' data-reveal="blur"')}
    <div class="ab-people-text rv"><span class="ab-n">05 · The people behind the welcome</span><h2 class="ab-h ab-caps" id="people-h" style="font-size:clamp(2rem,1.2rem + 2.6vw,3.6rem)" data-split="lines">Hospitality with a personal touch.</h2><p>The Breez team welcomes guests at reception, looks after the rooms, serves the restaurant and bar, and sets up meetings and celebrations.</p><a class="link" href="contact.html">Talk to reception</a></div>
  </div>
</section>

<section class="ab-close" aria-labelledby="close-h">
  {hx('building-palms-pool-court', '', '100vw')}
  <div class="ab-close-in">
    <div><span class="hx-k hx-k--light">06 · Busia, Kenya</span><h2 id="close-h" data-split="lines">Your next stay starts here.</h2></div>
    <div class="rv"><ul><li><span>Call</span><a href="{TEL}">{PHONE_DISPLAY}</a></li><li><span>Email</span><a href="mailto:{EMAIL}">{EMAIL}</a></li><li><span>Find us</span><span style="color:#fff">Kisumu–Busia Road</span></li></ul>
      <div class="hx-actions"><a class="btn btn--wa" href="{WA}" target="_blank" rel="noopener">{ICON['wa']} WhatsApp us</a><a class="btn btn--book" href="book.html">Booking enquiry</a></div></div>
  </div>
</section>"""

RX = [('room-four-poster-2', 'Four-poster bed and mosquito net', 'organic'), ('room-grey-bedding', 'Made up for the night', 'double'), ('room-desk-armchair', 'A desk and an armchair', 'diagonal'),
      ('bed-detail', 'Fresh linen', 'arch'), ('bathroom-shower', 'The en-suite shower', 'circle'), ('room-fridge-tv', 'Fridge and TV in the room', 'full')]

def rooms():
    order = [('single', 'single-room', 'bed-detail', False), ('double', 'room-four-poster-window', 'bathroom-shower', True),
             ('deluxe', 'room-grey-bedding', 'room-vanity', False), ('king', 'room-four-poster-2', 'room-desk-armchair', True)]
    blurbs = {'single': 'A single bed, a desk and an en-suite bathroom. For the solo business traveller.',
              'double': 'A double bed for two, often with a four-poster frame and mosquito net.',
              'deluxe': 'A double room with air conditioning listed and a city view.',
              'king': 'The largest bed in the hotel, with a pool view as listed.'}
    sp = ''
    for i, (k, main, det, flip) in enumerate(order):
        d = ROOMS[k]
        dl = ''.join(f'<div><dt>{f}</dt><dd>{v}</dd></div>' for f, v in d.items() if f not in ('Room',))
        sp += f'''<article class="spread{' flip' if flip else ''}" id="{k}">
  <div class="spread-img">{ph(main, 'main', '(max-width:1100px) 100vw, 66vw', extra=' data-reveal="left"')}{ph(det, 'detail', '25vw')}</div>
  <div class="spec rv"><span class="label">0{i+1} · Room</span><h2>{d['Room']}</h2><p>{blurbs[k]}</p><dl>{dl}</dl><a class="btn btn--solid" href="book.html?room={d['Room'].replace(' ', '+')}">Request this room</a></div>
</article>'''
    return f'''<section class="hx-rooms" aria-labelledby="rooms-h1">
  <div class="hx-rooms-text">
    <div>{crumb('Stay')}<span class="hx-k hx-a1">02 · Rooms &amp; stays</span><h1 class="hx-title" id="rooms-h1" data-split="words">Rest in the garden.</h1><p class="hx-sub hx-a3" style="margin-top:18px">Four room categories, as listed on Booking.com. Reception confirms your room and rate.</p></div>
    <div class="hx-a4"><ul class="hx-index" data-index>{''.join(f'<li><a href="#{k}" data-swap="{IMAGES[m]["rel"]}" data-alt="{html.escape(ALT[m], quote=True)}"{" class=on" if k == "double" else ""}><b>{ROOMS[k]["Room"]}</b><span>{ROOMS[k]["Bed"]} · {ROOMS[k]["Sleeps"]}</span></a></li>' for k, m in [('single', 'single-room'), ('double', 'room-four-poster-window'), ('deluxe', 'room-grey-bedding'), ('king', 'room-four-poster-2')])}</ul><div class="hx-actions" style="margin-top:22px"><a class="btn btn--solid" href="book.html">Request a booking</a></div></div>
  </div>
  <div class="hx-rooms-media">
    {hx('room-four-poster-window', 'main mask-arch', '(max-width:760px) 100vw, 60vw', eager=True)}
    {hx('bed-detail', 'detail', '280px', extra=' data-parallax="0.06"')}
    <span class="note">Photographs of rooms at The Breez</span>
  </div>
</section>
<section class="xp" data-expand aria-labelledby="xp-h">
  <div class="xp-sticky"><span class="xp-word" aria-hidden="true">Rest.</span>
    <div class="xp-frame">{img('room-four-poster-2', '100vw')}</div>
    <div class="xp-title"><span class="hx-k hx-k--light">Rooms at The Breez</span><h2 id="xp-h">Unwind, by the garden.</h2></div>
  </div>
</section>
<section class="sec rx-sec" aria-labelledby="sl-h">
  <div class="wrap">
    <div class="rx-head"><div><span class="label">Inside the rooms</span><h2 class="h-l" id="sl-h" data-split="words">A closer look</h2></div><p>Photographs of rooms at The Breez. Furniture and layout vary by category.</p></div>
    <div class="rx" data-rx data-style="organic" tabindex="0" aria-roledescription="carousel" aria-label="Room photographs">
      <div class="rx-stage"><div class="rx-deco" aria-hidden="true"><span class="rx-offset"></span><span class="rx-circle"></span><span class="rx-corner rx-c1"></span><span class="rx-corner rx-c2"></span>
        <svg class="rx-trace" viewBox="0 0 100 100" preserveAspectRatio="none"><rect x=".4" y=".4" width="99.2" height="99.2" pathLength="100"/></svg></div>
      <div class="rx-frame">{''.join(f'<figure class="rx-slide{" on" if i == 0 else ""}" data-style="{st}" data-cap="{html.escape(c, quote=True)}">{img(k, "(max-width:760px) 100vw, 1200px", eager=(i == 0))}</figure>' for i, (k, c, st) in enumerate(RX))}<span class="rx-cut rx-k1" aria-hidden="true"></span><span class="rx-cut rx-k2" aria-hidden="true"></span></div></div>
      <div class="rx-meta"><span class="label">Room details</span><p class="rx-cap" aria-live="polite"><b data-count>01</b><span>{RX[0][1]}</span></p>
        <div class="rx-ctl"><button type="button" data-prev aria-label="Previous photo"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 5l-7 7 7 7"/></svg></button><span class="rx-num"><b data-num>01</b> / {len(RX):02d}<i class="rx-prog"><i data-prog></i></i></span><button type="button" data-play aria-pressed="false" aria-label="Pause slideshow"><svg viewBox="0 0 24 24" aria-hidden="true" class="i-pause"><path d="M9 6v12M15 6v12"/></svg><svg viewBox="0 0 24 24" aria-hidden="true" class="i-play"><path d="M8 5l11 7-11 7z"/></svg></button><button type="button" data-next aria-label="Next photo"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 5l7 7-7 7"/></svg></button></div>
      </div>
    </div>
  </div>
</section>
<section class="sec" style="padding-top:0"><div class="wrap">{sp}</div></section>
<section class="sec" aria-labelledby="every-h">
  <div class="wrap">
    {head('Every stay', '<span id="every-h">Included with every room</span>')}
    <div class="every rv"><div><b>Free Wi-Fi</b><span class="small">Across the hotel</span></div><div><b>Secure parking</b><span class="small">On site</span></div><div><b>Housekeeping</b><span class="small">Daily</span></div><div><b>Pool access</b><span class="small">Main and kids’ pools</span></div></div>
    <div class="closing" style="margin-top:clamp(48px,7vw,96px)"><h2 class="h-l">Ready to choose your dates?</h2><div class="btn-row" style="justify-content:center"><a class="btn btn--book" href="book.html">Request a booking</a><a class="btn btn--wa" href="{WA}" target="_blank" rel="noopener">{ICON['wa']} Ask on WhatsApp</a></div></div>
  </div>
</section>'''

def pools():
    steps = [('pool-umbrellas-above', 'The main pool', 'Lanes of clear water in a court of palms, ringed by umbrellas and loungers.'),
             ('kids-pool-umbrellas', 'The kids’ pool', 'A shallow pool alongside the main one, so families can swim together.'),
             ('poolside-tables', 'Poolside tables', 'Lunch, fresh juice and drinks from the bar, served at the water’s edge.'),
             ('pool-loungers', 'Afternoons on the deck', 'Loungers and shade for long afternoons in the sun.')]
    media = ''.join(f'{ph(k, "on" if i == 0 else "", "50vw", alt=ALT[k])}' for i, (k, a, b) in enumerate(steps))
    st = ''.join(f'<div class="ss-step" data-step="{i}">{ph(k, "ph-m", "100vw")}<span class="label label--light">0{i+1}</span><h2>{a}</h2><p class="lead" style="color:#DCEFF3">{b}</p></div>' for i, (k, a, b) in enumerate(steps))
    PD = [('pool-garden-view', 'A moment by the water'), ('pool-lanes-2', 'Your place in the sun'), ('pool-terrace-kids-pool', 'Slow afternoons, beautiful views'), ('pool-lawn-view', 'Water, lawn and open sky'), ('kids-pool-building', 'Room for the little ones'), ('pool-fence-umbrellas', 'Shade by the pool')]
    return f'''<section class="hx-pools" aria-labelledby="pools-h1">
  {hx('pool-loungers', '', '100vw', eager=True)}
  <div class="hx-pools-in">{crumb('Pools')}<span class="hx-k hx-k--light hx-a1">03 · Water &amp; shade</span><h1 class="hx-title" id="pools-h1"><span data-split="chars" style="display:block">Pools</span><em class="italic hx-a3">in the palm court</em></h1><p class="hx-sub hx-a3">A main pool and a kids’ pool, with loungers, umbrellas and food from the bar.</p></div>
  <div class="hx-rail glow-cool" aria-label="More pool photographs">{hx('pool-lanes', 'mask-pill fx-ripple', '(max-width:760px) 33vw, 220px')}{hx('kids-pool-umbrellas', 'mask-pill fx-ripple', '(max-width:760px) 33vw, 220px')}{hx('pool-top-down', 'mask-pill fx-ripple', '(max-width:760px) 33vw, 220px')}</div>
</section>
<section class="sec sec--pool" aria-label="The pools">
  <div class="wrap sticky-story"><div class="ss-media">{media}</div><div class="ss-steps">{st}</div></div>
</section>
<section class="sec pd" aria-labelledby="col-h">
  <div class="wrap">
    <div class="pd-wrap" data-pooldays tabindex="0" aria-roledescription="carousel" aria-label="Pool days photographs">
      <p class="pd-word" aria-hidden="true"><span>Pool</span><span>days</span></p>
      <div class="pd-stage" data-lightbox>{''.join(f'<a class="pd-card{" pd-p" if IMAGES[k]["h"] > IMAGES[k]["w"] else ""}" href="{IMAGES[k]["rel"]}-1600.webp" data-alt="{html.escape(ALT.get(k, c), quote=True)}" data-caption="{html.escape(ALT.get(k, c), quote=True)}" data-cap="{html.escape(c, quote=True)}"><span class="pd-mat">{img(k, "(max-width:760px) 74vw, 500px", eager=(i == 0))}</span></a>' for i, (k, c) in enumerate(PD))}</div>
      <div class="pd-meta"><span class="hx-k">Pool days</span><h2 id="col-h">Water, shade and a juice</h2><p class="pd-cap" aria-live="polite">{PD[0][1]}</p></div>
      <div class="pd-ctl" role="group" aria-label="Slideshow controls">
        <button type="button" data-prev aria-label="Previous photo"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 5l-7 7 7 7" fill="none" stroke="currentColor" stroke-width="1.6"/></svg></button>
        <span class="pd-count"><b data-count>01</b> / {len(PD):02d}<i class="pd-prog"><i data-prog></i></i></span>
        <button type="button" data-pause aria-pressed="false" aria-label="Pause slideshow"><svg viewBox="0 0 24 24" aria-hidden="true" class="i-pause"><path d="M9 6v12M15 6v12" stroke="currentColor" stroke-width="1.8"/></svg><svg viewBox="0 0 24 24" aria-hidden="true" class="i-play"><path d="M8 5l11 7-11 7z" fill="currentColor"/></svg></button>
        <button type="button" data-full aria-label="View photo full screen"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5" fill="none" stroke="currentColor" stroke-width="1.6"/></svg></button>
        <button type="button" data-next aria-label="Next photo"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 5l7 7-7 7" fill="none" stroke="currentColor" stroke-width="1.6"/></svg></button>
      </div>
    </div>
  </div>
</section>
<section class="sec sec--pool" aria-labelledby="pi-h">
  <div class="wrap">
    {head('Good to know', '<span id="pi-h">Before you swim</span>', '', light=True)}
    <div class="pl-info rv">
      <div><span class="label label--light">Who</span><b>Hotel guests</b><p>Day visits and events: ask reception.</p></div>
      <div><span class="label label--light">Families</span><b>Kids’ pool</b><p>Children should be supervised by an adult.</p></div>
      <div><span class="label label--light">Hours</span><b>Ask reception</b><p>Pool hours and any charges are confirmed by the hotel.</p></div>
    </div>
    <div class="btn-row" style="margin-top:40px"><a class="btn btn--book" href="book.html">Request a booking</a><a class="btn btn--light" href="{WA}" target="_blank" rel="noopener">Ask about day visits</a></div>
  </div>
</section>'''

def dining():
    strip = [('food-lunch-by-water', 'Lunch by the water'), ('food-salmon-plate', 'Colour on the plate'), ('drink-mocktails-sunlit', 'Mocktails'),
             ('food-burger-fries', 'Light bites'), ('food-breakfast-bowls', 'Morning'), ('food-table-set', 'Evening'), ('food-overhead-plate', 'Plated')]
    sf = ''.join(f'<figure>{hx(k, "", "(max-width:760px) 80vw, 30vw")}<figcaption>{c}</figcaption></figure>' for k, c in strip)
    return f'''<section class="hx-dining" aria-labelledby="dine-h1">
  <div class="hx-dining-text">
    <div>{crumb('Dining')}<span class="hx-k hx-a1">04 · Taste &amp; atmosphere</span><h1 class="hx-title" id="dine-h1" data-split="words">Restaurant <em class="italic">&amp;</em> bar</h1><p class="hx-sub hx-a3" style="margin-top:20px">Kenyan and international food, drinks from the bar and tables by the pool.</p></div>
    <div class="hx-a4"><div class="hx-dining-meta"><div><b>Breakfast</b>With stays, as listed</div><div><b>Poolside</b>Meals and juice</div><div><b>Events</b>Catering</div></div><a class="btn btn--light" style="margin-top:24px" href="{WA}" target="_blank" rel="noopener">Reserve a table on WhatsApp</a></div>
  </div>
  <div class="hx-dining-media">
    {hx('food-fries-golden', 'main', '(max-width:760px) 100vw, 58vw', eager=True)}
    <div class="detail glow-warm"><figure class="hx-ph mask-circle ring" style="margin:0">{img('drink-mango-juice', '250px')}</figure></div>
  </div>
</section>
<section class="sec" aria-labelledby="plates-h">
  <div class="wrap">{head('Dining mood', '<span id="plates-h" data-split="words">At the table</span>', '<div class="strip-ctl" data-strip="plates"><button type="button" data-dir="prev" aria-label="Previous photos">←</button><button type="button" data-dir="next" aria-label="Next photos">→</button></div>')}</div>
  <div class="strip" id="plates" tabindex="0" aria-label="Food photographs, scroll sideways" data-stagger>{sf}</div>
  <div class="wrap"><p class="note" style="margin-top:18px">These photographs set the mood and are not dishes from the Breez menu. Ask reception for today’s menu.</p></div>
</section>
<section class="sec sec--stone" aria-labelledby="real-h">
  <div class="wrap real-food" data-layered>
    {hx('poolside-meal-juice', 'rf-a ly-a', '(max-width:760px) 100vw, 55vw')}
    {hx('buffet-decor', 'rf-b ly-b mask-arch', '(max-width:760px) 45vw, 22vw')}
    {hx('buffet-samosa-chapati', 'rf-c ly-c', '(max-width:760px) 45vw, 22vw')}
    <div class="rf-t ly-t"><span class="hx-k">Photographed at The Breez</span><h2 class="ab-h" id="real-h">Poolside lunch and event dining.</h2><p class="hx-sub">The hotel’s own photographs of food served by the pool and at events.</p></div>
  </div>
</section>
<section class="sec sec--stone" aria-labelledby="menu-h">
  <div class="wrap">
    <div class="menu-card rv">
      <h2 id="menu-h">Through the day</h2><span class="label">The Breez Hotel · Busia</span>
      <div class="mc"><span class="label">Morning</span><h3>Breakfast</h3><p>Included with room stays, as listed on Booking.com.</p></div>
      <div class="mc"><span class="label">Restaurant</span><h3>Lunch &amp; dinner</h3><p>Kenyan and international dishes. Ask for today’s menu.</p></div>
      <div class="mc"><span class="label">Poolside</span><h3>By the water</h3><p>Meals, fresh juice and drinks served at the pool.</p></div>
      <div class="mc"><span class="label">Events</span><h3>Catering</h3><p>Buffets and packages for meetings, weddings and parties.</p></div>
      <p class="note">Menus, prices and opening hours come from the kitchen. Ask reception or send a WhatsApp.</p>
    </div>
  </div>
</section>
<section class="bar-split" aria-labelledby="bar-h">
  {ph('bar-shelves', '', '(max-width:760px) 100vw, 50vw')}
  <div class="rv"><span class="label label--light">The bar</span><h2 id="bar-h">Cold drinks, warm evenings</h2><p>A full bar with stools at the counter, ice buckets for the table and drinks carried out to the pool.</p><a class="btn btn--light" href="{WA}" target="_blank" rel="noopener">Reserve a table on WhatsApp</a></div>
</section>
<section class="sec" aria-labelledby="share-h">
  <div class="wrap find">
    <div class="rv"><span class="label">Gather</span><h2 class="h-l" id="share-h" style="margin:.3em 0 .5em">A table for everyone</h2><p class="lead">From a quick lunch to a long family dinner or an event buffet for hundreds, tell us what you are planning.</p><div class="btn-row" style="margin-top:20px"><a class="btn btn--solid" href="meetings.html#enquire">Plan a group meal</a></div></div>
    {ph('group-dinner', 'ratio-4-3 rv', '(max-width:760px) 100vw, 50vw')}
  </div>
</section>'''

def event_form():
    return f'''<div class="form-panel" id="enquire">
  <div><span class="label">Enquiry</span><h2>Tell us about your event</h2><p class="muted" style="margin-top:8px">Reception replies with availability, set-up options and a quote.</p></div>
  <form class="form-grid" data-form="event" novalidate>
    <label class="field" data-label="Event type">Event type<select name="event" required><option value="">Choose…</option><option>Conference / meeting</option><option>Training / workshop</option><option>Wedding</option><option>Ruracio</option><option>Birthday</option><option>Garden party</option><option>Other</option></select></label>
    <label class="field" data-label="Preferred date">Preferred date<input type="date" name="date" required></label>
    <label class="field" data-label="Expected guests">Expected guests<input type="number" name="guests" min="1" inputmode="numeric" required></label>
    <label class="field" data-label="Preferred arrangement">Preferred arrangement<select name="setup"><option value="">Not sure</option><option>Classroom</option><option>Theatre</option><option>Banquet</option><option>Marquee on the lawn</option></select></label>
    <label class="field" data-label="Name">Your name<input type="text" name="name" autocomplete="name" required></label>
    <label class="field" data-label="Phone">Phone<input type="tel" name="phone" autocomplete="tel" required></label>
    <label class="field full" data-label="Email">Email<input type="email" name="email" autocomplete="email"></label>
    <label class="field full" data-label="Additional requirements">Additional requirements<textarea name="details" placeholder="Timings, food, equipment, accommodation…"></textarea></label>
    <fieldset class="field full" style="border:0;padding:0;margin:0"><legend>Send by</legend><div class="btn-row" style="text-transform:none;letter-spacing:0;font-weight:400"><label><input type="radio" name="channel" value="whatsapp" checked> WhatsApp</label><label><input type="radio" name="channel" value="email"> Email</label></div></fieldset>
    <div class="full"><button class="btn btn--book" type="submit">Send enquiry</button></div>
    <p class="note full">An enquiry is not a confirmed booking. Reception confirms availability, set-up and price by reply.</p>
  </form>
  {status_box()}
</div>'''

def status_box():
    return f'''<div class="form-status" role="status" aria-live="polite"><b>Your request is ready to send</b><p>Reference <strong data-ref></strong>. We opened WhatsApp with your details. Press send there. If it did not open, use one of these:</p><div class="btn-row"><a class="btn btn--wa" data-wa href="{WA}" target="_blank" rel="noopener">{ICON['wa']} Send on WhatsApp</a><a class="btn" data-mail href="mailto:{EMAIL}">{ICON['mail']} Send by email</a></div><p class="small">Nothing is booked yet. Reception confirms availability and rate by reply.</p></div>'''

def meetings():
    def pic(k, cls='', sizes='(max-width:760px) 100vw, 50vw', eager=False, extra=''):
        return f'<figure class="mt2-ph {cls}"{extra}>{img(k, sizes, eager)}</figure>'
    SPACES = ['hall-red-skirting', 'hall-screen', 'hall-projector']
    CONF = [('classroom', 'Classroom', 'hall-classroom-setup', 'Tables in rows facing the front, for training sessions and workshops where everyone takes notes.'),
            ('theatre', 'Theatre', 'hall-theatre-grey', 'Rows of chairs facing the screen, for talks, presentations and launches.'),
            ('banquet', 'Banquet', 'hall-banquet-red', 'Round tables dressed in your colours, for dinners, receptions and celebrations.')]
    OUT = [('courtyard-fountain-gazebos', 'The courtyard fountain'), ('courtyard-lawn-fountain', 'An open lawn for your guests'), ('fountain-lawn-swing', 'Afternoons by the fountain'),
           ('garden-gazebo-roof', 'Thatched gazebos in the garden'), ('gazebo-cypress', 'Gazebos framed by cypress'), ('walkway-cottages', 'Garden paths between the cottages')]
    FAC = [('Meeting halls', 'Indoor halls dressed for your event', 'M4 20V9l8-5 8 5v11M9 20v-6h6v6'),
           ('Projector & screen', 'Set up in the halls', 'M3 5h18v11H3zM12 16v4M8 20h8'),
           ('Wi-Fi', 'For every delegate', 'M2 9a15 15 0 0 1 20 0M5 12.5a10 10 0 0 1 14 0M8.5 16a5 5 0 0 1 7 0M12 19.5h.01'),
           ('Room set-ups', 'Classroom, theatre or banquet', 'M4 6h16M4 12h16M4 18h16'),
           ('Food & drink', 'Tea breaks, lunch, buffets and the bar, in flexible packages', 'M7 3v8M5 3v5a2 2 0 0 0 4 0V3M7 11v10M17 3c-2 0-3 2-3 5s1 4 3 4v9'),
           ('Outdoor spaces', 'Lawns, gazebos, marquees and the courtyard fountain', 'M3 20h18M6 20V10l6-6 6 6v10'),
           ('Rooms for delegates', 'Single, Double, Deluxe and King, subject to availability', 'M3 18V8M3 14h18v4M21 18v-6a3 3 0 0 0-3-3h-7v5'),
           ('Capacity', 'Depends on the hall and set-up, confirmed on enquiry', 'M12 3a9 9 0 1 0 0 18 9 9 0 0 0 0-18zM12 7v5l3 3')]
    for k in SPACES + [c[2] for c in CONF] + [o[0] for o in OUT]: USED.add(k)
    spaces = ''.join(f'<figure class="mt2-sp{" on" if i == 0 else ""}">{img(k, "(max-width:760px) 100vw, 60vw")}</figure>' for i, k in enumerate(SPACES))
    conf_imgs = ''.join(f'<figure class="mt2-cf-img{" on" if i == 0 else ""}" data-conf="{key}">{img(k, "(max-width:760px) 100vw, 55vw")}</figure>' for i, (key, t, k, d) in enumerate(CONF))
    conf_tabs = ''.join(f'<button type="button" role="tab" aria-selected="{"true" if i == 0 else "false"}" data-conf="{key}" data-title="{t}" data-desc="{html.escape(d, quote=True)}"><span>0{i+1}</span>{t}</button>' for i, (key, t, k, d) in enumerate(CONF))
    out_slides = ''.join(f'<figure class="mt2-os{" on" if i == 0 else ""}" data-cap="{html.escape(c, quote=True)}">{img(k, "100vw")}</figure>' for i, (k, c) in enumerate(OUT))
    fac = ''.join(f'<li><span class="mt2-fn">0{i+1}</span><svg viewBox="0 0 24 24" aria-hidden="true"><path d="{ic}"/></svg><b>{t}</b><span class="mt2-fd">{d}</span></li>' for i, (t, d, ic) in enumerate(FAC))
    return f'''<section class="mt2-hero" aria-labelledby="meet-h1" data-spotlight>
  <div class="mt2-hero-in wrap">
    <div class="mt2-hero-text">
      {crumb('Meetings &amp; events')}
      <span class="hx-k hx-a1">05 · Meetings &amp; events</span>
      <h1 id="meet-h1" data-split="lines">Make room for something remarkable.</h1>
      <p class="mt2-lead hx-a3">From important business gatherings to unforgettable celebrations, discover a setting for occasions worth remembering.</p>
      <div class="hx-actions hx-a4"><a class="btn btn--solid" data-magnetic href="#enquire">Send an enquiry</a><a class="btn" data-magnetic href="{TEL}">Call {PHONE_DISPLAY}</a></div>
    </div>
    <div class="mt2-hero-art">
      <svg class="mt2-ring" viewBox="0 0 200 200" aria-hidden="true"><circle cx="100" cy="100" r="98"/></svg>
      {pic('hall-banquet-gold', 'mt2-circle', '(max-width:760px) 90vw, 46vw', eager=True)}
      {pic('tent-red-white', 'mt2-float', '(max-width:760px) 40vw, 18vw', extra=' data-parallax="0.06"')}
      <div class="mt2-glass hx-a4"><span class="hx-k">Halls · Lawns · Marquees</span><p>Projector and screen, Wi-Fi, full set-up and catering packages.</p></div>
    </div>
  </div>
</section>

<div class="mq mt2-mq" data-marquee aria-label="Conferences, training, workshops, weddings, ruracio, birthdays and garden parties."><div class="mq-track"><span>Conferences</span><span>Weddings</span><span>Training</span><span>Ruracio</span><span>Workshops</span><span>Garden parties</span></div></div>

<section class="sec mt2-intro" aria-labelledby="intro-h">
  <div class="wrap mt2-intro-grid">
    <span class="hx-v" aria-hidden="true">The setting</span>
    <div class="mt2-intro-head"><span class="label">01 · The setting</span><h2 id="intro-h" data-split="words">Business by day. <em>Celebrations</em> by evening.</h2></div>
    {pic('courtyard-fountain-tent', 'mt2-intro-img', '(max-width:760px) 100vw, 40vw', extra=' data-reveal="arch"')}
    <p class="mt2-intro-p rv">The Breez Hotel hosts conferences, training and workshops in its meeting halls, and weddings, ruracio, birthdays and garden parties on its lawns and under marquees. Events come with a full set-up, Wi-Fi and food and drink packages arranged with the team.</p>
  </div>
</section>

<section class="sec sec--stone mt2-spaces" aria-labelledby="spaces-h">
  <div class="wrap mt2-spaces-grid">
    <div class="mt2-sp-main" data-spaces tabindex="0" aria-roledescription="carousel" aria-label="Meeting hall photographs">{spaces}
      <div class="mt2-sp-nav"><button type="button" data-prev aria-label="Previous photo">←</button><span data-count>01 / 0{len(SPACES)}</span><button type="button" data-next aria-label="Next photo">→</button></div>
    </div>
    {pic('hall-banquet-2', 'mt2-sp-a', '(max-width:760px) 50vw, 22vw', extra=' data-reveal="up" data-parallax="0.05"')}
    {pic('hall-classroom-2', 'mt2-sp-b', '(max-width:760px) 50vw, 24vw', extra=' data-reveal="circle"')}
    <div class="mt2-panel rv"><span class="label">02 · Meetings &amp; conferences</span><h2 id="spaces-h">A setting for</h2>
      <ul><li>Conferences</li><li>Training</li><li>Workshops</li><li>Business gatherings</li></ul>
      <p class="small">Projector and screen, Wi-Fi and a full set-up in every hall.</p></div>
  </div>
</section>

<section class="sec mt2-conf" aria-labelledby="conf-h">
  <div class="wrap">
    <div class="mt2-conf-grid" data-config>
      <div class="mt2-cf-media">{conf_imgs}</div>
      <div class="mt2-cf-text">
        <span class="label">03 · Room configurations</span>
        <div class="mt2-cf-tabs" role="tablist" aria-label="Choose a layout">{conf_tabs}</div>
        <h2 id="conf-h" class="mt2-cf-title" aria-live="polite">{CONF[0][1]}</h2>
        <p class="mt2-cf-desc">{CONF[0][3]}</p>
        <p class="small">Capacity depends on the hall and is confirmed on enquiry.</p>
        <a class="btn btn--book" data-magnetic href="#enquire" data-setup="{CONF[0][1]}">Enquire about this layout</a>
      </div>
    </div>
  </div>
</section>

<section class="mt2-wed" aria-labelledby="wed-h">
  <div class="wrap mt2-wed-grid">
    {pic('tent-wedding-setup', 'mt2-wed-main', '(max-width:760px) 100vw, 46vw', extra=' data-reveal="up"')}
    <div class="mt2-wed-text"><span class="label label--light">04 · Weddings</span><h2 id="wed-h" data-split="chars">Weddings</h2>
      <p>Marquees on the lawn, tables dressed in your colours and a buffet line under canvas. Tell us your date and the team will help plan the day.</p>
      <a class="btn btn--light" data-magnetic href="#enquire">Plan a wedding</a></div>
    {pic('garden-party-setup', 'mt2-wed-side mask-arch', '(max-width:760px) 60vw, 24vw', extra=' data-reveal="arch" data-parallax="0.07"')}
    <p class="mt2-wed-cap">Under canvas, on the lawn</p>
  </div>
</section>

<section class="sec mt2-rur" aria-labelledby="rur-h">
  <svg width="0" height="0" aria-hidden="true" focusable="false"><defs><clipPath id="mt2-blob" clipPathUnits="objectBoundingBox"><path d="M.09.32C.14.1.36.02.56.04c.22.02.4.16.42.38.02.2-.06.38-.22.48C.6 1 .38 1 .22.9.06.8.03.52.09.32Z"><animate attributeName="d" dur="14s" repeatCount="indefinite" values="M.09.32C.14.1.36.02.56.04c.22.02.4.16.42.38.02.2-.06.38-.22.48C.6 1 .38 1 .22.9.06.8.03.52.09.32Z;M.06.4C.1.16.32.0.54.03c.24.03.42.2.42.42 0 .22-.12.38-.28.46C.52.99.3.98.17.86.04.74.02.6.06.4Z;M.09.32C.14.1.36.02.56.04c.22.02.4.16.42.38.02.2-.06.38-.22.48C.6 1 .38 1 .22.9.06.8.03.52.09.32Z"/></path></clipPath></defs></svg>
  <div class="wrap mt2-rur-grid">
    <div class="mt2-rur-art">
      <svg class="mt2-rur-line" viewBox="0 0 400 300" aria-hidden="true"><path d="M10 250C90 120 180 300 260 160S380 40 390 20"/></svg>
      {pic('marquee-lawn', 'mt2-blob', '(max-width:760px) 100vw, 50vw')}
      {pic('cottages-lawn', 'mt2-rur-c mask-circle', '(max-width:760px) 40vw, 16vw', extra=' data-reveal="circle"')}
    </div>
    <div class="mt2-rur-text"><span class="label">05 · Ruracio &amp; ceremonies</span><h2 id="rur-h" data-split="words">Ruracio and family ceremonies</h2>
      <p>Family ceremonies on the open lawn, with marquees, seating and catering arranged around your guests.</p></div>
  </div>
</section>

<section class="mt2-out" aria-labelledby="out-h">
  <div class="mt2-os-stage" data-outdoor tabindex="0" aria-roledescription="carousel" aria-label="Garden and outdoor event photographs">{out_slides}
    <div class="mt2-os-shade"></div>
    <div class="wrap mt2-os-text"><span class="hx-k hx-k--light">06 · Outdoor events</span><h2 id="out-h">Birthdays and garden parties</h2><p class="mt2-os-cap" aria-live="polite">{OUT[0][1]}</p>
      <div class="mt2-os-ctl"><button type="button" data-prev aria-label="Previous photo">←</button><span class="mt2-os-count"><b data-count>01</b> / 0{len(OUT)}<i class="mt2-os-prog"><i data-prog></i></i></span><button type="button" data-play aria-pressed="false" aria-label="Pause slideshow">❚❚</button><button type="button" data-next aria-label="Next photo">→</button></div>
    </div>
  </div>
</section>

<section class="sec mt2-cat" aria-labelledby="cat-h">
  <div class="wrap mt2-cat-grid">
    {pic('tent-buffet-line', 'mt2-cat-a', '(max-width:760px) 100vw, 40vw', extra=' data-reveal="up"')}
    {pic('buffet-samosa-chapati', 'mt2-cat-b', '(max-width:760px) 50vw, 24vw', extra=' data-reveal="left"')}
    {pic('buffet-decor', 'mt2-cat-c', '(max-width:760px) 50vw, 24vw', extra=' data-reveal="up"')}
    <div class="mt2-cat-text rv"><span class="label">07 · Catering</span><h2 id="cat-h">From tea break to buffet</h2><p>Tea breaks, lunch and buffets for meetings, and buffets and packages for weddings and parties. Menus are agreed with the kitchen.</p><p class="small">Photographed at The Breez.</p></div>
  </div>
</section>

<section class="sec sec--stone mt2-fac" aria-labelledby="fac-h">
  <div class="wrap mt2-fac-grid">
    <div class="mt2-fac-head"><span class="label">08 · Facilities</span><h2 id="fac-h" data-split="words">What every event can use</h2></div>
    <ol class="mt2-fac-list" data-stagger>{fac}</ol>
  </div>
</section>

<section class="mt2-enq" aria-labelledby="enq-h">
  <div class="mt2-enq-left">
    {pic('garden-party-balloons', 'mt2-enq-bg', '(max-width:760px) 100vw, 45vw')}
    <div class="mt2-enq-copy"><span class="hx-k hx-k--light">09 · Enquiry</span><h2 id="enq-h" data-split="lines">Plan your event with us.</h2>
      <p>Share your date, guest numbers and layout. Reception replies with availability, set-up options and a quote.</p>
      <ul class="mt2-enq-contact"><li><span>Call</span><a href="{TEL}">{PHONE_DISPLAY}</a></li><li><span>WhatsApp</span><a href="{WA}" target="_blank" rel="noopener">{PHONE_DISPLAY}</a></li><li><span>Email</span><a href="mailto:{EMAIL}">{EMAIL}</a></li></ul></div>
  </div>
  <div class="mt2-enq-right">{event_form()}</div>
</section>

<section class="mt2-close" aria-labelledby="close-h">
  {pic('hall-gold-cloths', 'mt2-close-bg', '100vw', extra=' data-reveal="circle"')}
  <div class="mt2-close-frame" aria-hidden="true"></div>
  <div class="wrap mt2-close-in"><span class="hx-k hx-k--light">10 · The Breez</span><h2 id="close-h" data-split="lines">Let’s make it memorable.</h2>
    <p>Tell us what you are planning. We would love to help bring your occasion together.</p>
    <div class="hx-actions"><a class="btn btn--book" data-magnetic href="#enquire">Send an enquiry</a><a class="btn btn--wa" data-magnetic href="{WA}" target="_blank" rel="noopener">{ICON['wa']} WhatsApp</a></div></div>
</section>'''


def gallery():
    cats = ['exterior', 'gardens', 'pools', 'rooms', 'interiors', 'dining', 'conference', 'events', 'people']
    items = [k for c in cats for k, m in IMAGES.items() if m['cat'] == c]
    pattern = ['w', '', 't', '', 's', 's', '', 'w', 't', '', '', 's']
    out = ''
    for i, k in enumerate(items):
        m = IMAGES[k]; USED.add(k)
        cls = pattern[i % len(pattern)]
        a = html.escape(ALT.get(k, ''), quote=True)
        out += f'<a{(" class=" + chr(34) + cls + chr(34)) if cls else ""} href="{m["rel"]}-1600.webp" data-cat="{m["cat"]}" data-alt="{a}" data-caption="{a}"><img src="{m["rel"]}-800.webp" width="{m["w"]}" height="{m["h"]}" alt="{a}" loading="lazy" decoding="async"><figcaption>{a}</figcaption></a>'
    chips = '<button type="button" data-filter="all" aria-pressed="true">All</button>' + ''.join(f'<button type="button" data-filter="{c}" aria-pressed="false">{CAT_LABEL[c]}</button>' for c in cats if any(IMAGES[k]['cat'] == c for k in items))
    LQ = [('pool-garden-view', 'The pool court and the guest wing'), ('hall-banquet-gold', 'A banquet hall dressed in gold'), ('room-grey-bedding', 'A room made up for the night'),
          ('marquee-lawn', 'A marquee on the lawn'), ('pool-lawn-view', 'Water, lawn and shade'), ('main-building-facade', 'The main building')]
    FILM = [('entrance-gate', 'Arrive at the gate', '1/1'), ('entrance-lobby', 'Step inside', '3/4'), ('room-four-poster-2', 'Settle in', '4/3'),
            ('pool-lanes-2', 'Swim', '4/5'), ('poolside-tables', 'Lunch by the pool', '4/3'), ('gazebo-steps', 'The garden', '3/2'), ('courtyard-fountain-tent', 'Evening on the lawn', '3/2')]
    for k, *_ in LQ + FILM: USED.add(k)
    lq_imgs = ''.join(f'<img src="{IMAGES[k]["rel"]}-1600.webp" srcset="{IMAGES[k]["rel"]}-800.webp 800w, {IMAGES[k]["rel"]}-1600.webp 1600w" sizes="(max-width:760px) 100vw, 1320px" alt="{html.escape(ALT[k], quote=True)}" width="{IMAGES[k]["w"]}" height="{IMAGES[k]["h"]}" decoding="async"{"" if i == 0 else " loading=lazy"}>' for i, (k, c) in enumerate(LQ))
    lq_caps = ''.join(f'<p data-cap{" class=on" if i == 0 else ""}>{c}</p>' for i, (k, c) in enumerate(LQ))
    film = ''.join(f'<figure>{hx(k, "", "(max-width:760px) 70vw, 30vw", extra=f" style=--ar:{ar}")}<figcaption><b>0{i+1}</b>{c}</figcaption></figure>' for i, (k, c, ar) in enumerate(FILM))
    return f'''<section class="hx-gal" aria-labelledby="gal-h1">
  <div class="wrap hx-gal-grid" data-lightbox data-drift>
    <div class="hx-gal-title">{crumb('Gallery')}<span class="hx-k hx-a1">06 · A visual journey</span><h1 class="hx-title" id="gal-h1" data-split="chars">Gallery</h1><p class="hx-sub hx-a3">{len(items)} photographs of the hotel, its grounds, rooms, food and events.</p></div>
    {''.join(f'<a class="{c}" href="{IMAGES[k]["rel"]}-1600.webp" data-alt="{html.escape(ALT[k], quote=True)}" data-caption="{html.escape(ALT[k], quote=True)}">{img(k, sz, eager=True)}<b>{n}</b></a>' for c, k, n, sz in [('g1 mask-arch', 'tower-and-terrace-tall', '01', '(max-width:760px) 66vw, 33vw'), ('g2', 'garden-gazebo-roof', '02', '25vw'), ('g3', 'kids-pool-building', '03', '25vw'), ('g4 mask-circle', 'fountain-seating', '04', '(max-width:760px) 33vw, 25vw'), ('g5', 'pool-umbrellas-above', '05', '(max-width:760px) 33vw, 50vw')])}
  </div>
</section>

<section class="lq" data-liquid tabindex="0" aria-roledescription="carousel" aria-labelledby="lq-h">
  <div class="wrap">
    <div class="lq-head"><div><span class="hx-k hx-k--light">Cinematic sequence</span><h2 id="lq-h" data-split="words">Six moments at The Breez</h2></div><p style="max-width:34ch;color:#CFC6B6;margin:0">Use the arrows, swipe, or the arrow keys.</p></div>
    <div class="lq-stage">{lq_imgs}</div>
    <div class="lq-foot"><div class="lq-caps" aria-live="polite">{lq_caps}</div><div class="sl-ctl"><span class="sl-count" data-count>01 / 06</span><button type="button" data-prev aria-label="Previous moment">←</button><button type="button" data-next aria-label="Next moment">→</button></div></div>
    <div class="lq-prog"><i data-bar></i></div>
  </div>
</section>

<section class="film" aria-labelledby="film-h">
  <div class="wrap">{head('Film strip', '<span id="film-h" data-split="words">A day, frame by frame</span>', '<p>Drag or scroll sideways.</p>')}</div>
  <div class="film-strip" data-filmstrip tabindex="0" aria-label="A day at The Breez, scroll sideways">{film}</div>
</section>

<section class="gcol" aria-labelledby="col-h">
  <div class="wrap gcol-in">
    {hx('cottage-courtyard-swing', 'cg-a mask-arch', '(max-width:760px) 80vw, 50vw', extra=' data-reveal="arch"')}
    {hx('fountain-lawn-swing', 'cg-b mask-circle', '(max-width:760px) 50vw, 25vw', extra=' data-reveal="circle" data-parallax="0.06"')}
    {hx('walkway-cottages', 'cg-c', '(max-width:760px) 50vw, 33vw', extra=' data-reveal="up"')}
    <div class="cg-t"><span class="hx-k">The garden</span><h2 data-split="lines">Gazebos, cypress and a fountain.</h2><p class="hx-sub">Between the guest wings, a lawn for slow afternoons and garden parties.</p></div>
  </div>
</section>

<section class="sec" aria-labelledby="arc-h">
  <div class="wrap">
    <div class="archive-head"><div><span class="hx-k">The archive</span><h2 id="arc-h">Every photograph</h2></div><div class="chips" data-filters="grid" role="group" aria-label="Filter photographs">{chips}</div></div>
    <div class="gl-grid" id="grid" data-lightbox data-drift>{out}</div>
    <p class="note" style="margin-top:32px">All photographs on this page are of The Breez Hotel, shared by the hotel. Stock photographs used elsewhere on the site are credited on the <a href="credits.html">credits page</a>.</p>
  </div>
</section>'''

def contact():
    return f'''<section class="hx-contact" aria-labelledby="ct-h1">
  <div class="hx-contact-text">
    <div>{crumb('Contact')}<span class="hx-k hx-a1">07 · Your way to The Breez</span><h1 class="hx-title" id="ct-h1" data-split="words">Find us in Busia.</h1></div>
    <ul class="hx-loc" data-stagger>
      <li><span>Address</span><b>Kisumu–Busia Road, Busia, Kenya</b></li>
      <li><span>Call</span><b><a href="{TEL}">{PHONE_DISPLAY}</a></b></li>
      <li><span>WhatsApp</span><b><a href="{WA}" target="_blank" rel="noopener">{PHONE_DISPLAY}</a></b></li>
      <li><span>Email</span><b><a href="mailto:{EMAIL}">{EMAIL}</a></b></li>
    </ul>
    <div class="hx-actions hx-a4"><a class="btn btn--wa" href="{WA}" target="_blank" rel="noopener">{ICON['wa']} WhatsApp</a><a class="btn btn--solid" href="{TEL}">{ICON['phone']} Call</a><a class="btn" href="{MAP_LINK}" target="_blank" rel="noopener">Directions</a></div>
  </div>
  <div class="hx-contact-media">
    {hx('entrance-gate', 'main', '(max-width:760px) 100vw, 50vw', eager=True)}
    <div class="detail"><figure class="hx-ph mask-circle ring" style="margin:0;height:100%">{img('sign-the-breeze-hotel-karibu', '230px')}</figure></div>
    <span class="cap">The gate on the Kisumu–Busia Road</span>
  </div>
</section>
<section class="ct-map" aria-label="Map"><iframe src="{MAP_EMBED}" title="Map showing The Breez Hotel in Busia" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></section>
<section class="sec sec--stone" aria-labelledby="dir-h">
  <div class="wrap">
    {head('Getting here', '<span id="dir-h">Directions</span>', f'<a class="link" href="{MAP_LINK}" target="_blank" rel="noopener">Open in Google Maps</a>')}
    <div class="dirs rv">
      <div><h3>By road</h3><p>The hotel is on the Kisumu–Busia Road in Busia town. Look for the stone sign and gate.</p></div>
      <div><h3>Arriving</h3><p>Drive through the gate to secure parking. Reception is in the main building.</p></div>
      <div><h3>Need help?</h3><p>Send your location on WhatsApp and reception will guide you in.</p></div>
    </div>
  </div>
</section>
<section class="sec" aria-labelledby="msg-h">
  <div class="wrap" style="max-width:880px">
    <div class="form-panel">
      <div><span class="label">Message</span><h2 id="msg-h">Send us a message</h2></div>
      <form class="form-grid" data-form="contact" novalidate>
        <label class="field" data-label="Name">Your name<input type="text" name="name" autocomplete="name" required></label>
        <label class="field" data-label="Phone">Phone<input type="tel" name="phone" autocomplete="tel" required></label>
        <label class="field full" data-label="Email">Email<input type="email" name="email" autocomplete="email"></label>
        <label class="field full" data-label="Message">Message<textarea name="message" required></textarea></label>
        <fieldset class="field full" style="border:0;padding:0;margin:0"><legend>Send by</legend><div class="btn-row" style="text-transform:none;letter-spacing:0;font-weight:400"><label><input type="radio" name="channel" value="whatsapp" checked> WhatsApp</label><label><input type="radio" name="channel" value="email"> Email</label></div></fieldset>
        <div class="full"><button class="btn btn--solid" type="submit">Send message</button></div>
      </form>
      {status_box()}
    </div>
  </div>
</section>'''

def book():
    opts = ''.join(f'<option>{v["Room"]}</option>' for v in ROOMS.values())
    return f'''<section class="bk">
  <div class="bk-side">{ph('pool-terrace-kids-pool', '', '(max-width:1100px) 100vw, 45vw', eager=True)}<span class="hx-v" aria-hidden="true">Request · not a confirmed booking</span><div><span class="hx-k hx-k--light">08 · Book a stay</span><h1>Request your dates</h1><p>Send your request straight to reception. They reply with availability and the rate for your room.</p></div></div>
  <div class="bk-form">
    <ol class="steps"><li data-n="1">Your stay</li><li data-n="2">Your details</li><li data-n="3">Send</li></ol>
    <form class="form-grid" data-form="booking" novalidate>
      <label class="field" data-label="Check-in">Check-in<input type="date" name="checkin" required></label>
      <label class="field" data-label="Check-out">Check-out<input type="date" name="checkout" required></label>
      <label class="field" data-label="Guests">Guests<select name="guests"><option>1 adult</option><option selected>2 adults</option><option>3 adults</option><option>4+ adults</option></select></label>
      <label class="field" data-label="Children">Children<select name="children"><option>0</option><option>1</option><option>2</option><option>3+</option></select></label>
      <label class="field full" data-label="Room">Room<select name="room" required><option value="">Choose a room…</option>{opts}<option>Not sure — please advise</option></select></label>
      <div class="summary full" aria-live="polite"><div><span class="label">Arrive</span><b data-show="checkin">—</b></div><div><span class="label">Leave</span><b data-show="checkout">—</b></div><div><span class="label">Stay</span><b data-nights>—</b></div></div>
      <label class="field" data-label="Name">Full name<input type="text" name="name" autocomplete="name" required></label>
      <label class="field" data-label="Phone">Phone<input type="tel" name="phone" autocomplete="tel" required></label>
      <label class="field full" data-label="Email">Email<input type="email" name="email" autocomplete="email"></label>
      <label class="field full" data-label="Requests">Special requests<textarea name="requests" placeholder="Arrival time, extra bed, airport or bus pick-up…"></textarea></label>
      <fieldset class="field full" style="border:0;padding:0;margin:0"><legend>Send by</legend><div class="btn-row" style="text-transform:none;letter-spacing:0;font-weight:400"><label><input type="radio" name="channel" value="whatsapp" checked> WhatsApp (fastest)</label><label><input type="radio" name="channel" value="email"> Email</label></div></fieldset>
      <div class="full"><button class="btn btn--book btn--framed" type="submit">Send booking request</button></div>
      <p class="note full">This is a request, not a confirmed booking. Availability is not shown live online. Nothing is charged here. Reception confirms by reply.</p>
    </form>
    {status_box()}
  </div>
</section>'''

def credits():
    rows = ''.join(f'<tr><td>{ALT[k]}</td><td>{STOCK[k][0]}</td><td><a href="{LICENSES[STOCK[k][1]]}" target="_blank" rel="noopener">{STOCK[k][1]} License</a></td></tr>' for k in sorted(USED) if IMAGES[k]['stock'])
    return f'''<section class="page-hero"><div class="wrap" style="max-width:960px"><nav class="crumb" aria-label="Breadcrumb"><a href="index.html">Home</a><span>/</span><span>Credits</span></nav><h1 class="h-xl">Photo credits</h1><p class="lead" style="margin-top:16px">Photographs of the hotel, its rooms, pools, gardens, food, halls, events and team are by The Breez Hotel and used with permission.</p></div></section>
<section class="sec credits" style="padding-top:0"><div class="wrap" style="max-width:960px"><h2 class="h-m" style="margin-bottom:16px">Stock photography</h2><p class="muted">These photographs are from Unsplash. They are not of The Breez Hotel, and the people in them are not hotel guests. Each is credited where it appears.</p><table><thead><tr><th>Photo</th><th>Photographer</th><th>Licence</th></tr></thead><tbody>{rows}</tbody></table><p class="small" style="margin-top:24px">Typefaces: Cormorant Garamond and Karla (SIL Open Font License), served by Google Fonts. Map © Google.</p></div></section>'''

def notfound():
    return f'''<section class="sec"><div class="wrap closing"><span class="label">404</span><h1 class="h-xl">This page has wandered off.</h1><p class="lead">The page you were looking for is not here. Try the home page or ask us on WhatsApp.</p><div class="btn-row" style="justify-content:center"><a class="btn btn--solid" href="index.html">Home</a><a class="btn btn--wa" href="{WA}" target="_blank" rel="noopener">WhatsApp</a></div></div></section>'''

# ---------------------------------------------------------------------------- assets
def og_image():
    src = ROOT / 'assets/images/breez/exterior/building-palms-pool-court-1600.webp'
    im = ImageOps.fit(Image.open(src).convert('RGB'), (1200, 630), centering=(.5, .45))
    ov = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    for y in range(630): d.line([(0, y), (1200, y)], fill=(20, 16, 12, int(max(0, (y - 230)) / 400 * 190)))
    im = Image.alpha_composite(im.convert('RGBA'), ov)
    d = ImageDraw.Draw(im)
    def font(names, size):
        for n in names:
            try: return ImageFont.truetype(n, size)
            except OSError: pass
        return ImageFont.load_default()
    serif = font(['/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'], 104)
    sans = font(['/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'], 24)
    d.rectangle([18, 18, 1181, 611], outline=(246, 241, 231, 200), width=2)
    d.text((64, 430), 'The Breez Hotel', font=serif, fill=(255, 255, 255))
    d.text((68, 556), 'POOLS · GARDENS · MEETINGS · BUSIA, KENYA', font=sans, fill=(233, 207, 164))
    im.convert('RGB').save(OUT / 'images/og-image.jpg', quality=84)
    # apple touch icon
    t = Image.new('RGB', (180, 180), (32, 57, 43)); dt = ImageDraw.Draw(t)
    dt.text((90, 92), 'B', font=font(['/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'], 120), fill=(246, 241, 231), anchor='mm')
    t.save(OUT / 'images/apple-touch-icon.png')

FAVICON = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="12" fill="#20392B"/><rect x="5" y="5" width="54" height="54" rx="8" fill="none" stroke="#B7772A" stroke-width="2"/><text x="32" y="45" text-anchor="middle" font-family="Georgia,serif" font-size="38" fill="#F6F1E7">B</text></svg>'

def main():
    if OUT.exists(): shutil.rmtree(OUT)
    (OUT / 'assets').mkdir(parents=True); (OUT / 'images').mkdir()
    scan()
    shutil.copy(ROOT / 'src/css/site.css', OUT / 'assets/site.css')
    shutil.copy(ROOT / 'src/js/site.js', OUT / 'assets/site.js')
    shutil.copy(ROOT / 'src/css/heroes.css', OUT / 'assets/heroes.css')
    shutil.copy(ROOT / 'src/css/motion.css', OUT / 'assets/motion.css')
    shutil.copy(ROOT / 'src/js/effects.js', OUT / 'assets/effects.js')
    (OUT / 'lab').mkdir(exist_ok=True); shutil.copy(ROOT / 'src/lab.html', OUT / 'lab/index.html')
    pages = [
        ('index', 'The Breez Hotel · Pools, gardens and rooms in Busia, Kenya', 'A garden hotel on the Kisumu–Busia Road in Busia, Kenya, with rooms, two pools, a restaurant and bar, meeting halls and lawns for weddings and events.', home),
        ('about', 'About the hotel', 'The Breez Hotel in Busia: the stone gate sign, the tower above the palms, gazebo gardens, a pool court and the team who run it.', about),
        ('rooms', 'Rooms & stays', 'Standard Single, Double, Deluxe and King rooms at The Breez Hotel, Busia. Compare listed features and request your dates.', rooms),
        ('pools', 'Pools', 'The main pool and kids’ pool at The Breez Hotel, Busia, with loungers, umbrellas and poolside food and drinks.', pools),
        ('dining', 'Restaurant & bar', 'Restaurant, bar and poolside dining at The Breez Hotel, Busia. Breakfast with stays, Kenyan and international food, and event catering.', dining),
        ('meetings', 'Meetings & events', 'Meeting halls with projector and Wi-Fi, and lawns and marquees for weddings, ruracio and garden parties at The Breez Hotel, Busia.', meetings),
        ('gallery', 'Gallery', 'Photographs of The Breez Hotel in Busia: the building, gardens, pools, rooms, food, halls and events.', gallery),
        ('contact', 'Contact & directions', 'Call or WhatsApp The Breez Hotel on 0707 461 665, email thebreezhotel@gmail.com, or find us on the Kisumu–Busia Road, Busia.', contact),
        ('book', 'Book a stay', 'Request a room at The Breez Hotel, Busia. Choose dates, guests and room, then send your request to reception by WhatsApp or email.', book),
    ]
    for slug, t, d, fn in pages: page(slug, t, d, fn())
    page('credits', 'Photo credits', 'Photo credits and licences for The Breez Hotel website.', credits())
    page('404', 'Page not found', 'This page could not be found.', notfound())
    # copy all images used anywhere
    for k in USED:
        m = IMAGES[k]
        for w in (800, 1600):
            s = ROOT / ('assets/' + m['rel'] + f'-{w}.webp'); dst = OUT / (m['rel'] + f'-{w}.webp')
            dst.parent.mkdir(parents=True, exist_ok=True); shutil.copy(s, dst)
    og_image()
    (OUT / 'favicon.svg').write_text(FAVICON)
    (OUT / '.nojekyll').write_text('')
    (OUT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\nDisallow: /lab/\nSitemap: {BASE_URL}sitemap.xml\n')
    urls = ''.join(f'<url><loc>{BASE_URL}{"" if s == "index" else s + ".html"}</loc><lastmod>{TODAY}</lastmod></url>' for s, *_ in pages + [('credits',)])
    (OUT / 'sitemap.xml').write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    hotel = sum(1 for k in USED if not IMAGES[k]['stock']); stock = sum(1 for k in USED if IMAGES[k]['stock'])
    print(f'Built {len(pages) + 2} pages · {hotel} hotel photos · {stock} stock photos · {hotel / (hotel + stock):.0%} hotel')

if __name__ == '__main__':
    main()
