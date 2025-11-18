# 🚀 QuantNexus Engine
### *Advanced Quantitative Market Analyzer for Indian Markets (NSE)*

QuantNexus Engine is a **quant-driven financial research tool** that fetches **live NSE market data** using `yfinance` and performs multiple quantitative analyses including **FII/DII flow modeling**, **India VIX volatility analysis**, **PCR approximation**, **Operator Volume Activity**, **Sector Heatmaps**, and a proprietary **MMI (Momentum vs Manipulation Index)**.  

It also exports a complete **Excel research report** with structured multi-sheet insights.

## 🔥 Key Features
- Manual input for **FII/DII**
- Live **NIFTY data** for PCR estimation
- **India VIX** fetch for volatility regime detection
- Custom **MMI (Momentum vs Manipulation Index)**
- **Operator Volume Tracker** for detecting spikes
- **Sectoral Heatmap Analysis**
- **Sentiment Visualization (PCR vs VIX)**
- Automatic **Excel report generation**

## 📦 Installation
### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/quantnexus-engine.git
cd quantnexus-engine
```

### 2. Install all dependencies
```bash
pip install -r requirements.txt
```

## ▶️ How to Run
```bash
python script.py
```

## 🧭 Workflow Overview
### Input Stage
Enter FII/DII values used in the quant model.

### Live Data Fetch
Retrieves:
- NIFTY prices
- India VIX
- Sector indices

### Operator Volume Tracker
Enter stock symbols to compute:
- Volume ratio
- Operator activity label
- LTP and % change

### Visual Outputs
- PCR vs VIX chart
- Sector heatmap

### Excel Research Report
Saved as:
`reports/market_analysis_yf.xlsx`

## 🧮 MMI (Momentum vs Manipulation Index)
Formula:
```
MMI = ((FII + DII) / abs(FII - DII + 1)) * (1 / (VIX / 15)) * (1 / PCR)
```

Regime Interpretation:
- >1.5 Momentum Driven
- 1.0–1.5 Balanced
- <1.0 Manipulation Risk

## 📁 Project Structure
```
.
├── script.py
├── README.md
├── requirements.txt
└── reports/
      └── market_analysis_yf.xlsx
```

## 🛠️ Tech Requirements
Python 3.8+  
Internet connection  
yfinance support  

## 🤝 Contributing
PRs welcome.

## 🧾 License
MIT License.
