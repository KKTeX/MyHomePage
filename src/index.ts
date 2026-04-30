//----------
// グラフデザイン
type SkillTier = {
  name: string;
  positionY: string; // 上からの位置 (0% ~ 100%)
};

// 上から順に配置するデータ
const skillTiers: SkillTier[] = [
  { name: "TeX, LaTeX", positionY: "10%" },
  { name: "Lua, expl3", positionY: "30%" },
  { name: "HTML", positionY: "50%" },
  { name: "CSS, TS", positionY: "70%" },
  { name: "Rust", positionY: "90%" },
];

// DOMへのレンダリング処理
const container = document.getElementById('skill-labels');

if (container) {
  skillTiers.forEach((skill) => {
    const el = document.createElement('div');
    el.className = 'skill-label';
    el.textContent = skill.name;
    // Y座標(高さ)を設定
    el.style.top = skill.positionY;
    container.appendChild(el);
  });
}
//----------


//----------
// パッケージへのリンクボタン
const keisennoteButton = document.getElementById('keisennote-button') as HTMLButtonElement | null;
if (keisennoteButton) {
  keisennoteButton.addEventListener('click', () => {
    window.open('https://ctan.org/pkg/keisennote', '_blank');
  })
}

const gckanbunButton = document.getElementById('gckanbun-button') as HTMLButtonElement | null;
if (gckanbunButton) {
  gckanbunButton.addEventListener('click', () => {
    window.open('https://ctan.org/pkg/gckanbun', '_blank');
  })
}

const kkluaverbButton = document.getElementById('kkluaverb-button') as HTMLButtonElement | null;
if (kkluaverbButton) {
  kkluaverbButton.addEventListener('click', () => {
    window.open('https://ctan.org/pkg/kkluaverb', '_blank');
  })
}

const luwaulButton = document.getElementById('luwa-ul-button') as HTMLButtonElement | null;
if (luwaulButton) {
  luwaulButton.addEventListener('click', () => {
    window.open('https://ctan.org/pkg/luwa-ul', '_blank');
  })
}

const modernrulerButton = document.getElementById('modernruler-button') as HTMLButtonElement | null;
if (modernrulerButton) {
  modernrulerButton.addEventListener('click', () => {
    window.open('https://ctan.org/pkg/modernruler', '_blank');
  })
}

const kkranButton = document.getElementById('kkran-button') as HTMLButtonElement | null;
if (kkranButton) {
  kkranButton.addEventListener('click', () => {
    window.open('https://ctan.org/pkg/kkran', '_blank');
  })
}

const kksymbolsButton = document.getElementById('kksymbols-button') as HTMLButtonElement | null;
if (kksymbolsButton) {
  kksymbolsButton.addEventListener('click', () => {
    window.open('https://ctan.org/pkg/kksymbols', '_blank');
  })
}
//----------
