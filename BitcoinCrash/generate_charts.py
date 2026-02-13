import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

# Setup
ASSETS_DIR = "assets"
os.makedirs(ASSETS_DIR, exist_ok=True)

# Define tickers
# IBIT: BlackRock Bitcoin ETF
# IGV: iShares Expanded Tech-Software Sector ETF
# GLD: SPDR Gold Shares
# BTC-USD: Bitcoin Spot
tickers = ["IBIT", "IGV", "GLD", "BTC-USD"]
start_date = "2025-07-01"
end_date = "2026-02-14" # Extended to capture Feb 13

print(f"Fetching data for {tickers} from {start_date} to {end_date}...")

def fetch_data():
    data = {}
    for ticker in tickers:
        df = yf.download(ticker, start=start_date, end=end_date)
        if not df.empty:
            # Flatten columns if MultiIndex (sometimes happens with yfinance)
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            data[ticker] = df['Close']
    return pd.DataFrame(data)

def generate_charts(df):
    plt.style.use('seaborn-v0_8-darkgrid')
    
    # 1. BTC vs Software Stocks (Correlation)
    plt.figure(figsize=(12, 6))
    norm_df = df[['IBIT', 'IGV']].dropna()
    norm_df = (norm_df / norm_df.iloc[0]) * 100
    
    plt.plot(norm_df.index, norm_df['IBIT'], label='IBIT (Bitcoin ETF)', color='#F7931A', linewidth=2)
    plt.plot(norm_df.index, norm_df['IGV'], label='IGV (Software Stocks)', color='#0078D4', linewidth=2)
    
    # Highlight the crash areas
    crash1_start = datetime(2026, 2, 4)
    crash1_end = datetime(2026, 2, 7)
    crash2_start = datetime(2026, 2, 12)
    crash2_end = datetime(2026, 2, 13)
    
    plt.axvspan(crash1_start, crash1_end, color='red', alpha=0.1, label='Mechanical (Feb 5)')
    plt.axvspan(crash2_start, crash2_end, color='orange', alpha=0.1, label='Macro (Feb 13)')
    
    plt.title('Bitcoin vs. Software Equities: The Double-Dip (Indexed to 100)', fontsize=14, fontweight='bold')
    plt.ylabel('Indexed Price')
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{ASSETS_DIR}/btc_vs_software.png", dpi=300)
    plt.close()

    # 2. BTC vs Gold Divergence (and later Convergence)
    plt.figure(figsize=(12, 6))
    gold_df = df[['IBIT', 'GLD']].dropna()
    gold_df = (gold_df / gold_df.iloc[0]) * 100
    
    plt.plot(gold_df.index, gold_df['IBIT'], label='IBIT (Bitcoin ETF)', color='#F7931A', linewidth=2)
    plt.plot(gold_df.index, gold_df['GLD'], label='GLD (Gold)', color='#D4AF37', linewidth=2)
    
    plt.axvspan(crash1_start, crash1_end, color='red', alpha=0.1, label='Feb 5 Divergence')
    plt.axvspan(crash2_start, crash2_end, color='purple', alpha=0.1, label='Feb 13 Macro-Risk')
    
    plt.title('Bitcoin vs. Gold: Divergence to Convergence', fontsize=14, fontweight='bold')
    plt.ylabel('Indexed Price')
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{ASSETS_DIR}/btc_vs_gold.png", dpi=300)
    plt.close()

    # 3. BTC Price Crash Detail (Showing both legs)
    plt.figure(figsize=(12, 6))
    btc_detail = df['BTC-USD'].dropna().loc['2026-01-20':]
    
    plt.plot(btc_detail.index, btc_detail, color='#F7931A', linewidth=2.5)
    plt.scatter(datetime(2026, 2, 5), btc_detail.loc['2026-02-05'], color='red', s=100, zorder=5)
    plt.scatter(datetime(2026, 2, 13), btc_detail.loc['2026-02-13'], color='orange', s=100, zorder=5)
    
    plt.annotate('Mechanical Crash', 
                 xy=(datetime(2026, 2, 5), btc_detail.loc['2026-02-05']),
                 xytext=(datetime(2026, 2, 1), btc_detail.loc['2026-02-05'] * 0.95),
                 arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=8))
    
    plt.annotate('Macro Liquidity Crash', 
                 xy=(datetime(2026, 2, 13), btc_detail.loc['2026-02-13']),
                 xytext=(datetime(2026, 2, 8), btc_detail.loc['2026-02-13'] * 1.05),
                 arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=8))
    
    plt.title('Bitcoin Price: The February 2026 Liquidity Event', fontsize=14, fontweight='bold')
    plt.ylabel('Price (USD)')
    plt.tight_layout()
    plt.savefig(f"{ASSETS_DIR}/btc_crash_detail.png", dpi=300)
    plt.close()

    print(f"Charts generated successfully in {ASSETS_DIR}/")

if __name__ == "__main__":
    df = fetch_data()
    if not df.empty:
        generate_charts(df)
    else:
        print("Error: No data fetched.")
