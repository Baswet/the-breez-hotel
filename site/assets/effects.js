/* The Breez Hotel — selective image effects. No dependencies.
   - [data-parallax="0.08"]  gentle vertical parallax (translate only)
   - .fx-ripple             water ripple on hover (fine pointers only; SVG filter)
   - [data-drift]           cursor-responsive image drift (fine pointers only)
   - [data-liquid]          gallery slider with WebGL displacement transitions,
                            crossfade fallback when WebGL or motion is unavailable
   Everything degrades to static images under prefers-reduced-motion. */
(() => {
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const fine = matchMedia('(hover: hover) and (pointer: fine)').matches;

  /* ---------------------------------------------------------------- parallax */
  const px = [...document.querySelectorAll('[data-parallax]')];
  if (px.length && !reduce) {
    let ticking = false;
    const run = () => {
      const vh = innerHeight;
      px.forEach((el) => {
        const r = el.getBoundingClientRect();
        if (r.bottom < -200 || r.top > vh + 200) return;
        const f = parseFloat(el.dataset.parallax) || 0.08;
        el.style.transform = `translate3d(0, ${((r.top + r.height / 2) - vh / 2) * -f}px, 0)`;
      });
      ticking = false;
    };
    addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(run); } }, { passive: true });
    run();
  }

  /* ---------------------------------------------------------------- ripple */
  const ripples = document.querySelectorAll('.fx-ripple');
  if (ripples.length && fine && !reduce) {
    const ns = 'http://www.w3.org/2000/svg';
    const svg = document.createElementNS(ns, 'svg');
    svg.setAttribute('width', '0'); svg.setAttribute('height', '0'); svg.setAttribute('aria-hidden', 'true');
    svg.style.position = 'absolute';
    svg.innerHTML = '<filter id="brz-ripple" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency="0.012 0.04" numOctaves="2" seed="3" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="0" xChannelSelector="R" yChannelSelector="G"/></filter>';
    document.body.appendChild(svg);
    const turb = svg.querySelector('feTurbulence'), disp = svg.querySelector('feDisplacementMap');
    let active = null, amt = 0, target = 0, t = 0, raf = 0;
    const loop = () => {
      amt += (target - amt) * 0.08; t += 0.012;
      turb.setAttribute('baseFrequency', `${0.012 + Math.sin(t) * 0.002} ${0.04 + Math.cos(t * 0.8) * 0.006}`);
      disp.setAttribute('scale', amt.toFixed(2));
      if (target === 0 && amt < 0.15) { if (active) active.style.filter = ''; active = null; raf = 0; return; }
      raf = requestAnimationFrame(loop);
    };
    ripples.forEach((el) => {
      const img = el.querySelector('img'); if (!img) return;
      el.addEventListener('pointerenter', () => { if (active && active !== img) active.style.filter = ''; active = img; img.style.filter = 'url(#brz-ripple)'; target = 14; if (!raf) raf = requestAnimationFrame(loop); });
      el.addEventListener('pointerleave', () => { target = 0; });
    });
  }

  /* ---------------------------------------------------------------- drift */
  if (fine && !reduce) {
    document.querySelectorAll('[data-drift]').forEach((wrap) => {
      wrap.addEventListener('pointermove', (e) => {
        const tile = e.target.closest('a,figure'); if (!tile || !wrap.contains(tile)) return;
        const r = tile.getBoundingClientRect();
        const x = (e.clientX - r.left) / r.width - 0.5, y = (e.clientY - r.top) / r.height - 0.5;
        tile.style.setProperty('--dx', `${(-x * 14).toFixed(1)}px`); tile.style.setProperty('--dy', `${(-y * 14).toFixed(1)}px`);
      });
      wrap.addEventListener('pointerout', (e) => { const tile = e.target.closest('a,figure'); if (tile && !tile.contains(e.relatedTarget)) { tile.style.removeProperty('--dx'); tile.style.removeProperty('--dy'); } });
    });
  }

  /* ---------------------------------------------------------------- liquid slider */
  document.querySelectorAll('[data-liquid]').forEach((root) => {
    const stage = root.querySelector('.lq-stage');
    const imgs = [...stage.querySelectorAll('img')];
    const caps = [...root.querySelectorAll('[data-cap]')];
    const count = root.querySelector('[data-count]');
    const bar = root.querySelector('[data-bar]');
    const n = imgs.length; let idx = 0, busy = false;
    const setUI = (i) => {
      caps.forEach((c, k) => c.classList.toggle('on', k === i));
      if (count) count.textContent = `${String(i + 1).padStart(2, '0')} / ${String(n).padStart(2, '0')}`;
      if (bar) bar.style.transform = `scaleX(${(i + 1) / n})`;
      imgs.forEach((im, k) => im.setAttribute('aria-hidden', String(k !== i)));
    };

    /* fallback: stacked images, crossfade */
    const fallback = () => {
      root.classList.add('lq-fallback');
      imgs.forEach((im, k) => im.classList.toggle('on', k === 0));
      return (i, dir) => { imgs[idx].classList.remove('on'); imgs[i].classList.add('on'); idx = i; setUI(i); };
    };

    let go = null;
    const canvas = document.createElement('canvas');
    const gl = !reduce && (canvas.getContext('webgl', { premultipliedAlpha: false, antialias: false }) || null);
    if (!gl) go = fallback();
    else {
      canvas.className = 'lq-canvas'; canvas.setAttribute('aria-hidden', 'true'); stage.appendChild(canvas);
      const vs = 'attribute vec2 p;varying vec2 v;void main(){v=p*.5+.5;v.y=1.-v.y;gl_Position=vec4(p,0.,1.);}';
      const fs = `precision mediump float;varying vec2 v;uniform sampler2D a,b,d;uniform float t,dir;uniform vec2 ra,rb,rs;
        vec2 cover(vec2 uv,vec2 ri){float s=rs.x/rs.y,i=ri.x/ri.y;vec2 k=s>i?vec2(1.,i/s):vec2(s/i,1.);return (uv-.5)*k+.5;}
        void main(){float m=texture2D(d,v).r;float e=smoothstep(0.,1.,t);
          vec2 o=vec2(dir*.32,.06);
          vec2 ua=cover(v,ra)-o*m*(1.-e);vec2 ub=cover(v,rb)+o*m*e;
          float f=m*.6+(dir>0.?v.x:1.-v.x)*.4;float pe=e*1.4-.2;
          float w=1.-smoothstep(pe-.2,pe+.2,f);
          gl_FragColor=mix(texture2D(b,ub),texture2D(a,ua),w);}`;
      const sh = (type, src) => { const s = gl.createShader(type); gl.shaderSource(s, src); gl.compileShader(s); return s; };
      const prog = gl.createProgram(); gl.attachShader(prog, sh(gl.VERTEX_SHADER, vs)); gl.attachShader(prog, sh(gl.FRAGMENT_SHADER, fs)); gl.linkProgram(prog);
      if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) { canvas.remove(); go = fallback(); }
      else {
        gl.useProgram(prog);
        const buf = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, buf);
        gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]), gl.STATIC_DRAW);
        const loc = gl.getAttribLocation(prog, 'p'); gl.enableVertexAttribArray(loc); gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);
        const U = (k) => gl.getUniformLocation(prog, k);
        const tex = (unit, source) => { const tx = gl.createTexture(); gl.activeTexture(gl.TEXTURE0 + unit); gl.bindTexture(gl.TEXTURE_2D, tx);
          gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
          gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
          if (source) gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, source); return tx; };
        /* procedural displacement map: soft value noise, water-like */
        const dc = document.createElement('canvas'); dc.width = dc.height = 256; const dx = dc.getContext('2d');
        const id = dx.createImageData(256, 256);
        const rnd = (x, y) => { const s = Math.sin(x * 127.1 + y * 311.7) * 43758.5453; return s - Math.floor(s); };
        const noise = (x, y) => { const xi = Math.floor(x), yi = Math.floor(y), xf = x - xi, yf = y - yi; const u = xf * xf * (3 - 2 * xf), w = yf * yf * (3 - 2 * yf);
          return (rnd(xi, yi) * (1 - u) + rnd(xi + 1, yi) * u) * (1 - w) + (rnd(xi, yi + 1) * (1 - u) + rnd(xi + 1, yi + 1) * u) * w; };
        for (let y = 0; y < 256; y++) for (let x = 0; x < 256; x++) { const v = (noise(x / 32, y / 32) * 0.6 + noise(x / 12, y / 12) * 0.3 + noise(x / 5, y / 5) * 0.1) * 255; const o = (y * 256 + x) * 4; id.data[o] = id.data[o + 1] = id.data[o + 2] = v; id.data[o + 3] = 255; }
        dx.putImageData(id, 0, 0);
        const ta = tex(0, null), tb = tex(1, null); tex(2, dc);
        gl.uniform1i(U('a'), 0); gl.uniform1i(U('b'), 1); gl.uniform1i(U('d'), 2);
        const ready = (im) => im.complete && im.naturalWidth ? Promise.resolve(im) : new Promise((ok) => { im.addEventListener('load', () => ok(im), { once: true }); im.addEventListener('error', () => ok(im), { once: true }); if (im.loading === 'lazy') im.loading = 'eager'; });
        const put = (unit, tx, im) => { gl.activeTexture(gl.TEXTURE0 + unit); gl.bindTexture(gl.TEXTURE_2D, tx); try { gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, im); return true; } catch (e) { return false; } };
        let tVal = 0, dirVal = 1;
        const size = () => { const r = stage.getBoundingClientRect(); const dpr = Math.min(devicePixelRatio || 1, 2); canvas.width = Math.round(r.width * dpr); canvas.height = Math.round(r.height * dpr); gl.viewport(0, 0, canvas.width, canvas.height); gl.uniform2f(U('rs'), r.width, r.height); };
        const draw = () => { gl.uniform1f(U('t'), tVal); gl.uniform1f(U('dir'), dirVal); gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4); };
        const aspect = (im) => [im.naturalWidth || 16, im.naturalHeight || 9];
        let ok = true;
        ready(imgs[0]).then((im) => {
          ok = put(0, ta, im) && put(1, tb, im);
          if (!ok) { canvas.remove(); go = fallback(); return; }
          gl.uniform2f(U('ra'), ...aspect(im)); gl.uniform2f(U('rb'), ...aspect(im));
          size(); draw(); root.classList.add('lq-gl');
        });
        addEventListener('resize', () => { if (root.classList.contains('lq-gl')) { size(); draw(); } });
        /* a = incoming, b = outgoing. t: 0 → 1 */
        go = (i, dir) => {
          if (busy || !root.classList.contains('lq-gl')) return;
          busy = true; dirVal = dir;
          Promise.all([ready(imgs[idx]), ready(imgs[i])]).then(([from, to]) => {
            put(1, tb, from); gl.uniform2f(U('rb'), ...aspect(from));
            put(0, ta, to); gl.uniform2f(U('ra'), ...aspect(to));
            const start = performance.now(), dur = 1300;
            const step = (now) => { tVal = Math.min(1, (now - start) / dur); draw(); if (tVal < 1) requestAnimationFrame(step); else { busy = false; } };
            requestAnimationFrame(step); idx = i; setUI(i);
          });
        };
        /* test hook for screenshots: render a mid-transition frame */
        root.__frame = (from, to, t) => Promise.all([ready(imgs[from]), ready(imgs[to])]).then(([f, tt]) => { put(1, tb, f); gl.uniform2f(U('rb'), ...aspect(f)); put(0, ta, tt); gl.uniform2f(U('ra'), ...aspect(tt)); dirVal = 1; tVal = t; draw(); });
      }
    }
    const next = () => go && go((idx + 1) % n, 1);
    const prev = () => go && go((idx - 1 + n) % n, -1);
    root.querySelector('[data-next]')?.addEventListener('click', next);
    root.querySelector('[data-prev]')?.addEventListener('click', prev);
    root.addEventListener('keydown', (e) => { if (e.key === 'ArrowRight') next(); if (e.key === 'ArrowLeft') prev(); });
    let sx = null;
    stage.addEventListener('pointerdown', (e) => { sx = e.clientX; });
    stage.addEventListener('pointerup', (e) => { if (sx === null) return; const d = e.clientX - sx; if (Math.abs(d) > 40) (d < 0 ? next : prev)(); sx = null; });
    setUI(0);
  });

  /* ---------------------------------------------------------------- film strip drag */
  document.querySelectorAll('[data-filmstrip]').forEach((strip) => {
    if (!fine) return;
    let down = false, sx = 0, sl = 0, moved = false;
    strip.addEventListener('pointerdown', (e) => { down = true; moved = false; sx = e.clientX; sl = strip.scrollLeft; strip.classList.add('dragging'); });
    addEventListener('pointerup', () => { down = false; strip.classList.remove('dragging'); });
    strip.addEventListener('pointermove', (e) => { if (!down) return; const d = e.clientX - sx; if (Math.abs(d) > 4) moved = true; strip.scrollLeft = sl - d; });
    strip.addEventListener('click', (e) => { if (moved) { e.preventDefault(); e.stopPropagation(); } }, true);
  });
})();

/* ==========================================================================
   Motion system: kinetic type, reveals, expanding frames, marquee,
   pinned story, slide-mode slideshow. IntersectionObserver + rAF only.
   ========================================================================== */
(() => {
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const small = matchMedia('(max-width: 760px)').matches;

  /* split headings: data-split="words" | "chars" | "lines" (lines = words grouped by rendered line) */
  document.querySelectorAll('[data-split]').forEach((el) => {
    if (reduce) return;
    const mode = el.dataset.split;
    const walk = (node, out) => {
      node.childNodes.forEach((c) => {
        if (c.nodeType === 3) c.textContent.split(/(\s+)/).forEach((w) => { if (w) out.push({ t: w, wrap: null }); });
        else if (c.nodeType === 1) { const tag = c.cloneNode(false); out.push({ t: null, el: tag, kids: walk(c, []) }); }
      });
      return out;
    };
    const tokens = walk(el, []);
    el.textContent = '';
    let i = 0;
    const build = (list, parent) => list.forEach((tk) => {
      if (tk.t !== null) {
        if (/^\s+$/.test(tk.t)) { parent.appendChild(document.createTextNode(' ')); return; }
        const w = document.createElement('span'); w.className = 'sp-w';
        if (mode === 'chars') { [...tk.t].forEach((ch) => { const c = document.createElement('span'); c.className = 'sp-c'; c.textContent = ch; c.style.setProperty('--i', i++); w.appendChild(c); }); }
        else { const inner = document.createElement('span'); inner.className = 'sp-i'; inner.textContent = tk.t; w.style.setProperty('--i', i++); w.appendChild(inner); }
        parent.appendChild(w);
      } else { build(tk.kids, tk.el); parent.appendChild(tk.el); }
    });
    build(tokens, el);
    el.setAttribute('aria-label', el.textContent.replace(/\s+/g, ' ').trim());
    if (mode === 'lines') {           /* group words by their rendered line for line masks */
      const ws = [...el.querySelectorAll('.sp-w')]; let top = null, line = -1;
      ws.forEach((w) => { const t = w.offsetTop; if (t !== top) { top = t; line++; } w.style.setProperty('--i', line); });
    }
    el.classList.add('sp', `sp--${mode}`);
  });

  /* one observer for every reveal */
  const targets = document.querySelectorAll('.sp, [data-reveal], [data-stagger], [data-layered], .u-anim, .rv-arch');
  const show = (el) => el.classList.add('in');
  if ('IntersectionObserver' in window && !reduce) {
    /* clipped elements report no intersection, so masked reveals are observed through their parent */
    const proxy = new Map();
    const io = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) { (proxy.get(e.target) || [e.target]).forEach(show); io.unobserve(e.target); } }), { threshold: 0.15, rootMargin: '0px 0px -6% 0px' });
    targets.forEach((t) => {
      if (t.matches('[data-reveal],[data-layered]')) { const host = t.parentElement; if (!proxy.has(host)) { proxy.set(host, []); io.observe(host); } proxy.get(host).push(t); }
      else io.observe(t);
    });
  } else targets.forEach(show);

  /* scroll-progress driven pieces share one rAF loop */
  const tints = [...document.querySelectorAll('[data-tint]')];
  tints.forEach((p) => { if (reduce) return; p.innerHTML = p.textContent.trim().split(/\s+/).map((w) => `<span class="tw">${w}</span>`).join(' '); });
  const expands = [...document.querySelectorAll('[data-expand]')];
  const stories = [...document.querySelectorAll('[data-story]')];
  if (!reduce && (tints.length || expands.length || stories.length)) {
    let ticking = false;
    const prog = (el, start = 1, end = 0) => { const r = el.getBoundingClientRect(); const vh = innerHeight; return Math.min(1, Math.max(0, (vh * start - r.top) / (r.height + vh * (start - end)))); };
    const run = () => {
      tints.forEach((p) => { const r = p.getBoundingClientRect(); const vh = innerHeight; const k = Math.min(1, Math.max(0, (vh * 0.85 - r.top) / (vh * 0.5))); const ws = p.children; const lit = Math.round(k * ws.length); for (let i = 0; i < ws.length; i++) ws[i].classList.toggle('lit', i < lit); });
      expands.forEach((s) => { const r = s.getBoundingClientRect(); const run = s.offsetHeight - innerHeight; const k = run > 0 ? Math.min(1, Math.max(0, -r.top / run)) : 1; s.style.setProperty('--p', k.toFixed(3)); });
      stories.forEach((s) => {
        const steps = s.querySelectorAll('[data-step]'); const media = s.querySelectorAll('[data-scene]');
        let cur = 0; steps.forEach((st, i) => { const r = st.getBoundingClientRect(); if (r.top < innerHeight * 0.55) cur = i; });
        steps.forEach((st, i) => st.classList.toggle('on', i === cur));
        media.forEach((m, i) => m.classList.toggle('on', i === cur));
        s.dataset.tone = steps[cur]?.dataset.tone || '';
      });
      ticking = false;
    };
    addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(run); } }, { passive: true });
    addEventListener('resize', run); run();
  } else {
    tints.forEach((p) => p.querySelectorAll('.tw').forEach((w) => w.classList.add('lit')));
    /* reduced motion: the photograph still follows the story, only without animated transitions */
    const runS = () => stories.forEach((s) => {
      const steps = s.querySelectorAll('[data-step]'); const media = s.querySelectorAll('[data-scene]');
      let cur = 0; steps.forEach((st, i) => { if (st.getBoundingClientRect().top < innerHeight * 0.55) cur = i; });
      steps.forEach((st, i) => st.classList.toggle('on', i === cur)); media.forEach((m, i) => m.classList.toggle('on', i === cur));
    });
    if (stories.length) { addEventListener('scroll', runS, { passive: true }); runS(); }
  }

  /* slide-mode slideshow (rooms): directional clip-path transitions, swipe, dots */
  document.querySelectorAll('[data-slides]').forEach((root) => {
    const slides = [...root.querySelectorAll('.sl-slide')]; const dots = [...root.querySelectorAll('[data-dot]')];
    const count = root.querySelector('[data-count]'); let idx = 0;
    const set = (i, dir) => {
      i = (i + slides.length) % slides.length; if (i === idx) return;
      const from = slides[idx], to = slides[i];
      to.classList.add('on'); from.classList.remove('on');
      if (!reduce && to.animate) {
        to.animate([{ clipPath: dir > 0 ? 'inset(0 0 0 100%)' : 'inset(0 100% 0 0)' }, { clipPath: 'inset(0 0 0 0)' }], { duration: small ? 650 : 1000, easing: 'cubic-bezier(.77,0,.18,1)' });
        to.querySelector('img')?.animate([{ transform: 'scale(1.12)' }, { transform: 'scale(1)' }], { duration: small ? 900 : 1500, easing: 'cubic-bezier(.22,1,.36,1)' });
      }
      idx = i; dots.forEach((d, k) => d.setAttribute('aria-current', String(k === i)));
      if (count) count.textContent = `${String(i + 1).padStart(2, '0')} / ${String(slides.length).padStart(2, '0')}`;
      slides.forEach((s, k) => s.setAttribute('aria-hidden', String(k !== i)));
    };
    root.querySelector('[data-next]')?.addEventListener('click', () => set(idx + 1, 1));
    root.querySelector('[data-prev]')?.addEventListener('click', () => set(idx - 1, -1));
    dots.forEach((d, k) => d.addEventListener('click', () => set(k, k > idx ? 1 : -1)));
    root.addEventListener('keydown', (e) => { if (e.key === 'ArrowRight') set(idx + 1, 1); if (e.key === 'ArrowLeft') set(idx - 1, -1); });
    let sx = null; root.addEventListener('pointerdown', (e) => { sx = e.clientX; });
    root.addEventListener('pointerup', (e) => { if (sx === null) return; const d = e.clientX - sx; if (Math.abs(d) > 40) set(idx + (d < 0 ? 1 : -1), d < 0 ? 1 : -1); sx = null; });
    slides.forEach((s, k) => s.setAttribute('aria-hidden', String(k !== 0)));
  });

  /* marquee: duplicate content for a seamless loop; pause when off-screen */
  document.querySelectorAll('[data-marquee]').forEach((m) => {
    const track = m.querySelector('.mq-track'); track.innerHTML += track.innerHTML;
    track.querySelectorAll('span').forEach((s, i) => { if (i >= track.children.length / 2) s.setAttribute('aria-hidden', 'true'); });
    if ('IntersectionObserver' in window) new IntersectionObserver(([e]) => m.classList.toggle('run', e.isIntersecting)).observe(m);
  });
})();

/* ==========================================================================
   Pool days: living editorial stack. Three photographs at a time; the
   signature "editorial shuffle" plus a fixed cycle of quieter variations.
   ========================================================================== */
(() => {
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const fine = matchMedia('(hover: hover) and (pointer: fine)').matches;
  document.querySelectorAll('[data-pooldays]').forEach((root) => {
    const stage = root.querySelector('.pd-stage');
    const cards = [...stage.querySelectorAll('.pd-card')];
    const n = cards.length; if (n < 4) return;
    const count = root.querySelector('[data-count]'), cap = root.querySelector('.pd-cap'), prog = root.querySelector('[data-prog]');
    const playBtn = root.querySelector('[data-pause]');
    const INTERVAL = 7000, DUR = reduce ? 0 : 1350;
    const VARIANTS = ['shuffle', 'shuffle', 'cascade', 'shuffle', 'tilt', 'shuffle', 'fade'];
    const small = () => matchMedia('(max-width:760px)').matches;
    /* slot 0 = foreground, 1 = left support, 2 = right support (behind), -1 = waiting behind the stack */
    const SL = {
      0: { x: 6, y: 4, r: -2.5, s: 1, z: 30, o: 1, d: 16 },
      1: { x: -62, y: -6, r: -9, s: 0.72, z: 20, o: 1, d: 9 },
      2: { x: 66, y: -8, r: 7, s: 0.66, z: 10, o: 1, d: 6 },
      '-1': { x: 4, y: -6, r: 2, s: 0.56, z: 1, o: 0, d: 0 },
    };
    const K = () => (small() ? { x: 0.4, y: 0.8, r: 0.5 } : matchMedia('(max-width:1100px)').matches ? { x: 0.8, y: 0.9, r: 0.8 } : { x: 1, y: 1, r: 1 });
    const tf = (p, extra = '') => { const k = K(); return `translate(-50%,-50%) translate(${p.x * k.x}%, ${p.y * k.y}%) rotate(${p.r * k.r}deg) scale(${p.s})${extra}`; };
    const FULL = 'polygon(0% 0%, 100% 0%, 100% 100%, 0% 100%)';
    const DIAG0 = 'polygon(0% 0%, 0% 0%, -40% 100%, 0% 100%)', DIAG1 = 'polygon(0% 0%, 140% 0%, 100% 100%, 0% 100%)';
    let idx = 0, step = 0, busy = false, timer = 0, progA = null, hovering = false, userPaused = reduce, visible = false, entered = false, readyAt = 0;
    const slotOf = (i) => { const r = (idx - i + n) % n; return r === 0 ? 0 : r === 1 ? 1 : r === 2 ? 2 : -1; };
    const set = (c, slot) => { const p = SL[slot]; c.dataset.slot = slot; c.style.transform = tf(p); c.style.opacity = p.o; c.style.zIndex = p.z; c.style.clipPath = FULL; c.style.setProperty('--d', p.d); c.tabIndex = slot === 0 ? 0 : -1; c.setAttribute('aria-hidden', String(slot !== 0)); };
    const layout = () => cards.forEach((c, i) => set(c, slotOf(i)));
    const ui = () => {
      if (count) count.textContent = String(idx + 1).padStart(2, '0');
      if (cap) { cap.classList.add('out'); setTimeout(() => { cap.textContent = cards[idx].dataset.cap || ''; cap.classList.remove('out'); }, reduce ? 0 : 380); }
    };
    const arc = (a, b, lift) => ({ x: (a.x + b.x) / 2, y: (a.y + b.y) / 2 - lift, r: (a.r + b.r) / 2 + (b.r > a.r ? 4 : -4), s: (a.s + b.s) / 2 });

    const move = (c, from, to, variant, delay) => {
      const A = SL[from], B = SL[to];
      const kf = [{ transform: tf(A), opacity: A.o, zIndex: A.z, clipPath: FULL }];
      if (to === 0 && from === -1) {                                  /* incoming: emerges from behind the stack */
        if (variant === 'fade') kf.splice(0, 1, { transform: tf({ ...B, s: 1.06 }), opacity: 0, zIndex: 35, clipPath: FULL });
        else if (variant === 'tilt') kf.splice(0, 1, { transform: tf({ ...B, s: 0.9 }, ' perspective(1200px) rotateY(-38deg)'), opacity: 0, zIndex: 35, clipPath: FULL });
        else if (variant === 'cascade') kf.splice(0, 1, { transform: tf({ ...B, y: B.y - 46, r: B.r + 6, s: 0.92 }), opacity: 0, zIndex: 35, clipPath: FULL });
        else kf.splice(0, 1, { transform: tf({ ...A, s: 0.8 }), opacity: 1, zIndex: 35, clipPath: DIAG0 },
                         { transform: tf({ ...B, s: 0.94, r: B.r - 3 }), opacity: 1, zIndex: 35, clipPath: DIAG1, offset: 0.7 });
      } else if (from === 0 && to === -1) {                           /* reverse: foreground retreats behind */
        kf.push({ transform: tf({ ...A, s: 0.86, r: A.r + 5 }), opacity: 1, zIndex: 35, clipPath: DIAG1, offset: 0.3 },
                { transform: tf({ ...B }), opacity: 0, zIndex: 1, clipPath: DIAG0 });
        return c.animate(kf, { duration: DUR, delay, easing: 'cubic-bezier(.65,0,.25,1)', fill: 'backwards' });
      } else if (from === -1) {                                       /* waiting card slides out into a support slot */
        kf.splice(0, 1, { transform: tf(A), opacity: 0, zIndex: 0, clipPath: FULL });
      } else if (to !== -1) {
        kf.push({ transform: tf(arc(A, B, from === 0 || to === 0 ? 10 : 18)), opacity: 1, zIndex: Math.max(A.z, B.z) - (to === 0 ? 0 : 1), clipPath: FULL, offset: 0.5 });
      }
      kf.push({ transform: tf(B), opacity: B.o, zIndex: B.z, clipPath: FULL });
      return c.animate(kf, { duration: DUR, delay, easing: 'cubic-bezier(.65,0,.25,1)', fill: 'backwards' });
    };

    const go = (dir) => {
      if (busy || !entered) return;
      const before = cards.map((_, i) => slotOf(i));
      idx = (idx + dir + n) % n;
      const variant = dir > 0 ? VARIANTS[step++ % VARIANTS.length] : 'shuffle';
      const after = cards.map((_, i) => slotOf(i));
      layout(); ui();
      if (reduce || !cards[0].animate) return;
      busy = true;
      const anims = [];
      cards.forEach((c, i) => {
        const f = before[i], t = after[i]; if (f === t && f === -1) return;
        const delay = variant === 'cascade' ? (t === 0 ? 260 : t === 1 ? 0 : 120) : 0;
        anims.push(move(c, f, t, variant, delay));
      });
      const done = () => { busy = false; };
      Promise.all(anims.map((a) => a.finished.catch(() => {}))).then(done);
      setTimeout(done, DUR + 700);                                    /* never stuck */
    };

    /* autoplay */
    const stop = () => { clearTimeout(timer); timer = 0; if (progA) { progA.cancel(); progA = null; } };
    const can = () => entered && visible && !hovering && !userPaused && !document.hidden;
    const start = () => {
      stop(); if (!can()) return;
      const wait = Math.max(0, readyAt - Date.now());
      timer = setTimeout(() => {
        if (prog && prog.animate) progA = prog.animate([{ transform: 'scaleX(0)' }, { transform: 'scaleX(1)' }], { duration: INTERVAL, easing: 'linear', fill: 'forwards' });
        timer = setTimeout(() => { go(1); start(); }, INTERVAL);
      }, wait);
    };
    const manual = (dir) => { if (busy) return; go(dir); start(); };
    const setPlay = (paused) => { userPaused = paused; playBtn.setAttribute('aria-pressed', String(paused)); playBtn.setAttribute('aria-label', paused ? 'Play slideshow' : 'Pause slideshow'); paused ? stop() : start(); };

    root.querySelector('[data-next]').addEventListener('click', () => manual(1));
    root.querySelector('[data-prev]').addEventListener('click', () => manual(-1));
    root.querySelector('[data-full]')?.addEventListener('click', () => cards[idx].click());
    playBtn.addEventListener('click', () => setPlay(!userPaused));
    if (reduce) setPlay(true);
    stage.addEventListener('pointerenter', (e) => { if (e.pointerType === 'mouse') { hovering = true; stop(); } });
    stage.addEventListener('pointerleave', (e) => { if (e.pointerType === 'mouse') { hovering = false; root.style.setProperty('--px', 0); root.style.setProperty('--py', 0); start(); } });
    /* keyboard focus pauses; a mouse click on a control does not */
    root.addEventListener('focusin', (e) => { if (e.target.matches(':focus-visible')) { hovering = true; stop(); } });
    root.addEventListener('focusout', (e) => { if (!root.contains(e.relatedTarget)) { hovering = false; start(); } });
    root.addEventListener('keydown', (e) => { if (e.key === 'ArrowRight') manual(1); if (e.key === 'ArrowLeft') manual(-1); });
    document.addEventListener('visibilitychange', () => (document.hidden ? stop() : start()));
    if (fine && !reduce) stage.addEventListener('pointermove', (e) => { const r = stage.getBoundingClientRect(); root.style.setProperty('--px', (((e.clientX - r.left) / r.width) - 0.5).toFixed(3)); root.style.setProperty('--py', (((e.clientY - r.top) / r.height) - 0.5).toFixed(3)); });
    root.style.setProperty('--px', 0); root.style.setProperty('--py', 0);
    stage.querySelectorAll('.pd-mat').forEach((m) => { m.style.transform = 'translate3d(calc(var(--px) * var(--d) * 1px), calc(var(--py) * var(--d) * 1px), 0)'; });

    /* swipe; a tap on a supporting photograph brings the stack round instead of opening the viewer */
    let sx = null, swiped = false;
    stage.addEventListener('pointerdown', (e) => { sx = e.clientX; swiped = false; });
    stage.addEventListener('pointerup', (e) => { if (sx === null) return; const d = e.clientX - sx; if (Math.abs(d) > 40) { swiped = true; manual(d < 0 ? 1 : -1); } sx = null; });
    stage.addEventListener('click', (e) => {
      const c = e.target.closest('.pd-card'); if (!c) return;
      if (swiped) { e.preventDefault(); e.stopPropagation(); swiped = false; return; }
      const s = +c.dataset.slot; if (s > 0) { e.preventDefault(); e.stopPropagation(); manual(s === 1 ? -1 : 1); }
    }, true);

    /* first-time entrance only: POOL days, supports, foreground, controls */
    const enter = () => {
      if (entered) return; entered = true;
      root.classList.add('pd-in');
      layout(); ui();
      if (!reduce && cards[0].animate) {
        cards.forEach((c, i) => {
          const s = slotOf(i); if (s < 0) return; const p = SL[s];
          const delay = s === 2 ? 380 : s === 1 ? 560 : 820;
          const from = s === 0 ? { transform: tf({ ...p, s: 0.86, r: p.r + 4 }), opacity: 1, clipPath: DIAG0 } : { transform: tf({ ...p, x: p.x * 0.3, y: p.y + 10, s: p.s * 0.8 }), opacity: 0, clipPath: FULL };
          c.animate([from, { transform: tf(p), opacity: 1, clipPath: FULL }], { duration: s === 0 ? 1300 : 1100, delay, easing: 'cubic-bezier(.22,1,.36,1)', fill: 'backwards' });
        });
      }
      readyAt = Date.now() + (reduce ? 0 : 1900);
      setTimeout(() => root.classList.add('pd-ready'), reduce ? 0 : 1500);
      start();
    };
    if ('IntersectionObserver' in window) new IntersectionObserver(([e]) => { visible = e.isIntersecting; if (visible) enter(); visible ? start() : stop(); }, { threshold: 0.25 }).observe(root);
    else { visible = true; enter(); }
    addEventListener('resize', () => { if (entered && !busy) layout(); });
  });
})();

/* ==========================================================================
   Meetings & events: configuration selector, hall gallery, outdoor slideshow,
   magnetic buttons, hero spotlight, line drawing. No dependencies.
   ========================================================================== */
(() => {
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const fine = matchMedia('(hover: hover) and (pointer: fine)').matches;

  /* stop the SVG blob morph for reduced motion */
  if (reduce) document.querySelectorAll('#mt2-blob animate').forEach((a) => a.remove());

  /* hero cursor spotlight */
  document.querySelectorAll('[data-spotlight]').forEach((h) => {
    if (!fine || reduce) return;
    h.addEventListener('pointermove', (e) => { const r = h.getBoundingClientRect(); h.style.setProperty('--sx', `${((e.clientX - r.left) / r.width) * 100}%`); h.style.setProperty('--sy', `${((e.clientY - r.top) / r.height) * 100}%`); });
  });

  /* magnetic buttons */
  if (fine && !reduce) document.querySelectorAll('[data-magnetic]').forEach((b) => {
    b.addEventListener('pointermove', (e) => { const r = b.getBoundingClientRect(); b.style.transform = `translate(${((e.clientX - r.left) / r.width - 0.5) * 10}px, ${((e.clientY - r.top) / r.height - 0.5) * 8}px)`; });
    b.addEventListener('pointerleave', () => { b.style.transform = ''; });
  });

  /* ruracio line draws when the section enters */
  document.querySelectorAll('.mt2-rur').forEach((s) => {
    if (!('IntersectionObserver' in window)) { s.classList.add('in-view'); return; }
    const io = new IntersectionObserver(([e]) => { if (e.isIntersecting) { s.classList.add('in-view'); io.disconnect(); } }, { threshold: 0.3 }); io.observe(s);
  });

  /* hall gallery (crossfade) */
  document.querySelectorAll('[data-spaces]').forEach((root) => {
    const f = [...root.querySelectorAll('.mt2-sp')]; const c = root.querySelector('[data-count]'); let i = 0;
    const show = (k) => { i = (k + f.length) % f.length; f.forEach((x, j) => x.classList.toggle('on', j === i)); if (c) c.textContent = `${String(i + 1).padStart(2, '0')} / ${String(f.length).padStart(2, '0')}`; };
    root.querySelector('[data-next]').addEventListener('click', () => show(i + 1));
    root.querySelector('[data-prev]').addEventListener('click', () => show(i - 1));
    root.addEventListener('keydown', (e) => { if (e.key === 'ArrowRight') show(i + 1); if (e.key === 'ArrowLeft') show(i - 1); });
    let sx = null; root.addEventListener('pointerdown', (e) => { sx = e.clientX; }); root.addEventListener('pointerup', (e) => { if (sx !== null && Math.abs(e.clientX - sx) > 40) show(i + (e.clientX < sx ? 1 : -1)); sx = null; });
  });

  /* configuration selector: mask transition, heading/description swap, enquiry preset */
  document.querySelectorAll('[data-config]').forEach((root) => {
    const tabs = [...root.querySelectorAll('[role=tab]')]; const imgs = [...root.querySelectorAll('.mt2-cf-img')];
    const title = root.querySelector('.mt2-cf-title'), desc = root.querySelector('.mt2-cf-desc'), cta = root.querySelector('[data-setup]');
    let cur = 0, busy = false;
    const pick = (k) => {
      if (k === cur || busy) return; const dir = k > cur ? 1 : -1; const from = imgs[cur], to = imgs[k]; busy = true;
      tabs.forEach((t, j) => { t.setAttribute('aria-selected', String(j === k)); t.tabIndex = j === k ? 0 : -1; });
      to.classList.add('on');
      const done = () => { from.classList.remove('on'); busy = false; };
      if (reduce || !to.animate) { done(); }
      else {
        to.style.zIndex = 2;
        const a = to.animate([{ clipPath: `circle(0% at ${dir > 0 ? '85% 50%' : '15% 50%'})` }, { clipPath: `circle(150% at ${dir > 0 ? '85% 50%' : '15% 50%'})` }], { duration: 1100, easing: 'cubic-bezier(.77,0,.18,1)' });
        to.querySelector('img').animate([{ transform: 'scale(1.15)' }, { transform: 'scale(1)' }], { duration: 1400, easing: 'cubic-bezier(.22,1,.36,1)' });
        from.querySelector('img').animate([{ transform: 'scale(1)' }, { transform: 'scale(.94)' }], { duration: 1100, easing: 'cubic-bezier(.65,0,.25,1)', fill: 'forwards' }).onfinish = function () { this.cancel(); };
        a.onfinish = () => { to.style.zIndex = ''; done(); }; setTimeout(() => { if (busy) done(); }, 1500);
        [title, desc].forEach((el, n) => el.animate([{ opacity: 1, transform: 'none' }, { opacity: 0, transform: 'translateY(10px)' }, { opacity: 1, transform: 'none' }], { duration: 900, delay: n * 80, easing: 'cubic-bezier(.22,1,.36,1)' }));
      }
      setTimeout(() => { title.textContent = tabs[k].dataset.title; desc.textContent = tabs[k].dataset.desc; cta.dataset.setup = tabs[k].dataset.title; }, reduce ? 0 : 420);
      cur = k;
    };
    tabs.forEach((t, j) => { t.addEventListener('click', () => pick(j)); t.tabIndex = j === 0 ? 0 : -1; });
    root.querySelector('[role=tablist]').addEventListener('keydown', (e) => { if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') { const k = (cur + (e.key === 'ArrowRight' ? 1 : -1) + tabs.length) % tabs.length; pick(k); tabs[k].focus(); } });
    cta.addEventListener('click', () => { const sel = document.querySelector('form[data-form=event] [name=setup]'); if (sel) sel.value = cta.dataset.setup; });
  });

  /* outdoor slideshow: 7 s, diagonal reveal, progress, pause, swipe, keyboard */
  document.querySelectorAll('[data-outdoor]').forEach((root) => {
    const s = [...root.querySelectorAll('.mt2-os')]; const n = s.length;
    const count = root.querySelector('[data-count]'), cap = root.querySelector('.mt2-os-cap'), prog = root.querySelector('[data-prog]'), play = root.querySelector('[data-play]');
    let i = 0, t = 0, pa = null, paused = reduce, hover = false, vis = false, busy = false;
    const show = (k, dir = 1) => {
      if (busy) return; k = (k + n) % n; if (k === i) return; const from = s[i], to = s[k]; busy = true;
      to.classList.add('on');
      if (!reduce && to.animate) {
        to.style.zIndex = 2;
        const a = to.animate([{ clipPath: dir > 0 ? 'polygon(100% 0,100% 0,140% 100%,100% 100%)' : 'polygon(0 0,0 0,-40% 100%,0 100%)' }, { clipPath: 'polygon(-40% 0,100% 0,140% 100%,0 100%)' }], { duration: 1300, easing: 'cubic-bezier(.77,0,.18,1)' });
        a.onfinish = () => { to.style.zIndex = ''; from.classList.remove('on'); busy = false; };
      } else { from.classList.remove('on'); busy = false; }
      setTimeout(() => { busy = false; }, 1700);
      i = k; count.textContent = String(i + 1).padStart(2, '0');
      cap.style.opacity = 0; setTimeout(() => { cap.textContent = s[i].dataset.cap; cap.style.opacity = 1; }, reduce ? 0 : 400);
    };
    const stop = () => { clearTimeout(t); if (pa) { pa.cancel(); pa = null; } };
    const start = () => { stop(); if (paused || hover || !vis || document.hidden) return; if (prog.animate) pa = prog.animate([{ transform: 'scaleX(0)' }, { transform: 'scaleX(1)' }], { duration: 7000, easing: 'linear', fill: 'forwards' }); t = setTimeout(() => { show(i + 1, 1); start(); }, 7000); };
    const man = (d) => { show(i + d, d); start(); };
    root.querySelector('[data-next]').addEventListener('click', () => man(1));
    root.querySelector('[data-prev]').addEventListener('click', () => man(-1));
    play.addEventListener('click', () => { paused = !paused; play.setAttribute('aria-pressed', String(paused)); play.setAttribute('aria-label', paused ? 'Play slideshow' : 'Pause slideshow'); play.textContent = paused ? '▶' : '❚❚'; paused ? stop() : start(); });
    if (reduce) { play.setAttribute('aria-pressed', 'true'); play.textContent = '▶'; }
    root.addEventListener('pointerenter', (e) => { if (e.pointerType === 'mouse') { hover = true; stop(); } });
    root.addEventListener('pointerleave', (e) => { if (e.pointerType === 'mouse') { hover = false; start(); } });
    root.addEventListener('keydown', (e) => { if (e.key === 'ArrowRight') man(1); if (e.key === 'ArrowLeft') man(-1); });
    document.addEventListener('visibilitychange', () => (document.hidden ? stop() : start()));
    let sx = null; root.addEventListener('pointerdown', (e) => { if (e.target.closest('button')) return; sx = e.clientX; });
    root.addEventListener('pointerup', (e) => { if (sx !== null && Math.abs(e.clientX - sx) > 40) man(e.clientX < sx ? 1 : -1); sx = null; });
    if ('IntersectionObserver' in window) new IntersectionObserver(([e]) => { vis = e.isIntersecting; vis ? start() : stop(); }, { threshold: 0.35 }).observe(root); else { vis = true; start(); }
  });
})();


/* Location map: the Breez marker label sits on the hotel's coordinates; once the
   visitor starts moving the map (focus enters the iframe) the label steps aside. */
(() => {
  const maps = document.querySelectorAll('[data-map]'); if (!maps.length) return;
  addEventListener('blur', () => setTimeout(() => { maps.forEach((m) => { if (m.contains(document.activeElement)) m.classList.add('moved'); }); }, 0));
})();

/* ==========================================================================
   HOMEPAGE PHOTOGRAPHIC BEHAVIOUR (after Casa Angelina). Active only where the
   homepage markup opts in, so no other page is affected.
   - [data-pan="f"]   the photograph moves gently inside its unchanged frame
                      (f = share of frame height; negative = opposite way, for
                      accents); a slight overscan keeps edges covered
   - [data-hero-pan]  hero photograph drifts down and settles larger as the
                      hero scrolls away, so it hands over to the next section
   - [data-welcome]   the art of welcome: the lower photograph is uncovered
                      upwards as it arrives; the writings travel with the
                      visitor and settle onto its upper part; the arch caption
                      moves from "The exterior" to "The arrival"
   All scroll-linked, reversible, rAF-throttled; nothing locks or hijacks the
   scroll. Reduced motion: still photographs, writings in their place.
   ========================================================================== */
(() => {
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const small = () => innerWidth <= 760;
  const cl = (v) => Math.max(0, Math.min(1, v));
  const io = (t) => t < .5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
  const pans = [...document.querySelectorAll('[data-pan]')].map((el) => ({ el, f: parseFloat(el.dataset.pan) || 0, img: el.querySelector('img') })).filter((p) => p.img);
  pans.forEach((p) => { p.img.style.scale = String(1 + Math.abs(p.f) * 2.2); });
  const hero = document.querySelector('[data-hero-pan]'), heroImg = hero && hero.querySelector('img');
  const wel = document.querySelector('[data-welcome]');
  let W = null;
  if (wel) {
    const copy = wel.querySelector('.ed-k-copy'), ph = wel.querySelector('.ed-k-ph'), labels = wel.querySelectorAll('.ed-xp-prog span'), prog = wel.querySelector('.ed-xp-prog');
    W = { copy, ph, labels, prog, D: 0 };
    const measure = () => { W.copy.style.translate = ''; W.D = small() ? 0 : Math.max(0, W.ph.offsetTop - W.copy.offsetTop - W.copy.offsetHeight * 0.05); };
    measure(); addEventListener('resize', measure);
  }
  let raf = 0;
  const draw = () => {
    raf = 0; const vh = innerHeight, k = small() ? 0.55 : 1;
    pans.forEach(({ el, f, img }) => {
      const r = el.getBoundingClientRect(); if (r.bottom < -100 || r.top > vh + 100) return;
      const c = Math.max(-1, Math.min(1, (r.top + r.height / 2 - vh / 2) / (vh / 2 + r.height / 2)));
      img.style.translate = `0 ${(-c * f * 100 * k).toFixed(2)}%`;
    });
    if (heroImg) {
      const r = hero.getBoundingClientRect(), t = cl(-r.top / Math.max(1, r.height));
      heroImg.style.translate = `0 ${(t * 18 * k).toFixed(2)}%`; heroImg.style.scale = String(1 + t * 0.06);
    }
    if (W) {
      const r = W.ph.getBoundingClientRect();
      const rev = io(cl((vh * 1.02 - r.top) / (r.height * 0.95)));            // lower photograph uncovered upwards
      W.ph.style.clipPath = `inset(${((1 - rev) * 100).toFixed(2)}% 0 0 0)`;
      const q = small() ? 0 : io(cl((vh * 0.78 - r.top) / (vh * 0.5)));       // writings settle onto it
      W.copy.style.translate = `0 ${(q * W.D).toFixed(1)}px`;
      W.copy.style.setProperty('--q', q.toFixed(3)); W.ph.style.setProperty('--q', q.toFixed(3));
      W.prog.style.setProperty('--pp', (rev * 0.5 + q * 0.5).toFixed(3));
      W.labels[0].classList.toggle('on', q < 0.5); W.labels[1].classList.toggle('on', q >= 0.5);
    }
  };
  const req = () => { if (!raf) raf = requestAnimationFrame(draw); };
  addEventListener('scroll', req, { passive: true }); addEventListener('resize', req); draw();
})();

/* The many moods: captions read light while they travel over the anchored
   band, dark once they are on the ivory below. */
(() => {
  const mm = document.querySelector('[data-mm]'); if (!mm) return;
  const band = mm.querySelector('.mm-band'), tiles = [...mm.querySelectorAll('.mm-t')];
  let raf = 0;
  const run = () => { raf = 0; const b = band.getBoundingClientRect().bottom;
    tiles.forEach((t) => { const c = t.querySelector('.mm-cap').getBoundingClientRect(); t.classList.toggle('on-band', c.top + c.height * 0.4 < b && getComputedStyle(band).position === 'sticky'); }); };
  addEventListener('scroll', () => { if (!raf) raf = requestAnimationFrame(run); }, { passive: true }); addEventListener('resize', run); run();
})();

/* The many moods: "The Breez is a place to ..." rotating word (one at a time,
   fixed line box so nothing shifts; pauses off-screen; static if reduced motion). */
(() => {
  const box = document.querySelector('[data-words]'); if (!box) return;
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const w = [...box.children]; let i = 0, t = 0, vis = false;
  const step = () => { const cur = w[i]; i = (i + 1) % w.length; cur.classList.remove('on'); cur.classList.add('out'); w[i].classList.remove('out'); w[i].classList.add('on'); setTimeout(() => cur.classList.remove('out'), 1100); };
  const run = () => { clearInterval(t); if (vis && !document.hidden) t = setInterval(step, 2600); };
  new IntersectionObserver(([en]) => { vis = en.isIntersecting; run(); }, { threshold: 0.3 }).observe(box);
  document.addEventListener('visibilitychange', run);
})();

/* Breez signature: draw-on when the section arrives; a very small sideways drift with scroll */
(function(){
  var sec=document.querySelector('[data-sig]'); if(!sec) return;
  var reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if(reduce || !('IntersectionObserver' in window)){ sec.classList.add('in'); return; }
  new IntersectionObserver(function(es,o){ es.forEach(function(e){ if(e.isIntersecting){ sec.classList.add('in'); o.disconnect(); } }); },{threshold:.22}).observe(sec);
  var tick=false;
  function upd(){ tick=false; var r=sec.getBoundingClientRect(), vh=innerHeight; var p=(vh-r.top)/(vh+r.height); p=Math.max(0,Math.min(1,p)); sec.style.setProperty('--sp',p.toFixed(3)); }
  addEventListener('scroll',function(){ if(!tick){ tick=true; requestAnimationFrame(upd);} },{passive:true}); upd();
  /* safety: never leave it hidden if the observer is throttled */
  addEventListener('scroll',function chk(){ var r=sec.getBoundingClientRect(); if(r.top<innerHeight*.8){ sec.classList.add('in'); removeEventListener('scroll',chk); } },{passive:true});
})();

/* Rooms opening: full-screen photographs cross-fading about every six seconds, with the room list, counter and dots.
   Pauses while the controls are hovered, on keyboard focus, a hidden tab or when scrolled away; manual choices restart the timer. */
(function () {
  const root = document.querySelector('[data-rh]'); if (!root) return;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const stage = root;
  const slides = [...root.querySelectorAll('.rh-slide')], n = slides.length; if (n < 2) return;
  const dots = [...root.querySelectorAll('[data-rh-dot]')], tabs = [...root.querySelectorAll('[data-rh-go]')];
  const nums = [...root.querySelectorAll('[data-rh-num]')], note = root.querySelector('[data-rh-note]');
  const live = root.querySelector('[data-rh-live]'), play = root.querySelector('[data-rh-play]');
  const DUR = 5800;                                        // about six seconds a slide
  let i = 0, t = 0, paused = reduce, hover = false, focus = false, vis = false, busy = false;

  const ready = (k) => { const im = slides[k].querySelector('img'); if (!im) return Promise.resolve();
    im.loading = 'eager'; return (im.complete ? Promise.resolve() : new Promise((r) => { im.addEventListener('load', r, { once: true }); im.addEventListener('error', r, { once: true }); }))
      .then(() => (im.decode ? im.decode().catch(() => {}) : 0)); };
  const set = (list, k, cls = 'on') => list.forEach((el, j) => { el.classList.toggle(cls, j === k); if (el.hasAttribute('aria-hidden') || j !== k) el.setAttribute('aria-hidden', String(j !== k)); });

  async function show(k, user) {
    k = (k + n) % n; if (k === i || busy) return;
    busy = true; await ready(k); busy = false;            // never fade towards an unloaded photo
    i = k; const d = slides[k].dataset;
    set(slides, k);
    dots.forEach((b, j) => { b.classList.toggle('on', j === k); b.setAttribute('aria-current', String(j === k)); });
    tabs.forEach((b) => { const on = +b.dataset.rhGo === k; b.classList.toggle('on', on); b.setAttribute('aria-pressed', String(on)); });
    nums.forEach((el) => { el.textContent = String(k + 1).padStart(2, '0'); });
    note.innerHTML = d.note;
    if (user) live.textContent = `Slide ${k + 1} of ${n}: ${d.title}`;
    ready((k + 1) % n);                                    // have the next one waiting
  }
  const stop = () => { clearTimeout(t); root.classList.remove('rh-run'); };
  const start = () => {
    stop(); if (paused || hover || focus || !vis || document.hidden) return;
    void root.offsetWidth; root.classList.add('rh-run');   // restart the progress line
    t = setTimeout(() => show(i + 1).then(start), DUR);
  };
  const go = (k) => show(k, true).then(start);

  root.querySelector('[data-rh-next]').addEventListener('click', () => go(i + 1));
  root.querySelector('[data-rh-prev]').addEventListener('click', () => go(i - 1));
  dots.forEach((b) => b.addEventListener('click', () => go(+b.dataset.rhDot)));
  tabs.forEach((b) => b.addEventListener('click', () => go(+b.dataset.rhGo)));
  const syncPlay = () => { play.setAttribute('aria-pressed', String(paused)); play.setAttribute('aria-label', paused ? 'Play slideshow' : 'Pause slideshow'); };
  play.addEventListener('click', () => { paused = !paused; syncPlay(); paused ? stop() : start(); });
  syncPlay();
  stage.addEventListener('keydown', (e) => { if (e.key === 'ArrowRight') { e.preventDefault(); go(i + 1); } if (e.key === 'ArrowLeft') { e.preventDefault(); go(i - 1); } });
  const ctl = root.querySelector('.rp-ctl');                // hovering the controls holds the slide; the photo keeps playing
  ctl.addEventListener('pointerenter', (e) => { if (e.pointerType === 'mouse') { hover = true; stop(); } });
  ctl.addEventListener('pointerleave', (e) => { if (e.pointerType === 'mouse') { hover = false; start(); } });
  stage.addEventListener('focusin', (e) => { if (e.target.matches(':focus-visible')) { focus = true; stop(); } });
  stage.addEventListener('focusout', (e) => { if (!stage.contains(e.relatedTarget)) { focus = false; start(); } });
  const photo = root.querySelector('.rp-hero-in'); let sx = null;
  photo.addEventListener('pointerdown', (e) => { sx = e.clientX; });
  photo.addEventListener('pointerup', (e) => { if (sx !== null && Math.abs(e.clientX - sx) > 40) go(e.clientX < sx ? i + 1 : i - 1); sx = null; });
  document.addEventListener('visibilitychange', () => (document.hidden ? stop() : start()));
  if ('IntersectionObserver' in window) new IntersectionObserver(([e]) => { vis = e.isIntersecting; vis ? start() : stop(); }, { threshold: 0.35 }).observe(stage);
  else { vis = true; start(); }
  ready(1);
})();

/* Meetings & events opening, after the Casa Angelina recording. While the page sits at the top, the hero photographs
   cross-fade under the script title. As the visitor scrolls, the stage stays on screen (position: sticky, scrolling is
   never taken over) and one progress value p, 0 to 1 across the section, choreographs the scene: the title fades, the
   photograph shrinks out of the full frame towards the right and settles into .me-slot as a wide image, the panoramic
   strip slides in from the left edge and the four lines open around them. Each part has its own window of p and its
   own easing, so nothing moves in lockstep. With reduced motion the scene switches between its two states. */
(function () {
  const hero = document.querySelector('[data-me-hero]'); if (!hero) return;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const stage = hero.querySelector('.me-stage'), win = hero.querySelector('.me-hero-win'), slot = hero.querySelector('.me-slot');
  const slides = [...hero.querySelectorAll('.me-hs')];
  const clamp = (v) => Math.min(1, Math.max(0, v));
  const seg = (p, a, b) => clamp((p - a) / (b - a));
  const inOut = (t) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);
  const out = (t) => 1 - Math.pow(1 - t, 3);
  const lerp = (a, b, t) => a + (b - a) * t;
  let i = 0, timer = 0, ticking = false, atTop = true, W = 0, H = 0, S = null;

  /* the film at the top of the page */
  const loadImg = (k) => { const im = slides[k].querySelector('img'); im.loading = 'eager'; return im.complete ? Promise.resolve() : new Promise((r) => { im.onload = im.onerror = r; }); };
  const show = (k) => loadImg(k).then(() => {
    if (k === i) return;
    slides[i].classList.remove('on'); slides[i].setAttribute('aria-hidden', 'true');
    slides[k].classList.add('on', 'run'); slides[k].removeAttribute('aria-hidden');
    const old = slides[i]; setTimeout(() => old.classList.remove('run'), 2400); i = k; });
  const play = () => { clearInterval(timer); if (!reduce && atTop && !document.hidden && slides.length > 1) timer = setInterval(() => show((i + 1) % slides.length), 6500); };
  if (slides.length > 1) { slides[0].classList.add('run'); loadImg(1); play(); document.addEventListener('visibilitychange', play); }

  /* the scroll-driven scene */
  const measure = () => { W = stage.clientWidth; H = stage.clientHeight; S = { x: slot.offsetLeft, y: slot.offsetTop, w: slot.offsetWidth, h: slot.offsetHeight }; };
  const set = (n, v) => hero.style.setProperty(n, v);
  const frame = () => {
    ticking = false; if (!S) return;
    const r = hero.getBoundingClientRect(), travel = hero.offsetHeight - stage.offsetHeight;
    let p = travel > 0 ? clamp(-r.top / travel) : 0;
    if (reduce) p = p > 0.3 ? 1 : 0;
    // the photograph: its left edge and bottom lead, the right edge holds and then tucks in, the top follows,
    // so it draws away towards the right and then lifts into its place
    const kl = out(seg(p, 0.03, 0.5)), kb = inOut(seg(p, 0.03, 0.58)), kt = inOut(seg(p, 0.1, 0.62)), kr = inOut(seg(p, 0.26, 0.62));
    const x0 = lerp(0, S.x, kl), x1 = lerp(W, S.x + S.w, kr), y0 = lerp(0, S.y, kt), y1 = lerp(H, S.y + S.h, kb);
    win.style.setProperty('--bx', x0.toFixed(1) + 'px'); win.style.setProperty('--by', y0.toFixed(1) + 'px');
    win.style.setProperty('--bw', (x1 - x0).toFixed(1) + 'px'); win.style.setProperty('--bh', (y1 - y0).toFixed(1) + 'px');
    set('--o', (1 - seg(p, 0, 0.14)).toFixed(3));
    set('--k', inOut(seg(p, 0.03, 0.62)).toFixed(4));
    set('--s', out(seg(p, 0.26, 0.72)).toFixed(4));
    set('--wa', out(seg(p, 0.4, 0.72)).toFixed(4));
    set('--wb', out(seg(p, 0.5, 0.8)).toFixed(4));
    set('--wc', out(seg(p, 0.55, 0.84)).toFixed(4));
    set('--wd', out(seg(p, 0.42, 0.84)).toFixed(4));
    hero.classList.toggle('is-set', p > 0.2);
    // the film plays only at the top; once the scene starts it settles back on the hall, which is what moves into place
    const top = p < 0.015 && r.bottom > 0;
    if (top !== atTop) { atTop = top; if (atTop) play(); else { clearInterval(timer); show(0); } }
  };
  const req = () => { if (!ticking) { ticking = true; requestAnimationFrame(frame); } };
  addEventListener('scroll', req, { passive: true });
  addEventListener('resize', () => { measure(); frame(); });
  measure(); frame();
})();

/* Gallery, the garden: photographs standing on the inside of a curve, after the supplied reference. The viewer sits
   between the curve's centre and its far wall, so the photographs nearer the edges turn towards the eye and grow.
   One position s (in photographs) drives it: it drifts slowly while on screen, follows a drag or swipe, and the
   arrow keys step it. Cards are re-used round the ring, so the strip never ends. Reduced motion: no drift. */
(function () {
  const view = document.querySelector('[data-curve]'); if (!view) return;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const cards = [...view.querySelectorAll('.gc-card')], n = cards.length; if (!n) return;
  let s = 0, target = null, vis = false, last = 0, drag = null, W = 0, R = 0, step = 0;
  const measure = () => {
    W = cards[0].offsetWidth;
    R = Math.max(view.clientWidth * 0.95, W * 4);                       // radius of the curve
    view.style.setProperty('--gc-p', Math.round(R * 0.52) + 'px');      // the eye: a little behind the curve's centre
    step = 2 * Math.atan((W * 0.56) / R);                               // radians between photographs
  };
  const place = () => {
    cards.forEach((c, i) => {
      let k = ((i - s) % n + n) % n; if (k > n / 2) k -= n;              // position relative to the centre, -n/2..n/2
      const th = k * step, deg = th * 180 / Math.PI;
      const fade = Math.max(0, Math.min(1, (0.95 - Math.abs(th)) / 0.22));   // fade out before the edge of sight
      c.style.transform = `translateZ(${R.toFixed(0)}px) rotateY(${(-deg).toFixed(3)}deg) translateZ(${(-R).toFixed(0)}px)`;
      c.style.opacity = fade.toFixed(3); c.style.visibility = fade > 0 ? 'visible' : 'hidden';
      c.setAttribute('aria-hidden', String(Math.abs(k) > 0.5));
    });
  };
  const tick = (t) => {
    if (!vis) { last = 0; return; }
    const dt = last ? Math.min(0.05, (t - last) / 1000) : 0; last = t;
    if (target !== null) { s += (target - s) * Math.min(1, dt * 6); if (Math.abs(target - s) < 0.002) { s = target; target = null; } }
    else if (!drag && !reduce) s += dt * 0.12;                           // about one photograph every eight seconds
    place(); requestAnimationFrame(tick);
  };
  const start = () => { if (vis) { last = 0; requestAnimationFrame(tick); } };
  view.addEventListener('pointerdown', (e) => { drag = { x: e.clientX, s }; target = null; view.setPointerCapture(e.pointerId); });
  view.addEventListener('pointermove', (e) => { if (drag) { s = drag.s - (e.clientX - drag.x) / (W * 1.1); if (reduce) place(); } });
  const end = () => { if (drag) { target = Math.round(s); drag = null; if (reduce) { s = target; target = null; place(); } } };
  view.addEventListener('pointerup', end); view.addEventListener('pointercancel', end);
  view.addEventListener('keydown', (e) => {
    if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return; e.preventDefault();
    target = Math.round(target ?? s) + (e.key === 'ArrowRight' ? 1 : -1);
    if (reduce) { s = target; target = null; place(); }
  });
  addEventListener('resize', () => { measure(); place(); });
  measure(); place();
  if ('IntersectionObserver' in window) new IntersectionObserver(([e]) => { const was = vis; vis = e.isIntersecting; if (vis && !was) start(); }).observe(view);
  else { vis = true; start(); }
})();

/* Rooms, below the opening: entrances that play once. Each element waits just out of place (a little lower, or a
   little to its own side for data-glide="l"/"r") and settles when it comes into view; photographs open from their
   lower edge while easing from 1.025 to their own scale. Elements arriving together are staggered in reading
   order, so a section unfolds as a sequence rather than all at once. Once shown, an element stays shown.
   No JavaScript, no IntersectionObserver or reduced motion: everything is simply visible. */
(function () {
  const root = document.querySelector('main:has(.rp-hero)'); if (!root) return;
  if (!('IntersectionObserver' in window) || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const sections = [...root.querySelectorAll(':scope > section:not(.rp-hero)')];
  const els = [];
  sections.forEach((sec) => {
    sec.querySelectorAll('[data-glide], .rp-ph, .rp-n, .rp-frame, .rp-p-frame, .rp-a-frame, .rp-vert, .rp-port-note, .rp-close-foot').forEach((el) => {
      if (el.closest('[data-glide]') && el.closest('[data-glide]') !== el && !el.matches('.rp-ph')) return;   // moves with its parent
      el.classList.add(el.matches('.rp-ph') ? 'rv-img' : 'rv-el'); els.push(el);
    });
  });
  const show = (batch) => {
    batch.sort((a, b) => (a.compareDocumentPosition(b) & Node.DOCUMENT_POSITION_FOLLOWING ? -1 : 1));
    batch.forEach((el, i) => { el.style.setProperty('--rd', Math.min(i * 110, 660) + 'ms'); el.classList.add('rv-in'); });
  };
  const io = new IntersectionObserver((entries) => {
    const batch = entries.filter((e) => e.isIntersecting).map((e) => e.target);
    batch.forEach((el) => io.unobserve(el));
    if (batch.length) show(batch);
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
  els.forEach((el) => io.observe(el));
  // anything the visitor has already scrolled past (a jump link, a fast flick) is shown at once
  let t = 0;
  addEventListener('scroll', () => { clearTimeout(t); t = setTimeout(() => {
    const past = els.filter((el) => !el.classList.contains('rv-in') && el.getBoundingClientRect().bottom < 0);
    past.forEach((el) => { io.unobserve(el); el.style.setProperty('--rd', '0ms'); el.classList.add('rv-in'); });
  }, 120); }, { passive: true });
})();

/* Gallery, the archive: every photograph played as a living exhibition in the homepage mosaic's format (rows of three
   on a dark band, column spans 5-3-4, 3-4-5, 4-5-3, 5-3-4). The frames stay where they are; the photographs in them
   change. Each category keeps its own shuffled queue, so no photograph returns until all of that category's have
   appeared, and none shows in two frames at once. A change waits until the incoming photograph has loaded and
   decoded, then dissolves over the outgoing one, which stays until it is covered. One frame changes at a time, in a
   reshuffled order, so the mosaic is always quietly moving. Choosing a category fills the frames with that
   category's photographs, frame by frame, and carries on with it; a small category uses fewer frames, its last row
   widened to the full measure. Playback pauses off screen and in a hidden tab and resumes where it was. */
(function () {
  const gx = document.querySelector('[data-gx]'); if (!gx) return;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  let all = []; try { all = JSON.parse(gx.querySelector('[data-gx-list]').textContent); } catch (e) { return; }
  const frames = [...gx.querySelectorAll('.gx-f')];
  const SPANS = frames.map((f) => +getComputedStyle(f).getPropertyValue('--s') || 4);
  const bar = document.querySelector('[data-filters="grid"]');
  const STEP = 1150;   // one frame every 1.15 s: with twelve frames, each holds its photograph for about 14 s
  let cat = 'all', order = [], timer = 0, vis = false;
  const queues = {};
  const pool = (c) => (c === 'all' ? all : all.filter((x) => x.c === c));
  const shuffle = (a) => { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
  const active = () => frames.filter((f) => !f.hidden);
  const showing = () => active().map((f) => (f.querySelector('img:last-child') || {}).dataset?.k);
  const nextItem = (c) => {
    const q = queues[c] || (queues[c] = { list: [], last: null });
    const busyKeys = showing();
    for (let tries = 0; tries < 2; tries++) {
      if (!q.list.length) { q.list = shuffle(pool(c)); if (q.list.length > 1 && q.list[0].s === q.last) q.list.push(q.list.shift()); }
      const i = q.list.findIndex((x) => !busyKeys.includes(x.s));
      if (i >= 0) { const [it] = q.list.splice(i, 1); q.last = it.s; return it; }
      if (pool(c).length <= busyKeys.filter(Boolean).length) return null;   // every photograph of the category is already up
      q.list = [];
    }
    return null;
  };
  const load = (it) => new Promise((res) => {
    const im = new Image(); im.alt = it.a; im.dataset.k = it.s; im.decoding = 'async';
    im.onload = () => (im.decode ? im.decode().catch(() => {}) : Promise.resolve()).then(() => res(im));
    im.onerror = () => res(null);
    im.src = `${it.s}-800.webp`;
  });
  const put = (f, im) => {
    const old = [...f.querySelectorAll('img')];
    f.appendChild(im); void im.offsetWidth; im.classList.add('on');
    setTimeout(() => old.forEach((o) => o.remove()), 1900);   // the outgoing photograph stays until it is covered
  };
  const swap = async (f, c) => {
    if (f.dataset.busy) return; f.dataset.busy = '1';
    let im = null;
    for (let tries = 0; tries < 3 && !im; tries++) { const it = nextItem(c); if (!it) break; im = await load(it); }
    if (im && c === cat && !f.hidden) put(f, im);
    delete f.dataset.busy;
  };
  const tick = () => {
    const fs = active(); if (!fs.length) return;
    if (!order.length) order = shuffle(fs);
    swap(order.shift(), cat);
  };
  const play = () => { clearInterval(timer); if (!reduce && vis && !document.hidden) timer = setInterval(tick, STEP); };
  const layout = (n) => {   // the first n frames, rows of three on the reference spans; a short last row is widened
    frames.forEach((f, i) => { f.hidden = i >= n; f.style.setProperty('--s', SPANS[i]); });
    const rem = n % 3, start = n - rem;
    if (rem === 1) frames[start].style.setProperty('--s', 12);
    if (rem === 2) { frames[start].style.setProperty('--s', 7); frames[start + 1].style.setProperty('--s', 5); }
    gx.dataset.n = String(n);
  };
  const warm = (c) => {
    const q = queues[c] || (queues[c] = { list: [], last: null });
    if (!q.list.length) q.list = shuffle(pool(c));
    q.list.slice(0, 6).forEach((it) => { const im = new Image(); im.src = `${it.s}-800.webp`; });
  };
  const setCat = (c) => {
    if (c === cat) return; cat = c; clearInterval(timer); order = [];
    const n = Math.min(frames.length, pool(c).length);
    const fs = frames.slice(0, n);
    fs.forEach((f) => { f.querySelectorAll('img').forEach((im) => { im.dataset.k = ''; }); });   // the previous category no longer counts as showing
    const t0 = performance.now();
    const picks = fs.map(() => nextItem(c));
    let laid = false;
    fs.forEach((f, i) => {
      const it = picks[i]; if (!it) return;
      load(it).then((im) => {
        if (!im || c !== cat) return;
        setTimeout(() => {
          if (c !== cat) return;
          if (!laid) { layout(n); laid = true; }
          put(f, im);
        }, Math.max(0, i * 110 - (performance.now() - t0)));
      });
    });
    play();
  };
  if (bar) {
    bar.addEventListener('click', (e) => { const b = e.target.closest('button[data-filter]'); if (b) setCat(b.dataset.filter); });
    ['pointerover', 'focusin'].forEach((ev) => bar.addEventListener(ev, (e) => { const b = e.target.closest('button[data-filter]'); if (b && b.dataset.filter !== cat) warm(b.dataset.filter); }));
  }
  document.addEventListener('visibilitychange', play);
  new IntersectionObserver(([e]) => { vis = e.isIntersecting; play(); }, { threshold: 0.15 }).observe(gx);
})();
