# KKTeX Portfolio

Static single-page site, live at <https://kktexportfolio.klassikore.com/>.

`public/` is what ships. It is **generated**, not hand-authored — read
[build/README.md](build/README.md) before editing anything in it.

## Deploying

Cloudflare Pages project `kktexportfolio`. It is a **direct-upload project with
no Git connection**, so pushing to GitHub deploys nothing. Deploys are manual:

```bash
npx wrangler pages deploy public --project-name kktexportfolio --branch master
```

`--branch master` is not optional. The project's production branch is `master`;
any other branch name produces a *preview* deployment, which the custom domain
does not serve. `--branch main` looks like it worked and silently doesn't.

Check the result against the live domain rather than a browser, which caches:

```bash
curl -sSL https://kktexportfolio.klassikore.com/ | shasum -a 256
shasum -a 256 public/index.html
```

The two hashes must match. Give it about a minute first — for a short window
after a deploy the edge still serves the previous build from some locations, so
an immediate check can report a stale mismatch that resolves itself.

Note that `/index.html` 308-redirects to `/`, so fetch with `-L` or fetch `/`.

## Do not remove

```html
<meta name="google-site-verification" content="...">
```

in the `<head>` — it is in `build/assemble.py`'s head template and in the
generated `public/index.html`. This tag is the ownership proof for the Google
Search Console property `https://kktexportfolio.klassikore.com/` (URL-prefix
type, verified by meta tag rather than by the `google….html` file so that the
token survives a regeneration). Deleting it un-verifies the property, and the
sitemap and indexing reports stop working until it is verified again.

## Search assets

- **`public/sitemap.xml`** — a single URL. The site is one page with in-page
  anchors, and search engines ignore fragments, so listing the anchors would be
  wrong. Submitted in Search Console; update `<lastmod>` on substantive edits.

- **`public/robots.txt`** — allows everything and declares the sitemap.
  **Cloudflare prepends its own managed block to whatever this file contains.**
  The served `/robots.txt` therefore opens with a `Content-Signal:` section and
  `Disallow: /` rules for AI crawlers (ClaudeBot, GPTBot, CCBot, Google-Extended
  and others) before this file's contents appear. That block comes from the
  Cloudflare dashboard (AI Crawl Control), not from here, and editing this file
  cannot remove it. Search engines are unaffected — `Google-Extended` gates
  Gemini training, not Google Search — but while it stands, AI assistants will
  not cite the site.

- **JSON-LD** (`Person` + `WebSite`) in the `<head>`, also from `assemble.py`.
  Every claim in it is stated somewhere on the page; keep it that way rather
  than adding facts the page does not carry.

## Backlinks

The author byline at the foot of each Qiita article links here and is the only
set of links to the site that is not `nofollow`. The GitHub and Qiita profile
URL fields carry `rel="nofollow"` (GitHub adds `me`), so they help discovery and
human traffic but pass no ranking signal. CTAN's author page does not link here.
