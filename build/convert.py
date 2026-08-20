#!/usr/bin/env python3
"""Convert 'KKTeX Portfolio v2.dc.html' (Design Component prototype) into a
plain static page: no dc-runtime, no React, no unpkg.

Transforms
  <sc-if value="{{ isJa }}">…</sc-if>  -> data-l="ja" on each top-level child
  <sc-if value="{{ isEn }}">…</sc-if>  -> data-l="en" on each top-level child
  style-hover="…"                      -> class="hvN" + a real :hover rule
  ref="{{ barRef }}"                   -> id="bar"
  onClick="{{ toggleLang }}"           -> id="langToggle"
  {{ typed }} / {{ langLabel }}        -> real DOM the vanilla JS drives
Also injects data-* hooks the responsive stylesheet needs.
"""
import re, sys, json, pathlib

SRC = pathlib.Path(sys.argv[1])
OUT = pathlib.Path(sys.argv[2])
raw = SRC.read_text(encoding="utf-8")

# ---------------------------------------------------------------- extract ---
style = re.search(r"<style>(.*?)</style>", raw, re.S).group(1)
body  = re.search(r"</helmet>\s*(.*?)\s*</x-dc>", raw, re.S).group(1)

VOID = {"area","base","br","col","embed","hr","img","input","link",
        "meta","param","source","track","wbr"}
TAG  = re.compile(r"<(/?)([a-zA-Z][-\w]*)([^>]*?)(/?)>", re.S)

def add_attr_to_top_level(inner: str, attr: str) -> str:
    """Insert `attr` into the opening tag of every top-level element in `inner`."""
    out, depth, pos = [], 0, 0
    for m in TAG.finditer(inner):
        closing, name, attrs, selfclose = m.group(1), m.group(2).lower(), m.group(3), m.group(4)
        if closing:
            depth -= 1
            continue
        if depth == 0:
            out.append(inner[pos:m.start()])
            out.append(f"<{m.group(2)} {attr}{attrs}{'/' if selfclose else ''}>")
            pos = m.end()
        if not (selfclose or name in VOID):
            depth += 1
    out.append(inner[pos:])
    return "".join(out)

# ------------------------------------------------------------- 1. <sc-if> ---
SCIF = re.compile(r'<sc-if\s+value="\{\{\s*(isJa|isEn)\s*\}\}"[^>]*>(.*?)</sc-if>', re.S)
counts = {"isJa": 0, "isEn": 0}
def sub_scif(m):
    var, inner = m.group(1), m.group(2)
    counts[var] += 1
    lang = "ja" if var == "isJa" else "en"
    return add_attr_to_top_level(inner, f'data-l="{lang}" ')
body, n_scif = SCIF.subn(sub_scif, body)
assert "<sc-if" not in body, "unconverted sc-if remains"

# -------------------------------------------------------- 2. style-hover ---
hovers, hover_css = {}, []
def sub_hover(m):
    decls = m.group(1)
    if decls not in hovers:
        hovers[decls] = f"hv{len(hovers)+1}"
        hover_css.append(f".{hovers[decls]}:hover{{{decls.replace(';', '!important;')}!important}}")
    return f' class="{hovers[decls]}"'
body, n_hover = re.subn(r'\s*style-hover="([^"]*)"', sub_hover, body)

# ---------------------------------------------------------- 3. bindings ----
body, n_bar = re.subn(r'ref="\{\{\s*barRef\s*\}\}"', 'id="bar"', body)
body, n_tog = re.subn(r'onClick="\{\{\s*toggleLang\s*\}\}"',
                      'id="langToggle" type="button" aria-label="Switch language"', body)
body, n_lbl = re.subn(r'\{\{\s*langLabel\s*\}\}', 'EN', body)

LATEX = ("\\documentclass[a4paper]{jsarticle}\n"
         "\\usepackage{KKsymbols,KKran}\n"
         "\\usepackage{gckanbun}\n\n"
         "\\author{川口 晃世 (KKTeX)}\n"
         "\\title{Portfolio}\n\n"
         "\\begin{document}\n"
         "\\maketitle\n"
         "\\end{document}")
body, n_typed = re.subn(r'\{\{\s*typed\s*\}\}',
                        lambda _m: f'<span id="typed">{LATEX}</span>', body)

leftover = re.findall(r"\{\{[^}]*\}\}", body)
assert not leftover, f"unresolved bindings: {leftover}"

# ------------------------------------------------- 4. responsive hooks -----
hooks = [
  # (marker found inside the element's style attribute, hook attribute, expected count)
  ('gap:22px;font:500 11px/1 Archivo',                          'data-navlinks',  1),
  ('grid-template-columns:minmax(0,1.45fr) minmax(0,.85fr)',    'data-herogrid',  1),
  ('grid-template-columns:minmax(0,.75fr) minmax(0,1.25fr)',    'data-aboutgrid', 1),
  ('grid-template-columns:minmax(150px,.42fr) minmax(0,1fr)',   'data-tlrow',     6),
]
for marker, attr, expect in hooks:
    pat = re.compile(r'<div((?:(?!>)[^"]|"[^"]*")*?style="[^"]*'
                     + re.escape(marker) + r'[^"]*"[^>]*)>')
    body, got = pat.subn(lambda m, a=attr: f'<div {a}{m.group(1)}>', body)
    assert got == expect, f"hook {attr}: expected {expect}, injected {got}"

# ------------------------------------------------- 5. self-hosted OG art ---
IMG = {
  "https://tex64.com/og.jpg":                 "uploads/tex64-og.jpg",
  "https://mathhover.com/og-en.png":          "uploads/mathhover-og.jpg",
  "https://evolton.jp/og-image.png?v=20260811":"uploads/evolton-og.jpg",
}
for remote, local in IMG.items():
    assert remote in body, f"missing image src: {remote}"
    body = body.replace(remote, local)

# The hero shows the avatar at 112x112; ship a 512px copy, not the 1722px original.
assert body.count('uploads/NoTEXNoLIFE.jpeg') == 1
body = body.replace('uploads/NoTEXNoLIFE.jpeg', 'uploads/icon-512.jpg')

OUT.write_text(body, encoding="utf-8")
pathlib.Path(str(OUT) + ".style").write_text(style, encoding="utf-8")
pathlib.Path(str(OUT) + ".hover").write_text("\n".join(hover_css), encoding="utf-8")

print(json.dumps({
    "sc_if_converted": n_scif, "ja": counts["isJa"], "en": counts["isEn"],
    "style_hover": n_hover, "hover_classes": len(hovers),
    "barRef": n_bar, "toggleLang": n_tog, "langLabel": n_lbl, "typed": n_typed,
    "body_bytes": len(body),
}, indent=2, ensure_ascii=False))
