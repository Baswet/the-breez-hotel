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
    stories.forEach((s) => { s.querySelectorAll('[data-scene]').forEach((m, i) => m.classList.toggle('on', i === 0)); });
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
