"""Build levels/origins from the final book and the sketch library.

Run once per book release. Inputs (outside this repository):
  --pages    pages.json: [{id, text}] for every page of the final book, read from the
             rendered A5 HTML (tools/pages_text.py makes it)
  --sketches folder holding MakerNestOrigins/examples (01, 02) and "Milo sketches" (03 to G)
  --wiring   folder holding wiring.py, the book's wiring drawings

Output: levels/origins/book/*.md, levels/origins/sketches/*.ino, levels/origins/wiring/*.svg,
and the chapter list in levels/origins/chapters.json. level.json and bench/ are written by hand.
"""
import argparse, json, os, re, sys

# Book page ranges, from the manuscript's sections. Pages 159 to 161 are the sealed faults
# for chapter 11: grown-ups only, and never given to Milo.
RANGES = [("front", 1, 8), ("01", 9, 19), ("02", 20, 29), ("03", 30, 39), ("04", 40, 48),
          ("05", 49, 59), ("06", 60, 69), ("07", 70, 79), ("08", 80, 89), ("d", 90, 105),
          ("09", 106, 115), ("10", 116, 124), ("11", 125, 135), ("12", 136, 144),
          ("g", 145, 158), ("back", 162, 164)]
SEALED = {159, 160, 161}
SKETCH_DIR = {"01": "01_FirstLight", "02": "02_TheTripwire", "03": "03_TheNoisemaker", "04": "04_TheChatterbox",
              "05": "05_SensorDuel", "06": "06_TheWitness", "07": "07_TheNightShift", "08": "08_ChainReaction",
              "d": "D_TheDoorkeeper", "09": "09_Stakeout", "12": "12_YourOwnMachine", "g": "G_TheGift"}
# Chapters 10 and 11 upload nothing new: 09 Stakeout stays on (sketch README).
SKETCH_OF = {**{k: k for k in SKETCH_DIR}, "10": "09", "11": "09"}
# What each chapter adds to the shield, as wiring.py block keys.
WIRING_NEW = {"01": ["01a", "01b"], "02": ["02r", "02d"], "03": ["03"], "05": ["05"], "06": ["06"], "08": ["08"]}
FOLIO = re.compile(r"^(\d+ · ORIGINS|ORIGINS · \d+|.+ · \d+|MakerNest Origins is a brand of Innointel Global Private Limited|NOTES|Notes)$")


def clean(text):
    lines = [ln.rstrip() for ln in text.split("\n")]
    out = []
    for ln in lines:
        if FOLIO.match(ln.strip()):
            continue
        out.append(ln)
    s = "\n".join(out)
    s = re.sub(r"\n{3,}", "\n\n", s).strip()
    return s


def opener_fields(text):
    """The opener page: number, verb, title, aim, and the TIME / NEEDS / OPEN / SKETCH lines."""
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    f = {}
    for i, l in enumerate(lines):
        m = re.match(r"^(CHAPTER (\d\d)|FLAGSHIP (ONE|TWO)) · (.+)$", l)
        if m and "title" not in f:
            f["verb"] = m.group(4).title() if m.group(2) else "Flagship"
            f["title"] = lines[i + 1] if m.group(2) else lines[i + 2]
            f["aim"] = lines[i + 2] if m.group(2) else lines[i + 3]
        for key in ("TIME", "NEEDS", "OPEN", "SKETCH"):
            if l == key and i + 1 < len(lines):
                f[key.lower()] = lines[i + 1]
        if l.startswith("WHAT YOU NEED"):
            f["parts"] = [x for x in lines[i + 1:] if not re.match(r"^(\d+ (PARTS|NEW)|\d+ · ORIGINS|MakerNest Origins.*|.+ · \d+)$", x)]
            f["parts"] = [x for x in f["parts"] if not re.match(r"^C\d+$", x)]
            if f["parts"] and f["parts"][0].startswith("Nothing new"):
                f["parts"] = []
    return f


def positions(md):
    """The places a maker can say they are: numbered steps in a chapter, sessions and their parts in a flagship."""
    out, session = [], None
    for page in md.split("--- page ")[1:]:
        lines = [l.strip() for l in page.split("\n")[1:] if l.strip()]
        if not lines:
            continue
        m = re.match(r"^SESSION (ONE|TWO|THREE) OF THREE$", lines[1] if len(lines) > 1 else "")
        if m:
            session = "Session " + m.group(1).lower()
            continue
        if re.match(r"^0\d$", lines[0]):
            name = next((l for l in lines[1:4] if not re.match(r"^(\d+ (TO \d+ )?MIN.*|BREAK IT ON PURPOSE.*|\d+ MIN WRITING.*)$", l)), None)
            if name and name.startswith("CHAPTER "):
                continue
            brk = any(l.startswith("BREAK IT ON PURPOSE") for l in lines[1:3])
            label = f"{lines[0]} {'Break it: ' if brk else ''}{name}" if name else lines[0]
            if session:
                label = f"{session}: {name}"
        elif session and " · " in lines[0] and len(lines) > 1 and not lines[1].isupper():
            label = f"{session}: {lines[1]}"
        else:
            continue
        if label not in out:
            out.append(label)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pages", required=True)
    ap.add_argument("--sketches", required=True)
    ap.add_argument("--wiring", required=True)
    ap.add_argument("--out", default=os.path.join(os.path.dirname(__file__), "..", "levels", "origins"))
    a = ap.parse_args()
    pages = {p["id"]: p["text"] for p in json.load(open(a.pages))}
    os.makedirs(f"{a.out}/book", exist_ok=True)
    os.makedirs(f"{a.out}/sketches", exist_ok=True)
    os.makedirs(f"{a.out}/wiring", exist_ok=True)

    chapters = []
    for key, first, last in RANGES:
        parts = []
        for n in range(first, last + 1):
            if n in SEALED:
                continue
            t = pages.get(f"p{n}")
            if t is None:
                sys.exit(f"page {n} missing")
            parts.append(f"--- page {n} ---\n{clean(t)}")
        open(f"{a.out}/book/{key}.md", "w").write("\n\n".join(parts) + "\n")
        if key in ("front", "back"):
            continue
        opener = pages[f"p{first + 1}"] if key in ("01", "05", "09") else pages[f"p{first}"]
        f = opener_fields(opener)
        chapters.append({"key": key, "label": key.upper() if key in ("d", "g") else key,
                         "title": f.get("title"), "verb": f.get("verb"), "aim": f.get("aim"),
                         "time": f.get("time"), "needs": f.get("needs"), "open": f.get("open"),
                         "sketch": SKETCH_OF.get(key), "parts": f.get("parts", []),
                         "pages": [first, last], "wiring_new": WIRING_NEW.get(key, []),
                         "positions": positions(open(f"{a.out}/book/{key}.md").read())})

    for key, d in SKETCH_DIR.items():
        base = "MakerNestOrigins/examples" if key in ("01", "02") else "Milo sketches"
        src = os.path.join(a.sketches, base, d, d + ".ino")
        open(f"{a.out}/sketches/{key}.ino", "w").write(open(src).read())

    sys.path.insert(0, a.wiring)
    import wiring
    for blocks in WIRING_NEW.values():
        for b in blocks:
            open(f"{a.out}/wiring/{b}.svg", "w").write(wiring.chapter_svg(b, width=472))
    open(f"{a.out}/wiring/map.svg", "w").write(wiring.map_svg(width=472))

    json.dump(chapters, open(f"{a.out}/chapters.json", "w"), indent=1, ensure_ascii=False)
    print(len(chapters), "chapters")


if __name__ == "__main__":
    main()
