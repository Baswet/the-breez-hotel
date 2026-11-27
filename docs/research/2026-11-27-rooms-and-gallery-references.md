# Design references, 27 Nov 2026: Rooms details, Gallery hero, Gallery garden

Screenshots of the references are kept privately (not in the repository); they belong to their owners.

## Rooms: the rooms, one by one (`rooms.html`, section `.rd`)
- **Reference:** pin https://pin.it/6WhKxw3ax → pinterest.com/pin/957929783241001681, "Animated Website Design – Dev.UN Studio" by Pavlo Klymash (Behance). The supplied screen recording is the same video.
- **Seen in it:** large two-line uppercase headings, the second line indented ("OUR / SERVICES"); a small three-line label at the top left; per project a tall photograph, a title in capitals, a short paragraph, label/value pairs by a fine vertical rule ("location / KYIV", "terms of execution / 30 DAYS"), an outlined number ("01") inside a fine offset rectangle, and a mosaic of a wide and a tall photograph; alternate projects mirrored; plain vertical scrolling with photographs arriving as they enter.
- **Breez translation:** ivory and cream grounds (#F6F0E6, #F1E8DA), champagne lines (#D8C4A3), forest green accents (#344A3B), taupe labels (#9B8874), charcoal type (#302D28); Cormorant Garamond in place of the reference's grotesque; pairs are bed, sleeps and rate. Photographs open from the bottom (the site's existing `[data-reveal]`).
- **Prices:** none verified. Every room's rate reads "On request, confirmed by reception", taken from `ROOMS[...]['Rate']` in `tools/build_site.py`; entering a verified figure there shows it instead.

## Gallery: the opening (`gallery.html`, section `.gh`)
- **Reference:** pinterest.com/pin/1073897473637807308, "This gallery effect will get you more engagement", Fusion Sketch.
- **Seen in it:** one strong flat colour behind everything; a heading and a short line at the upper left, a pill button at the right; two rows of square-ish photographs drifting continuously in opposite directions, small even gaps.
- **Breez translation:** forest green (#344A3B) in place of the coral; ivory serif heading; ivory pill button; the hotel's own photographs; hover pauses a row; reduced motion turns the rows into still, sideways-scrollable strips.

## Gallery: the garden (`gallery.html`, section `.gc`), beneath "A day, frame by frame"
- **Reference:** pinterest.com/pin/845058317631376231, "Immersive 3D Website Design | Creative Art Gallery Web UI Inspiration", thedesigners.
- **Seen in it:** a dark stage; a centred serif heading and one small line; portrait frames standing on the inside of a curve, the outer ones turned towards the eye and larger; a slow continuous drift.
- **Breez translation:** warm charcoal (#2C2A25) instead of black; the hotel's own garden photographs; drift, drag/swipe and arrow keys; reduced motion stops the drift.

All photographs in these sections are the hotel's own; no external images were added.
