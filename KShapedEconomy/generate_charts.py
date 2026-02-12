import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os

# Tickers representing different segments of the economy
tickers = {
    'NVDA': 'AI Infrastructure (The New Oil)',
    'XLK': 'Big Tech / SaaS Ecosystem',
    'SPY': 'S&P 500 (Weighted)',
    'RSP': 'Traditional Business (Equal Weight)',
    'IWM': 'Service Agencies / SMBs (Struggling)'
}

# Start of the AI Boom
start_date = '2023-01-01'
print(f"Fetching data for {list(tickers.keys())} from {start_date}...")

# Fetch data
data = yf.download(list(tickers.keys()), start=start_date)

# Handle MultiIndex columns
if isinstance(data.columns, pd.MultiIndex):
    if 'Adj Close' in data.columns.get_level_values(0):
        data = data['Adj Close']
    elif 'Close' in data.columns.get_level_values(0):
        print("Using 'Close' price...")
        data = data['Close']
    else:
        print("Error: Could not find Close price data.")
        exit(1)
elif 'Adj Close' in data.columns:
    data = data['Adj Close']
elif 'Close' in data.columns:
    data = data['Close']

# Rebase to 100
normalized_data = (data / data.iloc[0]) * 100

# Plotting
plt.style.use('seaborn-v0_8-darkgrid')
fig, ax = plt.subplots(figsize=(14, 8))

# Define colors and line styles for clarity
colors = {
    'NVDA': '#ff0000', # Red for extreme outlier
    'XLK': '#1f77b4',  # Blue for Tech
    'SPY': '#2ca02c',  # Green for Market Benchmark
    'RSP': '#ff7f0e',  # Orange for "Real Economy"
    'IWM': '#bcbd22',  # Yellow/Green for Small Caps
    'MCHI': '#7f7f7f'  # Grey for laggard
}

styles = {
    'NVDA': '-',
    'XLK': '-',
    'SPY': '-',
    'RSP': '--',
    'IWM': '--',
    'MCHI': ':'
}

for ticker, label in tickers.items():
    ax.plot(normalized_data.index, normalized_data[ticker], 
            label=f"{label} (+{normalized_data[ticker].iloc[-1]-100:.1f}%)", 
            color=colors.get(ticker), 
            linestyle=styles.get(ticker),
            linewidth=2 if ticker != 'NVDA' else 3) # Make NVDA stand out

# Chart annotations and styling
ax.set_title("The AI-Driven 'K-Shaped' Economy (Rebased to 100 at Jan 2023)", fontsize=16, fontweight='bold', pad=20)
ax.set_ylabel('Performance (Indexed to 100)', fontsize=12)
ax.set_xlabel('Date (Start of AI Boom)', fontsize=12)

# Format Date Axis
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
plt.xticks(rotation=45)

# Add Legend
ax.legend(fontsize=12, loc='upper left', frameon=True, framealpha=0.9)

# Add Grid
ax.grid(True, linestyle='--', alpha=0.7)

# Add Annotation for K-Shape Split
last_date = normalized_data.index[-1]
# Get y-values for annotation positioning
y_nvda = normalized_data['NVDA'].iloc[-1]
y_iwm = normalized_data['IWM'].iloc[-1]

output_dir = 'assets'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Ensure tight layout
plt.tight_layout()

# Save locally to be picked up
save_path = os.path.join(output_dir, 'k_shaped_economy.png')
plt.savefig(save_path, dpi=300)
print(f"Chart saved to {save_path}")
