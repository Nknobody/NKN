from PIL import Image, ImageDraw, ImageFont
import math, os, random

W, H = 1280, 720
BG = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (210, 30, 30)
BLUE = (40, 90, 200)
LIGHTBLUE = (160, 210, 255)
SKYBLUE = (180, 225, 255)
GREEN = (45, 155, 45)
LIGHTGREEN = (160, 225, 160)
YELLOW = (255, 215, 30)
ORANGE = (230, 130, 30)
BROWN = (130, 80, 35)
GRAY = (155, 155, 155)
LIGHTGRAY = (210, 210, 210)
GOLD = (205, 165, 25)
DARKBLUE = (20, 40, 130)
WHITE = (255, 255, 255)
CREAM = (255, 248, 220)
SEPIA = (230, 200, 150)

OUT = "/home/user/NKN/wayah_stopmotion"
os.makedirs(OUT, exist_ok=True)

FRAME = [0]

def save(img, label):
    FRAME[0] += 1
    path = f"{OUT}/frame_{FRAME[0]:03d}_{label}.png"
    img.save(path)
    print(f"  [{FRAME[0]:03d}] {label}")
    return path

def new_img(bg=BG):
    img = Image.new("RGB", (W, H), bg)
    return img, ImageDraw.Draw(img)

def font(size):
    try:
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size)
    except:
        return ImageFont.load_default()

def txt(d, text, x, y, size=28, color=BLACK, center=False):
    f = font(size)
    if center:
        bb = d.textbbox((0,0), text, font=f)
        x = x - (bb[2]-bb[0])//2
        y = y - (bb[3]-bb[1])//2
    d.text((x, y), text, fill=color, font=f)

def wline(d, x1, y1, x2, y2, color=BLACK, w=4, wobble=3):
    steps = max(4, int(math.dist((x1,y1),(x2,y2))//20))
    pts = []
    for i in range(steps+1):
        t = i/steps
        px = x1+(x2-x1)*t + (random.randint(-wobble,wobble) if 0<i<steps else 0)
        py = y1+(y2-y1)*t + (random.randint(-wobble,wobble) if 0<i<steps else 0)
        pts.append((int(px),int(py)))
    for i in range(len(pts)-1):
        d.line([pts[i],pts[i+1]], fill=color, width=w)

def wrect(d, x1, y1, x2, y2, color=BLACK, w=4, fill=None, wobble=3):
    if fill: d.rectangle([x1,y1,x2,y2], fill=fill)
    wline(d,x1,y1,x2,y1,color,w,wobble)
    wline(d,x2,y1,x2,y2,color,w,wobble)
    wline(d,x2,y2,x1,y2,color,w,wobble)
    wline(d,x1,y2,x1,y1,color,w,wobble)

def sky_ground(d, sky=SKYBLUE, ground=LIGHTGREEN, horizon=380):
    d.rectangle([0,0,W,horizon], fill=sky)
    d.rectangle([0,horizon,W,H], fill=ground)

def stadium(d, cx, cy, w=500, h=280, color=BLACK, lw=5):
    # walls
    d.rectangle([cx-w//2, cy, cx+w//2, cy+h], fill=GRAY)
    # arch top
    d.ellipse([cx-w//2, cy-h//3, cx+w//2, cy+h//3], fill=GRAY, outline=color)
    d.arc([cx-w//2, cy-h//3, cx+w//2, cy+h//3], 180, 0, fill=color, width=lw)
    # walls outline
    wrect(d, cx-w//2, cy, cx+w//2, cy+h, color, lw)
    # field
    d.ellipse([cx-w//2+50, cy+30, cx+w//2-50, cy+h-20], fill=GREEN)

def stickman(d, cx, cy, scale=1.0, color=BLACK, arms="normal", leg="normal"):
    lw = max(3, int(4*scale))
    hr = int(22*scale)
    # head
    d.ellipse([cx-hr, cy-hr, cx+hr, cy+hr], outline=color, width=lw)
    er = max(2, int(3*scale))
    d.ellipse([cx-hr//2-er, cy-er, cx-hr//2+er, cy+er], fill=color)
    d.ellipse([cx+hr//2-er, cy-er, cx+hr//2+er, cy+er], fill=color)
    d.arc([cx-9, cy+4, cx+9, cy+13], 0, 180, fill=color, width=lw)
    bt = cy+hr; bb = bt+int(55*scale)
    wline(d, cx, bt, cx, bb, color, lw)
    ay = bt+int(18*scale)
    if arms == "up":
        wline(d, cx-int(32*scale), ay-int(22*scale), cx, ay, color, lw)
        wline(d, cx, ay, cx+int(32*scale), ay-int(22*scale), color, lw)
    elif arms == "one_up":
        wline(d, cx-int(32*scale), ay+int(10*scale), cx, ay, color, lw)
        wline(d, cx, ay, cx+int(32*scale), ay-int(22*scale), color, lw)
    elif arms == "cross":
        wline(d, cx-int(32*scale), ay-int(5*scale), cx, ay, color, lw)
        wline(d, cx, ay, cx+int(32*scale), ay-int(5*scale), color, lw)
    else:
        wline(d, cx-int(32*scale), ay+int(10*scale), cx, ay, color, lw)
        wline(d, cx, ay, cx+int(32*scale), ay+int(10*scale), color, lw)
    if leg == "kick":
        wline(d, cx, bb, cx-int(22*scale), bb+int(40*scale), color, lw)
        wline(d, cx, bb, cx+int(45*scale), bb+int(15*scale), color, lw)
    elif leg == "run1":
        wline(d, cx, bb, cx-int(30*scale), bb+int(35*scale), color, lw)
        wline(d, cx, bb, cx+int(15*scale), bb+int(42*scale), color, lw)
    elif leg == "run2":
        wline(d, cx, bb, cx-int(15*scale), bb+int(42*scale), color, lw)
        wline(d, cx, bb, cx+int(30*scale), bb+int(35*scale), color, lw)
    else:
        wline(d, cx, bb, cx-int(22*scale), bb+int(40*scale), color, lw)
        wline(d, cx, bb, cx+int(22*scale), bb+int(40*scale), color, lw)

def el_manco(d, cx, cy, scale=1.0, color=BLACK, arms="normal", leg="normal"):
    """One-armed stickman."""
    lw = max(3, int(4*scale))
    hr = int(22*scale)
    d.ellipse([cx-hr, cy-hr, cx+hr, cy+hr], outline=color, width=lw)
    er = max(2, int(3*scale))
    d.ellipse([cx-hr//2-er, cy-er, cx-hr//2+er, cy+er], fill=color)
    d.ellipse([cx+hr//2-er, cy-er, cx+hr//2+er, cy+er], fill=color)
    d.arc([cx-9, cy+4, cx+9, cy+13], 0, 180, fill=color, width=lw)
    bt = cy+hr; bb = bt+int(55*scale)
    wline(d, cx, bt, cx, bb, color, lw)
    ay = bt+int(18*scale)
    # Only right arm
    if arms == "up":
        wline(d, cx, ay, cx+int(32*scale), ay-int(22*scale), color, lw)
    else:
        wline(d, cx, ay, cx+int(32*scale), ay+int(10*scale), color, lw)
    # stub on left
    wline(d, cx, ay, cx-int(12*scale), ay+int(8*scale), color, lw)
    if leg == "kick":
        wline(d, cx, bb, cx-int(22*scale), bb+int(40*scale), color, lw)
        wline(d, cx, bb, cx+int(45*scale), bb+int(15*scale), color, lw)
    elif leg == "run1":
        wline(d, cx, bb, cx-int(30*scale), bb+int(35*scale), color, lw)
        wline(d, cx, bb, cx+int(15*scale), bb+int(42*scale), color, lw)
    else:
        wline(d, cx, bb, cx-int(22*scale), bb+int(40*scale), color, lw)
        wline(d, cx, bb, cx+int(22*scale), bb+int(40*scale), color, lw)

def ball(d, cx, cy, r=18, color=BLACK):
    d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=color)
    d.ellipse([cx-r+4, cy-r+4, cx+r-4, cy+r-4], fill=WHITE)
    d.ellipse([cx-r//2, cy-r//2, cx+r//2, cy+r//2], fill=color)

def net(d, cx, cy, w=100, h=70):
    wrect(d, cx-w//2, cy-h, cx+w//2, cy, BLACK, 4)
    for i in range(1,4):
        wline(d, cx-w//2, cy-h+i*h//3, cx+w//2, cy-h+i*h//3, GRAY, 2)
    for i in range(1,5):
        wline(d, cx-w//2+i*w//4, cy-h, cx-w//2+i*w//4, cy, GRAY, 2)

def speech(d, x, y, w, h, text, size=22, tail_dir="left"):
    wrect(d, x, y, x+w, y+h, BLACK, 3, fill=CREAM)
    if tail_dir == "left":
        d.polygon([(x+20,y+h),(x,y+h+20),(x+40,y+h)], fill=CREAM)
        wline(d, x+20, y+h, x, y+h+20, BLACK, 3)
        wline(d, x, y+h+20, x+40, y+h, BLACK, 3)
    else:
        d.polygon([(x+w-40,y+h),(x+w,y+h+20),(x+w-20,y+h)], fill=CREAM)
        wline(d, x+w-40, y+h, x+w, y+h+20, BLACK, 3)
        wline(d, x+w, y+h+20, x+w-20, y+h, BLACK, 3)
    txt(d, text, x+10, y+10, size, BLACK)

def scoreboard(d, u_score, a_score, label="", half=""):
    wrect(d, W//2-200, 20, W//2+200, 130, BLACK, 5, fill=BLACK)
    txt(d, "URU", W//2-185, 35, 32, WHITE)
    txt(d, str(u_score), W//2-65, 28, 55, YELLOW)
    txt(d, "-", W//2-18, 35, 50, WHITE)
    txt(d, str(a_score), W//2+18, 28, 55, YELLOW)
    txt(d, "ARG", W//2+100, 35, 32, WHITE)
    if half: txt(d, half, W//2, 90, 22, LIGHTGRAY, center=True)
    if label: txt(d, label, W//2, 148, 24, RED, center=True)

def confetti(d, n=80):
    for _ in range(n):
        x,y = random.randint(0,W), random.randint(0,H//2)
        c = random.choice([RED,GREEN,BLUE,YELLOW,ORANGE,(180,0,180)])
        r = random.randint(4,10)
        d.ellipse([x-r,y-r,x+r,y+r], fill=c)

def boat(d, cx, cy, scale=1.0):
    s = scale
    hull = [(cx-int(90*s),cy),(cx-int(110*s),cy+int(45*s)),(cx+int(110*s),cy+int(45*s)),(cx+int(90*s),cy)]
    d.polygon(hull, fill=BROWN, outline=BLACK)
    for i in range(len(hull)-1): wline(d,*hull[i],*hull[i+1],BLACK,4)
    wline(d, cx, cy, cx, cy-int(90*s), BLACK, 4)
    d.polygon([(cx,cy-int(90*s)),(cx,cy-int(15*s)),(cx+int(65*s),cy-int(52*s))], fill=(220,220,255),outline=BLACK)
    for dx in range(-int(150*s),int(150*s),int(30*s)):
        d.arc([cx+dx,cy+int(38*s),cx+dx+int(28*s),cy+int(58*s)],0,180,fill=BLUE,width=3)

def medal(d, cx, cy, year, r=40):
    d.ellipse([cx-r,cy-r,cx+r,cy+r], fill=GOLD, outline=BLACK)
    d.ellipse([cx-r+6,cy-r+6,cx+r-6,cy+r-6], outline=BLACK, width=2)
    txt(d, str(year), cx, cy, 20, BLACK, center=True)
    # ribbon
    d.polygon([(cx-12,cy-r),(cx,cy-r-20),(cx+12,cy-r)], fill=RED, outline=BLACK)

def trophy(d, cx, cy, scale=1.0):
    s=scale
    # cup
    d.polygon([(cx-int(50*s),cy-int(60*s)),(cx+int(50*s),cy-int(60*s)),(cx+int(35*s),cy),(cx-int(35*s),cy)], fill=GOLD, outline=BLACK)
    # handles
    d.arc([cx-int(70*s),cy-int(50*s),cx-int(40*s),cy-int(20*s)],90,270,fill=GOLD,width=5)
    d.arc([cx+int(40*s),cy-int(50*s),cx+int(70*s),cy-int(20*s)],270,90,fill=GOLD,width=5)
    # stem
    d.rectangle([cx-int(12*s),cy,cx+int(12*s),cy+int(30*s)],fill=GOLD,outline=BLACK)
    # base
    d.rectangle([cx-int(40*s),cy+int(30*s),cx+int(40*s),cy+int(45*s)],fill=GOLD,outline=BLACK)
    wrect(d,cx-int(40*s),cy+int(30*s),cx+int(40*s),cy+int(45*s),BLACK,3)

def flag_uru(d, cx, cy, w=80, h=50):
    # Uruguay: blue stripes with sun
    for i in range(4):
        d.rectangle([cx,cy+i*(h//4),cx+w,cy+(i+1)*(h//4)], fill=BLUE if i%2==0 else WHITE)
    d.ellipse([cx+w//4-15,cy+h//2-15,cx+w//4+15,cy+h//2+15], fill=YELLOW, outline=BLACK)
    wrect(d,cx,cy,cx+w,cy+h,BLACK,3)

def flag_arg(d, cx, cy, w=80, h=50):
    # Argentina: light blue white light blue with sun
    d.rectangle([cx,cy,cx+w,cy+h//3], fill=LIGHTBLUE)
    d.rectangle([cx,cy+h//3,cx+w,cy+2*h//3], fill=WHITE)
    d.rectangle([cx,cy+2*h//3,cx+w,cy+h], fill=LIGHTBLUE)
    d.ellipse([cx+w//2-12,cy+h//2-12,cx+w//2+12,cy+h//2+12], fill=YELLOW, outline=BLACK)
    wrect(d,cx,cy,cx+w,cy+h,BLACK,3)

random.seed(42)

print("=== WAYAH Ep.02 — Stop Motion Frames ===\n")

# ──────────────────────────────────────────────────────────
# COLD OPEN [00:00-00:30] — 8 frames
# ──────────────────────────────────────────────────────────
print("COLD OPEN")

# 1: distant stadium silhouette
img,d = new_img()
sky_ground(d, SKYBLUE, LIGHTGREEN, 400)
# tiny stadium far away
d.rectangle([500,330,780,400], fill=GRAY)
d.ellipse([500,290,780,360], fill=GRAY, outline=BLACK)
wline(d,500,360,500,400,BLACK,4); wline(d,780,360,780,400,BLACK,4)
txt(d,"Montevideo...",W//2,450,28,GRAY,center=True)
save(img,"cold_open_stadium_far")

# 2: stadium closer
img,d = new_img()
sky_ground(d)
stadium(d, W//2, 200, 580, 310)
txt(d,"ESTADIO CENTENARIO",W//2,560,34,BLACK,center=True)
save(img,"cold_open_stadium_close")

# 3: stickman walking toward stadium (frame 1 - leg pos 1)
img,d = new_img()
sky_ground(d)
stadium(d, 800, 200, 420, 240)
stickman(d, 300, 330, 1.1, leg="run1")
# motion lines
for i in range(3): wline(d,230-i*20,390+i*8,270-i*20,395+i*8,GRAY,2)
save(img,"cold_open_walk1")

# 4: stickman walking (frame 2 - leg pos 2)
img,d = new_img()
sky_ground(d)
stadium(d, 800, 200, 420, 240)
stickman(d, 380, 330, 1.1, leg="run2")
for i in range(3): wline(d,300-i*20,390+i*8,340-i*20,395+i*8,GRAY,2)
save(img,"cold_open_walk2")

# 5: stickman looks up at stadium
img,d = new_img()
sky_ground(d)
stadium(d, W//2+100, 160, 540, 300)
stickman(d, 220, 310, 1.2, arms="up")
# awe lines from stickman eyes upward
for a in range(-30,31,15):
    r=math.radians(a-90)
    wline(d,220,310,220+int(80*math.cos(r)),310+int(80*math.sin(r)),YELLOW,2)
speech(d,260,200,200,50,"WOW!",28)
save(img,"cold_open_stickman_looks")

# 6: plaque closeup
img,d = new_img()
d.rectangle([0,0,W,H], fill=LIGHTGRAY)
wrect(d,350,200,930,480,BLACK,6,fill=YELLOW)
txt(d,"1930",W//2,270,90,BLACK,center=True)
txt(d,"WORLD CUP FINAL",W//2,380,36,BLACK,center=True)
# shine star
for a in range(0,360,45):
    r=math.radians(a); wline(d,350,200,350+int(40*math.cos(r)),200+int(40*math.sin(r)),GOLD,4)
save(img,"cold_open_plaque")

# 7: WAYAH title
img,d = new_img()
txt(d,"WAYAH.",W//2,280,110,BLACK,center=True)
txt(d,'"Two Balls, One Crown"',W//2,420,36,GRAY,center=True)
wline(d,200,460,1080,460,BLACK,4)
save(img,"cold_open_title")

# 8: episode card
img,d = new_img()
wrect(d,150,150,1130,570,BLACK,6,fill=BLACK)
txt(d,"Episode 02",W//2,220,40,YELLOW,center=True)
txt(d,"Uruguay vs Argentina",W//2,295,46,WHITE,center=True)
wline(d,250,360,1030,360,GRAY,3)
txt(d,"1930 — Estadio Centenario",W//2,395,34,LIGHTGRAY,center=True)
save(img,"cold_open_episode_card")

# ──────────────────────────────────────────────────────────
# THE HOOK [00:30-01:20] — 12 frames
# ──────────────────────────────────────────────────────────
print("THE HOOK")

# 9: old TV with stadium
img,d = new_img()
wrect(d,300,150,980,600,BLACK,6,fill=GRAY)
wrect(d,350,180,930,520,BLACK,5,fill=SEPIA)
# tiny stadium on screen
d.rectangle([450,300,830,510], fill=(180,160,120))
d.ellipse([450,260,830,340], fill=(180,160,120),outline=(100,80,60))
wline(d,450,310,450,510,(100,80,60),4); wline(d,830,310,830,510,(100,80,60),4)
# antenna
wline(d,500,150,450,60,BLACK,5); wline(d,780,150,830,60,BLACK,5)
txt(d,"1930",550,480,32,(80,60,40))
save(img,"hook_old_tv")

# 10: 2030 hype banner
img,d = new_img()
d.rectangle([0,0,W,H],fill=(220,240,255))
wrect(d,100,100,1180,400,RED,6,fill=RED)
txt(d,"FIFA WORLD CUP 2030",W//2,175,52,WHITE,center=True)
txt(d,"100 YEARS. BACK WHERE IT STARTED.",W//2,265,30,YELLOW,center=True)
txt(d,"MONTEVIDEO",W//2,315,34,WHITE,center=True)
for _ in range(60):
    x,y=random.randint(0,W),random.randint(400,H)
    c=random.choice([RED,BLUE,YELLOW,GREEN])
    d.ellipse([x,y,x+10,y+10],fill=c)
save(img,"hook_2030_banner")

# 11: split 1930 vs 2030
img,d = new_img()
d.rectangle([0,0,W//2,H],fill=SEPIA)
d.rectangle([W//2,0,W,H],fill=(220,240,255))
wline(d,W//2,0,W//2,H,BLACK,6)
# left: old stadium sketch
d.rectangle([80,160,520,420],fill=(180,160,120))
d.ellipse([80,110,520,230],fill=(180,160,120),outline=(80,60,40))
txt(d,"1930",W//4,460,52,BLACK,center=True)
txt(d,"THE START",W//4,530,30,(100,80,60),center=True)
# right: modern stadium
stadium(d, W//2+340, 180, 420, 240)
txt(d,"2030",W//2+340,460,52,BLUE,center=True)
txt(d,"THE RETURN",W//2+340,530,30,BLUE,center=True)
save(img,"hook_split_eras")

# 12: two stickmen arguing about GOAT
img,d = new_img()
stickman(d,300,280,1.2,arms="up")
stickman(d,980,280,1.2,arms="up")
speech(d,170,130,230,60,"MESSI!",30)
speech(d,880,130,230,60,"PELE!",30,"right")
txt(d,"?",W//2,240,120,RED,center=True)
txt(d,"Who's the greatest EVER?",W//2,570,32,BLACK,center=True)
save(img,"hook_goat_argue")

# 13: globe with arrow to Uruguay
img,d = new_img()
cx,cy=W//2,320
r=220
d.ellipse([cx-r,cy-r,cx+r,cy+r],fill=LIGHTBLUE,outline=BLACK)
# crude continents
d.ellipse([cx-80,cy-120,cx+60,cy+60],fill=GREEN,outline=BLACK) # europe/africa blob
d.ellipse([cx-200,cy-80,cx-60,cy+100],fill=GREEN,outline=BLACK) # americas
d.ellipse([cx+60,cy-60,cx+180,cy+100],fill=GREEN,outline=BLACK) # asia
# arrow to south america
d.polygon([(cx-165,cy+90),(cx-145,cy+90),(cx-150,cy+115)],fill=RED)
wline(d,cx-100,cy+130,cx-155,cy+100,RED,4)
txt(d,"URUGUAY",cx-200,cy+125,22,RED)
txt(d,"Before trophies had names...",W//2,590,32,BLACK,center=True)
save(img,"hook_globe_uruguay")

# 14: 100 years timeline
img,d = new_img()
wline(d,100,380,1180,380,BLACK,5)
# left: 1930
d.ellipse([80,360,120,400],fill=GOLD,outline=BLACK)
trophy(d,100,230,0.6)
txt(d,"1930",100,430,28,BLACK,center=True)
txt(d,"First Final",100,465,22,GRAY,center=True)
# right: 2030
d.ellipse([1160,360,1200,400],fill=BLUE,outline=BLACK)
wrect(d,1130,210,1200,350,RED,4,fill=RED)
txt(d,"2030",W//2,430,28,BLUE,center=True)
txt(d,"100 YEARS",W//2,370,36,BLACK,center=True)
# tick marks
for i in range(1,10):
    x=100+i*118
    wline(d,x,368,x,392,GRAY,2)
    if i==5: txt(d,"1980",x,400,18,GRAY,center=True)
save(img,"hook_100yr_timeline")

# 15: crowd waving flags (frame 1)
img,d = new_img()
sky_ground(d,SKYBLUE,GREEN,550)
for i,cx in enumerate(range(80,1200,95)):
    cy=450
    col=[BLUE,WHITE,RED,GREEN,YELLOW,ORANGE,BLUE,RED,WHITE,GREEN,YELLOW,RED][i%12]
    stickman(d,cx,cy,0.75,arms="up")
    wrect(d,cx+18,cy-80,cx+55,cy-50,BLACK,2,fill=col)
    wline(d,cx+18,cy-80,cx+18,cy-20,BLACK,3)
txt(d,"A PLANET WATCHING",W//2,610,36,BLACK,center=True)
save(img,"hook_crowd_flags1")

# 16: crowd waving flags (frame 2 — arms slightly different)
img,d = new_img()
sky_ground(d,SKYBLUE,GREEN,550)
for i,cx in enumerate(range(80,1200,95)):
    cy=450
    col=[RED,WHITE,BLUE,YELLOW,GREEN,ORANGE,RED,BLUE,WHITE,YELLOW,GREEN,BLUE][i%12]
    stickman(d,cx,cy,0.75,arms="normal")
    wrect(d,cx-35,cy-75,cx-5,cy-48,BLACK,2,fill=col)
    wline(d,cx-5,cy-75,cx-5,cy-20,BLACK,3)
txt(d,"A PLANET WATCHING",W//2,610,36,BLACK,center=True)
save(img,"hook_crowd_flags2")

# 17: two rivals face-off
img,d = new_img()
stickman(d,250,250,1.3,arms="cross")
stickman(d,1030,250,1.3,arms="cross")
flag_uru(d,170,140)
flag_arg(d,1010,140)
# lightning bolt between
pts=[(W//2-20,200),(W//2+30,300),(W//2-10,300),(W//2+40,430)]
for i in range(len(pts)-1): d.line([pts[i],pts[i+1]],fill=RED,width=8)
txt(d,"ZERO LOVE LOST",W//2,570,38,BLACK,center=True)
save(img,"hook_rivals_faceoff")

# 18: first ever final card
img,d = new_img()
wrect(d,100,150,1180,560,BLACK,6,fill=(10,10,10))
wline(d,150,280,1130,280,RED,4)
txt(d,"THE FIRST WORLD CUP FINAL",W//2,195,42,YELLOW,center=True)
txt(d,"E  V  E  R",W//2,300,52,WHITE,center=True)
wline(d,150,400,1130,400,RED,4)
txt(d,"July 30, 1930  •  Montevideo",W//2,430,30,LIGHTGRAY,center=True)
txt(d,"Uruguay vs Argentina",W//2,475,36,WHITE,center=True)
save(img,"hook_first_final_card")

# 19: energy explosion
img,d = new_img()
cx,cy=W//2,H//2
for a in range(0,360,20):
    r=math.radians(a)
    col=random.choice([RED,YELLOW,ORANGE,BLUE])
    wline(d,cx,cy,cx+int(350*math.cos(r)),cy+int(280*math.sin(r)),col,5)
d.ellipse([cx-120,cy-120,cx+120,cy+120],fill=YELLOW,outline=BLACK)
txt(d,"GAME ON",cx,cy,40,BLACK,center=True)
save(img,"hook_game_on_explosion")

# 20: narrator intro card
img,d = new_img()
stickman(d,200,300,1.1)
wrect(d,280,180,1150,420,BLACK,4,fill=CREAM)
txt(d,'"Before any of that..."',300,210,28,BLACK)
txt(d,"Before the trophies had names.",300,260,24,BLACK)
txt(d,"Before the world was watching.",300,295,24,BLACK)
txt(d,"There was one stadium.",300,335,24,BLACK)
txt(d,"One weekend. One question.",300,370,24,BLACK)
save(img,"hook_narrator_intro")

# ──────────────────────────────────────────────────────────
# CHAPTER 1 — THE SETUP [01:20-04:30] — 35 frames
# ──────────────────────────────────────────────────────────
print("CHAPTER 1 — SETUP")

# 21: world map with 41 flags
img,d = new_img()
# crude map
d.ellipse([100,80,1180,640],fill=LIGHTBLUE,outline=BLACK)
land_blobs = [(300,200,520,420),(550,150,850,450),(870,160,1100,400),(200,420,420,600),(700,440,900,620)]
for b in land_blobs: d.ellipse(b,fill=GREEN,outline=BLACK)
# flag dots
positions=[(320,260),(400,280),(470,300),(600,230),(650,270),(700,250),(750,290),(800,230),(820,270),(900,210),
           (950,250),(980,290),(1020,230),(310,480),(350,500),(250,380),(600,470),(700,500),(760,460),(650,380)]
flag_cols=[RED,BLUE,GREEN,YELLOW,ORANGE,RED,BLUE,(150,0,150),GREEN,RED,BLUE,YELLOW,GREEN,ORANGE,RED,BLUE,GREEN,YELLOW,RED,BLUE]
for (fx,fy),fc in zip(positions,flag_cols):
    d.rectangle([fx-10,fy-8,fx+10,fy+8],fill=fc,outline=BLACK)
txt(d,"41 NATIONS INVITED",W//2,660,34,BLACK,center=True)
save(img,"setup_world_map_41")

# 22: big red X over most flags
img,d = new_img()
d.ellipse([100,80,1180,640],fill=LIGHTBLUE,outline=BLACK)
for b in land_blobs: d.ellipse(b,fill=GREEN,outline=BLACK)
for (fx,fy),fc in zip(positions,flag_cols):
    d.rectangle([fx-10,fy-8,fx+10,fy+8],fill=fc,outline=BLACK)
wline(d,100,80,1180,640,RED,14)
wline(d,1180,80,100,640,RED,14)
# circle 4 flags that stayed
for fx,fy in [(320,260),(400,280),(470,300),(310,480)]:
    d.ellipse([fx-25,fy-22,fx+25,fy+22],outline=GREEN,width=4)
txt(d,"MOST SAID NO",W//2,660,34,RED,center=True)
save(img,"setup_big_x_nobody_came")

# 23: only 13 showed up
img,d = new_img()
wrect(d,60,80,1220,200,BLACK,5,fill=YELLOW)
txt(d,"ONLY 13 SHOWED UP   (out of 41)",W//2,130,36,BLACK,center=True)
for i in range(13):
    cx=100+i*88; cy=380
    stickman(d,cx,cy,0.8)
wline(d,60,480,1220,480,GRAY,2)
txt(d,"28 countries stayed home.",W//2,520,28,GRAY,center=True)
save(img,"setup_only_13")

# 24: ocean with tiny distant boat
img,d = new_img()
d.rectangle([0,0,W,300],fill=SKYBLUE)
d.rectangle([0,300,W,H],fill=BLUE)
for i in range(0,W,40): d.arc([i,290,i+40,330],0,180,fill=LIGHTBLUE,width=3)
# tiny boat far
boat(d,W//2,280,0.35)
txt(d,"16 DAYS ON A BOAT",W//2,550,34,WHITE,center=True)
txt(d,"(from Europe to Uruguay)",W//2,600,24,LIGHTBLUE,center=True)
save(img,"setup_ocean_tiny_boat")

# 25: boat closer, stickman seasick (frame 1)
img,d = new_img()
d.rectangle([0,0,W,320],fill=SKYBLUE)
d.rectangle([0,320,W,H],fill=BLUE)
for i in range(0,W,40): d.arc([i,310,i+40,350],0,180,fill=LIGHTBLUE,width=3)
boat(d,W//2,310,0.8)
stickman(d,W//2-30,200,0.9)
# squiggly lines for seasick
for dy in range(0,30,8): wline(d,W//2+50,220+dy,W//2+90,220+dy+4,(0,200,0),3,1)
speech(d,W//2+80,140,220,55,"UGHHH...",24)
save(img,"setup_boat_seasick1")

# 26: boat closer frame 2 (bob)
img,d = new_img()
d.rectangle([0,0,W,310],fill=SKYBLUE)
d.rectangle([0,310,W,H],fill=BLUE)
for i in range(0,W,40): d.arc([i,300,i+40,340],0,180,fill=LIGHTBLUE,width=3)
boat(d,W//2,300,0.8)
stickman(d,W//2-30,190,0.9)
for dy in range(0,30,8): wline(d,W//2+50,215+dy,W//2+90,215+dy+4,(0,200,0),3,1)
speech(d,W//2+80,130,220,55,"UGHHH...",24)
save(img,"setup_boat_seasick2")

# 27: calendar — 16 days
img,d = new_img()
wrect(d,380,100,900,580,BLACK,5,fill=WHITE)
wrect(d,380,100,900,200,BLACK,5,fill=RED)
txt(d,"DAYS AT SEA",W//2,140,30,WHITE,center=True)
txt(d,"16",W//2,310,160,BLACK,center=True)
# X marks for days
for i in range(16):
    cx=430+i%8*60; cy=490+i//8*50
    wline(d,cx-12,cy-12,cx+12,cy+12,RED,3)
    wline(d,cx+12,cy-12,cx-12,cy+12,RED,3)
save(img,"setup_calendar_16_days")

# 28: stickman with empty wallet
img,d = new_img()
stickman(d,W//2-50,250,1.2,arms="one_up")
# wallet
wrect(d,W//2+60,250,W//2+160,320,BLACK,4,fill=BROWN)
wline(d,W//2+60,270,W//2+160,270,BLACK,3)
# nothing falling out, empty
txt(d,"GREAT DEPRESSION",W//2,520,32,BLACK,center=True)
txt(d,"No money to travel. Jobs at risk.",W//2,565,24,GRAY,center=True)
speech(d,W//2+120,150,270,60,"my JOB tho...",24)
save(img,"setup_empty_wallet")

# 29: Europe to Uruguay boat route
img,d = new_img()
d.rectangle([0,0,W,H],fill=LIGHTBLUE)
# crude Europe
d.ellipse([60,100,320,350],fill=GREEN,outline=BLACK)
txt(d,"EUROPE",160,380,24,BLACK,center=True)
# crude South America
d.ellipse([850,250,1150,600],fill=GREEN,outline=BLACK)
txt(d,"URUGUAY",990,620,24,BLACK,center=True)
# dotted route
for i in range(0,16):
    t=i/15
    x=int(200+690*t); y=int(220+80*math.sin(t*math.pi)+120*t)
    d.ellipse([x-6,y-6,x+6,y+6],fill=RED)
# arrow
d.polygon([(1010,450),(990,415),(1030,415)],fill=RED)
txt(d,"16-DAY VOYAGE",W//2,680,30,BLACK,center=True)
save(img,"setup_route_map")

# 30: 4 teams boarding — France stickman
img,d = new_img()
d.rectangle([0,0,W,H],fill=SKYBLUE)
boat(d,W//2+200,400,0.9)
stickman(d,300,310,1.1,leg="run2")
flag_col_stripe=[(BLUE,WHITE,RED),(BLACK,YELLOW,RED),(BLUE,YELLOW,RED),(BLUE,WHITE,RED)]
txt(d,"FRANCE boards the boat",W//2,600,30,BLACK,center=True)
# French flag
d.rectangle([240,130,310,190],fill=BLUE,outline=BLACK)
d.rectangle([310,130,360,190],fill=WHITE,outline=BLACK)
d.rectangle([360,130,420,190],fill=RED,outline=BLACK)
wrect(d,240,130,420,190,BLACK,3)
save(img,"setup_france_boards")

# 31: Belgium boards
img,d = new_img()
d.rectangle([0,0,W,H],fill=SKYBLUE)
boat(d,W//2+200,400,0.9)
stickman(d,300,310,1.1,leg="run1")
d.rectangle([240,130,300,190],fill=BLACK,outline=BLACK)
d.rectangle([300,130,360,190],fill=YELLOW,outline=BLACK)
d.rectangle([360,130,420,190],fill=RED,outline=BLACK)
wrect(d,240,130,420,190,BLACK,3)
txt(d,"BELGIUM boards the boat",W//2,600,30,BLACK,center=True)
save(img,"setup_belgium_boards")

# 32: Romania boards
img,d = new_img()
d.rectangle([0,0,W,H],fill=SKYBLUE)
boat(d,W//2+200,400,0.9)
stickman(d,330,310,1.1,leg="run2")
d.rectangle([240,130,300,190],fill=BLUE,outline=BLACK)
d.rectangle([300,130,360,190],fill=YELLOW,outline=BLACK)
d.rectangle([360,130,420,190],fill=RED,outline=BLACK)
wrect(d,240,130,420,190,BLACK,3)
txt(d,"ROMANIA boards the boat",W//2,600,30,BLACK,center=True)
save(img,"setup_romania_boards")

# 33: Yugoslavia boards
img,d = new_img()
d.rectangle([0,0,W,H],fill=SKYBLUE)
boat(d,W//2+200,400,0.9)
stickman(d,310,310,1.1)
d.rectangle([240,130,300,190],fill=BLUE,outline=BLACK)
d.rectangle([300,130,360,190],fill=WHITE,outline=BLACK)
d.rectangle([360,130,420,190],fill=RED,outline=BLACK)
wrect(d,240,130,420,190,BLACK,3)
txt(d,"YUGOSLAVIA boards the boat",W//2,600,30,BLACK,center=True)
save(img,"setup_yugoslavia_boards")

# 34: all 4 on the boat
img,d = new_img()
d.rectangle([0,0,W,350],fill=SKYBLUE)
d.rectangle([0,350,W,H],fill=BLUE)
for i in range(0,W,40): d.arc([i,340,i+40,380],0,180,fill=LIGHTBLUE,width=3)
boat(d,W//2,340,1.0)
for i,cx in enumerate([W//2-110,W//2-37,W//2+37,W//2+110]):
    stickman(d,cx,220,0.8,arms="up")
txt(d,"All 4 European teams. One boat.",W//2,560,30,BLACK,center=True)
save(img,"setup_four_on_boat")

# 35: Uruguay "WE'LL PAY" sign
img,d = new_img()
stickman(d,W//2-50,260,1.2,arms="up")
wrect(d,W//2+50,150,W//2+450,310,BLACK,5,fill=YELLOW)
txt(d,"WE WILL PAY",W//2+80,175,32,BLACK)
txt(d,"YOUR TRIP!",W//2+80,220,32,RED)
txt(d,"( Uruguay, 1930 )",W//2+80,265,20,GRAY)
flag_uru(d,W//2-160,120,90,60)
save(img,"setup_uruguay_pays")

# 36: trophy nobody has lifted
img,d = new_img()
sky_ground(d)
trophy(d,W//2,200,1.4)
txt(d,"?",W//2-10,80,100,RED,center=True)
txt(d,"No one has ever lifted this.",W//2,580,32,BLACK,center=True)
txt(d,"No one knows who's best.",W//2,625,28,GRAY,center=True)
save(img,"setup_trophy_mystery")

# 37: 1924 + 1928 Olympic gold medals
img,d = new_img()
medal(d,W//2-160,300,1924,70)
medal(d,W//2+160,300,1928,70)
wline(d,W//2-80,300,W//2+80,300,GOLD,4)
txt(d,"BACK-TO-BACK OLYMPIC GOLD",W//2,430,34,BLACK,center=True)
txt(d,"Uruguay earned the right to host",W//2,480,26,GRAY,center=True)
save(img,"setup_olympic_golds")

# 38: 100 years independence + host
img,d = new_img()
d.rectangle([0,0,W,H],fill=(220,240,220))
flag_uru(d,W//2-50,100,120,80)
txt(d,"1830 → 1930",W//2,240,38,BLACK,center=True)
txt(d,"100 YEARS OF INDEPENDENCE",W//2,300,34,GREEN,center=True)
txt(d,"+ Host the World Cup",W//2,360,30,BLACK,center=True)
txt(d,"= Perfect reason to celebrate",W//2,410,30,GRAY,center=True)
# party stars
for _ in range(20):
    x,y=random.randint(50,W-50),random.randint(440,H-30)
    for a2 in range(0,360,72):
        r2=math.radians(a2); wline(d,x,y,x+int(20*math.cos(r2)),y+int(20*math.sin(r2)),GOLD,3)
save(img,"setup_100yr_independence")

# 39: house party nobody came
img,d = new_img()
# house
wrect(d,200,200,700,550,BLACK,5,fill=CREAM)
d.polygon([(160,200),(450,60),(740,200)],fill=ORANGE,outline=BLACK)
# window
wrect(d,250,270,400,400,BLACK,4,fill=LIGHTBLUE)
wrect(d,500,270,650,400,BLACK,4,fill=LIGHTBLUE)
# door
wrect(d,350,420,550,550,BLACK,4,fill=BROWN)
# 3 lonely stickmen inside (through window)
stickman(d,310,330,0.5); stickman(d,450,320,0.5); stickman(d,580,330,0.5)
# many stickmen outside NOT coming
for i,cx in enumerate(range(820,1260,80)):
    stickman(d,cx,350,0.7,arms="cross")
wline(d,790,200,790,H-50,RED,5)
txt(d,"BIGGEST PARTY.",280,570,28,BLACK)
txt(d,"HALF THE GUESTS SKIPPED.",730,570,22,RED)
save(img,"setup_house_party")

# 40: ball on ground before kickoff
img,d = new_img()
sky_ground(d,SKYBLUE,GREEN,440)
ball(d,W//2,490,30)
wline(d,100,440,W-100,440,(100,200,100),3)
txt(d,"Before a single ball was kicked...",W//2,570,32,BLACK,center=True)
txt(d,"the tournament almost didn't happen.",W//2,620,26,GRAY,center=True)
save(img,"setup_ball_pregame")

# 41: FIFA near-collapse card
img,d = new_img()
wrect(d,150,150,1130,550,BLACK,5,fill=(240,240,200))
txt(d,'"Think about that."',W//2,210,36,BLACK,center=True)
wline(d,200,260,1080,260,BLACK,3)
txt(d,"The biggest tournament on Earth",W//2,295,28,BLACK,center=True)
txt(d,"started as a long-shot house party",W//2,335,28,BLACK,center=True)
txt(d,"half the guests skipped.",W//2,375,28,BLACK,center=True)
txt(d,"The whole thing nearly collapsed.",W//2,430,30,RED,center=True)
txt(d,"before a single ball was kicked.",W//2,470,28,GRAY,center=True)
save(img,"setup_collapse_quote")

# ──────────────────────────────────────────────────────────
# CHAPTER 2 — WHO ARE THEY [04:30-06:30] — 20 frames
# ──────────────────────────────────────────────────────────
print("CHAPTER 2 — WHO ARE THEY")

# 42: river plate splits map
img,d = new_img()
d.rectangle([0,0,W//2,H],fill=(220,240,255))
d.rectangle([W//2,0,W,H],fill=(255,220,220))
# river (wavy)
river_x=[]
for y in range(0,H,8):
    x=W//2+int(18*math.sin(y*0.05))
    river_x.append((x,y))
for i in range(len(river_x)-1):
    d.line([river_x[i],river_x[i+1]],fill=BLUE,width=22)
txt(d,"RIVER PLATE",W//2,360,18,WHITE,center=True)
txt(d,"URUGUAY",W//4,120,48,DARKBLUE,center=True)
txt(d,"ARGENTINA",W//2+W//4,120,44,RED,center=True)
save(img,"chap2_river_splits")

# 43: Uruguay — tiny nation
img,d = new_img()
d.rectangle([0,0,W//2,H],fill=(220,240,255))
d.rectangle([W//2,0,W,H],fill=WHITE)
txt(d,"URUGUAY",W//4,60,46,DARKBLUE,center=True)
txt(d,"Population:",60,130,26,BLACK)
txt(d,"1.75 MILLION",60,170,42,DARKBLUE)
txt(d,"(smaller than most",60,230,22,GRAY)
txt(d," modern cities today)",60,258,22,GRAY)
# 3 stickmen representing tiny pop
stickman(d,180,430,1.0); stickman(d,310,420,1.0); stickman(d,440,435,0.9)
txt(d,"Small nation. BIG heart.",W//4,600,26,DARKBLUE,center=True)
# right side: big comparison
txt(d,"The world:",W//2+60,130,26,GRAY)
for i,cx in enumerate(range(W//2+80,W-30,55)):
    stickman(d,cx,350,0.55)
txt(d,"(most cities are bigger)",W//2+60,550,22,GRAY)
save(img,"chap2_uruguay_tiny")

# 44: Olympic gold callout
img,d = new_img()
txt(d,"URUGUAY'S CREDENTIALS:",W//2,80,34,BLACK,center=True)
medal(d,W//2-200,300,1924,80)
medal(d,W//2+200,300,1928,80)
txt(d,"OLYMPIC GOLD",W//2-200,410,22,GOLD,center=True)
txt(d,"OLYMPIC GOLD",W//2+200,410,22,GOLD,center=True)
txt(d,"Paris",W//2-200,440,20,GRAY,center=True)
txt(d,"Amsterdam",W//2+200,440,20,GRAY,center=True)
wline(d,200,500,1080,500,GOLD,4)
txt(d,"Short-passing game that dazzled Europe.",W//2,545,28,BLACK,center=True)
save(img,"chap2_olympic_golds")

# 45: Argentina — bigger hungrier
img,d = new_img()
d.rectangle([0,0,W,H],fill=(255,220,220))
txt(d,"ARGENTINA",W//2,60,50,RED,center=True)
txt(d,"BIGGER.",W//2,150,56,BLACK,center=True)
txt(d,"HUNGRIER.",W//2,230,56,RED,center=True)
for cx in [200,350,500,650,800,950,1100]:
    stickman(d,cx,450,0.9,arms="up")
txt(d,"Led by top scorer: GUILLERMO STABILE",W//2,610,28,BLACK,center=True)
save(img,"chap2_argentina_hungry")

# 46: Stabile with big boot
img,d = new_img()
sky_ground(d)
# stickman with oversized foot
lw=4; hr=26; cx,cy=W//2,240
d.ellipse([cx-hr,cy-hr,cx+hr,cy+hr],outline=BLACK,width=lw)
d.ellipse([cx-8,cy-5,cx-2,cy+1],fill=BLACK); d.ellipse([cx+2,cy-5,cx+8,cy+1],fill=BLACK)
d.arc([cx-10,cy+4,cx+10,cy+14],0,180,fill=BLACK,width=lw)
bt=cy+hr; bb=bt+60
wline(d,cx,bt,cx,bb,BLACK,lw)
wline(d,cx-35,bt+20,cx,bt+18,BLACK,lw)
wline(d,cx,bt+18,cx+38,bt+25,BLACK,lw)
wline(d,cx,bb,cx-25,bb+45,BLACK,lw)
# oversized boot on right leg
d.ellipse([cx+10,bb+5,cx+130,bb+50],fill=BROWN,outline=BLACK)
txt(d,"STABILE",W//2+80,350,28,RED)
txt(d,"TOP SCORER",W//2+80,388,24,RED)
ball(d,W//2+145,bb+30,16)
save(img,"chap2_stabile_big_boot")

# 47: 1928 Olympic final scoreboard
img,d = new_img()
sky_ground(d,(200,220,240),GREEN,400)
stadium(d,W//2,120,500,260)
wrect(d,350,450,930,580,BLACK,5,fill=BLACK)
txt(d,"1928 OLYMPIC FINAL — AMSTERDAM",W//2,466,26,WHITE,center=True)
txt(d,"URU  2  -  1  ARG",W//2,510,40,YELLOW,center=True)
txt(d,"( after a replay )",W//2,550,22,LIGHTGRAY,center=True)
save(img,"chap2_1928_final_score")

# 48: Argentina angry after 1928
img,d = new_img()
stickman(d,W//2,240,1.3,arms="up")
# steaming head
for a2 in [30,90,150]: d.arc([W//2-30+a2*0,220-60,W//2+30,260-60],180,0,fill=ORANGE,width=4)
speech(d,W//2+80,80,300,60,"NOT HAPPY.",32)
txt(d,"Argentina wanted a rematch.",W//2,560,30,BLACK,center=True)
txt(d,"1930 was their chance.",W//2,605,28,RED,center=True)
save(img,"chap2_arg_angry")

# 49: shaking fists across river
img,d = new_img()
d.rectangle([0,0,W//2-30,H],fill=(220,240,255))
d.rectangle([W//2+30,0,W,H],fill=(255,220,220))
for y in range(0,H,8):
    x=W//2+int(18*math.sin(y*0.05))
    d.rectangle([x-30,y,x+30,y+8],fill=BLUE)
stickman(d,280,280,1.2,arms="up")
stickman(d,1000,280,1.2,arms="up")
# angry scribbles in bubbles
speech(d,120,150,230,60,"REMATCH!!",30)
speech(d,940,150,230,60,"BRING IT!",30,"right")
d.polygon([(W//2,300),(W//2-25,340),(W//2+25,340)],fill=RED)
wline(d,W//2-25,340,W//2+25,340,RED,4)
save(img,"chap2_fists_across_river")

# 50: same language sign
img,d = new_img()
wrect(d,100,160,1180,540,BLACK,5,fill=(255,255,220))
txt(d,"Same river.",W//2,210,42,BLUE,center=True)
txt(d,"Same language.",W//2,280,42,BLACK,center=True)
txt(d,"ZERO love lost.",W//2,360,50,RED,center=True)
wline(d,150,430,1130,430,BLACK,3)
txt(d,"— The River Plate Rivalry",W//2,470,28,GRAY,center=True)
save(img,"chap2_same_language")

# 51: July 30 match day calendar
img,d = new_img()
wrect(d,350,80,930,580,BLACK,5,fill=WHITE)
wrect(d,350,80,930,200,BLACK,5,fill=RED)
txt(d,"JULY 1930",W//2,133,38,WHITE,center=True)
# calendar grid
days=["SUN","MON","TUE","WED","THU","FRI","SAT"]
for i,day in enumerate(days): txt(d,day,380+i*78,215,18,GRAY)
# week with the 30th
for i,num in enumerate([27,28,29,30,31]):
    cx2=380+i*78
    if num==30:
        d.ellipse([cx2-25,270,cx2+50,340],fill=RED)
        txt(d,str(num),cx2+5,292,36,WHITE)
    else:
        txt(d,str(num),cx2+5,290,30,BLACK)
txt(d,"MATCH DAY",W//2,430,44,RED,center=True)
txt(d,"July 30, 1930",W//2,490,30,BLACK,center=True)
save(img,"chap2_match_day_calendar")

# 52: world is watching
img,d = new_img()
cx,cy=W//2,H//2
# circle of stickmen looking inward
for i in range(16):
    a2=math.radians(i*22.5)
    sx=cx+int(280*math.cos(a2)); sy=cy+int(200*math.sin(a2))
    stickman(d,sx,sy,0.6)
# ball in center
ball(d,cx,cy,35)
txt(d,"THE WHOLE WORLD IS WATCHING",W//2,640,32,BLACK,center=True)
save(img,"chap2_world_watching")

# ──────────────────────────────────────────────────────────
# CHAPTER 3 — THE MATCH [06:30-09:45] — 30 frames
# ──────────────────────────────────────────────────────────
print("CHAPTER 3 — THE MATCH")

# 53: two teams line up
img,d = new_img()
d.rectangle([0,0,W,H],fill=GREEN)
# field markings
wrect(d,60,50,W-60,H-50,(80,180,80),3)
d.ellipse([W//2-80,H//2-80,W//2+80,H//2+80],outline=(80,180,80),width=3)
wline(d,W//2,50,W//2,H-50,(80,180,80),3)
for i in range(5):
    stickman(d,200,120+i*105,0.75,color=(20,60,200))
for i in range(5):
    stickman(d,1080,120+i*105,0.75,color=(150,180,255))
txt(d,"URU",130,50,28,WHITE)
txt(d,"ARG",1055,50,28,WHITE)
txt(d,"JULY 30, 1930",W//2,670,24,WHITE,center=True)
save(img,"match_teams_lineup")

# 54: coin toss
img,d = new_img()
d.rectangle([0,0,W,H],fill=GREEN)
# referee
stickman(d,W//2,230,1.1,color=BLACK,arms="up")
# striped shirt on referee
for i in range(4):
    y=330+i*14
    wline(d,W//2-18,y,W//2+18,y,WHITE,3)
# coin in air
d.ellipse([W//2-20,100,W//2+20,140],fill=GOLD,outline=BLACK)
for a2 in range(0,360,60):
    r2=math.radians(a2); wline(d,W//2,120,W//2+int(15*math.cos(r2)),120+int(15*math.sin(r2)),YELLOW,2)
stickman(d,W//2-200,260,1.0,color=(20,60,200))
stickman(d,W//2+200,260,1.0,color=(100,140,220))
txt(d,"COIN TOSS",W//2,600,34,WHITE,center=True)
save(img,"match_coin_toss")

# 55: THE BALL DRAMA — two different balls
img,d = new_img()
d.rectangle([0,0,W,H],fill=CREAM)
txt(d,"THE BALL DRAMA",W//2,70,44,BLACK,center=True)
wline(d,100,120,W-100,120,BLACK,4)
# URU ball (left)
ball(d,350,300,55)
txt(d,"URU BALL",350,390,28,BLACK,center=True)
txt(d,"2nd Half",350,430,24,GRAY,center=True)
# ARG ball (right)
ball(d,930,300,55,(40,40,40))
d.ellipse([895,265,965,335],outline=WHITE,width=3)
txt(d,"ARG BALL",930,390,28,BLACK,center=True)
txt(d,"1st Half",930,430,24,GRAY,center=True)
# vs
txt(d,"VS",W//2,290,60,RED,center=True)
stickman(d,W//2-180,510,0.9,arms="up")
stickman(d,W//2+180,510,0.9,arms="up")
speech(d,W//2-400,390,200,55,"OUR ball!",22)
speech(d,W//2+200,390,200,55,"OUR ball!",22,"right")
txt(d,"They couldn't agree. So they used both.",W//2,640,26,BLACK,center=True)
save(img,"match_ball_drama")

# 56: kickoff
img,d = new_img()
d.rectangle([0,0,W,H],fill=GREEN)
d.ellipse([W//2-80,H//2-80,W//2+80,H//2+80],outline=(80,180,80),width=3)
wline(d,W//2,50,W//2,H-50,(80,180,80),3)
stickman(d,W//2-40,H//2-30,1.0,leg="kick",color=(20,60,200))
ball(d,W//2+70,H//2+20,22)
for i in range(4): wline(d,W//2+70,H//2+20,W//2+70+20+i*15,H//2+20+i*5,YELLOW,2)
txt(d,"KICKOFF!",W//2,610,40,WHITE,center=True)
txt(d,"0:00",60,40,30,WHITE)
save(img,"match_kickoff")

# 57: Dorado scores 1-0 (ball approaching)
img,d = new_img()
d.rectangle([0,0,W,H],fill=GREEN)
net(d,W//2+400,300,130,90)
stickman(d,W//2-100,300,1.0,leg="kick",color=(20,60,200))
ball(d,W//2+200,310,22)
for i in range(5): wline(d,W//2+100+i*20,310,W//2+200,310,YELLOW,2)
txt(d,"12'  — DORADO SHOOTS!",W//2,600,34,WHITE,center=True)
save(img,"match_dorado_shoots")

# 58: GOAL! 1-0 Uruguay
img,d = new_img()
d.rectangle([0,0,W,H],fill=GREEN)
net(d,W//2,300,140,100)
ball(d,W//2+20,270,22)
for a2 in range(0,360,25):
    r2=math.radians(a2); wline(d,W//2,150,W//2+int(120*math.cos(r2)),150+int(80*math.sin(r2)),YELLOW,4)
wrect(d,200,50,1080,180,BLACK,5,fill=RED)
txt(d,"GOAL!  1 - 0  URUGUAY",W//2,100,44,WHITE,center=True)
txt(d,"DORADO  —  12th MINUTE",W//2,148,26,YELLOW,center=True)
stickman(d,300,420,1.1,arms="up",color=(20,60,200))
stickman(d,450,410,1.1,arms="up",color=(20,60,200))
save(img,"match_goal_dorado_10")

# 59: Argentina equalizes — Peucelle running
img,d = new_img()
d.rectangle([0,0,W,H],fill=GREEN)
stickman(d,W//2,260,1.1,leg="run1",color=(100,140,220))
ball(d,W//2+60,380,22)
for i in range(4): wline(d,W//2-60+i*15,350,W//2,350-i*5,(100,140,220),2)
txt(d,"PEUCELLE",W//2,190,30,WHITE,center=True)
txt(d,"Argentina fights back!",W//2,580,32,WHITE,center=True)
save(img,"match_peucelle_runs")

# 60: 1-1 equalized
img,d = new_img()
d.rectangle([0,0,W,H],fill=GREEN)
net(d,200,300,130,90)
ball(d,200,270,22)
wrect(d,W//2-300,50,W//2+300,160,BLACK,5,fill=BLACK)
txt(d,"1 - 1",W//2,80,65,YELLOW,center=True)
txt(d,"PEUCELLE EQUALIZES",W//2,148,28,WHITE,center=True)
stickman(d,950,380,1.1,arms="up",color=(100,140,220))
stickman(d,1080,370,1.0,arms="up",color=(100,140,220))
save(img,"match_equalizer_11")

# 61: Stabile gives Argentina lead
img,d = new_img()
d.rectangle([0,0,W,H],fill=GREEN)
stickman(d,W//2+100,280,1.1,leg="kick",color=(100,140,220))
ball(d,200,330,24)
for i in range(6): wline(d,200+i*40,330,400+i*20,330+i*5,YELLOW,3)
net(d,150,340,130,90)
wrect(d,W//2-250,50,W//2+250,155,BLACK,5,fill=BLACK)
txt(d,"2 - 1  ARG",W//2,80,55,YELLOW,center=True)
txt(d,"STABILE!  HALFTIME LEAD!",W//2,148,26,WHITE,center=True)
save(img,"match_stabile_21")

# 62: halftime scoreboard
img,d = new_img()
d.rectangle([0,0,W,H],fill=(50,50,50))
wrect(d,200,150,1080,420,BLACK,6,fill=BLACK)
txt(d,"H A L F T I M E",W//2,175,36,YELLOW,center=True)
wline(d,250,240,1030,240,GRAY,3)
txt(d,"ARGENTINA",W//2-230,270,34,WHITE,center=True)
txt(d,"2",W//2-120,260,90,YELLOW,center=True)
txt(d,"-",W//2,270,70,WHITE,center=True)
txt(d,"1",W//2+80,260,90,YELLOW,center=True)
txt(d,"URUGUAY",W//2+180,270,34,WHITE,center=True)
txt(d,"Argentina leads at the break.",W//2,530,30,LIGHTGRAY,center=True)
save(img,"match_halftime_21")

# 63: Uruguay halftime huddle
img,d = new_img()
d.rectangle([0,0,W,H],fill=GREEN)
# circle of stickmen
for i in range(6):
    a2=math.radians(i*60)
    cx2=W//2+int(160*math.cos(a2)); cy2=H//2+int(120*math.sin(a2))
    stickman(d,cx2,cy2,0.8,color=(20,60,200))
# central speaker
stickman(d,W//2,H//2-40,1.0,arms="up",color=(20,60,200))
speech(d,W//2+80,120,360,60,"WE CAN DO THIS!!",26)
txt(d,"HALFTIME HUDDLE",W//2,620,30,WHITE,center=True)
save(img,"match_halftime_huddle")

# 64: 2nd half kickoff
img,d = new_img()
d.rectangle([0,0,W,H],fill=GREEN)
d.ellipse([W//2-80,H//2-80,W//2+80,H//2+80],outline=(80,180,80),width=3)
wline(d,W//2,50,W//2,H-50,(80,180,80),3)
stickman(d,W//2+30,H//2-20,1.0,leg="kick",color=(20,60,200))
ball(d,W//2-60,H//2+15,22)
txt(d,"2nd HALF",W//2,610,38,WHITE,center=True)
txt(d,"45:00",60,40,30,WHITE)
save(img,"match_2ndhalf_kickoff")

# 65: Cea equalizes — running
img,d = new_img()
d.rectangle([0,0,W,H],fill=GREEN)
stickman(d,W//2-80,270,1.1,leg="run2",color=(20,60,200))
ball(d,W//2+50,360,22)
txt(d,"CEA",W//2-80,195,34,WHITE,center=True)
txt(d,"Uruguay pressing...",W//2,590,30,WHITE,center=True)
save(img,"match_cea_running")

# 66: 2-2 equalized
img,d = new_img()
d.rectangle([0,0,W,H],fill=GREEN)
net(d,200,290,130,90)
ball(d,210,265,22)
wrect(d,W//2-280,40,W//2+280,155,BLACK,5,fill=DARKBLUE)
txt(d,"2 - 2",W//2,60,68,YELLOW,center=True)
txt(d,"CEA LEVELS IT!",W//2,140,30,WHITE,center=True)
stickman(d,900,380,1.1,arms="up",color=(20,60,200))
stickman(d,1040,370,1.0,arms="up",color=(20,60,200))
for a2 in range(0,360,30): d.line([(W//2,H//2-60),(W//2+int(50*math.cos(math.radians(a2))),H//2-60+int(40*math.sin(math.radians(a2))))],fill=YELLOW,width=3)
save(img,"match_cea_22")

# 67: Iriarte scores — 68th minute
img,d = new_img()
d.rectangle([0,0,W,H],fill=GREEN)
stickman(d,W//2-50,270,1.1,leg="kick",color=(20,60,200))
ball(d,W//2+200,310,24)
net(d,W-180,320,130,90)
for i in range(5): wline(d,W//2+100+i*25,310-i*3,W//2+200,310,YELLOW,3)
txt(d,"68'  —  IRIARTE!",W//2,590,36,WHITE,center=True)
save(img,"match_iriarte_shoots")

# 68: 3-2 scoreboard
img,d = new_img()
d.rectangle([0,0,W,H],fill=GREEN)
wrect(d,W//2-280,40,W//2+280,155,BLACK,5,fill=BLACK)
txt(d,"3 - 2  URUGUAY!",W//2,68,52,YELLOW,center=True)
txt(d,"IRIARTE  68th MINUTE",W//2,135,26,WHITE,center=True)
confetti(d,40)
stickman(d,300,390,1.1,arms="up",color=(20,60,200))
stickman(d,450,380,1.0,arms="up",color=(20,60,200))
stickman(d,600,395,1.1,arms="up",color=(20,60,200))
txt(d,"URU lead with minutes to go!",W//2,600,28,WHITE,center=True)
save(img,"match_iriarte_32")

# 69: stadium erupts
img,d = new_img()
stadium(d,W//2,100,600,360)
for a2 in range(0,360,15):
    r2=math.radians(a2); L=random.randint(180,320)
    col=random.choice([YELLOW,RED,BLUE,WHITE,ORANGE])
    wline(d,W//2,290,W//2+int(L*math.cos(r2)),290+int(L*math.sin(r2)),col,3)
txt(d,"THE STADIUM ERUPTS",W//2,590,36,BLACK,center=True)
save(img,"match_stadium_erupts")

# 70: El Manco — close up reveal
img,d = new_img()
d.rectangle([0,0,W,H],fill=GREEN)
el_manco(d,W//2,220,1.3)
wrect(d,W//2-320,510,W//2+320,620,BLACK,5,fill=BLACK)
txt(d,'"EL MANCO"',W//2,530,38,YELLOW,center=True)
txt(d,"Hector Castro — lost forearm as a child",W//2,575,24,WHITE,center=True)
txt(d,"Now 90 minutes in. Game almost over.",W//2,660,26,GRAY,center=True)
save(img,"match_el_manco_reveal")

# 71: El Manco runs (frame 1)
img,d = new_img()
d.rectangle([0,0,W,H],fill=GREEN)
el_manco(d,W//2-100,270,1.2,leg="run1")
ball(d,W//2+80,380,22)
for i in range(5): wline(d,W//2-180+i*15,360,W//2-100,360+i*5,YELLOW,2)
txt(d,"CASTRO BREAKS FORWARD...",W//2,590,32,WHITE,center=True)
save(img,"match_manco_run1")

# 72: El Manco runs (frame 2)
img,d = new_img()
d.rectangle([0,0,W,H],fill=GREEN)
el_manco(d,W//2,270,1.2,leg="run2")
ball(d,W//2+120,370,22)
for i in range(5): wline(d,W//2-80+i*15,355,W//2+20,355+i*4,YELLOW,2)
txt(d,"CASTRO BREAKS FORWARD...",W//2,590,32,WHITE,center=True)
save(img,"match_manco_run2")

# 73: El Manco shoots
img,d = new_img()
d.rectangle([0,0,W,H],fill=GREEN)
el_manco(d,W//2-120,280,1.2,leg="kick")
ball(d,W//2+200,350,26)
net(d,W-200,350,140,100)
for i in range(6): wline(d,W//2+80+i*25,350-i*3,W//2+200,350,(255,220,0),4)
txt(d,"EL MANCO SHOOTS!!!",W//2,600,38,WHITE,center=True)
save(img,"match_manco_shoots")

# 74: GOAL! 4-2 explosion
img,d = new_img()
d.rectangle([0,0,W,H],fill=(0,0,0))
for a2 in range(0,360,15):
    r2=math.radians(a2); L=random.randint(200,380)
    col=random.choice([YELLOW,RED,ORANGE,WHITE,GOLD])
    wline(d,W//2,H//2,W//2+int(L*math.cos(r2)),H//2+int(L*math.sin(r2)),col,6)
d.ellipse([W//2-160,H//2-100,W//2+160,H//2+100],fill=YELLOW,outline=BLACK)
txt(d,"4 - 2 !!!!",W//2,H//2,64,BLACK,center=True)
txt(d,"EL MANCO — ONE ARMED HERO",W//2,600,30,YELLOW,center=True)
save(img,"match_goal_42_explosion")

# 75: El Manco celebrates
img,d = new_img()
d.rectangle([0,0,W,H],fill=GREEN)
el_manco(d,W//2,220,1.4,arms="up")
confetti(d,100)
txt(d,"HECTOR CASTRO",W//2,560,36,YELLOW,center=True)
txt(d,'"EL MANCO" — THE ONE-ARMED ONE',W//2,605,28,WHITE,center=True)
save(img,"match_manco_celebrates")

# 76: final whistle
img,d = new_img()
d.rectangle([0,0,W,H],fill=GREEN)
# referee arms up
stickman(d,W//2,240,1.2,arms="up",color=BLACK)
for i in range(4): wline(d,W//2-8+i*5,240,W//2-8+i*5,240,WHITE,3)
txt(d,"FULL TIME!",W//2,590,52,WHITE,center=True)
confetti(d,60)
save(img,"match_final_whistle")

# 77: final scoreboard
img,d = new_img()
d.rectangle([0,0,W,H],fill=(20,20,60))
wrect(d,120,120,1160,500,GOLD,6,fill=BLACK)
txt(d,"FULL TIME",W//2,148,34,GOLD,center=True)
wline(d,180,210,1100,210,GOLD,3)
txt(d,"URUGUAY",W//2-230,240,40,WHITE,center=True)
txt(d,"4",W//2-80,225,100,YELLOW,center=True)
txt(d,"-",W//2,240,70,WHITE,center=True)
txt(d,"2",W//2+35,225,100,YELLOW,center=True)
txt(d,"ARGENTINA",W//2+120,240,40,WHITE,center=True)
wline(d,180,390,1100,390,GOLD,3)
txt(d,"WORLD CHAMPIONS 1930",W//2,415,34,GOLD,center=True)
trophy(d,W//2,570,0.55)
save(img,"match_final_scoreboard_42")

# ──────────────────────────────────────────────────────────
# CHAPTER 4 — AFTERMATH [09:45-11:15] — 15 frames
# ──────────────────────────────────────────────────────────
print("CHAPTER 4 — AFTERMATH")

# 78: Uruguay newspaper
img,d = new_img()
wrect(d,100,60,1180,640,BLACK,5,fill=WHITE)
wrect(d,100,60,1180,200,BLACK,5,fill=DARKBLUE)
txt(d,"EL DÍA — JULY 31, 1930",W//2,80,24,WHITE,center=True)
txt(d,"¡CAMPEONES!",W//2,120,70,YELLOW,center=True)
wline(d,150,210,1130,210,BLACK,4)
txt(d,"URUGUAY WINS FIRST",W//2,240,42,BLACK,center=True)
txt(d,"WORLD CUP FINAL",W//2,295,42,BLACK,center=True)
wline(d,150,355,1130,355,BLACK,2)
txt(d,"4-2 victory over Argentina in front of packed Centenario",W//2,385,24,BLACK,center=True)
stickman(d,200,520,0.9,arms="up"); stickman(d,340,510,0.9,arms="up")
txt(d,"Uruguay celebrates!",520,510,28,BLACK)
save(img,"aftermath_uru_newspaper")

# 79: stickmen dancing in streets (frame 1)
img,d = new_img()
d.rectangle([0,0,W,H],fill=LIGHTBLUE)
d.rectangle([0,H-80,W,H],fill=GRAY)
for cx in [150,310,470,640,810,960,1120]:
    stickman(d,cx,380,1.0,arms="up")
confetti(d,100)
txt(d,"NATIONAL CELEBRATION!",W//2,580,36,BLACK,center=True)
txt(d,"The streets of Montevideo",W//2,630,26,GRAY,center=True)
save(img,"aftermath_dancing1")

# 80: dancing frame 2
img,d = new_img()
d.rectangle([0,0,W,H],fill=LIGHTBLUE)
d.rectangle([0,H-80,W,H],fill=GRAY)
for cx in [150,310,470,640,810,960,1120]:
    stickman(d,cx,380,1.0,arms="one_up")
confetti(d,100)
txt(d,"NATIONAL CELEBRATION!",W//2,580,36,BLACK,center=True)
txt(d,"July 31 declared a national holiday",W//2,630,26,GRAY,center=True)
save(img,"aftermath_dancing2")

# 81: national holiday calendar
img,d = new_img()
wrect(d,350,80,930,560,BLACK,5,fill=WHITE)
wrect(d,350,80,930,200,BLACK,5,fill=RED)
txt(d,"JULY 1930",W//2,133,38,WHITE,center=True)
for i,num in enumerate([27,28,29,30,31]):
    cx2=390+i*90
    if num==30:
        d.ellipse([cx2-28,280,cx2+62,360],fill=BLUE); txt(d,"30",cx2+6,302,40,WHITE)
    elif num==31:
        d.ellipse([cx2-28,280,cx2+62,360],fill=GREEN,outline=BLACK); txt(d,"31",cx2+6,302,40,BLACK)
    else:
        txt(d,str(num),cx2+6,300,36,BLACK)
txt(d,"JULY 31 = NATIONAL HOLIDAY",W//2,420,30,GREEN,center=True)
save(img,"aftermath_holiday_calendar")

# 82: fireworks
img,d = new_img()
d.rectangle([0,0,W,H],fill=(5,5,30))
centers=[(250,200),(640,150),(1000,220),(430,350),(850,300),(180,420),(1050,400)]
colors_fw=[[RED,ORANGE,YELLOW],[BLUE,LIGHTBLUE,WHITE],[GREEN,(0,255,0),YELLOW],[RED,WHITE,BLUE],[GOLD,YELLOW,ORANGE],[WHITE,LIGHTBLUE,BLUE],[RED,YELLOW,ORANGE]]
for (fcx,fcy),fcols in zip(centers,colors_fw):
    for a2 in range(0,360,18):
        r2=math.radians(a2); L=random.randint(50,90)
        col=random.choice(fcols)
        wline(d,fcx,fcy,fcx+int(L*math.cos(r2)),fcy+int(L*math.sin(r2)),col,4)
    d.ellipse([fcx-8,fcy-8,fcx+8,fcy+8],fill=WHITE)
txt(d,"¡FIESTA!",W//2,580,60,YELLOW,center=True)
save(img,"aftermath_fireworks")

# 83: Argentina newspaper — angry
img,d = new_img()
wrect(d,100,60,1180,620,BLACK,5,fill=CREAM)
wrect(d,100,60,1180,185,BLACK,5,fill=RED)
txt(d,"LA PRENSA — ARGENTINA",W//2,80,24,WHITE,center=True)
txt(d,"¡ESCÁNDALO!",W//2,118,62,WHITE,center=True)
wline(d,150,195,1130,195,BLACK,4)
txt(d,"ARGENTINA OUTRAGED",W//2,225,40,BLACK,center=True)
txt(d,"After defeat in Montevideo final",W//2,275,28,GRAY,center=True)
stickman(d,250,470,1.0,arms="up")
stickman(d,450,460,1.0,arms="up")
# angry scribbles
speech(d,500,370,340,55,"OUTRAGE!",30)
save(img,"aftermath_arg_newspaper")

# 84: angry mob assembles (frame 1)
img,d = new_img()
d.rectangle([0,0,W,H],fill=(255,220,200))
for cx in [100,220,350,480,610,740,870,1000,1130]:
    stickman(d,cx,370,0.85,arms="up")
for i in range(0,W,130):
    wrect(d,i+30,200,i+100,240,BLACK,3,fill=RED)
    txt(d,"GRRRR",i+32,200,16,WHITE)
txt(d,"ANGRY MOB — BUENOS AIRES",W//2,570,34,BLACK,center=True)
txt(d,"Marching on the Uruguayan consulate",W//2,620,26,RED,center=True)
save(img,"aftermath_mob1")

# 85: angry mob marching (frame 2)
img,d = new_img()
d.rectangle([0,0,W,H],fill=(255,220,200))
for cx in [140,270,400,530,660,790,920,1050,1180]:
    stickman(d,cx,370,0.85,arms="one_up")
d.polygon([(W//2-30,200),(W//2+30,200),(W//2,150)],fill=RED)
txt(d,"MARCH!",W//2,220,28,RED,center=True)
txt(d,"ANGRY MOB — BUENOS AIRES",W//2,570,34,BLACK,center=True)
save(img,"aftermath_mob2")

# 86: consulate building
img,d = new_img()
d.rectangle([0,0,W,H],fill=LIGHTBLUE)
d.rectangle([0,H-80,W,H],fill=GRAY)
# building
d.rectangle([300,120,980,600],fill=LIGHTGRAY,outline=BLACK)
wrect(d,300,120,980,600,BLACK,5)
for col in range(4):
    cx2=360+col*160
    wline(d,cx2,120,cx2,600,BLACK,4)
txt(d,"URUGUAYAN",W//2,165,30,BLACK,center=True)
txt(d,"CONSULATE",W//2,205,30,BLACK,center=True)
for wx in [370,530,690,850]:
    wrect(d,wx,280,wx+80,360,BLACK,4,fill=LIGHTBLUE)
wrect(d,590,450,710,600,BLACK,4,fill=BROWN)
# steps
d.rectangle([520,580,760,615],fill=LIGHTGRAY,outline=BLACK)
txt(d,"Buenos Aires, Argentina",W//2,660,26,GRAY,center=True)
save(img,"aftermath_consulate_building")

# 87: broken window — attack
img,d = new_img()
d.rectangle([0,0,W,H],fill=LIGHTBLUE)
d.rectangle([0,H-80,W,H],fill=GRAY)
d.rectangle([300,120,980,600],fill=LIGHTGRAY,outline=BLACK)
wrect(d,300,120,980,600,BLACK,5)
for wx in [370,530,690,850]:
    wrect(d,wx,280,wx+80,360,BLACK,4,fill=LIGHTBLUE)
wrect(d,590,450,710,600,BLACK,4,fill=BROWN)
d.rectangle([520,580,760,615],fill=LIGHTGRAY,outline=BLACK)
# broken window — X
wrect(d,530,280,610,360,BLACK,4,fill=(200,220,240))
wline(d,530,280,610,360,RED,5); wline(d,610,280,530,360,RED,5)
# rock
d.ellipse([540,340,560,360],fill=BROWN,outline=BLACK)
txt(d,"MOB ATTACKS CONSULATE",W//2,640,30,RED,center=True)
stickman(d,140,410,0.9,arms="up"); stickman(d,1060,410,0.9,arms="up")
save(img,"aftermath_broken_window")

# 88: diplomatic relations severed
img,d = new_img()
d.rectangle([0,0,W,H],fill=CREAM)
flag_uru(d,200,250,110,75)
flag_arg(d,970,250,110,75)
# chain link being cut
for i in range(7):
    cx2=360+i*80; cy2=295
    d.ellipse([cx2-20,cy2-12,cx2+20,cy2+12],outline=GRAY,width=4)
# scissors
d.polygon([(620,250),(650,295),(680,250)],fill=RED)
d.polygon([(620,340),(650,295),(680,340)],fill=RED)
wline(d,640,295,700,295,RED,6)
txt(d,"DIPLOMATIC RELATIONS",W//2,420,36,BLACK,center=True)
txt(d,":  SEVERED",W//2,470,40,RED,center=True)
txt(d,"Argentina temporarily broke ties with Uruguay",W//2,580,24,GRAY,center=True)
save(img,"aftermath_diplomatic_severed")

# 89: template for everything
img,d = new_img()
trophy(d,W//2,160,1.2)
wline(d,100,360,W-100,360,BLACK,4)
txt(d,"This tournament created the TEMPLATE",W//2,400,30,BLACK,center=True)
txt(d,"for everything that came after:",W//2,442,28,GRAY,center=True)
items=["The rivalries","The political drama","The moments nobody expects","The global stage"]
for i,item in enumerate(items):
    txt(d,f"✓  {item}",240,490+i*42,26,BLACK if i%2==0 else RED)
save(img,"aftermath_template")

# 90: El Manco portrait
img,d = new_img()
wrect(d,350,80,930,560,BLACK,6,fill=CREAM)
el_manco(d,W//2,280,1.3)
wline(d,380,450,900,450,BLACK,4)
txt(d,"HECTOR CASTRO",W//2,475,32,BLACK,center=True)
txt(d,'"EL MANCO"',W//2,515,28,RED,center=True)
txt(d,"Lost forearm in childhood accident.",W//2,558,22,GRAY,center=True)
txt(d,"Scored the 4th goal. World Champion.",W//2,590,22,GRAY,center=True)
save(img,"aftermath_el_manco_portrait")

# 91: bend bow weave break quote
img,d = new_img()
d.rectangle([0,0,W,H],fill=(20,20,60))
txt(d,'"A nation of under two million',W//2,120,28,WHITE,center=True)
txt(d,"beat the world with a borrowed format,",W//2,170,28,WHITE,center=True)
txt(d,"a disputed ball, and a one-armed striker.",W//2,220,28,WHITE,center=True)
wline(d,200,270,1080,270,GOLD,3)
txt(d,"BEND",280,320,52,RED,center=True)
txt(d,"BOW",560,320,52,YELLOW,center=True)
txt(d,"WEAVE",840,320,52,BLUE,center=True)
txt(d,"BREAK",W//2,400,56,WHITE,center=True)
wline(d,200,460,1080,460,GOLD,3)
txt(d,'"That\'s not a footnote. That\'s the foundation."',W//2,510,28,GOLD,center=True)
save(img,"aftermath_bbwb_quote")

# 92: 1.75 million beat the world
img,d = new_img()
d.rectangle([0,0,W,H],fill=(10,10,40))
txt(d,"1.75 MILLION PEOPLE",W//2,200,56,YELLOW,center=True)
txt(d,"BEAT",W//2,295,100,WHITE,center=True)
txt(d,"THE WORLD",W//2,410,70,RED,center=True)
for a2 in range(0,360,25):
    r2=math.radians(a2); L=100
    wline(d,W//2,H//2+50,W//2+int(L*math.cos(r2)),H//2+50+int(L*math.sin(r2)),GOLD,3)
save(img,"aftermath_175m_beat_world")

# ──────────────────────────────────────────────────────────
# OUTRO [11:15-12:00] — 8 frames
# ──────────────────────────────────────────────────────────
print("OUTRO")

# 93: modern Centenario with 2030 banners
img,d = new_img()
sky_ground(d)
stadium(d,W//2,150,600,350)
for i,col in enumerate([RED,BLUE,YELLOW,RED,BLUE]):
    bx=W//2-240+i*120
    wrect(d,bx,80,bx+90,150,BLACK,3,fill=col)
    txt(d,"2030",bx+8,98,22,WHITE)
    wline(d,bx+45,80,bx+45,155,BLACK,3)
txt(d,"100 YEARS LATER",W//2,570,36,BLACK,center=True)
txt(d,"Same ground. Same ghosts.",W//2,620,28,GRAY,center=True)
save(img,"outro_modern_centenario")

# 94: plaque glinting
img,d = new_img()
d.rectangle([0,0,W,H],fill=LIGHTGRAY)
wrect(d,380,200,900,450,GOLD,6,fill=YELLOW)
txt(d,"1930",W//2,255,90,BLACK,center=True)
txt(d,"FIRST WORLD CUP FINAL",W//2,365,30,BLACK,center=True)
txt(d,"ESTADIO CENTENARIO",W//2,405,26,GRAY,center=True)
for a2 in range(0,360,30):
    r2=math.radians(a2); L=random.randint(40,80)
    wline(d,W//2,325,W//2+int(L*math.cos(r2)),325+int(L*math.sin(r2)),GOLD,5)
save(img,"outro_plaque_glinting")

# 95: narrator with mic
img,d = new_img()
stickman(d,W//2,270,1.2)
wrect(d,W//2+35,310,W//2+55,360,BLACK,3,fill=BLACK)
d.ellipse([W//2+25,285,W//2+65,325],fill=BLACK)
speech(d,W//2+80,140,420,80,'"I\'m Nobody."',28)
txt(d,'"You\'re Nobody."',W//2+80,230,28,BLACK)
txt(d,"Now you know who they were at home.",W//2,580,28,BLACK,center=True)
save(img,"outro_narrator_mic")

# 96: now you know
img,d = new_img()
txt(d,"NOW",W//2,160,110,BLACK,center=True)
txt(d,"YOU KNOW",W//2,290,80,RED,center=True)
txt(d,"who they were at home.",W//2,400,42,GRAY,center=True)
wline(d,150,460,1130,460,BLACK,5)
txt(d,"WAYAH — Episode 02",W//2,510,30,BLACK,center=True)
save(img,"outro_now_you_know")

# 97: WAYAH logo card
img,d = new_img()
d.rectangle([0,0,W,H],fill=BLACK)
txt(d,"WAYAH.",W//2,250,110,YELLOW,center=True)
wline(d,200,400,1080,400,GOLD,4)
txt(d,"An NKN Joint.",W//2,440,36,WHITE,center=True)
txt(d,"Two Balls, One Crown.",W//2,500,28,LIGHTGRAY,center=True)
save(img,"outro_wayah_logo")

# 98: subscribe end card
img,d = new_img()
d.rectangle([0,0,W,H],fill=(20,20,20))
wrect(d,100,80,1180,620,RED,6,fill=RED)
txt(d,"LIKE  •  SUBSCRIBE  •  COMMENT",W//2,230,38,WHITE,center=True)
stickman(d,250,430,1.0,arms="up",color=WHITE)
stickman(d,640,420,1.1,arms="up",color=WHITE)
stickman(d,1020,430,1.0,arms="up",color=WHITE)
txt(d,'"Who wins in 2030?"',W//2,560,32,YELLOW,center=True)
save(img,"outro_end_card")

print(f"\n=== DONE: {FRAME[0]} frames saved to {OUT} ===")
