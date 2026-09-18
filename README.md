# True Wellness Site

Static website for True Wellness (truewellness.life): product portfolio from two origins (Quiron CBD, USA and CanniFex, Switzerland), pages by condition, article library, company history and legal pages.

## Structure

- `index.html` — home
- `portfolio.html` — full portfolio with origin/category filters
- `conditions.html`, `condition-*.html` — support by condition
- `articles.html`, `article-*.html` — article library
- `history.html` — company history
- `*-spectrum-*.html`, `swiss-*.html`, `delta-9-*.html`, `cbg-*.html`, `relief-rub-*.html`, `weight-control-softgels.html` — product pages
- `terms-of-service.html`, `privacy-policy.html`, `shipping-policy.html`, `refund-policy.html`, `sitemap.html`, `sitemap.xml`
- `cdn/shop/files/` — images; `cdn/shop/t/85/assets/` — theme CSS/JS

## Run locally

```bash
python3 -m http.server 8777
```

Open http://localhost:8777/. The age gate stores its confirmation in `localStorage` (`tw_age_ok`).

## Deploy (Cloudflare Workers static assets)

Some theme asset filenames contain `?`, `&` and `=` (inherited from the Shopify export). The build script copies the site to `dist/`, renames those files and rewrites references:

```bash
python3 scripts/build-deploy.py && cd dist && npx wrangler deploy
```

Production: https://true-wellnes-website.luizotaviobsr.workers.dev

Note: because of those filenames, clone this repo on macOS or Linux (Windows cannot check out files with `?` in the name).
