import sys, base64, io; sys.path.insert(0,'/tmp/idw')
from PIL import Image
from emblems import svg as emb
from marks import signature, caps, setword
IMG='/home/claude/the-breez-hotel/site/images/breez/'
FONTCSS=open('/tmp/idw/fonts.css').read()
def ph(path, w=900, q=72):
    im=Image.open(IMG+path+'-1600.webp').convert('RGB'); im.thumbnail((w,w)); b=io.BytesIO(); im.save(b,'JPEG',quality=q,optimize=True)
    return 'data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode()
P={k:ph(v) for k,v in {
 'gazebo':'gardens/gazebo-steps','tower':'exterior/tower-and-terrace-tall','lanes':'pools/pool-lanes-2','court':'exterior/building-palms-pool-court',
 'lobby':'interiors/entrance-lobby','pooltop':'pools/pool-top-down','veranda':'interiors/veranda-corridor','cypress':'gardens/gazebo-cypress','fountain':'gardens/courtyard-fountain-gazebos'}.items()}
sd,sw,sh=signature()
def sig(c, style='', stroke=1.3):
    return f'<svg viewBox="-6 -6 {sw+12:.0f} {sh+12:.0f}" {style} role="img" aria-label="Breez"><path d="{sd}" fill="{c}" stroke="{c}" stroke-width="{stroke}" stroke-linejoin="round"/></svg>'
bd,bw,bh=caps('THE BREEZ','bodoni-moda','500-normal',40,230)
def bod(c, style=''): return f'<svg viewBox="0 -2 {bw:.0f} {bh+4:.0f}" {style} role="img" aria-label="The Breez"><path d="{bd}" fill="{c}"/></svg>'
bd2,bw2,bh2=caps('BREEZ','bodoni-moda','500-normal',40,300)
def bod2(c, style=''): return f'<svg viewBox="0 -2 {bw2:.0f} {bh2+4:.0f}" {style}><path d="{bd2}" fill="{c}"/></svg>'
it,iw,ih=caps('BREEZ','italiana','400-normal',100,330)
def ital(c, style=''): return f'<svg viewBox="0 -2 {iw:.0f} {ih+4:.0f}" {style} role="img" aria-label="Breez"><path d="{it}" fill="{c}"/></svg>'
sub = lambda txt, c, ls='.42em', fs='10px': f'<span style="font:600 {fs}/1 Karla,sans-serif;letter-spacing:{ls};text-transform:uppercase;color:{c}">{txt}</span>'

CSS='''
'''+FONTCSS+'''
*{box-sizing:border-box}body{margin:0;background:#EDE6D9;color:#1E1A16;font:15px/1.6 Karla,system-ui,sans-serif}
.page{max-width:1320px;margin:0 auto;padding:56px 40px 120px}
h1{font:300 clamp(2.6rem,5vw,4.6rem)/1 "Cormorant Garamond",serif;margin:0 0 18px}h1 em{color:#2E5340}
.lede{max-width:760px;font:400 1.12rem/1.65 "Cormorant Garamond",serif;font-size:1.25rem;color:#3d362e}
.k{font:700 11px/1 Karla;letter-spacing:.22em;text-transform:uppercase;color:#8A6A3C}
.dir{margin-top:110px}.dir-h{display:grid;grid-template-columns:auto 1fr;gap:28px;align-items:end;border-bottom:1px solid #cfc3ad;padding-bottom:22px;margin-bottom:34px}
.dir-h .n{font:300 7rem/0.8 "Cormorant Garamond";color:#b6a689}.dir-h h2{font:400 2.6rem/1 "Cormorant Garamond";margin:8px 0 10px}.dir-h p{margin:0;max-width:760px;color:#4a4238}
.row{display:grid;gap:20px;margin-top:20px}.r3{grid-template-columns:1fr 1.25fr 1fr}.r2{grid-template-columns:1fr 1fr}
.card{background:#F6F1E7;padding:26px;min-height:240px;display:grid;align-content:space-between;gap:16px}.card.d{background:#20392B}.card .k{display:block}
.cap{font:600 10px/1.4 Karla;letter-spacing:.16em;text-transform:uppercase;color:#8b7f6e}
.sw{display:grid;grid-template-columns:repeat(5,1fr);gap:10px}.sw div{height:92px;outline:1px solid rgba(0,0,0,.08);outline-offset:-1px;padding:10px;font:600 10px/1.3 Karla;letter-spacing:.08em;display:flex;align-items:flex-end}
.frame{background:#fff;box-shadow:0 30px 60px -40px rgba(0,0,0,.45);overflow:hidden;position:relative}
.hdr{display:grid;grid-template-columns:1fr auto 1fr;align-items:center;padding:16px 28px;font:700 10px/1 Karla;letter-spacing:.2em;text-transform:uppercase}
.hdr nav{display:flex;gap:22px}.hdr nav:last-child{justify-content:flex-end}
.ftr{padding:46px 40px;display:grid;grid-template-columns:1.3fr 1fr 1fr 1fr;gap:30px;font-size:13px}.ftr b{display:block;font:700 10px Karla;letter-spacing:.2em;text-transform:uppercase;margin-bottom:10px;opacity:.7}
.phone{width:390px;height:780px;border-radius:34px;border:10px solid #1d1b18;overflow:hidden;background:#F6F1E7;position:relative;justify-self:center}
.verdict{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-top:30px}.verdict div{background:#F6F1E7;padding:24px}.verdict h3{font:500 1.5rem "Cormorant Garamond";margin:0 0 8px}
.pick{background:#20392B!important;color:#E9EFE7}.pick .k{color:#E9CFA4}
img{display:block;width:100%;height:100%;object-fit:cover}
@media (max-width:900px){.page{padding:32px 16px 80px}.r3,.r2,.verdict,.row[style]{grid-template-columns:minmax(0,1fr)!important}.row>*,.card{min-width:0}.card svg{max-width:100%}.sw{grid-template-columns:repeat(3,1fr)}.frame{overflow-x:auto}.frame>div,.frame>svg{min-width:900px}.phone{transform:scale(.85);transform-origin:top center}.dir-h{grid-template-columns:1fr}.dir-h .n{font-size:4rem}.hdr nav{display:none}table{display:block;overflow-x:auto}}
table{width:100%;border-collapse:collapse;background:#F6F1E7;margin-top:24px;font-size:14px}td,th{padding:12px 16px;text-align:left;border-bottom:1px solid #e2d8c6;vertical-align:top}th{font:700 10px Karla;letter-spacing:.18em;text-transform:uppercase;color:#8A6A3C}
'''
def palette(items): return '<div class="sw">'+''.join(f'<div style="background:{c};color:{t}">{n}<br>{c}</div>' for n,c,t in items)+'</div>'
NAV1='<nav><span>Stay</span><span>Pools</span><span>Dining</span><span>Meetings</span></nav>'
NAV2='<nav><span>Gallery</span><span>About</span><span>Contact</span><span style="padding:9px 14px;background:#B7772A;color:#1b1712">Book</span></nav>'

# ---------- DIRECTION 1 — THE PAVILION ----------
d1 = f'''
<section class="dir"><div class="dir-h"><span class="n">01</span><div><span class="k">Heritage crest · in the spirit of Le Sirenuse</span><h2>The Pavilion</h2>
<p>An emblem drawn from the hotel’s own garden gazebo — the two-tier octagonal roof with its windowed lantern — standing under an arch, with a breeze line passing through the open sides. Above a spaced Bodoni wordmark, it reads like a house crest that could be cast in brass for keyrings, embossed on stationery or carved at reception.</p></div></div>
<div class="row r3">
 <div class="card"><span class="k">Emblem</span><div style="height:230px">{emb('pavilion','#20392B',style='style="height:100%;display:block;margin:auto"')}</div><span class="cap">Original vector · drawn from the Breez gazebos</span></div>
 <div class="card" style="justify-items:center;text-align:center"><span class="k" style="justify-self:start">Full crest</span>
   <div style="display:grid;justify-items:center;gap:14px">{emb('pavilion','#20392B',style='style="height:96px"')}{bod('#20392B','style="height:26px"')}{sub('Hotel &middot; Busia &middot; Kenya','#6E6355','.5em','9px')}</div><span class="cap" style="justify-self:start">Stationery, signage, menus, keyrings</span></div>
 <div class="card d"><span class="k" style="color:#E9CFA4">On forest green</span><div style="display:grid;justify-items:center;gap:14px">{emb('pavilion','#F6F1E7',style='style="height:96px"')}{bod('#F6F1E7','style="height:26px"')}</div>
   <div style="display:flex;gap:26px;align-items:end">{emb('pavilion','#F6F1E7',style='style="height:34px"')}{emb('pavilion','#F6F1E7',style='style="height:18px"')}<span class="cap" style="color:#b9c4b9">34px · 18px — still a gazebo</span></div></div>
</div>
<div class="row r2">
 <div class="card"><span class="k">Type pairing</span><div>{bod2('#1E1A16','style="height:46px"')}<p style="font:italic 300 2.1rem/1.1 'Cormorant Garamond';margin:18px 0 6px">A garden house in Busia.</p><p style="margin:0;color:#4a4238">Bodoni Moda 500 (wordmark, outlined) · Cormorant Garamond italic (editorial) · Karla (text and labels). All SIL Open Font Licence.</p></div></div>
 <div class="card"><span class="k">Palette</span>{palette([('Forest','#20392B','#E9EFE7'),('Ivory','#F6F1E7','#6E6355'),('Stone','#E0D5C2','#6E6355'),('Antique brass','#A8823F','#fff'),('Ink','#1E1A16','#ccc')])}<span class="cap">No new colours — brass replaces the brighter sand for details.</span></div>
</div>
<div class="row"><span class="k">Header — over a photograph and solid</span>
 <div class="frame"><div style="position:relative;height:150px"><img src="{P['court']}" style="position:absolute;inset:0;filter:brightness(.72)"><div class="hdr" style="position:relative;color:#F6F1E7">{NAV1}<div style="display:grid;justify-items:center;gap:6px">{emb('pavilion','#F6F1E7',style='style="height:40px"')}{bod('#F6F1E7','style="height:12px"')}</div>{NAV2}</div></div>
 <div class="hdr" style="background:#F6F1E7;color:#20392B">{NAV1}<div style="display:flex;align-items:center;gap:12px">{emb('pavilion','#20392B',style='style="height:30px"')}{bod('#20392B','style="height:11px"')}</div>{NAV2}</div></div></div>
<div class="row"><span class="k">Homepage signature composition</span>
 <div class="frame" style="background:#F6F1E7;height:760px">
   <div style="position:absolute;left:50%;top:70px;transform:translateX(-50%);display:grid;justify-items:center;gap:18px;text-align:center;z-index:2">
     {emb('pavilion','#20392B',style='style="height:150px"')}{bod('#20392B','style="height:40px"')}{sub('Hotel &middot; Busia &middot; Kenya','#6E6355','.55em','11px')}
     <p style="font:italic 300 1.5rem/1.3 'Cormorant Garamond';color:#4a4238;margin:4px 0 0">Karibu — a garden house on the Kisumu&ndash;Busia Road.</p></div>
   <div style="position:absolute;left:5%;top:380px;width:24%;height:340px"><img src="{P['tower']}"></div>
   <div style="position:absolute;left:32%;top:440px;width:36%;height:320px"><img src="{P['gazebo']}"></div>
   <div style="position:absolute;right:5%;top:340px;width:22%;height:300px"><img src="{P['lanes']}"></div>
 </div></div>
<div class="row" style="grid-template-columns:1fr 390px;align-items:start"><div><span class="k">Footer</span>
 <div class="frame" style="background:#20392B;color:#E9EFE7;margin-top:14px"><div class="ftr"><div style="display:grid;gap:14px;justify-items:start">{emb('pavilion','#E9CFA4',style='style="height:70px"')}{bod('#F6F1E7','style="height:16px"')}<span style="opacity:.75">Karibu. We look forward to welcoming you.</span></div><div><b>Visit</b>Kisumu&ndash;Busia Road<br>Busia, Kenya</div><div><b>Stay</b>Rooms<br>Pools<br>Dining</div><div><b>Talk to us</b>Reception<br>WhatsApp</div></div></div></div>
 <div><span class="k">Mobile</span><div class="phone" style="margin-top:14px"><div style="display:flex;justify-content:space-between;align-items:center;padding:16px 18px">{emb('pavilion','#20392B',style='style="height:34px"')}<span style="font:700 10px Karla;letter-spacing:.2em;border:1px solid #20392B;padding:9px 12px">MENU</span></div>
  <div style="display:grid;justify-items:center;gap:12px;padding:26px 0 30px">{emb('pavilion','#20392B',style='style="height:110px"')}{bod('#20392B','style="height:24px"')}{sub('Hotel &middot; Busia','#6E6355','.5em','9px')}</div>
  <div style="display:grid;grid-template-columns:1.2fr 1fr;gap:8px;padding:0 14px;height:330px"><img src="{P['gazebo']}" style="height:100%"><div style="display:grid;gap:8px"><img src="{P['tower']}"><img src="{P['lanes']}"></div></div></div></div>
</div></section>'''

# ---------- DIRECTION 2 — THE SIGNATURE ----------
PLUM='#4A2131'
d2 = f'''
<section class="dir"><div class="dir-h"><span class="n">02</span><div><span class="k">Expressive signature · in the spirit of The Drake</span><h2>The Signature</h2>
<p>A custom script “Breez” — Italianno letterforms, tightened through the double e, thickened as outlines and finished with a drawn swash that leaves the z and returns beneath the word. It carries forward the gold script already on the hotel’s gate sign rather than importing a foreign style. The B monogram holds a single leaf-blade stroke through its bowls. Deep plum appears only where the signature appears.</p></div></div>
<div class="row r3">
 <div class="card"><span class="k">Monogram</span><div style="height:230px">{emb('monogram','#20392B',style='style="height:100%;display:block;margin:auto"')}</div><span class="cap">Bodoni B, redrawn with a leaf cut</span></div>
 <div class="card"><span class="k">Signature wordmark</span><div>{sig('#20392B','style="width:100%"')}</div><span class="cap">Outlined vector · custom swash · OFL base (Italianno)</span></div>
 <div class="card" style="background:{PLUM}"><span class="k" style="color:#E9CFA4">On plum</span><div>{sig('#F6F1E7','style="width:100%"')}</div><div style="display:flex;gap:24px;align-items:end">{emb('monogram','#F6F1E7',style='style="height:36px"')}{emb('monogram','#F6F1E7',style='style="height:18px"')}<span class="cap" style="color:#d8bfc7">Monogram at 36 and 18px</span></div></div>
</div>
<div class="row r2">
 <div class="card"><span class="k">Type pairing</span><div><div style="display:flex;align-items:end;gap:18px">{sig('#1E1A16','style="height:70px"')}<span style="font:500 1.6rem 'Cormorant Garamond';letter-spacing:.3em">HOTEL</span></div><p style="font:300 2.1rem/1.1 'Cormorant Garamond';margin:18px 0 6px">The many moods <em>of The Breez</em></p><p style="margin:0;color:#4a4238">Breez signature (outlined) · Cormorant Garamond (headings, already on the site) · Karla (text). The script is never typed as running text.</p></div></div>
 <div class="card"><span class="k">Palette</span>{palette([('Forest','#20392B','#E9EFE7'),('Ivory','#F6F1E7','#6E6355'),('Plum accent',PLUM,'#E9CFA4'),('Brass','#B08A4E','#fff'),('Blush stone','#E7D9CC','#6E6355')])}<span class="cap">Plum is reserved for signature moments — never full pages.</span></div>
</div>
<div class="row"><span class="k">Header — over a photograph and solid</span>
 <div class="frame"><div style="position:relative;height:150px"><img src="{P['court']}" style="position:absolute;inset:0;filter:brightness(.72)"><div class="hdr" style="position:relative;color:#F6F1E7">{NAV1}<div>{sig('#F6F1E7','style="height:52px"')}</div>{NAV2}</div></div>
 <div class="hdr" style="background:#F6F1E7;color:#20392B">{NAV1}<div style="display:flex;align-items:center;gap:12px">{emb('monogram','#20392B',style='style="height:30px"')}{sig('#20392B','style="height:34px"')}</div>{NAV2}</div></div></div>
<div class="row"><span class="k">Homepage signature composition — the lettering crosses from colour into photography</span>
 <div class="frame" style="background:#F6F1E7;height:780px">
   <div style="position:absolute;left:0;right:0;top:0;height:330px;background:{PLUM}"></div>
   <div style="position:absolute;left:6%;top:56px;color:#E9CFA4">{sub('The Breez &middot; Busia, Kenya','#E9CFA4','.4em','11px')}</div>
   <div style="position:absolute;right:6%;top:52px;max-width:300px;color:#F1E3E7;font:300 1.35rem/1.35 'Cormorant Garamond'">Palms, pools and a garden of gazebos on the Kisumu&ndash;Busia Road.</div>
   <div style="position:absolute;left:44%;top:250px;width:50%;height:470px"><img src="{P['court']}"></div>
   <div style="position:absolute;left:6%;top:400px;width:24%;height:330px"><img src="{P['lobby']}" style="object-position:50% 40%"></div>
   <div style="position:absolute;left:32%;top:560px;width:10%;height:170px"><img src="{P['pooltop']}"></div>
   <div style="position:absolute;left:3%;top:120px;width:84%;z-index:3">{sig('#F6F1E7','style="width:100%;filter:drop-shadow(0 2px 30px rgba(40,10,20,.25))"',1.6)}</div>
 </div></div>
<div class="row" style="grid-template-columns:1fr 390px;align-items:start"><div><span class="k">Footer</span>
 <div class="frame" style="background:{PLUM};color:#F1E3E7;margin-top:14px"><div style="padding:40px 40px 0">{sig('#F6F1E7','style="width:62%"')}</div><div class="ftr" style="padding-top:20px"><div>Karibu. We look forward to welcoming you.</div><div><b>Visit</b>Kisumu&ndash;Busia Road<br>Busia, Kenya</div><div><b>Stay</b>Rooms<br>Pools<br>Dining</div><div><b>Talk to us</b>Reception<br>WhatsApp</div></div></div></div>
 <div><span class="k">Mobile</span><div class="phone" style="margin-top:14px"><div style="height:250px;background:{PLUM};padding:16px 18px;position:relative"><div style="display:flex;justify-content:space-between;align-items:center">{emb('monogram','#F6F1E7',style='style="height:30px"')}<span style="font:700 10px Karla;letter-spacing:.2em;color:#F6F1E7;border:1px solid #F6F1E7;padding:9px 12px">MENU</span></div></div>
  <div style="position:absolute;left:10px;right:10px;top:150px;z-index:2">{sig('#F6F1E7','style="width:100%"')}</div>
  <div style="position:absolute;left:0;right:0;top:220px;height:290px"><img src="{P['court']}"></div>
  <div style="position:absolute;left:18px;top:530px;width:46%;height:200px"><img src="{P['lobby']}"></div><div style="position:absolute;right:18px;top:560px;width:38%;height:150px"><img src="{P['pooltop']}"></div></div></div>
</div></section>'''

# ---------- DIRECTION 3 — THE GARDEN FAN ----------
d3 = f'''
<section class="dir"><div class="dir-h"><span class="n">03</span><div><span class="k">Architectural wordmark · editorial landscape</span><h2>The Garden Fan</h2>
<p>A fan-palm emblem whose blades all lean one way — the breeze made visible — paired with very widely spaced Italiana capitals. At scale the letters become windows onto the hotel’s architecture: the veranda, the tower, the pool lanes.</p></div></div>
<div class="row r3">
 <div class="card"><span class="k">Emblem</span><div style="height:230px">{emb('palm','#20392B',style='style="height:100%;display:block;margin:auto"')}</div><span class="cap">Original vector · fan palm in the wind</span></div>
 <div class="card" style="justify-items:center"><span class="k" style="justify-self:start">Wordmark</span>{ital('#20392B','style="width:88%"')}{sub('The Breez &middot; Hotel &middot; Busia','#6E6355','.6em','9px')}</div>
 <div class="card" style="background:#8E9283"><span class="k" style="color:#F6F1E7">On sage</span><div style="display:grid;justify-items:center;gap:16px">{emb('palm','#F6F1E7',style='style="height:96px"')}{ital('#F6F1E7','style="width:70%"')}</div><div style="display:flex;gap:24px;align-items:end">{emb('palm','#F6F1E7',style='style="height:36px"')}{emb('palm','#F6F1E7',style='style="height:18px"')}<span class="cap" style="color:#eef0e8">Fine blades fill in below 24px</span></div></div>
</div>
<div class="row r2">
 <div class="card"><span class="k">Type pairing</span><div>{ital('#1E1A16','style="height:40px"')}<p style="font:400 2rem/1.15 'Cormorant Garamond';margin:18px 0 6px">Architecture, gardens and light.</p><p style="margin:0;color:#4a4238">Italiana (wordmark, outlined) · Cormorant Garamond · Karla. All SIL Open Font Licence.</p></div></div>
 <div class="card"><span class="k">Palette</span>{palette([('Forest','#20392B','#E9EFE7'),('Sage','#8E9283','#fff'),('Stone','#E0D5C2','#6E6355'),('Ivory','#F6F1E7','#6E6355'),('Ink','#1E1A16','#ccc')])}<span class="cap">Cooler, quieter; no warm accent at all.</span></div>
</div>
<div class="row"><span class="k">Header — over a photograph and solid</span>
 <div class="frame"><div style="position:relative;height:150px"><img src="{P['court']}" style="position:absolute;inset:0;filter:brightness(.72)"><div class="hdr" style="position:relative;color:#F6F1E7">{NAV1}<div style="display:grid;justify-items:center;gap:8px">{emb('palm','#F6F1E7',style='style="height:34px"')}{ital('#F6F1E7','style="height:13px"')}</div>{NAV2}</div></div>
 <div class="hdr" style="background:#F6F1E7;color:#20392B">{NAV1}<div style="display:flex;align-items:center;gap:12px">{emb('palm','#20392B',style='style="height:28px"')}{ital('#20392B','style="height:13px"')}</div>{NAV2}</div></div></div>
<div class="row"><span class="k">Homepage signature composition — photographs seen through the letters</span>
 <div class="frame" style="background:#E0D5C2;height:700px">
   <svg viewBox="0 0 {iw:.0f} {ih:.0f}" style="position:absolute;left:4%;top:90px;width:92%">
     <defs><clipPath id="lt"><path d="{it}"/></clipPath></defs>
     <g clip-path="url(#lt)"><image href="{P['veranda']}" x="0" y="-30" width="{iw*0.42:.0f}" height="200" preserveAspectRatio="xMidYMid slice"/><image href="{P['tower']}" x="{iw*0.40:.0f}" y="-60" width="{iw*0.24:.0f}" height="260" preserveAspectRatio="xMidYMid slice"/><image href="{P['lanes']}" x="{iw*0.62:.0f}" y="-40" width="{iw*0.40:.0f}" height="200" preserveAspectRatio="xMidYMid slice"/></g></svg>
   <div style="position:absolute;left:4%;top:56px">{sub('The Breez &middot; Hotel &middot; Busia, Kenya','#4a4238','.5em','11px')}</div>
   <div style="position:absolute;left:4%;top:410px;width:30%;height:250px"><img src="{P['cypress']}"></div>
   <div style="position:absolute;left:38%;top:440px;max-width:340px;font:300 1.6rem/1.3 'Cormorant Garamond'">Verandas, a tower and two pools behind a garden of palms.</div>
   <div style="position:absolute;right:4%;top:400px;width:24%;height:270px"><img src="{P['fountain']}"></div>
 </div></div>
<div class="row" style="grid-template-columns:1fr 390px;align-items:start"><div><span class="k">Footer</span>
 <div class="frame" style="background:#8E9283;color:#F6F1E7;margin-top:14px"><div class="ftr"><div style="display:grid;gap:14px;justify-items:start">{emb('palm','#F6F1E7',style='style="height:64px"')}{ital('#F6F1E7','style="height:14px"')}</div><div><b>Visit</b>Kisumu&ndash;Busia Road<br>Busia, Kenya</div><div><b>Stay</b>Rooms<br>Pools<br>Dining</div><div><b>Talk to us</b>Reception<br>WhatsApp</div></div></div></div>
 <div><span class="k">Mobile</span><div class="phone" style="margin-top:14px;background:#E0D5C2"><div style="display:flex;justify-content:space-between;align-items:center;padding:16px 18px">{emb('palm','#20392B',style='style="height:32px"')}<span style="font:700 10px Karla;letter-spacing:.2em;border:1px solid #20392B;padding:9px 12px">MENU</span></div>
  <svg viewBox="0 0 {iw:.0f} {ih:.0f}" style="width:92%;margin:40px 4% 0"><defs><clipPath id="lt2"><path d="{it}"/></clipPath></defs><g clip-path="url(#lt2)"><image href="{P['veranda']}" x="0" y="-30" width="{iw*0.5:.0f}" height="200" preserveAspectRatio="xMidYMid slice"/><image href="{P['lanes']}" x="{iw*0.48:.0f}" y="-40" width="{iw*0.55:.0f}" height="200" preserveAspectRatio="xMidYMid slice"/></g></svg>
  <p style="padding:0 18px;margin:30px 0 18px;font:300 1.4rem/1.3 'Cormorant Garamond'">Verandas, a tower and two pools behind a garden of palms.</p><div style="height:300px;margin:0 18px"><img src="{P['cypress']}"></div></div></div>
</div></section>'''

compare = f'''
<section class="dir"><div class="dir-h"><span class="n">→</span><div><span class="k">Comparison and recommendation</span><h2>Which direction should become The Breez?</h2></div></div>
<table><tr><th></th><th>01 The Pavilion</th><th>02 The Signature</th><th>03 The Garden Fan</th></tr>
<tr><td>Rooted in the actual hotel</td><td>Strongest — the gazebo is a real Breez building</td><td>Strong — continues the script on the gate sign</td><td>Moderate — palms are present but generic to the region</td></tr>
<tr><td>Recognisable at 18–34px</td><td>Yes (arch + roof silhouette)</td><td>Monogram yes; script needs ≥ 34px</td><td>Weak — fine blades fill in</td></tr>
<tr><td>Physical applications</td><td>Excellent: brass, emboss, embroidery</td><td>Excellent for signage, menus, packaging</td><td>Good for prints and patterns</td></tr>
<tr><td>Expressive impact on the homepage</td><td>Calm, established</td><td>Highest — Drake-level confidence</td><td>High, but the letter-window trick is familiar</td></tr>
<tr><td>Risk</td><td>Could feel formal if used alone</td><td>Plum overused would feel borrowed</td><td>Least distinctive of the three</td></tr></table>
<div class="verdict">
 <div class="pick"><span class="k">Recommended</span><h3>Pavilion crest + Breez signature</h3><p>Use the Pavilion crest and Bodoni wordmark as the primary identity (header, footer, stationery, signage, keyrings). Use the Breez script signature as the expressive secondary mark for one large homepage composition, menus and promotional pieces, with plum only in that composition. This mirrors how a heritage house keeps a crest and a signature side by side.</p></div>
 <div><span class="k">Header</span><h3>Small and balanced</h3><p>Emblem at 30–40px with the spaced wordmark beside it on solid backgrounds, stacked and centred over the hero. Light and dark versions; the crest stays legible at 18px.</p></div>
 <div><span class="k">Before it goes live</span><h3>Your decision</h3><p>The current header text logo stays until you approve. Note: the gate sign reads “The Breeze Hotel” (with a final e) while the website uses “The Breez”. Please confirm the official spelling before any new mark is drawn on it.</p></div>
</div></section>'''

html=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>The Breez — identity studies</title><style>{CSS}</style></head><body><div class="page">
<span class="k">The Breez Hotel · Identity studies · 27 November 2026</span><h1>Three directions for <em>The Breez</em></h1>
<p class="lede">Every emblem and wordmark here is an original vector drawn for The Breez, using only open-licence typefaces as starting letterforms. Photographs are the hotel’s own. The current website logo is a typed “The Breez / Hotel · Busia” in Cormorant Garamond and Karla, with no emblem; the gate sign carries a gold script “Breeze” over serif “HOTEL”. These studies keep forest green, ivory and stone as the foundation.</p>
{d1}{d2}{d3}{compare}</div></body></html>'''
open('/tmp/idw/study/breez-identity-studies.html','w').write(html)
print(len(html)//1024,'KB')
