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
// 1. パッケージ名のリストを作る
const ctanPackages = [
  'keisennote',
  'gckanbun',
  'kkluaverb',
  'luwa-ul',
  'modernruler',
  'kkran',
  'kksymbols'
];

// 2. リストをループして、一気にイベントを登録する
ctanPackages.forEach(pkgName => {
  const button = document.getElementById(`${pkgName}-button`) as HTMLButtonElement | null;
  
  if (button) {
    button.addEventListener('click', () => {
      window.open(`https://ctan.org/pkg/${pkgName}`, '_blank');
    });
  }
});
//----------
