# -*- coding: utf-8 -*-
"""מייצר את פני השעון האנלוגי (rendered מראש) - ללא טבעת צבעונית.
המסגרת הדקה וסימוני שעות השיא מצוירים בזמן ריצה ע"י התוכנה."""
import math
from PIL import Image, ImageDraw, ImageFilter

S = 720
CX = CY = S // 2
R_FACE = 272              # פנים (68px בקנבס 180)
R_TICK_MAJ = 246
R_TICK_MIN = 234
FACE_BASE = (15, 23, 44)
EDGE = (35, 48, 88)
TICK_MAJ = (236, 241, 255)
TICK_MIN = (52, 66, 104)

img = Image.new("RGBA", (S, S), (0, 0, 0, 0))

# 1) צל רך עדין
shadow = Image.new("RGBA", (S, S), (0, 0, 0, 0))
ImageDraw.Draw(shadow).ellipse([CX - 322, CY - 316, CX + 322, CY + 336],
                               fill=(0, 0, 0, 110))
shadow = shadow.filter(ImageFilter.GaussianBlur(24))
img.alpha_composite(shadow)

# 2) פנים: בסיס כהה + הארה מרכזית עדינה
face = Image.new("RGBA", (S, S), (0, 0, 0, 0))
fd = ImageDraw.Draw(face)
fd.ellipse([CX - R_FACE, CY - R_FACE, CX + R_FACE, CY + R_FACE], fill=FACE_BASE)

small = 90
glow = Image.new("L", (small, small), 0)
gd = ImageDraw.Draw(glow)
for y in range(small):
    for x in range(small):
        d = math.hypot(x - small / 2, y - small / 2) / (small / 2)
        v = max(0.0, 1.0 - d)
        gd.point((x, y), fill=int(255 * v ** 2.2))
glow = glow.resize((S, S), Image.BILINEAR)
tint = Image.new("RGBA", (S, S), (150, 178, 255))
tint.putalpha(glow.point(lambda a: int(a * 0.10)))
mask = Image.new("L", (S, S), 0)
ImageDraw.Draw(mask).ellipse([CX - R_FACE, CY - R_FACE, CX + R_FACE, CY + R_FACE],
                             fill=255)
face.paste(tint, (0, 0), mask)
fd2 = ImageDraw.Draw(face)
fd2.ellipse([CX - R_FACE + 3, CY - R_FACE + 3, CX + R_FACE - 3, CY + R_FACE - 3],
            outline=EDGE, width=4)
img.alpha_composite(face)

# 3) סימונים: 60 קטנים + 12 גדולים (קצוות מעוגלים)
marks = Image.new("RGBA", (S, S), (0, 0, 0, 0))
md = ImageDraw.Draw(marks)
for i in range(60):
    a = math.radians(i * 6 - 90)
    ca, sa = math.cos(a), math.sin(a)
    if i % 5 == 0:
        r0, r1, w, col = R_TICK_MAJ - 16, R_TICK_MAJ, 12, TICK_MAJ
    else:
        r0, r1, w, col = R_TICK_MIN - 8, R_TICK_MIN, 6, TICK_MIN
    md.line([CX + r0 * ca, CY + r0 * sa, CX + r1 * ca, CY + r1 * sa],
            fill=col, width=w)
    for rr in (r0, r1):
        md.ellipse([CX + rr * ca - w / 2, CY + rr * sa - w / 2,
                    CX + rr * ca + w / 2, CY + rr * sa + w / 2], fill=col)
img.alpha_composite(marks)

# 4) פלט
face_180 = img.resize((180, 180), Image.LANCZOS)
face_180.save("face_180.png")

prev = Image.new("RGB", (300, 300), (15, 17, 26))
f240 = img.resize((240, 240), Image.LANCZOS)
prev.paste(f240, (30, 30), f240)
prev.save("face_preview.png")
print("OK: face_180.png + face_preview.png")
