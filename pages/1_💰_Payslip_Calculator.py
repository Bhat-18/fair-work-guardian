import streamlit as st
import asyncio
import re
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db import set_setting, save_payslip, get_payslip_history, delete_payslip, clear_payslip_history
from session import get_user_id

user_id = get_user_id()

st.set_page_config(page_title="Payslip Calculator", layout="centered", page_icon="💰", initial_sidebar_state="collapsed")

# ==========================================
# CSS
# ==========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    .stApp {
        background: linear-gradient(180deg, #0a0a0f 0%, #1a1a2e 100%);
        font-family: 'Inter', -apple-system, sans-serif;
    }
    
    .main .block-container { padding: 1.5rem; max-width: 700px; }
    
    /* Hide sidebar */
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="stSidebarNav"] { display: none !important; }
    section[data-testid="stSidebar"] { display: none !important; }
    button[kind="header"] { display: none !important; }
    
    /* Back button */
    .back-btn {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        color: #9ca3af;
        text-decoration: none;
        font-size: 0.9rem;
        margin-bottom: 1rem;
        padding: 0.5rem 1rem;
        background: rgba(255,255,255,0.05);
        border-radius: 8px;
        cursor: pointer;
    }
    .back-btn:hover { color: #fff; background: rgba(255,255,255,0.1); }
    
    /* Hero */
    .hero {
        text-align: center;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        border-radius: 16px;
    }
    .hero h1 { font-size: 1.75rem; font-weight: 800; color: #fff; margin: 0; }
    .hero p { color: rgba(255,255,255,0.9); margin-top: 0.25rem; font-size: 0.9rem; }
    
    /* Cards */
    .card {
        background: #1a1a2e;
        border: 1px solid #2d2d4a;
        border-radius: 14px;
        padding: 1.25rem;
        margin-bottom: 1rem;
    }
    .card-header { display: flex; align-items: center; gap: 0.5rem; }
    .card-icon { font-size: 1.25rem; }
    .card-title { font-size: 1rem; font-weight: 700; color: #fff; }
    
    /* Form elements */
    .stSelectbox label, .stNumberInput label, .stCheckbox label { 
        color: #e5e7eb !important; 
        font-weight: 600 !important; 
        font-size: 0.85rem !important;
    }
    .stSelectbox > div > div { 
        background: #252542 !important; 
        border: 1px solid #3d3d5a !important; 
        border-radius: 10px !important; 
        color: #fff !important; 
    }
    .stNumberInput > div > div > input { 
        background: #252542 !important; 
        border: 1px solid #3d3d5a !important; 
        border-radius: 10px !important; 
        color: #fff !important; 
    }
    .stTextArea textarea { 
        background: #252542 !important; 
        border: 1px solid #3d3d5a !important; 
        border-radius: 10px !important; 
        color: #fff !important; 
        caret-color: #10b981 !important;
        font-family: 'SF Mono', Monaco, monospace !important;
        font-size: 0.9rem !important;
    }
    .stCheckbox label span { color: #e5e7eb !important; }
    
    /* Badges */
    .rate-badge {
        background: rgba(16, 185, 129, 0.15);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 10px;
        padding: 0.75rem 1rem;
        color: #10b981;
        font-weight: 600;
        font-size: 0.9rem;
    }
    .holiday-badge {
        background: rgba(245, 158, 11, 0.15);
        border: 1px solid rgba(245, 158, 11, 0.3);
        border-radius: 10px;
        padding: 0.75rem 1rem;
        color: #f59e0b;
        font-weight: 600;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    
    /* Button */
    .stButton > button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        color: #fff !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
    }
    
    /* Results */
    .success-banner {
        background: linear-gradient(135deg, #10b981, #059669);
        border-radius: 12px;
        padding: 0.75rem;
        color: #fff;
        font-weight: 600;
        text-align: center;
        margin: 1rem 0;
        font-size: 0.95rem;
    }
    .badge { background: rgba(255,255,255,0.2); padding: 3px 8px; border-radius: 4px; font-size: 0.8rem; }
    
    .result-card {
        background: #1a1a2e;
        border: 1px solid #2d2d4a;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.75rem 0;
    }
    .shift-header { display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.75rem; padding-bottom: 0.75rem; border-bottom: 1px solid #2d2d4a; }
    .shift-title { font-size: 0.95rem; font-weight: 700; color: #fff; }
    
    .breakdown-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem; margin-bottom: 0.75rem; }
    .breakdown-item { background: #252542; border-radius: 8px; padding: 0.6rem 0.75rem; }
    .breakdown-label { font-size: 0.7rem; color: #9ca3af; }
    .breakdown-value { font-size: 0.85rem; color: #fff; font-weight: 600; }
    
    .shift-total {
        background: rgba(16, 185, 129, 0.15);
        border-radius: 10px;
        padding: 0.75rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border: 1px solid rgba(16, 185, 129, 0.2);
    }
    .shift-total-label { font-weight: 600; color: #10b981; font-size: 0.9rem; }
    .shift-total-value { font-size: 1.2rem; font-weight: 800; color: #10b981; }
    
    .weekly-summary {
        background: rgba(245, 158, 11, 0.1);
        border: 1px solid rgba(245, 158, 11, 0.2);
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .weekly-title { font-size: 0.95rem; font-weight: 700; color: #f59e0b; margin-bottom: 0.5rem; }
    .weekly-stat { display: flex; justify-content: space-between; padding: 0.3rem 0; font-size: 0.85rem; }
    .weekly-label { color: #fbbf24; }
    .weekly-value { color: #f59e0b; font-weight: 600; }
    
    .overtime-warning {
        background: rgba(239, 68, 68, 0.15);
        border: 1px solid rgba(239, 68, 68, 0.3);
        border-radius: 10px;
        padding: 0.75rem;
        color: #ef4444;
        font-weight: 600;
        font-size: 0.85rem;
    }
    
    .grand-total {
        background: linear-gradient(135deg, #1e1b4b, #312e81);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        text-align: center;
    }
    .grand-total-amount { font-size: 2.5rem; font-weight: 800; color: #fff; }
    .grand-total-label { color: rgba(255,255,255,0.7); font-size: 0.9rem; margin-top: 0.25rem; }
    
    /* Fix ALL text visibility */
    h1, h2, h3, h4, h5, h6 { color: #ffffff !important; }
    .stMarkdown, .stMarkdown p, .stMarkdown span, .stMarkdown strong { color: #e5e7eb !important; }
    .stCaption, .stCaption p { color: #9ca3af !important; }
    p, span, label, div { color: #e5e7eb; }
    
    /* Slider styling */
    .stSlider label { color: #e5e7eb !important; font-weight: 600 !important; }
    .stSlider [data-testid="stTickBarMin"], .stSlider [data-testid="stTickBarMax"] { color: #9ca3af !important; }
    .stSlider [data-testid="stThumbValue"] { color: #ffffff !important; }
    .stSlider > div > div > div { color: #ffffff !important; }
    [data-baseweb="slider"] div { color: #e5e7eb !important; }
    
    /* Metric styling */
    [data-testid="stMetricLabel"] { color: #9ca3af !important; }
    [data-testid="stMetricValue"] { color: #ffffff !important; }
    [data-testid="stMetricDelta"] { color: #10b981 !important; }
    
    /* Widget labels */
    .stCheckbox label span { color: #e5e7eb !important; }
    .stRadio label { color: #e5e7eb !important; }
    
    /* Plotly chart legends */
    .js-plotly-plot .plotly .legendtext { fill: #e5e7eb !important; }
    .js-plotly-plot .plotly .gtitle { fill: #ffffff !important; }
    .js-plotly-plot .plotly .xtick text, .js-plotly-plot .plotly .ytick text { fill: #9ca3af !important; }
    
    /* Expander */
    [data-testid="stExpander"] summary span { color: #ffffff !important; }
    
    #MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# Back Button
if st.button("← Back to Home"):
    st.switch_page("app.py")

# ==========================================
# PAY CALCULATION
# ==========================================
def parse_time(time_str):
    time_str = time_str.strip().lower().replace(" ", "")
    match = re.match(r'(\d{1,2}):?(\d{2})?(am|pm)?', time_str)
    if not match: return None
    hour = int(match.group(1))
    minutes = int(match.group(2)) if match.group(2) else 0
    period = match.group(3)
    if period == 'pm' and hour != 12: hour += 12
    elif period == 'am' and hour == 12: hour = 0
    return hour + minutes / 60

def calculate_shift(shift_line, hourly_rate, is_public_holiday=False, weekly_hours_so_far=0):
    PENALTIES = {
        "mon": (1.0, "Monday"), "tue": (1.0, "Tuesday"), "wed": (1.0, "Wednesday"),
        "thu": (1.0, "Thursday"), "thur": (1.0, "Thursday"), "fri": (1.0, "Friday"),
        "sat": (1.25, "Saturday"), "sun": (1.50, "Sunday")
    }
    EVENING_START, EVENING_END, EVENING_LOADING = 18, 6, 0.25
    BREAK_THRESHOLD, BREAK_DURATION = 5, 0.5
    
    shift = shift_line.strip()
    if ':' in shift:
        parts = shift.split(':', 1)
        day = parts[0].strip().lower()
        times = parts[1].strip()
    else:
        day, times = "mon", shift
    
    day_key = day[:3]
    if is_public_holiday:
        day_multiplier = 2.5
        day_name = PENALTIES.get(day_key, (1.0, "Weekday"))[1] + " (PH)"
    else:
        day_multiplier, day_name = PENALTIES.get(day_key, (1.0, "Weekday"))
    
    time_parts = times.replace('–', '-').replace('—', '-').split('-')
    start_time = time_parts[0].strip() if len(time_parts) >= 2 else "9am"
    end_time = time_parts[1].strip() if len(time_parts) >= 2 else "5pm"
    
    start, end = parse_time(start_time), parse_time(end_time)
    
    if start is None or end is None:
        raw_hours, evening_hours = 8, 0
    else:
        if end <= start: end += 24
        raw_hours = end - start
        evening_hours = sum(1 for h in range(int(start), int(start + raw_hours)) if (h % 24) >= EVENING_START or (h % 24) < EVENING_END)
    
    day_hours = raw_hours - evening_hours
    break_deducted = BREAK_DURATION if raw_hours >= BREAK_THRESHOLD else 0
    paid_hours = raw_hours - break_deducted
    
    if raw_hours > 0:
        day_hours_paid = day_hours * (paid_hours / raw_hours)
        evening_hours_paid = evening_hours * (paid_hours / raw_hours)
    else:
        day_hours_paid, evening_hours_paid = day_hours, evening_hours
    
    overtime_hours, overtime_pay, regular_hours = 0, 0, paid_hours
    new_weekly_total = weekly_hours_so_far + paid_hours
    if new_weekly_total > 38:
        overtime_hours = min(paid_hours, new_weekly_total - 38)
        regular_hours = paid_hours - overtime_hours
        ot_first_3 = min(overtime_hours, 3)
        ot_after_3 = max(0, overtime_hours - 3)
        overtime_pay = (ot_first_3 * hourly_rate * 1.5) + (ot_after_3 * hourly_rate * 2.0)
    
    if regular_hours > 0 and paid_hours > 0:
        regular_day = day_hours_paid * (regular_hours / paid_hours)
        regular_evening = evening_hours_paid * (regular_hours / paid_hours)
        regular_pay = (regular_day * hourly_rate * day_multiplier) + (regular_evening * hourly_rate * day_multiplier * (1 + EVENING_LOADING))
    else:
        regular_pay = 0
    
    gross_pay = regular_pay + overtime_pay
    weekend_pct = 150 if is_public_holiday else int((day_multiplier - 1) * 100)
    
    return {
        "day": day_name, "start": start_time, "end": end_time,
        "raw_hours": raw_hours, "break_deducted": break_deducted, "paid_hours": paid_hours,
        "day_hours": day_hours_paid, "evening_hours": evening_hours_paid,
        "overtime_hours": overtime_hours, "hourly_rate": hourly_rate,
        "weekend_pct": weekend_pct, "is_public_holiday": is_public_holiday,
        "overtime_pay": overtime_pay, "gross_pay": gross_pay
    }

async def process_shifts(shifts, hourly_rate, is_public_holiday):
    results, weekly_hours = [], 0
    for shift in shifts:
        calc = calculate_shift(shift, hourly_rate, is_public_holiday, weekly_hours)
        weekly_hours += calc['paid_hours']
        results.append({"shift": shift, "calc": calc})
    return results, weekly_hours

# ==========================================
# UI
# ==========================================
st.markdown("""
<div class="hero">
    <h1>💰 Payslip Calculator</h1>
    <p>Fair Work compliant • Retail Award 2024-25</p>
</div>
""", unsafe_allow_html=True)

# Employment Details
st.markdown('<div class="card"><div class="card-header"><span class="card-icon">⚙️</span><span class="card-title">Employment Details</span></div></div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    employment_type = st.selectbox("Employment Type", ["Casual", "Part-time"])
with col2:
    default_rate = 32.06 if employment_type == "Casual" else 25.65
    hourly_rate = st.number_input("Hourly Rate ($)", 15.0, 100.0, default_rate, 0.01, "%.2f")

is_public_holiday = st.checkbox("🎉 Public Holiday shifts (2.5x rate)")

rate_text = f"${hourly_rate:.2f}/hr {'(+25% casual loading)' if employment_type == 'Casual' else ''}"
st.markdown(f'<div class="rate-badge">💰 {rate_text}</div>', unsafe_allow_html=True)
if is_public_holiday:
    st.markdown('<div class="holiday-badge">🎉 Public Holiday: 2.5x penalty (+150%)</div>', unsafe_allow_html=True)

# Shifts
st.markdown('<div class="card"><div class="card-header"><span class="card-icon">📋</span><span class="card-title">Enter Shifts</span></div></div>', unsafe_allow_html=True)

query = st.text_area("shifts", "Mon: 9am-5pm\nTue: 9am-5pm\nWed: 9am-5pm\nThu: 9am-5pm\nFri: 9am-5pm\nSat: 10am-6pm", height=130, label_visibility="collapsed")

if st.button("🚀 Generate Payslip", use_container_width=True):
    if query.strip():
        shifts = [s.strip() for s in query.split('\n') if s.strip()]
        results, weekly_hours = asyncio.run(process_shifts(shifts, hourly_rate, is_public_holiday))
        
        total_paid = sum(r['calc']['paid_hours'] for r in results)
        total_ot = sum(r['calc']['overtime_hours'] for r in results)
        total_breaks = sum(r['calc']['break_deducted'] for r in results)
        total_pay = sum(r['calc']['gross_pay'] for r in results)
        total_ot_pay = sum(r['calc']['overtime_pay'] for r in results)
        
        st.markdown(f'<div class="success-banner">✅ Payslip Generated! <span class="badge">{employment_type}</span></div>', unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="weekly-summary">
            <div class="weekly-title">📊 Weekly Summary</div>
            <div class="weekly-stat"><span class="weekly-label">Raw Hours</span><span class="weekly-value">{sum(r['calc']['raw_hours'] for r in results):.1f}h</span></div>
            <div class="weekly-stat"><span class="weekly-label">Breaks</span><span class="weekly-value">-{total_breaks:.1f}h</span></div>
            <div class="weekly-stat"><span class="weekly-label">Paid Hours</span><span class="weekly-value">{total_paid:.1f}h</span></div>
            <div class="weekly-stat"><span class="weekly-label">Overtime</span><span class="weekly-value">{total_ot:.1f}h</span></div>
        </div>
        """, unsafe_allow_html=True)
        
        if total_ot > 0:
            st.markdown(f'<div class="overtime-warning">⚠️ Overtime: {total_ot:.1f}h = ${total_ot_pay:.2f}</div>', unsafe_allow_html=True)
        
        for r in results:
            c = r['calc']
            penalties = []
            if c['is_public_holiday']: penalties.append("+150%")
            elif c['weekend_pct'] > 0: penalties.append(f"+{c['weekend_pct']}%")
            if c['evening_hours'] > 0: penalties.append("+25% eve")
            penalty_text = " ".join(penalties) if penalties else "Standard"
            
            st.markdown(f"""
            <div class="result-card">
                <div class="shift-header"><span class="shift-title">📅 {c['day']}: {c['start']} → {c['end']}</span></div>
                <div class="breakdown-grid">
                    <div class="breakdown-item"><div class="breakdown-label">⏱️ Paid</div><div class="breakdown-value">{c['paid_hours']:.1f}h</div></div>
                    <div class="breakdown-item"><div class="breakdown-label">🌞 Day</div><div class="breakdown-value">{c['day_hours']:.1f}h</div></div>
                    <div class="breakdown-item"><div class="breakdown-label">🌙 Evening</div><div class="breakdown-value">{c['evening_hours']:.1f}h</div></div>
                    <div class="breakdown-item"><div class="breakdown-label">📈 Load</div><div class="breakdown-value">{penalty_text}</div></div>
                </div>
                <div class="shift-total"><span class="shift-total-label">💰 Total</span><span class="shift-total-value">${c['gross_pay']:.2f}</span></div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="grand-total">
            <div class="grand-total-amount">${total_pay:.2f}</div>
            <div class="grand-total-label">{total_paid:.1f}h • {employment_type}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.session_state['last_pay'] = total_pay
        set_setting('last_pay', str(total_pay), user_id)
        
        # Save to payslip history
        shifts_data = []
        for r in results:
            c = r['calc']
            shifts_data.append({
                'day': c['day'], 'start': c['start'], 'end': c['end'],
                'paid_hours': c['paid_hours'], 'day_hours': c['day_hours'],
                'evening_hours': c['evening_hours'], 'overtime_hours': c['overtime_hours'],
                'gross_pay': c['gross_pay'],
            })
        save_payslip(employment_type, hourly_rate, total_paid, total_ot, total_pay, shifts_data, user_id)

# ==========================================
# PAYSLIP HISTORY
# ==========================================
st.markdown("---")

col_title, col_clear = st.columns([3, 1])
with col_title:
    st.markdown("### 📜 Payslip History")
with col_clear:
    if st.button("🗑️ Clear All", use_container_width=True):
        clear_payslip_history(user_id)
        st.rerun()

history = get_payslip_history(user_id)

if history:
    for entry in history:
        # Parse date
        from datetime import datetime
        try:
            dt = datetime.fromisoformat(entry['calculated_at'].replace('Z', '+00:00'))
            date_str = dt.strftime('%d %b %Y, %I:%M %p')
        except:
            date_str = entry['calculated_at'][:16]
        
        with st.expander(f"💰 ${entry['total_pay']:.2f} — {date_str} • {entry['employment_type']}"):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Pay", f"${entry['total_pay']:.2f}")
            with col2:
                st.metric("Hours Worked", f"{entry['total_hours']:.1f}h")
            with col3:
                st.metric("Rate", f"${entry['hourly_rate']:.2f}/hr")
            
            if entry.get('overtime_hours', 0) > 0:
                st.markdown(f"⚠️ Overtime: **{entry['overtime_hours']:.1f}h**")
            
            # Show shift breakdown
            import json
            shifts = json.loads(entry['shifts_data']) if isinstance(entry['shifts_data'], str) else entry['shifts_data']
            if shifts:
                st.markdown("**Shift Breakdown:**")
                for s in shifts:
                    st.markdown(f"📅 **{s['day']}**: {s['start']} → {s['end']} — {s['paid_hours']:.1f}h — **${s['gross_pay']:.2f}**")
            
            st.markdown("---")
            if st.button(f"🗑️ Delete this payslip", key=f"del_payslip_{entry['id']}"):
                delete_payslip(entry['id'])
                st.rerun()
else:
    st.info("No payslip history yet. Generate your first payslip above! ☝️")

