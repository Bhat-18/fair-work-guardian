import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import yfinance as yf
from datetime import datetime

st.set_page_config(page_title="Market Dashboard", layout="wide", page_icon="📊", initial_sidebar_state="collapsed")

# ==========================================
# CSS
# ==========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    .stApp { background: linear-gradient(180deg, #0a0a0f 0%, #1a1a2e 100%); font-family: 'Inter', sans-serif; }
    .main .block-container { padding: 1.5rem; max-width: 1200px; }
    
    /* Hide sidebar */
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="stSidebarNav"] { display: none !important; }
    section[data-testid="stSidebar"] { display: none !important; }
    button[kind="header"] { display: none !important; }
    
    .hero { text-align: center; padding: 1.5rem; margin-bottom: 1.5rem; background: linear-gradient(135deg, #f59e0b, #d97706); border-radius: 16px; }
    .hero h1 { font-size: 1.75rem; font-weight: 800; color: #fff; margin: 0; }
    .hero p { color: rgba(255,255,255,0.9); margin-top: 0.25rem; font-size: 0.9rem; }
    
    .region-header { font-size: 1.1rem; font-weight: 700; color: #fff; padding: 0.6rem 1rem; background: #252542; border-radius: 10px 10px 0 0; margin-top: 1rem; }
    .ticker-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 0.5rem; padding: 0.75rem; background: #1a1a2e; border-radius: 0 0 10px 10px; border: 1px solid #2d2d4a; border-top: none; }
    .ticker-card { background: #252542; border-radius: 8px; padding: 0.6rem; text-align: center; }
    .ticker-symbol { font-weight: 700; color: #fff; font-size: 0.8rem; }
    .ticker-name { font-size: 0.65rem; color: #9ca3af; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .ticker-price { font-size: 1rem; font-weight: 800; color: #fff; margin-top: 0.2rem; }
    .ticker-change { font-size: 0.75rem; }
    .positive { color: #10b981; }
    .negative { color: #ef4444; }
    
    /* Tab styling - make labels visible */
    .stTabs [data-baseweb="tab-list"] { background: #1a1a2e; border-radius: 10px; padding: 0.5rem; gap: 0.5rem; }
    .stTabs [data-baseweb="tab"] { 
        color: #ffffff !important; 
        font-weight: 700 !important; 
        font-size: 1rem !important;
        background: #252542 !important;
        border-radius: 8px !important;
        padding: 0.75rem 1.5rem !important;
        border: 1px solid #3d3d5a !important;
    }
    .stTabs [data-baseweb="tab"]:hover { 
        background: #3d3d5a !important; 
    }
    .stTabs [aria-selected="true"] { 
        background: linear-gradient(135deg, #4f46e5, #7c3aed) !important; 
        border-color: #7c3aed !important;
    }
    .stTabs [data-baseweb="tab-highlight"] { background: transparent !important; }
    .stTabs [data-baseweb="tab-border"] { display: none !important; }
    
    .stSelectbox label { color: #e5e7eb !important; font-weight: 600 !important; font-size: 0.85rem !important; }
    .stSelectbox > div > div { background: #252542 !important; border: 1px solid #3d3d5a !important; border-radius: 8px !important; color: #fff !important; }
    
    /* All text visibility */
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
# EXPANDED MARKET DATA (matching Investment Portfolio)
# ==========================================
MARKETS = {
    "🇺🇸 US Indices": [
        {"symbol": "^GSPC", "name": "S&P 500"},
        {"symbol": "^IXIC", "name": "NASDAQ"},
        {"symbol": "^DJI", "name": "Dow Jones"},
        {"symbol": "^RUT", "name": "Russell 2000"},
        {"symbol": "^VIX", "name": "VIX (Volatility)"},
    ],
    "🇺🇸 US Stocks": [
        {"symbol": "AAPL", "name": "Apple"},
        {"symbol": "MSFT", "name": "Microsoft"},
        {"symbol": "GOOGL", "name": "Google"},
        {"symbol": "AMZN", "name": "Amazon"},
        {"symbol": "NVDA", "name": "NVIDIA"},
        {"symbol": "TSLA", "name": "Tesla"},
        {"symbol": "META", "name": "Meta"},
        {"symbol": "JPM", "name": "JPMorgan"},
        {"symbol": "V", "name": "Visa"},
        {"symbol": "JNJ", "name": "J&J"},
        {"symbol": "WMT", "name": "Walmart"},
        {"symbol": "MA", "name": "Mastercard"},
        {"symbol": "DIS", "name": "Disney"},
        {"symbol": "NFLX", "name": "Netflix"},
        {"symbol": "AMD", "name": "AMD"},
    ],
    "🇺🇸 US ETFs": [
        {"symbol": "SPY", "name": "S&P 500 ETF"},
        {"symbol": "QQQ", "name": "NASDAQ 100"},
        {"symbol": "VTI", "name": "Total Market"},
        {"symbol": "VOO", "name": "Vanguard S&P"},
        {"symbol": "IWM", "name": "Russell 2000"},
        {"symbol": "DIA", "name": "Dow Jones ETF"},
        {"symbol": "ARKK", "name": "ARK Innovation"},
        {"symbol": "GLD", "name": "Gold ETF"},
        {"symbol": "XLF", "name": "Financials"},
        {"symbol": "XLK", "name": "Technology"},
    ],
    "🇦🇺 ASX Indices": [
        {"symbol": "^AXJO", "name": "ASX 200"},
        {"symbol": "^AORD", "name": "All Ordinaries"},
    ],
    "🇦🇺 ASX Stocks": [
        {"symbol": "CBA.AX", "name": "CommBank"},
        {"symbol": "BHP.AX", "name": "BHP Group"},
        {"symbol": "CSL.AX", "name": "CSL Limited"},
        {"symbol": "WBC.AX", "name": "Westpac"},
        {"symbol": "NAB.AX", "name": "NAB"},
        {"symbol": "ANZ.AX", "name": "ANZ Bank"},
        {"symbol": "RIO.AX", "name": "Rio Tinto"},
        {"symbol": "WES.AX", "name": "Wesfarmers"},
        {"symbol": "WOW.AX", "name": "Woolworths"},
        {"symbol": "MQG.AX", "name": "Macquarie"},
        {"symbol": "TLS.AX", "name": "Telstra"},
        {"symbol": "FMG.AX", "name": "Fortescue"},
    ],
    "🇦🇺 ASX ETFs": [
        {"symbol": "VAS.AX", "name": "Vanguard ASX"},
        {"symbol": "STW.AX", "name": "SPDR ASX 200"},
        {"symbol": "IOZ.AX", "name": "iShares ASX"},
        {"symbol": "VGS.AX", "name": "Vanguard Intl"},
        {"symbol": "IVV.AX", "name": "iShares S&P"},
        {"symbol": "NDQ.AX", "name": "NASDAQ 100"},
    ],
    "🇮🇳 India Indices": [
        {"symbol": "^NSEI", "name": "NIFTY 50"},
        {"symbol": "^BSESN", "name": "SENSEX"},
        {"symbol": "^NSEBANK", "name": "Bank NIFTY"},
    ],
    "🇮🇳 India Stocks": [
        {"symbol": "RELIANCE.NS", "name": "Reliance"},
        {"symbol": "TCS.NS", "name": "TCS"},
        {"symbol": "INFY.NS", "name": "Infosys"},
        {"symbol": "HDFCBANK.NS", "name": "HDFC Bank"},
        {"symbol": "ICICIBANK.NS", "name": "ICICI Bank"},
        {"symbol": "BHARTIARTL.NS", "name": "Airtel"},
        {"symbol": "ITC.NS", "name": "ITC"},
        {"symbol": "SBIN.NS", "name": "SBI"},
        {"symbol": "HINDUNILVR.NS", "name": "HUL"},
        {"symbol": "KOTAKBANK.NS", "name": "Kotak Bank"},
        {"symbol": "LT.NS", "name": "L&T"},
        {"symbol": "WIPRO.NS", "name": "Wipro"},
        {"symbol": "TATAMOTORS.NS", "name": "Tata Motors"},
        {"symbol": "TATASTEEL.NS", "name": "Tata Steel"},
        {"symbol": "ADANIENT.NS", "name": "Adani Ent"},
    ],
}

@st.cache_data(ttl=300)
def fetch_data(symbols):
    data = {}
    for sym in symbols:
        try:
            hist = yf.Ticker(sym).history(period="5d")
            if len(hist) >= 2:
                curr, prev = hist['Close'].iloc[-1], hist['Close'].iloc[-2]
                data[sym] = {"price": curr, "change": curr - prev, "pct": ((curr - prev) / prev) * 100}
            elif len(hist) == 1:
                data[sym] = {"price": hist['Close'].iloc[-1], "change": 0, "pct": 0}
        except:
            data[sym] = {"price": 0, "change": 0, "pct": 0}
    return data

# ==========================================
# UI
# ==========================================
st.markdown("""
<div class="hero">
    <h1>📊 Market Dashboard</h1>
    <p>Live prices from US, Australia & India markets</p>
</div>
""", unsafe_allow_html=True)

# Market tabs for better organization
tab1, tab2, tab3 = st.tabs(["🇺🇸 US Markets", "🇦🇺 ASX Markets", "🇮🇳 India Markets"])

us_markets = ["🇺🇸 US Indices", "🇺🇸 US Stocks", "🇺🇸 US ETFs"]
au_markets = ["🇦🇺 ASX Indices", "🇦🇺 ASX Stocks", "🇦🇺 ASX ETFs"]
in_markets = ["🇮🇳 India Indices", "🇮🇳 India Stocks"]

def display_market_section(markets_list):
    symbols = [t['symbol'] for m in markets_list for t in MARKETS.get(m, [])]
    with st.spinner("📡 Fetching data..."):
        market_data = fetch_data(symbols)
    
    for region in markets_list:
        if region in MARKETS:
            st.markdown(f'<div class="region-header">{region}</div>', unsafe_allow_html=True)
            cards = '<div class="ticker-grid">'
            for t in MARKETS[region]:
                d = market_data.get(t['symbol'], {"price": 0, "pct": 0})
                cls = "positive" if d['pct'] >= 0 else "negative"
                sign = "+" if d['pct'] >= 0 else ""
                price = f"{d['price']:,.0f}" if d['price'] > 1000 else f"{d['price']:.2f}"
                cards += f'<div class="ticker-card"><div class="ticker-symbol">{t["symbol"].replace("^","").replace(".NS","").replace(".AX","")}</div><div class="ticker-name">{t["name"]}</div><div class="ticker-price">${price}</div><div class="ticker-change {cls}">{sign}{d["pct"]:.2f}%</div></div>'
            cards += '</div>'
            st.markdown(cards, unsafe_allow_html=True)

with tab1:
    display_market_section(us_markets)

with tab2:
    display_market_section(au_markets)

with tab3:
    display_market_section(in_markets)

# Comparison Chart
st.markdown("---")
st.markdown("### 📈 Global Index Comparison (30 Days)")

indices = ["^GSPC", "^NSEI", "^AXJO"]
names = ["S&P 500", "NIFTY 50", "ASX 200"]
colors = ["#4f46e5", "#f59e0b", "#10b981"]

@st.cache_data(ttl=300)
def get_index_hist(symbols):
    data = {}
    for sym in symbols:
        try:
            hist = yf.Ticker(sym).history(period="30d")
            if len(hist) > 0:
                data[sym] = (hist['Close'] / hist['Close'].iloc[0]) * 100
        except:
            pass
    return data

index_data = get_index_hist(indices)

fig = go.Figure()
for i, sym in enumerate(indices):
    if sym in index_data:
        fig.add_trace(go.Scatter(x=index_data[sym].index, y=index_data[sym].values, name=names[i], line=dict(color=colors[i], width=2)))

fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#fff', 
                  xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor='#2d2d4a', title="Base=100"), 
                  legend=dict(orientation="h", y=1.02, x=0.5, xanchor="center"), height=350, hovermode='x unified', margin=dict(t=40, b=20))
st.plotly_chart(fig, use_container_width=True)

# Detail View
st.markdown("---")
st.markdown("### 🔍 Detailed View")

c1, c2 = st.columns([1, 3])
with c1:
    market = st.selectbox("Market", list(MARKETS.keys()))
    ticker = st.selectbox("Symbol", [t['symbol'] for t in MARKETS[market]], format_func=lambda x: f"{x} - {next((t['name'] for t in MARKETS[market] if t['symbol'] == x), x)}")
    period = st.selectbox("Period", ["1mo", "3mo", "6mo", "1y"])

with c2:
    @st.cache_data(ttl=300)
    def get_detail(sym, p):
        try:
            return yf.Ticker(sym).history(period=p)
        except:
            return pd.DataFrame()
    
    hist = get_detail(ticker, period)
    if len(hist) > 0:
        # Calculate stats
        start_price = hist['Close'].iloc[0]
        end_price = hist['Close'].iloc[-1]
        change_pct = ((end_price - start_price) / start_price) * 100
        high = hist['Close'].max()
        low = hist['Close'].min()
        
        # Show metrics
        mc1, mc2, mc3, mc4 = st.columns(4)
        mc1.metric("Current", f"${end_price:.2f}")
        mc2.metric("Change", f"{change_pct:+.1f}%")
        mc3.metric("High", f"${high:.2f}")
        mc4.metric("Low", f"${low:.2f}")
        
        fig2 = go.Figure(go.Candlestick(x=hist.index, open=hist['Open'], high=hist['High'], low=hist['Low'], close=hist['Close'], increasing_line_color='#10b981', decreasing_line_color='#ef4444'))
        fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#fff', xaxis=dict(showgrid=False, rangeslider=dict(visible=False)), yaxis=dict(showgrid=True, gridcolor='#2d2d4a'), height=350, margin=dict(t=20, b=20))
        st.plotly_chart(fig2, use_container_width=True)

st.caption(f"Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
