import streamlit as st
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db import get_goals, add_goal as db_add_goal, update_goal_saved, get_setting, set_setting
from session import get_user_id

user_id = get_user_id()

st.set_page_config(page_title="Savings Goals", layout="centered", page_icon="🎯", initial_sidebar_state="collapsed")

# ==========================================
# CSS
# ==========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    .stApp { background: linear-gradient(180deg, #0a0a0f 0%, #1a1a2e 100%); font-family: 'Inter', sans-serif; }
    .main .block-container { padding: 1.5rem; max-width: 800px; }
    
    /* Hide sidebar */
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="stSidebarNav"] { display: none !important; }
    section[data-testid="stSidebar"] { display: none !important; }
    button[kind="header"] { display: none !important; }
    
    .hero { text-align: center; padding: 1.5rem; margin-bottom: 1.5rem; background: linear-gradient(135deg, #a855f7, #7c3aed); border-radius: 16px; }
    .hero h1 { font-size: 1.75rem; font-weight: 800; color: #fff; margin: 0; }
    .hero p { color: rgba(255,255,255,0.9); margin-top: 0.25rem; font-size: 0.9rem; }
    
    /* Fix ALL text visibility */
    h1, h2, h3, h4, h5, h6 { color: #ffffff !important; }
    .stMarkdown, .stMarkdown h3, .stMarkdown p, .stMarkdown span, .stMarkdown strong { color: #e5e7eb !important; }
    .stCaption, .stCaption p { color: #9ca3af !important; }
    p, span, label, div { color: #e5e7eb; }
    
    /* Slider styling */
    .stSlider label { color: #e5e7eb !important; font-weight: 600 !important; font-size: 0.85rem !important; }
    .stSlider [data-testid="stTickBarMin"], .stSlider [data-testid="stTickBarMax"] { color: #9ca3af !important; }
    .stSlider [data-testid="stThumbValue"] { color: #ffffff !important; }
    .stSlider > div > div > div { color: #ffffff !important; }
    [data-baseweb="slider"] div { color: #e5e7eb !important; }
    
    /* Metric styling */
    [data-testid="stMetricLabel"] { color: #9ca3af !important; }
    [data-testid="stMetricValue"] { color: #ffffff !important; }
    [data-testid="stMetricDelta"] { color: #10b981 !important; }
    
    /* All widget labels */
    .stCheckbox label span { color: #e5e7eb !important; }
    .stRadio label { color: #e5e7eb !important; }
    .stMultiSelect label { color: #e5e7eb !important; }
    
    /* Plotly chart legends */
    .js-plotly-plot .plotly .legendtext { fill: #e5e7eb !important; }
    .js-plotly-plot .plotly .gtitle { fill: #ffffff !important; }
    .js-plotly-plot .plotly .xtick text, .js-plotly-plot .plotly .ytick text { fill: #9ca3af !important; }
    
    /* Expander */
    .streamlit-expanderHeader { color: #ffffff !important; }
    [data-testid="stExpander"] summary span { color: #ffffff !important; }
    
    .goal-card { background: #1a1a2e; border: 1px solid #2d2d4a; border-radius: 14px; padding: 1.25rem; margin: 0.75rem 0; }
    .goal-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem; }
    .goal-title { font-size: 1.1rem; font-weight: 700; color: #fff; }
    .goal-amount { color: #9ca3af; font-size: 0.85rem; }
    
    .goal-progress { background: #252542; border-radius: 8px; height: 12px; overflow: hidden; margin: 0.5rem 0; }
    .goal-bar { height: 100%; border-radius: 8px; }
    
    .goal-stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.5rem; margin-top: 0.75rem; }
    .goal-stat { text-align: center; padding: 0.5rem; background: #252542; border-radius: 8px; }
    .goal-stat-value { font-size: 1rem; font-weight: 700; color: #fff; }
    .goal-stat-label { font-size: 0.7rem; color: #9ca3af; }
    
    .calc-box { background: #1a1a2e; border: 1px solid #2d2d4a; border-radius: 14px; padding: 1.25rem; margin: 1rem 0; }
    .calc-result { background: linear-gradient(135deg, #10b981, #059669); border-radius: 12px; padding: 1.25rem; text-align: center; margin-top: 0.75rem; }
    .calc-amount { font-size: 2rem; font-weight: 800; color: #fff; }
    .calc-label { color: rgba(255,255,255,0.8); font-size: 0.85rem; }
    
    .stSelectbox label, .stNumberInput label, .stTextInput label, .stSlider label { color: #e5e7eb !important; font-weight: 600 !important; font-size: 0.85rem !important; }
    .stSelectbox > div > div, .stTextInput > div > div > input { background: #252542 !important; border: 1px solid #3d3d5a !important; border-radius: 8px !important; color: #fff !important; }
    .stNumberInput > div > div > input { background: #252542 !important; border: 1px solid #3d3d5a !important; border-radius: 8px !important; color: #fff !important; }
    .stButton > button { background: linear-gradient(135deg, #a855f7, #7c3aed) !important; color: #fff !important; border: none !important; border-radius: 8px !important; font-weight: 700 !important; }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] { background: #1a1a2e; border-radius: 10px; padding: 0.5rem; }
    .stTabs [data-baseweb="tab"] { color: #ffffff !important; font-weight: 700 !important; background: #252542 !important; border-radius: 8px !important; padding: 0.5rem 1rem !important; }
    .stTabs [aria-selected="true"] { background: linear-gradient(135deg, #a855f7, #7c3aed) !important; }
    
    #MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# Back Button
if st.button("← Back to Home"):
    st.switch_page("app.py")

# ==========================================
# GOALS DATA (from Supabase)
# ==========================================
if 'goals' not in st.session_state:
    db_goals = get_goals(user_id)
    if db_goals is not None:
        st.session_state.goals = db_goals
    else:
        st.session_state.goals = [
            {"name": "Emergency Fund", "target": 5000, "saved": 2500, "icon": "🛡️", "weekly": 100, "color": "#10b981"},
            {"name": "House Deposit", "target": 50000, "saved": 12000, "icon": "🏠", "weekly": 200, "color": "#4f46e5"},
            {"name": "Holiday Trip", "target": 3000, "saved": 800, "icon": "✈️", "weekly": 50, "color": "#f59e0b"},
        ]

# ==========================================
# UI
# ==========================================
st.markdown("""
<div class="hero">
    <h1>🎯 Savings Goals</h1>
    <p>Track goals & watch your money grow</p>
</div>
""", unsafe_allow_html=True)

# User-editable Total Savings Target
st.markdown("### 💰 Your Savings Overview")

# Initialize user's total goal if not set
if 'user_total_goal' not in st.session_state:
    st.session_state.user_total_goal = float(get_setting('total_goal', user_id, '100000'))

if 'user_total_saved' not in st.session_state:
    st.session_state.user_total_saved = float(get_setting('total_saved', user_id, str(sum(g['saved'] for g in st.session_state.goals))))

col1, col2 = st.columns(2)
with col1:
    user_total_goal = st.number_input(
        "🎯 Your Total Savings Goal ($)", 
        min_value=1000.0, 
        max_value=10000000.0,
        value=float(st.session_state.user_total_goal),
        step=1000.0,
        help="Set your overall savings target"
    )
    if user_total_goal != st.session_state.user_total_goal:
        st.session_state.user_total_goal = float(user_total_goal)
        set_setting('total_goal', str(user_total_goal), user_id)

with col2:
    user_total_saved = st.number_input(
        "💵 Total Saved So Far ($)", 
        min_value=0.0, 
        max_value=10000000.0,
        value=float(st.session_state.user_total_saved),
        step=100.0,
        help="Enter how much you've saved in total"
    )
    if user_total_saved != st.session_state.user_total_saved:
        st.session_state.user_total_saved = float(user_total_saved)
        set_setting('total_saved', str(user_total_saved), user_id)

# Calculate progress from user inputs
progress = (st.session_state.user_total_saved / st.session_state.user_total_goal * 100) if st.session_state.user_total_goal > 0 else 0
remaining = st.session_state.user_total_goal - st.session_state.user_total_saved

# Show progress bar and stats
st.markdown(f"""
<div class="goal-card">
    <div class="goal-header">
        <span class="goal-title">📊 Overall Progress</span>
        <span class="goal-amount">${st.session_state.user_total_saved:,.0f} / ${st.session_state.user_total_goal:,.0f}</span>
    </div>
    <div class="goal-progress"><div class="goal-bar" style="width: {min(progress, 100)}%; background: linear-gradient(90deg, #a855f7, #10b981);"></div></div>
    <div class="goal-stats">
        <div class="goal-stat"><div class="goal-stat-value" style="color: #10b981;">{progress:.1f}%</div><div class="goal-stat-label">Progress</div></div>
        <div class="goal-stat"><div class="goal-stat-value" style="color: #f59e0b;">${remaining:,.0f}</div><div class="goal-stat-label">Remaining</div></div>
        <div class="goal-stat"><div class="goal-stat-value" style="color: #a855f7;">${st.session_state.user_total_saved:,.0f}</div><div class="goal-stat-label">Saved</div></div>
    </div>
</div>
""", unsafe_allow_html=True)

# Goals
st.markdown("### 📋 Your Goals")

for i, g in enumerate(st.session_state.goals):
    pct = (g['saved'] / g['target'] * 100) if g['target'] > 0 else 0
    remaining = g['target'] - g['saved']
    weeks = remaining / g['weekly'] if g['weekly'] > 0 else 0
    
    st.markdown(f"""
    <div class="goal-card">
        <div class="goal-header">
            <span class="goal-title">{g['icon']} {g['name']}</span>
            <span class="goal-amount">${g['saved']:,.0f} / ${g['target']:,.0f}</span>
        </div>
        <div class="goal-progress"><div class="goal-bar" style="width: {min(pct, 100)}%; background: {g['color']};"></div></div>
        <div class="goal-stats">
            <div class="goal-stat"><div class="goal-stat-value">{pct:.0f}%</div><div class="goal-stat-label">Progress</div></div>
            <div class="goal-stat"><div class="goal-stat-value">${remaining:,.0f}</div><div class="goal-stat-label">Remaining</div></div>
            <div class="goal-stat"><div class="goal-stat-value">{weeks:.0f}w</div><div class="goal-stat-label">@ ${g['weekly']}/wk</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    add_amt = st.number_input(f"Add to {g['name']}", min_value=0.0, value=0.0, step=10.0, key=f"add_{i}")
    if st.button(f"➕ Add ${add_amt:.0f}", key=f"btn_{i}", use_container_width=True):
        st.session_state.goals[i]['saved'] += add_amt
        if 'db_id' in g:
            update_goal_saved(g['db_id'], st.session_state.goals[i]['saved'])
        st.rerun()

# New Goal
st.markdown("---")
st.markdown("### ➕ New Goal")

c1, c2 = st.columns(2)
with c1:
    new_name = st.text_input("Name", placeholder="New Car")
    new_icon = st.selectbox("Icon", ["🎯", "🚗", "🏠", "✈️", "💻", "📱", "🎓", "💍", "🛡️"])
with c2:
    new_target = st.number_input("Target ($)", min_value=100.0, value=5000.0, step=100.0)
    new_weekly = st.number_input("Weekly ($)", min_value=10.0, value=100.0, step=10.0)

if st.button("🎯 Create Goal", use_container_width=True):
    if new_name:
        new_goal = {"name": new_name, "target": new_target, "saved": 0, "icon": new_icon, "weekly": new_weekly, "color": "#a855f7"}
        db_add_goal(new_goal, user_id)
        st.session_state.goals.append(new_goal)
        st.success(f"Created: {new_name}!")
        st.rerun()

# Calculator
st.markdown("---")
st.markdown('<div class="calc-box">', unsafe_allow_html=True)
st.markdown("### 📈 Compound Calculator")

c1, c2 = st.columns(2)
with c1:
    weekly = st.number_input("Weekly ($)", 50.0, 1000.0, 100.0, 10.0, key="calc_weekly")
    rate = st.slider("Annual Return (%)", 1, 15, 7)
with c2:
    years = st.slider("Years", 1, 30, 10)

# Calculate
total_contrib = weekly * 52 * years
weekly_rate = rate / 100 / 52
weeks = years * 52
fv = weekly * (((1 + weekly_rate) ** weeks - 1) / weekly_rate) if weekly_rate > 0 else total_contrib
interest = fv - total_contrib

st.markdown(f"""
<div class="calc-result">
    <div class="calc-amount">${fv:,.0f}</div>
    <div class="calc-label">After {years} years</div>
    <div style="margin-top: 0.5rem; font-size: 0.85rem; color: rgba(255,255,255,0.7);">
        Contributions: ${total_contrib:,.0f} • Interest: ${interest:,.0f}
    </div>
</div>
""", unsafe_allow_html=True)

# Chart
yrs = list(range(1, years + 1))
contribs, values = [], []
for y in yrs:
    c = weekly * 52 * y
    v = weekly * (((1 + weekly_rate) ** (y * 52) - 1) / weekly_rate) if weekly_rate > 0 else c
    contribs.append(c)
    values.append(v)

fig = go.Figure()
fig.add_trace(go.Scatter(x=yrs, y=contribs, name='Contributions', fill='tozeroy', line=dict(color='#4f46e5'), fillcolor='rgba(79,70,229,0.3)'))
fig.add_trace(go.Scatter(x=yrs, y=values, name='Total', fill='tonexty', line=dict(color='#10b981'), fillcolor='rgba(16,185,129,0.3)'))
fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#fff', xaxis=dict(showgrid=False, title="Years"), yaxis=dict(showgrid=True, gridcolor='#2d2d4a'), legend=dict(orientation="h", y=1.02, x=0.5, xanchor="center"), height=300, margin=dict(t=40, b=20))
st.plotly_chart(fig, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)
