/* ============================================================
   LearnQuest AI - Main JavaScript Utilities
   Handles: navbar scroll, reveal animations, mobile menu
   ============================================================ */

'use strict';

// ── Navbar scroll effect ───────────────────────────────────────
const navbar = document.getElementById('navbar');
if (navbar) {
  window.addEventListener('scroll', () => {
    navbar.classList.toggle('scrolled', window.scrollY > 30);
  }, { passive: true });
}

// ── Mobile hamburger ───────────────────────────────────────────
const hamburger     = document.getElementById('hamburger');
const mobileDrawer  = document.getElementById('mobileDrawer');
if (hamburger && mobileDrawer) {
  hamburger.addEventListener('click', () => {
    mobileDrawer.classList.toggle('open');
    // Animate spans
    const spans = hamburger.querySelectorAll('span');
    if (mobileDrawer.classList.contains('open')) {
      spans[0].style.transform = 'rotate(45deg) translate(5px, 5px)';
      spans[1].style.opacity   = '0';
      spans[2].style.transform = 'rotate(-45deg) translate(5px, -5px)';
    } else {
      spans.forEach(s => { s.style.transform = ''; s.style.opacity = ''; });
    }
  });
}

// ── Scroll reveal ─────────────────────────────────────────────
const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
    }
  });
}, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

document.querySelectorAll('.reveal').forEach(el => revealObserver.observe(el));

// ── Auto-dismiss flash messages ───────────────────────────────
document.querySelectorAll('.flash').forEach(flash => {
  setTimeout(() => {
    flash.style.opacity    = '0';
    flash.style.transform  = 'translateX(30px)';
    flash.style.transition = 'all 0.4s';
    setTimeout(() => flash.remove(), 400);
  }, 5000);
});

// ── Smooth anchor scrolling ────────────────────────────────────
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', e => {
    const target = document.querySelector(a.getAttribute('href'));
    if (target) {
      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      if (mobileDrawer) mobileDrawer.classList.remove('open');
    }
  });
});

// ── Active nav-link on scroll ──────────────────────────────────
const sections    = document.querySelectorAll('section[id]');
const navLinks    = document.querySelectorAll('.nav-link[href^="#"]');
if (sections.length && navLinks.length) {
  const sectionObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        navLinks.forEach(l => {
          l.classList.toggle('active', l.getAttribute('href') === '#' + entry.target.id);
        });
      }
    });
  }, { threshold: 0.5 });
  sections.forEach(s => sectionObserver.observe(s));
}

// ── Particle burst on button click ───────────────────────────
document.querySelectorAll('.btn-primary').forEach(btn => {
  btn.addEventListener('click', function(e) {
    const colors = ['#7c3aed','#3b82f6','#06b6d4','#f59e0b','#ec4899'];
    for (let i = 0; i < 8; i++) {
      const p = document.createElement('div');
      p.className = 'particle';
      p.style.cssText = `
        left: ${e.clientX - 4}px;
        top:  ${e.clientY - 4}px;
        background: ${colors[i % colors.length]};
        --px: ${(Math.random() - 0.5) * 100}px;
        position: fixed;
        pointer-events: none;
        z-index: 9999;
      `;
      document.body.appendChild(p);
      setTimeout(() => p.remove(), 1000);
    }
  });
});

// ── Number counter animation ───────────────────────────────────
function animateCounter(el, target, duration = 2000) {
  const start    = performance.now();
  const startVal = 0;
  const update   = (time) => {
    const elapsed  = time - start;
    const progress = Math.min(elapsed / duration, 1);
    const ease     = 1 - Math.pow(1 - progress, 3);
    el.textContent = Math.round(startVal + (target - startVal) * ease).toLocaleString();
    if (progress < 1) requestAnimationFrame(update);
  };
  requestAnimationFrame(update);
}

// Trigger counter on stat cards
const counterObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting && !entry.target.dataset.animated) {
      entry.target.dataset.animated = '1';
      const val = parseFloat(entry.target.textContent.replace(/[^0-9.]/g, ''));
      if (!isNaN(val) && val > 0) animateCounter(entry.target, val);
    }
  });
}, { threshold: 0.5 });

document.querySelectorAll('.stat-value').forEach(el => counterObserver.observe(el));

// ── Typewriter effect ─────────────────────────────────────────
function typeWriter(el, texts, speed = 80) {
  let textIdx = 0, charIdx = 0, deleting = false;
  el.classList.add('typing-cursor');
  function type() {
    const current = texts[textIdx];
    if (!deleting) {
      el.textContent = current.slice(0, ++charIdx);
      if (charIdx === current.length) { deleting = true; setTimeout(type, 2000); return; }
    } else {
      el.textContent = current.slice(0, --charIdx);
      if (charIdx === 0) { deleting = false; textIdx = (textIdx + 1) % texts.length; }
    }
    setTimeout(type, deleting ? speed / 2 : speed);
  }
  type();
}

// Apply to elements with data-typewriter
document.querySelectorAll('[data-typewriter]').forEach(el => {
  const texts = el.dataset.typewriter.split('|');
  typeWriter(el, texts);
});
