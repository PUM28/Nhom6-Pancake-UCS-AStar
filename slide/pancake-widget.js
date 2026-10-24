/**
 * Pancake Widget Runtime (pancake-widget.js)
 * Implements interactive pancake stacks, spatula flip animations,
 * manual play, cost tracking, race mode synchronization, and heuristic annotations.
 */
(function () {
  'use strict';

  // SVG Spatula definition
  const SPATULA_SVG = `
    <svg viewBox="0 0 100 32" fill="none" xmlns="http://www.w3.org/2000/svg" class="pk-spatula-svg">
      <path d="M2 16h38l8-6h46a4 4 0 0 1 4 4v8a4 4 0 0 1-4 4H48l-8-6H2a2 2 0 0 1-2-2v-2a2 2 0 0 1 2-2z" fill="url(#pk-spatula-grad)" filter="drop-shadow(0 2px 4px rgba(0,0,0,0.4))"/>
      <line x1="56" y1="13" x2="88" y2="13" stroke="rgba(0,0,0,0.25)" stroke-width="2" stroke-linecap="round"/>
      <line x1="56" y1="17" x2="88" y2="17" stroke="rgba(0,0,0,0.25)" stroke-width="2" stroke-linecap="round"/>
      <defs>
        <linearGradient id="pk-spatula-grad" x1="0" y1="0" x2="100" y2="30" gradientUnits="userSpaceOnUse">
          <stop stop-color="#94a3b8"/>
          <stop offset="0.5" stop-color="#cbd5e1"/>
          <stop offset="1" stop-color="#64748b"/>
        </linearGradient>
      </defs>
    </svg>
  `;

  class PancakeWidget {
    constructor(container) {
      this.el = container;
      this.startState = this.parseArray(this.el.getAttribute('data-start') || '6,5,4,3,2,1');
      this.goalState = this.parseArray(this.el.getAttribute('data-goal') || '1,2,3,4,5,6');
      this.actions = this.parseArray(this.el.getAttribute('data-actions') || '');
      this.mode = this.el.getAttribute('data-mode') || 'auto'; // auto | manual | annotate
      this.group = this.el.getAttribute('data-group') || '';
      this.title = this.el.getAttribute('data-title') || '';

      this.n = this.startState.length;
      this.state = [...this.startState];
      this.stepIndex = 0;
      this.flips = 0;
      this.cost = 0;
      this.history = []; // for undo in manual mode
      this.isPlaying = false;
      this.timer = null;
      this.isFlipping = false;

      // Validate actions on init
      this.validateExpectedActions();

      // Render skeleton
      this.render();
      this.bindEvents();
    }

    parseArray(str) {
      if (!str || !str.trim()) return [];
      return str.split(',').map(s => parseInt(s.trim(), 10)).filter(n => !isNaN(n));
    }

    validateExpectedActions() {
      if (!this.actions.length) return;
      let s = [...this.startState];
      let c = 0;
      for (const k of this.actions) {
        if (k >= 2 && k <= s.length) {
          s = s.slice(0, k).reverse().concat(s.slice(k));
          c += k;
        }
      }
      const reachedGoal = s.join(',') === this.goalState.join(',');
      console.assert(reachedGoal, `[PancakeWidget] Actions ${this.actions} did not reach goal ${this.goalState}. Result: ${s}`);
      if (!reachedGoal) {
        this.el.classList.add('pk-invalid');
      }
    }

    render() {
      const isRace = this.group === 'race';
      const isAnnotate = this.mode === 'annotate';
      const isManual = this.mode === 'manual';

      this.el.innerHTML = `
        <div class="pk-header">
          <div class="pk-title">
            <span>🥞</span>
            <span>${this.title || (isAnnotate ? 'Phân tích Heuristic' : (isRace ? 'So tài UCS vs A*' : 'Trạng thái Pancake'))}</span>
          </div>
          <div class="pk-status-badge">Khởi đầu</div>
        </div>

        <div class="pk-counters">
          <div class="pk-counter-pill">
            <span class="pk-counter-label">Số lần lật</span>
            <span class="pk-counter-val pk-flip-count">0</span>
          </div>
          <div class="pk-counter-pill pk-cost-pill">
            <span class="pk-counter-label">Tổng chi phí (Σk)</span>
            <span class="pk-counter-val pk-cost-count">0</span>
          </div>
        </div>

        ${isRace ? `
          <div class="pk-race-progress-bar">
            <div class="pk-race-progress-fill" style="width: 0%"></div>
          </div>
        ` : ''}

        <div class="pk-stage-wrap">
          <div class="pk-spatula">${SPATULA_SVG}</div>
          <div class="pk-flip-toast">flip(k) · +k</div>
          <div class="pk-stack"></div>
          <div class="pk-fake-plate">Đĩa giả (n+1 = ${this.n + 1})</div>
          <div class="pk-plate"></div>
          <div class="pk-plate-base"></div>
        </div>

        ${isAnnotate ? `
          <div class="pk-annotate-controls">
            <button class="pk-btn pk-btn-toggle pk-btn-anno-l" type="button">Lớp 1: h<sub>L</sub> (Bánh sai)</button>
            <button class="pk-btn pk-btn-toggle pk-btn-anno-b" type="button">Lớp 2: h<sub>B</sub> (Điểm đứt)</button>
          </div>
          <div class="pk-anno-summary pk-anno-summary-l">
            h<sub>L</sub> = <span class="pk-hl-val">4</span> (Bánh sai vị trí lớn nhất)
          </div>
          <div class="pk-anno-summary pk-anno-summary-b">
            B = <span class="pk-b-val">4</span> điểm đứt ⇒ h<sub>B</sub> = 2 × 4 = 8
          </div>
        ` : `
          <div class="pk-controls ${isRace ? 'pk-race-hidden-controls' : ''}">
            <button class="pk-btn pk-btn-primary pk-btn-play" type="button" title="Chạy tự động">▶</button>
            <button class="pk-btn pk-btn-step" type="button" title="Bước tiếp theo">⏭</button>
            <button class="pk-btn pk-btn-reset" type="button" title="Về trạng thái đầu">⏮</button>
          </div>
        `}

        ${isManual ? `
          <div class="pk-manual-row">
            ${Array.from({ length: this.n - 1 }, (_, i) => i + 2).map(k => `
              <button class="pk-btn pk-btn-action" data-k="${k}" type="button">flip(${k})</button>
            `).join('')}
            <button class="pk-btn pk-btn-undo" type="button">↩ Hoàn tác</button>
          </div>
        ` : ''}
      `;

      this.stackEl = this.el.querySelector('.pk-stack');
      this.statusBadgeEl = this.el.querySelector('.pk-status-badge');
      this.flipCountEl = this.el.querySelector('.pk-flip-count');
      this.costCountEl = this.el.querySelector('.pk-cost-count');
      this.spatulaEl = this.el.querySelector('.pk-spatula');
      this.toastEl = this.el.querySelector('.pk-flip-toast');
      this.playBtn = this.el.querySelector('.pk-btn-play');
      this.stepBtn = this.el.querySelector('.pk-btn-step');
      this.resetBtn = this.el.querySelector('.pk-btn-reset');
      this.progressFillEl = this.el.querySelector('.pk-race-progress-fill');

      this.updateStackDOM();
      this.updateCounters();
      this.updateStatus();
    }

    updateStackDOM() {
      // Map pancake value to visual width
      // Min width ~34%, max width ~92%
      this.stackEl.innerHTML = '';
      const minW = 34;
      const maxW = 92;
      const stepW = this.n > 1 ? (maxW - minW) / (this.n - 1) : 0;

      // Find largest wrong pancake for annotate mode
      let maxWrong = -1;
      this.state.forEach((val, idx) => {
        const goalVal = this.goalState[idx];
        if (val !== goalVal && val > maxWrong) {
          maxWrong = val;
        }
      });

      this.state.forEach((val, idx) => {
        const p = document.createElement('div');
        p.className = 'pk-pancake';
        p.dataset.val = val;
        p.dataset.pos = idx + 1;
        const wPct = minW + (val - 1) * stepW;
        p.style.width = `${wPct}%`;

        // Annotation classes
        const isGoalMatch = val === this.goalState[idx];
        if (isGoalMatch) {
          p.classList.add('pk-correct');
        } else {
          p.classList.add('pk-wrong');
          if (val === maxWrong) {
            p.classList.add('pk-max-wrong');
          }
        }

        p.innerHTML = `
          <span class="pk-num">${val}</span>
          ${val === maxWrong ? `<span class="pk-max-wrong-pill">h<sub>L</sub> = ${val}</span>` : ''}
        `;

        // Breakpoint marker between idx and idx+1
        if (idx < this.state.length - 1) {
          const nextVal = this.state[idx + 1];
          if (Math.abs(val - nextVal) !== 1) {
            const bp = document.createElement('div');
            bp.className = 'pk-breakpoint-mark';
            p.appendChild(bp);
          }
        } else {
          // Bottom pancake compared to fake plate (n+1)
          if (Math.abs(val - (this.n + 1)) !== 1) {
            const bp = document.createElement('div');
            bp.className = 'pk-breakpoint-mark';
            p.appendChild(bp);
          }
        }

        this.stackEl.appendChild(p);
      });
    }

    updateCounters() {
      if (this.flipCountEl) this.flipCountEl.textContent = this.flips;
      if (this.costCountEl) this.costCountEl.textContent = this.cost;

      if (this.progressFillEl) {
        // Assume maximum expected cost ~25
        const maxExpected = 20;
        const pct = Math.min(100, Math.round((this.cost / maxExpected) * 100));
        this.progressFillEl.style.width = `${pct}%`;
      }
    }

    updateStatus() {
      const isGoal = this.state.join(',') === this.goalState.join(',');
      if (isGoal) {
        this.statusBadgeEl.textContent = '✓ Đích (Goal)';
        this.statusBadgeEl.className = 'pk-status-badge pk-at-goal';
        this.el.classList.add('pk-at-goal');
      } else {
        this.statusBadgeEl.textContent = this.flips > 0 ? `Bước ${this.stepIndex}` : 'Khởi đầu';
        this.statusBadgeEl.className = 'pk-status-badge';
        this.el.classList.remove('pk-at-goal');
      }
    }

    flip(k, callback) {
      if (this.isFlipping || k < 2 || k > this.n) return;
      this.isFlipping = true;

      // Save for undo
      this.history.push({ state: [...this.state], flips: this.flips, cost: this.cost, stepIndex: this.stepIndex });

      // Wrap top k pancakes in .pk-flip-group
      const pancakes = Array.from(this.stackEl.children);
      const topKPancakes = pancakes.slice(0, k);

      const group = document.createElement('div');
      group.className = 'pk-flip-group';
      this.stackEl.insertBefore(group, topKPancakes[0]);
      topKPancakes.forEach(p => group.appendChild(p));

      // Spatula positioning
      const targetPancake = topKPancakes[topKPancakes.length - 1];
      const stageRect = this.el.querySelector('.pk-stage-wrap').getBoundingClientRect();
      const pRect = targetPancake.getBoundingClientRect();
      const relativeTop = pRect.top - stageRect.top + pRect.height / 2;

      this.spatulaEl.style.top = `${relativeTop - 12}px`;
      this.spatulaEl.classList.add('pk-active');

      // Toast
      this.toastEl.textContent = `flip(${k}) · +${k}`;
      this.toastEl.classList.add('pk-show');

      // Trigger animation
      requestAnimationFrame(() => {
        this.el.classList.add('pk-flipping');
      });

      setTimeout(() => {
        // Complete flip logically
        this.state = this.state.slice(0, k).reverse().concat(this.state.slice(k));
        this.flips += 1;
        this.cost += k;
        this.stepIndex += 1;

        this.el.classList.remove('pk-flipping');
        this.spatulaEl.classList.remove('pk-active');
        this.toastEl.classList.remove('pk-show');

        this.updateStackDOM();
        this.updateCounters();
        this.updateStatus();

        this.isFlipping = false;
        if (typeof callback === 'function') callback();
      }, 820);
    }

    step() {
      if (this.stepIndex < this.actions.length) {
        const k = this.actions[this.stepIndex];
        this.flip(k, () => {
          if (this.isPlaying && this.stepIndex < this.actions.length) {
            this.timer = setTimeout(() => this.step(), 600);
          } else {
            this.pause();
          }
        });
      } else {
        this.pause();
      }
    }

    play() {
      if (this.isPlaying || this.isFlipping) return;
      if (this.stepIndex >= this.actions.length) {
        this.reset();
      }
      this.isPlaying = true;
      if (this.playBtn) this.playBtn.textContent = '⏸';
      this.step();
    }

    pause() {
      this.isPlaying = false;
      if (this.timer) clearTimeout(this.timer);
      this.timer = null;
      if (this.playBtn) this.playBtn.textContent = '▶';
    }

    reset() {
      this.pause();
      this.state = [...this.startState];
      this.stepIndex = 0;
      this.flips = 0;
      this.cost = 0;
      this.history = [];
      this.isFlipping = false;
      this.el.classList.remove('pk-flipping');
      if (this.spatulaEl) this.spatulaEl.classList.remove('pk-active');
      if (this.toastEl) this.toastEl.classList.remove('pk-show');

      this.updateStackDOM();
      this.updateCounters();
      this.updateStatus();
    }

    undo() {
      if (this.isFlipping || !this.history.length) return;
      const prev = this.history.pop();
      this.state = prev.state;
      this.flips = prev.flips;
      this.cost = prev.cost;
      this.stepIndex = prev.stepIndex;

      this.updateStackDOM();
      this.updateCounters();
      this.updateStatus();
    }

    bindEvents() {
      if (this.playBtn) {
        this.playBtn.addEventListener('click', () => {
          if (this.isPlaying) this.pause();
          else this.play();
        });
      }

      if (this.stepBtn) {
        this.stepBtn.addEventListener('click', () => {
          this.pause();
          this.step();
        });
      }

      if (this.resetBtn) {
        this.resetBtn.addEventListener('click', () => {
          this.reset();
        });
      }

      // Manual buttons
      const actionBtns = this.el.querySelectorAll('.pk-btn-action');
      actionBtns.forEach(btn => {
        btn.addEventListener('click', () => {
          const k = parseInt(btn.getAttribute('data-k'), 10);
          this.flip(k);
        });
      });

      const undoBtn = this.el.querySelector('.pk-btn-undo');
      if (undoBtn) {
        undoBtn.addEventListener('click', () => this.undo());
      }

      // Annotate buttons
      const annoLBtn = this.el.querySelector('.pk-btn-anno-l');
      const annoBBtn = this.el.querySelector('.pk-btn-anno-b');

      if (annoLBtn) {
        if (this.el.classList.contains('pk-anno-active')) annoLBtn.classList.add('pk-toggled');
        annoLBtn.addEventListener('click', () => {
          this.el.classList.toggle('pk-anno-active');
          annoLBtn.classList.toggle('pk-toggled');
        });
      }

      if (annoBBtn) {
        if (this.el.classList.contains('pk-breaks-active')) annoBBtn.classList.add('pk-toggled');
        annoBBtn.addEventListener('click', () => {
          this.el.classList.toggle('pk-breaks-active');
          annoBBtn.classList.toggle('pk-toggled');
        });
      }

      // Auto-trigger on slide activation via MutationObserver
      const parentSlide = this.el.closest('.slide');
      if (parentSlide) {
        const observer = new MutationObserver(mutations => {
          mutations.forEach(m => {
            if (m.type === 'attributes' && m.attributeName === 'class') {
              const isActive = parentSlide.classList.contains('is-active');
              if (isActive) {
                if (this.mode === 'auto' && !this.group) {
                  setTimeout(() => {
                    if (parentSlide.classList.contains('is-active')) {
                      this.play();
                    }
                  }, 500);
                }
              } else {
                this.reset();
              }
            }
          });
        });
        observer.observe(parentSlide, { attributes: true, attributeFilter: ['class'] });

        // If slide is already active on load
        if (parentSlide.classList.contains('is-active') && this.mode === 'auto' && !this.group) {
          setTimeout(() => this.play(), 600);
        }
      }
    }
  }

  // Master race controller for data-group="race"
  function initRaceGroups() {
    const raceWidgets = Array.from(document.querySelectorAll('.pk[data-group="race"]'));
    if (!raceWidgets.length) return;

    // Attach to slide 5
    const slide5 = raceWidgets[0].closest('.slide');
    if (!slide5) return;

    // Find or create shared race controller
    let masterBar = slide5.querySelector('.pk-race-controls-wrap');
    if (!masterBar) {
      masterBar = document.createElement('div');
      masterBar.className = 'pk-race-controls-wrap';
      masterBar.innerHTML = `
        <button class="pk-btn pk-btn-primary pk-race-play-btn" type="button" style="padding: 10px 24px; font-size: 1rem;">
          ▶ So sánh trực tiếp (Chạy song song)
        </button>
        <button class="pk-btn pk-race-reset-btn" type="button" style="padding: 10px 18px;">
          ⏮ Về ban đầu
        </button>
      `;
      const comparisonCard = slide5.querySelector('.race-grid') || slide5.querySelector('.comparison') || slide5.querySelector('.grid');
      if (comparisonCard) {
        comparisonCard.parentNode.insertBefore(masterBar, comparisonCard);
      }
    }

    const instances = raceWidgets.map(el => el.__pkInstance).filter(Boolean);
    const playBtn = masterBar.querySelector('.pk-race-play-btn');
    const resetBtn = masterBar.querySelector('.pk-race-reset-btn');

    let isRacing = false;
    let raceTimer = null;

    function stepBoth() {
      let anyStepped = false;
      instances.forEach(inst => {
        if (inst.stepIndex < inst.actions.length) {
          inst.step();
          anyStepped = true;
        }
      });
      if (anyStepped && isRacing) {
        raceTimer = setTimeout(stepBoth, 1200);
      } else {
        isRacing = false;
        playBtn.textContent = '▶ So sánh trực tiếp';
      }
    }

    playBtn.addEventListener('click', () => {
      if (isRacing) {
        isRacing = false;
        if (raceTimer) clearTimeout(raceTimer);
        instances.forEach(inst => inst.pause());
        playBtn.textContent = '▶ So sánh tiếp';
      } else {
        const allDone = instances.every(inst => inst.stepIndex >= inst.actions.length);
        if (allDone) {
          instances.forEach(inst => inst.reset());
        }
        isRacing = true;
        playBtn.textContent = '⏸ Tạm dừng';
        stepBoth();
      }
    });

    resetBtn.addEventListener('click', () => {
      isRacing = false;
      if (raceTimer) clearTimeout(raceTimer);
      instances.forEach(inst => inst.reset());
      playBtn.textContent = '▶ So sánh trực tiếp';
    });

    // Auto race trigger on slide enter
    const observer = new MutationObserver(mutations => {
      mutations.forEach(m => {
        if (m.type === 'attributes' && m.attributeName === 'class') {
          if (slide5.classList.contains('is-active')) {
            setTimeout(() => {
              if (slide5.classList.contains('is-active') && !isRacing) {
                isRacing = true;
                playBtn.textContent = '⏸ Tạm dừng';
                stepBoth();
              }
            }, 600);
          } else {
            isRacing = false;
            if (raceTimer) clearTimeout(raceTimer);
            instances.forEach(inst => inst.reset());
            playBtn.textContent = '▶ So sánh trực tiếp';
          }
        }
      });
    });
    observer.observe(slide5, { attributes: true, attributeFilter: ['class'] });
  }

  // Auto-init all widgets on DOM ready
  function init() {
    document.querySelectorAll('.pk').forEach(el => {
      if (!el.__pkInstance) {
        el.__pkInstance = new PancakeWidget(el);
      }
    });
    initRaceGroups();
  }

  if (document.readyState !== 'loading') {
    init();
  } else {
    document.addEventListener('DOMContentLoaded', init);
  }
})();
