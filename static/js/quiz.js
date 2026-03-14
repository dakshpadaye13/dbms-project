/* ============================================================
   LearnQuest AI - Quiz JavaScript Module
   Additional quiz utilities (keyboard, review mode, etc.)
   Core quiz logic is embedded in quiz_game.html
   ============================================================ */

'use strict';

// ── Keyboard navigation ────────────────────────────────────────
document.addEventListener('keydown', (e) => {
  if (!window.QUESTIONS) return;

  const keyMap = { 'a': 'A', 'b': 'B', 'c': 'C', 'd': 'D',
                   '1': 'A', '2': 'B', '3': 'C', '4': 'D' };

  if (keyMap[e.key.toLowerCase()] && window.currentIdx !== undefined) {
    const currentQ = window.QUESTIONS[window.currentIdx];
    if (currentQ) {
      window.selectAnswer(currentQ.id, keyMap[e.key.toLowerCase()]);
    }
  }

  if (e.key === 'ArrowRight' || e.key === 'Enter') {
    const nextBtn = document.getElementById('nextBtn');
    if (nextBtn && nextBtn.style.display !== 'none') window.nextQuestion();
  }
  if (e.key === 'ArrowLeft') {
    if (!document.getElementById('prevBtn')?.disabled) window.prevQuestion();
  }
});
