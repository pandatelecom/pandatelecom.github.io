#!/usr/bin/env python3
"""Generate category-specific SVG placeholders for Panda Telecom products."""

import json, os

BRAND_COLORS = {
    'Momax': '#e91e63',
    'ARGO': '#2196F3',
    'Sincos': '#FF9800',
    'SMARTCOBY': '#00BCD4',
    'Ismartdigi': '#4CAF50',
    '10Denki': '#9C27B0',
    'Rhythm': '#00BCD4',
    'Heal Force': '#009688',
    'MOTOROLA': '#3F51B5',
    'Lonzuer': '#FF5722',
    'CREATIVE': '#607D8B',
    'YOHOME': '#795548',
    'IPEAK': '#8BC34A',
}

def brand_color(brand):
    return BRAND_COLORS.get(brand, '#666666')

# Category -> (shape_svg, label)
# Each shape_svg is an inline SVG group centered at (200, 155) scaled to fit 120x120 area
SHAPES = {}

# Charger shape - brick with lightning bolt
SHAPES['充電器'] = '''<g transform="translate(200,155)" fill="COLOR" opacity="0.8">
<rect x="-35" y="-50" width="70" height="90" rx="8" fill="none" stroke="COLOR" stroke-width="3.5"/>
<rect x="-12" y="-62" width="24" height="12" rx="3" fill="COLOR"/>
<rect x="-25" y="-30" width="50" height="20" rx="4" fill="COLOR" opacity="0.2"/>
<polygon points="-6,-12 0,-24 4,-18 10,-28 14,-18 8,-12" fill="COLOR"/>
</g>'''

SHAPES['旅行充電器'] = SHAPES['充電器']

# Powerbank - rectangle with USB ports
SHAPES['行動電源'] = '''<g transform="translate(200,155)" fill="COLOR" opacity="0.8">
<rect x="-45" y="-35" width="90" height="60" rx="10" fill="none" stroke="COLOR" stroke-width="3.5"/>
<rect x="-38" y="-25" width="16" height="10" rx="3" fill="COLOR" opacity="0.3"/>
<rect x="-18" y="-25" width="16" height="10" rx="3" fill="COLOR" opacity="0.3"/>
<rect x="2" y="-25" width="16" height="10" rx="3" fill="COLOR" opacity="0.3"/>
<circle cx="30" cy="-20" r="3" fill="COLOR" opacity="0.5"/>
<circle cx="30" cy="-12" r="3" fill="COLOR" opacity="0.5"/>
<circle cx="30" cy="-4" r="3" fill="COLOR" opacity="0.5"/>
</g>'''

SHAPES['流動電源'] = SHAPES['行動電源']

# Cable shape
SHAPES['充電線'] = '''<g transform="translate(200,155)" fill="COLOR" opacity="0.8">
<rect x="42" y="-30" width="18" height="14" rx="3" fill="COLOR"/>
<path d="M51,-16 C51,10 35,25 20,5 C5,-15 -15,-5 -30,15 C-40,30 -50,25 -48,15" fill="none" stroke="COLOR" stroke-width="4" stroke-linecap="round"/>
<rect x="-60" y="8" width="20" height="16" rx="3" fill="COLOR"/>
</g>'''

# Earbud/headphone
SHAPES['耳機'] = '''<g transform="translate(200,155)" fill="COLOR" opacity="0.8">
<path d="M160,155 A45,50 0 0,1 240,155" fill="none" stroke="COLOR" stroke-width="5"/>
<rect x="150" y="135" width="22" height="30" rx="10" fill="COLOR" opacity="0.2" stroke="COLOR" stroke-width="3"/>
<rect x="228" y="135" width="22" height="30" rx="10" fill="COLOR" opacity="0.2" stroke="COLOR" stroke-width="3"/>
</g>'''

SHAPES['耳機 / 音響'] = SHAPES['耳機']

# Speaker
SHAPES['喇叭'] = '''<g transform="translate(200,155)" fill="COLOR" opacity="0.8">
<rect x="-45" y="-50" width="90" height="95" rx="12" fill="none" stroke="COLOR" stroke-width="3.5"/>
<circle cx="0" cy="-10" r="25" fill="COLOR" opacity="0.15" stroke="COLOR" stroke-width="2"/>
<circle cx="0" cy="-10" r="8" fill="COLOR" opacity="0.3"/>
<circle cx="0" cy="-10" r="3" fill="COLOR"/>
</g>'''

# Car charger
SHAPES['車充'] = '''<g transform="translate(200,155)" fill="COLOR" opacity="0.8">
<rect x="-18" y="35" width="36" height="20" rx="5" fill="COLOR" opacity="0.2" stroke="COLOR" stroke-width="2.5"/>
<rect x="-14" y="-40" width="28" height="60" rx="6" fill="COLOR" opacity="0.15" stroke="COLOR" stroke-width="2.5"/>
<circle cx="0" cy="-20" r="5" fill="COLOR"/>
<rect x="-8" y="10" width="16" height="15" rx="3" fill="COLOR" opacity="0.3"/>
<polygon points="-5,-55 0,-65 5,-55" fill="COLOR"/>
</g>'''

SHAPES['車載支架'] = SHAPES['車充']

# Fan
SHAPES['風扇'] = '''<g transform="translate(200,155)" fill="COLOR" opacity="0.8">
<circle cx="0" cy="0" r="40" fill="none" stroke="COLOR" stroke-width="3"/>
<path d="M0,0 C-10,-35 -30,-40 -25,-20 C-20,0 -10,10 0,0" fill="COLOR" opacity="0.3" stroke="COLOR" stroke-width="2"/>
<path d="M0,0 C35,-10 40,-30 20,-25 C0,-20 -10,-10 0,0" fill="COLOR" opacity="0.3" stroke="COLOR" stroke-width="2"/>
<path d="M0,0 C10,35 30,40 25,20 C20,0 10,-10 0,0" fill="COLOR" opacity="0.3" stroke="COLOR" stroke-width="2"/>
<circle cx="0" cy="0" r="6" fill="COLOR"/>
</g>'''

SHAPES['風扇 / 冷風'] = SHAPES['風扇']

# Home
SHAPES['家居'] = '''<g transform="translate(200,155)" fill="COLOR" opacity="0.8">
<polygon points="0,-55 -55,10 55,10" fill="none" stroke="COLOR" stroke-width="3.5"/>
<rect x="-30" y="10" width="60" height="50" fill="COLOR" opacity="0.1" stroke="COLOR" stroke-width="2.5"/>
<rect x="-5" y="30" width="25" height="30" rx="2" fill="COLOR" opacity="0.2"/>
</g>'''

SHAPES['家電'] = SHAPES['家居']

# Gift/star for 卡通精品
SHAPES['卡通精品'] = '''<g transform="translate(200,155)" fill="COLOR" opacity="0.8">
<polygon points="0,-55 12,-18 52,-18 20,5 32,42 0,22 -32,42 -20,5 -52,-18 -12,-18" fill="COLOR" opacity="0.25" stroke="COLOR" stroke-width="2.5"/>
</g>'''

# Gear/tool for 配件/其他
SHAPES['配件'] = '''<g transform="translate(200,155)" fill="COLOR" opacity="0.8">
<circle cx="0" cy="0" r="22" fill="none" stroke="COLOR" stroke-width="3"/>
<circle cx="0" cy="0" r="10" fill="COLOR" opacity="0.2"/>
<rect x="-4" y="-48" width="8" height="18" rx="3" fill="COLOR" opacity="0.3"/>
<rect x="-4" y="30" width="8" height="18" rx="3" fill="COLOR" opacity="0.3"/>
<rect x="-48" y="-4" width="18" height="8" rx="3" fill="COLOR" opacity="0.3"/>
<rect x="30" y="-4" width="18" height="8" rx="3" fill="COLOR" opacity="0.3"/>
<rect x="-34" y="-34" width="16" height="8" rx="3" fill="COLOR" opacity="0.2" transform="rotate(-45,-26,-30)"/>
<rect x="18" y="-34" width="16" height="8" rx="3" fill="COLOR" opacity="0.2" transform="rotate(45,26,-30)"/>
<rect x="-34" y="26" width="16" height="8" rx="3" fill="COLOR" opacity="0.2" transform="rotate(45,-26,30)"/>
<rect x="18" y="26" width="16" height="8" rx="3" fill="COLOR" opacity="0.2" transform="rotate(-45,26,30)"/>
</g>'''

SHAPES['其他'] = SHAPES['配件']

# Watch/smart device
SHAPES['Wearable'] = '''<g transform="translate(200,155)" fill="COLOR" opacity="0.8">
<rect x="-25" y="-38" width="50" height="55" rx="12" fill="none" stroke="COLOR" stroke-width="3.5"/>
<rect x="-15" y="-25" width="30" height="28" rx="5" fill="COLOR" opacity="0.2"/>
<path d="M-8,-38 L-12,-48 L-8,-42 L-4,-48 L0,-42 L4,-48 L8,-42 L12,-48 L8,-38" fill="COLOR" opacity="0.3"/>
<path d="M-8,17 L-12,27 L-8,21 L-4,27 L0,21 L4,27 L8,21 L12,27 L8,17" fill="COLOR" opacity="0.3"/>
</g>'''

SHAPES['智能手錶'] = SHAPES['Wearable']
SHAPES['智能家居'] = SHAPES['Wearable']

# Location pin
SHAPES['定位器 / FindMy'] = '''<g transform="translate(200,155)" fill="COLOR" opacity="0.8">
<path d="M0,-50 C-35,-50 -45,-10 -45,10 C-45,30 0,55 0,55 C0,55 45,30 45,10 C45,-10 35,-50 0,-50Z" fill="COLOR" opacity="0.2" stroke="COLOR" stroke-width="3"/>
<circle cx="0" cy="0" r="10" fill="COLOR" opacity="0.4"/>
<circle cx="0" cy="-50" r="4" fill="COLOR"/>
</g>'''

# Stylus
SHAPES['觸控筆'] = '''<g transform="translate(200,155)" fill="COLOR" opacity="0.8">
<path d="M-40,50 L30,-30" stroke="COLOR" stroke-width="4" stroke-linecap="round"/>
<rect x="20" y="-45" width="25" height="35" rx="6" fill="COLOR" opacity="0.2" stroke="COLOR" stroke-width="2.5"/>
<circle cx="-30" cy="40" r="6" fill="COLOR" opacity="0.4"/>
</g>'''

# Stand/holder
SHAPES['支架 / 座'] = '''<g transform="translate(200,155)" fill="COLOR" opacity="0.8">
<rect x="-10" y="-55" width="20" height="70" rx="4" fill="COLOR" opacity="0.15" stroke="COLOR" stroke-width="3"/>
<rect x="-35" y="-45" width="70" height="36" rx="6" fill="COLOR" opacity="0.2" stroke="COLOR" stroke-width="2.5"/>
<line x1="-25" y1="-25" x2="25" y2="-25" stroke="COLOR" stroke-width="2" opacity="0.4"/>
</g>'''

# Health
SHAPES['醫療健康'] = '''<g transform="translate(200,155)" fill="COLOR" opacity="0.8">
<rect x="-20" y="-55" width="40" height="65" rx="10" fill="none" stroke="COLOR" stroke-width="3.5"/>
<path d="M-5,-10 L-5,-30 M5,-10 L5,-30 M-10,-20 L10,-20" stroke="COLOR" stroke-width="3" stroke-linecap="round"/>
<circle cx="0" cy="10" r="6" fill="COLOR" opacity="0.3"/>
</g>'''

SHAPES['按摩 / 健康'] = SHAPES['醫療健康']
SHAPES['按摩器'] = SHAPES['醫療健康']
SHAPES['個人護理'] = SHAPES['醫療健康']

# Translation device
SHAPES['智能翻譯設備'] = '''<g transform="translate(200,155)" fill="COLOR" opacity="0.8">
<rect x="-20" y="-45" width="40" height="70" rx="8" fill="none" stroke="COLOR" stroke-width="3.5"/>
<rect x="-12" y="-35" width="24" height="18" rx="3" fill="COLOR" opacity="0.2"/>
<text x="0" y="-23" text-anchor="middle" font-size="10" fill="COLOR" font-weight="700">A</text>
</g>'''

# Air purifier
SHAPES['空氣淨化'] = '''<g transform="translate(200,155)" fill="COLOR" opacity="0.8">
<rect x="-25" y="-50" width="50" height="85" rx="10" fill="none" stroke="COLOR" stroke-width="3.5"/>
<circle cx="0" cy="-10" r="18" fill="COLOR" opacity="0.15" stroke="COLOR" stroke-width="2"/>
<path d="M-8,-10 L8,-10 M0,-18 L0,-2" stroke="COLOR" stroke-width="2"/>
</g>'''

# Tool
SHAPES['工具'] = '''<g transform="translate(200,155)" fill="COLOR" opacity="0.8">
<rect x="-35" y="-40" width="70" height="12" rx="4" fill="COLOR" opacity="0.2" stroke="COLOR" stroke-width="2.5"/>
<rect x="-18" y="-28" width="36" height="60" rx="4" fill="COLOR" opacity="0.15" stroke="COLOR" stroke-width="2.5"/>
<rect x="-8" y="32" width="16" height="25" rx="3" fill="COLOR" opacity="0.3"/>
</g>'''

# Bottle
SHAPES['水壺/保溫'] = '''<g transform="translate(200,155)" fill="COLOR" opacity="0.8">
<rect x="-18" y="-55" width="36" height="70" rx="10" fill="none" stroke="COLOR" stroke-width="3.5"/>
<rect x="-20" y="-62" width="40" height="10" rx="4" fill="COLOR" opacity="0.3"/>
<line x1="-8" y1="-30" x2="8" y2="-30" stroke="COLOR" stroke-width="2" opacity="0.4"/>
<line x1="-8" y1="-10" x2="8" y2="-10" stroke="COLOR" stroke-width="2" opacity="0.4"/>
</g>'''

# Camera
SHAPES['相機'] = '''<g transform="translate(200,155)" fill="COLOR" opacity="0.8">
<rect x="-35" y="-30" width="70" height="50" rx="8" fill="none" stroke="COLOR" stroke-width="3.5"/>
<circle cx="0" cy="-5" r="16" fill="COLOR" opacity="0.15" stroke="COLOR" stroke-width="2.5"/>
<circle cx="0" cy="-5" r="6" fill="COLOR" opacity="0.3"/>
<rect x="-10" y="-40" width="20" height="10" rx="3" fill="COLOR" opacity="0.2"/>
</g>'''

# Create SVG for a product
def make_svg(brand, category):
    color = brand_color(brand)
    shape = SHAPES.get(category, SHAPES['其他']).replace('COLOR', color)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="400" height="400" viewBox="0 0 400 400">
  <defs>
    <radialGradient id="bg" cx="50%" cy="40%" r="60%">
      <stop offset="0%" style="stop-color:{color};stop-opacity:0.10"/>
      <stop offset="100%" style="stop-color:{color};stop-opacity:0.03"/>
    </radialGradient>
  </defs>
  <rect width="400" height="400" fill="url(#bg)" rx="12"/>
  {shape}
  <text x="200" y="280" text-anchor="middle" font-family="system-ui,sans-serif" font-size="13" font-weight="600" fill="{color}" letter-spacing="0.5">{brand}</text>
  <text x="200" y="310" text-anchor="middle" font-family="system-ui,sans-serif" font-size="10" fill="#999999">{category}</text>
  <text x="200" y="355" text-anchor="middle" font-family="system-ui,sans-serif" font-size="9" fill="#aaaaaa">Panda Telecom</text>
</svg>'''


def main():
    with open('products-all.js', 'r') as f:
        content = f.read()

    start = content.index('[')
    depth = 0
    end = start
    for i in range(start, len(content)):
        if content[i] == '[':
            depth += 1
        elif content[i] == ']':
            depth -= 1
            if depth == 0:
                end = i + 1
                break

    products = json.loads(content[start:end])

    os.makedirs('products-img', exist_ok=True)

    generated = 0
    skipped = 0
    errors = []

    for p in products:
        img = p.get('image', '').strip()
        if not img or '.svg' not in img.lower():
            skipped += 1
            continue

        # Extract the filename
        fn = img.replace('products-img/', '')
        if not fn or fn == '.svg':
            # Broken entry -- skip
            errors.append(f'Broken: {p.get("name","?")} id={p.get("id","?")}')
            continue

        path = os.path.join('products-img', fn)
        brand = p.get('brand', '')
        category = p.get('category', '其他')

        svg_content = make_svg(brand, category)
        with open(path, 'w') as f:
            f.write(svg_content)
        generated += 1

    print(f'Generated: {generated} SVGs')
    print(f'Skipped (real images): {skipped}')
    if errors:
        print(f'Broken entries: {len(errors)}')
        for e in errors[:5]:
            print(f'  {e}')

if __name__ == '__main__':
    main()
