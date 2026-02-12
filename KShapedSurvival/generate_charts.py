import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os

# Tickers representing the "Survival Assets" vs the "Struggling Economy"
tickers = {
    'BTC-USD': 'Bitcoin (Measurement)',
    'XLK': 'Big Tech (Infrastructure)',
    'XLE': 'Energy (Commodities)',
    'GLD': 'Gold (Hedge)',
    'IWM': 'Small Caps (Legacy/Labor)'
}

# Start of the AI Boom (Approx Jan 2023)
start_date = '2023-01-01'
print(f"Fetching data from {start_date}...")

# Fetch data
data = yf.download(list(tickers.keys()), start=start_date)

# Handle MultiIndex columns
if isinstance(data.columns, pd.MultiIndex):
    if 'Adj Close' in data.columns.get_level_values(0):
        data = data['Adj Close']
    elif 'Close' in data.columns.get_level_values(0):
        data = data['Close']
    else:
        print("Error: Could not find Close price data.")
        exit(1)
elif 'Adj Close' in data.columns:
    data = data['Adj Close']
elif 'Close' in data.columns:
    data = data['Close']

# Handle NaN from different trading days (Stocks vs Crypto)
# Crypto trades 24/7, stocks only on business days
# Drop rows where everything is NaN (weekends/holidays) then ffill for stock-gaps on crypto-days
data = data.dropna(how='all').ffill()

# Drop the first few rows if they contain NaNs for stocks (e.g. holiday on Jan 1)
# This ensures we rebase to a day where all tickers have data
data = data.dropna()

# Rebase to 100 for comparison
normalized_data = (data / data.iloc[0]) * 100

# Plotting
plt.style.use('seaborn-v0_8-darkgrid')
fig, ax = plt.subplots(figsize=(14, 8))

# Define colors for the "Stay Meaningful" vs "Struggling" narrative
colors = {
    'BTC-USD': '#F7931A', # Bitcoin Orange
    'XLK': '#00A4EF',     # Microsoft/Tech Blue
    'XLE': '#2ECC71',     # Energy Green
    'GLD': '#F1C40F',     # Gold
    'IWM': '#E74C3C'      # Small Cap Red (The "Lower K")
}

for ticker, label in tickers.items():
    ax.plot(normalized_data.index, normalized_data[ticker], 
            label=f"{label} (+{normalized_data[ticker].iloc[-1]-100:.1f}%)", 
            color=colors.get(ticker), 
            linewidth=2.5 if ticker == 'BTC-USD' else 2)

# Chart annotations
ax.set_title("The Great Divergence: Asset Ownership vs Labor Economy (2023-Present)", fontsize=16, fontweight='bold', pad=20)
ax.set_ylabel('Performance (Indexed to 100)', fontsize=12)
ax.set_xlabel('Date (AI Boom Era)', fontsize=12)

# Format Axis
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
plt.xticks(rotation=45)

# Legend and Aesthetics
ax.legend(fontsize=11, loc='upper left', frameon=True, framealpha=0.9)
ax.grid(True, linestyle='--', alpha=0.6)

# Save
output_dir = 'assets'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

plt.tight_layout()
save_path = os.path.join(output_dir, 'asset_divergence.png')
plt.savefig(save_path, dpi=300)
print(f"Chart saved to {save_path}")

print("\nFinal Performance Figures:")
for ticker in tickers:
    perf = normalized_data[ticker].iloc[-1] - 100
    print(f"{ticker}: {perf:+.1f}%")
