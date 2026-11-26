/* Small shared behaviours: scroll reveal, lightbox, booking nights, menus. No dependencies. */
(() => {
  // Reveal on scroll
  const els = document.querySelectorAll('.reveal, .reveal-mask');
  if ('IntersectionObserver' in window && els.length) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e) => { if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); } });
    }, { threshold: 0.15 });
    els.forEach((el) => io.observe(el));
  } else { els.forEach((el) => el.classList.add('is-in')); }

  // Booking forms: validate dates, count nights
  document.querySelectorAll('[data-booking]').forEach((form) => {
    const inEl = form.querySelector('[name=checkin]');
    const outEl = form.querySelector('[name=checkout]');
    const msg = form.querySelector('[data-nights]');
    if (!inEl || !outEl) return;
    const today = new Date(); today.setHours(0, 0, 0, 0);
    const iso = (d) => d.toISOString().slice(0, 10);
    inEl.min = iso(today);
    const update = () => {
      if (inEl.value) {
        const next = new Date(inEl.value); next.setDate(next.getDate() + 1);
        outEl.min = iso(next);
        if (outEl.value && outEl.value <= inEl.value) outEl.value = iso(next);
      }
      if (msg) {
        if (inEl.value && outEl.value) {
          const n = Math.round((new Date(outEl.value) - new Date(inEl.value)) / 86400000);
          msg.textContent = n > 0 ? `${n} night${n > 1 ? 's' : ''} · request only — we confirm availability and rate` : 'Check-out must be after check-in';
        } else { msg.textContent = 'Choose your dates — this sends a booking request, not a confirmed booking'; }
      }
    };
    inEl.addEventListener('change', update); outEl.addEventListener('change', update); update();
    form.addEventListener('submit', (ev) => {
      ev.preventDefault();
      if (!form.reportValidity()) return;
      const ref = 'BRZ-' + Math.random().toString(36).slice(2, 7).toUpperCase();
      if (msg) msg.textContent = `Demo only: request ${ref} would be sent to reservations. Nothing has been booked.`;
    });
  });

  // Mobile / fullscreen menus
  document.querySelectorAll('[data-menu-toggle]').forEach((btn) => {
    const target = document.getElementById(btn.getAttribute('aria-controls'));
    if (!target) return;
    btn.addEventListener('click', () => {
      const open = btn.getAttribute('aria-expanded') === 'true';
      btn.setAttribute('aria-expanded', String(!open));
      target.toggleAttribute('data-open', !open);
      document.body.style.overflow = open ? '' : 'hidden';
    });
    target.querySelectorAll('a').forEach((a) => a.addEventListener('click', () => {
      btn.setAttribute('aria-expanded', 'false'); target.removeAttribute('data-open'); document.body.style.overflow = '';
    }));
  });

  // Lightbox for any [data-lightbox] container of links to images
  const groups = document.querySelectorAll('[data-lightbox]');
  if (groups.length) {
    const box = document.createElement('div');
    box.className = 'lb'; box.setAttribute('role', 'dialog'); box.setAttribute('aria-modal', 'true'); box.hidden = true;
    box.innerHTML = '<button class="lb-close" aria-label="Close">×</button><button class="lb-prev" aria-label="Previous">‹</button><figure><img alt=""><figcaption></figcaption></figure><button class="lb-next" aria-label="Next">›</button>';
    document.body.appendChild(box);
    const st = document.createElement('style');
    st.textContent = '.lb{position:fixed;inset:0;z-index:1000;background:rgba(20,15,10,.94);display:grid;grid-template-columns:56px 1fr 56px;align-items:center}.lb[hidden]{display:none}.lb figure{margin:0;display:grid;gap:10px;justify-items:center;padding:16px}.lb img{max-height:80vh;width:auto;max-width:100%}.lb figcaption{color:#efe6d6;font:14px/1.4 Karla,sans-serif;text-align:center}.lb button{background:none;border:0;color:#fff;font-size:40px;min-height:56px;cursor:pointer}.lb-close{position:absolute;top:8px;right:12px}';
    document.head.appendChild(st);
    let items = [], idx = 0;
    const img = box.querySelector('img'), cap = box.querySelector('figcaption');
    const show = (i) => { idx = (i + items.length) % items.length; const a = items[idx]; img.src = a.getAttribute('href'); img.alt = a.dataset.alt || ''; cap.textContent = a.dataset.caption || ''; };
    const close = () => { box.hidden = true; document.body.style.overflow = ''; };
    groups.forEach((g) => g.addEventListener('click', (ev) => {
      const a = ev.target.closest('a[href]'); if (!a || !g.contains(a)) return;
      ev.preventDefault(); items = [...g.querySelectorAll('a[href]')].filter((x) => x.offsetParent !== null); show(items.indexOf(a)); box.hidden = false; document.body.style.overflow = 'hidden'; box.querySelector('.lb-close').focus();
    }));
    box.querySelector('.lb-close').onclick = close;
    box.querySelector('.lb-prev').onclick = () => show(idx - 1);
    box.querySelector('.lb-next').onclick = () => show(idx + 1);
    box.addEventListener('click', (ev) => { if (ev.target === box) close(); });
    box.addEventListener('keydown', (ev) => { if (ev.key === 'Escape') close(); if (ev.key === 'ArrowLeft') show(idx - 1); if (ev.key === 'ArrowRight') show(idx + 1); });
  }

  // Gallery filters
  document.querySelectorAll('[data-filters]').forEach((bar) => {
    const grid = document.getElementById(bar.dataset.filters);
    bar.addEventListener('click', (ev) => {
      const b = ev.target.closest('button[data-filter]'); if (!b) return;
      bar.querySelectorAll('button').forEach((x) => x.setAttribute('aria-pressed', String(x === b)));
      const f = b.dataset.filter;
      grid.querySelectorAll('[data-cat]').forEach((it) => { it.hidden = !(f === 'all' || it.dataset.cat === f); });
    });
  });
})();
