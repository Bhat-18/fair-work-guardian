import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import yfinance as yf
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db import get_portfolio, add_holding as db_add_holding, delete_holding as db_delete_holding, get_setting

st.set_page_config(page_title="Investment Portfolio", layout="wide", page_icon="📈", initial_sidebar_state="collapsed")

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
    .main .block-container { padding: 1.5rem; max-width: 1100px; }
    
    /* Hide sidebar */
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="stSidebarNav"] { display: none !important; }
    section[data-testid="stSidebar"] { display: none !important; }
    button[kind="header"] { display: none !important; }
    
    .hero { text-align: center; padding: 1.5rem; margin-bottom: 1.5rem; background: linear-gradient(135deg, #4f46e5, #7c3aed); border-radius: 16px; }
    .hero h1 { font-size: 1.75rem; font-weight: 800; color: #fff; margin: 0; }
    .hero p { color: rgba(255,255,255,0.9); margin-top: 0.25rem; font-size: 0.9rem; }
    
    .card { background: #1a1a2e; border: 1px solid #2d2d4a; border-radius: 14px; padding: 1.25rem; margin-bottom: 1rem; }
    .card-title { font-size: 1rem; font-weight: 700; color: #fff; margin-bottom: 0.75rem; }
    
    .metric-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.75rem; margin: 1rem 0; }
    .metric-card { background: #1a1a2e; border: 1px solid #2d2d4a; border-radius: 10px; padding: 1rem; text-align: center; }
    .metric-value { font-size: 1.25rem; font-weight: 800; }
    .metric-label { font-size: 0.75rem; color: #9ca3af; margin-top: 0.15rem; }
    .positive { color: #10b981; }
    .negative { color: #ef4444; }
    
    .suggest-box { background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 12px; padding: 1rem; margin: 1rem 0; }
    .suggest-title { font-size: 0.9rem; font-weight: 700; color: #10b981; }
    .suggest-amount { font-size: 1.5rem; font-weight: 800; color: #fff; }
    
    .stSelectbox label, .stNumberInput label, .stTextInput label { color: #e5e7eb !important; font-weight: 600 !important; font-size: 0.85rem !important; }
    .stSelectbox > div > div { background: #252542 !important; border: 1px solid #3d3d5a !important; border-radius: 8px !important; color: #fff !important; }
    .stNumberInput > div > div > input, .stTextInput > div > div > input { background: #252542 !important; border: 1px solid #3d3d5a !important; border-radius: 8px !important; color: #fff !important; }
    .stButton > button { background: linear-gradient(135deg, #4f46e5, #7c3aed) !important; color: #fff !important; border: none !important; border-radius: 8px !important; font-weight: 700 !important; }
    
    /* Fix text visibility - ALL elements */
    .stMarkdown, .stMarkdown p, .stMarkdown span, .stMarkdown strong, .stMarkdown h3 { color: #ffffff !important; }
    .stCaption, .stCaption p { color: #9ca3af !important; }
    h1, h2, h3, h4, h5, h6 { color: #ffffff !important; }
    p, span, label, div { color: #e5e7eb; }
    hr { border-color: #2d2d4a !important; }
    
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
    
    /* Plotly chart legends and text */
    .js-plotly-plot .plotly .legendtext { fill: #e5e7eb !important; }
    .js-plotly-plot .plotly .gtitle { fill: #ffffff !important; }
    .js-plotly-plot .plotly .xtick text, .js-plotly-plot .plotly .ytick text { fill: #9ca3af !important; }
    
    /* Expander */
    .streamlit-expanderHeader { color: #ffffff !important; }
    [data-testid="stExpander"] summary span { color: #ffffff !important; }
    
    /* Table */
    .stDataFrame { color: #ffffff !important; }
    .stTable td, .stTable th { color: #e5e7eb !important; }
    
    /* Holdings card */
    .holding-card {
        background: #1e1e30;
        border: 1px solid #2d2d4a;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 0.75rem;
    }
    .holding-header { display: flex; justify-content: space-between; align-items: flex-start; }
    .holding-info { flex: 1; }
    .holding-symbol { font-size: 1.1rem; font-weight: 700; color: #ffffff; }
    .holding-name { color: #9ca3af; font-size: 0.85rem; margin-left: 0.5rem; }
    .holding-region { background: #4f46e5; color: #fff; padding: 2px 8px; border-radius: 4px; font-size: 0.7rem; margin-left: 0.5rem; }
    .holding-details { color: #d1d5db; font-size: 0.85rem; margin-top: 0.5rem; }
    .holding-value { text-align: right; }
    .holding-amount { font-size: 1.25rem; font-weight: 700; color: #ffffff; }
    .holding-pct { font-size: 0.9rem; margin-top: 0.25rem; }
    
    #MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# Back Button
if st.button("← Back to Home"):
    st.switch_page("app.py")

# ==========================================
# PORTFOLIO DATA (from Supabase)
# ==========================================
if 'portfolio' not in st.session_state:
    db_data = get_portfolio()
    if db_data is not None:
        st.session_state.portfolio = db_data
    else:
        st.session_state.portfolio = [
            {"symbol": "SPY", "name": "S&P 500 ETF", "shares": 5, "avg_cost": 450.00, "region": "🇺🇸 US"},
            {"symbol": "VAS.AX", "name": "Vanguard ASX 300", "shares": 20, "avg_cost": 95.00, "region": "🇦🇺 AU"},
            {"symbol": "QQQ", "name": "NASDAQ 100 ETF", "shares": 3, "avg_cost": 380.00, "region": "🇺🇸 US"},
        ]

# ==========================================
# UI
# ==========================================
st.markdown("""
<div class="hero">
    <h1>📈 Investment Portfolio</h1>
    <p>Track investments across global markets</p>
</div>
""", unsafe_allow_html=True)

# Investment Suggestion
last_pay = float(get_setting('last_pay', '1000'))

col1, col2 = st.columns([2, 1])
with col1:
    invest_pct = st.slider("💵 Invest % of your pay", min_value=1, max_value=50, value=10, step=1, help="Choose what percentage of your payslip to invest")
with col2:
    st.markdown(f"""
    <div style="background: #252542; border-radius: 10px; padding: 1rem; text-align: center; margin-top: 1.5rem;">
        <div style="color: #10b981; font-size: 1.5rem; font-weight: 800;">{invest_pct}%</div>
        <div style="color: #9ca3af; font-size: 0.75rem;">of pay</div>
    </div>
    """, unsafe_allow_html=True)

invest_amount = last_pay * (invest_pct / 100)

st.markdown(f"""
<div class="suggest-box">
    <div class="suggest-title">💡 Suggested from Last Payslip</div>
    <div class="suggest-amount">${invest_amount:.2f}</div>
    <span style="color: #9ca3af; font-size: 0.85rem;">From ${last_pay:.2f} × {invest_pct}%</span>
</div>
""", unsafe_allow_html=True)

# Fetch prices
@st.cache_data(ttl=300)
def get_prices(symbols):
    prices = {}
    for sym in symbols:
        try:
            ticker = yf.Ticker(sym)
            hist = ticker.history(period="1d")
            prices[sym] = hist['Close'].iloc[-1] if len(hist) > 0 else 0
        except:
            prices[sym] = 0
    return prices

if st.session_state.portfolio:
    symbols = [h['symbol'] for h in st.session_state.portfolio]
    with st.spinner("📊 Fetching prices..."):
        prices = get_prices(symbols)
    
    # Calculate values
    total_value, total_cost = 0, 0
    holdings_data = []
    
    for h in st.session_state.portfolio:
        current_price = prices.get(h['symbol'], h['avg_cost'])
        if current_price == 0:
            current_price = h['avg_cost']  # Fallback to cost if price fetch fails
        value = h['shares'] * current_price
        cost = h['shares'] * h['avg_cost']
        gain = value - cost
        gain_pct = ((current_price / h['avg_cost']) - 1) * 100 if h['avg_cost'] > 0 else 0
        total_value += value
        total_cost += cost
        holdings_data.append({
            "Symbol": h['symbol'], 
            "Name": h['name'], 
            "Region": h['region'], 
            "Shares": h['shares'], 
            "AvgCost": h['avg_cost'],
            "Price": current_price, 
            "Value": value, 
            "Gain": gain, 
            "Pct": gain_pct
        })
    
    total_gain = total_value - total_cost
    total_pct = ((total_value / total_cost) - 1) * 100 if total_cost > 0 else 0
    
    # Metrics
    st.markdown(f"""
    <div class="metric-grid">
        <div class="metric-card"><div class="metric-value" style="color: #4f46e5;">${total_value:,.0f}</div><div class="metric-label">Portfolio Value</div></div>
        <div class="metric-card"><div class="metric-value" style="color: #9ca3af;">${total_cost:,.0f}</div><div class="metric-label">Total Invested</div></div>
        <div class="metric-card"><div class="metric-value {'positive' if total_gain >= 0 else 'negative'}">${total_gain:+,.0f}</div><div class="metric-label">Gain/Loss</div></div>
        <div class="metric-card"><div class="metric-value {'positive' if total_pct >= 0 else 'negative'}">{total_pct:+.1f}%</div><div class="metric-label">Return</div></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="card"><div class="card-title">📊 Allocation by Region</div></div>', unsafe_allow_html=True)
        region_values = {}
        for h in holdings_data:
            r = h['Region']
            region_values[r] = region_values.get(r, 0) + h['Value']
        
        if region_values:
            fig_pie = px.pie(names=list(region_values.keys()), values=list(region_values.values()), 
                             color_discrete_sequence=['#4f46e5', '#10b981', '#f59e0b', '#ef4444'], hole=0.45)
            fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#fff', 
                                  showlegend=True, legend=dict(orientation="h", y=-0.1, font=dict(color='#e5e7eb', size=12)), margin=dict(t=20, b=20, l=20, r=20), height=280)
            st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        st.markdown('<div class="card"><div class="card-title">📈 Performance by Holding</div></div>', unsafe_allow_html=True)
        if holdings_data:
            df = pd.DataFrame(holdings_data)
            colors = ['#10b981' if x >= 0 else '#ef4444' for x in df['Pct']]
            fig_bar = go.Figure(go.Bar(x=df['Symbol'], y=df['Pct'], marker_color=colors, text=[f"{x:+.1f}%" for x in df['Pct']], textposition='outside'))
            fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#fff', 
                                  xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor='#2d2d4a'), margin=dict(t=20, b=20), height=280)
            st.plotly_chart(fig_bar, use_container_width=True)
    
    # Holdings Table with Delete buttons
    st.markdown("---")
    st.markdown("### 📋 Your Holdings")
    
    for i, h in enumerate(holdings_data):
        pct_color = "#10b981" if h['Pct'] >= 0 else "#ef4444"
        
        st.markdown(f"""
        <div class="holding-card">
            <div class="holding-header">
                <div class="holding-info">
                    <span class="holding-symbol">{h['Symbol']}</span>
                    <span class="holding-name">{h['Name']}</span>
                    <span class="holding-region">{h['Region']}</span>
                    <div class="holding-details">{h['Shares']} shares @ ${h['AvgCost']:.2f} → ${h['Price']:.2f}</div>
                </div>
                <div class="holding-value">
                    <div class="holding-amount">${h['Value']:,.0f}</div>
                    <div class="holding-pct" style="color: {pct_color};">{h['Pct']:+.1f}%</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"🗑️ Remove {h['Symbol']}", key=f"del_{i}"):
            db_delete_holding(h['Symbol'])
            st.session_state.portfolio.pop(i)
            st.rerun()
    
    # Historical Chart
    st.markdown("---")
    st.markdown("### 📈 Historical Performance (30 Days)")
    
    # Create a list of symbol options with names for better display
    symbol_list = [h['symbol'] for h in st.session_state.portfolio]
    symbol_names = {h['symbol']: h.get('name', h['symbol']) for h in st.session_state.portfolio}
    
    selected = st.selectbox(
        "Select holding to view", 
        symbol_list,
        format_func=lambda x: f"{x} - {symbol_names.get(x, x)}",
        key="historical_chart_selector"
    )
    
    # Fetch historical data - cache with symbol as key
    @st.cache_data(ttl=300, show_spinner=False)
    def get_history(symbol: str):
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="30d")
            return hist
        except Exception as e:
            return pd.DataFrame()
    
    if selected:
        with st.spinner(f"Loading {selected} history..."):
            hist = get_history(selected)
        
        if len(hist) > 0:
            # Calculate price change for the period
            start_price = hist['Close'].iloc[0]
            end_price = hist['Close'].iloc[-1]
            change_pct = ((end_price - start_price) / start_price) * 100
            change_color = "#10b981" if change_pct >= 0 else "#ef4444"
            
            # Create the chart
            fig = go.Figure(go.Scatter(
                x=hist.index, 
                y=hist['Close'], 
                mode='lines', 
                fill='tozeroy', 
                line=dict(color='#4f46e5', width=2), 
                fillcolor='rgba(79, 70, 229, 0.2)',
                name=selected
            ))
            fig.update_layout(
                title=dict(
                    text=f"{selected} ({symbol_names.get(selected, '')}) - <span style='color:{change_color}'>{change_pct:+.1f}%</span>",
                    font=dict(size=14, color='#fff')
                ),
                paper_bgcolor='rgba(0,0,0,0)', 
                plot_bgcolor='rgba(0,0,0,0)', 
                font_color='#fff', 
                xaxis=dict(showgrid=False, title='Date'), 
                yaxis=dict(showgrid=True, gridcolor='#2d2d4a', title='Price ($)'), 
                height=350, 
                margin=dict(t=50, b=30)
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Show some stats
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("30D High", f"${hist['Close'].max():.2f}")
            col2.metric("30D Low", f"${hist['Close'].min():.2f}")
            col3.metric("Current", f"${end_price:.2f}")
            col4.metric("30D Change", f"{change_pct:+.1f}%")
        else:
            st.warning(f"⚠️ Could not fetch historical data for {selected}. The symbol may be invalid or market data unavailable.")

else:
    st.info("📭 Your portfolio is empty. Add your first holding below!")

# Add Holding Section
st.markdown("---")
st.markdown("### ➕ Add New Holding")

# Expanded stocks/ETFs by region (removed EU, added many more US/AU/IN)
POPULAR_SYMBOLS = {
    "🇺🇸 US Stocks": [
        ("AAPL", "Apple Inc."),
        ("MSFT", "Microsoft"),
        ("GOOGL", "Google (Alphabet)"),
        ("AMZN", "Amazon"),
        ("NVDA", "NVIDIA"),
        ("TSLA", "Tesla"),
        ("META", "Meta/Facebook"),
        ("BRK-B", "Berkshire Hathaway"),
        ("JPM", "JPMorgan Chase"),
        ("V", "Visa"),
        ("JNJ", "Johnson & Johnson"),
        ("UNH", "UnitedHealth"),
        ("WMT", "Walmart"),
        ("MA", "Mastercard"),
        ("PG", "Procter & Gamble"),
        ("HD", "Home Depot"),
        ("DIS", "Disney"),
        ("PYPL", "PayPal"),
        ("NFLX", "Netflix"),
        ("ADBE", "Adobe"),
        ("CRM", "Salesforce"),
        ("INTC", "Intel"),
        ("AMD", "AMD"),
        ("CSCO", "Cisco"),
        ("PEP", "PepsiCo"),
        ("KO", "Coca-Cola"),
        ("NKE", "Nike"),
        ("MCD", "McDonald's"),
        ("COST", "Costco"),
        ("BA", "Boeing"),
    ],
    "🇺🇸 US ETFs": [
        ("SPY", "S&P 500 ETF"),
        ("QQQ", "NASDAQ 100 ETF"),
        ("VTI", "Vanguard Total Market"),
        ("VOO", "Vanguard S&P 500"),
        ("VGT", "Vanguard IT"),
        ("IWM", "Russell 2000 ETF"),
        ("DIA", "Dow Jones ETF"),
        ("VYM", "Vanguard High Dividend"),
        ("SCHD", "Schwab Dividend"),
        ("ARKK", "ARK Innovation"),
        ("VNQ", "Vanguard Real Estate"),
        ("BND", "Vanguard Bond"),
        ("GLD", "Gold ETF"),
        ("SLV", "Silver ETF"),
        ("XLF", "Financial Sector ETF"),
        ("XLE", "Energy Sector ETF"),
        ("XLK", "Technology Sector ETF"),
        ("XLV", "Healthcare Sector ETF"),
    ],
    "🇦🇺 ASX Stocks": [
        ("CBA.AX", "Commonwealth Bank"),
        ("BHP.AX", "BHP Group"),
        ("CSL.AX", "CSL Limited"),
        ("WBC.AX", "Westpac"),
        ("NAB.AX", "National Australia Bank"),
        ("ANZ.AX", "ANZ Bank"),
        ("RIO.AX", "Rio Tinto"),
        ("WES.AX", "Wesfarmers"),
        ("WOW.AX", "Woolworths"),
        ("MQG.AX", "Macquarie Group"),
        ("TLS.AX", "Telstra"),
        ("FMG.AX", "Fortescue Metals"),
        ("NCM.AX", "Newcrest Mining"),
        ("WDS.AX", "Woodside Energy"),
        ("STO.AX", "Santos"),
        ("TCL.AX", "Transurban"),
        ("AMC.AX", "Amcor"),
        ("ALL.AX", "Aristocrat Leisure"),
        ("REA.AX", "REA Group"),
        ("COL.AX", "Coles Group"),
        ("JHX.AX", "James Hardie"),
        ("SHL.AX", "Sonic Healthcare"),
        ("QBE.AX", "QBE Insurance"),
        ("ORG.AX", "Origin Energy"),
        ("AGL.AX", "AGL Energy"),
        ("APT.AX", "Afterpay (Block)"),
        ("XRO.AX", "Xero"),
        ("A2M.AX", "a2 Milk"),
    ],
    "🇦🇺 ASX ETFs": [
        ("VAS.AX", "Vanguard ASX 300"),
        ("STW.AX", "SPDR ASX 200"),
        ("IOZ.AX", "iShares Core ASX 200"),
        ("VGS.AX", "Vanguard Intl Shares"),
        ("IVV.AX", "iShares S&P 500"),
        ("NDQ.AX", "BetaShares NASDAQ 100"),
        ("VDHG.AX", "Vanguard Diversified High Growth"),
        ("A200.AX", "BetaShares ASX 200"),
        ("DHHF.AX", "BetaShares Diversified High Growth"),
        ("VGAD.AX", "Vanguard Intl Hedged"),
        ("VHY.AX", "Vanguard High Yield"),
        ("VTS.AX", "Vanguard US Total Market"),
        ("VEU.AX", "Vanguard All-World ex-US"),
        ("ETHI.AX", "BetaShares Global Sustainability"),
        ("HACK.AX", "BetaShares Cybersecurity"),
    ],
    "🇮🇳 NSE Stocks": [
        ("RELIANCE.NS", "Reliance Industries"),
        ("TCS.NS", "Tata Consultancy Services"),
        ("INFY.NS", "Infosys"),
        ("HDFCBANK.NS", "HDFC Bank"),
        ("ICICIBANK.NS", "ICICI Bank"),
        ("BHARTIARTL.NS", "Bharti Airtel"),
        ("ITC.NS", "ITC Limited"),
        ("HINDUNILVR.NS", "Hindustan Unilever"),
        ("SBIN.NS", "State Bank of India"),
        ("HDFC.NS", "HDFC Limited"),
        ("KOTAKBANK.NS", "Kotak Mahindra Bank"),
        ("AXISBANK.NS", "Axis Bank"),
        ("LT.NS", "Larsen & Toubro"),
        ("WIPRO.NS", "Wipro"),
        ("ASIANPAINT.NS", "Asian Paints"),
        ("MARUTI.NS", "Maruti Suzuki"),
        ("TATAMOTORS.NS", "Tata Motors"),
        ("TATASTEEL.NS", "Tata Steel"),
        ("SUNPHARMA.NS", "Sun Pharma"),
        ("BAJFINANCE.NS", "Bajaj Finance"),
        ("NESTLEIND.NS", "Nestle India"),
        ("TITAN.NS", "Titan Company"),
        ("ULTRACEMCO.NS", "UltraTech Cement"),
        ("POWERGRID.NS", "Power Grid Corp"),
        ("ONGC.NS", "ONGC"),
        ("NTPC.NS", "NTPC"),
        ("HCLTECH.NS", "HCL Technologies"),
        ("TECHM.NS", "Tech Mahindra"),
        ("ADANIENT.NS", "Adani Enterprises"),
        ("ADANIPORTS.NS", "Adani Ports"),
    ],
    "🇮🇳 NSE ETFs & Indices": [
        ("NIFTYBEES.NS", "Nippon NIFTY 50 ETF"),
        ("BANKBEES.NS", "Nippon Bank NIFTY ETF"),
        ("JUNIORBEES.NS", "Nippon NIFTY Next 50"),
        ("GOLDBEES.NS", "Nippon Gold ETF"),
        ("SETFNIF50.NS", "SBI NIFTY 50 ETF"),
        ("ICICIB22.NS", "ICICI Bharat 22 ETF"),
        ("NETFMID150.NS", "Nippon NIFTY Midcap 150"),
        ("ITBEES.NS", "Nippon IT Sector ETF"),
    ],
    "✏️ Custom Symbol": [
        ("CUSTOM", "Enter your own symbol"),
    ],
}

# Region selector OUTSIDE form - this allows dynamic updates
new_region = st.selectbox("📍 Select Category", list(POPULAR_SYMBOLS.keys()), key="region_selector")

# Get symbols for selected region
symbols_for_region = POPULAR_SYMBOLS[new_region]
symbol_options = [f"{sym} - {name}" for sym, name in symbols_for_region]

# Check if custom symbol selected
is_custom = new_region == "✏️ Custom Symbol"

with st.form("add_holding_form"):
    if is_custom:
        st.markdown("**Enter Custom Symbol:**")
        custom_col1, custom_col2 = st.columns(2)
        with custom_col1:
            custom_sym = st.text_input("Symbol (e.g., AAPL, CBA.AX, TCS.NS)", placeholder="AAPL")
        with custom_col2:
            custom_name = st.text_input("Name (optional)", placeholder="Apple Inc.")
        new_sym = custom_sym.upper() if custom_sym else ""
        new_name = custom_name if custom_name else new_sym
        new_region_final = "🌍 Custom"
    else:
        selected_symbol = st.selectbox("📈 Select Stock/ETF", symbol_options)
        # Parse selected symbol
        new_sym = selected_symbol.split(" - ")[0] if selected_symbol else ""
        new_name = selected_symbol.split(" - ")[1] if " - " in selected_symbol else new_sym
        new_region_final = new_region
    
    st.markdown("---")
    c3, c4 = st.columns(2)
    with c3:
        new_shares = st.number_input("📊 Number of Shares", min_value=0.01, value=1.0, step=0.1)
    with c4:
        new_cost = st.number_input("💰 Avg Cost per Share ($)", min_value=0.01, value=100.0, step=1.0)
    
    submitted = st.form_submit_button("➕ Add to Portfolio", use_container_width=True)
    
    if submitted:
        if new_sym and new_sym != "CUSTOM":
            # Check if symbol already exists
            existing = [h['symbol'].upper() for h in st.session_state.portfolio]
            if new_sym.upper() in existing:
                st.warning(f"⚠️ {new_sym.upper()} already in portfolio!")
            else:
                new_holding = {
                    "symbol": new_sym.upper(), 
                    "name": new_name, 
                    "shares": new_shares, 
                    "avg_cost": new_cost, 
                    "region": new_region_final
                }
                db_add_holding(new_holding)
                st.session_state.portfolio.append(new_holding)
                st.success(f"✅ Added {new_sym.upper()} to portfolio!")
                st.rerun()
        else:
            st.error("Please enter a valid symbol")

# Symbol format help
st.caption("💡 **Symbol formats**: US stocks: AAPL, MSFT | Australian: CBA.AX, BHP.AX | Indian: TCS.NS, INFY.NS")
