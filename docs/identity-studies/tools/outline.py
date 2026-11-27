import sys, json
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.transformPen import TransformPen
FS='/tmp/idw/node_modules/@fontsource/'
def font(name, style='400-normal', sub='latin'):
    return TTFont(f'{FS}{name}/files/{name}-{sub}-{style}.woff2')
def word(f, text, track=0, kern=True):
    gs=f.getGlyphSet(); cmap=f.getBestCmap(); upm=f['head'].unitsPerEm
    names=[cmap[ord(c)] for c in text]
    # simple kerning via GPOS is complex; use hmtx + manual tracking
    pen=SVGPathPen(gs); bp=BoundsPen(gs); x=0; parts=[]
    for i,n in enumerate(names):
        tp=TransformPen(pen,(1,0,0,-1,x,0)); gs[n].draw(tp)
        tb=TransformPen(bp,(1,0,0,-1,x,0)); gs[n].draw(tb)
        x+=gs[n].width+track*upm/1000
    return pen.getCommands(), bp.bounds, upm
if __name__=='__main__':
    print(word(font(sys.argv[1]),sys.argv[2])[1])
