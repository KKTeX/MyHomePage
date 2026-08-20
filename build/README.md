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
plain HTML; `assemble.py` wraps the result in the real `<head>` and writes
`public/index.html`. Both assert on every substitution they expect to make, so
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
- `public/site.js` — language toggle, progress bar, typewriter, scroll reveals.
- `build/og.html` — source for the 1200x630 social card. To re-render:
  ```
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless \
    --screenshot=og.png --window-size=1200,630 "file://$PWD/build/og.html"
  sips -s format jpeg -s formatOptions 88 og.png --out public/uploads/og.jpg
  ```

## Images

Product cards hot-linked other sites' OG images in the prototype; they are
self-hosted in `public/uploads/` now. Re-fetch and re-compress with
`sips -s format jpeg -s formatOptions 80 -Z 1200 <src> --out <dest>`.

Still outstanding from the handoff: the 8th Packages cell is a vermilion
placeholder waiting on a real typeset sample image.
