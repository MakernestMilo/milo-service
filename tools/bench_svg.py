"""Breadboard drawings for the Origins bench experiments.

One placement list per experiment, the same columns as the steps in bench.json.
A part is (kind, (col, half), (col, half), label). A jumper is (shield pin, colour, (col, half)).
Run: python tools/bench_svg.py  ->  levels/origins/bench/svg/<key>.svg
"""
import json, os

INK = "#191713"; PAPER = "#FBF9F3"; BOARD = "#EFEBE1"; HOLE = "#B9B3A6"; MID = "#6B675F"
COL = {"red": "#E0302A", "black": INK, "blue": "#1F4FD8", "light blue": "#8EC9F0", "yellow": "#F2D21B",
       "pink": "#FF5FA2", "green": "#1E8A3C", "orange": "#F39A1E", "brown": "#8B4A2B"}
P = 22                      # hole pitch in px
X0, Y0 = 100, 130           # first hole
GAP = 18                    # middle channel
W = X0 + 16 * P + 50


def hole(col, half, row=2):
    """Centre of a hole. half 't' rows 0..4 (a..e), 'b' rows 0..4 (f..j). row 2 is the middle one."""
    x = X0 + (col - 1) * P
    y = Y0 + row * P if half == "t" else Y0 + 5 * P + GAP + row * P
    return x, y


def board():
    s = [f'<rect x="{X0-30}" y="{Y0-34}" width="{16*P+60}" height="{10*P+GAP+46}" rx="10" fill="{BOARD}" stroke="{HOLE}" stroke-width="1.5"/>']
    for c in range(1, 18):
        x = X0 + (c - 1) * P
        for half in "tb":
            for r in range(5):
                hx, hy = hole(c, half, r)
                s.append(f'<rect x="{hx-3}" y="{hy-3}" width="6" height="6" rx="1" fill="{HOLE}"/>')
    yg = Y0 + 5 * P - P / 2 + GAP / 2 + 2
    s.append(f'<line x1="{X0-20}" y1="{yg}" x2="{X0+16*P+20}" y2="{yg}" stroke="{HOLE}" stroke-width="1" stroke-dasharray="3 3"/>')
    s.append(f'<text x="{X0-40}" y="{Y0+2*P+4}" text-anchor="end" font-family="Space Mono,monospace" font-size="10" fill="{MID}">TOP</text>')
    s.append(f'<text x="{X0-40}" y="{Y0+7*P+GAP+4}" text-anchor="end" font-family="Space Mono,monospace" font-size="10" fill="{MID}">BOTTOM</text>')
    return s


def numbers():
    s = []
    for c in range(1, 18):
        x = X0 + (c - 1) * P
        s.append(f'<rect x="{x-8}" y="{Y0-27}" width="16" height="14" rx="3" fill="{BOARD}"/>')
        s.append(f'<text x="{x}" y="{Y0-16}" text-anchor="middle" font-family="Space Mono,monospace" font-size="10" fill="{MID}">{c}</text>')
    return s


def lead(a, b):
    return f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="#8C8C8C" stroke-width="2.5" stroke-linecap="round"/>'


def part(kind, p1, p2, label, row=1):
    a = hole(p1[0], p1[1], row); b = hole(p2[0], p2[1], row if p1[1] == p2[1] else 0)
    if p1[1] != p2[1]:
        a = hole(p1[0], p1[1], 4); b = hole(p2[0], p2[1], 0)
    mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
    s = [lead(a, b)]
    if kind.startswith("led"):
        c = {"led_red": "#E0302A", "led_yellow": "#F2C21B", "led_green": "#2FA84F"}[kind]
        s.append(f'<circle cx="{mx}" cy="{my-12}" r="9" fill="{c}" stroke="{INK}" stroke-width="1.5"/>')
        s.append(lead(a, (mx - 3, my - 6))); s.append(lead(b, (mx + 3, my - 6)))
        s.append(f'<text x="{a[0]-8}" y="{a[1]-10}" text-anchor="middle" font-family="Space Mono,monospace" font-size="11" font-weight="700" fill="{INK}">+</text>')
    elif kind in ("r220", "r10k"):
        bands = ["#C62828", "#C62828", "#7B4A2A"] if kind == "r220" else ["#7B4A2A", INK, "#F39A1E"]
        s.append(f'<rect x="{mx-14}" y="{my-6}" width="28" height="12" rx="5" fill="#E9D7A8" stroke="{INK}" stroke-width="1.2"/>')
        for i, bc in enumerate(bands):
            s.append(f'<rect x="{mx-9+i*6}" y="{my-6}" width="3" height="12" fill="{bc}"/>')
    elif kind == "ldr":
        s.append(f'<circle cx="{mx}" cy="{my-10}" r="10" fill="#F1E3C2" stroke="{INK}" stroke-width="1.5"/>')
        s.append(f'<path d="M{mx-6} {my-12} q3 -4 6 0 t6 0" fill="none" stroke="#C0392B" stroke-width="1.5"/>')
        s.append(lead(a, (mx - 4, my - 2))); s.append(lead(b, (mx + 4, my - 2)))
    elif kind == "button":
        x1, x2 = sorted([hole(p1[0], "t", 4)[0], hole(p2[0], "t", 4)[0]])
        y1 = hole(p1[0], "t", 4)[1]; y2 = hole(p1[0], "b", 0)[1]
        s = [f'<rect x="{x1-8}" y="{y1-8}" width="{x2-x1+16}" height="{y2-y1+16}" rx="4" fill="#2B2B2B" stroke="{INK}"/>',
             f'<circle cx="{(x1+x2)/2}" cy="{(y1+y2)/2}" r="9" fill="#5A5A5A"/>']
        for x in (x1, x2):
            for y in (y1, y2):
                s.append(f'<circle cx="{x}" cy="{y}" r="3" fill="#C9C9C9"/>')
    if label:
        s.append(f'<text x="{mx}" y="{my+22}" text-anchor="middle" font-family="Space Mono,monospace" font-size="10" fill="{INK}">{label}</text>')
    return s


def jumper(pin, colour, to, i, n, row=None, dx=0):
    """A jumper's breadboard end, with a tag naming the shield pin its other end goes to.
    Top-half jumpers leave upwards, bottom-half ones downwards, so no wire crosses the board.
    Two jumpers in one column use different rows, and the second tag steps sideways by dx."""
    up = to[1] == "t"
    tx, ty = hole(to[0], to[1], row if row is not None else (0 if up else 4))
    c = COL.get(colour, INK)
    edge = Y0 - 40 if up else Y0 + 10 * P + GAP + 18
    tag_y = edge - 66 if up else edge + 6
    gx = tx + dx
    path = f"M{tx} {ty} L{tx} {edge + (8 if up else -8)} L{gx} {edge}"
    s = []
    if colour in ("yellow", "light blue", "pink"):
        s.append(f'<path d="{path}" fill="none" stroke="{INK}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>')
    s.append(f'<path d="{path}" fill="none" stroke="{c}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>')
    s.append(f'<circle cx="{tx}" cy="{ty}" r="4" fill="{c}" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<rect x="{gx-9}" y="{tag_y}" width="18" height="60" rx="4" fill="{PAPER}" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<text transform="translate({gx+4} {tag_y+30}) rotate(-90)" text-anchor="middle" font-family="Space Mono,monospace" '
             f'font-size="10" font-weight="700" fill="{INK}">{pin}</text>')
    return s


LAYOUT = {
    "01": {"parts": [("led_red", (5, "t"), (6, "t"), "LED"), ("r220", (6, "t"), (8, "t"), "220"), ("r220", (8, "t"), (10, "t"), "220")],
           "jumpers": [("9V +", "red", (5, "t")), ("9V −", "black", (10, "t"))]},
    "02": {"parts": [("ldr", (3, "t"), (6, "t"), "LDR"), ("r10k", (6, "t"), (10, "t"), "10k"),
                     ("led_red", (13, "t"), (14, "t"), "LED"), ("r220", (14, "t"), (17, "t"), "220")],
           "jumpers": [("A0 V", "red", (3, "t")), ("A0 S", "blue", (6, "t")), ("A0 G", "black", (10, "t")),
                       ("12 S", "yellow", (13, "t")), ("12 G", "black", (17, "t"))]},
    "05": {"parts": [("ldr", (3, "t"), (6, "t"), "A"), ("r10k", (6, "t"), (10, "t"), "10k"),
                     ("led_red", (13, "t"), (14, "t"), "LED"), ("r220", (14, "t"), (17, "t"), "220"),
                     ("ldr", (3, "b"), (6, "b"), "B"), ("r10k", (6, "b"), (10, "b"), "10k")],
           "jumpers": [("A0 V", "red", (3, "t")), ("A0 S", "blue", (6, "t")), ("A0 G", "black", (10, "t")),
                       ("12 S", "yellow", (13, "t")), ("12 G", "black", (17, "t")),
                       ("A1 V", "red", (3, "b")), ("A1 S", "light blue", (6, "b")), ("A1 G", "black", (10, "b"))]},
    "06": {"parts": [("button", (3, "t"), (5, "t"), ""), ("button", (10, "t"), (12, "t"), "")],
           "jumpers": [("12 S", "yellow", (3, "t")), ("12 G", "black", (5, "b")), ("10 S", "green", (10, "t")), ("10 G", "black", (12, "b"))]},
    "07": {"parts": [("ldr", (3, "t"), (6, "t"), "LDR"), ("r10k", (6, "t"), (10, "t"), "10k")],
           "jumpers": [("A0 V", "red", (3, "t")), ("A0 S", "blue", (6, "t")), ("A0 G", "black", (10, "t"))]},
    "08": {"parts": [("led_red", (2, "t"), (3, "t"), "RED"), ("r220", (3, "t"), (5, "t"), "220"),
                     ("led_yellow", (7, "t"), (8, "t"), "YEL"), ("r220", (8, "t"), (10, "t"), "220"),
                     ("led_green", (12, "t"), (13, "t"), "GRN"), ("r220", (13, "t"), (15, "t"), "220")],
           "jumpers": [("12 S", "yellow", (2, "t")), ("12 G", "black", (5, "t")), ("13 S", "pink", (7, "t")),
                       ("13 G", "black", (10, "t")), ("10 S", "green", (12, "t")), ("10 G", "black", (15, "t"))]},
    "d": {"parts": [("button", (3, "t"), (5, "t"), ""), ("ldr", (9, "b"), (12, "b"), "LDR"), ("r10k", (12, "b"), (16, "b"), "10k")],
          "jumpers": [("12 S", "yellow", (3, "t")), ("12 G", "black", (5, "b")),
                      ("A0 V", "red", (9, "b")), ("A0 S", "blue", (12, "b")), ("A0 G", "black", (16, "b"))]},
    "09": {"parts": [("led_red", (13, "t"), (14, "t"), "LED"), ("r220", (14, "t"), (17, "t"), "220")],
           "jumpers": [("12 S", "yellow", (13, "t")), ("12 G", "black", (17, "t"))]},
    "10": {"parts": [("ldr", (3, "t"), (6, "t"), "LDR"), ("r10k", (6, "t"), (10, "t"), "10k")],
           "jumpers": [("A0 V", "red", (3, "t")), ("A0 S", "blue", (6, "t")), ("A0 G", "black", (10, "t"))]},
}
LAYOUT["04"] = LAYOUT["02"]
# The faults, drawn as built: wrong on purpose.
LAYOUT["f1"] = {"parts": [("led_red", (6, "t"), (5, "t"), "LED"), ("r220", (6, "t"), (8, "t"), "220"), ("r220", (8, "t"), (10, "t"), "220")],
                "jumpers": [("9V +", "red", (5, "t")), ("9V −", "black", (10, "t"))]}
LAYOUT["f2"] = {"parts": LAYOUT["06"]["parts"],
                "jumpers": [("12 S", "yellow", (3, "t")), ("12 G", "black", (3, "t"), 1, -26), ("10 S", "green", (10, "t")), ("10 G", "black", (12, "b"))]}
LAYOUT["f3"] = {"parts": [p for p in LAYOUT["02"]["parts"] if p[0] != "r10k"], "jumpers": LAYOUT["02"]["jumpers"]}
LAYOUT["f4"] = {"parts": [p if p[3] != "220" or p[1] != (8, "t") else ("r220", (9, "t"), (10, "t"), "220") for p in LAYOUT["08"]["parts"]],
                "jumpers": LAYOUT["08"]["jumpers"]}
LAYOUT["f5"] = LAYOUT["02"]


def svg(key):
    L = LAYOUT[key]
    s = board()
    for p in L["parts"]:
        s += part(*p)
    n = len(L["jumpers"])
    for i, j in enumerate(L["jumpers"]):
        s += jumper(j[0], j[1], j[2], i, n, *j[3:])
    s += numbers()
    H = Y0 + 10 * P + GAP + 96
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" '
            f'aria-label="Breadboard layout for bench {key}">' + "".join(s) + "</svg>")


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "..", "levels", "origins", "bench", "svg")
    os.makedirs(out, exist_ok=True)
    for k in LAYOUT:
        open(os.path.join(out, f"{k}.svg"), "w").write(svg(k))
    print(len(LAYOUT), "drawings")
