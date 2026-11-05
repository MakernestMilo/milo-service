"""The Milo service: the chapter pages the books link to, and Milo on each of them.

Routes a maker sees
  GET  /                         -> /origins
  GET  /{level}                  the level's home: every chapter, and Milo for getting started
  GET  /{level}/00               set up the computer, once
  GET  /{level}/{chapter}        a chapter page: sketch, wiring, bench, Ask Milo
  GET  /c/{chapter}              the September QR route, kept so old cards still land
Files
  GET  /{level}/{chapter}/sketch/{name}.ino   and   /{level}/{chapter}/bench/{name}.ino
  GET  /{level}/library/{zip}
API
  GET  /api/{level}/{chapter}/history?session=
  POST /api/{level}/{chapter}/turn   {session, text, position?, tab?}
Grown-ups and us
  GET  /health
  GET  /panel, POST /panel, GET /panel/c/{conversation}   (404 unless PANEL_TOKEN is set)
"""
import asyncio
import hmac
import hashlib
from urllib.parse import parse_qs
import logging
import os
import subprocess
import time
import uuid
import json

from fastapi import FastAPI, Request
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, PlainTextResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from . import guard, pages, prompt
from .levels import ROOT, Chapter, load_all
from .model import AnthropicModel, ModelUnavailable
from .store import Conversation, from_env

log = logging.getLogger("milo")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
HERE = os.path.dirname(os.path.abspath(__file__))
BOOTED = time.time()

# Chapter 11's hint ladder counts from when the maker says the hunt has started.
HUNTING = {"11": ("04 First test", "05 Find it")}

FALLBACK = ("I can't think straight right now, sorry. Try again in a minute. "
            "Your book has everything you need for this step, and the help table is on page 163.")
TOO_FAST = "Give me a moment to catch up. Try again in a minute."
TOO_LONG = "That's a lot for me in one go. Send the part you're stuck on, or the first error line."


def build_id():
    for k in ("GIT_COMMIT", "RENDER_GIT_COMMIT"):
        if os.getenv(k) and os.getenv(k) != "unknown":
            return os.getenv(k)[:7]
    try:
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=HERE, stderr=subprocess.DEVNULL).decode().strip()
    except Exception:
        return "unknown"


def setup_chapter(level):
    return Chapter(key="00", label="00", title="Starting out", verb="Setup",
                   aim="Get the computer ready, and find your way round the box.", time="", needs="", open="Top tray",
                   sketch_key=None, parts=[], positions=[s[0] for s in pages.SETUP], wiring_new=[],
                   book="The maker is on the level's home page or the set-up page (makernest.com/origins/00), not in a chapter. "
                        "Help with the box, the parts, power, setting up the computer and the first upload. "
                        "Set-up steps on the page: " + " ".join(f"{t}: {b}" for t, b, _ in pages.SETUP))


def create_app(model=None, store=None, levels=None, env=os.environ):
    app = FastAPI(title="MakerNest Milo", docs_url=None, redoc_url=None, openapi_url=None)
    app.state.levels = levels or load_all()
    app.state.model = model or AnthropicModel(env.get("MODEL_API_KEY"))
    if store is None:
        store, degraded = from_env(env)
    else:
        degraded = False
    app.state.store, app.state.degraded = store, degraded
    app.state.panel_token = env.get("PANEL_TOKEN") or None
    # Fast bursts are caught in each process; the hourly and daily limits are shared through the store.
    app.state.by_session = guard.RateLimit(per_minute=6, burst=10)
    app.state.by_address = guard.RateLimit(per_minute=30, burst=60)
    app.state.limits = {"session_hour": int(env.get("MILO_SESSION_PER_HOUR", "40")),
                        "address_hour": int(env.get("MILO_ADDRESS_PER_HOUR", "150")),
                        "day": int(env.get("MILO_DAILY_CAP", "5000"))}
    app.state.build = build_id()
    app.mount("/static", StaticFiles(directory=os.path.join(HERE, "static")), name="static")

    @app.middleware("http")
    async def headers_and_log(request: Request, call_next):
        rid = uuid.uuid4().hex[:12]
        started = time.monotonic()
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self'; "
            "connect-src 'self'; font-src 'self'; frame-ancestors 'self' https://makernest.com https://*.makernest.com; "
            "base-uri 'none'; form-action 'self'")
        # Never the body of a request or a reply: those are a maker's words.
        # The panel's paths name conversations, so they are never logged; nor is any query string.
        path = "/panel/…" if request.url.path.startswith("/panel") else request.url.path
        if path.startswith("/panel") or path.startswith("/api"):
            response.headers["Cache-Control"] = "no-store"
            response.headers["X-Robots-Tag"] = "noindex"
        log.info("rid=%s %s %s %s %.0fms", rid, request.method, path, response.status_code,
                 (time.monotonic() - started) * 1000)
        return response

    def live_level(level_id):
        lv = app.state.levels.get(level_id.lower())
        return lv

    def find(level_id, key):
        lv = live_level(level_id)
        if not lv or not lv.live:
            return lv, None
        k = key.lower()
        if k == "00":
            return lv, setup_chapter(lv)
        return lv, lv.chapter(k)

    # ---------------------------------------------------------------- pages
    @app.get("/", include_in_schema=False)
    def root():
        return RedirectResponse("/origins", status_code=302)

    @app.get("/health")
    def health():
        lv = app.state.levels
        return {"status": "ok", "build": app.state.build, "uptime_s": int(time.time() - BOOTED),
                "levels": {k: {"status": v.meta.get("status"), "chapters": len(v.chapters)} for k, v in lv.items()},
                "store": app.state.store.name, "store_degraded": app.state.degraded,
                "model": getattr(app.state.model, "name", "?"), "model_configured": bool(getattr(app.state.model, "configured", False))}

    @app.get("/c/{chapter}", include_in_schema=False)
    def old_card(chapter: str):
        return RedirectResponse(f"/origins/{chapter.lower()}", status_code=301)

    # ---------------------------------------------------------------- the panel
    # The token is typed into a form once and kept in a cookie scoped to /panel. It never appears in
    # a URL, so it never reaches a log, a browser history or a referrer.
    def panel_ok(request):
        tok = app.state.panel_token
        if not tok:
            return False
        want = hashlib.sha256(tok.encode()).hexdigest()
        got = request.cookies.get("milo_panel", "")
        return hmac.compare_digest(got.encode(), want.encode())

    @app.get("/panel", response_class=HTMLResponse, include_in_schema=False)
    def panel(request: Request):
        if not app.state.panel_token:
            return HTMLResponse(pages.not_found(), status_code=404)
        if not panel_ok(request):
            return pages.panel_login()
        return pages.panel_list(app.state.store.recent(100))

    @app.post("/panel", include_in_schema=False)
    async def panel_login(request: Request):
        if not app.state.panel_token:
            return HTMLResponse(pages.not_found(), status_code=404)
        body = (await request.body())[:2048].decode("utf-8", "replace")
        tok = (parse_qs(body).get("token") or [""])[0]
        if not hmac.compare_digest(tok.encode(), app.state.panel_token.encode()):
            await asyncio.sleep(1)
            return HTMLResponse(pages.panel_login(wrong=True), status_code=403)
        r = RedirectResponse("/panel", status_code=303)
        r.set_cookie("milo_panel", hashlib.sha256(tok.encode()).hexdigest(), max_age=8 * 3600,
                     path="/panel", httponly=True, samesite="strict",
                     secure=request.headers.get("x-forwarded-proto", request.url.scheme) == "https")
        return r

    @app.get("/panel/c/{key:path}", response_class=HTMLResponse, include_in_schema=False)
    def panel_one(request: Request, key: str):
        if not app.state.panel_token or not panel_ok(request):
            return HTMLResponse(pages.not_found(), status_code=404)
        c = app.state.store.get(key)
        if not c:
            return HTMLResponse(pages.not_found(), status_code=404)
        return pages.panel_one(key, c.__dict__)

    @app.get("/{level_id}/library/{name}", include_in_schema=False)
    def library(level_id: str, name: str):
        lv = live_level(level_id)
        path = os.path.join(ROOT, level_id.lower(), "library", name)
        if not lv or "/" in name or ".." in name or not name.endswith(".zip") or not os.path.isfile(path):
            return HTMLResponse(pages.not_found(lv), status_code=404)
        return FileResponse(path, media_type="application/zip", filename=name)

    @app.get("/{level_id}/{key}/sketch/{name}.ino", include_in_schema=False)
    def sketch_file(level_id: str, key: str, name: str):
        lv, ch = find(level_id, key)
        if not ch or not lv.sketch(ch.key) or name != ch.sketch_key:
            return PlainTextResponse("not found", status_code=404)
        return PlainTextResponse(lv.sketch(ch.key), headers={"Content-Disposition": f'attachment; filename="{name}.ino"'})

    @app.get("/{level_id}/{key}/bench/{name}.ino", include_in_schema=False)
    def bench_file(level_id: str, key: str, name: str):
        lv, ch = find(level_id, key)
        allowed = set()
        if ch and ch.bench:
            if ch.bench.get("sketch"):
                allowed.add(ch.bench["sketch"])
            for f in ch.bench.get("faults", []):
                if f.get("sketch"):
                    allowed.add(f["sketch"])
        if not ch or name not in allowed or name not in lv.bench_sketches:
            return PlainTextResponse("not found", status_code=404)
        return PlainTextResponse(lv.bench_sketches[name], headers={"Content-Disposition": f'attachment; filename="bench_{name}.ino"'})

    @app.get("/{level_id}", response_class=HTMLResponse)
    def level_home(level_id: str):
        lv = live_level(level_id)
        if not lv:
            return HTMLResponse(pages.not_found(), status_code=404)
        if level_id != lv.id:
            return RedirectResponse(f"/{lv.id}", status_code=301)
        if not lv.live:
            return pages.coming_level(lv)
        return pages.level_home(lv, app.state.levels)

    @app.get("/{level_id}/{key}", response_class=HTMLResponse)
    def chapter(level_id: str, key: str):
        lv, ch = find(level_id, key)
        if not lv:
            return HTMLResponse(pages.not_found(), status_code=404)
        if not lv.live:
            return pages.coming_level(lv)
        if not ch:
            return HTMLResponse(pages.not_found(lv), status_code=404)
        if key != ch.key or level_id != lv.id:
            return RedirectResponse(f"/{lv.id}/{ch.key}", status_code=301)
        if ch.key == "00":
            return pages.setup_page(lv)
        return pages.chapter_page(lv, ch)

    # ---------------------------------------------------------------- Milo
    def conv_key(lv, ch, session):
        return f"{lv.id}/{ch.key}/{session}"

    @app.get("/api/{level_id}/{key}/history")
    def history(level_id: str, key: str, session: str = ""):
        lv, ch = find(level_id, key)
        if not ch or not guard.SESSION_ID.match(session or ""):
            return JSONResponse({"turns": []}, status_code=404 if not ch else 400)
        try:
            c = app.state.store.get(conv_key(lv, ch, session))
        except Exception as e:
            log.error("store read failed: %s", type(e).__name__)
            c = None
        return {"turns": [{"who": t["who"], "said": t["said"]} for t in (c.turns if c else [])],
                "position": c.position if c else None}

    def client_address(request):
        """Render appends the address it saw to X-Forwarded-For, so the right-most entry is the real one.
        Anything to its left was written by the client and can't be trusted."""
        xff = [p.strip() for p in request.headers.get("x-forwarded-for", "").split(",") if p.strip()]
        if xff:
            return xff[-1]
        return request.client.host if request.client else "?"

    def over_limit(session, address):
        if not app.state.by_session.allow(session) or not app.state.by_address.allow(address):
            return True
        st, lim = app.state.store, app.state.limits
        try:
            hour = time.strftime("%Y%m%d%H", time.gmtime())
            if st.count(f"s:{session}:{hour}", 3600) > lim["session_hour"]:
                return True
            if st.count(f"a:{address}:{hour}", 3600) > lim["address_hour"]:
                return True
            if st.count("day:" + time.strftime("%Y%m%d", time.gmtime()), 2 * 86400) > lim["day"]:
                log.error("daily turn cap reached")
                return True
        except Exception as e:  # a store hiccup must not stop every maker
            log.warning("limit store error: %s", type(e).__name__)
        return False

    @app.post("/api/{level_id}/{key}/turn")
    async def turn(level_id: str, key: str, request: Request):
        lv, ch = find(level_id, key)
        if not ch:
            return JSONResponse({"error": "no such chapter"}, status_code=404)
        if int(request.headers.get("content-length") or 0) > guard.MAX_BODY_BYTES:
            return JSONResponse({"reply": TOO_LONG}, status_code=413)
        raw = b""
        async for chunk in request.stream():
            raw += chunk
            if len(raw) > guard.MAX_BODY_BYTES:
                return JSONResponse({"reply": TOO_LONG}, status_code=413)
        try:
            body = json.loads(raw)
        except Exception:
            return JSONResponse({"error": "bad request"}, status_code=400)
        session = body.get("session") if isinstance(body, dict) else None
        if not isinstance(session, str) or not guard.SESSION_ID.match(session):
            return JSONResponse({"error": "bad session"}, status_code=400)
        if over_limit(session, client_address(request)):
            return JSONResponse({"reply": TOO_FAST, "retry": True}, status_code=429)
        try:
            text, redacted = guard.clean(body.get("text"))
        except ValueError as e:
            if str(e) == "too_long":
                return JSONResponse({"reply": TOO_LONG}, status_code=413)
            return JSONResponse({"error": "empty"}, status_code=400)
        position = body.get("position")
        if position not in ch.positions:
            position = None
        tab = body.get("tab") if body.get("tab") in ("sketch", "wiring", "bench", "milo") else None

        store = app.state.store
        ck = conv_key(lv, ch, session)
        try:
            c = await run_in_threadpool(store.get, ck)
        except Exception as e:
            log.error("store read failed: %s", type(e).__name__)
            return JSONResponse({"reply": FALLBACK, "retry": True}, status_code=503)
        c = c or Conversation(level=lv.id, chapter=ch.key)
        if position:
            c.set_position(position, HUNTING.get(ch.key, ()))
        c.add("maker", text)
        system = prompt.system_blocks(lv, ch, position=c.position, minutes=c.minutes(), turns=c.milo_turns(), tab=tab)
        try:
            reply = await run_in_threadpool(app.state.model.reply, system, c.messages())
        except ModelUnavailable as e:
            log.warning("model unavailable: %s", e)
            return JSONResponse({"reply": FALLBACK, "retry": True}, status_code=503)
        c.add("milo", reply)
        try:
            await run_in_threadpool(store.put, ck, c)
        except Exception as e:  # the maker still gets the reply; only the memory of it is lost
            log.error("store write failed: %s", type(e).__name__)
        out = {"reply": reply}
        if redacted:
            out["note"] = "I took out a phone number or email address. Milo doesn't need them."
        return out

    @app.exception_handler(404)
    async def nf(request, exc):
        return HTMLResponse(pages.not_found(), status_code=404)

    return app
