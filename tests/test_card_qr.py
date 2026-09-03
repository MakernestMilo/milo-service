"""The card's QR code — M-10 step 02.

The artefact under test is printed, and a printed mistake cannot be patched.
So the tests here are about the things that would reach a card silently: the
host written down in two places drifting apart, a longer URL pushing the symbol
to a denser version and quietly taking the smallest print size below what a
phone can read, and the payload simply not being the URL.

What is deliberately *not* claimed: the decoder in tools/qr_read.py is
exercised against symbols segno generated, so a fault both implementations
shared would pass here. The evidence that a real detector agrees is a phone,
and that is step 02's own acceptance rather than a test.
"""
import pathlib
import re

import pytest

import corpus
from tools import make_card_qr as mk
from tools import qr_read


ROOT = pathlib.Path(__file__).resolve().parent.parent
CARD = ROOT / "card"

# A printed module below this is where cheap printing and phone cameras start
# to fail. It is a floor, not a target.
FLOOR_MM = 0.50


def test_the_host_is_written_down_in_two_places_and_they_agree():
    readme = (ROOT / "README.md").read_text()
    assert mk.SERVICE in readme, (
        f"{mk.SERVICE} is not the host the README names")
    hosts = set(re.findall(r"https://[a-z0-9.-]+\.onrender\.com", readme))
    assert hosts == {mk.SERVICE}, f"the README names {hosts}"


def test_the_url_is_built_from_the_chapter_and_only_from_the_chapter():
    assert mk.url_for("01") == f"{mk.SERVICE}/c/01"
    for key in corpus.BY_KEY:
        assert mk.url_for(key).endswith("/c/" + key)


def test_a_chapter_the_service_does_not_have_cannot_be_printed():
    with pytest.raises(KeyError):
        mk.write("99")


def test_the_committed_symbol_decodes_to_the_committed_url():
    """Read back by an independent decoder, not by segno."""
    got = qr_read.decode(CARD / "chapter-01-decode-check.png")
    assert got["payload"] == mk.url_for("01")
    assert got["ec"] == "Q", "the card's error correction level changed"
    assert got["format_distance"] == 0, (
        "the format bits are not an exact match for any legal value")


def test_the_smallest_print_size_stays_above_the_floor():
    """The failure this catches is not in this file.

    A longer URL — a different host, a path with a slug in it — pushes the
    symbol to a denser version, which at a fixed 20 mm makes every module
    smaller. Nothing about that change looks like it touches a printed card.
    """
    n = mk.symbol("01").symbol_size(border=0)[0]
    smallest = min(mk.SIZES_MM)
    per_module = smallest / n
    assert per_module >= FLOOR_MM, (
        f"{smallest} mm is {per_module:.3f} mm per module at {n}x{n} — "
        f"below the {FLOOR_MM} mm floor. The URL got longer, or SIZES_MM "
        f"got smaller.")


@pytest.mark.parametrize("mm", mk.SIZES_MM)
def test_the_svg_is_the_size_it_says_including_the_quiet_zone(mm):
    """SIZES_MM name the black square. The four-module quiet zone is outside
    it, so the file is wider than its name — which is the mistake this test
    exists because of."""
    svg = (CARD / f"chapter-01-{mm}mm.svg").read_text()
    width = float(re.search(r'width="([\d.]+)mm"', svg).group(1))
    n = mk.symbol("01").symbol_size(border=0)[0]
    assert width == pytest.approx(mm * (n + 8) / n, abs=0.01), (
        f"the {mm} mm file is {width:.2f} mm wide")


def test_the_decoder_reads_payloads_it_was_not_written_around():
    """Several lengths, so the decoder is not passing on one memorised case.
    Each crosses a version boundary, which changes the block interleaving."""
    import segno
    for payload in ("https://milo-service.onrender.com/c/01",
                    "https://milo-service.onrender.com/c/14",
                    "x",
                    "https://milo-service.onrender.com/c/01?a=" + "b" * 20):
        qr = segno.make(payload, error="q", boost_error=False, micro=False)
        png = ROOT / "card" / "_tmp-decoder-check.png"
        qr.save(png, scale=8, border=4)
        try:
            assert qr_read.decode(png)["payload"] == payload
        finally:
            png.unlink(missing_ok=True)


def test_the_card_is_never_a_micro_qr():
    """segno returns a Micro QR for a short enough payload and phone cameras
    are markedly worse at those. Today's URL is far too long to trigger it; a
    shorter one — a custom domain, a redirector — would, and the first anyone
    would know is a card half the phones in a room cannot read.

    The decoder found this, by refusing a 17-module symbol as not a QR size.
    """
    import segno
    assert mk.symbol("01").symbol_size(border=0)[0] >= 21
    assert segno.make("x", error="q", micro=False).symbol_size(border=0)[0] >= 21
    # and the guard is the one being tested, not the URL's length
    assert "micro=False" in (ROOT / "tools" / "make_card_qr.py").read_text()


def test_the_proof_sheet_puts_one_symbol_on_each_page():
    """Side by side, a phone aimed at the smallest reads the largest, and
    because every symbol carries the same URL the page opens and the scan
    looks like a pass."""
    html = (CARD / "chapter-01-proof-sheet.html").read_text()
    assert html.count('class="page"') == len(mk.SIZES_MM)
    assert "page-break-after: always" in html
    for mm in mk.SIZES_MM:
        assert f"<b>{mm} mm</b>" in html
