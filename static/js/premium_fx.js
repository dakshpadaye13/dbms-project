/* ============================================================
   EduQuest — Premium Animation Engine v4  (Cyberpunk Arcade)
   COMPLETE REWRITE — Safe to load after main.js
   Libraries: GSAP + ScrollTrigger, Lenis, VanillaTilt (CDN)
   ============================================================ */

(function () {
  'use strict';

  /* ─────────────────────────────────────────────────────────────
     0. GUARD — Don't run during the intro video
     ─────────────────────────────────────────────────────────── */
  function isIntroPlaying() {
    const screen = document.getElementById('intro-video-screen');
    return screen && !screen.classList.contains('fade-out') && screen.style.display !== 'none';
  }

  /* ─────────────────────────────────────────────────────────────
     1. INJECT CDN SCRIPTS
     ─────────────────────────────────────────────────────────── */
  function loadScript(src, onload) {
    const s = document.createElement('script');
    s.src = src;
    s.async = true;
    if (onload) s.onload = onload;
    document.head.appendChild(s);
  }

  /* ─────────────────────────────────────────────────────────────
     2. SCROLL PROGRESS BAR
     ─────────────────────────────────────────────────────────── */
  function initScrollProgress() {
    const bar = document.getElementById('eq-scroll-progress');
    if (!bar) return;
    function update() {
      const h = document.documentElement.scrollHeight - window.innerHeight;
      const pct = h > 0 ? (window.scrollY / h) * 100 : 0;
      bar.style.width = pct + '%';
    }
    window.addEventListener('scroll', update, { passive: true });
    update();
  }

  /* ─────────────────────────────────────────────────────────────
     3. CUSTOM CURSOR + GHOST TRAIL
     ─────────────────────────────────────────────────────────── */
  function initCursor() {
    if (window.matchMedia('(hover:none)').matches) return;

    const dot = document.createElement('div');
    dot.id = 'eq-cursor-dot';
    const ring = document.createElement('div');
    ring.id = 'eq-cursor-ring';
    document.body.appendChild(dot);
    document.body.appendChild(ring);

    // Ghost trail — 8 fading dots
    const GHOST_COUNT = 8;
    const ghosts = [];
    for (let i = 0; i < GHOST_COUNT; i++) {
      const g = document.createElement('div');
      g.className = 'eq-cursor-ghost';
      g.style.opacity = (1 - i / GHOST_COUNT) * 0.35;
      document.body.appendChild(g);
      ghosts.push({ el: g, x: 0, y: 0 });
    }

    let mouseX = 0, mouseY = 0;
    let ringX = 0, ringY = 0;

    document.addEventListener('mousemove', function (e) {
      mouseX = e.clientX;
      mouseY = e.clientY;
      dot.style.left = mouseX + 'px';
      dot.style.top = mouseY + 'px';
    }, { passive: true });

    function animateRing() {
      ringX += (mouseX - ringX) * 0.12;
      ringY += (mouseY - ringY) * 0.12;
      ring.style.left = ringX + 'px';
      ring.style.top = ringY + 'px';

      // Update ghost trail
      for (let i = ghosts.length - 1; i > 0; i--) {
        ghosts[i].x = ghosts[i - 1].x;
        ghosts[i].y = ghosts[i - 1].y;
      }
      if (ghosts.length) {
        ghosts[0].x = mouseX;
        ghosts[0].y = mouseY;
      }
      ghosts.forEach(function (g) {
        g.el.style.left = g.x + 'px';
        g.el.style.top = g.y + 'px';
        g.el.style.transform = 'translate(-50%, -50%)';
      });

      requestAnimationFrame(animateRing);
    }
    animateRing();

    // Expand on hover
    var hoverSel = 'a, button, .btn, .game-card, .glass-card, .nav-link, input, textarea, [role="button"]';
    document.addEventListener('mouseover', function (e) {
      if (e.target.closest(hoverSel)) document.body.classList.add('cursor-hover');
    }, { passive: true });
    document.addEventListener('mouseout', function (e) {
      if (e.target.closest(hoverSel)) document.body.classList.remove('cursor-hover');
    }, { passive: true });

    // Hide/show on window enter/leave
    document.addEventListener('mouseleave', function () { dot.style.opacity = '0'; ring.style.opacity = '0'; }, { passive: true });
    document.addEventListener('mouseenter', function () { dot.style.opacity = '1'; ring.style.opacity = '1'; }, { passive: true });
  }

  /* ─────────────────────────────────────────────────────────────
     4. BUTTON MOUSE-TRACK
     ─────────────────────────────────────────────────────────── */
  function initButtonFX() {
    document.querySelectorAll('.btn').forEach(function (btn) {
      btn.addEventListener('mousemove', function (e) {
        var r = btn.getBoundingClientRect();
        var x = ((e.clientX - r.left) / r.width * 100).toFixed(1);
        var y = ((e.clientY - r.top) / r.height * 100).toFixed(1);
        btn.style.setProperty('--mx', x + '%');
        btn.style.setProperty('--my', y + '%');
      }, { passive: true });
    });
  }

  /* ─────────────────────────────────────────────────────────────
     5. PARALLAX GRID BACKGROUND
     ─────────────────────────────────────────────────────────── */
  function initParallaxGrid() {
    var grid = document.getElementById('eq-parallax-grid');
    if (!grid) return;
    var ticking = false;
    window.addEventListener('scroll', function () {
      if (!ticking) {
        requestAnimationFrame(function () {
          grid.style.transform = 'translateY(' + (window.scrollY * 0.15) + 'px)';
          ticking = false;
        });
        ticking = true;
      }
    }, { passive: true });
  }

  /* ─────────────────────────────────────────────────────────────
     6. FLOATING PARTICLES CANVAS
     ─────────────────────────────────────────────────────────── */
  function initParticles() {
    var canvas = document.getElementById('eq-particle-canvas');
    if (!canvas) return;
    var ctx = canvas.getContext('2d');
    var W, H;
    var PARTICLE_COUNT = 70;
    var particles = [];
    var colors = ['#a855f7', '#22d3ee', '#f0abfc'];
    var lastScrollY = window.scrollY;
    var scrollDelta = 0;

    function resize() {
      W = canvas.width = window.innerWidth;
      H = canvas.height = window.innerHeight;
    }
    resize();
    window.addEventListener('resize', resize, { passive: true });

    window.addEventListener('scroll', function () {
      scrollDelta = Math.abs(window.scrollY - lastScrollY);
      lastScrollY = window.scrollY;
    }, { passive: true });

    // Create particles
    for (var i = 0; i < PARTICLE_COUNT; i++) {
      particles.push({
        x: Math.random() * (W || 1920),
        y: Math.random() * (H || 1080),
        r: 1 + Math.random() * 2,
        speed: 0.2 + Math.random() * 0.5,
        color: colors[Math.floor(Math.random() * colors.length)],
        alpha: 0.3 + Math.random() * 0.5
      });
    }

    function animate() {
      ctx.clearRect(0, 0, W, H);
      var boost = Math.min(scrollDelta * 0.3, 8);
      scrollDelta *= 0.92; // decay

      for (var i = 0; i < particles.length; i++) {
        var p = particles[i];
        p.y -= p.speed + boost;
        if (p.y < -10) {
          p.y = H + 10;
          p.x = Math.random() * W;
        }
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
        ctx.fillStyle = p.color;
        ctx.globalAlpha = p.alpha;
        ctx.fill();
      }
      ctx.globalAlpha = 1;
      requestAnimationFrame(animate);
    }
    animate();
  }

  /* ─────────────────────────────────────────────────────────────
     7. GLITCH TEXT EFFECT
     ─────────────────────────────────────────────────────────── */
  function initGlitchText() {
    var headings = document.querySelectorAll('h2');
    if (!headings.length) return;
    var cycles = 0;
    var MAX_CYCLES = 3;

    var interval = setInterval(function () {
      if (cycles >= MAX_CYCLES) { clearInterval(interval); return; }
      var idx = Math.floor(Math.random() * headings.length);
      var h = headings[idx];
      h.setAttribute('data-text', h.textContent);
      h.classList.add('glitch-active');
      setTimeout(function () { h.classList.remove('glitch-active'); }, 120);
      cycles++;
    }, 5000);
  }

  /* ─────────────────────────────────────────────────────────────
     8. LENIS SMOOTH SCROLL
     ─────────────────────────────────────────────────────────── */
  var lenisInstance = null;

  function initLenis() {
    if (typeof Lenis === 'undefined') return;

    function startLenis() {
      lenisInstance = new Lenis({
        duration: 1.25,
        easing: function (t) { return Math.min(1, 1.001 - Math.pow(2, -10 * t)); },
        smoothWheel: true,
        touchMultiplier: 2
      });

      function raf(time) {
        lenisInstance.raf(time);
        requestAnimationFrame(raf);
      }
      requestAnimationFrame(raf);

      // Sync with GSAP if available
      if (typeof ScrollTrigger !== 'undefined' && typeof gsap !== 'undefined') {
        lenisInstance.on('scroll', ScrollTrigger.update);
        gsap.ticker.add(function (time) { lenisInstance.raf(time * 1000); });
        gsap.ticker.lagSmoothing(0);
      }
    }

    if (document.body.classList.contains('intro-active')) {
      var obs = new MutationObserver(function (mutations, o) {
        if (!document.body.classList.contains('intro-active')) {
          o.disconnect();
          startLenis();
        }
      });
      obs.observe(document.body, { attributes: true, attributeFilter: ['class'] });
    } else {
      startLenis();
    }
  }

  /* ─────────────────────────────────────────────────────────────
     9. GSAP SCROLL EFFECTS (all-in-one)
     ─────────────────────────────────────────────────────────── */
  function initGSAP() {
    if (typeof gsap === 'undefined' || typeof ScrollTrigger === 'undefined') return;
    gsap.registerPlugin(ScrollTrigger);

    // Disable normalizeScroll so Lenis stays in control
    ScrollTrigger.normalizeScroll(false);

    // ── matchMedia: desktop vs mobile ──
    ScrollTrigger.matchMedia({

      // ── DESKTOP (>768px) ──────────────────────────────────
      '(min-width: 769px)': function () {

        // 1. HERO 3-LAYER PARALLAX
        var heroSection = document.querySelector('.hero-section');
        if (heroSection) {
          // Background orbs — fastest
          gsap.utils.toArray('.hero-orb').forEach(function (orb) {
            gsap.to(orb, {
              yPercent: -60,
              ease: 'none',
              scrollTrigger: { trigger: heroSection, start: 'top top', end: 'bottom top', scrub: 1.5 }
            });
          });

          // Hero visual (3D sphere / card) — medium
          var heroVisual = heroSection.querySelector('.hero-visual');
          if (heroVisual) {
            gsap.to(heroVisual, {
              yPercent: -30,
              ease: 'none',
              scrollTrigger: { trigger: heroSection, start: 'top top', end: 'bottom top', scrub: 1.5 }
            });
          }

          // Hero text — slowest
          var heroText = heroSection.querySelector('.animate-fadeInUp');
          if (heroText) {
            gsap.to(heroText, {
              yPercent: -15,
              ease: 'none',
              scrollTrigger: { trigger: heroSection, start: 'top top', end: 'bottom top', scrub: 1.5 }
            });
          }
        }

        // Scroll-down hint fade
        var scrollHint = document.getElementById('eq-scroll-hint');
        if (scrollHint) {
          gsap.to(scrollHint, {
            opacity: 0,
            scrollTrigger: { trigger: 'body', start: '20% top', end: '25% top', scrub: true }
          });
        }

        // 3. HORIZONTAL SCROLL — Game Modes
        var hscrollSection = document.querySelector('.hscroll-section');
        var hscrollTrack = document.querySelector('.hscroll-track');
        var hscrollFill = document.querySelector('.hscroll-progress-fill');
        if (hscrollSection && hscrollTrack) {
          var cards = hscrollTrack.children;
          var totalWidth = 0;
          for (var i = 0; i < cards.length; i++) {
            totalWidth += cards[i].offsetWidth + 24;
          }
          totalWidth -= 24; // remove last gap
          var scrollDist = totalWidth - hscrollSection.offsetWidth + 100;

          var hscrollTween = gsap.to(hscrollTrack, {
            x: function () { return -scrollDist; },
            ease: 'none',
            scrollTrigger: {
              trigger: hscrollSection,
              pin: true,
              scrub: 1,
              end: '+=2500',
              onUpdate: function (self) {
                if (hscrollFill) hscrollFill.style.width = (self.progress * 100) + '%';
              }
            }
          });
        }
      },

      // ── MOBILE (<768px) ───────────────────────────────────
      '(max-width: 768px)': function () {
        // Parallax & horizontal scroll disabled via CSS + no GSAP triggers
      },

      // ── ALL SIZES ─────────────────────────────────────────
      'all': function () {

        // 2. SECTION REVEALS — staggered cards
        document.querySelectorAll('.stagger-children').forEach(function (container) {
          gsap.from(container.children, {
            scrollTrigger: { trigger: container, start: 'top 82%', toggleActions: 'play none none reverse' },
            y: 80, opacity: 0, scale: 0.94,
            duration: 0.9, ease: 'expo.out', stagger: 0.12
          });
        });

        // Glass card individual reveals
        gsap.utils.toArray('.glass-card').forEach(function (card) {
          gsap.from(card, {
            scrollTrigger: { trigger: card, start: 'top 88%', toggleActions: 'play none none reverse' },
            y: 80, opacity: 0, scale: 0.94,
            duration: 0.9, ease: 'expo.out'
          });
        });

        // 4. STATS COUNTER — number roll
        document.querySelectorAll('.stat-value').forEach(function (el) {
          var targetText = el.textContent.trim();
          var targetNum = parseFloat(targetText.replace(/[^0-9.]/g, ''));
          if (isNaN(targetNum) || targetNum <= 0) return;
          var suffix = targetText.replace(/[0-9.,]/g, '');

          ScrollTrigger.create({
            trigger: el,
            start: 'top 70%',
            once: true,
            onEnter: function () {
              gsap.from({ val: 0 }, {
                val: targetNum,
                duration: 2,
                ease: 'power2.out',
                onUpdate: function () {
                  el.textContent = Math.round(this.targets()[0].val).toLocaleString() + suffix;
                }
              });
            }
          });
        });

        // 6. SECTION WIPE LINES
        document.querySelectorAll('.section-wipe-line').forEach(function (line) {
          gsap.to(line, {
            width: '100%',
            duration: 1.2,
            ease: 'power2.inOut',
            scrollTrigger: { trigger: line, start: 'top 85%', toggleActions: 'play none none none' }
          });
        });

        // Section transition opacity
        document.querySelectorAll('section').forEach(function (sec) {
          gsap.from(sec, {
            scrollTrigger: { trigger: sec, start: 'top 95%', toggleActions: 'play none none none' },
            opacity: 0, duration: 0.5, ease: 'power1.out'
          });
        });

        // 7. LEADERBOARD CASCADE LEFT ENTRANCE
        document.querySelectorAll('.lb-row').forEach(function (row, i) {
          gsap.from(row, {
            scrollTrigger: { trigger: row, start: 'top 90%', toggleActions: 'play none none none' },
            x: -100, opacity: 0,
            duration: 0.7, ease: 'back.out(1.4)', delay: i * 0.08
          });
        });

        // 8. XP PROGRESS BARS — scroll fill
        document.querySelectorAll('.progress-bar-fill').forEach(function (bar) {
          var w = bar.style.width || bar.getAttribute('data-width') || '0%';
          bar.style.width = '0%';

          ScrollTrigger.create({
            trigger: bar,
            start: 'top 85%',
            once: true,
            onEnter: function () {
              gsap.to(bar, {
                width: w,
                duration: 1.8,
                ease: 'power3.out',
                onComplete: function () { bar.classList.add('shimmer-active'); }
              });
            }
          });
        });

        // Stat cards scale-in
        document.querySelectorAll('.stat-card').forEach(function (card, i) {
          gsap.from(card, {
            scrollTrigger: { trigger: card, start: 'top 88%', toggleActions: 'play none none none' },
            y: 30, opacity: 0, scale: 0.95,
            duration: 0.6, ease: 'back.out(1.5)', delay: i * 0.1
          });
        });

        // Game cards
        document.querySelectorAll('.game-card').forEach(function (card, i) {
          gsap.from(card, {
            scrollTrigger: { trigger: card, start: 'top 90%', toggleActions: 'play none none none' },
            y: 40, opacity: 0, duration: 0.6, ease: 'power3.out', delay: (i % 4) * 0.08
          });
        });

        // Heading reveals
        gsap.utils.toArray('h1, h2').forEach(function (el) {
          gsap.from(el, {
            scrollTrigger: { trigger: el, start: 'top 88%', toggleActions: 'play none none none' },
            y: 28, opacity: 0, duration: 0.75, ease: 'power3.out'
          });
        });
      }
    });
  }

  /* ─────────────────────────────────────────────────────────────
     10. VANILLA TILT
     ─────────────────────────────────────────────────────────── */
  function initVanillaTilt() {
    if (typeof VanillaTilt === 'undefined') return;
    VanillaTilt.init(document.querySelectorAll('.glass-card, .hero-card-demo, .stat-card'), {
      max: 8,
      speed: 600,
      glare: true,
      'max-glare': 0.12,
      perspective: 1000,
      scale: 1.02,
      easing: 'cubic-bezier(.03,.98,.52,.99)'
    });
  }

  /* ─────────────────────────────────────────────────────────────
     11. SECTION WIPE LINE INJECTOR
     ─────────────────────────────────────────────────────────── */
  function injectWipeLines() {
    var sections = document.querySelectorAll('#main-website > section, main > section, section');
    var seen = new Set();
    sections.forEach(function (sec, i) {
      if (i === 0 || seen.has(sec)) return;
      seen.add(sec);
      var hr = document.createElement('hr');
      hr.className = 'section-wipe-line';
      sec.parentNode.insertBefore(hr, sec);
    });
  }

  /* ─────────────────────────────────────────────────────────────
     12. BOOTSTRAP — Load CDNs then init in order
     ─────────────────────────────────────────────────────────── */
  function bootstrap() {
    // Immediate (no deps)
    initScrollProgress();
    initCursor();
    initButtonFX();
    initParallaxGrid();
    initParticles();
    initGlitchText();
    injectWipeLines();

    // Load Lenis
    loadScript('https://cdn.jsdelivr.net/npm/@studio-freight/lenis@1.0.42/dist/lenis.min.js', function () {
      initLenis();
    });

    // Load VanillaTilt
    loadScript('https://cdn.jsdelivr.net/npm/vanilla-tilt@1.8.1/dist/vanilla-tilt.min.js', function () {
      setTimeout(initVanillaTilt, 500);
    });

    // Load GSAP core → ScrollTrigger → init
    loadScript('https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js', function () {
      loadScript('https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/ScrollTrigger.min.js', function () {
        var main = document.getElementById('main-website');
        if (main && !main.classList.contains('visible')) {
          var obs = new MutationObserver(function (mutations, o) {
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

  // Fire after full load
  if (document.readyState === 'complete') {
    bootstrap();
  } else {
    window.addEventListener('load', bootstrap);
  }

})();
