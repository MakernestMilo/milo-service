"""The four levels, loaded once at boot from levels/<id>/.

A level is live when its level.json says "status": "live" and its chapters, book text and
sketches are all present. Motion, Connected and Autonomy are listed but "coming" until their
folders are filled the way Origins is.
"""
import json
import os
from dataclasses import dataclass, field

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "levels")
LEVEL_ORDER = ["origins", "motion", "connected", "autonomy"]


@dataclass
class Chapter:
    key: str
    label: str
    title: str
    verb: str
    aim: str
    time: str
    needs: str
    open: str
    sketch_key: str | None
    parts: list
    positions: list
    wiring_new: list
    book: str
    bench: dict | None = None

    @property
    def slug(self):
        return self.key


@dataclass
class Level:
    id: str
    meta: dict
    chapters: dict = field(default_factory=dict)
    order: list = field(default_factory=list)
    front: str = ""
    back: str = ""
    sketches: dict = field(default_factory=dict)
    wiring: dict = field(default_factory=dict)
    bench: dict = field(default_factory=dict)
    bench_sketches: dict = field(default_factory=dict)
    bench_svg: dict = field(default_factory=dict)

    @property
    def live(self):
        return self.meta.get("status") == "live"

    @property
    def name(self):
        return self.meta["name"]

    def chapter(self, key):
        return self.chapters.get(key.lower())

    def sketch(self, key):
        """The sketch a chapter uploads: its own, or the one that stays on (10 and 11 keep 09)."""
        ch = self.chapter(key)
        if not ch or not ch.sketch_key:
            return None
        return self.sketches.get(ch.sketch_key)


def _read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def load_level(level_id, root=ROOT):
    d = os.path.join(root, level_id)
    meta = json.loads(_read(os.path.join(d, "level.json")))
    lv = Level(id=level_id, meta=meta)
    if meta.get("status") != "live":
        return lv
    lv.front = _read(os.path.join(d, "book", "front.md"))
    lv.back = _read(os.path.join(d, "book", "back.md"))
    for name in sorted(os.listdir(os.path.join(d, "sketches"))):
        if name.endswith(".ino"):
            lv.sketches[name[:-4]] = _read(os.path.join(d, "sketches", name))
    for name in sorted(os.listdir(os.path.join(d, "wiring"))):
        if name.endswith(".svg"):
            lv.wiring[name[:-4]] = _read(os.path.join(d, "wiring", name))
    bench_path = os.path.join(d, "bench", "bench.json")
    if os.path.exists(bench_path):
        lv.bench = json.loads(_read(bench_path))
        for name in sorted(os.listdir(os.path.join(d, "bench", "sketches"))):
            if name.endswith(".ino"):
                lv.bench_sketches[name[:-4]] = _read(os.path.join(d, "bench", "sketches", name))
        for name in sorted(os.listdir(os.path.join(d, "bench", "svg"))):
            if name.endswith(".svg"):
                lv.bench_svg[name[:-4]] = _read(os.path.join(d, "bench", "svg", name))
    for c in json.loads(_read(os.path.join(d, "chapters.json"))):
        ch = Chapter(key=c["key"], label=c["label"], title=c["title"], verb=c["verb"], aim=c["aim"],
                     time=c["time"], needs=c["needs"], open=c["open"], sketch_key=c["sketch"],
                     parts=c["parts"], positions=c["positions"], wiring_new=c["wiring_new"],
                     book=_read(os.path.join(d, "book", f"{c['key']}.md")),
                     bench=(lv.bench.get("experiments") or {}).get(c["key"]))
        lv.chapters[ch.key] = ch
    lv.order = meta["order"]
    missing = [k for k in lv.order if k not in lv.chapters]
    if missing:
        raise ValueError(f"{level_id}: chapters listed in level.json but not built: {missing}")
    return lv


def load_all(root=ROOT):
    return {lid: load_level(lid, root) for lid in LEVEL_ORDER if os.path.exists(os.path.join(root, lid, "level.json"))}
