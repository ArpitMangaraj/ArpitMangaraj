import os
import requests
from bs4 import BeautifulSoup
import re
import json
from datetime import datetime, timedelta

def fetch_contributions(username, output_json_path):
    url = f"https://github.com/users/{username}/contributions"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    print(f"Fetching contributions from {url}...")
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error fetching contributions: status code {response.status_code}")
        return False
        
    soup = BeautifulSoup(response.text, "html.parser")
    
    # 1. Extract total contributions string (e.g., "88 contributions in the last year")
    total_str = "0 contributions"
    heading_text = soup.find(string=re.compile(r"contributions\s+in\s+the\s+last\s+year", re.IGNORECASE))
    if heading_text:
        heading_text_clean = heading_text.strip().replace("\n", " ")
        # collapse spaces
        heading_text_clean = " ".join(heading_text_clean.split())
        match = re.search(r'^([\d,]+)\s+contributions', heading_text_clean, re.IGNORECASE)
        if match:
            total_str = f"{match.group(1)} contributions in the last year"
            
    # 2. Extract daily contributions
    # First, build a map of element IDs to tooltips
    tooltip_map = {}
    for tooltip in soup.find_all("tool-tip"):
        for_id = tooltip.get("for")
        if for_id:
            tooltip_map[for_id] = tooltip.text.strip()
            
    # Find all calendar day cells
    days_data = []
    day_cells = soup.find_all("td", class_="ContributionCalendar-day")
    if not day_cells:
        day_cells = soup.find_all("rect", class_="ContributionCalendar-day")
        
    print(f"Found {len(day_cells)} day cells")
    
    for cell in day_cells:
        cell_id = cell.get("id")
        date_str = cell.get("data-date")
        level_str = cell.get("data-level", "0")
        
        if not date_str:
            continue
            
        level = int(level_str)
        
        # Determine contribution count from tooltip text or estimate from level
        count = 0
        tooltip_text = tooltip_map.get(cell_id, "")
        if tooltip_text:
            match = re.search(r'^(\d+|No)\s+contribution', tooltip_text, re.IGNORECASE)
            if match:
                val = match.group(1)
                count = 0 if val.lower() == "no" else int(val.replace(",", ""))
            else:
                # fallback simple level estimates
                count = level if level == 0 else (level * 2 - 1)
        else:
            # Fallback estimation if tooltip is missing
            count = level if level == 0 else (level * 2 - 1)
            
        days_data.append({
            "date": date_str,
            "count": count,
            "level": level
        })
        
    # Sort days by date
    days_data.sort(key=lambda d: d["date"])
    
    # 3. Calculate statistics
    total_sum = sum(d["count"] for d in days_data)
    
    # Peak day
    best_day = {"date": "N/A", "count": 0}
    for d in days_data:
        if d["count"] > best_day["count"]:
            best_day = {"date": d["date"], "count": d["count"]}
            
    # Streaks calculation
    longest_streak = 0
    current_streak = 0
    running_streak = 0
    
    # To determine current streak, we check from the end of the list.
    # If the last day has 0 contributions, we check if it is today or yesterday.
    # If both have 0 contributions, current streak is 0.
    for d in days_data:
        if d["count"] > 0:
            running_streak += 1
            longest_streak = max(longest_streak, running_streak)
        else:
            running_streak = 0
            
    # Count backwards from the last element
    if days_data:
        last_index = len(days_data) - 1
        
        # Check if last day or second-to-last day is active
        # (This allows today to be 0 without breaking the streak immediately, as today might have just started)
        start_streak_idx = -1
        
        if days_data[last_index]["count"] > 0:
            start_streak_idx = last_index
        elif last_index > 0 and days_data[last_index - 1]["count"] > 0:
            # Check if last_index is today
            last_date = datetime.strptime(days_data[last_index]["date"], "%Y-%m-%d")
            prev_date = datetime.strptime(days_data[last_index - 1]["date"], "%Y-%m-%d")
            # If the difference is 1 day, it means yesterday has contributions, so streak is active
            if (last_date - prev_date).days <= 1:
                start_streak_idx = last_index - 1
                
        if start_streak_idx != -1:
            for idx in range(start_streak_idx, -1, -1):
                if days_data[idx]["count"] > 0:
                    current_streak += 1
                else:
                    break
                    
    # monthly totals
    monthly_totals = {}
    for d in days_data:
        dt = datetime.strptime(d["date"], "%Y-%m-%d")
        month_key = dt.strftime("%Y-%m")
        monthly_totals[month_key] = monthly_totals.get(month_key, 0) + d["count"]
        
    # Build statistics payload
    stats = {
        "total_contributions_text": total_str if total_sum > 0 else f"{total_sum} contributions in the last year",
        "total_contributions_count": total_sum,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "best_day": best_day,
        "monthly_totals": monthly_totals,
        "days": days_data
    }
    
    # Save to data/contributions.json
    os.makedirs(os.path.dirname(output_json_path), exist_ok=True)
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)
        
    print(f"Saved contributions statistics to {output_json_path}")
    print(f"Total contributions: {total_sum}")
    print(f"Current Streak: {current_streak} days, Longest Streak: {longest_streak} days")
    print(f"Best Day: {best_day['date']} ({best_day['count']} contributions)")
    return True

if __name__ == "__main__":
    fetch_contributions("ArpitMangaraj", "data/contributions.json")
