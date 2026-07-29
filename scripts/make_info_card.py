import os

def generate_info_card_svg(output_path, static=False):
    width = 490
    height = 500  # Will look neat next to the ascii portrait

    # Content data
    username = "arpitmangaraj"
    hostname = "github"
    
    # ANSI color palette hex values
    ansi_colors = [
        "#161b22",  # Black
        "#ff7b72",  # Red
        "#39d353",  # Green
        "#f2cc60",  # Yellow
        "#58a6ff",  # Blue
        "#bc8cff",  # Magenta
        "#39c5cf",  # Cyan
        "#ffffff"   # White
    ]

    # Key-value rows to render
    rows = [
        ("OS", "Ubuntu 24.04 LTS x86_64 / Cloud"),
        ("Host", "Arpit Mangaraj Profile"),
        ("Kernel", "Python 3.12.7 & Node.js"),
        ("Uptime", "25 years (Continuous Learning)"),
        ("Shell", "zsh / pwsh / agentic"),
        ("Now", "Building AI systems & full-stack applications"),
        ("Prev", "Full-Stack Architect & DevOps Enthusiast"),
        ("Stack", "React, Next.js, Node, Go, Python, Docker, AWS"),
        ("Focus", "Web automation, distributed APIs & high scale systems")
    ]

    svg_lines = []
    svg_lines.append(f'<svg width="100%" height="100%" viewBox="0 0 {width} {height}" fill="none" xmlns="http://www.w3.org/2000/svg">')
    
    # CSS Styles & Animations
    svg_lines.append('  <style>')
    svg_lines.append('    .terminal-bg {')
    svg_lines.append('      fill: #0d1117;')
    svg_lines.append('      stroke: #30363d;')
    svg_lines.append('      stroke-width: 1.5;')
    svg_lines.append('      rx: 8px;')
    svg_lines.append('    }')
    svg_lines.append('    .title-bar-bg {')
    svg_lines.append('      fill: #161b22;')
    svg_lines.append('      stroke: #30363d;')
    svg_lines.append('      stroke-width: 1.5;')
    svg_lines.append('    }')
    svg_lines.append('    .terminal-text {')
    svg_lines.append('      font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace;')
    svg_lines.append('      font-size: 13px;')
    svg_lines.append('      fill: #c9d1d9;')
    svg_lines.append('    }')
    svg_lines.append('    .title-text {')
    svg_lines.append('      fill: #8b949e;')
    svg_lines.append('      text-anchor: middle;')
    svg_lines.append('    }')
    svg_lines.append('    .prompt-user { font-weight: bold; fill: #58a6ff; }')
    svg_lines.append('    .prompt-host { font-weight: bold; fill: #39d353; }')
    svg_lines.append('    .prompt-sep { fill: #8b949e; }')
    svg_lines.append('    .prompt-cmd { fill: #c9d1d9; }')
    svg_lines.append('    .key { font-weight: bold; fill: #ff7b72; }')
    svg_lines.append('    .val { fill: #c9d1d9; }')
    
    # Animations
    if static:
        svg_lines.append('    .animate-line { opacity: 1; }')
    else:
        svg_lines.append('    @keyframes fadeInUp {')
        svg_lines.append('      from {')
        svg_lines.append('        opacity: 0;')
        svg_lines.append('        transform: translateY(6px);')
        svg_lines.append('      }')
        svg_lines.append('      to {')
        svg_lines.append('        opacity: 1;')
        svg_lines.append('        transform: translateY(0);')
        svg_lines.append('      }')
        svg_lines.append('    }')
        svg_lines.append('    .animate-line {')
        svg_lines.append('      opacity: 0;')
        svg_lines.append('      animation: fadeInUp 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards;')
        svg_lines.append('    }')
    svg_lines.append('  </style>')

    # 1. Background Card
    svg_lines.append(f'  <rect x="1" y="1" width="{width-2}" height="{height-2}" class="terminal-bg" />')

    # 2. Window Title Bar (macOS style window buttons)
    svg_lines.append(f'  <path d="M 1,36 L {width-1},36 L {width-1},8 A 8,8 0 0,0 {width-9},0 L 9,0 A 8,8 0 0,0 1,8 Z" class="title-bar-bg" />')
    
    # Red, Yellow, Green Window Dots
    svg_lines.append('  <circle cx="18" cy="18" r="6" fill="#ff5f56" />')
    svg_lines.append('  <circle cx="38" cy="18" r="6" fill="#ffbd2e" />')
    svg_lines.append('  <circle cx="58" cy="18" r="6" fill="#27c93f" />')
    
    # Title Text
    svg_lines.append(f'  <text x="{width // 2}" y="22" class="terminal-text title-text">{username}@{hostname}: ~</text>')

    # 3. Main Terminal Area
    # Delay offset (in seconds)
    base_delay = 0.2
    delay_step = 0.15

    # Prompt line: arpit@github ~ $ neofetch
    delay_str = f'style="animation-delay: {base_delay:.2f}s;"' if not static else ''
    svg_lines.append(f'  <g class="terminal-text animate-line" {delay_str}>')
    svg_lines.append(f'    <text x="25" y="65">')
    svg_lines.append(f'      <tspan class="prompt-user">{username}</tspan>')
    svg_lines.append(f'      <tspan class="prompt-sep">@</tspan>')
    svg_lines.append(f'      <tspan class="prompt-host">{hostname}</tspan>')
    svg_lines.append(f'      <tspan class="prompt-sep"> ~ $ </tspan>')
    svg_lines.append(f'      <tspan class="prompt-cmd">neofetch</tspan>')
    svg_lines.append(f'    </text>')
    svg_lines.append(f'  </g>')

    # User Header
    base_delay += delay_step
    delay_str = f'style="animation-delay: {base_delay:.2f}s;"' if not static else ''
    svg_lines.append(f'  <g class="terminal-text animate-line" {delay_str}>')
    svg_lines.append(f'    <text x="25" y="95" class="prompt-host" style="font-weight: bold; font-size: 15px;">{username}@{hostname}</text>')
    svg_lines.append(f'  </g>')

    # Divider
    base_delay += delay_step
    delay_str = f'style="animation-delay: {base_delay:.2f}s;"' if not static else ''
    svg_lines.append(f'  <g class="terminal-text animate-line" {delay_str}>')
    svg_lines.append(f'    <text x="25" y="112" class="prompt-sep">----------------------</text>')
    svg_lines.append(f'  </g>')

    # Key-value rows
    start_y = 135
    row_height = 24
    for idx, (k, v) in enumerate(rows):
        y_pos = start_y + (idx * row_height)
        base_delay += delay_step
        delay_str = f'style="animation-delay: {base_delay:.2f}s;"' if not static else ''
        svg_lines.append(f'  <g class="terminal-text animate-line" {delay_str}>')
        svg_lines.append(f'    <text x="25" y="{y_pos}">')
        svg_lines.append(f'      <tspan class="key">{k}</tspan>')
        svg_lines.append(f'      <tspan class="prompt-sep">: </tspan>')
        # Wrap long text values slightly or just print
        # SVG doesn't auto-wrap tspan, but since width is 490, 13px font characters are ~8px wide.
        # Max chars we can fit is (490-25-100) / 8 = 45 chars. Let's make sure strings are compact.
        svg_lines.append(f'      <tspan class="val">{v}</tspan>')
        svg_lines.append(f'    </text>')
        svg_lines.append(f'  </g>')

    # 4. ANSI Colors Blocks
    base_delay += delay_step
    delay_str = f'style="animation-delay: {base_delay:.2f}s;"' if not static else ''
    blocks_y = start_y + (len(rows) * row_height) + 15
    svg_lines.append(f'  <g class="animate-line" {delay_str}>')
    for c_idx, color in enumerate(ansi_colors):
        x_pos = 25 + (c_idx * 24)
        svg_lines.append(f'    <rect x="{x_pos}" y="{blocks_y}" width="20" height="20" fill="{color}" rx="3" />')
    svg_lines.append('  </g>')

    svg_lines.append('</svg>')

    dirname = os.path.dirname(output_path)
    if dirname:
        os.makedirs(dirname, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_lines))
    print(f"Generated info card SVG at {output_path} (static={static})")

if __name__ == "__main__":
    is_static = os.environ.get("STATIC") == "1"
    generate_info_card_svg("info-card.svg", static=is_static)
