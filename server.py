import os
from fastmcp import FastMCP
from dotenv import load_dotenv
from datetime import datetime
import re

# 1. SETUP & CONFIG
load_dotenv()
mcp = FastMCP("FairWorkAdvancedServer")

# 2. PAY RATES (Fair Work Australia - Retail Award 2024-2025)
BASE_RATES = {
    "Level 1": {"adult": 25.65, "20": 23.09, "19": 20.52, "18": 17.96, "17": 15.39, "16": 12.83},
    "Level 2": {"adult": 27.20, "20": 24.48, "19": 21.76, "18": 19.04, "17": 16.32, "16": 13.60},
    "Level 3": {"adult": 27.65, "20": 24.89, "19": 22.12, "18": 19.36, "17": 16.59, "16": 13.83},
    "Level 4": {"adult": 28.20, "20": 25.38, "19": 22.56, "18": 19.74, "17": 16.92, "16": 14.10},
}

# Penalty rates
PENALTY_MULTIPLIERS = {
    "monday": 1.0,
    "tuesday": 1.0,
    "wednesday": 1.0,
    "thursday": 1.0,
    "friday": 1.0,
    "saturday": 1.25,  # 25% loading
    "sunday": 1.50,    # 50% loading
    "public_holiday": 2.50,
}

DAY_ALIASES = {
    "mon": "monday", "tue": "tuesday", "wed": "wednesday",
    "thu": "thursday", "thur": "thursday", "fri": "friday",
    "sat": "saturday", "sun": "sunday"
}


def parse_time(time_str):
    """Parse time string like '9am', '10pm', '9:30am' to hours (24h)"""
    time_str = time_str.strip().lower().replace(" ", "")
    
    # Handle formats: 9am, 9:30am, 9:00pm
    match = re.match(r'(\d{1,2}):?(\d{2})?(am|pm)?', time_str)
    if not match:
        return None
    
    hour = int(match.group(1))
    minutes = int(match.group(2)) if match.group(2) else 0
    period = match.group(3)
    
    if period == 'pm' and hour != 12:
        hour += 12
    elif period == 'am' and hour == 12:
        hour = 0
    
    return hour + minutes / 60


def calculate_hours(start_str, end_str):
    """Calculate hours between start and end time"""
    start = parse_time(start_str)
    end = parse_time(end_str)
    
    if start is None or end is None:
        return 8  # Default to 8 hours
    
    if end <= start:
        end += 24  # Overnight shift
    
    return end - start


def get_penalty_multiplier(day_str):
    """Get penalty multiplier for a given day"""
    day_lower = day_str.lower().strip().rstrip(':')
    
    # Check aliases
    for alias, full_day in DAY_ALIASES.items():
        if day_lower.startswith(alias):
            return PENALTY_MULTIPLIERS.get(full_day, 1.0), full_day.title()
    
    # Check full day names
    for day, mult in PENALTY_MULTIPLIERS.items():
        if day_lower.startswith(day[:3]):
            return mult, day.title()
    
    return 1.0, "Weekday"


@mcp.tool()
def calculate_shift_pay(shift: str, level: str = "Level 1", age: str = "21") -> str:
    """
    Calculates total pay for a shift with detailed breakdown.
    
    Args:
        shift: The shift description like "Mon: 9am-5pm"
        level: Classification level (Level 1-4)
        age: Employee age for junior rates
    
    Returns:
        Detailed breakdown of pay calculation
    """
    # Parse the shift
    shift = shift.strip()
    
    # Extract day and times
    if ':' in shift:
        parts = shift.split(':', 1)
        day = parts[0].strip()
        times = parts[1].strip() if len(parts) > 1 else ""
    else:
        day = "Monday"
        times = shift
    
    # Parse start/end times
    time_parts = times.replace('–', '-').split('-')
    if len(time_parts) == 2:
        start_time = time_parts[0].strip()
        end_time = time_parts[1].strip()
    else:
        start_time = "9am"
        end_time = "5pm"
    
    # Calculate hours
    hours = calculate_hours(start_time, end_time)
    
    # Get base rate
    level_key = "Level 1"
    for l in ["Level 1", "Level 2", "Level 3", "Level 4"]:
        if l[-1] in level:
            level_key = l
            break
    
    age_key = "adult" if int(age) >= 21 else str(age)
    base_rate = BASE_RATES.get(level_key, BASE_RATES["Level 1"]).get(age_key, 26.55)
    
    # Get penalty multiplier
    multiplier, day_name = get_penalty_multiplier(day)
    
    # Calculate total
    gross_pay = hours * base_rate * multiplier
    
    # Build breakdown
    breakdown = f"""
📊 **SHIFT BREAKDOWN**
━━━━━━━━━━━━━━━━━━━━
📅 Day: {day_name}
⏰ Time: {start_time} - {end_time}
⏱️ Hours: {hours:.1f}h

💵 Base Rate: ${base_rate:.2f}/hr ({level_key}, {'Adult' if age_key == 'adult' else f'Age {age}'})
📈 Penalty: {multiplier}x {f'({int((multiplier-1)*100)}% loading)' if multiplier > 1 else '(No loading)'}
━━━━━━━━━━━━━━━━━━━━
💰 **TOTAL PAY: ${gross_pay:.2f}**
"""
    return breakdown.strip()


@mcp.tool()
def lookup_pay_rate(level: str, age: str) -> str:
    """Finds the Base Hourly Rate ($) for a given level and age."""
    level_key = "Level 1"
    for l in ["Level 1", "Level 2", "Level 3", "Level 4"]:
        if l[-1] in level:
            level_key = l
            break
    
    age_str = str(age).strip()
    age_key = "adult" if age_str.isdigit() and int(age_str) >= 21 else age_str
    if age_key not in ["adult", "20", "19", "18", "17", "16"]:
        age_key = "adult"
    
    rate = BASE_RATES.get(level_key, {}).get(age_key, 26.55)
    return f"${rate:.2f}/hour"


@mcp.tool()
def check_penalty_rates(day: str, start_time: str, end_time: str) -> str:
    """Checks penalty rates for a specific day and time."""
    multiplier, day_name = get_penalty_multiplier(day)
    
    if multiplier > 1:
        loading = int((multiplier - 1) * 100)
        return f"{day_name}: {multiplier}x multiplier ({loading}% loading applies)"
    else:
        return f"{day_name}: Standard rate (no penalty loading)"


if __name__ == "__main__":
    mcp.run()