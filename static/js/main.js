/* ============================================================
   EduQuest - Main JavaScript Utilities
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

// ── 3D Tilt Effect ────────────────────────────────────────────
function applyTilt(el) {
  el.addEventListener('mousemove', e => {
    const rect = el.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const centerX = rect.width / 2;
    const centerY = rect.height / 2;
    const rotateX = (centerY - y) / 10;
    const rotateY = (x - centerX) / 10;

    // Use a custom property to store the tilt transform so it can be merged if needed
    el.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.02, 1.02, 1.02)`;
    el.style.transition = 'transform 0.1s ease';
  });

  el.addEventListener('mouseleave', () => {
    el.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) scale3d(1, 1, 1)';
    el.style.transition = 'transform 0.5s ease';
  });
}

// Global initialization for all cards
setTimeout(() => {
  document.querySelectorAll('.glass-card, .hero-card-demo').forEach(applyTilt);
}, 1000);

// ── 3D Slider Logic ──────────────────────────────────────────
class Slider3D {
  constructor(container) {
    this.container = container;
    this.track = container.querySelector('.slider-3d-track');
    this.items = container.querySelectorAll('.slider-item');
    this.currentIndex = 0;
    this.visibleCount = 3; 

    this.init();
  }

  init() {
    this.updateSlider();
    const prevBtn = document.getElementById('prevSlide');
    const nextBtn = document.getElementById('nextSlide');
    if (prevBtn) prevBtn.addEventListener('click', () => this.prev());
    if (nextBtn) nextBtn.addEventListener('click', () => this.next());

    setInterval(() => this.next(), 6000);
  }

  updateSlider() {
    const itemWidth = 100 / this.visibleCount;
    const offset = -this.currentIndex * itemWidth;
    
    // The track handles the horizontal shift
    this.track.style.transform = `translateX(${offset}%)`;
    
    this.items.forEach((item, index) => {
      const isActive = index >= this.currentIndex && index < this.currentIndex + this.visibleCount;
      item.classList.toggle('active', isActive);
      
      // We apply subtle depth to the slider items
      if (isActive) {
        item.style.opacity = '1';
        item.style.visibility = 'visible';
      } else {
        item.style.opacity = '0.3';
        // Only hide if far away to allow smooth transition
        item.style.visibility = (Math.abs(index - this.currentIndex) > this.visibleCount) ? 'hidden' : 'visible';
      }
    });
  }

  next() {
    const maxIndex = this.items.length - this.visibleCount;
    this.currentIndex = (this.currentIndex >= maxIndex) ? 0 : this.currentIndex + 1;
    this.updateSlider();
  }

  prev() {
    const maxIndex = this.items.length - this.visibleCount;
    this.currentIndex = (this.currentIndex <= 0) ? maxIndex : this.currentIndex - 1;
    this.updateSlider();
  }
}

const sliderEl = document.querySelector('.slider-3d-container');
if (sliderEl) new Slider3D(sliderEl);
