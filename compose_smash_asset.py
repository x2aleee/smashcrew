#!/usr/bin/env python3
"""Compose the standalone 'SMASH' typographic artwork.

Pipeline (deterministic, fully offline):
  1. Bebas Neue glyph mask for the word SMASH (ultra-heavy condensed look)
  2. Patty texture (frame from the real sizzle video) cover-fit inside the glyphs
  3. ONE stroke pass (#FF5500) around the letterforms - no double lines
  4. Ember glow = blurred copy of the stroke layer, composited under the art
  5. Pure black (#000000) background for seamless web overlay
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 3840, 1180           # ~32:10 canvas: word fills it edge to edge
MARGIN = 40                 # breathing room for stroke + glow so nothing clips
FONT = "assets/fonts/BebasNeue-Regular.ttf"
TEXTURE = "assets/patty-frame.png"
OUT = "assets/smash-typographic-art.png"

# ---------------------------------------------------------------- glyph mask
# size the font so the word ink spans W - 2*MARGIN
probe = ImageFont.truetype(FONT, 100)
tmp = Image.new("L", (10, 10))
d = ImageDraw.Draw(tmp)
bb = d.textbbox((0, 0), "SMASH", font=probe)
w100 = bb[2] - bb[0]
fs = int((W - 2 * MARGIN) * 100 / w100)
font = ImageFont.truetype(FONT, fs)
bb = d.textbbox((0, 0), "SMASH", font=font)
ink_w = bb[2] - bb[0]
ink_h = bb[3] - bb[1]

mask = Image.new("L", (W, H), 0)
md = ImageDraw.Draw(mask)
ox = (W - ink_w) // 2 - bb[0]      # center the ink horizontally
oy = (H - ink_h) // 2 - bb[1]      # center the ink vertically
md.text((ox, oy), "SMASH", font=font, fill=255)

# ------------------------------------------------------- texture-filled fill
tex = Image.open(TEXTURE).convert("RGB")
# scale to cover the glyph band, center-crop to canvas size
s = max(W / tex.width, H / tex.height)
tex = tex.resize((int(tex.width * s) + 1, int(tex.height * s) + 1), Image.LANCZOS)
tex = tex.crop(((tex.width - W) // 2, (tex.height - H) // 2,
                (tex.width - W) // 2 + W, (tex.height - H) // 2 + H))
# slight darkening so the neon stroke pops over the texture
tex = Image.eval(tex, lambda v: int(v * 0.9))

fill = Image.new("RGB", (W, H), (0, 0, 0))
fill.paste(tex, (0, 0), mask)                       # texture only inside glyphs

# RGBA fill with per-glyph alpha (used by the transparent variant)
fill_rgba = tex.convert("RGBA")
fill_rgba.putalpha(mask)

# ------------------------------------------------------------- single stroke
stroke_l = Image.new("L", (W, H), 0)
sd = ImageDraw.Draw(stroke_l)
STROKE = 14                                         # px at 4K ~= 2px at 1080p CSS
for dx in range(-STROKE, STROKE + 1):
    for dy in range(-STROKE, STROKE + 1):
        if dx * dx + dy * dy <= STROKE * STROKE:
            sd.text((ox + dx, oy + dy), "SMASH", font=font, fill=255)
stroke_mask = Image.composite(stroke_l, Image.new("L", (W, H), 0), stroke_l)
stroke_only = Image.new("RGB", (W, H), (255, 85, 0))   # #FF5500
stroke_only.paste((255, 85, 0), (0, 0), stroke_mask)
stroke_only = Image.composite(stroke_only, Image.new("RGB", (W, H), (0, 0, 0)), stroke_mask)

# stroke ring = stroke area minus glyph interior
ring_mask = Image.new("L", (W, H), 0)
ring_mask.paste(stroke_l, (0, 0))
ring_mask.paste(0, (0, 0), mask)                    # punch out the interior

ring = Image.new("RGB", (W, H), (255, 85, 0))
ring.putalpha(ring_mask)

# ---------------------------------------------------------------- ember glow
glow_src = Image.new("RGBA", (W, H), (0, 0, 0, 0))
glow_src.paste((255, 85, 0), (0, 0), ring_mask)
glow = glow_src.filter(ImageFilter.GaussianBlur(26))
glow = Image.eval(glow, lambda v: min(255, int(v * 1.15)))

# ------------------------------------------------------------------ assemble
# black-background master (handoff / standalone use)
base = Image.new("RGBA", (W, H), (0, 0, 0, 255))     # pure black background
base = Image.alpha_composite(base, glow)
base = Image.alpha_composite(base, fill.convert("RGBA"))
base = Image.alpha_composite(base, ring)

# transparent-background variant (site overlay: no rectangle over gradients)
trans = Image.new("RGBA", (W, H), (0, 0, 0, 0))
trans = Image.alpha_composite(trans, glow)
trans = Image.alpha_composite(trans, fill_rgba)
trans = Image.alpha_composite(trans, ring)

crop = (int((W - ink_w) / 2 - MARGIN), int((H - ink_h) / 2 - MARGIN),
        int((W + ink_w) / 2 + MARGIN), int((H + ink_h) / 2 + MARGIN))
base = base.crop(crop)
trans = trans.crop(crop)

base.save(OUT, optimize=True)
trans.save(OUT.replace('.png', '-transparent.png'), optimize=True)
print("saved:", OUT, base.size)
print("saved:", OUT.replace('.png', '-transparent.png'), trans.size)
