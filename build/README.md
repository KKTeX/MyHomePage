# build/

`public/` is generated from the Claude Design canvas export, not hand-edited.
When a new export arrives, regenerate rather than patching `public/index.html`.

## Regenerating

Unpack the export (`design_handoff_kktex_portfolio/`) somewhere, then:

```
python3 build/convert.py "<export>/KKTeX Portfolio v2.dc.html" build/body.html
python3 build/assemble.py
```

`convert.py` strips the design-canvas runtime and rewrites its constructs into
plain HTML, writing three files: `body.html` plus `body.html.style` and
`body.html.hover` alongside it. `assemble.py` reads all three, wraps them in the
real `<head>` and writes `public/index.html`. None of the three are committed,
so `assemble.py` cannot be run until `convert.py` has been. Both assert on every substitution they expect to make, so
a canvas export whose structure has drifted fails loudly instead of silently
producing a broken page.

| prototype construct | becomes |
|---|---|
| `<sc-if value="{{ isJa }}">` | `data-l="ja"` on each child; CSS picks the language |
| `style-hover="…"` | a real `:hover` rule (`.hv1`…`.hv7`) |
| `ref="{{ barRef }}"` | `id="bar"`, driven by `public/site.js` |
| `onClick="{{ toggleLang }}"` | `id="langToggle"` |
| `{{ typed }}` | `#typed`, holding the full source so it survives no-JS |

Both languages are always in the DOM and CSS hides the inactive one. Nothing is
added or removed on a language switch, so a reveal cannot be stranded mid-
animation — the failure the handoff notes warn about.

## Hand-maintained files

- `build/head.css` — language switching, hover rules, typefaces, page gutter,
  responsive overrides. The design's own values stay in inline styles, so these
  use `!important` and select on inline-style substrings (`[style*="…"]`) where
  a type role has no class of its own.
- `build/assemble.py` — the `<head>`: meta, Open Graph, the font link, the
  JSON-LD, and the Google Search Console verification tag. **That verification
  tag must survive any regeneration** — removing it un-verifies the Search
  Console property. See the root [README](../README.md#do-not-remove).
- `public/site.js` — language toggle, progress bar, typewriter, scroll reveals.
- `build/og.html` — source for the 1200x630 social card. To re-render:
  ```
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless \
    --screenshot=og.png --window-size=1200,630 "file://$PWD/build/og.html"
  sips -s format jpeg -s formatOptions 88 og.png --out public/uploads/og.jpg
  ```
- `build/mcp-card.html` — source for the 1200x800 TeX64 MCP card image. It fans
  the three pages in `build/assets/mcp/`, which are the samples the MCP page
  itself publishes (`https://tex64.com/mcp/sample-{cover,body,exercise}.png`,
  fetched 2026-08-23) — a B5 lecture note the server typeset. To re-render:
  ```
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless \
    --force-device-scale-factor=2 --screenshot=mcp.png --window-size=1200,800 \
    "file://$PWD/build/mcp-card.html"
  sips -s format jpeg -s formatOptions 92 -Z 1200 mcp.png \
    --out public/uploads/tex64-mcp-og.jpg
  ```
  Render at 2x and let `sips -Z 1200` downsample; at 1x the page text in the
  fanned pages goes to mush.

## Images

Product cards hot-linked other sites' OG images in the prototype; they are
self-hosted in `public/uploads/` now. Re-fetch and re-compress with
`sips -s format jpeg -s formatOptions 80 -Z 1200 <src> --out <dest>`.

The TeX64 MCP card is the exception: it has no OG image worth reusing — the MCP
page's own `og:image` is just the TeX64 one, already on the card next to it —
so it gets a composed image instead. See `build/mcp-card.html` above.

## Edits that are not in the canvas export

`public/index.html` carries three body changes made by hand after the last
export, so regenerating from that export silently reverts them:

- the TeX64 MCP card's image. The export drew a CSS terminal mock
  (`$ curl mcp.tex64.com`) in the image slot; it is now an `<img>` matching the
  other three product cards.
- the 8th Packages cell. The export left a vermilion `typeset sample /
  組版サンプル` placeholder there; it is now the **paracolrule** card
  (CTAN, 2026-08-22), which fills the 4x2 grid exactly.
- the package count. Seven became eight in the two hero paragraphs, the `08`
  hero stat, the Packages heading, the About paragraphs and the 2025-26
  timeline row — and in `assemble.py`'s `DESC`/`DESC_EN`/JSON-LD and in
  `og.html`, which are regenerated from source and so are safe.

When the next export arrives, re-apply the first two before running
`assemble.py`, and check the counts against `ctan.org/author/kktex`.
