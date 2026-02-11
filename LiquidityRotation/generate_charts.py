import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import datetime

# Set visual style
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Inter', 'Roboto', 'Arial']

def fetch_real_data():
    # Define tickers
    tickers = {
        'Bitcoin': 'BTC-USD',
        'S&P 500': 'SPY',
        'Gold': 'GC=F',
        'USD Index': 'DX-Y.NYB'
    }
    
    start_date = '2016-01-01'
    end_date = datetime.now().strftime('%Y-%m-%d')
    
    data = pd.DataFrame()
    for name, ticker in tickers.items():
        print(f"Fetching {name} ({ticker})...")
        df = yf.download(ticker, start=start_date, end=end_date)
        
        if isinstance(df.columns, pd.MultiIndex):
            try:
                data[name] = df.xs('Close', axis=1, level=1).iloc[:,0]
            except (KeyError, IndexError):
                data[name] = df.iloc[:,0]
        else:
            if 'Adj Close' in df.columns:
                data[name] = df['Adj Close']
            elif 'Close' in df.columns:
                data[name] = df['Close']
            else:
                data[name] = df.iloc[:,0]
    
    data = data.ffill().dropna()
    
    # 2026 Projection Logic
    last_real_date = data.index[-1]
    target_date = pd.Timestamp('2026-02-11')
    
    if last_real_date < target_date:
        future_dates = pd.date_range(start=last_real_date + pd.Timedelta(days=1), end=target_date, freq='D')
        future_data = pd.DataFrame(index=future_dates, columns=data.columns)
        total_days = (target_date - last_real_date).days
        days_to_peak = max(1, total_days // 2)
        
        for asset in data.columns:
            last_val = float(data[asset].iloc[-1])
            if asset == 'Bitcoin':
                peak_val = last_val * 2.2
                winter_val = peak_val * 0.72  # Showing a real drop
                path = np.zeros(total_days)
                path[:days_to_peak] = np.linspace(last_val, peak_val, days_to_peak)
                path[days_to_peak:] = np.linspace(peak_val, winter_val, total_days - days_to_peak)
                future_data[asset] = path
            elif asset in ['Gold', 'USD Index']:
                future_data[asset] = np.linspace(last_val, last_val * 1.35, total_days)
            else: # S&P 500
                future_data[asset] = np.linspace(last_val, last_val * 1.15, total_days)
        
        combined_data = pd.concat([data, future_data])
    else:
        combined_data = data
    
    combined_data.columns = [str(c[0]) if isinstance(c, tuple) else str(c) for c in combined_data.columns]
    combined_data = combined_data.astype(float)
    return combined_data

def plot_strength_index(df, output_path, title, is_zoomed=False):
    if is_zoomed:
        df = df[df.index >= '2024-01-01']
    
    # Normalize all to 100 at the start of the visible period
    norm_df = df / df.iloc[0] * 100
    
    plt.figure(figsize=(15, 10))
    
    # Define colors and styles
    colors = {
        'Bitcoin': '#F7931A',    # Orange
        'S&P 500': '#2E7D32',    # Green
        'Gold': '#D4AF37',       # Gold
        'USD Index': '#1565C0'   # Blue
    }
    
    # Plot overlapping lines
    for asset in norm_df.columns:
        lw = 3 if asset == 'Bitcoin' else 2
        alpha = 1.0 if asset == 'Bitcoin' else 0.8
        plt.plot(norm_df.index, norm_df[asset], label=asset, color=colors.get(asset, 'black'), linewidth=lw, alpha=alpha)

    # --- CROSS FILL LOGIC ---
    # We want to highlight when Bitcoin crosses the Safe Haven Basket (Avg of Gold & USD)
    safe_haven_basket = (norm_df['Gold'] + norm_df['USD Index']) / 2
    
    # Fill areas where BTC > Safe Haven (Growth Mode)
    plt.fill_between(norm_df.index, norm_df['Bitcoin'], safe_haven_basket, 
                     where=(norm_df['Bitcoin'] >= safe_haven_basket), 
                     color='#F7931A', alpha=0.1, label='Bitcoin Outperformance')
    
    # Fill areas where Safe Haven > BTC (Rotation Mode)
    plt.fill_between(norm_df.index, norm_df['Bitcoin'], safe_haven_basket, 
                     where=(norm_df['Bitcoin'] < safe_haven_basket), 
                     color='#1565C0', alpha=0.1, label='Safe Haven Rotation')

    plt.title(title, fontsize=22, fontweight='bold', pad=25)
    plt.ylabel('Strength Index (Start = 100)', fontsize=14, fontweight='bold')
    plt.xlabel('Date', fontsize=13)
    
    # Log scale if macro, Linear if micro for better "overlap" comparison in short term
    if not is_zoomed:
        plt.yscale('log')
        plt.ylabel('Strength Index (Log Scale, Start=100)', fontsize=14, fontweight='bold')
    
    plt.legend(loc='upper left', frameon=True, fontsize=12, facecolor='white', framealpha=0.9)
    plt.grid(True, linestyle='--', alpha=0.3)
    
    # Mark real data boundary
    current_time = datetime.now()
    if current_time < norm_df.index[-1] and current_time > norm_df.index[0]:
        plt.axvline(current_time, color='black', linestyle='--', linewidth=2, alpha=0.6)
        plt.text(current_time, plt.ylim()[0]*1.1, ' ← REAL DATA | PROJECTION →', 
                 rotation=90, verticalalignment='bottom', fontweight='bold', fontsize=11, alpha=0.7)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()

if __name__ == "__main__":
    save_dir = "assets"
    os.makedirs(save_dir, exist_ok=True)
    
    print("Executing Overlapping Strength Analytics...")
    try:
        raw_data = fetch_real_data()
        
        # Macro Comparison (2016-2026)
        macro_path = os.path.join(save_dir, "strength_overlap_macro.png")
        plot_strength_index(raw_data, macro_path, 'Macro Analytics: Relative Strength & Rotation Cycles')
        
        # Micro Comparison (2024-2026)
        micro_path = os.path.join(save_dir, "strength_overlap_micro.png")
        plot_strength_index(raw_data, micro_path, 'Micro Analytics: The 2026 Rotation Crossing', is_zoomed=True)
        
        print(f"Success! Charts saved to {save_dir}")
    except Exception as e:
        print(f"Error in pipeline: {e}")
        import traceback
        traceback.print_exc()
