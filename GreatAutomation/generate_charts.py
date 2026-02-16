import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import yfinance as yf
import os

# Create assets directory if it doesn't exist
os.makedirs('assets', exist_ok=True)

# Set style
plt.style.use('dark_background')
accent_color = '#00ffcc'  # Neon cyan
secondary_color = '#ff007f'  # Neon pink

def extract_val(series_or_scalar):
    """Robustly extract a scalar value from pandas series or scalar."""
    if hasattr(series_or_scalar, 'iloc'):
        val = series_or_scalar.iloc[0]
    else:
        val = series_or_scalar
    
    if hasattr(val, 'item'):
        return val.item()
    return val

def generate_ai_costs_chart():
    print("Generating AI Training Costs vs Human Labor chart...")
    years = [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]
    # AI training costs (Log scale impact)
    ai_costs = [930, 3288, 160000, 3000000, 10000000, 15000000, 100000000, 200000000]
    # Human labor index (Steady growth)
    labor_index = [100, 103, 106, 110, 115, 122, 128, 134]

    fig, ax1 = plt.subplots(figsize=(12, 7))

    ax1.set_xlabel('Year', color='white', fontsize=12)
    ax1.set_ylabel('AI Training Cost ($)', color=accent_color, fontsize=12)
    ax1.plot(years, ai_costs, marker='o', color=accent_color, linewidth=3, label='AI Model Training Cost')
    ax1.tick_params(axis='y', labelcolor=accent_color)
    ax1.set_yscale('log')
    ax1.grid(True, alpha=0.1)

    ax2 = ax1.twinx()
    ax2.set_ylabel('Human Labor Cost Index', color=secondary_color, fontsize=12)
    ax2.plot(years, labor_index, marker='s', color=secondary_color, linewidth=2, label='Human Labor Cost Index', linestyle='--')
    ax2.tick_params(axis='y', labelcolor=secondary_color)

    plt.title('The Automation Disparity: AI Scaling vs Human Labor', fontsize=16, pad=20, color='white')
    fig.tight_layout()
    plt.savefig('assets/ai_vs_labor.png', dpi=300, facecolor='#121212')
    plt.close()

def generate_smc_chart():
    print("Generating Bitcoin SMC Chart (Order Blocks & FVG)...")
    # Fetch BTC data for the last 60 days
    df = yf.download('BTC-USD', period='60d', interval='1d')
    
    # Check if data is empty
    if df.empty:
        print("Error: No data fetched for BTC-USD")
        return

    # Flatten columns if MultiIndex (sometimes yfinance does this)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    # Prepare for plotting
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # 1. Identify Fair Value Gaps (FVG)
    fvgs = []
    for i in range(1, len(df)-1):
        low_next = extract_val(df['Low'].iloc[i+1])
        high_prev = extract_val(df['High'].iloc[i-1])
        close_curr = extract_val(df['Close'].iloc[i])
        open_curr = extract_val(df['Open'].iloc[i])

        # Bullish FVG
        if low_next > high_prev and close_curr > open_curr:
            fvgs.append({'top': low_next, 'bottom': high_prev, 'index': i})
            
    # 2. Identify Order Blocks (OB)
    obs = []
    for i in range(1, len(df)-2):
        close_curr = extract_val(df['Close'].iloc[i])
        open_curr = extract_val(df['Open'].iloc[i])
        close_next = extract_val(df['Close'].iloc[i+1])
        open_next = extract_val(df['Open'].iloc[i+1])
        close_next2 = extract_val(df['Close'].iloc[i+2])
        high_curr = extract_val(df['High'].iloc[i])
        low_curr = extract_val(df['Low'].iloc[i])

        if close_curr < open_curr and close_next > open_next and close_next2 > open_next:
             obs.append({'top': high_curr, 'bottom': low_curr, 'index': i})

    # Plot Price
    ax.plot(df.index, df['Close'], color='white', alpha=0.3, label='BTC Price')
    
    # Plot Candles (simplified)
    for idx, row in df.iterrows():
        c = extract_val(row['Close'])
        o = extract_val(row['Open'])
        h = extract_val(row['High'])
        l = extract_val(row['Low'])
        color = 'green' if c >= o else 'red'
        ax.vlines(idx, l, h, color=color, linewidth=1)
        ax.vlines(idx, o, c, color=color, linewidth=4)

    # Highlight FVGs
    for fvg in fvgs[-3:]: 
        rect = plt.Rectangle((df.index[fvg['index']], fvg['bottom']), 
                             pd.Timedelta(days=5), fvg['top'] - fvg['bottom'], 
                             color=accent_color, alpha=0.3, label='Fair Value Gap (FVG)')
        ax.add_patch(rect)

    # Highlight Order Blocks
    for ob in obs[-2:]: 
        rect = plt.Rectangle((df.index[ob['index']], ob['bottom']), 
                             pd.Timedelta(days=10), ob['top'] - ob['bottom'], 
                             color=secondary_color, alpha=0.4, label='Institutional Order Block')
        ax.add_patch(rect)

    plt.title('Decoding Institutional Intent: BTC/USD Order Blocks & FVGs', fontsize=16, color='white')
    plt.xlabel('Date', color='white')
    plt.ylabel('Price (USD)', color='white')
    ax.grid(True, alpha=0.05)
    
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys(), loc='upper left')

    plt.savefig('assets/smc_visualization.png', dpi=300, facecolor='#121212')
    plt.close()

if __name__ == "__main__":
    generate_ai_costs_chart()
    generate_smc_chart()
    print("Charts generated successfully in assets/ folder.")
