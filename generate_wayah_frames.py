from PIL import Image, ImageDraw, ImageFont
import math, os, random

W, H = 1280, 720
BG = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 30, 30)
BLUE = (30, 80, 200)
LIGHTBLUE = (150, 200, 255)
GREEN = (50, 160, 50)
LIGHTGREEN = (150, 220, 150)
YELLOW = (255, 220, 30)
ORANGE = (230, 130, 30)
BROWN = (140, 90, 40)
GRAY = (160, 160, 160)
LIGHTGRAY = (210, 210, 210)
SKYBLUE = (180, 220, 255)
GOLD = (210, 170, 30)

OUT = "/home/user/NKN/wayah_frames"
os.makedirs(OUT, exist_ok=True)

def new_img():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    return img, d

def font(size):
    try:
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size)
    except:
        return ImageFont.load_default()

def wobbly_line(d, x1, y1, x2, y2, color=BLACK, width=4, segments=8):
    """Draw a slightly wobbly line to simulate hand-drawn feel."""
    pts = []
    for i in range(segments + 1):
        t = i / segments
        x = x1 + (x2 - x1) * t + (random.randint(-4, 4) if 0 < i < segments else 0)
        y = y1 + (y2 - y1) * t + (random.randint(-4, 4) if 0 < i < segments else 0)
        pts.append((x, y))
    for i in range(len(pts) - 1):
        d.line([pts[i], pts[i+1]], fill=color, width=width)

def wobbly_rect(d, x1, y1, x2, y2, color=BLACK, width=4, fill=None):
    if fill:
        d.rectangle([x1, y1, x2, y2], fill=fill)
    wobbly_line(d, x1, y1, x2, y1, color, width)
    wobbly_line(d, x2, y1, x2, y2, color, width)
    wobbly_line(d, x2, y2, x1, y2, color, width)
    wobbly_line(d, x1, y2, x1, y1, color, width)

def stickman(d, cx, cy, scale=1.0, color=BLACK):
    """Draw a simple stick figure."""
    lw = max(3, int(4 * scale))
    head_r = int(22 * scale)
    # head
    d.ellipse([cx - head_r, cy - head_r, cx + head_r, cy + head_r], outline=color, width=lw)
    # eyes
    er = max(2, int(3 * scale))
    d.ellipse([cx - head_r//2 - er, cy - er, cx - head_r//2 + er, cy + er], fill=color)
    d.ellipse([cx + head_r//2 - er, cy - er, cx + head_r//2 + er, cy + er], fill=color)
    # smile
    d.arc([cx - 10*scale, cy + 4*scale, cx + 10*scale, cy + 14*scale], 0, 180, fill=color, width=lw)
    body_top = cy + head_r
    body_bot = body_top + int(55 * scale)
    # body
    wobbly_line(d, cx, body_top, cx, body_bot, color, lw)
    # arms
    arm_y = body_top + int(18 * scale)
    wobbly_line(d, cx - int(30*scale), arm_y + int(10*scale), cx, arm_y, color, lw)
    wobbly_line(d, cx, arm_y, cx + int(30*scale), arm_y + int(10*scale), color, lw)
    # legs
    wobbly_line(d, cx, body_bot, cx - int(22*scale), body_bot + int(40*scale), color, lw)
    wobbly_line(d, cx, body_bot, cx + int(22*scale), body_bot + int(40*scale), color, lw)

def stickman_arms_up(d, cx, cy, scale=1.0, color=BLACK):
    lw = max(3, int(4 * scale))
    head_r = int(22 * scale)
    d.ellipse([cx - head_r, cy - head_r, cx + head_r, cy + head_r], outline=color, width=lw)
    er = max(2, int(3 * scale))
    d.ellipse([cx - head_r//2 - er, cy - er, cx - head_r//2 + er, cy + er], fill=color)
    d.ellipse([cx + head_r//2 - er, cy - er, cx + head_r//2 + er, cy + er], fill=color)
    d.arc([cx - 10, cy + 4, cx + 10, cy + 14], 0, 180, fill=color, width=lw)
    body_top = cy + head_r
    body_bot = body_top + int(55 * scale)
    wobbly_line(d, cx, body_top, cx, body_bot, color, lw)
    arm_y = body_top + int(18 * scale)
    wobbly_line(d, cx - int(30*scale), arm_y - int(20*scale), cx, arm_y, color, lw)
    wobbly_line(d, cx, arm_y, cx + int(30*scale), arm_y - int(20*scale), color, lw)
    wobbly_line(d, cx, body_bot, cx - int(22*scale), body_bot + int(40*scale), color, lw)
    wobbly_line(d, cx, body_bot, cx + int(22*scale), body_bot + int(40*scale), color, lw)

def draw_text_centered(d, text, cx, cy, size=32, color=BLACK):
    f = font(size)
    bbox = d.textbbox((0, 0), text, font=f)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    d.text((cx - tw//2, cy - th//2), text, fill=color, font=f)

def draw_text(d, text, x, y, size=28, color=BLACK):
    d.text((x, y), text, fill=color, font=font(size))

def draw_stadium(d, cx, cy, w=400, h=200):
    """Simple childish stadium drawing."""
    # ground
    wobbly_line(d, cx - w//2, cy + h//2, cx + w//2, cy + h//2, GREEN, 5)
    # arch/oval shape for stadium
    d.arc([cx - w//2, cy - h//2, cx + w//2, cy + h//2], 180, 0, fill=GRAY, width=6)
    d.arc([cx - w//2 + 30, cy - h//2 + 30, cx + w//2 - 30, cy + h//2 - 30], 180, 0, fill=WHITE if False else BG, width=4)
    # walls
    wobbly_line(d, cx - w//2, cy, cx - w//2, cy + h//2, BLACK, 5)
    wobbly_line(d, cx + w//2, cy, cx + w//2, cy + h//2, BLACK, 5)

def draw_boat(d, cx, cy):
    """Simple boat shape."""
    # hull
    pts = [(cx-80, cy), (cx-100, cy+40), (cx+100, cy+40), (cx+80, cy)]
    d.polygon(pts, fill=BROWN, outline=BLACK)
    for i in range(len(pts)-1):
        wobbly_line(d, *pts[i], *pts[i+1], BLACK, 4)
    # mast
    wobbly_line(d, cx, cy, cx, cy-80, BLACK, 4)
    # sail
    d.polygon([(cx, cy-80), (cx, cy-10), (cx+60, cy-45)], fill=(220,220,255), outline=BLACK)
    # waves
    for dx in range(-140, 140, 30):
        d.arc([cx+dx, cy+35, cx+dx+30, cy+55], 0, 180, fill=BLUE, width=3)

# ─────────────────────────────────────────────────────────────────────────────
# IMAGE 1 — [00:00–00:30] Cold Open: Estadio Centenario, plaque
# ─────────────────────────────────────────────────────────────────────────────
def img1():
    img, d = new_img()
    # sky
    d.rectangle([0, 0, W, H//2], fill=SKYBLUE)
    # ground
    d.rectangle([0, H//2, W, H], fill=LIGHTGREEN)

    # Simple stadium: big rectangle with arch top
    sx, sy, sw, sh = 400, 180, 480, 280
    d.rectangle([sx, sy + 60, sx+sw, sy+sh], fill=GRAY)
    d.ellipse([sx, sy, sx+sw, sy+120], fill=GRAY, outline=BLACK)
    wobbly_rect(d, sx, sy+60, sx+sw, sy+sh, BLACK, 5)
    # arch top outline
    d.arc([sx, sy, sx+sw, sy+120], 180, 0, fill=BLACK, width=5)
    # field inside
    d.ellipse([sx+60, sy+100, sx+sw-60, sy+sh-40], fill=GREEN, outline=BLACK)

    # plaque on wall
    plaque_x, plaque_y = 220, 380
    wobbly_rect(d, plaque_x, plaque_y, plaque_x+160, plaque_y+70, GOLD, 4, fill=YELLOW)
    draw_text(d, "1930", plaque_x+30, plaque_y+10, 24, BLACK)
    draw_text(d, "PLAQUE", plaque_x+18, plaque_y+38, 20, BLACK)

    # stickman looking at plaque
    stickman(d, 180, 310, 0.9)

    # arrow pointing at plaque
    d.line([(205, 390), (215, 395)], fill=RED, width=3)

    # title
    draw_text_centered(d, "ESTADIO CENTENARIO", 640, 640, 40, BLACK)
    draw_text_centered(d, "Montevideo, Uruguay", 640, 688, 26, GRAY)

    img.save(f"{OUT}/frame_01_cold_open.png")
    print("Saved frame 1")

# ─────────────────────────────────────────────────────────────────────────────
# IMAGE 2 — [00:30–01:20] The Hook: 2030 vs 1930, same ground
# ─────────────────────────────────────────────────────────────────────────────
def img2():
    img, d = new_img()
    # dividing line down middle
    wobbly_line(d, W//2, 40, W//2, H-40, BLACK, 5)

    # LEFT SIDE — 1930 (sepia-ish: yellowish bg)
    d.rectangle([0, 0, W//2, H], fill=(255, 245, 220))

    # Old stadium sketch on left
    wobbly_rect(d, 60, 120, 380, 380, BLACK, 5, fill=LIGHTGRAY)
    d.ellipse([80, 90, 360, 200], fill=LIGHTGRAY, outline=BLACK)
    draw_text(d, "1930", 160, 400, 48, BLACK)
    draw_text(d, "FIRST EVER", 100, 460, 28, BLACK)
    draw_text(d, "WORLD CUP FINAL", 70, 498, 24, BLACK)
    # few stickmen
    stickman(d, 120, 230, 0.7)
    stickman(d, 220, 240, 0.7)
    stickman(d, 300, 225, 0.7)

    # RIGHT SIDE — 2030
    d.rectangle([W//2, 0, W, H], fill=(220, 240, 255))
    # banner
    wobbly_rect(d, W//2+60, 100, W-60, 220, RED, 5, fill=RED)
    draw_text_centered(d, "FIFA 2030", W//2 + 300, 155, 44, (255,255,255))
    draw_text_centered(d, "100 YEARS LATER", W//2 + 300, 280, 30, BLACK)
    draw_text_centered(d, "SAME STADIUM!", W//2 + 300, 330, 28, RED)
    # many stickmen celebrating
    for cx in [750, 830, 920, 1010, 1100, 1180]:
        stickman_arms_up(d, cx, 430, 0.8)

    # big arrow connecting them
    d.line([(380, 360), (W//2+60, 360)], fill=RED, width=6)
    d.polygon([(W//2+55, 348), (W//2+80, 360), (W//2+55, 372)], fill=RED)

    draw_text_centered(d, "SAME GROUND. 100 YEARS APART.", W//2, 660, 32, BLACK)

    img.save(f"{OUT}/frame_02_hook.png")
    print("Saved frame 2")

# ─────────────────────────────────────────────────────────────────────────────
# IMAGE 3 — [01:20–04:30] Chapter 1: The Setup — nobody showed up
# ─────────────────────────────────────────────────────────────────────────────
def img3():
    img, d = new_img()
    # sky
    d.rectangle([0, 0, W, 200], fill=SKYBLUE)
    # ocean
    d.rectangle([0, 200, W, H], fill=LIGHTBLUE)

    # 41 flags on left — just a cluster of colored rectangles
    draw_text(d, "41 FIFA MEMBERS", 30, 30, 30, BLACK)
    flag_colors = [RED, BLUE, GREEN, ORANGE, YELLOW, (150,0,150), (0,150,150), RED, BLUE]
    for i, fc in enumerate(flag_colors):
        fx = 40 + (i % 3) * 70
        fy = 70 + (i // 3) * 50
        wobbly_rect(d, fx, fy, fx+50, fy+35, BLACK, 3, fill=fc)
        # flag pole
        wobbly_line(d, fx, fy, fx, fy+55, BLACK, 3)

    # big X over most of them
    d.line([(30, 60), (240, 280)], fill=RED, width=8)
    d.line([(240, 60), (30, 280)], fill=RED, width=8)

    # Only 13 showed up box
    wobbly_rect(d, 320, 50, 660, 200, BLACK, 5, fill=YELLOW)
    draw_text(d, "ONLY 13 SHOWED UP", 330, 80, 28, BLACK)
    draw_text(d, "(out of 41 invited)", 360, 125, 22, BLACK)

    # Boat in ocean
    draw_boat(d, 900, 400)
    draw_text(d, "16-DAY BOAT TRIP!", 800, 300, 28, BLACK)

    # Arrow from Europe to Uruguay
    wobbly_line(d, 700, 350, 840, 370, RED, 4)
    d.polygon([(835, 360), (855, 372), (840, 385)], fill=RED)

    # stickman on boat looking sad
    stickman(d, 900, 290, 0.85)

    # speech bubble
    wobbly_rect(d, 920, 220, 1080, 280, BLACK, 3, fill=(255,255,200))
    draw_text(d, '"my JOB tho..."', 928, 238, 20, BLACK)

    # GREAT DEPRESSION label
    wobbly_rect(d, 30, 460, 280, 530, BLACK, 4, fill=GRAY)
    draw_text(d, "GREAT DEPRESSION", 38, 478, 20, BLACK)
    draw_text(d, "= no $$ to travel", 42, 504, 18, BLACK)

    # Uruguay flag simple
    wobbly_rect(d, 1050, 80, 1200, 160, BLACK, 4, fill=BLUE)
    draw_text(d, "URUGUAY", 1055, 175, 24, BLACK)
    draw_text(d, "HOSTING!", 1060, 204, 22, GREEN)

    draw_text_centered(d, '"The biggest tournament nearly had no guests"', W//2, 655, 28, BLACK)

    img.save(f"{OUT}/frame_03_setup.png")
    print("Saved frame 3")

# ─────────────────────────────────────────────────────────────────────────────
# IMAGE 4 — [04:30–06:30] Chapter 2: Who Are They At Home?
# ─────────────────────────────────────────────────────────────────────────────
def img4():
    img, d = new_img()
    # split background
    d.rectangle([0, 0, W//2, H], fill=(135, 206, 250))   # light blue - Uruguay
    d.rectangle([W//2, 0, W, H], fill=(200, 220, 255))    # slightly different - Argentina

    # River Plate dividing line (wavy blue river down middle)
    river_pts = []
    for y in range(0, H, 10):
        x = W//2 + int(15 * math.sin(y * 0.05))
        river_pts.append((x, y))
    for i in range(len(river_pts)-1):
        d.line([river_pts[i], river_pts[i+1]], fill=BLUE, width=18)
    draw_text_centered(d, "RIVER PLATE", W//2, 360, 18, (255,255,255))

    # URUGUAY SIDE
    draw_text(d, "URUGUAY", 50, 30, 42, BLACK)
    draw_text(d, "Pop: 1.75 million", 50, 90, 24, BLACK)
    draw_text(d, "(smaller than", 60, 122, 20, BLACK)
    draw_text(d, " most big cities!)", 60, 148, 20, BLACK)
    # Olympic gold medals
    draw_text(d, "OLYMPIC GOLD:", 50, 200, 24, GREEN)
    # medal 1924
    d.ellipse([55, 235, 105, 285], fill=GOLD, outline=BLACK)
    draw_text(d, "1924", 58, 295, 20, BLACK)
    # medal 1928
    d.ellipse([125, 235, 175, 285], fill=GOLD, outline=BLACK)
    draw_text(d, "1928", 128, 295, 20, BLACK)
    # stickmen playing football (Uruguay)
    stickman(d, 120, 430, 1.0)
    stickman(d, 220, 420, 1.0)
    stickman(d, 320, 435, 1.0)
    # ball
    d.ellipse([175, 470, 205, 500], fill=BLACK)

    # ARGENTINA SIDE
    draw_text(d, "ARGENTINA", W//2 + 50, 30, 38, BLACK)
    draw_text(d, "BIGGER. HUNGRIER.", W//2 + 50, 90, 28, RED)
    draw_text(d, "Top scorer:", W//2 + 50, 140, 24, BLACK)
    draw_text(d, "Guillermo Stabile", W//2 + 50, 170, 26, RED)
    # stickman Argentina (angry face)
    stickman(d, W//2 + 200, 380, 1.1)
    stickman(d, W//2 + 320, 370, 1.1)
    stickman(d, W//2 + 440, 385, 1.1)

    # "1928 Olympic Final" callout
    wobbly_rect(d, W//2 - 260, 540, W//2 + 260, 620, BLACK, 4, fill=YELLOW)
    draw_text_centered(d, "1928 OLYMPIC FINAL: URU 2-1 ARG", W//2, 575, 22, BLACK)
    draw_text_centered(d, "grudge match incoming...", W//2, 605, 19, RED)

    # angry face between them
    d.ellipse([W//2 - 25, 340, W//2 + 25, 390], fill=YELLOW, outline=BLACK)
    draw_text(d, ">:(", W//2 - 18, 350, 28, BLACK)

    draw_text_centered(d, "Same river. Same language. ZERO love lost.", W//2, 668, 30, BLACK)

    img.save(f"{OUT}/frame_04_who_are_they.png")
    print("Saved frame 4")

# ─────────────────────────────────────────────────────────────────────────────
# IMAGE 5 — [06:30–09:45] Chapter 3: The Match — ball drama & goals
# ─────────────────────────────────────────────────────────────────────────────
def img5():
    img, d = new_img()
    # Green pitch background
    d.rectangle([0, H//2, W, H], fill=GREEN)
    d.rectangle([0, 0, W, H//2], fill=(220, 240, 255))

    # pitch lines
    wobbly_rect(d, 80, H//2 + 20, W - 80, H - 30, (100, 200, 100), 3)
    # centre circle
    d.ellipse([W//2 - 60, H//2 - 20, W//2 + 60, H//2 + 100], outline=(100,200,100), width=3)

    # Scoreboard top
    wobbly_rect(d, 380, 20, 900, 130, BLACK, 5, fill=BLACK)
    draw_text(d, "URU", 420, 40, 36, (255,255,255))
    draw_text(d, "ARG", 720, 40, 36, (255,255,255))
    draw_text(d, "4", 545, 32, 56, YELLOW)
    draw_text(d, "-", 625, 32, 56, (255,255,255))
    draw_text(d, "2", 675, 32, 56, YELLOW)

    # THE BALL DRAMA - two balls with flags
    wobbly_rect(d, 30, 80, 340, 240, BLACK, 4, fill=(255,255,200))
    draw_text(d, "BALL DRAMA!", 45, 88, 26, RED)
    # Argentina ball (1st half)
    d.ellipse([50, 120, 100, 170], fill=BLACK)
    d.ellipse([60, 130, 90, 160], fill=(255,255,255))
    draw_text(d, "ARG ball", 108, 135, 20, BLACK)
    draw_text(d, "1st half", 108, 158, 18, GRAY)
    # Uruguay ball (2nd half)
    d.ellipse([50, 185, 100, 235], fill=(255,255,255), outline=BLACK)
    d.ellipse([68, 200, 82, 214], fill=BLACK)
    draw_text(d, "URU ball", 108, 197, 20, BLACK)
    draw_text(d, "2nd half", 108, 220, 18, GRAY)

    # Goals timeline
    goals = [
        (185, "URU 1-0", "Dorado 12'", GREEN),
        (295, "URU 1-1", "Peucelle", BLUE),
        (390, "ARG LEAD", "Stabile 2-1", RED),
        (510, "URU 2-2", "Cea", GREEN),
        (630, "URU 3-2", "Iriarte 68'", GREEN),
        (780, "URU 4-2", "Castro!!!", GREEN),
    ]
    # timeline bar
    wobbly_line(d, 120, 320, W-80, 320, BLACK, 4)
    for gx, label, detail, col in goals:
        d.line([(gx, 305), (gx, 335)], fill=col, width=3)
        draw_text(d, label, gx - 30, 340, 16, col)
        draw_text(d, detail, gx - 30, 362, 14, BLACK)

    # El Manco (one-armed stickman) scoring the 4th
    cx, cy = 1050, 450
    head_r = 24
    d.ellipse([cx - head_r, cy - head_r, cx + head_r, cy + head_r], outline=BLACK, width=4)
    d.ellipse([cx-8, cy-5, cx-2, cy+1], fill=BLACK)
    d.ellipse([cx+2, cy-5, cx+8, cy+1], fill=BLACK)
    d.arc([cx-10, cy+4, cx+10, cy+14], 0, 180, fill=BLACK, width=3)
    body_top = cy + head_r
    body_bot = body_top + 55
    wobbly_line(d, cx, body_top, cx, body_bot, BLACK, 4)
    # only ONE arm
    wobbly_line(d, cx, body_top+18, cx+35, body_top+5, BLACK, 4)
    # stub
    wobbly_line(d, cx, body_top+18, cx-12, body_top+28, BLACK, 4)
    wobbly_line(d, cx, body_bot, cx-22, body_bot+40, BLACK, 4)
    wobbly_line(d, cx, body_bot, cx+22, body_bot+40, BLACK, 4)
    # ball near foot
    d.ellipse([cx+25, body_bot+20, cx+50, body_bot+45], fill=BLACK)

    draw_text(d, "HECTOR CASTRO", 950, 610, 22, BLACK)
    draw_text(d, '"El Manco" (one arm!)', 938, 638, 20, RED)

    draw_text_centered(d, "July 30, 1930 — Estadio Centenario", W//2, 670, 26, GRAY)

    img.save(f"{OUT}/frame_05_the_match.png")
    print("Saved frame 5")

# ─────────────────────────────────────────────────────────────────────────────
# IMAGE 6 — [09:45–11:15] Chapter 4: Aftermath — holiday vs. mob
# ─────────────────────────────────────────────────────────────────────────────
def img6():
    img, d = new_img()
    # split: Uruguay left celebrating, Argentina right angry
    d.rectangle([0, 0, W//2, H], fill=(220, 255, 220))
    d.rectangle([W//2, 0, W, H], fill=(255, 210, 210))

    # URUGUAY LEFT — national holiday
    draw_text(d, "URUGUAY", 50, 25, 38, GREEN)
    draw_text(d, "NATIONAL HOLIDAY!", 50, 75, 28, GREEN)
    # calendar
    wobbly_rect(d, 50, 120, 200, 220, BLACK, 4, fill=(255,255,200))
    draw_text(d, "JULY 31", 65, 145, 22, BLACK)
    draw_text(d, "HOLIDAY", 60, 175, 22, GREEN)
    # stickmen celebrating
    stickman_arms_up(d, 100, 360, 1.0)
    stickman_arms_up(d, 190, 350, 1.0)
    stickman_arms_up(d, 280, 365, 1.0)
    stickman_arms_up(d, 370, 355, 0.9)
    # confetti dots
    for _ in range(60):
        cx2 = random.randint(20, W//2-20)
        cy2 = random.randint(100, 550)
        col = random.choice([RED, GREEN, BLUE, YELLOW, ORANGE])
        d.ellipse([cx2, cy2, cx2+8, cy2+8], fill=col)
    # trophy
    d.polygon([(155, 440), (135, 530), (175, 530)], fill=GOLD, outline=BLACK)
    wobbly_rect(d, 130, 430, 180, 450, BLACK, 3, fill=GOLD)
    d.ellipse([115, 400, 195, 450], fill=GOLD, outline=BLACK)
    draw_text(d, "WORLD CHAMPS!", 50, 560, 28, GREEN)

    # dividing line
    wobbly_line(d, W//2, 0, W//2, H, BLACK, 5)

    # ARGENTINA RIGHT — angry mob
    draw_text(d, "ARGENTINA", W//2 + 40, 25, 34, RED)
    draw_text(d, "MOB ATTACKS", W//2 + 40, 75, 28, RED)
    draw_text(d, "URUGUAYAN CONSULATE!", W//2 + 30, 108, 22, RED)

    # simple building (consulate)
    wobbly_rect(d, W//2+100, 170, W//2+380, 380, BLACK, 5, fill=LIGHTGRAY)
    draw_text(d, "CONSULATE", W//2+120, 200, 20, BLACK)
    # door
    wobbly_rect(d, W//2+210, 310, W//2+270, 380, BLACK, 4, fill=BROWN)
    # windows
    wobbly_rect(d, W//2+130, 230, W//2+190, 280, BLACK, 3, fill=LIGHTBLUE)
    wobbly_rect(d, W//2+290, 230, W//2+350, 280, BLACK, 3, fill=LIGHTBLUE)
    # angry stickmen with fists
    stickman(d, W//2+80, 380, 0.9)
    stickman(d, W//2+450, 370, 0.9)
    stickman(d, W//2+530, 385, 0.85)
    # angry faces
    draw_text(d, "GRRRR", W//2+440, 460, 22, RED)
    draw_text(d, ">:(", W//2+70, 460, 28, RED)

    # diplomatic break callout
    wobbly_rect(d, W//2+30, 510, W-30, 600, BLACK, 4, fill=YELLOW)
    draw_text(d, "Argentina breaks", W//2+50, 525, 22, BLACK)
    draw_text(d, "diplomatic relations!", W//2+50, 555, 22, RED)

    draw_text_centered(d, "Same match. Very different reactions.", W//2, 660, 30, BLACK)

    img.save(f"{OUT}/frame_06_aftermath.png")
    print("Saved frame 6")

# ─────────────────────────────────────────────────────────────────────────────
# IMAGE 7 — [11:15–12:00] Outro: Back to present, 2030 banner
# ─────────────────────────────────────────────────────────────────────────────
def img7():
    img, d = new_img()
    # sky
    d.rectangle([0, 0, W, 300], fill=SKYBLUE)
    # ground
    d.rectangle([0, 300, W, H], fill=LIGHTGREEN)

    # Big stadium (same as frame 1 but with 2030 banners)
    sx, sy, sw, sh = 320, 80, 640, 340
    d.rectangle([sx, sy+80, sx+sw, sy+sh], fill=GRAY)
    d.ellipse([sx, sy, sx+sw, sy+180], fill=GRAY, outline=BLACK)
    wobbly_rect(d, sx, sy+80, sx+sw, sy+sh, BLACK, 5)
    d.arc([sx, sy, sx+sw, sy+180], 180, 0, fill=BLACK, width=5)
    d.ellipse([sx+80, sy+120, sx+sw-80, sy+sh-30], fill=GREEN, outline=(100,200,100))

    # 2030 banners hanging from stadium
    banner_cols = [RED, BLUE, YELLOW, RED, BLUE]
    for i, bc in enumerate(banner_cols):
        bx = sx + 60 + i * 110
        wobbly_rect(d, bx, sy+5, bx+80, sy+60, BLACK, 3, fill=bc)
        draw_text(d, "2030", bx+5, sy+18, 20, (255,255,255))

    # plaque glinting (yellow sparkle)
    plaque_x, plaque_y = 210, 360
    wobbly_rect(d, plaque_x, plaque_y, plaque_x+150, plaque_y+65, GOLD, 4, fill=YELLOW)
    draw_text(d, "1930", plaque_x+30, plaque_y+8, 22, BLACK)
    draw_text(d, "PLAQUE", plaque_x+20, plaque_y+36, 20, BLACK)
    # sparkle lines around plaque
    for angle in [0, 45, 90, 135, 180, 225, 270, 315]:
        r = math.radians(angle)
        px = plaque_x + 75 + int(40*math.cos(r))
        py = plaque_y + 32 + int(30*math.sin(r))
        d.line([(plaque_x+75, plaque_y+32), (px, py)], fill=GOLD, width=3)

    # stickman with mic (narrator)
    stickman(d, 120, 420, 1.0)
    # mic
    wobbly_rect(d, 152, 380, 165, 415, BLACK, 3, fill=BLACK)
    d.ellipse([148, 365, 169, 390], fill=BLACK)
    # speech bubble
    wobbly_rect(d, 170, 340, 460, 420, BLACK, 3, fill=(255,255,200))
    draw_text(d, '"I\'m Nobody."', 185, 355, 22, BLACK)
    draw_text(d, '"You\'re Nobody."', 185, 385, 22, BLACK)

    # WAYAH logo bottom right
    wobbly_rect(d, 900, 560, 1230, 680, BLACK, 5, fill=BLACK)
    draw_text(d, "WAYAH.", 930, 580, 52, YELLOW)
    draw_text(d, "An NKN Joint.", 950, 640, 22, (180,180,180))

    draw_text_centered(d, "Same ground. Same ghosts. 100 years later.", W//2, 490, 28, BLACK)

    img.save(f"{OUT}/frame_07_outro.png")
    print("Saved frame 7")

random.seed(42)
img1()
img2()
img3()
img4()
img5()
img6()
img7()
print("\nAll 7 frames saved to", OUT)
