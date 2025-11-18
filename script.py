# ===========================================================
# 🇮🇳 NSE Market Analyzer — YFinance Version (Live Visuals + Excel)
# Author : Sayyed Viquar Ahmed
# Version: 6.0
# ===========================================================

import warnings
warnings.filterwarnings("ignore")

import yfinance as yf
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

plt.style.use("seaborn-v0_8")
plt.rcParams["font.family"] = "DejaVu Sans"

# -----------------------------------------------------------
# 1️⃣ FII / DII (User Input)
# -----------------------------------------------------------
def get_fii_dii():
    print("🏦 Enter FII/DII Data (in ₹ Cr):")
    fii = float(input("Enter FII Net (positive for buy, negative for sell): "))
    dii = float(input("Enter DII Net (positive for buy, negative for sell): "))
    print(f"🏦 FII Net: ₹{fii:,.2f} Cr | DII Net: ₹{dii:,.2f} Cr")
    return fii, dii

# -----------------------------------------------------------
# 2️⃣ PCR (Approximated using NIFTY Open Interest)
# -----------------------------------------------------------
def get_pcr(symbol="^NSEI"):
    try:
        nifty = yf.Ticker(symbol)
        hist = nifty.history(period="5d", interval="1d")
        pcr = round((hist["Close"].iloc[-1] / hist["Close"].mean()), 2)
        print(f"🧮 Approx. PCR (Price Ratio): {pcr}")
        return pcr
    except Exception:
        return float(input("Enter manual PCR value (e.g. 1.05): "))

# -----------------------------------------------------------
# 3️⃣ India VIX
# -----------------------------------------------------------
def get_vix():
    try:
        vix = yf.Ticker("^INDIAVIX").history(period="5d")
        value = round(vix["Close"].iloc[-1], 2)
        print(f"⚡ India VIX: {value}")
        return value
    except Exception:
        return float(input("Enter manual India VIX value (e.g. 14.6): "))

# -----------------------------------------------------------
# 4️⃣ MMI (Momentum vs Manipulation Index)
# -----------------------------------------------------------
def calc_mmi(fii, dii, pcr, vix):
    if any(x == 0 for x in [vix, pcr]):
        print("⚠️ Cannot compute MMI with zero inputs.")
        return 0, "Undefined"
    mmi = ((fii + dii) / abs(fii - dii + 1)) * (1 / (vix / 15)) * (1 / pcr)
    mmi = round(mmi, 2)
    status = "Momentum Driven 🟢" if mmi > 1.5 else "Balanced ⚪" if mmi >= 1 else "Manipulation Risk 🔴"
    print(f"\n📊 MMI: {mmi} → {status}")
    return mmi, status

# -----------------------------------------------------------
# 5️⃣ Operator Volume Tracker
# -----------------------------------------------------------
def operator_volume_tracker(symbols):
    print("\n🎛️ Operator Volume Tracker (Based on Recent Volume Spikes)")
    records = []
    for s in symbols:
        try:
            data = yf.Ticker(f"{s}.NS").history(period="1mo")
            avg_vol = data["Volume"].mean()
            last_vol = data["Volume"].iloc[-1]
            ratio = round(last_vol / avg_vol, 2)
            ltp = round(data["Close"].iloc[-1], 2)
            chg = round(((data["Close"].iloc[-1] - data["Close"].iloc[-2]) / data["Close"].iloc[-2]) * 100, 2)
            act = "🟢 Normal" if ratio < 2 else "🟠 Operator Activity" if ratio < 4 else "🔴 Heavy Operator Control"
            records.append({
                "Symbol": s,
                "Volume Ratio": ratio,
                "Activity": act,
                "LTP": ltp,
                "Change (%)": chg
            })
        except Exception:
            print(f"⚠️ Failed to fetch {s}. Please enter manually.")
            ratio = float(input(f"Volume Ratio for {s}: "))
            ltp = float(input(f"LTP for {s}: "))
            chg = float(input(f"Change (%) for {s}: "))
            act = "🟢 Normal" if ratio < 2 else "🟠 Operator Activity" if ratio < 4 else "🔴 Heavy Operator Control"
            records.append({
                "Symbol": s,
                "Volume Ratio": ratio,
                "Activity": act,
                "LTP": ltp,
                "Change (%)": chg
            })
    df = pd.DataFrame(records)
    print(df.to_string(index=False))
    return df

# -----------------------------------------------------------
# 6️⃣ Sectoral Heatmap
# -----------------------------------------------------------
def sectoral_heatmap():
    print("\n🧭 Sectoral Heatmap (Based on Key NSE Sector Indices)")
    sectors = {
        "NIFTYBANK": "^NSEBANK",
        "NIFTYIT": "^CNXIT",
        "NIFTYFMCG": "^CNXFMCG",
        "NIFTYMETAL": "^CNXMETAL",
        "NIFTYAUTO": "^CNXAUTO",
        "NIFTYPHARMA": "^CNXPHARMA",
        "NIFTYREALTY": "^CNXREALTY",
        "NIFTYENERGY": "^CNXENERGY"
    }
    data = []
    for name, ticker in sectors.items():
        try:
            hist = yf.Ticker(ticker).history(period="5d")
            chg = round(((hist["Close"].iloc[-1] - hist["Close"].iloc[-2]) / hist["Close"].iloc[-2]) * 100, 2)
            data.append({"Sector": name, "Change (%)": chg})
        except:
            chg = float(input(f"Enter manual % Change for {name}: "))
            data.append({"Sector": name, "Change (%)": chg})
    df = pd.DataFrame(data).set_index("Sector")
    plt.figure(figsize=(8,4))
    sns.heatmap(df, annot=True, cmap="RdYlGn", linewidths=0.5)
    plt.title("📊 NSE Sectoral Performance Heatmap (via YFinance)")
    plt.tight_layout()
    plt.show()
    return df

# -----------------------------------------------------------
# 7️⃣ Sentiment Visualization
# -----------------------------------------------------------
def visualize_sentiment(pcr, vix):
    plt.figure(figsize=(5,3))
    sns.barplot(x=["PCR","VIX"], y=[pcr,vix], palette="RdYlGn")
    plt.title("Market Sentiment Snapshot")
    plt.tight_layout()
    plt.show()

# -----------------------------------------------------------
# MAIN
# -----------------------------------------------------------
if __name__ == "__main__":
    print("="*70)
    print("🇮🇳 NSE MARKET ANALYZER — YFinance (Live + Excel Report)")
    print("="*70)

    fii, dii = get_fii_dii()
    pcr = get_pcr("^NSEI")
    vix = get_vix()
    mmi, status = calc_mmi(fii, dii, pcr, vix)
    visualize_sentiment(pcr, vix)

    symbols = input("\nEnter stock symbols (e.g. RELIANCE,SBIN,INFY): ").upper().split(",")
    df_ops = operator_volume_tracker(symbols)
    df_sec = sectoral_heatmap()

    with pd.ExcelWriter("reports/market_analysis_yf.xlsx") as writer:
        df_ops.to_excel(writer, sheet_name="Operator Activity", index=False)
        df_sec.to_excel(writer, sheet_name="Sector Performance")
        pd.DataFrame([{
            "MMI": mmi, "Status": status, "FII (Cr)": fii, "DII (Cr)": dii,
            "VIX": vix, "PCR": pcr, "Date": datetime.now()
        }]).to_excel(writer, sheet_name="Summary", index=False)

    print("\n💾 Excel saved → reports/market_analysis_yf.xlsx")
    print(f"✅ Analysis Complete — MMI: {mmi} → {status}")

