/* ============================================================
   LearnQuest AI - Puzzle JavaScript Module
   Additional utilities for puzzle interactions
   Core puzzle logic is embedded in puzzle_game.html
   ============================================================ */

'use strict';

// ── Touch support for drag-and-drop ───────────────────────────
(function addTouchDragSupport() {
  let dragged = null;

  document.addEventListener('touchstart', (e) => {
    const target = e.target.closest('.drag-item');
    if (!target) return;
    dragged = target;
    target.classList.add('dragging');
    e.preventDefault();
  }, { passive: false });

  document.addEventListener('touchmove', (e) => {
    if (!dragged) return;
    const touch = e.touches[0];
    const el    = document.elementFromPoint(touch.clientX, touch.clientY);
    document.querySelectorAll('.drop-zone').forEach(z => z.classList.remove('over'));
    const zone = el?.closest('.drop-zone');
    if (zone) zone.classList.add('over');
    e.preventDefault();
  }, { passive: false });

  document.addEventListener('touchend', (e) => {
    if (!dragged) return;
    dragged.classList.remove('dragging');
    const touch = e.changedTouches[0];
    const el    = document.elementFromPoint(touch.clientX, touch.clientY);
    const zone  = el?.closest('.drop-zone');
    document.querySelectorAll('.drop-zone').forEach(z => z.classList.remove('over'));

    if (zone && window.dropTerm) {
      // Simulate drop for concept match
      const def = zone.querySelector('[style*="text-secondary"]')?.textContent?.trim() || '';
      if (def && window.draggedTerm !== dragged.dataset.term) {
        window.draggedTerm = dragged.dataset.term;
        window.dropTerm(e, def, zone);
      }
    } else if (zone && window.dropToCategory) {
      // Simulate drop for drag-drop category
      const cat = zone.id.replace('cat_', '');
      if (cat) {
        window.draggedTerm = dragged.dataset.item;
        window.dropToCategory(e, cat, zone);
      }
    }
    dragged = null;
  });
})();

// ── Confetti burst on puzzle complete ─────────────────────────
window.burstConfetti = function() {
  const colors  = ['#7c3aed','#3b82f6','#10b981','#f59e0b','#ec4899','#06b6d4'];
  const container = document.body;
  for (let i = 0; i < 30; i++) {
    const c = document.createElement('div');
    c.style.cssText = `
      position: fixed;
      width: ${4 + Math.random() * 8}px;
      height: ${4 + Math.random() * 8}px;
      background: ${colors[Math.floor(Math.random() * colors.length)]};
      border-radius: ${Math.random() > 0.5 ? '50%' : '3px'};
      top: ${20 + Math.random() * 40}%;
      left: ${10 + Math.random() * 80}%;
      z-index: 9999;
      pointer-events: none;
      animation: particleFly ${0.8 + Math.random() * 0.8}s ease forwards;
      --px: ${(Math.random() - 0.5) * 200}px;
    `;
    container.appendChild(c);
    setTimeout(() => c.remove(), 1600);
  }
};
