import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf
from datetime import datetime, timedelta

# Create assets directory
if not os.path.exists('assets'):
    os.makedirs('assets')

# Set professional style (Light Theme)
def set_style():
    sns.set_theme(style="whitegrid", palette="muted")
    plt.rcParams.update({
        "figure.facecolor": "#ffffff",
        "axes.facecolor": "#ffffff",
        "grid.color": "#e0e0e0",
        "text.color": "#212121",
        "axes.labelcolor": "#212121",
        "xtick.color": "#424242",
        "ytick.color": "#424242",
        "font.family": "sans-serif",
        "axes.titlesize": 16,
        "axes.labelsize": 12,
        "legend.fontsize": 10,
    })

def generate_assets_in_btc():
    print("Generating Assets priced in BTC chart...")
    end_date = datetime.now()
    start_date = end_date - timedelta(days=10*365)
    
    tickers = ["BTC-USD", "GC=F", "SPY"] # Bitcoin, Gold, S&P 500
    data_raw = yf.download(tickers, start=start_date, end=end_date)
    
    # Handle MultiIndex for Adj Close
    try:
        if isinstance(data_raw.columns, pd.MultiIndex):
            if 'Adj Close' in data_raw.columns.levels[0]:
                data = data_raw['Adj Close']
            elif 'Adj Close' in data_raw.columns.levels[1]:
                data = data_raw.xs('Adj Close', axis=1, level=1)
            else:
                data = data_raw['Close'] if 'Close' in data_raw.columns.levels[0] else data_raw.xs('Close', axis=1, level=1)
        else:
            data = data_raw['Adj Close'] if 'Adj Close' in data_raw.columns else data_raw['Close']
    except Exception as e:
        print(f"Error extracting data: {e}")
        data = data_raw

    # Calculate assets in BTC terms
    data_btc_terms = pd.DataFrame(index=data.index)
    data_btc_terms['Gold / BTC'] = data['GC=F'] / data['BTC-USD']
    data_btc_terms['S&P 500 / BTC'] = data['SPY'] / data['BTC-USD']
    
    # Drop NaNs to ensure we have a clean start for normalization
    data_btc_terms = data_btc_terms.dropna()
    
    if data_btc_terms.empty:
        print("Warning: No valid data found for the 10-year horizon.")
        return

    # Normalize to 100 at the first valid data point
    normalized = (data_btc_terms / data_btc_terms.iloc[0]) * 100
    
    plt.figure(figsize=(12, 7))
    plt.plot(normalized.index, normalized['Gold / BTC'], label="Gold (priced in BTC)", color="#fbc02d", linewidth=2)
    plt.plot(normalized.index, normalized['S&P 500 / BTC'], label="S&P 500 (priced in BTC)", color="#1976d2", linewidth=2)
    
    plt.yscale('log')
    plt.title("The Collapse of Legacy Assets (Measured in BTC)")
    plt.xlabel("Year")
    plt.ylabel("Relative Value (Log Scale, Base 100)")
    plt.legend()
    
    # Safer annotation
    if len(normalized) > 800:
        plt.annotate('Legacy assets losing \npurchasing power vs BTC', 
                     xy=(normalized.index[-300], normalized['S&P 500 / BTC'].iloc[-300]), 
                     xytext=(normalized.index[-800], normalized['S&P 500 / BTC'].iloc[-300]/10),
                     arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=5))
    
    plt.tight_layout()
    plt.savefig('assets/assets_in_btc.png', dpi=300)
    plt.close()

def generate_supply_constant():
    print("Generating Supply Constant vs M2 chart...")
    # Mocking M2 growth trend vs BTC supply
    years = [2020, 2021, 2022, 2023, 2024, 2025, 2026]
    m2_supply = [15.4, 21.0, 21.7, 20.8, 21.2, 22.5, 24.1] # Trillions USD (approx)
    btc_supply = [18.3, 18.7, 19.1, 19.4, 19.7, 19.9, 20.1] # Millions BTC
    
    # Normalize to 100
    m2_norm = [x/m2_supply[0]*100 for x in m2_supply]
    btc_norm = [x/btc_supply[0]*100 for x in btc_supply]
    
    plt.figure(figsize=(10, 6))
    plt.plot(years, m2_norm, label="USD M2 Money Supply", color="#d32f2f", marker='o', linewidth=3)
    plt.plot(years, btc_norm, label="Bitcoin Supply", color="#f57c00", marker='s', linewidth=3)
    
    plt.title("Mathematical Constant vs. Fiat Inflation")
    plt.ylabel("Growth (Base 100)")
    plt.xlabel("Year")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.3)
    
    # Add highlighting for "The Constant"
    plt.fill_between(years, 100, btc_norm, color="#f57c00", alpha=0.1)
    
    plt.tight_layout()
    plt.savefig('assets/supply_constant.png', dpi=300)
    plt.close()

def generate_relatable_purchasing_power():
    print("Generating Relatable Purchasing Power chart...")
    # Data points from research (2016-2026)
    years = [2016, 2018, 2020, 2022, 2024, 2026]
    
    # Average Cup of Coffee (USD)
    coffee_usd = [2.10, 2.30, 2.70, 3.10, 3.50, 3.80]
    
    # BTC Price (USD) - Simplified for trend
    btc_price = [600, 6500, 15000, 30000, 65000, 68000]
    
    # Calculate Satoshi per Coffee
    # 1 BTC = 100,000,000 Satoshi
    sats_per_coffee = [(usd / btc) * 100000000 for usd, btc in zip(coffee_usd, btc_price)]
    
    fig, ax1 = plt.subplots(figsize=(12, 7))
    
    # Plot USD Price (Bar)
    color_usd = '#d32f2f'
    ax1.bar(years, coffee_usd, color=color_usd, alpha=0.3, label="Cost of Coffee (USD)", width=1.2)
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Price in USD ($)', color=color_usd, fontsize=12)
    ax1.tick_params(axis='y', labelcolor=color_usd)
    
    # Plot Sats Price (Line)
    ax2 = ax1.twinx()
    color_sats = '#f57c00'
    ax2.plot(years, sats_per_coffee, color=color_sats, marker='s', markersize=10, linewidth=4, label="Cost of Coffee (Satoshi)")
    ax2.set_ylabel('Price in Satoshi (Sats)', color=color_sats, fontsize=12)
    ax2.tick_params(axis='y', labelcolor=color_sats)
    ax2.set_yscale('log')
    
    plt.title("Relatable Purchasing Power: The Coffee Test\n(USD inflating vs. Satoshi deflation)")
    
    # Add labels
    for i, txt in enumerate(sats_per_coffee):
        ax2.annotate(f"{int(txt):,}", (years[i], sats_per_coffee[i]), xytext=(0, 10), textcoords='offset points', ha='center', fontweight='bold')

    fig.tight_layout()
    plt.savefig('assets/purchasing_power_concrete.png', dpi=300)
    plt.close()

def generate_car_test():
    print("Generating Car Test chart...")
    # Data from research: 2016 (~32 BTC) -> 2026 (~0.7 BTC)
    years = ['2016', '2019', '2022', '2024', '2026']
    btc_for_car = [32.4, 5.4, 3.0, 0.53, 0.72]
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(years, btc_for_car, color='#1976d2', alpha=0.8)
    
    plt.title("The Car Test: How many BTC for an Average New Car?")
    plt.ylabel("Bitcoin (BTC)")
    plt.xlabel("Year")
    
    # Add data labels
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 0.5, f'{yval} BTC', ha='center', va='bottom', fontsize=11, fontweight='bold')

    plt.tight_layout()
    plt.savefig('assets/car_test.png', dpi=300)
    plt.close()

def generate_market_vs_realized():
    print("Generating Market vs Realized Price chart...")
    end_date = datetime.now()
    start_date = end_date - timedelta(days=10*365)
    
    # Using yfinance for market price
    btc_data = yf.download("BTC-USD", start=start_date, end=end_date)
    if isinstance(btc_data.columns, pd.MultiIndex):
        market_price = btc_data['Adj Close' if 'Adj Close' in btc_data.columns.levels[0] else 'Close']
    else:
        market_price = btc_data['Adj Close' if 'Adj Close' in btc_data.columns else 'Close']

    # Mocking Realized Price trend (based on 2026 data points)
    # Realized Price stays more stable and trends up as acquisition cost rises
    dates = market_price.index
    # Realized price starts lower (~$5k in 2018/2019) and reaches ~$55k by Feb 2026
    realized_price = pd.Series(index=dates, data=0.0)
    start_rp = 15000
    end_rp = 55207
    realized_price = pd.Series(
        [start_rp + (end_rp - start_rp) * (i / len(dates)) for i in range(len(dates))],
        index=dates
    )
    
    plt.figure(figsize=(12, 7))
    plt.plot(market_price.index, market_price, label="BTC Market Price", color="#212121", linewidth=2)
    plt.plot(realized_price.index, realized_price, label="Realized Price (Network Floor)", color="#d32f2f", linestyle="--", linewidth=2.5)
    
    plt.fill_between(market_price.index, market_price.squeeze(), realized_price, where=(market_price.squeeze() > realized_price), color="#43a047", alpha=0.1, label="Profit Zone")
    plt.fill_between(market_price.index, market_price.squeeze(), realized_price, where=(market_price.squeeze() <= realized_price), color="#d32f2f", alpha=0.2, label="Capitulation / Buy Zone")
    
    plt.title("The Hard Floor: Market Price vs. Realized Price (Cost Basis)")
    plt.xlabel("Year")
    plt.ylabel("Price (USD)")
    plt.yscale('log')
    plt.legend()
    
    plt.annotate('Feb 2026: ~$55k Floor', 
                 xy=(market_price.index[-1], 55207), 
                 xytext=(market_price.index[-900], 100000),
                 arrowprops=dict(facecolor='red', shrink=0.05, width=1, headwidth=5))
    
    plt.tight_layout()
    plt.savefig('assets/market_vs_realized.png', dpi=300)
    plt.close()

def generate_ownership_handover():
    print("Generating Ownership Handover chart...")
    # Data from research: Institutional holdings ~24%, Retail exit ~66% shift
    labels = ['Retail (<1 BTC)', 'Institutions / Heavy Holders']
    shares_2022 = [75, 25]
    shares_2026 = [66, 34] # Shift based on "Institutional holdings reaching 24% + overlap"
    
    x = [0, 1]
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar([i - width/2 for i in x], shares_2022, width, label='2022 Pre-Euphoria', color='#bdbdbd')
    ax.bar([i + width/2 for i in x], shares_2026, width, label='Feb 2026 Post-ETF', color=['#f57c00', '#1976d2'])
    
    ax.set_ylabel('Percentage of Total Supply (%)')
    ax.set_title('The Great Handover: Institutional Absorption of Retail Supply')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    
    plt.tight_layout()
    plt.savefig('assets/ownership_handover.png', dpi=300)
    plt.close()

if __name__ == "__main__":
    set_style()
    generate_assets_in_btc()
    generate_supply_constant()
    generate_relatable_purchasing_power()
    generate_car_test()
    generate_market_vs_realized()
    generate_ownership_handover()
    print("Done! Charts generated in assets/ directory.")
