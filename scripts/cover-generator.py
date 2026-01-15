import argparse
import random
import math

# ==========================
# ARGUMENT PARSING
# ==========================

parser = argparse.ArgumentParser(
    description="Generate SVG cover art for the Open Source Supply Chain book series."
)
parser.add_argument(
    "-b", "--book",
    type=int,
    choices=[1, 2, 3],
    default=3,
    help="Book number: 1=Understanding, 2=Protecting, 3=Governing (default: 3)"
)
parser.add_argument(
    "-s", "--seed",
    type=int,
    default=None,
    help="Random seed for reproducible generation (default: random)"
)
parser.add_argument(
    "-o", "--output",
    type=str,
    default="output.svg",
    help="Output SVG file path (default: output.svg)"
)
parser.add_argument(
    "--no-guides",
    action="store_true",
    help="Disable bleed and spine guide overlays"
)

args = parser.parse_args()

# ==========================
# CONFIGURATION
# ==========================

WIDTH = 4000
HEIGHT = 2250
SEED = args.seed

NODE_COUNT = 300
EDGE_DISTANCE = 260
RISK_RATIO = 0.145

BOOK = args.book
OUTPUT_FILE = args.output
SHOW_GUIDES = not args.no_guides
BLEED = 36            # px (0.125in @ 300dpi)
SPINE_WIDTH = 180     # px (adjust per page count)

if not SEED:
    SEED = random.randint(1, 1000000)
    print(f"Random seed: {SEED}")
else:
    print("Using seed: " + str(SEED))

random.seed(SEED)

# ==========================
# COLOR PALETTES
# ==========================

PALETTES = {
    1: {  # Blue / Cyan
        "bg_left": "#050A18",
        "bg_right": "#071A31",
        "node_fg": "#CFFBFF",
        "node_mid": "#78E7FF",
        "node_bg": "#1E88E5",
        "edge": "#2FB7FF",
        "risk": "#FF6A3D",
    },
    2: {  # Blue / Green
        "bg_left": "#050A18",
        "bg_right": "#063A2B",
        "node_fg": "#B7FFE3",
        "node_mid": "#4DFFB2",
        "node_bg": "#1E8E6E",
        "edge": "#36D399",
        "risk": "#FFC857",
    },
    3: {  # Blue / Purple / Bronze
        "bg_left": "#060916",
        "bg_right": "#2A1F4D",
        "node_fg": "#E6D8FF",
        "node_mid": "#B18CFF",
        "node_bg": "#6A5ACD",
        "edge": "#9F7AEA",
        "risk": "#C9A24D",
    },
}

TITLES = [
    ("UNDERSTANDING THE", "OPEN SOURCE SUPPLY CHAIN", "Threats, Risks, and Attacks", "for the Modern Software Organization"),
    ("PROTECTING THE", "OPEN SOURCE SUPPLY CHAIN", "Practical Security Defenses", "for the Modern Software Organization"),
    ("GOVERNING THE", "OPEN SOURCE SUPPLY CHAIN", "Policy, Compliance, and Leadership", "for the Modern Software Organization"),
]

C = PALETTES[BOOK]
title = TITLES[BOOK - 1]

# ==========================
# HELPERS
# ==========================

def rand_right_weighted():
    location = WIDTH
    while location >= (WIDTH - BLEED - 30):
        location = WIDTH * (0.48 + 0.52 * random.random() ** 0.55)
    return location

def jitter(v):
    return random.uniform(-v, v)

def depth_from_y(y):
    if random.uniform(0, 1) < 0.20:
        return "foreground"
    elif random.uniform(0, 1) < 0.50:
        return "mid"
    else:
        return "background"
    
def distance(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])

# ==========================
# NODE GENERATION
# ==========================

nodes = []
for _ in range(NODE_COUNT):
    x = 0
    while x < WIDTH / 2 + SPINE_WIDTH / 2 + 25:
        x = rand_right_weighted() + jitter(28)

    y = random.uniform(100, HEIGHT - 100) + jitter(22)
    depth = depth_from_y(y)
    is_risk = random.random() < RISK_RATIO
    nodes.append((x, y, depth, is_risk))

# ==========================
# SVG OUTPUT
# ==========================

with open(OUTPUT_FILE, "w") as f:
    f.write(f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg"
     width="{WIDTH}" height="{HEIGHT}"
     viewBox="0 0 {WIDTH} {HEIGHT}">
  <defs>
    <linearGradient id="bg-1" x1="0" y1="0" x2="6000" y2="0" gradientUnits="userSpaceOnUse">
        <stop offset="0" stop-color="#07002b" />
        <stop offset="0.09090909090909091" stop-color="#070028" />
        <stop offset="0.18181818181818182" stop-color="#080025" />
        <stop offset="0.2727272727272727" stop-color="#070021" />
        <stop offset="0.36363636363636365" stop-color="#07001e" />
        <stop offset="0.45454545454545453" stop-color="#06001b" />
        <stop offset="0.5454545454545454" stop-color="#050018" />
        <stop offset="0.6363636363636364" stop-color="#040015" />
        <stop offset="0.7272727272727273" stop-color="#030011" />
        <stop offset="0.8181818181818182" stop-color="#02000c" />
        <stop offset="0.9090909090909091" stop-color="#010006" />
        <stop offset="1" stop-color="#000000" />
    </linearGradient>

    <linearGradient id="bg-2" x1="0" y1="0" x2="6000" y2="0" gradientUnits="userSpaceOnUse">
        <stop offset="0" stop-color="#100000" />
        <stop offset="0.09090909090909091" stop-color="#0f0000" />
        <stop offset="0.18181818181818182" stop-color="#0e0000" />
        <stop offset="0.2727272727272727" stop-color="#0c0000" />
        <stop offset="0.36363636363636365" stop-color="#0b0000" />
        <stop offset="0.45454545454545453" stop-color="#090000" />
        <stop offset="0.5454545454545454" stop-color="#080000" />
        <stop offset="0.6363636363636364" stop-color="#060000" />
        <stop offset="0.7272727272727273" stop-color="#050000" />
        <stop offset="0.8181818181818182" stop-color="#030000" />
        <stop offset="0.9090909090909091" stop-color="#020000" />
    </linearGradient>
    
    <linearGradient id="bg-3" x1="0" y1="0" x2="6000" y2="0" gradientUnits="userSpaceOnUse">
        <stop offset="0" stop-color="#101311" />
        <stop offset="0.09090909090909091" stop-color="#0f1210" />
        <stop offset="0.18181818181818182" stop-color="#0e100f" />
        <stop offset="0.2727272727272727" stop-color="#0c0f0d" />
        <stop offset="0.36363636363636365" stop-color="#0b0d0c" />
        <stop offset="0.45454545454545453" stop-color="#090c0a" />
        <stop offset="0.5454545454545454" stop-color="#080a08" />
        <stop offset="0.6363636363636364" stop-color="#060807" />
        <stop offset="0.7272727272727273" stop-color="#050605" />
        <stop offset="0.8181818181818182" stop-color="#030403" />
        <stop offset="0.9090909090909091" stop-color="#020202" />
        <stop offset="1" stop-color="#000000" />
    </linearGradient>

    <!-- Node Glows -->
    <filter id="glowFG" x="-200%" y="-200%" width="500%" height="500%">
        <feGaussianBlur stdDeviation="15" result="blur" />
        <feFlood flood-color="#FF4B2B" result="color" />
        <feComposite in="color" in2="blur" operator="in" />
        <feMerge>
            <feMergeNode />
            <feMergeNode in="SourceGraphic" />
        </feMerge>
    </filter>

    <filter id="glowMID" x="-200%" y="-200%" width="500%" height="500%">
        <feGaussianBlur stdDeviation="20" result="blur" />
        <feFlood flood-color="#2FB7FF" result="color" />
        <feComposite in="color" in2="blur" operator="in" />
        <feMerge>
            <feMergeNode />
            <feMergeNode in="SourceGraphic" />
        </feMerge>
    </filter>
    
    <filter id="glowBG" x="-200%" y="-200%" width="500%" height="500%">
        <feGaussianBlur stdDeviation="25" result="blur" />
        <feFlood flood-color="#5F5FDA" result="color" />
        <feComposite in="color" in2="blur" operator="in" />
        <feMerge>
            <feMergeNode />
            <feMergeNode in="SourceGraphic" />
        </feMerge>
    </filter>
    
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
        <feGaussianBlur in="SourceAlpha" stdDeviation="2" result="blur"/>
        <feOffset dx="0" dy="2" result="offsetBlur"/>
        <feFlood flood-color="#000000" flood-opacity="0.45"/>
        <feComposite in2="offsetBlur" operator="in"/>
        <feMerge>
            <feMergeNode/>
            <feMergeNode in="SourceGraphic"/>
        </feMerge>
    </filter>

    <!-- Subtle glow for title text -->
    <filter id="titleGlow" x="-30%" y="-30%" width="160%" height="160%">
        <!-- Soft outer glow -->
        <feGaussianBlur stdDeviation="35" result="blur"/>
        <feColorMatrix
            type="matrix"
            values="
                0 0 0 0 0.15
                0 0 0 0 0.20
                0 0 0 0 0.1
                0 0 0 0.25 0"
            result="glowColor" />
        <feMerge>
            <feMergeNode in="glowColor"/>
            <feMergeNode in="SourceGraphic"/>
        </feMerge>
    </filter>
    <radialGradient
       id="radialGradient"
       color-interpolation="sRGB"
       cx="1800"
       cy="1325"
       fx="2000"
       fy="1125"
       r="2000"
       gradientTransform="matrix(1,0,0,0.5625,0,492.1875)"
       gradientUnits="userSpaceOnUse">
      <stop
         style="stop-color:#030323;stop-opacity:1;"
         offset="0" />
      <stop
         style="stop-color:#000000;stop-opacity:1;"
         offset="1" />

    </radialGradient>

    <mask id="authorFadeMask" maskUnits="userSpaceOnUse">
        <rect width="4000" height="2250" fill="white"/>

        <!-- Inner stronger fade -->
        <rect
            x="2680"
            y="2125"
            width="720"
            height="120"
            rx="24"
            ry="24"
            fill="black"
            opacity="0.35"
        />

        <!-- Outer softer fade -->
        <rect
            x="2580"
            y="2075"
            width="920"
            height="220"
            rx="40"
            ry="40"
            fill="black"
            opacity="0.18"
        />


    </mask> 

    <!-- Line Filters -->
    <linearGradient id="separatorGradient" x1="2250" y1="0" x2="3850" y2="0" gradientUnits="userSpaceOnUse">
        <stop offset="0%" stop-color="black" />
        <stop offset="20%" stop-color="white" />
        <stop offset="80%" stop-color="white" />
        <stop offset="100%" stop-color="black" />
    </linearGradient>

    <mask id="separatorMask" maskUnits="userSpaceOnUse">
        <rect x="2250" y="550" width="1600" height="100" fill="url(#separatorGradient)" />
    </mask>

    <filter id="softEdge" x="-50%" y="-200%" width="200%" height="400%">
        <feGaussianBlur stdDeviation="1.3" />
    </filter>
    
    <!-- Title readability mask -->
    <mask id="titleFadeMask" maskUnits="userSpaceOnUse">
    <!-- Default: fully visible -->
    <rect width="4000" height="2250" fill="white"/>

    <!-- Title readability zone -->
    <rect
        x="2460"
        y="180"
        width="1160"
        height="420"
        rx="40"
        ry="40"
        fill="black"
        opacity="0.32"
    />
    </mask>    

    <mask id="combinedFadeMask" maskUnits="userSpaceOnUse">
        <rect width="4000" height="2250" fill="white"/>    

         <!-- Inner stronger fade -->
        <rect
            x="2680"
            y="2125"
            width="720"
            height="120"
            rx="24"
            ry="24"
            fill="black"
            opacity="0.35"
        />

        <!-- Outer softer fade -->
        <rect
            x="2580"
            y="2075"
            width="920"
            height="220"
            rx="40"
            ry="40"
            fill="black"
            opacity="0.18"
        />

        <!-- Title readability zone -->
        <rect
            x="2235"
            y="250"
            width="1610"
            height="300"
            rx="40"
            ry="40"
            fill="black"
            opacity="0.32"
        />
    </mask>
<filter id="dither">
  <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="1" stitchTiles="stitch" />
  <feComponentTransfer>
    <feFuncA type="linear" slope="0.01" /> </feComponentTransfer>
  <feComposite operator="in" in2="SourceGraphic" />
  <feBlend in="SourceGraphic" mode="screen" />
</filter>
  </defs>

  <rect width="{WIDTH}" height="{HEIGHT}"
    style="fill:url(#bg-{BOOK});fill-opacity:1" />

  <g id="network" mask="url(#combinedFadeMask)">
  <!-- EDGES -->
  <g stroke-linecap="round">
''')

    for i, a in enumerate(nodes):
        for j in range(i + 1, len(nodes)):
            b = nodes[j]
            d = distance(a, b)
            if d < EDGE_DISTANCE:
                depth = a[2]
                width = {"foreground": 2.6, "mid": 2.1, "background": 1.6}[depth]
                opacity = max(0.10, 1 - d / EDGE_DISTANCE)

                color = C["risk"] if a[3] or b[3] else C["edge"]
                color = C["edge"]
                if a[3] or b[3]:
                    opacity *= 0.55

                f.write(
                    f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" '
                    f'x2="{b[0]:.1f}" y2="{b[1]:.1f}" '
                    f'stroke="{color}" stroke-width="{width}" '
                    f'stroke-opacity="{opacity:.2f}"/>\n'
                )
    f.write('</g>\n'
            )
    # BACKGROUND NODES
    f.write('<g filter="url(#glowBG)">\n')
    for x, y, d, _ in nodes:
        if d == "background":
            f.write(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="{C["node_bg"]}" fill-opacity="0.28"/>\n')
    f.write('</g>\n')

    # MID NODES
    f.write('<g filter="url(#glowMID)">\n')
    for x, y, d, _ in nodes:
        if d == "mid":
            f.write(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="9" fill="{C["node_mid"]}" fill-opacity="0.75"/>\n')
    f.write('</g>\n')

    # FOREGROUND NODES
    f.write('<g filter="url(#glowFG)">\n')
    for x, y, d, is_risk in nodes:
        if d == "foreground":
            r = 13 if not is_risk else 11
            color = C["risk"] if is_risk else C["node_fg"]
            f.write(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{color}" fill-opacity="0.95"/>\n')
    f.write('</g>\n')
    f.write('</g>\n')

    # TITLE TEXT
    f.write(f'''
        <!-- Title/Author overlay -->
        <g id="coverTypography" filter="url(#softShadow)">

        <!-- Title line 1 -->
        <text
            x="76%"
            y="15.8%"
            text-anchor="middle"
            font-family="Libertinus Sans"
            font-size="90"
            font-weight="600"
            letter-spacing="1.4"
            fill="#FFFFFF"
            opacity="1.0"
            style="
                paint-order: stroke fill;
                stroke: #000000;
                stroke-width: 2;
                stroke-opacity: 0.45;
            "
            filter="url(#titleGlow)"
        >{title[0]}</text>

        <!-- Title line 2 -->
        <g transform="translate(0, -30) scale(1, 1.09)">
            <text
                x="76%"
                y="22.4%"
                text-anchor="middle"
                font-family="Libertinus Sans"
                font-size="122"
                font-weight="700"
                letter-spacing="0.8"
                fill="#7BD8F3"
                opacity="1"
                style="
                    paint-order: stroke fill;
                    stroke: #000000;
                    stroke-width: 2.2;
                    stroke-opacity: 0.45;
                "
                filter="url(#titleGlow)"
            >{title[1]}</text>
        </g>

        <!-- Title line 3 -->
        <text
            x="76%"
            y="33.9%"
            text-anchor="middle"
            font-family="Libertinus Sans"
            font-size="75"
            font-weight="500"
            letter-spacing="1.2"
            fill="#fff"
            opacity="1"
            style="
                paint-order: stroke fill;
                stroke: #000000;
                stroke-width: 2;
                stroke-opacity: 0.45;
            "
            filter="url(#titleGlow)"
        >{title[2]}</text>
        
        <!-- Title line 3 -->
        <text
            x="76%"
            y="38.0%"
            text-anchor="middle"
            font-family="Libertinus Sans"
            font-size="75"
            font-weight="500"
            letter-spacing="1.2"
            fill="#fff"
            opacity="1.0"
            style="
                paint-order: stroke fill;
                stroke: #000000;
                stroke-width: 2;
                stroke-opacity: 0.45;
            "
            filter="url(#titleGlow)"
        >{title[3]}</text>

        <!-- Author (bottom) -->
        <text
            x="76%"
            y="95%"
            text-anchor="middle"
            font-family="Libertinus Sans"
            font-size="64"
            font-weight="700"
            letter-spacing="2.2"
            fill="#C4C01D"
            opacity="1"
            style="
                paint-order: stroke fill;
                stroke: #000000;
                stroke-width: 2.2;
                stroke-opacity: 0.7;
            "    
        >MICHAEL V. SCOVETTA</text>

        <rect
            x="2250"
            y="575"
            width="1600"
            height="3"
            fill="#666"
            fill-opacity="0.65"
            mask="url(#separatorMask)"
            filter="url(#softEdge)"
        />

        </g>


    ''')

    # GUIDES
    if SHOW_GUIDES:
        f.write(f'''
  <!-- BLEED -->
  <rect x="{BLEED}" y="{BLEED}"
        width="{WIDTH - 2*BLEED}" height="{HEIGHT - 2*BLEED}"
        fill="none" stroke="#FFFFFF" stroke-opacity="0.15"
        stroke-dasharray="16 12"/>

  <!-- SPINE -->
  <rect x="{WIDTH/2 - SPINE_WIDTH/2}" y="0"
        width="{SPINE_WIDTH}" height="{HEIGHT}"
        fill="none" stroke="#FFAA00" stroke-opacity="0.25"
        stroke-dasharray="20 12"/>
''')

    f.write('</svg>')

print(f"Generated: {OUTPUT_FILE}")
