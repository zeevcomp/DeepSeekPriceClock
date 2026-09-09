# -*- coding: utf-8 -*-
"""יוצר את האייקון של DeepSeekPriceClock: שעון כחול-כהה עם טבעת ומחוגים."""
import math
from PIL import Image, ImageDraw

S = 2048          # קנבס-על (סופר-סמפלינג לאנטי-אליאסינג)
CX = CY = S // 2

# פלטה
BG_TOP = (33, 43, 64)
BG_BOT = (8, 11, 19)
RING = (77, 107, 254)        # כחול דיפסיק
RING_DK = (48, 66, 168)
FACE = (13, 20, 36)
FACE_EDGE = (44, 55, 88)
TICK_LONG = (232, 237, 255)
TICK_SHORT = (76, 88, 122)
HAND_H = (240, 244, 255)
HAND_M = (255, 255, 255)
SEC = (255, 176, 32)         # זהב/ענבר
CAP = (240, 244, 255)


def grad_rect(d, x0, y0, x1, y1, r, c_top, c_bot):
    d.rounded_rectangle([x0, y0, x1, y1], radius=r, fill=(0, 0, 0, 0))
    for y in range(y0, y1):
        t = (y - y0) / max(1, y1 - y0)
        c = tuple(int(a + (b - a) * t) for a, b in zip(c_top, c_bot))
        d.line([x0, y, x1, y], fill=c)
    # מסכת פינות מעוגלות
    mask = Image.new("L", (S, S), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle([x0, y0, x1, y1], radius=r, fill=255)
    return mask


def cap_line(d, p1, p2, w, fill):
    """קו עם קצוות עגולים (ציור קו + עיגולי קצה)."""
    d.line([p1, p2], fill=fill, width=w)
    r = w // 2
    for p in (p1, p2):
        d.ellipse([p[0] - r, p[1] - r, p[0] + r, p[1] + r], fill=fill)


def polar(deg, r):
    a = math.radians(deg)
    return (CX + r * math.sin(a), CY - r * math.cos(a))


img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
d = ImageDraw.Draw(img)

# רקע: ריבוע מעוגל עם גרדיאנט
M = 70
mask = grad_rect(d, M, M, S - M, S - M, 400, BG_TOP, BG_BOT)
bg = Image.new("RGBA", (S, S), (0, 0, 0, 0))
bd = ImageDraw.Draw(bg)
bd.rounded_rectangle([M, M, S - M, S - M], radius=400, fill=BG_TOP)
px = bg.load()
for y in range(M, S - M):
    t = (y - M) / (S - 2 * M)
    c = tuple(int(a + (b - a) * t) for a, b in zip(BG_TOP, BG_BOT))
    bd.line([M, y, S - M, y], fill=c)
img.paste(bg, (0, 0), mask)

# טבעת חיצונית כהה (עומק) + טבעת כחולה ראשית
d.ellipse([CX - 900, CY - 900, CX + 900, CY + 900], outline=RING_DK, width=56)
d.ellipse([CX - 830, CY - 830, CX + 830, CY + 830], outline=RING, width=110)

# פני השעון
d.ellipse([CX - 700, CY - 700, CX + 700, CY + 700], fill=FACE)
d.ellipse([CX - 700, CY - 700, CX + 700, CY + 700], outline=FACE_EDGE, width=10)

# 12 סימוני שעות
for i in range(12):
    long = (i % 3 == 0)
    r1, r2 = (620, 668) if long else (642, 668)
    w = 34 if long else 18
    c = TICK_LONG if long else TICK_SHORT
    cap_line(d, polar(i * 30, r1), polar(i * 30, r2), w, c)

# מחוג שניות (10:10:38 → 228 מעלות) עם זנב
cap_line(d, polar(228, 150), polar(228, 645), 18, SEC)

# מחוג דקות → 10 דקות = 60 מעלות
cap_line(d, (CX, CY), polar(60, 560), 54, HAND_M)
# מחוג שעות → 10 שעות ו-10 דקות = 305 מעלות
cap_line(d, (CX, CY), polar(305, 415), 68, HAND_H)

# ציר מרכזי
d.ellipse([CX - 96, CY - 96, CX + 96, CY + 96], fill=CAP)
d.ellipse([CX - 46, CY - 46, CX + 46, CY + 46], fill=SEC)

# קבצי פלט
ICO_SIZES = [16, 20, 24, 32, 40, 48, 64, 128, 256]
img.resize((256, 256), Image.LANCZOS).save("icon_256.png")
img.resize((512, 512), Image.LANCZOS).save("icon_preview.png")
img.save("DeepSeekClock.ico", format="ICO",
         sizes=[(s, s) for s in ICO_SIZES])
print("OK: DeepSeekClock.ico (9 sizes), icon_256.png, icon_preview.png")
