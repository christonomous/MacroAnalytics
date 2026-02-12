import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os

# Set output directory
output_dir = 'assets'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Helper function to clean and normalize data
def clean_and_normalize(df):
    df = df.dropna(how='all').ffill().dropna()
    return (df / df.iloc[0]) * 100

# Chart 1: The Great Divergence (Survival Assets vs Labor Economy)
print("Generating Chart 1: Asset Divergence...")
tickers1 = {
    'BTC-USD': 'Bitcoin (Measurement)',
    'XLK': 'Big Tech (Infrastructure)',
    'GLD': 'Gold (Hedge)',
    'IWM': 'Small Caps (Labor/Legacy)'
}
data1 = yf.download(list(tickers1.keys()), start='2023-01-01')['Close']
norm_data1 = clean_and_normalize(data1)

plt.style.use('seaborn-v0_8-darkgrid')
fig1, ax1 = plt.subplots(figsize=(12, 7))
colors1 = {'BTC-USD': '#F7931A', 'XLK': '#00A4EF', 'GLD': '#F1C40F', 'IWM': '#E74C3C'}

for t, label in tickers1.items():
    ax1.plot(norm_data1.index, norm_data1[t], label=f"{label} (+{norm_data1[t].iloc[-1]-100:.1f}%)", 
             color=colors1[t], linewidth=2.5 if t == 'BTC-USD' else 2)

ax1.set_title("The Great Divergence: Asset Ownership vs Labor Economy", fontsize=14, fontweight='bold')
ax1.legend(loc='upper left', frameon=True)
plt.tight_layout()
fig1.savefig(os.path.join(output_dir, 'asset_divergence.png'), dpi=300)

# Chart 2: The SaaS Trap (Monopolies vs Small SaaS)
print("Generating Chart 2: The SaaS Trap...")
tickers2 = {
    'XLK': 'Big Tech (The Infrastructure)',
    'WCLD': 'Cloud/Small SaaS (The Trap)'
}
data2 = yf.download(list(tickers2.keys()), start='2023-01-01')['Close']
norm_data2 = clean_and_normalize(data2)

fig2, ax2 = plt.subplots(figsize=(12, 7))
ax2.plot(norm_data2.index, norm_data2['XLK'], label=f"Big Tech (+{norm_data2['XLK'].iloc[-1]-100:.1f}%)", color='#00A4EF', linewidth=2.5)
ax2.plot(norm_data2.index, norm_data2['WCLD'], label=f"Small SaaS (+{norm_data2['WCLD'].iloc[-1]-100:.1f}%)", color='#7f7f7f', linestyle='--')
ax2.fill_between(norm_data2.index, norm_data2['WCLD'], norm_data2['XLK'], color='#00A4EF', alpha=0.1, label='The Automation Gap')

ax2.set_title("The SaaS Trap: Winners vs The Replaced", fontsize=14, fontweight='bold')
ax2.legend(loc='upper left')
plt.tight_layout()
fig2.savefig(os.path.join(output_dir, 'saas_trap.png'), dpi=300)

# Chart 3: Fiat Debasement Proxy (Assets vs M2 Approximation)
# We use GLD as a proxy for "Stable Value" to show how much more 'Energy' BTC/XLK capture
print("Generating Chart 3: Capturing Monetary Energy...")
tickers3 = {
    'BTC-USD': 'Bitcoin',
    'XLK': 'Big Tech',
    'GLD': 'Gold (Monetary Baseline)',
}
data3 = yf.download(list(tickers3.keys()), start='2023-01-01')['Close']
norm_data3 = clean_and_normalize(data3)

fig3, ax3 = plt.subplots(figsize=(12, 7))
ax3.plot(norm_data3.index, norm_data3['BTC-USD'], label='Bitcoin', color='#F7931A', linewidth=2.5)
ax3.plot(norm_data3.index, norm_data3['XLK'], label='Big Tech (AI)', color='#00A4EF')
ax3.axhline(100, color='black', linestyle='--', alpha=0.5, label='Original Capital')
ax3.plot(norm_data3.index, norm_data3['GLD'], label='Gold (Store of Value)', color='#F1C40F', linestyle=':')

ax3.set_title("Capturing Monetary Energy in the AI Era", fontsize=14, fontweight='bold')
ax3.set_yscale('log') # Use log scale to show the magnitude of divergence
ax3.legend(loc='upper left')
plt.tight_layout()
fig3.savefig(os.path.join(output_dir, 'monetary_energy.png'), dpi=300)

print("\nAll charts generated in /assets/")
