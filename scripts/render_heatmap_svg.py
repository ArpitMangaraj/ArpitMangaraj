import os
import json
from datetime import datetime

def render_heatmap(json_path, svg_path):
    print(f"Reading contributions data from {json_path}...")
    if not os.path.exists(json_path):
        print(f"Error: JSON file {json_path} does not exist. Run fetch_contributions.py first.")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        stats = json.load(f)

    days = stats["days"]
    
    # Group days by week (Sunday to Saturday)
    # The first day in days is a Sunday, so we can group in chunks of 7
    weeks = []
    for i in range(0, len(days), 7):
        weeks.append(days[i:i+7])

    # SVG Canvas dimensions
    width = 860
    height = 250
    
    # Positions & Spacing
    grid_x = 55
    grid_y = 55
    cell_size = 11
    cell_gap = 3
    col_width = cell_size + cell_gap # 14px

    # Palette
    # Level 0 to 4 colors
    palette = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]

    svg_lines = []
    svg_lines.append(f'<svg width="100%" height="100%" viewBox="0 0 {width} {height}" fill="none" xmlns="http://www.w3.org/2000/svg">')
    
    # CSS Styles & Animations
    svg_lines.append('  <style>')
    svg_lines.append('    .card-bg {')
    svg_lines.append('      fill: #0d1117;')
    svg_lines.append('      stroke: #30363d;')
    svg_lines.append('      stroke-width: 1.5;')
    svg_lines.append('      rx: 8px;')
    svg_lines.append('    }')
    svg_lines.append('    .text-main {')
    svg_lines.append('      font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace;')
    svg_lines.append('      font-size: 11px;')
    svg_lines.append('      fill: #8b949e;')
    svg_lines.append('    }')
    svg_lines.append('    .text-title {')
    svg_lines.append('      font-size: 13px;')
    svg_lines.append('      font-weight: bold;')
    svg_lines.append('      fill: #c9d1d9;')
    svg_lines.append('    }')
    svg_lines.append('    .text-stats {')
    svg_lines.append('      font-size: 12px;')
    svg_lines.append('      fill: #a5d6ff;')
    svg_lines.append('    }')
    svg_lines.append('    @keyframes cellFadeIn {')
    svg_lines.append('      from {')
    svg_lines.append('        opacity: 0;')
    svg_lines.append('        transform: scale(0.3);')
    svg_lines.append('      }')
    svg_lines.append('      to {')
    svg_lines.append('        opacity: 1;')
    svg_lines.append('        transform: scale(1);')
    svg_lines.append('      }')
    svg_lines.append('    }')
    svg_lines.append('    .cell {')
    svg_lines.append('      opacity: 0;')
    svg_lines.append('      animation: cellFadeIn 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards;')
    svg_lines.append('      transform-origin: center;')
    svg_lines.append('      transform-box: fill-box;')
    svg_lines.append('    }')
    svg_lines.append('  </style>')

    # 1. Background Card
    svg_lines.append(f'  <rect x="1" y="1" width="{width-2}" height="{height-2}" class="card-bg" />')

    # 2. Title Label
    svg_lines.append(f'  <text x="25" y="30" class="text-main text-title">Contributions Calendar</text>')

    # 3. Month labels
    # We find the month for each column and render it above the grid
    month_labels = []
    prev_month = None
    for col_idx, week in enumerate(weeks):
        if not week:
            continue
        first_day_dt = datetime.strptime(week[0]["date"], "%Y-%m-%d")
        month_name = first_day_dt.strftime("%b")
        if month_name != prev_month:
            month_labels.append((col_idx, month_name))
            prev_month = month_name

    # Filter month labels to avoid crowding
    filtered_months = []
    last_col = -10
    for col_idx, name in month_labels:
        if col_idx - last_col >= 3:
            filtered_months.append((col_idx, name))
            last_col = col_idx

    for col_idx, name in filtered_months:
        x_pos = grid_x + (col_idx * col_width)
        svg_lines.append(f'  <text x="{x_pos}" y="45" class="text-main">{name}</text>')

    # 4. Weekday labels (Mon, Wed, Fri) on the left
    # Row 1 is Mon, 3 is Wed, 5 is Fri
    svg_lines.append(f'  <text x="25" y="{grid_y + 1 * col_width + 9}" class="text-main">Mon</text>')
    svg_lines.append(f'  <text x="25" y="{grid_y + 3 * col_width + 9}" class="text-main">Wed</text>')
    svg_lines.append(f'  <text x="25" y="{grid_y + 5 * col_width + 9}" class="text-main">Fri</text>')

    # 5. Grid of cells
    for col_idx, week in enumerate(weeks):
        x_pos = grid_x + (col_idx * col_width)
        for row_idx, day_info in enumerate(week):
            y_pos = grid_y + (row_idx * col_width)
            
            level = day_info["level"]
            color = palette[min(level, len(palette)-1)]
            
            # Staggered delay based on diagonal coordinates
            delay = (col_idx + row_idx) * 0.015
            
            svg_lines.append(f'  <rect x="{x_pos}" y="{y_pos}" width="{cell_size}" height="{cell_size}" fill="{color}" rx="2" class="cell" style="animation-delay: {delay:.3f}s;" />')

    # 6. Legend at the bottom right
    # Placed below the grid
    legend_start_x = width - 150
    legend_y = grid_y + 7 * col_width + 12
    svg_lines.append(f'  <text x="{legend_start_x - 35}" y="{legend_y + 9}" class="text-main">Less</text>')
    for idx, color in enumerate(palette):
        x_pos = legend_start_x + (idx * 14)
        svg_lines.append(f'    <rect x="{x_pos}" y="{legend_y}" width="{cell_size}" height="{cell_size}" fill="{color}" rx="2" />')
    svg_lines.append(f'  <text x="{legend_start_x + len(palette)*14 + 5}" y="{legend_y + 9}" class="text-main">More</text>')

    # 7. Stats Footer
    footer_y = legend_y + 35
    total_text = stats["total_contributions_text"]
    current_streak = stats["current_streak"]
    longest_streak = stats["longest_streak"]
    best_day_date = stats["best_day"]["date"]
    best_day_count = stats["best_day"]["count"]
    
    stats_str = f"Streak: {current_streak} days (Current) | {longest_streak} days (Longest)"
    best_day_str = f"Best Day: {best_day_count} ({best_day_date})"
    
    svg_lines.append(f'  <text x="25" y="{footer_y}" class="text-main text-stats" style="font-weight: bold;">{total_text}</text>')
    svg_lines.append(f'  <text x="320" y="{footer_y}" class="text-main text-stats">{stats_str}</text>')
    svg_lines.append(f'  <text x="640" y="{footer_y}" class="text-main text-stats">{best_day_str}</text>')

    svg_lines.append('</svg>')

    dirname = os.path.dirname(svg_path)
    if dirname:
        os.makedirs(dirname, exist_ok=True)
        
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_lines))
        
    print(f"Successfully rendered contribution heatmap SVG to {svg_path}")

if __name__ == "__main__":
    render_heatmap("data/contributions.json", "contrib-heatmap.svg")
