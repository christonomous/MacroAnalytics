import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

# Setup
ASSETS_DIR = "assets"
os.makedirs(ASSETS_DIR, exist_ok=True)

# Tickers: SPX, DEU40, US100, Gold, Silver, Bitcoin
tickers = {
    "^GSPC": "SPX (S&P 500)",
    "^GDAXI": "DEU40 (DAX)",
    "^IXIC": "US100 (Nasdaq)",
    "GC=F": "Gold",
    "SI=F": "Silver",
    "BTC-USD": "Bitcoin"
}

start_date = "2026-01-29" # Extended to capture baseline for Feb 1
end_date = "2026-02-14"

def fetch_data():
    print("Fetching synchronized 'Everything Crash' data...")
    data = {}
    for symbol, name in tickers.items():
        df = yf.download(symbol, start=start_date, end=end_date)
        if not df.empty:
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            data[name] = df['Close']
    return pd.DataFrame(data)

def generate_everything_chart(df):
    plt.style.use('seaborn-v0_8-whitegrid')
    
    # Baseline: The value on or immediately before Feb 1
    # We bfill to get the last known price for traditionally closed markets on Sunday Feb 1
    feb_data = df.loc['2026-02-01':]
    pre_feb_data = df.loc[:'2026-02-01'].ffill().iloc[-1]
    
    norm_df = (feb_data / pre_feb_data) * 100
    plot_df = norm_df.ffill()
    
    import matplotlib.dates as mdates
    
    plt.figure(figsize=(14, 8))
    
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#F7931A']
    for i, column in enumerate(plot_df.columns):
        plt.plot(plot_df.index, plot_df[column], label=column, linewidth=2, color=colors[i], marker='o', markersize=4, alpha=0.8)
        
    # Highlight Feb 12 (Thursday)
    plt.axvspan(datetime(2026, 2, 12), datetime(2026, 2, 12, 23, 59), color='red', alpha=0.1, label='Feb 12 Crash')
    
    # Specific annotation for the crash
    crash_date = datetime(2026, 2, 12)
    plt.annotate('Systemic Liquidity Crisis\n(Dash for Cash)', 
                 xy=(crash_date, plot_df.loc['2026-02-12'].min()), 
                 xytext=(datetime(2026, 2, 7), 82),
                 arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=8),
                 fontsize=12, fontweight='bold', bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="black", alpha=0.8))

    # X-Axis formatting for daily precision
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
    plt.xticks(rotation=45)

    plt.title('The February 12 "Everything Crash": Synchronous Liquidation', fontsize=16, fontweight='bold')
    plt.ylabel('Indexed Price (Feb 1 = 100)')
    plt.xlabel('Date')
    plt.legend(loc='lower left')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(f"{ASSETS_DIR}/everything_crash_synchronous.png", dpi=300)
    plt.close()
    
    print("Everything Crash chart generated successfully.")

if __name__ == "__main__":
    df = fetch_data()
    if not df.empty:
        generate_everything_chart(df)
    else:
        print("Error: No data fetched for Everything Crash.")
