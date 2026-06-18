#!/bin/bash
# WAYAH Ep.02 — Full Stop-Motion Frame Generation via Higgsfield
# ~123 frames across 12 minutes for stop-motion animation style
# Run after: higgsfield auth login

set -e
OUT="./wayah_higgsfield_frames"
mkdir -p "$OUT"

MODEL="gpt_image_2"
STYLE="MS Paint style beginner drawing, white background, thick wobbly black outlines, stick figure humans with round heads, simple dot eyes, flat colors only, no shading, no 3D, no realistic art, childish amateur drawing, hand-drawn look, simple shapes and symbols, 16:9 wide frame"

run() {
  local num="$1"
  local label="$2"
  local prompt="$3"
  local outfile="$OUT/frame_$(printf '%03d' $num)_${label}.png"
  echo ">>> Generating frame $num: $label"
  higgsfield generate create "$MODEL" \
    --prompt "$STYLE. $prompt" \
    --aspect_ratio 16:9 \
    --wait \
    --json | python3 -c "
import sys, json, urllib.request, os
data = json.load(sys.stdin)
jobs = data if isinstance(data, list) else [data]
for j in jobs:
    urls = j.get('result_urls') or j.get('urls') or []
    if urls:
        url = urls[0]
        urllib.request.urlretrieve(url, '$outfile')
        print('Saved: $outfile')
        break
    else:
        print('No URL in response:', json.dumps(j)[:300])
"
}

# ─────────────────────────────────────────────────────────────────────
# COLD OPEN [00:00–00:30] — 8 frames
# ─────────────────────────────────────────────────────────────────────
run 1  "stadium_far"         "Simple stick-drawing of a stadium silhouette on the horizon. Green ground, blue sky. Very small building in distance with two stick towers."
run 2  "stadium_closer"      "Simple stick-drawing of Estadio Centenario up close. Big rectangle with arch roof. Simple brick lines on walls. Uruguay flag on top. Blue sky."
run 3  "stickman_walking"    "One stick figure walking toward a simple rectangle stadium building. Motion lines behind the stickman. Green ground."
run 4  "stickman_looks_up"   "Stick figure standing next to a tall stadium wall, looking up with open mouth. Small 'WOW' in speech bubble. Very simple."
run 5  "plaque_on_wall"      "Close-up of a simple yellow rectangle plaque on a gray wall. The plaque has the number 1930 written on it in big black letters. A small stick hand pointing at it."
run 6  "stickman_points_plaque" "Stick figure pointing at a yellow plaque on a wall. Plaque says 1930. Stickman looks excited with big smile."
run 7  "title_wayah"         "White background. Big bold hand-drawn wobbly letters spelling WAYAH in the center. Below it in smaller letters: Two Balls, One Crown."
run 8  "subtitle_card"       "White background. Simple text drawn in thick black marker style: Episode 02. Below: Uruguay vs Argentina. Below: 1930. Very simple layout."

# ─────────────────────────────────────────────────────────────────────
# THE HOOK [00:30–01:20] — 12 frames
# ─────────────────────────────────────────────────────────────────────
run 9  "old_tv_stadium"      "Simple drawing of a boxy old television set with antenna. On the screen is a tiny stick drawing of a stadium. The TV looks old and wobbly drawn."
run 10 "two_eras_banner"     "Screen split in half. Left side: yellow tinted background with text 1930 and tiny simple stadium. Right side: bright background with text 2030 and a banner. Simple dividing line."
run 11 "two_stickmen_argue"  "Two stick figures facing each other with angry faces. Left stickman has speech bubble saying MESSI! Right stickman has speech bubble saying PELE! Big question mark above both."
run 12 "globe_arrow_uruguay" "Simple round circle representing Earth with crude land shapes drawn on it. A big red arrow pointing to a small spot labeled URUGUAY. Very childish map drawing."
run 13 "100_years_timeline"  "Simple horizontal line across the page. Left end labeled 1930 with a tiny trophy. Right end labeled 2030 with a star. Arrow pointing right. Text: 100 YEARS."
run 14 "crowd_waving_flags"  "Many small stick figures in a row. Each holding a simple colored rectangle flag. Some flags are red and white, some blue and white. All stickmen have happy faces."
run 15 "two_rivals_faceoff"  "Two large stick figures facing each other nose to nose. One wearing blue and white stripes (Argentina). One wearing light blue (Uruguay). Both look angry. Red lightning bolt between them."
run 16 "first_final_card"    "White background. Simple hand-drawn box with text inside: THE FIRST WORLD CUP FINAL EVER. Below: July 30 1930. Wobbly lettering. Red border around the box."
run 17 "zero_love_lost"      "Two stick figures with arms crossed, turned away from each other. A river squiggle between them labeled RIVER PLATE. Big red heart with X through it above them."
run 18 "vuvuzela_stickman"   "Stick figure blowing a long horn (vuvuzela). Musical notes coming out of the horn. Simple crowd of tiny stick figures behind. Big stadium shape in background."
run 19 "energy_explosion"    "Simple starburst explosion shape in center of page. Text in the middle: GAME ON. Colorful simple lines shooting outward. Red yellow and blue colors."
run 20 "narrator_intro"      "Stick figure standing at a podium with a microphone. Speech bubble says: Before any of that. Background is just white with simple lines."

# ─────────────────────────────────────────────────────────────────────
# CHAPTER 1 — THE SETUP [01:20–04:30] — 35 frames
# ─────────────────────────────────────────────────────────────────────
run 21 "world_map_flags"     "Simple wobbly map of the world. Little colored rectangle flags placed on different countries. Text above: 41 INVITED. Very crude map shapes."
run 22 "big_red_x_flags"     "Same crude world map but with a huge red X drawn over most of the flags. Only a few small flags remain circled in green. Text: MOST SAID NO."
run 23 "only_13_showed"      "White background. Text: ONLY 13 SHOWED UP. Below: 13 tiny stick figures standing in a row looking small and lonely. Simple."
run 24 "ocean_boat_far"      "Simple drawing of blue wavy ocean. A tiny boat far in the distance. Big blue sky above. Lots of empty ocean space to show the distance."
run 25 "stickman_seasick"    "Stick figure on a simple boat, leaning over the side looking green and dizzy. Wavy lines around the boat. Squiggly lines to show sickness. Speech bubble: UGHHH."
run 26 "calendar_16_days"    "Simple drawing of a calendar page. Big number 16 on it. Below: DAYS ON A BOAT. Simple ship icon next to it. Red marks crossing out each day."
run 27 "stickman_empty_wallet" "Stick figure holding open an empty wallet upside down. Nothing falling out. Sad face. Speech bubble: NO MONEY. Simple dollar sign with X through it."
run 28 "stickman_job_worry"  "Stick figure standing outside a simple rectangle building labeled JOB. Stickman has worried face. Speech bubble: But my job tho. Factory chimney on building."
run 29 "boat_route_map"      "Crude world map. A dotted line with arrow going from Europe blob to South America blob. Small boat icon on the dotted line. Text: 16 DAYS."
run 30 "boat_getting_closer" "Simple ocean scene. Boat slightly bigger and closer than before. Stick figure on boat waving. Land visible on horizon as a green stripe."
run 31 "boat_arriving_dock"  "Simple boat tied to a dock made of rectangles. Stick figure walking off a gangplank. Sign on dock: MONTEVIDEO. Happy faces."
run 32 "france_stickman"     "Stick figure with French flag colors on shirt (blue white red stripes). Small France flag next to them. Carrying a suitcase. Simple boarding dock in background."
run 33 "belgium_stickman"    "Stick figure with Belgian flag colors (black yellow red). Small Belgium flag. Carrying a bag. Standing on a boat deck."
run 34 "romania_stickman"    "Stick figure with Romanian flag colors (blue yellow red). Small Romania flag. Waving. On a simple boat."
run 35 "yugoslavia_stickman" "Stick figure with Yugoslav flag colors (blue white red). Small flag. Also on the boat waving. Simple drawing."
run 36 "four_flags_on_boat"  "Simple boat shape. Four stick figures standing on deck. Each has a different colored flag: France blue white red, Belgium black yellow red, Romania blue yellow red, Yugoslavia blue white red."
run 37 "uruguay_pays_sign"   "Stick figure holding a big sign that says: WE WILL PAY YOUR TRIP! Next to a Uruguay flag (blue stripes with sun). Stickman smiling and pointing at the sign."
run 38 "stickman_gives_money" "Stick figure handing stacks of rectangle money to another stick figure. Money has dollar signs on it. Both smiling. Simple."
run 39 "trophy_on_pedestal"  "Simple drawing of a trophy (cup shape) sitting on a box pedestal. Big question mark above the trophy. Text below: NO ONE HAS EVER LIFTED THIS. White background."
run 40 "question_mark_trophy" "Close-up of the same trophy with an even bigger red question mark above it. Trophy has a small soccer ball symbol drawn on it."
run 41 "stadium_being_built" "Simple rectangle stadium shape with stick figures on scaffolding (just ladder shapes). Some walls not finished yet. Stickmen carry bricks (small rectangles). Text: BUILDING THE CENTENARIO."
run 42 "stadium_finished_flag" "Completed simple rectangle stadium with arch. Uruguay flag on top. Text: ESTADIO CENTENARIO. Green field inside. Blue sky."
run 43 "olympic_medal_1924"  "Simple circle medal shape, gold colored, with the number 1924 on it. A ribbon above it. Text: OLYMPIC GOLD. Very simple drawing."
run 44 "olympic_medal_1928"  "Same style medal with 1928 on it. Gold circle. Ribbon above. Text: OLYMPIC GOLD AGAIN. Two gold stars around it."
run 45 "both_medals"         "Two gold circle medals side by side. 1924 on left, 1928 on right. Ribbon on each. Big text above: BACK TO BACK. Happy face between them."
run 46 "100_years_independence" "Simple calendar or banner shape. Text: 1930. Below: 100 YEARS OF INDEPENDENCE. Simple firework starburst next to it. Uruguay flag colors."
run 47 "party_hat_uruguay"   "Uruguay flag (blue stripes with yellow sun circle) but the sun is wearing a simple party hat. Text: PARTY TIME. Streamers drawn around it."
run 48 "fifa_logo_wobbly"    "White background. The letters FIFA written in big wobbly hand-drawn style. Below: 41 MEMBERS. Simple. Looks like a child wrote it."
run 49 "small_country_map"   "Very simple outline of South America. Uruguay is a tiny blob on the coast, colored in. Text pointing to it: 1.75 MILLION PEOPLE. Arrow showing it is smaller than nearby blobs."
run 50 "tiny_vs_big"         "Left side: tiny stick figure labeled URUGUAY 1.75M. Right side: many stick figures labeled THE WORLD. Simple size comparison. Tiny vs huge."
run 51 "house_of_cards"      "Simple drawing of playing cards (rectangles) stacked in a wobbly house shape. It looks like it is about to fall. Text: ALMOST FELL APART. Red arrow pointing at the shaky top."
run 52 "ball_on_ground"      "White background. Just a simple black and white soccer ball (circle with pentagon patches drawn on it) sitting on green ground. Text: BEFORE A SINGLE BALL WAS KICKED. Nothing else."
run 53 "stickman_kicks_ball" "Stick figure with one leg extended kicking a simple soccer ball. Ball has motion lines. Simple green ground. Sky background."
run 54 "crowd_arrives"       "Many small stick figures walking toward a simple stadium shape in background. Arrow pointing toward stadium. Smiling faces on the stickmen."
run 55 "party_house_guests"  "Simple house shape. Inside: a few lonely stick figures at a party table. Outside: many more stickmen not coming in. Text above: THE BIGGEST PARTY HALF THE GUESTS SKIPPED."

# ─────────────────────────────────────────────────────────────────────
# CHAPTER 2 — WHO ARE THEY AT HOME [04:30–06:30] — 20 frames
# ─────────────────────────────────────────────────────────────────────
run 56 "river_splits_map"    "Simple top-down map drawing. A wavy blue river line splits the screen in half. Left side says URUGUAY. Right side says ARGENTINA. Very simple crude map."
run 57 "population_compare"  "Left: 3 stick figures labeled URUGUAY 1.75M. Right: many more stick figures labeled ARGENTINA BIGGER. Simple size comparison drawing."
run 58 "two_gold_medals"     "Uruguay stick figure holding two gold circle medals up high. Happy face. Text: 1924 + 1928 OLYMPIC GOLD. Simple."
run 59 "argentina_hungry"    "Argentina stick figure with angry/hungry face. Big open mouth. Text next to them: HUNGRY. Red background on right side. Aggressive pose."
run 60 "stabile_big_boot"    "Stick figure with one comically oversized boot/foot. Text next to them: STABILE. Below: TOP SCORER. Arrow pointing to the big foot. Simple."
run 61 "golden_boot_trophy"  "Simple boot shape colored gold. Text: GUILLERMO STABILE. Below: LEADING SCORER. Trophy star above it. Childish drawing."
run 62 "1928_olympic_final"  "Simple soccer pitch rectangle. URU stick figures on left side, ARG stick figures on right side. Text: 1928 OLYMPIC FINAL AMSTERDAM. Simple."
run 63 "scoreboard_1928"     "Simple scoreboard rectangle shape. URU: 2  ARG: 1. Below: AFTER REPLAY. Text: AMSTERDAM 1928. Wobbly drawn."
run 64 "argentina_angry_face" "Close-up of a stick figure face. Very angry expression. Downturned thick eyebrows. Frowning mouth. Red cheeks. Text: NOT HAPPY. ARG flag color background."
run 65 "shaking_fists_river" "Two stick figures on opposite sides of a wavy blue river. Both shaking fists at each other. Speech bubbles with angry scribbles. Simple."
run 66 "rematch_speech"      "Two stick figures. One has speech bubble: REMATCH! Other has speech bubble: BRING IT! Red lightning bolt between them. Simple."
run 67 "globe_spotlight"     "Simple circle globe. A yellow spotlight cone pointing down at the South America section. Text: THE WHOLE WORLD WATCHING. Star burst light effect."
run 68 "same_language_sign"  "White background. Simple sign or banner. Text: Same language. Same river. Different feelings. Red arrow pointing down. Stick figure scratching head."
run 69 "newspaper_rivals"    "Simple rectangle newspaper shape. Headline in wobbly letters: RIVALS MEET AGAIN. Small soccer ball icon. Stickman reading it with wide eyes."
run 70 "crowd_dots_stadium"  "Simple rectangle stadium shape. Inside the stands: hundreds of tiny dots representing people. Field is green. Very packed looking. Text: PACKED."
run 71 "two_flags_side"      "Two flags side by side. Left: Uruguay flag (blue stripes and yellow sun). Right: Argentina flag (light blue and white stripes with sun). Both drawn simply."
run 72 "world_is_watching"   "Many tiny stick figures arranged in a circle looking inward at a soccer ball in the center. Text: THE WORLD IS WATCHING. Simple composition."
run 73 "calendar_july30"     "Simple calendar page. Month written: JULY. Date circled in red: 30. Year: 1930. Red circle with exclamation mark. Text: MATCH DAY."
run 74 "stadium_gates_open"  "Simple drawing of two big rectangle gates swinging open. People (dots) flowing through. Text: GATES OPEN. Green grass visible inside."
run 75 "referee_whistle"     "Stick figure in black and white striped shirt. Blowing a whistle (small circle to mouth). Arm raised. Text: LET'S GO. Simple."

# ─────────────────────────────────────────────────────────────────────
# CHAPTER 3 — THE MATCH [06:30–09:45] — 30 frames
# ─────────────────────────────────────────────────────────────────────
run 76 "two_teams_lineup"    "Two rows of stick figures facing each other on a simple green rectangle pitch. Left row labeled URU in blue. Right row labeled ARG in light blue and white stripes. Simple."
run 77 "referee_coin_toss"   "Referee stick figure tossing a coin in the air. Two other stick figures watching. Simple coin with shine lines. Text: COIN TOSS."
run 78 "argentina_ball"      "Close-up of a simple soccer ball (black and white pentagon patches). Label next to it with arrow: ARG BALL (1ST HALF). Text below: They argued about the ball."
run 79 "arguing_over_balls"  "Two stick figures arguing. One pulling a ball one way, other pulling a different ball the other way. Angry speech scribbles in bubbles. Text: WHOSE BALL?!"
run 80 "two_balls_labeled"   "Two soccer balls drawn side by side. Left ball: ARG BALL - 1st HALF. Right ball: URU BALL - 2nd HALF. Simple arrow between them. Text: THEY COMPROMISED."
run 81 "kickoff_moment"      "Stick figure kicking a soccer ball in center of green rectangle field. Other stick figures around. Clock in corner shows 0:00. Text: KICKOFF."
run 82 "dorado_scores"       "Stick figure shooting. Ball going into a simple net (rectangle with lines). Big text: GOAL! 1-0 URU! Clock shows 12. Text: DORADO!"
run 83 "uruguay_celebrates"  "Three stick figures with arms raised up celebrating. Jumping. Confetti dots around them. Text: 1-0 URUGUAY! Happy faces."
run 84 "peucelle_runs"       "Stick figure with ARG label running with a soccer ball. Speed lines behind. Text: PEUCELLE. Simple green field background."
run 85 "argentina_equalizes" "Ball going into net. Scoreboard: URU 1 - ARG 1. Text: EQUALIZER! ARG stick figures celebrating with arms up."
run 86 "stabile_shoots"      "Stick figure labeled STABILE with a very big foot kicking hard. Ball flying fast with speed lines. Text: TOP SCORER STRIKES."
run 87 "halftime_21_arg"     "Simple scoreboard rectangle. ARG 2 - URU 1. Text: HALFTIME. Arrow pointing to ARG side. Little ARG stickman doing thumbs up."
run 88 "halftime_huddle_uru" "5 URU stick figures in a circle huddle on simple green field. One stickman in center pointing. Speech bubble: WE CAN DO THIS. Text: HALFTIME."
run 89 "second_half_kickoff" "Center of simple green field. Ball in center circle (just a circle). Text: 2ND HALF. Clock reset to 45 min. Two stick figures running toward ball."
run 90 "cea_equalizes"       "Stick figure labeled CEA shooting. Ball in net. Scoreboard showing URU 2 - ARG 2. Text: CEA LEVELS IT! Celebration arms."
run 91 "iriarte_scores_68"   "Stick figure shooting. Ball in net. Big scoreboard: URU 3 - ARG 2. Clock shows 68. Text: IRIARTE! URU IN FRONT!"
run 92 "stadium_erupts"      "Simple rectangle stadium shape. Wavy excited lines all around it. Dots flying everywhere. Text: THE STADIUM ERUPTS. Simple energy lines."
run 93 "el_manco_runs"       "Stick figure running with only ONE arm visible (the other arm is missing, just a short stub). Simple speed lines. Text: EL MANCO. Text: ONE ARM."
run 94 "el_manco_shoots"     "One-armed stick figure with leg extended kicking ball. Very simple. Ball flying toward simple rectangle net. Text: CASTRO SHOOTS!"
run 95 "ball_hits_net_42"    "Simple net drawing. Ball inside net. Big text: 4-2 URUGUAY!!!. Exclamation marks all over. Simple starbursts."
run 96 "el_manco_celebrates" "One-armed stick figure with single arm raised as high as possible. Other side is just a small stub. Big happy smile. Text: EL MANCO SCORES!"
run 97 "final_whistle"       "Referee stick figure with arm up high and whistle at mouth. Both arms of other stick figures raised. Text: FULL TIME! Simple."
run 98 "final_scoreboard"    "Big simple scoreboard rectangle. URUGUAY: 4 in large numbers. ARGENTINA: 2 in large numbers. Text: WORLD CHAMPIONS. Star above."
run 99 "players_on_ground"   "Several stick figures on green field. Some collapsed in joy, some in sadness. Simple happy and sad faces. Text: JULY 30 1930."
run 100 "trophy_lifted"      "Stick figure holding simple cup trophy above head with both arms. Trophy shining with star lines around it. Text: WORLD CHAMPIONS 1930. Simple."

# ─────────────────────────────────────────────────────────────────────
# CHAPTER 4 — AFTERMATH [09:45–11:15] — 15 frames
# ─────────────────────────────────────────────────────────────────────
run 101 "uruguay_newspaper"  "Simple rectangle newspaper shape. Big wobbly headline: CAMPEONES! Below: smaller text: URUGUAY WINS FIRST WORLD CUP. Stick figure holding paper with huge smile."
run 102 "stickmen_dancing"   "Four stick figures dancing in a row on a simple street. Arms waving. Music notes floating above them. Text: NATIONAL CELEBRATION."
run 103 "holiday_calendar"   "Simple calendar page. July 31 circled in red. Big green star on that date. Text: NATIONAL HOLIDAY! Below: Uruguay celebrates."
run 104 "fireworks"          "Dark blue background. Simple starburst firework shapes in red yellow green blue white. Lines shooting outward from center points. Text: FIESTA!"
run 105 "argentina_newspaper" "Simple newspaper shape. Headline: ESCANDALO! Below: Smaller text: ARGENTINA NOT HAPPY. Stick figure reading with angry face and steam lines from head."
run 106 "angry_mob_stickmen" "Many stick figures marching together. Angry faces. Some holding signs (rectangles on sticks). Arrow pointing direction of march. Text: ANGRY MOB."
run 107 "consulate_building" "Simple rectangle building with columns drawn as vertical lines. Sign on front: URUGUAYAN CONSULATE. Two windows. Simple door. Looks official but drawn badly."
run 108 "broken_window"      "Same simple building but one window has an X through it to show broken. Simple crack lines. Red arrow pointing at window. Text: MOB ATTACKS CONSULATE."
run 109 "diplomat_with_suitcase" "Stick figure in simple suit (rectangle body, tie drawn as triangle) carrying a suitcase. Walking away from a building. Text: ARGENTINA SEVERS TIES. Sad face."
run 110 "diplomatic_severed" "White background. Simple two flag icons side by side with a big scissors cutting the line between them. Text: DIPLOMATIC RELATIONS: SEVERED. Red X between flags."
run 111 "world_map_x_line"   "Simple world map. Dotted line between South America showing URU and ARG. Big red X across the dotted line. Text: TIES CUT."
run 112 "template_trophy"    "Simple trophy on a box. Text: THIS CHANGED EVERYTHING. Arrow pointing to trophy. Below: Created the template for all World Cups. Simple."
run 113 "world_cup_timeline" "Horizontal arrow timeline. 1930 with small star at left. Several dots along the line with years. Present day star at right. Text: THE TEMPLATE."
run 114 "el_manco_portrait"  "Simple stick figure portrait in a rectangle frame. ONE arm visible, one side is a stub. Text below frame: HECTOR CASTRO. Below that: EL MANCO. Below: ONE-ARMED STRIKER."
run 115 "175_million_text"   "White background. Big text: 1.75 MILLION PEOPLE. Below: BEAT THE WORLD. Simple trophy icon. Star burst around the text. Powerful simple layout."

# ─────────────────────────────────────────────────────────────────────
# OUTRO [11:15–12:00] — 8 frames
# ─────────────────────────────────────────────────────────────────────
run 116 "modern_centenario"  "Simple stick-drawing of stadium from outside. Looks similar to opening but now with modern details: 2030 banner flag on side. Same white background and blue sky."
run 117 "2030_banners"       "Simple stadium front view. Several colorful rectangle banners hanging. Each says 2030 in simple text. Confetti dots around. Text: 100 YEARS LATER."
run 118 "plaque_glinting"    "Simple yellow rectangle plaque on gray wall. Star shine lines around it showing it glints. Text on plaque: 1930. Yellow sunburst around plaque edges."
run 119 "narrator_with_mic"  "Stick figure holding a simple microphone (circle on stick). Looking at viewer. Simple background. Text: I AM NOBODY. YOU ARE NOBODY."
run 120 "nobody_speech"      "Stick figure with speech bubble. Inside bubble: Now you know who they were at home. Simple white background. Narrator pose."
run 121 "now_you_know"       "White background. Large hand-drawn text: NOW YOU KNOW. Below: WHO THEY WERE AT HOME. Simple underline. Red accent line."
run 122 "wayah_logo_card"    "Black background. Big yellow wobbly letters: WAYAH. Below in smaller white text: An NKN Joint. Simple dot star accents around it."
run 123 "end_card"           "Black background. White text: SUBSCRIBE. Below: LIKE. Below: COMMENT. Three simple stick hands pointing to each word. Very simple end card."

echo ""
echo "=== ALL 123 FRAMES GENERATED ==="
echo "Saved to: $OUT"
ls "$OUT" | wc -l
