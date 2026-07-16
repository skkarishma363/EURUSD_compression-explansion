# 📈 EURUSD Volatility Compression → Expansion Trading Strategy

A professional quantitative trading research platform for **EURUSD**, built in Python. The project detects low-volatility compression zones, identifies breakout opportunities, synchronizes multi-timeframe signals, performs historical backtesting, optimizes strategy parameters, evaluates robustness using Monte Carlo simulations, and provides an interactive Streamlit dashboard.

---

## 🚀 Features

- Multi-Timeframe Analysis (H1 + M5)
- Volatility Compression Detection
- Breakout Confirmation
- Pullback-Based Entries
- Trend Filtering using EMA200
- ATR-Based Stop Loss & Take Profit
- Session Filtering (London & New York)
- Dynamic Risk Management
- Historical Backtesting Engine
- Performance Metrics
- Walk-Forward Testing
- Grid Search Parameter Optimization
- Monte Carlo Robustness Analysis
- Interactive Streamlit Dashboard
- Interactive Candlestick Trade Visualization

---

## 📂 Project Structure

```text
EURUSD_Project/
│
├── data/
│   └── EURUSD_M1_2020.csv
│
├── strategy/
│   ├── indicators.py
│   ├── compression.py
│   ├── breakout.py
│   ├── pullback.py
│   ├── entries.py
│   ├── risk.py
│   ├── filters.py
│
├── backtest/
│   ├── engine.py
│   ├── metrics.py
│   ├── optimizer.py
│   ├── walkforward.py
│   ├── montecarlo.py
│   ├── visualization.py
│   └── synchronizer.py
│
├── utils/
│   ├── loader.py
│   ├── cleaner.py
│   ├── resampler.py
│
├── dashboard.py
├── main.py
├── requirements.txt
└── README.md
```

---

# 📊 Trading Strategy

## Higher Timeframe (H1)

The strategy first identifies low-volatility compression zones.

Compression conditions include:

- ATR(14) below historical average
- Narrow Bollinger Band Width
- Significant candle overlap
- Compression range identification

---

## Trend Filter

Long Trades

- Price above EMA200
- EMA200 upward slope

Short Trades

- Price below EMA200
- EMA200 downward slope

---

## Breakout Conditions

A valid breakout requires:

- Candle closes outside the compression range
- Strong breakout candle
- ADX confirmation
- EMA distance filter

---

## Entry (M5)

After breakout:

- Wait for pullback
- Bullish/Bearish Engulfing confirmation
- Swing High/Low confirmation
- Entry executed only during valid trading sessions

---

## Risk Management

- ATR-based Stop Loss
- Dynamic Position Sizing
- Partial Profit Booking
- ATR Trailing Stop
- Breakeven Protection

---

# 📈 Performance Analysis

The project automatically calculates:

- Win Rate
- Net Profit
- Gross Profit
- Gross Loss
- Profit Factor
- Expectancy
- Average Win
- Average Loss
- Maximum Drawdown
- Sharpe Ratio

---

# 🔬 Research Modules

## Walk Forward Testing

Evaluates strategy stability across different market periods.

---

## Grid Search Optimization

Optimizes:

- ATR Multiplier
- TP1 Multiplier
- ADX Threshold
- EMA Distance Threshold

---

## Monte Carlo Simulation

Evaluates strategy robustness through randomized trade sequence simulations.

Provides:

- Average Final Balance
- Worst Balance
- Best Balance
- Average Drawdown
- Equity Curve Simulations

---

# 📊 Interactive Dashboard

Built using Streamlit and Plotly.

Includes:

- Live Performance Metrics
- Equity Curve
- Candlestick Trade Viewer
- Trade Log
- Profit Distribution
- Optimization Results
- Monte Carlo Analysis

---

# 🛠 Technologies Used

- Python
- Pandas
- NumPy
- Plotly
- Streamlit
- Matplotlib
- TA Library

---

# ▶ Installation

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/EURUSD_Project.git
```

Move into the project

```bash
cd EURUSD_Project
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# ▶ Run Backtest

```bash
python main.py
```

---

# ▶ Launch Dashboard

```bash
streamlit run dashboard.py
```

---

# 📷 Dashboard Preview

Add screenshots of:

- Dashboard Home
- Equity Curve
- Candlestick View
- Monte Carlo Analysis
- Optimization Results

inside the repository's screenshots folder.

---

# ⚠ Disclaimer

This project is intended for educational and quantitative research purposes only.

It should not be considered financial advice or a guarantee of future trading performance.

---

# 👩‍💻 Author

**Shaik Karishma**

Computer Science Engineering Student

Quantitative Trading | Python | Algorithmic Trading | Data Analysis | Streamlit

---

# ⭐ Future Improvements

- Multi-Currency Support
- Live Market Data Integration
- Paper Trading
- Broker API Integration
- Portfolio Optimization
- Machine Learning Trade Filter
- AI-Based Market Regime Detection
- Cloud Deployment
