import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
from datetime import datetime

# Setup
ASSETS_DIR = "assets"
os.makedirs(ASSETS_DIR, exist_ok=True)

# Tickers
# BTC-USD: Spot
# BTCG26.CME: Feb 2026 Futures
# BTC=F: Continuous Futures
# IBIT: ETF
# VIX: Volatility Index
# IGV: Software Stocks
tickers = ["BTC-USD", "BTCG26.CME", "BTC=F", "IBIT", "^VIX", "IGV"]
start_date = "2025-12-01"
end_date = "2026-02-14" # Extended to capture Feb 13

def fetch_data():
    print(f"Fetching deep data for {tickers}...")
    data = {}
    for t in tickers:
        df = yf.download(t, start=start_date, end=end_date)
        if not df.empty:
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            data[t] = df['Close']
            if 'Volume' in df.columns:
                data[f"{t}_Vol"] = df['Volume']
    return pd.DataFrame(data)

def generate_deep_charts(df):
    plt.style.use('seaborn-v0_8-whitegrid')
    
    # 1. Annualized CME Basis (The "Unwind" Trigger)
    # Annualized Basis (%) = ((Futures / Spot) - 1) * (365 / days_to_expiry)
    # Assuming Feb 2026 contract expires Feb 27, 2026
    expiry = datetime(2026, 2, 27)
    df = df.dropna(subset=['BTC-USD', 'BTCG26.CME'])
    
    basis_df = df.copy()
    basis_df['days_to_expiry'] = [(expiry - d).days for d in basis_df.index]
    basis_df['days_to_expiry'] = basis_df['days_to_expiry'].replace(0, 1) # Avoid div by zero
    basis_df['basis_annualized'] = ((basis_df['BTCG26.CME'] / basis_df['BTC-USD']) - 1) * (365 / basis_df['days_to_expiry']) * 100

    plt.figure(figsize=(12, 6))
    plt.plot(basis_df.index, basis_df['basis_annualized'], color='#2ECC71', linewidth=2, label='CME Annualized Basis (%)')
    plt.axhline(0, color='black', linestyle='--', alpha=0.3)
    plt.axvspan(datetime(2026, 2, 4), datetime(2026, 2, 6), color='red', alpha=0.1, label='Feb 5 Unwind')
    plt.axvspan(datetime(2026, 2, 12), datetime(2026, 2, 13), color='orange', alpha=0.1, label='Feb 13 Macro Panic')
    
    plt.title('CME Bitcoin Basis: The Two Faces of Contraction', fontsize=14, fontweight='bold')
    plt.ylabel('Annualized Yield (%)')
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{ASSETS_DIR}/cme_basis_deep.png", dpi=300)
    plt.close()

    # 2. ETF Volume Spike vs Price (The "Mechanical Inflow" Paradox)
    plt.figure(figsize=(12, 6))
    etf_df = df[['IBIT', 'IBIT_Vol']].dropna()
    
    fig, ax1 = plt.subplots(figsize=(12, 6))
    ax1.plot(etf_df.index, etf_df['IBIT'], color='#F7931A', label='IBIT Price', linewidth=2)
    ax1.set_ylabel('ETF Price ($)', color='#F7931A', fontweight='bold')
    
    ax2 = ax1.twinx()
    ax2.bar(etf_df.index, etf_df['IBIT_Vol'], color='#34495E', alpha=0.2, label='ETF Volume')
    ax2.set_ylabel('Trading Volume', color='#34495E', fontweight='bold')
    
    plt.title('IBIT ETF: Price Collapse vs Record Volume Spike', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f"{ASSETS_DIR}/etf_volume_paradox.png", dpi=300)
    plt.close()

    # 3. Cross-Asset Volatility Correlation
    # Calculate rolling 10-day volatility
    vol_df = df[['BTC-USD', 'IGV', '^VIX']].pct_change().rolling(10).std() * np.sqrt(252) * 100
    vol_df = vol_df.dropna()

    plt.figure(figsize=(12, 6))
    plt.plot(vol_df.index, vol_df['BTC-USD'], label='BTC Volatility', color='#F7931A', linewidth=2)
    plt.plot(vol_df.index, vol_df['IGV'], label='Software (IGV) Volatility', color='#0078D4', linewidth=2)
    plt.plot(vol_df.index, vol_df['^VIX'], label='Equity VIX (Market Risk)', color='#E74C3C', linewidth=1.5, linestyle='--')
    
    plt.title('Cross-Asset Volatility: The Contagion Map', fontsize=14, fontweight='bold')
    plt.ylabel('Annualized Volatility (%)')
    plt.legend()
    plt.savefig(f"{ASSETS_DIR}/volatility_contagion.png", dpi=300)
    plt.close()

    print("Deeper charts generated successfully.")

if __name__ == "__main__":
    df = fetch_data()
    if not df.empty:
        generate_deep_charts(df)
    else:
        print("Error fetching deep data.")
