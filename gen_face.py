# -*- coding: utf-8 -*-
"""מייצר את פני השעון האנלוגי (rendered מראש באיכות גבוהה) להטבעה בתוכנה."""
import math
from PIL import Image, ImageDraw, ImageFilter

S = 720
CX = CY = S // 2
R_RING_OUT = 332          # טבעת חיצונית
R_RING_IN = 274
R_FACE = 272              # פנים
R_TICK_MAJ = 246
R_TICK_MIN = 234

RING = (77, 107, 254)
RING_DK = (43, 60, 168)
RING_LT = (150, 178, 255)
FACE_BASE = (15, 23, 44)
EDGE = (35, 48, 88)
TICK_MAJ = (236, 241, 255)
TICK_MIN = (52, 66, 104)


def annulus(d, r_out, r_in, fill):
    d.ellipse([CX - r_out, CY - r_out, CX + r_out, CY + r_out], fill=fill)
    d.ellipse([CX - r_in, CY - r_in, CX + r_in, CY + r_in], fill=(0, 0, 0, 0))


img = Image.new("RGBA", (S, S), (0, 0, 0, 0))

# 1) צל רך סביב השעון
shadow = Image.new("RGBA", (S, S), (0, 0, 0, 0))
ImageDraw.Draw(shadow).ellipse([CX - R_RING_OUT - 6, CY - R_RING_OUT + 12,
                                CX + R_RING_OUT + 6, CY + R_RING_OUT + 24],
                               fill=(0, 0, 0, 150))
shadow = shadow.filter(ImageFilter.GaussianBlur(26))
img.alpha_composite(shadow)

# 2) טבעת ראשית + ברק עליון ותחתון
ring = Image.new("RGBA", (S, S), (0, 0, 0, 0))
rd = ImageDraw.Draw(ring)
annulus(rd, R_RING_OUT, R_RING_IN, RING)
# ברק: קשת בהירה למעלה-שמאל וקשת כהה למטה
rd.arc([CX - 308, CY - 308, CX + 308, CY + 308], start=-125, end=-55,
       fill=RING_LT, width=13)
rd.arc([CX - 308, CY - 308, CX + 308, CY + 308], start=55, end=125,
       fill=RING_DK, width=15)
img.alpha_composite(ring)

# 3) פני השעון: בסיס כהה + הארה מרכזית (רדיוס גרדיאנט)
face = Image.new("RGBA", (S, S), (0, 0, 0, 0))
fd = ImageDraw.Draw(face)
fd.ellipse([CX - R_FACE, CY - R_FACE, CX + R_FACE, CY + R_FACE], fill=FACE_BASE)

small = 90  # גרדיאנט קטן שמוגדל - זול ומהיר
glow = Image.new("L", (small, small), 0)
gd = ImageDraw.Draw(glow)
for y in range(small):
    for x in range(small):
        d = math.hypot(x - small / 2, y - small / 2) / (small / 2)
        v = max(0.0, 1.0 - d)
        gd.point((x, y), fill=int(255 * v ** 2.2))
glow = glow.resize((S, S), Image.BILINEAR)
light = Image.new("RGBA", (S, S), (0, 0, 0, 0))
light.putalpha(glow.point(lambda a: int(a * 0.16)))
light = Image.composite(light, Image.new("RGBA", (S, S), (0, 0, 0, 0)), light)
mask = Image.new("L", (S, S), 0)
ImageDraw.Draw(mask).ellipse([CX - R_FACE, CY - R_FACE, CX + R_FACE, CY + R_FACE], fill=255)
face.paste(Image.new("RGBA", (S, S), (150, 178, 255)), (0, 0), Image.composite(
    glow.point(lambda a: a), Image.new("L", (S, S), 0), glow))
fd2 = ImageDraw.Draw(face)
# שפה פנימית עדינה
fd2.ellipse([CX - R_FACE + 4, CY - R_FACE + 4, CX + R_FACE - 4, CY + R_FACE - 4],
            outline=EDGE, width=5)
img.alpha_composite(face)

# 4) סימונים: 60 קטנים + 12 גדולים (עם קצוות מעוגלים)
marks = Image.new("RGBA", (S, S), (0, 0, 0, 0))
md = ImageDraw.Draw(marks)
for i in range(60):
    a = math.radians(i * 6 - 90)
    ca, sa = math.cos(a), math.sin(a)
    if i % 5 == 0:
        r0, r1, w, col = R_TICK_MAJ - 14, R_TICK_MAJ, 13, TICK_MAJ
    else:
        r0, r1, w, col = R_TICK_MIN - 8, R_TICK_MIN, 6, TICK_MIN
    md.line([CX + r0 * ca, CY + r0 * sa, CX + r1 * ca, CY + r1 * sa],
            fill=col, width=w)
    for rr in (r0, r1):  # קצוות עגולים
        md.ellipse([CX + rr * ca - w / 2, CY + rr * sa - w / 2,
                    CX + rr * ca + w / 2, CY + rr * sa + w / 2], fill=col)
img.alpha_composite(marks)

# 5) פלט
face_180 = img.resize((180, 180), Image.LANCZOS)
face_180.save("face_180.png")

# תצוגה מקדימה על רקע כהה (לצ'אט)
prev = Image.new("RGB", (300, 300), (15, 17, 26))
prev.paste(img.resize((240, 240), Image.LANCZOS), (30, 30), img.resize((240, 240), Image.LANCZOS))
prev.save("face_preview.png")
print("OK: face_180.png + face_preview.png")
