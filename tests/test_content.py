"""The Origins content is complete, matches the printed book, and keeps the sealed faults out."""
import json
import os
import re

from milo.levels import LEVEL_ORDER, ROOT

BOOK_LINKS = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "d", "09", "10", "11", "12", "g"]


def test_four_levels_in_order(levels):
    assert list(levels) == LEVEL_ORDER
    assert levels["origins"].live
    for k in ("motion", "connected", "autonomy"):
        assert levels[k].meta["status"] == "coming"


def test_every_chapter_is_built(origins):
    assert origins.order == ["01", "02", "03", "04", "05", "06", "07", "08", "d", "09", "10", "11", "12", "g"]
    for k in origins.order:
        ch = origins.chapter(k)
        assert ch.title and ch.aim and ch.verb
        assert len(ch.book) > 2000, k
        assert len(ch.positions) >= 6, k


def test_titles_match_the_book(origins):
    titles = {k: origins.chapter(k).title for k in origins.order}
    assert titles == {"01": "First Light", "02": "The Tripwire", "03": "The Noisemaker", "04": "The Chatterbox",
                      "05": "Sensor Duel", "06": "The Witness", "07": "The Night Shift", "08": "Chain Reaction",
                      "d": "The Doorkeeper", "09": "Stakeout", "10": "The Creature", "11": "Sabotage",
                      "12": "Your Own Machine", "g": "The Gift"}


def test_every_chapter_has_its_sketch(origins):
    for k in origins.order:
        sk = origins.sketch(k)
        assert sk and "#include <MakerNestOrigins.h>" in sk, k
    # 10 and 11 upload nothing new: Stakeout stays on.
    assert origins.chapter("10").sketch_key == "09" and origins.chapter("11").sketch_key == "09"


def test_sketches_01_and_02_are_the_printed_ones(origins):
    book01 = origins.chapter("01").book
    for line in origins.sketches["01"].splitlines():
        line = line.strip()
        if line and not line.startswith("//"):
            assert line in book01, line


def test_wiring_drawings_exist(origins):
    for k in origins.order:
        for b in origins.chapter(k).wiring_new:
            assert b in origins.wiring and origins.wiring[b].startswith("<svg")
    assert "map" in origins.wiring


def test_sealed_faults_never_reach_milo(origins):
    everything = origins.front + origins.back + "".join(origins.chapter(k).book for k in origins.order)
    for s in ("THE SEALED FAULTS", "Tear along the line", "FAULT 1 · KINDEST", "Pull the buzzer's magenta wire off row 6",
              "set the cold line to 0 degrees", "set step 2 of the sequence to NONE", "Move the door magnet a centimetre out of line"):
        assert s not in everything, s


def test_bench_covers_every_chapter_but_the_gift(origins):
    ex = origins.bench["experiments"]
    assert set(ex) == set(origins.order) - {"g"}
    for k, b in ex.items():
        assert b["title"], k
        if b.get("sketch"):
            assert b["sketch"] in origins.bench_sketches, k
        if k not in ("11", "12") and b.get("breadboard", True):
            assert (b.get("same_circuit_as") or k) in origins.bench_svg, k
    faults = ex["11"]["faults"]
    assert [f["n"] for f in faults] == [1, 2, 3, 4, 5]
    for f in faults:
        assert len(f["hints"]) == 3 and f["answer"]
        assert f"f{f['n']}" in origins.bench_svg


def test_bench_titles_are_the_printed_ones(origins):
    """Each bench title is the ON THE BENCH line printed in that chapter."""
    for k, b in origins.bench["experiments"].items():
        page = origins.chapter(k).book
        m = re.search(r"ON THE BENCH\s+(.+?)[.(]", page)
        assert m, k
        assert m.group(1).strip().rstrip(".").lower() == b["title"].lower(), (k, m.group(1), b["title"])


def test_bench_parts_are_kit_or_bench_pack(origins):
    known = set(origins.bench["parts"])
    for k, b in origins.bench["experiments"].items():
        for p in b.get("parts", []):
            assert p in known, (k, p)


def test_bench_uses_only_free_rows(origins):
    machine_rows = {"row 2", "row 3", "row 4", "row 5", "row 6", "row 7", "row 8", "row 9", "row 11", "A4", "A5"}
    for k, b in origins.bench["experiments"].items():
        for w in b.get("wiring", []):
            pin = w[0]
            if pin.startswith("battery"):
                continue
            assert not any(pin.startswith(r + " ") for r in machine_rows), (k, pin)


def test_bench_sketches_never_touch_saved_memory(origins):
    for name, code in origins.bench_sketches.items():
        assert "EEPROM" not in code, name
        assert "MakerNestOrigins" not in code, name


def test_book_links_all_have_pages(client):
    for k in BOOK_LINKS:
        assert client.get(f"/origins/{k}").status_code == 200, k


def test_errata_correct_the_help_table(origins):
    assert "yellow wire is loose" in origins.back          # the printed mistake is still in the book text...
    assert any("blue" in e for e in origins.meta["errata"])  # ...and the errata tell Milo the truth


def test_level_json_is_valid():
    for lid in LEVEL_ORDER:
        json.load(open(os.path.join(ROOT, lid, "level.json")))
