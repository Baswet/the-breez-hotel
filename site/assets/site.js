/* The Breez Hotel — site behaviour. No dependencies. */
(() => {
  document.documentElement.classList.add('js');
  const WA = '254707461665';
  const EMAIL = 'thebreezhotel@gmail.com';

  /* header shadow on scroll */
  const hdr = document.querySelector('.hdr');
  const onScroll = () => hdr && hdr.classList.toggle('scrolled', window.scrollY > 24);
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();

  /* reveal */
  const rv = document.querySelectorAll('.rv, .rv-mask');
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }), { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    rv.forEach((el) => io.observe(el));
  } else rv.forEach((el) => el.classList.add('in'));

  /* menu overlay */
  const ov = document.getElementById('menu');
  const openBtn = document.querySelector('[data-open-menu]');
  const setMenu = (open) => {
    if (!ov) return;
    ov.classList.toggle('open', open); ov.setAttribute('aria-hidden', String(!open));
    if (openBtn) openBtn.setAttribute('aria-expanded', String(open));
    document.body.style.overflow = open ? 'hidden' : '';
    if (open) setTimeout(() => ov.querySelector('.ov-close').focus(), 60); else if (openBtn) openBtn.focus();
  };
  if (openBtn) openBtn.addEventListener('click', () => setMenu(true));
  if (ov) {
    ov.querySelector('.ov-close').addEventListener('click', () => setMenu(false));
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && ov.classList.contains('open')) setMenu(false); });
  }

  /* dates helpers */
  const iso = (d) => { const z = new Date(d.getTime() - d.getTimezoneOffset() * 60000); return z.toISOString().slice(0, 10); };
  const nice = (s) => s ? new Date(s + 'T12:00:00').toLocaleDateString('en-GB', { weekday: 'short', day: 'numeric', month: 'short', year: 'numeric' }) : '';
  const ref = () => 'BRZ-' + new Date().toISOString().slice(2, 10).replace(/-/g, '') + '-' + Math.random().toString(36).slice(2, 6).toUpperCase();

  /* forms: [data-form="booking"|"event"|"contact"|"quick"] */
  document.querySelectorAll('form[data-form]').forEach((form) => {
    const type = form.dataset.form;
    const inEl = form.querySelector('[name=checkin]');
    const outEl = form.querySelector('[name=checkout]');
    const nightsEl = form.querySelector('[data-nights]');
    const today = new Date(); today.setHours(0, 0, 0, 0);
    if (inEl) inEl.min = iso(today);
    const params = new URLSearchParams(location.search);
    form.querySelectorAll('input,select,textarea').forEach((f) => { if (f.name && params.get(f.name)) f.value = params.get(f.name); });
    const upd = () => {
      if (!inEl || !outEl) return;
      if (inEl.value) {
        const n = new Date(inEl.value + 'T12:00:00'); n.setDate(n.getDate() + 1);
        outEl.min = iso(n);
        if (outEl.value && outEl.value <= inEl.value) outEl.value = iso(n);
      }
      if (nightsEl) {
        const n = inEl.value && outEl.value ? Math.round((new Date(outEl.value) - new Date(inEl.value)) / 864e5) : 0;
        nightsEl.textContent = n > 0 ? `${n} night${n > 1 ? 's' : ''}` : '—';
      }
      form.querySelectorAll('[data-show]').forEach((el) => { const f = form.querySelector(`[name=${el.dataset.show}]`); if (f) el.textContent = f.value ? (f.type === 'date' ? nice(f.value) : f.value) : '—'; });
    };
    form.addEventListener('input', upd); form.addEventListener('change', upd); upd();

    form.addEventListener('submit', (ev) => {
      ev.preventDefault();
      if (type === 'quick') {               // homepage strip → hand over to the full booking page
        const q = new URLSearchParams(new FormData(form)); location.href = form.action + '?' + q.toString(); return;
      }
      if (!form.reportValidity()) return;
      const fd = new FormData(form); const r = ref();
      const title = { booking: 'Room booking request', event: 'Meeting / event enquiry', contact: 'Website message' }[type] || 'Enquiry';
      const lines = [`${title} — ${r}`, ''];
      form.querySelectorAll('[name]').forEach((f) => {
        if (!f.name || f.type === 'hidden' || f.name === 'channel' || !fd.get(f.name)) return;
        const lab = (f.closest('label') && f.closest('label').dataset.label) || f.name;
        lines.push(`${lab}: ${f.type === 'date' ? nice(fd.get(f.name)) : fd.get(f.name)}`);
      });
      if (inEl && outEl && inEl.value && outEl.value) lines.push(`Nights: ${Math.round((new Date(outEl.value) - new Date(inEl.value)) / 864e5)}`);
      lines.push('', 'Sent from The Breez Hotel website. Please confirm availability and rate.');
      const text = lines.join('\n');
      const channel = (fd.get('channel') || 'whatsapp');
      const wa = `https://wa.me/${WA}?text=${encodeURIComponent(text)}`;
      const mail = `mailto:${EMAIL}?subject=${encodeURIComponent(title + ' ' + r)}&body=${encodeURIComponent(text)}`;
      const box = form.parentElement.querySelector('.form-status');
      if (box) {
        box.querySelector('[data-ref]').textContent = r;
        box.querySelector('[data-wa]').href = wa;
        box.querySelector('[data-mail]').href = mail;
        box.classList.add('show'); box.setAttribute('tabindex', '-1'); box.focus();
      }
      window.open(channel === 'email' ? mail : wa, channel === 'email' ? '_self' : '_blank', 'noopener');
    });
  });

  /* horizontal strip controls */
  document.querySelectorAll('[data-strip]').forEach((ctl) => {
    const strip = document.getElementById(ctl.dataset.strip);
    ctl.querySelectorAll('button').forEach((b) => b.addEventListener('click', () => strip.scrollBy({ left: (b.dataset.dir === 'next' ? 1 : -1) * strip.clientWidth * 0.8, behavior: 'smooth' })));
  });

  /* sticky story (pools) */
  const ss = document.querySelector('.ss-media');
  if (ss && 'IntersectionObserver' in window) {
    const media = ss.querySelectorAll('.ph');
    const io2 = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) { const i = +e.target.dataset.step; media.forEach((m, k) => m.classList.toggle('on', k === i)); } }), { rootMargin: '-45% 0px -45% 0px' });
    document.querySelectorAll('.ss-step').forEach((s) => io2.observe(s));
  }

  /* gallery filters */
  document.querySelectorAll('[data-filters]').forEach((bar) => {
    const grid = document.getElementById(bar.dataset.filters);
    bar.addEventListener('click', (ev) => {
      const b = ev.target.closest('button[data-filter]'); if (!b) return;
      bar.querySelectorAll('button').forEach((x) => x.setAttribute('aria-pressed', String(x === b)));
      const f = b.dataset.filter;
      grid.querySelectorAll('[data-cat]').forEach((it) => { it.hidden = !(f === 'all' || it.dataset.cat === f); });
    });
  });

  /* lightbox */
  const groups = document.querySelectorAll('[data-lightbox]');
  if (groups.length) {
    const box = document.createElement('div');
    box.className = 'lb'; box.hidden = true; box.setAttribute('role', 'dialog'); box.setAttribute('aria-modal', 'true'); box.setAttribute('aria-label', 'Photo viewer');
    box.innerHTML = '<span class="lb-n"></span><button class="lb-p" aria-label="Previous photo">‹</button><figure><img alt=""><figcaption></figcaption></figure><button class="lb-nx" aria-label="Next photo">›</button><button class="lb-x" aria-label="Close">×</button>';
    document.body.appendChild(box);
    let items = [], idx = 0, last = null;
    const img = box.querySelector('img'), cap = box.querySelector('figcaption'), num = box.querySelector('.lb-n');
    const still = matchMedia('(prefers-reduced-motion: reduce)').matches;
    const show = (i, dir = 0) => {
      idx = (i + items.length) % items.length; const a = items[idx];
      img.src = a.getAttribute('href'); img.alt = a.dataset.alt || ''; cap.textContent = a.dataset.caption || ''; num.textContent = `${idx + 1} / ${items.length}`;
      if (!still && img.animate) img.animate(dir ? [{ opacity: 0, transform: `translateX(${dir * 70}px) scale(.985)`, clipPath: dir > 0 ? 'inset(0 0 0 30%)' : 'inset(0 30% 0 0)' }, { opacity: 1, transform: 'none', clipPath: 'inset(0 0 0 0)' }] : [{ opacity: 0, transform: 'scale(.97)' }, { opacity: 1, transform: 'none' }], { duration: 650, easing: 'cubic-bezier(.22,1,.36,1)' });
    };
    const close = () => { box.hidden = true; document.body.style.overflow = ''; if (last) last.focus(); };
    groups.forEach((g) => g.addEventListener('click', (ev) => {
      const a = ev.target.closest('a[href]'); if (!a || !g.contains(a)) return;
      ev.preventDefault(); last = a; items = [...g.querySelectorAll('a[href]')].filter((x) => !x.hidden);
      show(items.indexOf(a)); box.hidden = false; document.body.style.overflow = 'hidden'; box.querySelector('.lb-x').focus();
    }));
    box.querySelector('.lb-x').onclick = close;
    box.querySelector('.lb-p').onclick = () => show(idx - 1, -1);
    box.querySelector('.lb-nx').onclick = () => show(idx + 1, 1);
    let tx = null; box.addEventListener('touchstart', (e) => { tx = e.touches[0].clientX; }, { passive: true }); box.addEventListener('touchend', (e) => { if (tx === null) return; const d = e.changedTouches[0].clientX - tx; if (Math.abs(d) > 50) show(idx + (d < 0 ? 1 : -1), d < 0 ? 1 : -1); tx = null; });
    box.addEventListener('click', (e) => { if (e.target === box) close(); });
    document.addEventListener('keydown', (e) => { if (box.hidden) return; if (e.key === 'Escape') close(); if (e.key === 'ArrowLeft') show(idx - 1, -1); if (e.key === 'ArrowRight') show(idx + 1, 1); });
  }


  /* rooms hero: image index swaps the main photograph on hover/focus */
  document.querySelectorAll('[data-index]').forEach((list) => {
    const main = document.querySelector('.hx-rooms-media .main img');
    if (!main) return;
    const links = list.querySelectorAll('a[data-swap]');
    const show = (a) => {
      links.forEach((x) => x.classList.toggle('on', x === a));
      const base = a.dataset.swap;
      if (main.dataset.base === base) return;
      main.style.opacity = '0';
      setTimeout(() => { main.srcset = `${base}-800.webp 800w, ${base}-1600.webp 1600w`; main.src = `${base}-1600.webp`; main.alt = a.dataset.alt || ''; main.dataset.base = base; main.onload = () => { main.style.opacity = '1'; }; }, 180);
    };
    links.forEach((a) => { a.addEventListener('mouseenter', () => show(a)); a.addEventListener('focus', () => show(a)); });
  });

  /* year */
  document.querySelectorAll('[data-year]').forEach((el) => { el.textContent = new Date().getFullYear(); });
})();
