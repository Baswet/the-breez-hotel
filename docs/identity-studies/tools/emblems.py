import sys; sys.path.insert(0,'/tmp/idw')
import math
from outline import font
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
G='#20392B'
from fontTools.pens.boundsPen import BoundsPen
def glyph(fontname, ch, x, y, height, style='400-normal'):
    """place glyph with its bounding box's bottom-left at (x,y) and given height"""
    f=font(fontname, style); gs=f.getGlyphSet(); n=f.getBestCmap()[ord(ch)]
    bp=BoundsPen(gs); gs[n].draw(bp); x0,y0,x1,y1=bp.bounds; sc=height/(y1-y0)
    pen=SVGPathPen(gs); gs[n].draw(TransformPen(pen,(sc,0,0,-sc,x-x0*sc,y+y0*sc))); return pen.getCommands()

# 1 THE PAVILION CREST — arch, the Breez gazebo roof (concave pyramid, flared eaves, finial), a breeze line through the open pavilion
pavilion = '''
<g fill="none" stroke="{c}"><path d="M34 226 V100 A66 66 0 0 1 166 100 V226" stroke-width="2.6"/><path d="M42 226 V101 A58 58 0 0 1 158 101 V226" stroke-width=".8"/></g>
<g fill="{c}">
 <path d="M99 50 h2 v8 h-2z"/><circle cx="100" cy="49" r="2.4"/>
 <path d="M100 58 L 124 76 C 125 77.5, 124.5 79, 122.5 79 L 77.5 79 C 75.5 79, 75 77.5, 76 76 Z"/>
 <path d="M81 81 h38 v13 h-38z M85 83.5 v8 h5 v-8z M93.5 83.5 v8 h5 v-8z M101.5 83.5 v8 h5 v-8z M110 83.5 v8 h5 v-8z" fill-rule="evenodd"/>
 <path d="M78 96 L 122 96 L 152 118 C 154 119.6, 153 121.6, 150.6 121.6 L 49.4 121.6 C 47 121.6, 46 119.6, 48 118 Z"/>
 <path d="M54 124 h92 v3.2 h-92z"/>
 <path d="M60 127 h4.2 v52 h-4.2z M80.5 127 h3.2 v52 h-3.2z M116.3 127 h3.2 v52 h-3.2z M135.8 127 h4.2 v52 h-4.2z"/>
 <path d="M50 179 h100 v3 h-100z M44 185 h112 v2.4 h-112z"/>
</g>
<path d="M44 206 C 68 194, 88 214, 112 205 C 132 198, 146 194, 158 199" fill="none" stroke="{c}" stroke-width="2.2" stroke-linecap="round"/>
<path d="M66 150 C 84 141, 104 159, 134 146" fill="none" stroke="{c}" stroke-width="1.5" stroke-linecap="round"/>'''

# 2 THE B MONOGRAM — Bodoni Moda B redrawn: a single breeze-curve cuts through both bowls as negative space, ending in a leaf tip
B = glyph('bodoni-moda','B', 52, 206, 172, '500-normal')
monogram = f'''
<defs><mask id="cut{{k}}"><rect width="200" height="240" fill="#fff"/><path d="M104 214 C 124 176, 140 142, 150 116 C 160 90, 170 64, 182 44" fill="none" stroke="#000" stroke-width="4.2" stroke-linecap="round"/></mask></defs>
<path d="{B}" fill="{{c}}" mask="url(#cut{{k}})"/>
<path d="M181 46 C 184 30, 192 20, 199 14 C 200 26, 194 38, 181 46 Z" fill="{{c}}"/>'''

# 3 THE PALM — a single frond drawn as calligraphic leaflets on a curved rib; reads as palm, wind and fan at once
def frond():
    parts=[]; ox,oy=100,170
    n=13
    for i in range(n):
        t=i/(n-1); ang=math.radians(-170+160*t)   # fan from left to right across the top
        L=92-30*abs(t-.42)**1.4*2
        bend=0.22   # every blade leans the same way: the breeze
        ux,uy=math.cos(ang),math.sin(ang); px,py=-uy,ux
        ex,ey=ox+ux*L+px*L*bend*.6, oy+uy*L+py*L*bend*.6
        mx,my=ox+ux*L*.55+px*L*bend*.5, oy+uy*L*.55+py*L*bend*.5
        w=5.6-1.8*abs(t-.5)
        s0x,s0y=ox+ux*14,oy+uy*14
        parts.append(f'<path d="M{s0x+px*1.2:.1f} {s0y+py*1.2:.1f} Q{mx+px*w:.1f} {my+py*w:.1f} {ex:.1f} {ey:.1f} Q{mx-px*w*.35:.1f} {my-py*w*.35:.1f} {s0x-px*1.2:.1f} {s0y-py*1.2:.1f} Z" fill="{{c}}"/>')
    parts.append(f'<circle cx="{ox}" cy="{oy}" r="6.5" fill="{{c}}"/>')
    parts.append(f'<path d="M{ox-2.2} {oy+4} C {ox-4} {oy+30}, {ox+2} {oy+50}, {ox+10} {oy+62} L {ox+13} {oy+61} C {ox+7} {oy+48}, {ox+2} {oy+30}, {ox+2.2} {oy+4} Z" fill="{{c}}"/>')
    return ''.join(parts)
palm = frond()
EMBLEMS={'pavilion':pavilion,'monogram':monogram,'palm':palm}
_k=[0]
def svg(key, c=G, vb='0 0 200 240', style=''):
    _k[0]+=1
    body=EMBLEMS[key].replace('{k}',str(_k[0])).replace('{c}',c).replace('{{c}}',c)
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" {style}>{body}</svg>'
