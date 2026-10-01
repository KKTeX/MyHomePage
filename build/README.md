# build/

Sources for the images in `public/uploads/`. The page itself is not built:
`public/index.html`, `public/style.css` and `public/site.js` are edited by hand.

Until 2026-09-27 the page was generated from a Claude Design canvas export by
`convert.py` + `assemble.py`, with `head.css` layered on top. That export is no
longer on disk, and the page has since been redesigned in the claude.com idiom
(see the header comment in `public/style.css` for the palette and the typeface
substitutions), so those scripts were removed. They are in git history before
that date if the old design is ever wanted back.

## Product card images

`cards/*.html` compose the three images on the Products section. Each is a flat
plate in one of the page's palette colours with the product's own current UI or
output laid on it. The only drawn element is the request bubble on the MCP
card.

| card | plate | source in `assets/` | where the source came from |
|---|---|---|---|
| `tex64.html` | oat `#E3DACC` | `cards/tex64-app.png` | `https://tex64.com/marketing/tex64-spectral-app-clean.png` |
| `evolton.html` | cactus `#BCD1CA` | `cards/evolton-answer.png`, `cards/evolton-bank.png` | `https://evolton.jp/home-todai-exam-prep-template.png`, `/home-problem-bank.png` |
| `mcp.html` | clay `#D97757` | `mcp/sample-{cover,body,exercise}.png` | `https://tex64.com/mcp/sample-{cover,body,exercise}.png` |

All fetched 2026-09-27.

`mcp.html` is 1200x960 rather than 1200x800: it fills the image half of the
page's featured card, which sits near 5:4 on desktop. Its speech bubble is the
first starter prompt the ChatGPT plugin is published with, and the three pages
are the samples tex64.com publishes for that request — keep the two matched if
either changes.

To re-render one (`mcp` needs `--window-size=1200,960`):

```
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless \
  --allow-file-access-from-files --virtual-time-budget=8000 \
  --force-device-scale-factor=2 --screenshot=card.png --window-size=1200,800 \
  "file://$PWD/build/cards/tex64.html"
sips -s format jpeg -s formatOptions 86 -Z 1200 card.png \
  --out public/uploads/tex64-card.jpg
```

Output names: `tex64-card.jpg`, `evolton-card.jpg`, `tex64-mcp-card.jpg`. Render at 2x and let `sips -Z 1200` downsample; at 1x the
text inside the screenshots goes to mush. `--allow-file-access-from-files` is
what lets the page load the images beside it.

## Social card

`og.html` is the 1200x630 Open Graph / Twitter image:

```
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless \
  --virtual-time-budget=8000 --force-device-scale-factor=2 \
  --screenshot=og.png --window-size=1200,630 "file://$PWD/build/og.html"
sips -s format jpeg -s formatOptions 88 -Z 1200 og.png --out public/uploads/og.jpg
```

## Facts on the page that come from elsewhere

- **Package count** (eight): the hero paragraph, the `08` stat, the Packages
  heading, About, the 2025–26 timeline row, `og.html`, and the `<meta>`
  descriptions and JSON-LD in the `<head>`. Check against
  `ctan.org/author/kktex`.
- **Product count** (three): the `3` stat in the hero counts the Fermion
  products the page shows — TeX64, TeX64 MCP, Evolton. MathHover was taken off
  the page on 2026-09-27 at the author's request; keep the stat matched to the
  cards rather than to Fermion's full lineup.
- **TeX64 MCP in ChatGPT**: published in the ChatGPT plugin directory
  (Education & Research) at
  `https://chatgpt.com/plugins/plugin_asdk_app_6a8abcc3f22c819196d21cf6e44e3a3b`.
  The Claude plugin is on GitHub (`Fermion-company/tex64-claude-plugin`) and
  its Anthropic directory listing was under review as of 2026-09-27; update the
  featured card's "Claude" row when that changes. The record of both is in the
  TeX64-mcp repo, `plugins/tex64/submission/`.
