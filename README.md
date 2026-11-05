# MakerNest Milo

Milo is the mentor on every chapter page the MakerNest books link to. One service, four levels:
**Origins** (live), Motion, Connected and Autonomy (listed as coming, filled the same way).

The book prints `makernest.com/origins` and `makernest.com/origins/00` to `/12`, `/d` and `/g`.
Every one of those is a page here:

| Page | What the maker gets |
|---|---|
| `/origins` | Every chapter, by act. Milo for questions about the box and getting started. |
| `/origins/00` | Set up the computer once: Arduino IDE, the CH340 driver, the MakerNest Origins library. |
| `/origins/01` … `/12`, `/d`, `/g` | The chapter's sketch (copy or download), its wiring drawings and the whole shield, the bench experiment with a breadboard drawing and its own sketch, and Ask Milo. |

## How Milo works

- **The book is the source.** Milo is given the chapter's pages exactly as printed, the front and
  back of the book, the kit's hardware facts, the chapter's sketch and its bench experiment
  (`milo/prompt.py`). It answers only from that. The sealed faults for chapter 11 (book pages 159
  to 161) are never given to it.
- **The maker says where they are.** Each chapter page has a "Where are you?" picker with that
  chapter's steps. Milo is told the step and believes it; it never infers it.
- **Sketches.** Milo gives a chapter's sketch exactly, never a different one. In chapter 12 and the
  Gift it writes code with the maker one line at a time, from the starter sketch.
- **Chapter 11.** Milo holds the book's hint ladder against the minutes the maker has been
  looking, and never names the fault.
- **Voice.** `milo/voice.md`: the book's voice, two to four sentences, one question at most,
  never "child", the maker's decisions stay the maker's, safety and privacy rules, and a
  kind route to a trusted grown-up and Childline 1098 if a maker is in trouble.
- **Privacy.** Phone numbers and email addresses are removed before anything is stored or sent
  (`milo/guard.py`). Conversations are kept 7 days (`MILO_KEEP_DAYS`). Request bodies are never logged.

## Content

`levels/origins/` holds everything a level needs:

| Path | What | Made by |
|---|---|---|
| `level.json` | Name, colours, chapter order, hardware facts, safety, errata | hand |
| `chapters.json`, `book/*.md` | Each chapter's printed pages, and its steps | `tools/build_origins.py` from the final book |
| `sketches/*.ino` | 01 and 02 from the library examples, 03 to G from "Milo sketches" | `tools/build_origins.py` |
| `wiring/*.svg` | The book's wiring drawings | `tools/build_origins.py`, using the book's `wiring.py` |
| `bench/bench.json` | 13 bench experiments and chapter 11's five faults | hand |
| `bench/sketches/*.ino` | Bench sketches. All compile for the UNO. None touches EEPROM. | hand |
| `bench/svg/*.svg` | Breadboard drawings, from the same columns as the steps | `tools/bench_svg.py` |
| `library/` | The MakerNest Origins library zip, until it is in Library Manager | copied |

To fill Motion, Connected or Autonomy: make the same folder, set `"status": "live"`, and run the
tests. Nothing in the code is Origins-specific except `pages.SETUP`.

When the book changes: render it to `pages.json` with `tools/pages_text.py`, then run
`tools/build_origins.py --pages … --sketches … --wiring …` and the tests.

## Run locally

Python 3.11.

```
python3.11 -m venv .venv && source .venv/bin/activate
python3 -m pip install -r requirements.txt -r requirements-dev.txt
python3 -m pytest -q
python3 main.py            # http://127.0.0.1:8000/origins
```

Without `MODEL_API_KEY` the pages work and Ask Milo answers that it can't think right now.

## Check Milo's replies against the real model

```
MODEL_API_KEY=… python3 evals/run.py --n 3
```

Thirty scripted messages: sketch requests, wiring facts, the decision steps, chapter 11 pressure,
code coaching, battery and mains safety, privacy, prompt injection, off-topic, distress, Tamil.
The checks are form checks: read the replies in the results file it writes.

## Where it runs

On one server in AWS's Mumbai region, through AWS India, billed in rupees: Milo, its Redis and
Caddy for HTTPS, from `docker-compose.yml`. `DEPLOY.md` sets it up from nothing; every merge to
`main` that passes CI is deployed by `.github/workflows/deploy.yml`.

| Variable (in `/opt/milo/.env` on the server) | |
|---|---|
| `DOMAIN` | `milo.makernest.com` |
| `MODEL_API_KEY` | Anthropic key. Never in this repository. |
| `PANEL_TOKEN` | Opens `/panel`. Unset means 404. |
| `MILO_MODEL`, `MILO_KEEP_DAYS`, `MILO_DAILY_CAP` | Optional. |

`SESSION_STORE_URL` is set by `docker-compose.yml` to the server's own Redis. `/health` gives
the build, the levels, the store and whether the model key is set.

## The September service

The first Milo (work orders M-01 to M-13) was built on the September book. Its rules no longer
match the final book (USB-only power, no sketches, no code writing), so it is kept for reference
in `legacy/` and is not run.
