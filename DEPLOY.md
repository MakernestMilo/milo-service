# Putting Milo live at makernest.com/origins

## 1. Render

The service already exists: `milo-service` on Render, deployed from `main`.

1. Merge the pull request. Render deploys it.
2. In the service's **Settings**, check the start command is `python3 main.py` (or
   `uvicorn main:app --host 0.0.0.0 --port $PORT`). Build command: `pip install -r requirements.txt`.
3. In **Environment**, check `MODEL_API_KEY`, `SESSION_STORE_URL` and `PANEL_TOKEN` are set.
4. Open `https://milo-service.onrender.com/health`. Expect `"store": "redis"`,
   `"model_configured": true` and `"origins": {"status": "live", "chapters": 14}`.
5. Open `https://milo-service.onrender.com/origins/01` on a phone and ask Milo something.

**The free tier sleeps.** The first visit after a quiet spell took 22 seconds in September. A
maker who opens a chapter page and waits 22 seconds will think it's broken. Before launch, move
the service to Render's Starter plan (always on).

## 2. makernest.com/origins

The book prints `makernest.com/origins/…`, so that address must reach this service. Pick one:

**A. A subdomain plus a forward (simplest).**
1. In Render, **Settings, Custom Domains**, add `milo.makernest.com`. Render shows a CNAME record.
2. At the domain registrar, add that CNAME. Render issues the certificate itself.
3. On the website, forward every path under `/origins` to `https://milo.makernest.com/origins`,
   keeping the rest of the path (`/origins/03` → `https://milo.makernest.com/origins/03`).
   Shopify, Wix, WordPress and Cloudflare all have a "URL redirect" with a wildcard for this.

The maker's browser then shows `milo.makernest.com/origins/03`. Every link in the book works.

**B. A proxy (the address bar stays on makernest.com).** If makernest.com sits behind
Cloudflare, add a Worker or a rule that proxies `makernest.com/origins*` to
`milo-service.onrender.com/origins*`. Same for `/static/*` and `/api/*`. Tell me what the website
runs on and I'll write the exact rule.

Either way, test every printed link afterwards: `/origins`, `/origins/00` to `/origins/12`,
`/origins/d`, `/origins/g`.

## 3. Before the first maker

- Run `python3 evals/run.py --n 3` with the real key and read the replies, chapter 11 first.
- Read the first week's conversations in the panel.
- The bench pack must be in the box before the bench pages are any use: see `BENCH-PACK.md`.
