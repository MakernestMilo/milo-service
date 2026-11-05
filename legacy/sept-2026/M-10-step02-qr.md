# M-10 · step 02 · the QR code

Chapter 01. `https://milo-service.onrender.com/c/01`, 38 characters.

The scan itself is the architect's — printed at 100%, on the phone that will be
in the room, at the distance a child holds it, under the light the table will
have. What is here is the artefact and the checks that can be made without a
camera.

---

## The symbol

| | |
|---|---|
| version | 4-Q · 33 × 33 modules |
| error correction | **Q**, 25% — not the default M |
| quiet zone | 4 modules, as the specification requires |

**Q rather than M.** M recovers 15% of a damaged symbol, Q recovers 25%. Q
costs modules — this URL is version 4 at Q, 33 × 33, where it is version 3 at
M, 29 × 29 — so at a fixed physical size the modules are smaller. The trade is
worth taking: this is card stock in the hands of a nine-year-old who is also
holding a screwdriver, and the failure Q protects against is a thumbprint over
a corner.

**Three sizes, in `card/`.** The number names the black square; the quiet zone
lies outside it.

| symbol | per module | clear card needed |
|---|---|---|
| 20 mm | 0.61 mm | 24.8 mm |
| 25 mm | 0.76 mm | 31.1 mm |
| 30 mm | 0.91 mm | 37.3 mm |

SVG rather than PNG, so a printer rasterises at its own resolution instead of
scaling ours.

---

## Checked without a camera

**The URL is built from one constant and the chapter key**, and `write()`
refuses a chapter the corpus does not have — the guard is in the function, not
only in the command line, so a card can only ever point at a chapter the
service has. A test asserts the host in `tools/make_card_qr.py` is the only
host the README names, because it is now written down in two places.

**The committed symbol decodes to the committed URL**, read back by
`tools/qr_read.py` — a decoder written for this step that shares nothing with
the encoder. It finds the module grid from the finder pattern, recovers the
mask from the format bits, unmasks, walks the codewords in the specification's
order, de-interleaves the blocks and parses the byte-mode segment. It does no
error correction, deliberately: a clean rendering of a correct symbol decodes
without it, and a wrong codeword here means the generator is wrong, which is
what we want to hear rather than have quietly repaired.

**The claim it does not support**, stated plainly: it is exercised against
symbols segno generated, so a fault both implementations shared would pass. The
evidence that a real detector agrees is a phone. I tried to add Apple's Vision
framework as a genuinely independent second detector — the same family the
iPhone camera uses — and abandoned it: the Swift compile against Command Line
Tools ran twenty-five minutes without producing a binary. It is not committed,
because a tool I could not build is a claim I cannot make.

**The smallest print size stays above 0.50 mm per module.** This test is not
about this file. A longer URL — a custom domain, a path with a slug — pushes
the symbol to a denser version, which at a fixed 20 mm makes every module
smaller. Nothing about that change looks like it touches a printed card.

`431 + 11` tests, all passing.

---

## Two findings

**1 · The proof sheet was a broken instrument on its first cut.** Three sizes
side by side, and a phone aimed at the 20 mm will happily read the 30 mm from
the same frame. Because all three carry the same URL, the page would open and
the scan would look like a pass — the instrument would have reported that the
smallest size worked when it had never been read. **One symbol per page now,**
and the sheet says why, because the person holding it is the one who has to
keep the other pages out of frame.

**2 · `segno.make(url, error="q")` can return a Micro QR, and the decoder
found it.** Micro QR is a different symbology and phone cameras are markedly
worse at it. This URL is far too long to trigger it — but a shorter one would,
and the first anyone would know is a card that half the phones in a room cannot
read. `micro=False` is now pinned in the generator with a test on the guard
rather than on the URL's length.

It was found by accident and by the right accident. The decoder was handed a
one-character payload as a spread-of-lengths check and **refused it** —
*17 modules is not a QR size* — which is a decoder declining to decode
something it was not built for, and is exactly what an instrument should do
when handed the wrong object. Had it been more accommodating it would have
decoded the Micro QR, the test would have passed, and the guard would not
exist.

One instrument correction of my own, recorded because the figure would have
been printed: the first cut of the generator wrote SVGs whose stated width
included the quiet zone while reporting module sizes as though it did not. The
files were 24% smaller than the numbers beside them. Both are right now and a
test holds them together.

---

## What the architect does with this

`card/chapter-01-proof-sheet.html` — print at 100%, no *fit to page*, which
rescales the symbols and makes every number on the sheet untrue. Three pages,
one symbol each. Scan each with the phone that will be in the room. Tick the
smallest that opens the page first time and without hunting; that is the size
for the card.

If none of the three reads first time, the finding is the size floor and not
the code, and 30 mm is not the ceiling — the generator takes any size.
