#!/usr/bin/env python3
"""Assemble public/index.html from the converted body + head/CSS."""
import re, pathlib, sys

B    = pathlib.Path(__file__).resolve().parent
OUT  = B.parent / "public" / "index.html"
SITE = "https://kktexportfolio.klassikore.com"

body     = (B / "body.html").read_text(encoding="utf-8")
base_css = (B / "body.html.style").read_text(encoding="utf-8").strip()
hover_css= (B / "body.html.hover").read_text(encoding="utf-8").strip()
extra_css= (B / "head.css").read_text(encoding="utf-8").strip()

def hook(marker, attr, expect):
    """Add `attr` to every <div> whose style attribute contains `marker`."""
    global body
    pat = re.compile(r'<div((?:(?!>)[^"]|"[^"]*")*?style="[^"]*'
                     + re.escape(marker) + r'[^"]*"[^>]*)>')
    body, got = pat.subn(lambda m: f'<div {attr}{m.group(1)}>', body)
    assert got == expect, f"{attr}: expected {expect}, injected {got}"

hook('repeat(auto-fill,minmax(290px,1fr))', 'data-cardgrid', 1)   # packages
hook('repeat(auto-fill,minmax(320px,1fr))', 'data-cardgrid', 1)   # products
hook('background:#0E0E0E;padding:22px 0 0 20px', 'data-stat', 2)  # hero stats

# Wrap the five nav anchors so they can scroll sideways on narrow screens
# without dragging the language toggle out of reach.
nav_pat = re.compile(r'(<a href="#about".*?#writing"[^>]*>Writing</a>)', re.S)
body, n = nav_pat.subn(
    r'<div data-navscroll style="display:flex;align-items:center;gap:22px">\1</div>', body)
assert n == 1, f"nav wrap: {n}"

TITLE = "川口 晃世 / KKTeX — Portfolio"
DESC  = ("TeXで組版の道具をつくっています。CTAN公式パッケージ7本の著作者、"
         "株式会社Fermion共同創業者、東京大学理科一類1年。")
DESC_EN = ("Kosei Kawaguchi (KKTeX) — author of seven packages on CTAN, "
           "co-founder of Fermion Inc., first-year student at the University of Tokyo.")

head = f'''<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{TITLE}</title>
<meta name="description" content="{DESC}">
<meta name="author" content="川口 晃世 (KKTeX)">
<meta name="theme-color" content="#0E0E0E">
<link rel="canonical" href="{SITE}/">

<meta property="og:type" content="website">
<meta property="og:site_name" content="KKTeX">
<meta property="og:url" content="{SITE}/">
<meta property="og:title" content="{TITLE}">
<meta property="og:description" content="{DESC}">
<meta property="og:image" content="{SITE}/uploads/og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{DESC_EN}">
<meta property="og:locale" content="ja_JP">
<meta property="og:locale:alternate" content="en_US">

<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@KKTeX_LaTeX3">
<meta name="twitter:creator" content="@KKTeX_LaTeX3">
<meta name="twitter:title" content="{TITLE}">
<meta name="twitter:description" content="{DESC}">
<meta name="twitter:image" content="{SITE}/uploads/og.jpg">

<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="uploads/icon-512.jpg">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700&amp;family=Zen+Old+Mincho:wght@400;500;700&amp;family=EB+Garamond:ital,wght@0,400;0,500;1,400&amp;family=JetBrains+Mono:wght@300;400;500&amp;display=swap" rel="stylesheet">

<style>
{base_css}

/* ── hover states ───────────────────────────────────────────────────────────
   The prototype carried these on a style-hover attribute its runtime read;
   here they are ordinary :hover rules. !important because the base values are
   inline styles. */
{hover_css}
{extra_css}
</style>'''

doc = f'''<!DOCTYPE html>
<html lang="ja">
<head>
{head}
</head>
<body>
{body}
<script src="site.js" defer></script>
</body>
</html>
'''

OUT.write_text(doc, encoding="utf-8")
print(f"wrote {OUT} ({len(doc):,} bytes)")
