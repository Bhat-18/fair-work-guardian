# 💰 Fair Work Guardian

A comprehensive personal finance dashboard built with **Streamlit**, designed to help Australian workers manage their pay, investments, and savings — all in one place.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B?logo=streamlit)
![Supabase](https://img.shields.io/badge/Supabase-Database-3ECF8E?logo=supabase)
![License](https://img.shields.io/badge/License-MIT-green)

---

## ✨ Features

### 💰 Payslip Calculator
- **Fair Work compliant** — based on Australia's General Retail Industry Award 2024-25
- Supports **Casual** (+25% loading) and **Part-time** employment types
- Automatic calculation of:
  - Day/Evening shift differentials (+25% after 6pm)
  - Weekend penalty rates (Saturday +25%, Sunday +50%)
  - Public holiday rates (2.5x)
  - Overtime (1.5x first 3h, 2x after)
  - Break deductions (30min for shifts >5h)
- **Payslip history** — every calculation saved to database with full shift breakdown

### 📈 Investment Portfolio
- Track holdings across **global markets** (US, Australia, India, Europe)
- Live stock prices via **Yahoo Finance API**
- Portfolio allocation visualizer (pie chart by region)
- Gain/loss tracking per holding
- Historical price charts
- Investment suggestions based on your last payslip

### 📊 Market Dashboard
- Real-time market data across multiple regions:
  - 🇺🇸 US: S&P 500, NASDAQ, Dow Jones
  - 🇦🇺 Australia: ASX 200
  - 🇮🇳 India: NIFTY 50, SENSEX
  - 🇪🇺 Europe: EURO STOXX 50, FTSE 100
- Interactive charts with customizable time periods
- Top gainers and losers

### 🎯 Savings Goals
- Create and track multiple savings goals
- Visual progress bars with weekly contribution tracking
- "Weeks remaining" calculator
- Overall savings progress dashboard
- Compound interest calculator

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| **Streamlit** | Frontend framework |
| **Supabase** | PostgreSQL database (cloud) |
| **Plotly** | Interactive charts & visualizations |
| **Yahoo Finance** | Real-time stock & market data |
| **Google Gemini AI** | Payslip shift parsing |
| **Python** | Backend logic |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- A [Supabase](https://supabase.com) account (free tier works)
- A [Google AI](https://aistudio.google.com/apikey) API key

### 1. Clone the repo
```bash
git clone https://github.com/Bhat-18/fair-work-guardian.git
cd fair-work-guardian
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up environment variables
Create a `.env` file in the project root:
```env
GEMINI_API_KEY=your-gemini-api-key
GOOGLE_API_KEY=your-google-api-key
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-publishable-key
```

### 4. Set up the database
1. Go to your Supabase dashboard → **SQL Editor**
2. Run the SQL from `supabase_setup.sql` to create the required tables:
   - `portfolio` — Investment holdings
   - `savings_goals` — Savings goals
   - `user_settings` — Key-value settings (last pay, goals totals)
   - `payslip_history` — Payslip calculation history

### 5. Run the app
```bash
streamlit run app.py
```

The app will be available at `http://localhost:8501`

---

## 📁 Project Structure

```
fair-work-guardian/
├── app.py                  # Home page & navigation hub
├── db.py                   # Supabase database helper module
├── server.py               # MCP server for AI-powered shift parsing
├── requirements.txt        # Python dependencies
├── supabase_setup.sql      # Database table creation SQL
├── .env                    # Environment variables (not tracked)
├── data/
│   ├── pay_guide.pdf       # Fair Work pay guide reference
│   └── retail_award.pdf    # Retail Award 2024-25 reference
└── pages/
    ├── 1_💰_Payslip_Calculator.py
    ├── 2_📈_Investment_Portfolio.py
    ├── 3_📊_Market_Dashboard.py
    └── 5_🎯_Savings_Goals.py
```

---

## ☁️ Deployment (Streamlit Cloud)

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **New app** → select this repo → set `app.py` as main file
4. Add your secrets in **Advanced settings → Secrets**:
   ```toml
   SUPABASE_URL = "https://your-project.supabase.co"
   SUPABASE_KEY = "your-publishable-key"
   GEMINI_API_KEY = "your-gemini-key"
   GOOGLE_API_KEY = "your-google-key"
   ```
5. Click **Deploy**!

---

## 📊 Database Schema

| Table | Description |
|---|---|
| `portfolio` | Stock holdings (symbol, name, shares, avg_cost, region) |
| `savings_goals` | Savings goals (name, target, saved, icon, weekly, color) |
| `user_settings` | Key-value store for app settings |
| `payslip_history` | Payslip calculations with shift breakdowns (JSONB) |

---

## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 👨‍💻 Author

**Bhat-18** — [GitHub](https://github.com/Bhat-18)

Built with ❤️ in Australia 🇦🇺
