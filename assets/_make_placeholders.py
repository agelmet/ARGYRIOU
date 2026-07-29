"""Generates temporary placeholder assets for the Argyriou build.

Angelo replaces logo-el.png, logo-en.png and georgina-argyriou.jpg with the real
files; this script exists only so the build renders before they arrive.
Delete once the real assets are in place.
"""
from PIL import Image, ImageDraw, ImageFont

SERIF = "/System/Library/Fonts/Supplemental/Georgia.ttf"
SERIF_I = "/System/Library/Fonts/Supplemental/Georgia Italic.ttf"
PURPLE, ACCENT, MAUVE, LILAC = "#5E2A84", "#8E5BB5", "#6D5560", "#F3EEF6"
S = 3  # supersample factor


def gr_upper(t):
    """Greek uppercase drops the tonos: Ψυχολόγος -> ΨΥΧΟΛΟΓΟΣ."""
    import unicodedata as u
    return "".join(c for c in u.normalize("NFD", t.upper())
                   if u.category(c) != "Mn")


def leaf(d, cx, cy, h, fill, rot=0):
    """Thin botanical leaf echoing the logo mark."""
    import math
    pts_r, pts_l = [], []
    for i in range(33):
        t = i / 32
        y = -h / 2 + t * h
        w = (h * 0.30) * math.sin(math.pi * t) ** 1.35
        pts_r.append((w, y))
        pts_l.append((-w, y))
    a = math.radians(rot)
    ca, sa = math.cos(a), math.sin(a)
    pts = [(cx + x * ca - y * sa, cy + x * sa + y * ca)
           for x, y in pts_r + pts_l[::-1]]
    d.polygon(pts, fill=fill)
    d.line([(cx + (-h / 2) * -sa, cy + (-h / 2) * ca),
            (cx + (h / 2) * -sa, cy + (h / 2) * ca)],
           fill="white", width=max(1, int(h // 90)))


def wordmark(path, name, role):
    """White-background placeholder wordmark (real logos also have white bg)."""
    W, H = 720 * S, 240 * S
    im = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(im)
    leaf(d, W * 0.5, H * 0.29, H * 0.34, PURPLE, rot=-24)
    leaf(d, W * 0.5 + H * 0.10, H * 0.32, H * 0.26, ACCENT, rot=22)

    f_name = ImageFont.truetype(SERIF, int(H * 0.20))
    f_role = ImageFont.truetype(SERIF, int(H * 0.078))
    d.text((W / 2, H * 0.60), name, font=f_name, fill=PURPLE, anchor="mm")
    # letter-spaced by hand: Pillow's shaper collapses padded spaces
    chars = list(gr_upper(role))
    track = int(H * 0.035)
    widths = [d.textlength(c, font=f_role) for c in chars]
    x = W / 2 - (sum(widths) + track * (len(chars) - 1)) / 2
    for c, w in zip(chars, widths):
        d.text((x, H * 0.82), c, font=f_role, fill=MAUVE, anchor='lm')
        x += w + track

    im.resize((720, 240), Image.LANCZOS).save(path, optimize=True)
    print(path)


def portrait(path):
    W, H = 900 * S, 1125 * S
    im = Image.new("RGB", (W, H), LILAC)
    d = ImageDraw.Draw(im)
    # soft silhouette
    d.ellipse([W * .5 - H * .115, H * .30, W * .5 + H * .115, H * .53], fill="#E2D5EA")
    d.ellipse([W * .5 - H * .215, H * .565, W * .5 + H * .215, H * 1.06], fill="#E2D5EA")
    leaf(d, W * .5, H * .175, H * .12, "#D9C8E4", rot=-20)

    f1 = ImageFont.truetype(SERIF_I, int(H * .042))
    f2 = ImageFont.truetype(SERIF, int(H * .026))
    d.text((W / 2, H * .72), "Τζωρτζίνα Αργυρίου", font=f1, fill=PURPLE, anchor="mm")
    d.text((W / 2, H * .78), "προσωρινή εικόνα — αναμονή φωτογραφίας",
           font=f2, fill=MAUVE, anchor="mm")

    im.resize((900, 1125), Image.LANCZOS).save(path, "JPEG", quality=80,
                                               optimize=True, progressive=True)
    print(path)


def touch_icon(path):
    """Purple monogram, matches the inline SVG favicon in index.html."""
    N = 180 * S
    im = Image.new("RGB", (N, N), PURPLE)
    d = ImageDraw.Draw(im)
    leaf(d, N * .5, N * .34, N * .30, "#A87DC9", rot=-22)
    f = ImageFont.truetype(SERIF, int(N * .30))
    d.text((N / 2, N * .70), "ΤΑ", font=f, fill="white", anchor="mm")
    im.resize((180, 180), Image.LANCZOS).save(path, optimize=True)
    print(path)


wordmark("logo-el.png", "Τζωρτζίνα Αργυρίου", "Ψυχολόγος")
wordmark("logo-en.png", "Georgina Argyriou", "Psychologist")
portrait("georgina-argyriou.jpg")
touch_icon("apple-touch-icon.png")
