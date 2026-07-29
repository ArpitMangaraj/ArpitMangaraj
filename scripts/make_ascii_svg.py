import cv2
import html
import os
import numpy as np

def img_to_ascii_svg(image_path, svg_path):
    print(f"Reading prepped image from {image_path}...")
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print(f"Error: Could not read image from {image_path}")
        return

    # Character aspect ratio in monospace is roughly 0.6
    char_w_h_ratio = 0.6
    cols = 100
    h, w = img.shape
    img_ratio = w / h
    rows = int(cols / (img_ratio * char_w_h_ratio))
    
    # Cap rows to fit nicely on the GitHub profile page
    max_rows = 53
    if rows > max_rows:
        rows = max_rows
        
    resized = cv2.resize(img, (cols, rows), interpolation=cv2.INTER_AREA)

    # ASCII density ramp: space -> @ (bright -> dark)
    # Brightest values (white background) map to spaces. Darkest values map to @.
    ramp = " .`:-=+*cs#%@"
    num_chars = len(ramp)

    ascii_rows = []
    for r in range(rows):
        row_chars = []
        for c in range(cols):
            pixel = resized[r, c]
            # Map 255 -> 0, 0 -> num_chars-1
            idx = int((255 - pixel) / 255.0 * (num_chars - 1))
            row_chars.append(ramp[idx])
        ascii_rows.append("".join(row_chars))

    char_w = 7.2
    char_h = 12
    svg_w = cols * char_w
    svg_h = rows * char_h

    # Build the animated SVG
    svg_lines = []
    svg_lines.append(f'<svg width="100%" height="100%" viewBox="0 0 {svg_w} {svg_h}" fill="none" xmlns="http://www.w3.org/2000/svg">')
    
    # Styling
    svg_lines.append('  <style>')
    svg_lines.append('    .ascii-text {')
    svg_lines.append('      font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace;')
    svg_lines.append('      font-size: 12px;')
    svg_lines.append('      font-weight: 700;')
    svg_lines.append('      fill: #8b949e; /* GitHub gray text */')
    svg_lines.append('    }')
    svg_lines.append('    .cursor {')
    svg_lines.append('      fill: #58a6ff; /* GitHub accent blue */')
    svg_lines.append('    }')
    svg_lines.append('  </style>')

    # Defs containing clip paths for row animations
    svg_lines.append('  <defs>')
    
    row_duration = 0.5   # Duration to type a single row
    row_stagger = 0.08   # Time delay before starting the next row
    
    for i in range(rows):
        begin_time = f"{i * row_stagger:.2f}s"
        svg_lines.append(f'    <clipPath id="clip-row-{i}">')
        svg_lines.append(f'      <rect x="0" y="{i * char_h}" width="0" height="{char_h}">')
        svg_lines.append(f'        <animate attributeName="width" from="0" to="{svg_w}" begin="{begin_time}" dur="{row_duration}s" fill="freeze" />')
        svg_lines.append(f'      </rect>')
        svg_lines.append(f'    </clipPath>')
    
    svg_lines.append('  </defs>')

    # Group containing the rows of text
    svg_lines.append('  <g class="ascii-text">')
    for i in range(rows):
        escaped_row = html.escape(ascii_rows[i])
        y_pos = (i + 1) * char_h - 2  # Baseline adjustment
        svg_lines.append(f'    <text x="0" y="{y_pos}" clip-path="url(#clip-row-{i})">{escaped_row}</text>')
    svg_lines.append('  </g>')

    # Add block cursor riders that move with the clip paths
    for i in range(rows):
        begin_time = f"{i * row_stagger:.2f}s"
        y_pos = i * char_h + 1
        svg_lines.append(f'  <rect class="cursor" x="0" y="{y_pos}" width="7" height="10" opacity="0">')
        svg_lines.append(f'    <animate attributeName="x" from="0" to="{svg_w}" begin="{begin_time}" dur="{row_duration}s" fill="freeze" />')
        svg_lines.append(f'    <animate attributeName="opacity" values="1;1;0" keyTimes="0;0.95;1" begin="{begin_time}" dur="{row_duration}s" fill="freeze" />')
        svg_lines.append(f'  </rect>')

    svg_lines.append('</svg>')

    dirname = os.path.dirname(svg_path)
    if dirname:
        os.makedirs(dirname, exist_ok=True)
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_lines))
    print(f"Generated ASCII SVG at {svg_path}")

if __name__ == "__main__":
    img_to_ascii_svg("data/source-prepped.png", "avi-ascii.svg")
