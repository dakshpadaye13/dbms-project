/* ============================================================
   EduQuest — Premium Animation Engine v3
   ADDITIVE ONLY — Safe to load after main.js
   Libraries loaded from CDN at runtime.
   ============================================================ */

(function () {
  'use strict';

  /* ─────────────────────────────────────────────────────────────
     0. GUARD — Don't run during the intro video
     ───────────────────────────────────────────────────────────*/
  function isIntroPlaying() {
    const screen = document.getElementById('intro-video-screen');
    return screen && !screen.classList.contains('fade-out') && screen.style.display !== 'none';
  }

  /* ─────────────────────────────────────────────────────────────
     1. INJECT CDN SCRIPTS (Lenis + GSAP + ScrollTrigger + VanillaTilt)
     ───────────────────────────────────────────────────────────*/
  function loadScript(src, onload) {
    const s = document.createElement('script');
    s.src = src;
    s.async = true;
    if (onload) s.onload = onload;
    document.head.appendChild(s);
  }

  /* ─────────────────────────────────────────────────────────────
     2. CUSTOM CURSOR
     ───────────────────────────────────────────────────────────*/
  function initCursor() {
    // Skip on touch devices
    if (window.matchMedia('(hover:none)').matches) return;

    const dot  = document.createElement('div');
    dot.id     = 'eq-cursor-dot';
    const ring = document.createElement('div');
    ring.id    = 'eq-cursor-ring';
    document.body.appendChild(dot);
    document.body.appendChild(ring);

    let mouseX = 0, mouseY = 0;
    let ringX  = 0, ringY  = 0;

    document.addEventListener('mousemove', e => {
      mouseX = e.clientX;
      mouseY = e.clientY;
      dot.style.left = mouseX + 'px';
      dot.style.top  = mouseY + 'px';
    }, { passive: true });

    // Smooth ring follow via rAF
    function animateRing() {
      ringX += (mouseX - ringX) * 0.13;
      ringY += (mouseY - ringY) * 0.13;
      ring.style.left = ringX + 'px';
      ring.style.top  = ringY + 'px';
      requestAnimationFrame(animateRing);
    }
    animateRing();

    // Expand on hover over interactive elements
    const hoverSel = 'a, button, .btn, .game-card, .glass-card, .nav-link, input, textarea, [role="button"]';
    document.querySelectorAll(hoverSel).forEach(el => {
      el.addEventListener('mouseenter', () => document.body.classList.add('cursor-hover'),    { passive: true });
      el.addEventListener('mouseleave', () => document.body.classList.remove('cursor-hover'), { passive: true });
    });

    // Hide cursor when it leaves the window
    document.addEventListener('mouseleave', () => { dot.style.opacity = '0'; ring.style.opacity = '0'; }, { passive: true });
    document.addEventListener('mouseenter', () => { dot.style.opacity = '1'; ring.style.opacity = '1'; }, { passive: true });
  }

  /* ─────────────────────────────────────────────────────────────
     3. BUTTON MOUSE-TRACK (ripple gradient follows cursor)
     ───────────────────────────────────────────────────────────*/
  function initButtonFX() {
    document.querySelectorAll('.btn').forEach(btn => {
      btn.addEventListener('mousemove', e => {
        const r = btn.getBoundingClientRect();
        const x = ((e.clientX - r.left) / r.width  * 100).toFixed(1);
        const y = ((e.clientY - r.top)  / r.height * 100).toFixed(1);
        btn.style.setProperty('--mx', x + '%');
        btn.style.setProperty('--my', y + '%');
      }, { passive: true });
    });
  }

  /* ─────────────────────────────────────────────────────────────
     4. PARALLAX EFFECT (pure JS, passive listeners)
     ───────────────────────────────────────────────────────────*/
  function initParallax() {
    const layers = document.querySelectorAll('.hero-orb, .grid-bg, .parallax-layer');
    if (!layers.length) return;

    let ticking = false;
    window.addEventListener('scroll', () => {
      if (!ticking) {
        requestAnimationFrame(() => {
          const sy = window.scrollY;
          layers.forEach((el, i) => {
            const speed = el.dataset.parallaxSpeed || (0.05 + i * 0.02);
            el.style.transform = `translateY(${sy * speed}px)`;
          });
          ticking = false;
        });
        ticking = true;
      }
    }, { passive: true });
  }

  /* ─────────────────────────────────────────────────────────────
     5. LENIS SMOOTH SCROLL  (loaded from CDN)
     ───────────────────────────────────────────────────────────*/
  function initLenis() {
    if (typeof Lenis === 'undefined') return;
    // Don't init if intro is blocking scroll
    if (document.body.classList.contains('intro-active')) {
      document.body.addEventListener('transitionend', () => {
        if (!document.body.classList.contains('intro-active')) startLenis();
      }, { once: true });
    } else {
      startLenis();
    }

    function startLenis() {
      const lenis = new Lenis({
        duration:   1.25,
        easing:     t => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
        smoothWheel: true,
        touchMultiplier: 2
      });
      function raf(time) {
        lenis.raf(time);
        requestAnimationFrame(raf);
      }
      requestAnimationFrame(raf);

      // Sync GSAP ScrollTrigger if available
      if (typeof ScrollTrigger !== 'undefined') {
        lenis.on('scroll', ScrollTrigger.update);
        gsap.ticker.add(time => lenis.raf(time * 1000));
        gsap.ticker.lagSmoothing(0);
      }
    }
  }

  /* ─────────────────────────────────────────────────────────────
     6. GSAP SCROLL REVEAL + PARALLAX
     ───────────────────────────────────────────────────────────*/
  function initGSAP() {
    if (typeof gsap === 'undefined' || typeof ScrollTrigger === 'undefined') return;
    gsap.registerPlugin(ScrollTrigger);

    // -- Section headings
    gsap.utils.toArray('h1, h2').forEach(el => {
      gsap.from(el, {
        scrollTrigger: { trigger: el, start: 'top 88%', toggleActions: 'play none none none' },
        y: 28, opacity: 0, duration: 0.75, ease: 'power3.out'
      });
    });

    // -- Glass cards stagger
    document.querySelectorAll('.stagger-children').forEach(container => {
      gsap.from(container.children, {
        scrollTrigger: { trigger: container, start: 'top 82%', toggleActions: 'play none none none' },
        y: 40, opacity: 0, duration: 0.7, ease: 'power3.out', stagger: 0.12
      });
    });

    // -- Custom gsap-reveal elements
    gsap.utils.toArray('.gsap-reveal').forEach(el => {
      gsap.from(el, {
        scrollTrigger: { trigger: el, start: 'top 85%', toggleActions: 'play none none none' },
        y: 36, opacity: 0, duration: 0.75, ease: 'power3.out'
      });
    });
    gsap.utils.toArray('.gsap-reveal-left').forEach(el => {
      gsap.from(el, {
        scrollTrigger: { trigger: el, start: 'top 85%', toggleActions: 'play none none none' },
        x: -36, opacity: 0, duration: 0.75, ease: 'power3.out'
      });
    });
    gsap.utils.toArray('.gsap-reveal-right').forEach(el => {
      gsap.from(el, {
        scrollTrigger: { trigger: el, start: 'top 85%', toggleActions: 'play none none none' },
        x: 36, opacity: 0, duration: 0.75, ease: 'power3.out'
      });
    });
    gsap.utils.toArray('.gsap-reveal-scale').forEach(el => {
      gsap.from(el, {
        scrollTrigger: { trigger: el, start: 'top 85%', toggleActions: 'play none none none' },
        scale: 0.92, opacity: 0, duration: 0.75, ease: 'back.out(1.4)'
      });
    });

    // -- Stat cards scale-in
    document.querySelectorAll('.stat-card').forEach((card, i) => {
      gsap.from(card, {
        scrollTrigger: { trigger: card, start: 'top 88%', toggleActions: 'play none none none' },
        y: 30, opacity: 0, scale: 0.95, duration: 0.6, ease: 'back.out(1.5)', delay: i * 0.1
      });
    });

    // -- Game cards
    document.querySelectorAll('.game-card').forEach((card, i) => {
      gsap.from(card, {
        scrollTrigger: { trigger: card, start: 'top 90%', toggleActions: 'play none none none' },
        y: 40, opacity: 0, duration: 0.6, ease: 'power3.out', delay: (i % 4) * 0.08
      });
    });

    // -- Parallax hero orb
    document.querySelectorAll('.hero-orb').forEach((orb, i) => {
      const dir = i % 2 === 0 ? 1 : -1;
      gsap.to(orb, {
        scrollTrigger: { trigger: '.hero-section', start: 'top top', end: 'bottom top', scrub: 1.5 },
        y: dir * 80, ease: 'none'
      });
    });

    // -- Section transition (slide-in from slight offset)
    document.querySelectorAll('section').forEach(sec => {
      gsap.from(sec, {
        scrollTrigger: { trigger: sec, start: 'top 95%', toggleActions: 'play none none none' },
        opacity: 0, duration: 0.5, ease: 'power1.out'
      });
    });
  }

  /* ─────────────────────────────────────────────────────────────
     7. VANILLA TILT (enhanced card 3D, replaces the basic tilt)
     ───────────────────────────────────────────────────────────*/
  function initVanillaTilt() {
    if (typeof VanillaTilt === 'undefined') return;
    VanillaTilt.init(document.querySelectorAll('.glass-card, .hero-card-demo, .stat-card'), {
      max:         8,
      speed:       400,
      glare:       true,
      'max-glare': 0.12,
      perspective: 1200,
      scale:       1.02,
      easing:      'cubic-bezier(.03,.98,.52,.99)'
    });
  }

  /* ─────────────────────────────────────────────────────────────
     8. SECTION DIVIDER GLOW LINES (injected between sections)
     ───────────────────────────────────────────────────────────*/
  function injectDividers() {
    const sections = document.querySelectorAll('#main-website > section, section');
    sections.forEach((sec, i) => {
      if (i === 0) return;
      const hr = document.createElement('hr');
      hr.className = 'section-divider-glow';
      sec.parentNode.insertBefore(hr, sec);
    });
  }

  /* ─────────────────────────────────────────────────────────────
     9. BOOTSTRAP — Load CDNs then initialize in order
     ───────────────────────────────────────────────────────────*/
  function bootstrap() {
    // Cursor & button FX — no deps
    initCursor();
    initButtonFX();
    initParallax();
    injectDividers();

    // Load Lenis → then init
    loadScript('https://cdn.jsdelivr.net/npm/@studio-freight/lenis@1.0.42/dist/lenis.min.js', () => {
      initLenis();
    });

    // Load VanillaTilt
    loadScript('https://cdn.jsdelivr.net/npm/vanilla-tilt@1.8.1/dist/vanilla-tilt.min.js', () => {
      // Small delay to ensure DOM elements are stable
      setTimeout(initVanillaTilt, 500);
    });

    // Load GSAP core → then ScrollTrigger → then init
    loadScript('https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js', () => {
      loadScript('https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/ScrollTrigger.min.js', () => {
        // Wait for page content to be visible (after intro video)
        const main = document.getElementById('main-website');
        if (main && !main.classList.contains('visible')) {
          // Observe when main-website becomes visible
          const obs = new MutationObserver((mutations, o) => {
            if (main.classList.contains('visible')) {
              o.disconnect();
              setTimeout(initGSAP, 200);
            }
          });
          obs.observe(main, { attributes: true, attributeFilter: ['class'] });
        } else {
          setTimeout(initGSAP, 100);
        }
      });
    });
  }

  // Fire after DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', bootstrap);
  } else {
    bootstrap();
  }

})();
