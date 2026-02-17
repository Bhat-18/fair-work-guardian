import streamlit as st

st.set_page_config(
    page_title="Fair Work Guardian",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==========================================
# CSS - Dark Theme (matching all pages)
# ==========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    .stApp {
        background: linear-gradient(180deg, #0a0a0f 0%, #1a1a2e 100%);
        font-family: 'Inter', -apple-system, sans-serif;
    }
    
    .main .block-container {
        padding: 2rem 1rem;
        max-width: 900px;
    }
    
    /* Hide sidebar completely */
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="stSidebarNav"] { display: none !important; }
    section[data-testid="stSidebar"] { display: none !important; }
    button[kind="header"] { display: none !important; }
    
    /* Make all headings visible */
    h1, h2, h3, h4, h5, h6 { color: #ffffff !important; }
    .stMarkdown p, .stMarkdown span { color: #e5e7eb !important; }
    
    /* Hero */
    .hero {
        text-align: center;
        padding: 3rem 2rem;
        margin-bottom: 2.5rem;
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #a855f7 100%);
        border-radius: 24px;
        box-shadow: 0 20px 60px rgba(79, 70, 229, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .hero::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.05'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
        opacity: 0.5;
    }
    
    .hero h1 {
        font-size: 2.75rem;
        font-weight: 800;
        color: #ffffff;
        margin: 0;
        letter-spacing: -0.02em;
        position: relative;
        z-index: 1;
    }
    
    .hero p {
        color: rgba(255,255,255,0.9);
        font-size: 1.15rem;
        margin-top: 0.75rem;
        font-weight: 500;
        position: relative;
        z-index: 1;
    }
    
    /* Feature Cards */
    .feature-card {
        background: linear-gradient(145deg, #1e1e2f 0%, #2a2a40 100%);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 20px;
        padding: 1.75rem;
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(0,0,0,0.4);
        border-color: rgba(79, 70, 229, 0.3);
    }
    
    .card-icon {
        font-size: 2.25rem;
        margin-bottom: 1rem;
    }
    
    .card-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 0.5rem;
    }
    
    .card-desc {
        color: #9ca3af;
        font-size: 0.9rem;
        line-height: 1.5;
    }
    
    /* Streamlit button styling */
    .stButton > button {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(79, 70, 229, 0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(79, 70, 229, 0.4) !important;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: #6b7280;
        padding: 2rem 0;
        font-size: 0.85rem;
    }
    
    .footer strong { color: #9ca3af; }
    
    #MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# HERO
# ==========================================
st.markdown("""
<div class="hero">
    <h1>🛡️ Fair Work Guardian</h1>
    <p>Your Complete Financial Wellness Platform</p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# FEATURE CARDS - Row 1
# ==========================================
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="card-icon">💰</div>
        <div class="card-title">Payslip Calculator</div>
        <div class="card-desc">Calculate your pay with penalty rates, overtime, public holidays & break deductions.</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Open Payslip", key="btn_payslip", use_container_width=True):
        st.switch_page("pages/1_💰_Payslip_Calculator.py")

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="card-icon">📈</div>
        <div class="card-title">Investment Portfolio</div>
        <div class="card-desc">Track investments across US, India & Australia markets with live data.</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Open Portfolio", key="btn_portfolio", use_container_width=True):
        st.switch_page("pages/2_📈_Investment_Portfolio.py")

# ==========================================
# FEATURE CARDS - Row 2
# ==========================================
col3, col4 = st.columns(2)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="card-icon">📊</div>
        <div class="card-title">Market Dashboard</div>
        <div class="card-desc">Live prices from S&P 500, NIFTY, ASX 200 and more indices.</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Open Markets", key="btn_markets", use_container_width=True):
        st.switch_page("pages/3_📊_Market_Dashboard.py")

with col4:
    st.markdown("""
    <div class="feature-card">
        <div class="card-icon">🎯</div>
        <div class="card-title">Savings Goals</div>
        <div class="card-desc">Set goals, track progress & see your money grow with compound interest.</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Open Goals", key="btn_goals", use_container_width=True):
        st.switch_page("pages/5_🎯_Savings_Goals.py")

# ==========================================
# FOOTER
# ==========================================
st.markdown("""
<div class="footer">
    <p><strong>Fair Work Guardian</strong> • Built for Australian Workers</p>
    <p>Retail Award 2024-25 • Real-time data via Yahoo Finance</p>
</div>
""", unsafe_allow_html=True)