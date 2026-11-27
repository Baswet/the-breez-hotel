import sys; sys.path.insert(0,'/tmp/idw')
from outline import font
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
def setword(fontname, text, height=100, track=0, style='400-normal', kern=None):
    """outline `text`, cap/x scaled so the full ink height == height; returns (d, w, h)"""
    f=font(fontname, style); gs=f.getGlyphSet(); cm=f.getBestCmap()
    names=[cm[ord(c)] for c in text]; kern=kern or {}
    # pass 1 bounds
    def draw(pen):
        x=0
        for i,n in enumerate(names):
            gs[n].draw(TransformPen(pen,(1,0,0,-1,x,0))); x+=gs[n].width+track+kern.get(i,0)
    bp=BoundsPen(gs); draw(bp); x0,y0,x1,y1=bp.bounds; sc=height/(y1-y0)
    pen=SVGPathPen(gs)
    x=0
    for i,n in enumerate(names):
        gs[n].draw(TransformPen(pen,(sc,0,0,-sc,(x-x0)*sc,(-y0)*sc))); x+=gs[n].width+track+kern.get(i,0)
    return pen.getCommands(), (x1-x0)*sc, height

# SIGNATURE — Italianno 'Breez', tightened e-e-z, plus a drawn swash leaving the z's tail and running back under the word
def signature():
    d,w,h=setword('italianno','Breez',height=100,kern={1:-30,2:-40,3:-30})
    # swash: a tapered ribbon from lower right (z tail) sweeping left under the word, thinning to a hairline
    X=lambda f: f*w; Y=lambda f: f*h
    sw=(f'M{X(.975):.1f} {Y(.975):.1f} '
        f'C {X(.94):.1f} {Y(1.005):.1f}, {X(.70):.1f} {Y(1.04):.1f}, {X(.40):.1f} {Y(1.01):.1f} '
        f'C {X(.24):.1f} {Y(.99):.1f}, {X(.12):.1f} {Y(.98):.1f}, {X(.03):.1f} {Y(.995):.1f} '
        f'C {X(.12):.1f} {Y(.993):.1f}, {X(.25):.1f} {Y(1.005):.1f}, {X(.41):.1f} {Y(1.04):.1f} '
        f'C {X(.70):.1f} {Y(1.075):.1f}, {X(.93):.1f} {Y(1.045):.1f}, {X(.968):.1f} {Y(.99):.1f} Z')
    return d+sw, w, h*1.1
def caps(text='THE BREEZ', fontname='bodoni-moda', style='500-normal', height=40, track=220):
    return setword(fontname, text, height, track, style)
