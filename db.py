"""
Supabase database helper module.
Provides CRUD operations for portfolio, savings goals, and user settings.
No authentication — single default user.
"""
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

_client = None

def get_client():
    """Get or create Supabase client (singleton)."""
    global _client
    if _client is None:
        if not SUPABASE_URL or not SUPABASE_KEY:
            raise ValueError("Missing SUPABASE_URL or SUPABASE_KEY in .env")
        _client = create_client(SUPABASE_URL, SUPABASE_KEY)
    return _client


# ==========================================
# PORTFOLIO
# ==========================================

def get_portfolio():
    """Fetch all portfolio holdings from Supabase."""
    try:
        res = get_client().table("portfolio").select("*").order("id").execute()
        return [
            {"symbol": r["symbol"], "name": r["name"], "shares": r["shares"],
             "avg_cost": r["avg_cost"], "region": r["region"], "db_id": r["id"]}
            for r in res.data
        ]
    except Exception as e:
        print(f"[DB] Error loading portfolio: {e}")
        return None


def add_holding(holding):
    """Add a new holding to the portfolio."""
    try:
        get_client().table("portfolio").insert({
            "symbol": holding["symbol"],
            "name": holding["name"],
            "shares": holding["shares"],
            "avg_cost": holding["avg_cost"],
            "region": holding["region"],
        }).execute()
        return True
    except Exception as e:
        print(f"[DB] Error adding holding: {e}")
        return False


def delete_holding(symbol):
    """Delete a holding by symbol."""
    try:
        get_client().table("portfolio").delete().eq("symbol", symbol).execute()
        return True
    except Exception as e:
        print(f"[DB] Error deleting holding: {e}")
        return False


# ==========================================
# SAVINGS GOALS
# ==========================================

def get_goals():
    """Fetch all savings goals from Supabase."""
    try:
        res = get_client().table("savings_goals").select("*").order("id").execute()
        return [
            {"name": r["name"], "target": r["target"], "saved": r["saved"],
             "icon": r["icon"], "weekly": r["weekly"], "color": r["color"], "db_id": r["id"]}
            for r in res.data
        ]
    except Exception as e:
        print(f"[DB] Error loading goals: {e}")
        return None


def add_goal(goal):
    """Add a new savings goal."""
    try:
        get_client().table("savings_goals").insert({
            "name": goal["name"],
            "target": goal["target"],
            "saved": goal.get("saved", 0),
            "icon": goal["icon"],
            "weekly": goal["weekly"],
            "color": goal.get("color", "#a855f7"),
        }).execute()
        return True
    except Exception as e:
        print(f"[DB] Error adding goal: {e}")
        return False


def update_goal_saved(db_id, new_saved):
    """Update the saved amount for a goal."""
    try:
        get_client().table("savings_goals").update(
            {"saved": new_saved}
        ).eq("id", db_id).execute()
        return True
    except Exception as e:
        print(f"[DB] Error updating goal: {e}")
        return False


# ==========================================
# USER SETTINGS
# ==========================================

def get_setting(key, default="0"):
    """Get a user setting by key."""
    try:
        res = get_client().table("user_settings").select("value").eq("key", key).execute()
        if res.data:
            return res.data[0]["value"]
        return default
    except Exception as e:
        print(f"[DB] Error getting setting '{key}': {e}")
        return default


def set_setting(key, value):
    """Set a user setting (upsert)."""
    try:
        get_client().table("user_settings").upsert(
            {"key": key, "value": str(value)},
            on_conflict="key"
        ).execute()
        return True
    except Exception as e:
        print(f"[DB] Error setting '{key}': {e}")
        return False


# ==========================================
# PAYSLIP HISTORY
# ==========================================

def save_payslip(employment_type, hourly_rate, total_hours, overtime_hours, total_pay, shifts_data):
    """Save a payslip calculation to history."""
    try:
        import json
        get_client().table("payslip_history").insert({
            "employment_type": employment_type,
            "hourly_rate": hourly_rate,
            "total_hours": total_hours,
            "overtime_hours": overtime_hours,
            "total_pay": total_pay,
            "shifts_data": json.dumps(shifts_data),
        }).execute()
        return True
    except Exception as e:
        print(f"[DB] Error saving payslip: {e}")
        return False


def get_payslip_history(limit=20):
    """Fetch recent payslip history."""
    try:
        res = get_client().table("payslip_history").select("*").order(
            "calculated_at", desc=True
        ).limit(limit).execute()
        return res.data
    except Exception as e:
        print(f"[DB] Error loading payslip history: {e}")
        return []

