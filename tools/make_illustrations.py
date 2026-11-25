import math, random, sys, os
out=sys.argv[1]
random.seed(7)
def palm(x,base,h,s=1.0,lean=0.0,trunk="#6b4a2f",leaf="#2f6b3a",leaf2="#3f8a4a"):
    # curved trunk
    tx=x+lean*h
    p=f'<path d="M{x-6*s},{base} Q{x+lean*h*0.4-4*s},{base-h*0.55} {tx-3*s},{base-h} L{tx+3*s},{base-h} Q{x+lean*h*0.4+4*s},{base-h*0.55} {x+6*s},{base} Z" fill="{trunk}"/>'
    for i in range(0,int(h),int(14*s)+1):
        yy=base-i; xx=x+lean*h*(i/h)**1.2
        p+=f'<path d="M{xx-5*s},{yy} l{10*s},-3" stroke="#4a321f" stroke-width="{1.4*s}" opacity=".5"/>'
    cx,cy=tx,base-h
    for k,a in enumerate(range(-170,10,20)):
        r=math.radians(a); L=(70+random.random()*30)*s
        ex=cx+math.cos(r)*L; ey=cy+math.sin(r)*L*0.55+L*0.35
        mx=cx+math.cos(r)*L*0.5; my=cy+math.sin(r)*L*0.5-8*s
        col=leaf if k%2 else leaf2
        p+=f'<path d="M{cx},{cy} Q{mx},{my-10*s} {ex},{ey} Q{mx+6*s},{my+6*s} {cx},{cy+4*s} Z" fill="{col}"/>'
    p+=f'<circle cx="{cx}" cy="{cy+4*s}" r="{6*s}" fill="#5a3b22"/>'
    return p
def umbrella(x,y,w,c1="#5a3a24",c2="#f1e4cc"):
    n=8; seg=w/n; p=''
    for i in range(n):
        col=c1 if i%2==0 else c2
        x0=x-w/2+i*seg
        p+=f'<path d="M{x},{y} L{x0},{y+w*0.22} L{x0+seg},{y+w*0.22} Z" fill="{col}"/>'
    p+=f'<path d="M{x-w/2},{y+w*0.22} Q{x},{y+w*0.27} {x+w/2},{y+w*0.22}" fill="none" stroke="{c1}" stroke-width="2"/>'
    p+=f'<rect x="{x-1.5}" y="{y}" width="3" height="{w*0.6}" fill="#3a2616"/>'
    return p
def building(x,y,w,floors,fh,tile="#c98f3e",tile2="#b97c2f"):
    h=floors*fh; p=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{tile}"/>'
    # tile texture
    for r in range(0,int(h),14):
        for c in range(0,int(w),22):
            if random.random()<.35: p+=f'<rect x="{x+c+((r//14)%2)*11}" y="{y+r}" width="20" height="12" fill="{tile2}" opacity=".55"/>'
    # parapet
    p+=f'<rect x="{x-8}" y="{y-14}" width="{w+16}" height="16" fill="#efe2c8"/><rect x="{x-8}" y="{y-2}" width="{w+16}" height="4" fill="#00000022"/>'
    for f in range(floors):
        fy=y+f*fh+fh*0.28
        p+=f'<rect x="{x+16}" y="{fy}" width="{w-32}" height="{fh*0.46}" fill="#23303a"/>'
        for c in range(x+16,int(x+w-16),46):
            p+=f'<rect x="{c+4}" y="{fy+4}" width="38" height="{fh*0.46-8}" fill="#5f87a0" opacity=".55"/>'
            p+=f'<rect x="{c+4}" y="{fy+4}" width="12" height="{fh*0.46-8}" fill="#cfe3ee" opacity=".35"/>'
        p+=f'<rect x="{x+10}" y="{fy+fh*0.46}" width="{w-20}" height="5" fill="#efe2c8"/>'
        # balcony rail
        p+=f'<rect x="{x+16}" y="{fy+fh*0.30}" width="{w-32}" height="2" fill="#efe2c8" opacity=".8"/>'
    return p,h
def svg(w,h,body,defs=''):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" preserveAspectRatio="xMidYMid slice"><defs>{defs}</defs>{body}</svg>'
def hero(dusk=False):
    W,H=1600,1000
    sky=('#f3b26b','#f7d9a8','#fbeed6') if dusk else ('#8fc3e6','#cfe6f2','#f6efe0')
    defs=f'<linearGradient id="sk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{sky[0]}"/><stop offset=".6" stop-color="{sky[1]}"/><stop offset="1" stop-color="{sky[2]}"/></linearGradient><linearGradient id="pl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4fb3c8"/><stop offset="1" stop-color="#1f7f98"/></linearGradient><linearGradient id="sh" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#000" stop-opacity=".18"/><stop offset="1" stop-color="#000" stop-opacity="0"/></linearGradient>'
    b=f'<rect width="{W}" height="{H}" fill="url(#sk)"/>'
    if dusk: b+='<circle cx="1220" cy="300" r="90" fill="#fff2d6" opacity=".8"/>'
    else:
        for cx,cy,s in [(300,160,1),(1100,120,1.3),(1400,230,.8)]:
            b+=f'<g opacity=".85" fill="#fff"><ellipse cx="{cx}" cy="{cy}" rx="{90*s}" ry="{26*s}"/><ellipse cx="{cx+50*s}" cy="{cy-18*s}" rx="{60*s}" ry="{28*s}"/><ellipse cx="{cx-50*s}" cy="{cy-8*s}" rx="{50*s}" ry="{22*s}"/></g>'
    # far trees
    for i in range(40):
        x=i*42+random.random()*20; r=30+random.random()*30
        b+=f'<circle cx="{x}" cy="{560-random.random()*30}" r="{r}" fill="{"#557a45" if i%2 else "#4b6f3d"}"/>'
    # cypress-like tall trees
    for x in [140,1500,1560]:
        b+=f'<ellipse cx="{x}" cy="420" rx="34" ry="170" fill="#3f6634"/>'
    bp,bh=building(520,250,640,4,78)
    b+=bp
    # side wing
    b+=f'<rect x="1160" y="380" width="220" height="200" fill="#d9a35a"/><rect x="1160" y="380" width="220" height="14" fill="#efe2c8"/>'
    for c in range(1180,1370,60): b+=f'<rect x="{c}" y="420" width="40" height="60" fill="#2c3a44"/><rect x="{c}" y="500" width="40" height="60" fill="#2c3a44"/>'
    b+='<rect x="1160" y="380" width="40" height="200" fill="url(#sh)"/>'
    # colonnade
    b+=f'<rect x="440" y="560" width="820" height="18" fill="#efe2c8"/>'
    for c in range(460,1260,70):
        b+=f'<rect x="{c}" y="578" width="16" height="110" fill="#f4ead6"/><rect x="{c-4}" y="578" width="24" height="8" fill="#e2d3b4"/><rect x="{c-4}" y="680" width="24" height="8" fill="#e2d3b4"/>'
    b+=f'<rect x="440" y="578" width="820" height="110" fill="#3b2a1d" opacity=".55"/>'
    for c in range(460,1260,70): b+=f'<rect x="{c}" y="578" width="16" height="110" fill="#f4ead6"/>'
    # lawn + deck
    b+=f'<rect x="0" y="688" width="{W}" height="{H-688}" fill="#6f9a4c"/>'
    b+=f'<path d="M0,700 L{W},700 L{W},740 L0,760Z" fill="#e8d6b4"/>'
    # pool
    b+=f'<path d="M180,780 L1420,760 L1520,960 L80,990 Z" fill="#efe2c8"/>'
    b+=f'<path d="M220,800 L1390,782 L1470,940 L130,966 Z" fill="url(#pl)"/>'
    for i in range(26):
        x=240+random.random()*1150; y=810+random.random()*140; l=30+random.random()*60
        b+=f'<path d="M{x},{y} q{l/2},-6 {l},0" stroke="#bfe9f2" stroke-width="3" fill="none" opacity=".7" stroke-linecap="round"/>'
    # umbrellas & loungers
    for x,y,w in [(330,600,190),(700,612,170),(1260,600,200)]:
        b+=umbrella(x,y,w)
        b+=f'<rect x="{x-60}" y="{y+w*0.6-8}" width="120" height="10" rx="3" fill="#f6f0e4"/><rect x="{x-60}" y="{y+w*0.6+2}" width="6" height="10" fill="#8a6a4a"/><rect x="{x+54}" y="{y+w*0.6+2}" width="6" height="10" fill="#8a6a4a"/>'
    # palms
    b+=palm(90,1000,700,1.5,0.05)
    b+=palm(1480,1000,640,1.35,-0.08)
    b+=palm(430,720,380,0.95,0.04)
    b+=palm(1130,720,420,1.0,-0.03)
    if dusk: b+=f'<rect width="{W}" height="{H}" fill="#f08a3c" opacity=".12"/>'
    return svg(W,H,b,defs)
def room():
    W,H=1200,900
    d='<linearGradient id="w" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f4ead8"/><stop offset="1" stop-color="#e7d6b8"/></linearGradient><linearGradient id="win" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#bfe0ef"/><stop offset="1" stop-color="#e9f3e2"/></linearGradient>'
    b=f'<rect width="{W}" height="{H}" fill="url(#w)"/><rect y="700" width="{W}" height="200" fill="#c9a77d"/>'
    for i in range(0,W,80): b+=f'<rect x="{i}" y="700" width="2" height="200" fill="#b08b5e"/>'
    b+='<rect x="760" y="150" width="300" height="400" fill="url(#win)"/><rect x="760" y="150" width="300" height="400" fill="none" stroke="#6b4a2f" stroke-width="10"/><rect x="905" y="150" width="10" height="400" fill="#6b4a2f"/>'
    b+=palm(930,560,300,0.8,0.05)
    b+='<path d="M700,120 q60,300 20,600 l60,0 q20,-300 -20,-600Z" fill="#a8562f"/><path d="M1120,120 q-60,300 -20,600 l-60,0 q-20,-300 20,-600Z" fill="#a8562f"/>'
    # four poster bed
    b+='<rect x="140" y="150" width="20" height="600" fill="#5a3a22"/><rect x="600" y="150" width="20" height="600" fill="#5a3a22"/><rect x="130" y="140" width="500" height="22" fill="#4a2f1b"/>'
    b+='<path d="M160,162 q-10,260 30,540 l-40,0 q-20,-280 -10,-540Z" fill="#ffffff" opacity=".75"/><path d="M600,162 q10,260 -30,540 l40,0 q20,-280 10,-540Z" fill="#ffffff" opacity=".75"/>'
    b+='<rect x="170" y="380" width="420" height="120" rx="6" fill="#6b4329"/>'
    b+='<rect x="170" y="500" width="420" height="150" rx="10" fill="#fbf7ef"/><rect x="170" y="560" width="420" height="40" fill="#8b4a2b"/>'
    for x,c in [(200,"#a65a33"),(300,"#d9b48a"),(400,"#a65a33"),(490,"#7b4a2a")]: b+=f'<rect x="{x}" y="455" width="90" height="70" rx="14" fill="{c}"/>'
    b+='<rect x="170" y="650" width="420" height="60" fill="#5a3a22"/>'
    b+='<rect x="660" y="560" width="80" height="140" fill="#6b4a2f"/><rect x="672" y="520" width="16" height="40" fill="#e8c98f"/><path d="M660,520 l40,-40 l40,40Z" fill="#f4e2bf"/>'
    return svg(W,H,b,d)
def dining():
    W,H=1200,900
    d='<radialGradient id="g" cx=".5" cy=".3" r=".8"><stop offset="0" stop-color="#4a2a1a"/><stop offset="1" stop-color="#1e120b"/></radialGradient>'
    b=f'<rect width="{W}" height="{H}" fill="url(#g)"/>'
    b+='<ellipse cx="600" cy="520" rx="520" ry="300" fill="#6b3f24"/><ellipse cx="600" cy="500" rx="520" ry="300" fill="#8a5431"/>'
    for i in range(0,1100,36): b+=f'<path d="M{80+i},{260+abs(550-i)*0.05} q20,240 0,500" stroke="#7a4728" stroke-width="2" fill="none" opacity=".5"/>'
    b+='<ellipse cx="600" cy="500" rx="250" ry="150" fill="#f5efe4"/><ellipse cx="600" cy="500" rx="200" ry="115" fill="#ece3d3"/>'
    b+='<ellipse cx="540" cy="490" rx="120" ry="70" fill="#f8f3e9"/>'  # ugali
    b+='<ellipse cx="540" cy="475" rx="100" ry="45" fill="#fffdf8"/>'
    b+='<ellipse cx="680" cy="520" rx="90" ry="55" fill="#3d6b2a"/>'  # sukuma
    for i in range(14): b+=f'<ellipse cx="{620+random.random()*120}" cy="{495+random.random()*50}" rx="16" ry="7" fill="#2f5a20" transform="rotate({random.random()*180} {650} {520})"/>'
    for i in range(6): b+=f'<ellipse cx="{640+i*18}" cy="{440+(i%2)*14}" rx="30" ry="18" fill="#b0541f"/>'  # fish/meat
    b+='<ellipse cx="680" cy="430" rx="110" ry="36" fill="#c6662a"/><path d="M570,430 l-40,-20 l0,40Z" fill="#c6662a"/>'
    for x,y in [(220,420),(980,420)]: b+=f'<ellipse cx="{x}" cy="{y}" rx="70" ry="40" fill="#f5efe4" opacity=".9"/><rect x="{x-6}" y="{y-150}" width="12" height="110" fill="#e9dcc4" opacity=".6"/><ellipse cx="{x}" cy="{y-160}" rx="34" ry="44" fill="#d88a3a" opacity=".55"/>'
    b+='<rect x="300" y="640" width="12" height="110" rx="6" fill="#c9b48e" transform="rotate(-20 300 640)"/><rect x="880" y="640" width="12" height="110" rx="6" fill="#c9b48e" transform="rotate(20 880 640)"/>'
    return svg(W,H,b,d)
def conference():
    W,H=1200,900
    b=f'<rect width="{W}" height="{H}" fill="#efe6d6"/><rect y="640" width="{W}" height="260" fill="#9c7a55"/>'
    b+='<rect x="380" y="120" width="440" height="250" fill="#2a2f35"/><rect x="396" y="136" width="408" height="218" fill="#d9a35a"/><rect x="430" y="170" width="200" height="18" fill="#fff7e8"/><rect x="430" y="205" width="300" height="10" fill="#fff7e8" opacity=".7"/><rect x="430" y="225" width="260" height="10" fill="#fff7e8" opacity=".7"/>'
    for i,x in enumerate(range(80,1140,130)):
        b+=f'<rect x="{x}" y="430" width="100" height="14" fill="#5a3a22"/>'
    b+='<path d="M120,560 L1080,560 L1160,700 L40,700Z" fill="#5a3a22"/><path d="M120,550 L1080,550 L1160,690 L40,690Z" fill="#7a5233"/>'
    for x in range(150,1080,110):
        b+=f'<rect x="{x}" y="470" width="70" height="90" rx="10" fill="#2e3b45"/><rect x="{x-8}" y="700" width="86" height="100" rx="10" fill="#2e3b45"/>'
        b+=f'<rect x="{x+10}" y="590" width="50" height="34" fill="#f6efe2"/><circle cx="{x+60}" cy="640" r="10" fill="#c9e3ea"/>'
    b+='<rect x="0" y="0" width="1200" height="60" fill="#e2d4bc"/>'
    for x in range(100,1200,200): b+=f'<circle cx="{x}" cy="60" r="18" fill="#fff4d6"/>'
    return svg(W,H,b)
def poolsoft():
    W,H=1200,900
    d='<linearGradient id="pl" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#5cc0d4"/><stop offset="1" stop-color="#1c7a93"/></linearGradient>'
    b=f'<rect width="{W}" height="{H}" fill="url(#pl)"/>'
    for i in range(60):
        x=random.random()*W; y=random.random()*H; l=40+random.random()*120
        b+=f'<path d="M{x},{y} q{l/3},-14 {l*2/3},0 t{l/3},0" stroke="#d7f3f8" stroke-width="{2+random.random()*3}" fill="none" opacity="{.3+random.random()*.5}" stroke-linecap="round"/>'
    b+='<rect x="0" y="0" width="1200" height="120" fill="#efe2c8"/><rect x="0" y="120" width="1200" height="10" fill="#0003"/>'
    b+='<path d="M0,0 L520,0 L380,900 L0,900Z" fill="#000" opacity=".12"/>'
    b+=umbrella(980,10,300)
    b+='<rect x="830" y="40" width="170" height="40" rx="8" fill="#f6f0e4" transform="rotate(4 900 60)"/>'
    b+='<g transform="translate(260 520) rotate(-12)"><ellipse rx="70" ry="70" fill="none" stroke="#f2a33a" stroke-width="22"/><ellipse rx="70" ry="70" fill="none" stroke="#fff" stroke-width="22" stroke-dasharray="40 70"/></g>'
    return svg(W,H,b,d)
for name,fn in [('hero-day',lambda:hero(False)),('hero-dusk',lambda:hero(True)),('room',room),('dining',dining),('conference',conference),('pool',poolsoft)]:
    open(os.path.join(out,name+'.svg'),'w').write(fn())
print('ok')
