"""The QR code for one chapter's card — M-10 step 02.

Two things this script is careful about, because both are printed and neither
can be corrected once the card is in a child's hand.

**The URL is built from one constant and the chapter key**, so a card can only
ever point at a chapter the service has. A typo in a path is a 404 an adult
sees at the proof stage; a typo in a printed card is a child holding a dead
card at the table.

**Error correction is Q, not the default M.** M recovers 15% of a damaged
symbol and Q recovers 25%. Q costs modules — this 38-character URL is version
4 at Q, 33x33, where it is version 3 at M, 29x29 — which at a fixed physical
size means smaller modules. That trade is worth taking here: the card is card stock in the hands
of a nine-year-old who is also holding a screwdriver, and the failure mode Q
protects against is a thumbprint over a corner.

Output is SVG for print, because a printer should rasterise the symbol at its
own resolution rather than scale someone's PNG, and PNG at a high fixed
resolution for the decode check.
"""
import argparse
import pathlib
import sys

import segno

# The one place the host is written down. tools/ and the README are the only
# two, and they are checked against each other by tests/test_card_qr.py.
SERVICE = "https://milo-service.onrender.com"

# Millimetres. The proof sheet prints all three so an adult can find the
# smallest that scans first time, rather than us guessing on their behalf.
SIZES_MM = (20, 25, 30)

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "card"


def url_for(chapter: str) -> str:
    return f"{SERVICE}/c/{chapter}"


def symbol(chapter: str):
    """The symbol itself.

    `boost_error=False` so the version and the error level are what this file
    says they are and not what the library decided was free — a printed
    artefact should not change because a URL got a character shorter.

    `micro=False` because segno will return a Micro QR for a short enough
    payload, and phone cameras are markedly worse at those than at the full
    symbology. Today's URL is far too long to trigger it. The point is that a
    shorter one — a custom domain, a redirector — would, and the first anyone
    would know is a card that half the phones in a room cannot read.
    """
    return segno.make(url_for(chapter), error="q",
                      boost_error=False, micro=False)


def write(chapter: str) -> dict:
    """Write the print files and the decode check.

    SIZES_MM name the **symbol** — the black square — and not the file. The
    four-module quiet zone lives outside it, so a 25 mm symbol needs 31.1 mm of
    clear card. Getting this the wrong way round is why the first cut of this
    script reported module sizes 24% larger than the files it had just written:
    segno's `unit` sizes the whole rendering, quiet zone included.
    """
    import corpus
    if chapter not in corpus.BY_KEY:
        # The guard is here and not only in the CLI: a card can only ever point
        # at a chapter the service has, whoever calls this.
        raise KeyError(f"no chapter {chapter} in the corpus")
    OUT.mkdir(exist_ok=True)
    qr = symbol(chapter)
    n = qr.symbol_size(border=0)[0]
    stem = f"chapter-{chapter}"

    for mm in SIZES_MM:
        # scale is millimetres per module, so the symbol comes out at `mm`.
        qr.save(OUT / f"{stem}-{mm}mm.svg", scale=mm / n, border=4, unit="mm")

    # The decode check reads this. 20 px per module is far above anything a
    # camera needs and removes resolution as an explanation if it fails.
    png = OUT / f"{stem}-decode-check.png"
    qr.save(png, scale=20, border=4)

    return {"chapter": chapter, "url": url_for(chapter), "version": qr.version,
            "error": qr.error, "modules": n, "png": png,
            "svg": {mm: (OUT / f"{stem}-{mm}mm.svg") for mm in SIZES_MM}}


SHEET = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><title>Milo · chapter __KEY__ · QR proof sheet</title>
<style>
@page {{ size: A4; margin: 18mm }}
body {{ font: 400 10pt/1.5 ui-monospace, "SFMono-Regular", Menlo, monospace;
        color: #111; margin: 0 }}
h1 {{ font-size: 13pt; margin: 0 0 2mm; letter-spacing: .04em }}
.url {{ font-size: 11pt; word-break: break-all; margin: 0 0 3mm }}
.note {{ font-size: 8.5pt; color: #444; max-width: 150mm; margin: 0 0 8mm }}
.page {{ page-break-after: always; page-break-inside: avoid }}
.page:last-of-type {{ page-break-after: auto }}
.cell {{ text-align: center; margin: 18mm 0 0 }}
.cell .q {{ display: block; margin-bottom: 4mm }}
.cell b {{ display: block; font-size: 10pt }}
.cell span {{ display: block; font-size: 8pt; color: #444 }}
.tick {{ margin-top: 3mm; font-size: 8pt; color: #444 }}
.tick i {{ display: inline-block; width: 5mm; height: 5mm; border: 1px solid #111;
           vertical-align: -1mm; margin-right: 2mm }}
footer {{ font-size: 8.5pt; color: #444; border-top: 1px solid #bbb; padding-top: 4mm }}
</style></head><body>
<h1>Milo · chapter __KEY__ · __NAME__ · QR proof sheet</h1>
<p class="url">__URL__</p>
<p class="note">Print this at 100% — no "fit to page", which rescales the symbols and
makes the sizes below untrue. Then scan each one with the phone that will be in the
room, at the distance a child would hold it, under the light the table will have.
Tick the smallest that opens the page first time and without hunting; that is the size
for the card. Every symbol here is the same version __VERSION____ERROR__ at __MODULES__x__MODULES__
modules and carries the same URL, so a size that fails failed on size alone.</p>
<p class="note"><b>One symbol per sheet, and that is the point.</b> Side by side, a
phone aimed at the smallest will happily read the largest instead — and because all
three carry the same URL, the page would open and the scan would look like a pass.
Keep the other sheets out of frame.</p>
__ROWS__
<footer>Generated by <code>tools/make_card_qr.py</code>. The payload of each symbol was
read back by <code>tools/qr_read.py</code>, an independent decoder, before this sheet
was written. What it cannot tell you is whether a phone camera agrees, which is what
the ticks are for.</footer>
</body></html>
"""


def proof_sheet(chapter: str, info: dict, name: str) -> pathlib.Path:
    """A sheet an adult prints and scans. Not a card and not a design — the
    card is the book's. This exists to answer one question the repository
    cannot: which physical size a real phone reads first time."""
    n = info["modules"]
    cells = []
    for mm in SIZES_MM:
        svg = info["svg"][mm].read_text()
        svg = svg[svg.index("<svg"):]
        cells.append(
            f'<div class="page"><div class="cell"><span class="q">{svg}</span>'
            f'<b>{mm} mm</b>'
            f'<span>{mm / n:.2f} mm per module</span>'
            f'<span>{mm * (n + 8) / n:.1f} mm of clear card</span>'
            f'<div class="tick"><i></i>scanned first time</div></div></div>')
    html = SHEET.replace("{{", "{").replace("}}", "}")
    for token, value in (("__KEY__", chapter), ("__NAME__", name),
                         ("__URL__", info["url"]),
                         ("__VERSION__", str(info["version"])),
                         ("__ERROR__", info["error"]),
                         ("__MODULES__", str(n)),
                         ("__ROWS__", "".join(cells))):
        html = html.replace(token, value)
    out = OUT / f"chapter-{chapter}-proof-sheet.html"
    out.write_text(html)
    return out


def report(chapter: str, info: dict, name: str) -> str:
    n = info["modules"]
    lines = [
        f"  chapter   {chapter}  ·  {name}",
        f"  url       {info['url']}  ({len(info['url'])} chars)",
        f"  symbol    version {info['version']}-{info['error']}  {n}x{n} modules",
    ]
    for mm in SIZES_MM:
        lines.append(
            f"  {mm}mm      {mm / n:.2f} mm per module   "
            f"needs {mm * (n + 8) / n:.1f} mm of clear card   "
            f"→ card/chapter-{chapter}-{mm}mm.svg")
    lines.append(f"  decode    card/{info['png'].name}")
    return "\n".join(lines)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("chapter", nargs="?", default="01")
    a = ap.parse_args()
    sys.path.insert(0, str(ROOT))
    import corpus
    if a.chapter not in corpus.BY_KEY:
        sys.exit(f"no chapter {a.chapter} in the corpus")
    info = write(a.chapter)
    name = corpus.BY_KEY[a.chapter]["name"]
    print(report(a.chapter, info, name))
    print(f"  sheet     card/{proof_sheet(a.chapter, info, name).name}")
