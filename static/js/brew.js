/* Brew Ritual - Main JS */

(function () {
  'use strict';

  // ── Custom Cursor ────────────────────────────────────────
  const cursor = document.getElementById('brew-cursor');
  const cursorDot = document.getElementById('brew-cursor-dot');
  const cursorTrail = document.getElementById('brew-cursor-trail');
  let mx = -200, my = -200, tx = -200, ty = -200;

  if (cursor && window.matchMedia('(pointer:fine)').matches) {
    document.addEventListener('mousemove', e => {
      mx = e.clientX; my = e.clientY;
      cursor.style.left = mx + 'px';
      cursor.style.top  = my + 'px';
      cursorDot.style.left = mx + 'px';
      cursorDot.style.top  = my + 'px';
    });

    function animTrail() {
      tx += (mx - tx) * 0.14;
      ty += (my - ty) * 0.14;
      cursorTrail.style.left = tx + 'px';
      cursorTrail.style.top  = ty + 'px';
      requestAnimationFrame(animTrail);
    }
    animTrail();

    document.querySelectorAll('a, button, [role="button"], .machine-card, .tab-btn, .filter-btn, .item-card').forEach(el => {
      el.addEventListener('mouseenter', () => { cursor.classList.add('hovering'); cursorTrail.classList.add('hovering'); });
      el.addEventListener('mouseleave', () => { cursor.classList.remove('hovering'); cursorTrail.classList.remove('hovering'); });
    });
    document.addEventListener('mousedown', () => cursor.classList.add('clicking'));
    document.addEventListener('mouseup',   () => cursor.classList.remove('clicking'));
  }

  // ── Navigation scroll state ──────────────────────────────
  const nav = document.getElementById('mainNav');
  if (nav) {
    const onScroll = () => nav.classList.toggle('scrolled', window.scrollY > 40);
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  // ── Mobile nav toggle ────────────────────────────────────
  const toggle = document.getElementById('navToggle');
  const links  = document.getElementById('navLinks');
  if (toggle && links) {
    toggle.addEventListener('click', () => {
      const open = links.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open);
    });
  }

  // ── Reveal on scroll ────────────────────────────────────
  const revealEls = document.querySelectorAll('.reveal');
  if (revealEls.length) {
    const io = new IntersectionObserver(entries => {
      entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in-view'); io.unobserve(e.target); } });
    }, { threshold: 0.12 });
    revealEls.forEach(el => io.observe(el));
  }

  // ── Auto-dismiss messages ────────────────────────────────
  document.querySelectorAll('[data-auto-dismiss]').forEach(msg => {
    setTimeout(() => msg.style.opacity = '0', 4500);
    setTimeout(() => msg.remove(), 5000);
    msg.querySelector('.message-close')?.addEventListener('click', () => msg.remove());
  });

  // ── Hero floating beans ──────────────────────────────────
  const heroBg = document.getElementById('heroBgArt');
  if (heroBg) {
    const beanSVG = () => `<svg viewBox="0 0 40 28" fill="none" xmlns="http://www.w3.org/2000/svg"><ellipse cx="20" cy="14" rx="18" ry="12" fill="#C8954A"/><path d="M20 2 Q24 8 20 14 Q16 20 20 26" stroke="#1C0F0A" stroke-width="2.2" fill="none" stroke-linecap="round"/></svg>`;
    for (let i = 0; i < 14; i++) {
      const b = document.createElement('div');
      b.className = 'bean';
      const size = 24 + Math.random() * 36;
      b.style.cssText = `width:${size}px;height:${size * 0.7}px;left:${Math.random()*100}%;animation-duration:${14+Math.random()*22}s;animation-delay:-${Math.random()*20}s;`;
      b.innerHTML = beanSVG();
      heroBg.appendChild(b);
    }
  }

  // ── Cart quantity controls ───────────────────────────────
  document.querySelectorAll('.qty-control').forEach(ctrl => {
    const minus = ctrl.querySelector('[data-qty-minus]');
    const plus  = ctrl.querySelector('[data-qty-plus]');
    const val   = ctrl.querySelector('.qty-val');
    const input = ctrl.closest('form')?.querySelector('input[name="quantity"]');
    if (!minus || !plus || !val) return;
    minus.addEventListener('click', () => {
      let v = parseInt(val.textContent) - 1;
      if (v < 1) v = 1;
      val.textContent = v;
      if (input) input.value = v;
    });
    plus.addEventListener('click', () => {
      let v = parseInt(val.textContent) + 1;
      val.textContent = v;
      if (input) input.value = v;
    });
  });

  // ── Add to cart AJAX ─────────────────────────────────────
  document.querySelectorAll('.add-to-cart-form').forEach(form => {
    form.addEventListener('submit', async e => {
      e.preventDefault();
      const btn = form.querySelector('[type="submit"]');
      const orig = btn.textContent;
      btn.disabled = true;
      btn.textContent = 'Adding...';
      try {
        const res = await fetch(form.action, {
          method: 'POST',
          headers: { 'X-Requested-With': 'XMLHttpRequest', 'X-CSRFToken': getCookie('csrftoken') },
          body: new FormData(form),
        });
        const data = await res.json();
        if (data.success) {
          btn.textContent = 'Added!';
          btn.style.background = 'var(--sage)';
          document.querySelectorAll('.nav-cart-count').forEach(el => { el.textContent = data.cart_count; el.style.display = 'flex'; });
          showToast(data.message);
        }
      } catch (_) { btn.textContent = orig; }
      setTimeout(() => { btn.textContent = orig; btn.disabled = false; btn.style.background = ''; }, 2000);
    });
  });

  function showToast(msg) {
    const t = document.createElement('div');
    t.className = 'message';
    t.innerHTML = `<span class="message-text">${msg}</span><button class="message-close">&times;</button>`;
    t.style.cssText = 'opacity:0;transition:opacity .3s;';
    let c = document.querySelector('.messages-container');
    if (!c) { c = document.createElement('div'); c.className = 'messages-container'; document.body.appendChild(c); }
    c.appendChild(t);
    requestAnimationFrame(() => t.style.opacity = '1');
    setTimeout(() => { t.style.opacity = '0'; setTimeout(() => t.remove(), 400); }, 3500);
    t.querySelector('.message-close').addEventListener('click', () => t.remove());
  }

  function getCookie(name) {
    const v = document.cookie.match('(^|;) ?' + name + '=([^;]*)(;|$)');
    return v ? v[2] : null;
  }

  // ── Size selector price update ───────────────────────────
  document.querySelectorAll('.size-opt').forEach(radio => {
    radio.addEventListener('change', function () {
      const price = this.dataset.price;
      const display = document.getElementById('current-price');
      if (display && price) display.textContent = '$' + price;
    });
  });

  // ── Ritual Guide Machine + Recipe explorer ───────────────
  const machineCards = document.querySelectorAll('.machine-card[data-machine]');
  const tabsWrap     = document.getElementById('coffeeTabsWrap');
  const recipeInfo   = document.getElementById('recipeInfo');
  const glassWrap    = document.getElementById('glassWrap');
  const legendWrap   = document.getElementById('ingredientsLegend');
  const glassPanel   = document.getElementById('glassPanel');

  if (machineCards.length && window.RITUAL_DATA) {
    machineCards.forEach(card => {
      card.addEventListener('click', () => {
        machineCards.forEach(c => c.classList.remove('active'));
        card.classList.add('active');
        const mid = card.dataset.machine;
        renderTabs(mid);
        if (tabsWrap) tabsWrap.scrollIntoView({ behavior: 'smooth', block: 'start' });
      });
    });
  }

  function renderTabs(machineId) {
    if (!tabsWrap) return;
    const machine = window.RITUAL_DATA?.machines?.find(m => m.id === machineId);
    if (!machine) return;
    const tabs = document.getElementById('coffeeTabs');
    if (!tabs) return;
    tabs.innerHTML = '';
    machine.coffees.forEach((key, i) => {
      const recipe = window.RITUAL_DATA.recipes[key];
      if (!recipe) return;
      const btn = document.createElement('button');
      btn.className = 'tab-btn' + (i === 0 ? ' active' : '');
      btn.textContent = recipe.name;
      btn.addEventListener('click', () => {
        tabs.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        renderRecipe(key);
      });
      tabs.appendChild(btn);
    });
    renderRecipe(machine.coffees[0]);
  }

  function renderRecipe(key) {
    if (!recipeInfo) return;
    const recipe = window.RITUAL_DATA?.recipes?.[key];
    if (!recipe) return;
    if (glassPanel) glassPanel.style.display = 'flex';
    recipeInfo.innerHTML = `
      <span class="compat-badge"><span class="compat-dot"></span>${recipe.machine.join(', ')}</span>
      <h2 class="detail-title">${recipe.name}</h2>
      <p class="detail-tagline mono" style="color:var(--crema)">${recipe.origin}</p>
      <p class="detail-desc">${recipe.desc}</p>
      <div class="recipe-stats-row">
        <div class="recipe-stat"><span class="recipe-stat-value">${recipe.volume}</span><span class="recipe-stat-label">Volume</span></div>
        <div class="recipe-stat"><span class="recipe-stat-value">${recipe.time}</span><span class="recipe-stat-label">Brew Time</span></div>
        <div class="recipe-stat"><span class="recipe-stat-value">${recipe.temp}</span><span class="recipe-stat-label">Temperature</span></div>
        <div class="recipe-stat"><span class="recipe-stat-value">${recipe.grind}</span><span class="recipe-stat-label">Grind</span></div>
      </div>
      <p class="recipe-steps-label">Method</p>
      <ol class="recipe-steps-list">${recipe.steps.map((s, i) => `<li class="step-item" style="transition-delay:${i*0.08}s"><span class="step-num">${i+1}</span><span class="step-text">${s}</span></li>`).join('')}</ol>
    `;
    setTimeout(() => recipeInfo.querySelectorAll('.step-item').forEach(el => el.classList.add('vis')), 80);
    if (glassWrap) glassWrap.innerHTML = buildGlassSVG(recipe);
    if (legendWrap) {
      legendWrap.innerHTML = recipe.layers.map(l =>
        `<div class="legend-item"><div class="legend-swatch" style="background:${l.colorSwatch}"></div><span class="legend-name">${l.name}</span><span class="legend-amount">${l.pct}%</span></div>`
      ).join('');
    }
  }

  function buildGlassSVG(recipe) {
    const W = 200, H = 280, gx = 30, gy = 30, gw = 140, gh = 210;
    let layers = recipe.layers;
    let defs = `<defs>
      <clipPath id="glassClip"><path d="M${gx+8},${gy} L${gx},${gy+gh} Q${gx},${gy+gh+8} ${gx+8},${gy+gh+8} L${gx+gw-8},${gy+gh+8} Q${gx+gw},${gy+gh+8} ${gx+gw},${gy+gh} L${gx+gw-8},${gy} Z"/></clipPath>
    </defs>`;
    let fills = '';
    let cumPct = 0;
    layers.slice().reverse().forEach(l => {
      const fillH = (l.pct / 100) * gh;
      const yStart = gy + gh - cumPct / 100 * gh - fillH;
      fills += `<rect x="${gx}" y="${yStart}" width="${gw}" height="${fillH + 2}" fill="${l.color}" clip-path="url(#glassClip)">
        <animate attributeName="height" from="0" to="${fillH + 2}" dur="0.7s" begin="${cumPct * 0.012}s" fill="freeze"/>
        <animate attributeName="y" from="${gy+gh}" to="${yStart}" dur="0.7s" begin="${cumPct * 0.012}s" fill="freeze"/>
      </rect>`;
      cumPct += l.pct;
    });
    const ripple = `<path d="M${gx},${gy+4} Q${gx+gw/2},${gy} ${gx+gw},${gy+4}" stroke="rgba(255,255,255,0.15)" stroke-width="1.5" fill="none">
      <animateTransform attributeName="transform" type="translate" values="0,0;0,3;0,0" dur="2.5s" repeatCount="indefinite"/>
    </path>`;
    const glass = `<path d="M${gx+8},${gy} L${gx},${gy+gh} Q${gx},${gy+gh+8} ${gx+8},${gy+gh+8} L${gx+gw-8},${gy+gh+8} Q${gx+gw},${gy+gh+8} ${gx+gw},${gy+gh} L${gx+gw-8},${gy} Z" stroke="rgba(200,149,74,0.5)" stroke-width="1.5" fill="none"/>`;
    const handle = recipe.hasSaucer ? `<ellipse cx="${W/2}" cy="${gy+gh+14}" rx="${gw/2+8}" ry="5" fill="rgba(200,149,74,0.15)" stroke="rgba(200,149,74,0.3)" stroke-width="1"/>` : '';
    return `<svg viewBox="0 0 ${W} ${H+20}" xmlns="http://www.w3.org/2000/svg" style="max-width:200px">${defs}${fills}${glass}${ripple}${handle}</svg>`;
  }

  // ── Stamp card animation ─────────────────────────────────
  document.querySelectorAll('.progress-fill[data-pct]').forEach(el => {
    const pct = el.dataset.pct;
    setTimeout(() => el.style.width = pct + '%', 300);
  });

})();
