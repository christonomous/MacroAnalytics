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

def generate_market_divergence():
    print("Generating Market Divergence (AI vs SPY)...")
    end_date = datetime.now()
    start_date = end_date - timedelta(days=5*365)
    
    ai_tickers = ["NVDA", "MSFT", "GOOGL", "AMZN", "META", "AVGO", "TSM"]
    spy_ticker = "SPY"
    
    data = yf.download(ai_tickers + [spy_ticker], start=start_date, end=end_date)
    print("Columns in data:", data.columns)
    
    # In recent yfinance, columns might be (Ticker, Column) or (Column, Ticker)
    # Let's try to get 'Adj Close' specifically
    try:
        if isinstance(data.columns, pd.MultiIndex):
            # Try finding 'Adj Close' in levels
            if 'Adj Close' in data.columns.levels[0]:
                adj_close = data['Adj Close']
            elif 'Adj Close' in data.columns.levels[1]:
                adj_close = data.xs('Adj Close', axis=1, level=1)
            else:
                # If 'Adj Close' is missing, try 'Close'
                adj_close = data['Close']
        else:
            adj_close = data['Adj Close'] if 'Adj Close' in data.columns else data['Close']
    except Exception as e:
        print(f"Error getting columns: {e}")
        # Last resort: use what's available
        adj_close = data
    
    # Normalize to 100
    normalized_data = (adj_close / adj_close.iloc[0]) * 100
    
    ai_leaders = normalized_data[ai_tickers].mean(axis=1)
    spy = normalized_data[spy_ticker]
    
    plt.figure(figsize=(12, 7))
    plt.plot(ai_leaders.index, ai_leaders, label="AI Leaders Index", color="#2979ff", linewidth=2.5)
    plt.plot(spy.index, spy, label="S&P 500 (SPY)", color="#f50057", linewidth=2.0, alpha=0.8)
    
    plt.title("The Great Divergence: AI Leaders vs. Traditional Market")
    plt.xlabel("Year")
    plt.ylabel("Normalized Performance (Base 100)")
    plt.legend()
    plt.tight_layout()
    plt.savefig('assets/market_divergence.png', dpi=300)
    plt.close()

def generate_china_divestment():
    print("Generating China Divestment Chart...")
    # Using data points from FACTS.md for the "future/current" part
    # Peak: $1.32T (2013), Feb 2026: $682B
    years = [2013, 2015, 2017, 2019, 2021, 2023, 2025, 2026]
    holdings = [1320, 1250, 1150, 1070, 1040, 850, 750, 682] # In Billion USD
    
    df = pd.DataFrame({'Year': years, 'Holdings': holdings})
    
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df, x='Year', y='Holdings', marker='o', markersize=8, color="#d32f2f", linewidth=3)
    plt.fill_between(df['Year'], df['Holdings'], color="#d32f2f", alpha=0.1)
    
    plt.title("China's Structural Exit from U.S. Debt")
    plt.ylabel("U.S. Treasury Holdings ($ Billions)")
    plt.xlabel("Year")
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.tight_layout()
    plt.savefig('assets/china_divestment.png', dpi=300)
    plt.close()

def generate_gold_vs_treasuries():
    print("Generating Gold vs Treasuries Share...")
    # Data from FACTS.md: 
    # Treasuries dropped from 30%+ to 23%
    # Gold rose to 27%
    labels = ['U.S. Treasuries', 'Gold']
    shares_2010s = [32, 18]
    shares_2026 = [23, 27]
    
    x = range(len(labels))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(10, 6))
    rects1 = ax.bar([i - width/2 for i in x], shares_2010s, width, label='2010s Average', color='#bdbdbd')
    rects2 = ax.bar([i + width/2 for i in x], shares_2026, width, label='Feb 2026', color=['#1976d2', '#fbc02d'])
    
    ax.set_ylabel('Percentage of Central Bank Reserves (%)')
    ax.set_title('The Safe Haven Flip: Gold Surpasses Treasuries')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    
    plt.tight_layout()
    plt.savefig('assets/safe_haven_flip.png', dpi=300)
    plt.close()

def generate_job_exposure():
    print("Generating AI Job Exposure Chart...")
    # Data from FACTS.md
    categories = ['Advanced Economies\n(US, UK, CH)', 'Low-Income Economies']
    exposure = [60, 26]
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(categories, exposure, color=['#e53935', '#43a047'], width=0.6)
    
    plt.title("AI Exposure Paradox: Debt vs Displacement")
    plt.ylabel("Job Exposure to AI (%)")
    plt.ylim(0, 100)
    
    # Add data labels
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 2, f'{yval}%', ha='center', va='bottom', fontsize=12, fontweight='bold')

    plt.tight_layout()
    plt.savefig('assets/job_exposure.png', dpi=300)
    plt.close()

if __name__ == "__main__":
    set_style()
    generate_market_divergence()
    generate_china_divestment()
    generate_gold_vs_treasuries()
    generate_job_exposure()
    print("Done! Charts generated in assets/ directory.")
