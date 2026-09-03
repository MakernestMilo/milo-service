# MakerNest Milo Service

M-01 — Stand the service up empty.

## Stack

Python + FastAPI.

Chosen because it provides a small, conventional HTTP service suitable for the M-01 runtime.

## Run locally

Python 3.11, as pinned in `.python-version`. These steps were run against 3.11.9.

Create and activate a virtual environment:

```
python3.11 -m venv .venv
source .venv/bin/activate
```

Activation is per terminal. A new window starts without it, and the symptom is
`ModuleNotFoundError` on the first command that needs a dependency.

Install both requirement sets. The dev set carries pytest and is required for
the tests:

```
python3 -m pip install -r requirements.txt -r requirements-dev.txt
```

Run the tests:

```
python3 -m pytest -q
```

Expected: `114 passed`.

Run the QC harness:

```
python3 qc.py
```

Expected first line: `5712 checks · 5712 pass · 0 fail`. The harness exits
non-zero if any check fails, or if a failure report matches no chapter, so its
exit status can be used as a gate.

Start the service:

```
python3 main.py
```

It listens on port 8000 unless `PORT` is set. Confirm it is up:

```
curl http://127.0.0.1:8000/health
```

Returns `status`, the build id, uptime, the chapter count (14), the session
store and whether it degraded, and the pause threshold in seconds.

## Deployment

`https://milo-service.onrender.com` — Render, free tier, deployed from `main`.

The build id in `/health` is the commit it is serving; check it against `main`
before reading anything into a run. The service sleeps when idle: a first
request after sleep took 22.4s on 2026-09-03, and the next took 0.18s.

`MODEL_API_KEY` and `SESSION_STORE_URL` are set in the Render environment and
exist nowhere in this repository — no file, no example, no fixture.

