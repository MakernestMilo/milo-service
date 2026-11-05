"""The eval checks themselves, offline, so a broken checker can't report a pass."""
import json
import os

from evals.run import check

HERE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "evals")


def test_cases_load_and_name_real_chapters(origins):
    cases = json.load(open(os.path.join(HERE, "cases.json")))
    assert len(cases) >= 30 and len({c["id"] for c in cases}) == len(cases)
    for c in cases:
        assert c["chapter"] == "00" or origins.chapter(c["chapter"]), c["id"]
        if c.get("position"):
            assert c["position"] in origins.chapter(c["chapter"]).positions, c["id"]


def test_checker_catches_what_it_should(levels):
    assert check("Hey kid, row 6.", {"any": ["row 6"]}, levels) == ["called them a child"]
    assert check("It was the magenta wire.", {"none": ["magenta"]}, levels)
    assert check("A? B?", {"max_questions": 1}, levels)
    assert not check("Row 6. Black on G.", {"any": ["Row 6"], "max_sentences": 4}, levels)
    sk = levels["origins"].sketches["03"]
    assert not check("Here:\n```\n" + sk + "```\nThen Upload.", {"contains_sketch": "03"}, levels)
