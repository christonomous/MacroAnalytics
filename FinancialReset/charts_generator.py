import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os

# Set visual style
plt.style.use('seaborn-v0_8-whitegrid')
COLORS = ['#1a2a6c', '#b21f1f', '#fdbb2d', '#20bf6b', '#8854d0', '#4b6584']
FONT_MAIN = 'Inter' # Defaulting to sans-serif if not found
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.titlepad'] = 20
plt.rcParams['axes.labelpad'] = 15

# Ensure assets directory exists
os.makedirs('assets', exist_ok=True)

def save_chart(name):
    plt.tight_layout()
    plt.savefig(f'assets/{name}', dpi=300, bbox_inches='tight')
    plt.close()

# 1. Asset Gap Chart
def chart_asset_gap():
    labels = ['Foreign-held US Assets', 'US-held Foreign Assets', 'The Gap (Net Debt)']
    values = [68.9, 41.0, 27.9]
    colors = ['#1a2a6c', '#4b6584', '#b21f1f']
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(labels, values, color=colors, width=0.6)
    plt.title('A $28 Trillion Imbalance: US Net International Investment Position', fontsize=16, fontweight='bold')
    plt.ylabel('Amount (Trillion USD)', fontsize=12)
    
    # Add values on top
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 1, f'${yval}T', ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    plt.ylim(0, 80)
    save_chart('asset_gap.png')

# 2. Foreign Treasury Holdings Trend
def chart_treasury_holdings():
    years = [2012, 2014, 2016, 2018, 2020, 2022, 2024, 2025]
    china = [1.2, 1.3, 1.1, 1.15, 1.05, 0.9, 0.75, 0.68]
    japan = [1.1, 1.2, 1.1, 1.05, 1.25, 1.1, 1.15, 1.2]
    russia = [0.16, 0.14, 0.08, 0.015, 0.005, 0.002, 0.000, 0.000]
    saudi = [0.06, 0.08, 0.10, 0.16, 0.18, 0.12, 0.14, 0.15]
    eu = [0.8, 0.9, 1.1, 1.3, 1.6, 1.8, 1.9, 2.0]
    
    plt.figure(figsize=(12, 7))
    plt.plot(years, china, label='China', color='#b21f1f', linewidth=3, marker='o')
    plt.plot(years, japan, label='Japan', color='#1a2a6c', linewidth=2, marker='D')
    plt.plot(years, russia, label='Russia', color='#4b6584', linewidth=2, linestyle='--')
    plt.plot(years, saudi, label='Saudi Arabia', color='#20bf6b', linewidth=2)
    plt.plot(years, eu, label='European Union', color='#fdbb2d', linewidth=4, marker='*')
    
    plt.title('Divergent Paths: Major Holders of US Treasuries (2012-2025)', fontsize=16, fontweight='bold')
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Amount (Trillion USD)', fontsize=12)
    plt.legend(frameon=True, fontsize=10)
    plt.annotate('EU now the largest holder', xy=(2025, 2.0), xytext=(2021, 2.1),
                 arrowprops=dict(facecolor='black', shrink=0.05), fontsize=10)
    
    save_chart('treasury_holdings.png')

# 3. EU Holdings of US Assets
def chart_eu_holdings():
    labels = ['US Equities', 'US Treasuries', 'US Corporate Bonds']
    sizes = [6, 2, 2] # Trillions
    colors = ['#1a2a6c', '#fdbb2d', '#4b6584']
    
    plt.figure(figsize=(9, 9))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors, 
            pctdistance=0.85, explode=(0.05, 0, 0), textprops={'fontsize': 12, 'fontweight': 'bold'})
    
    # Draw circle for donut chart
    centre_circle = plt.Circle((0,0), 0.70, fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    
    plt.title('Composition of EU Investment in US Assets ($10 Trillion Total)', fontsize=16, fontweight='bold')
    save_chart('eu_holdings.png')

# 4. Foreign Treasury Buying 2025
def chart_treasury_buying():
    labels = ['European Union', 'Rest of the World']
    sizes = [80, 20]
    colors = ['#fdbb2d', '#4b6584']
    
    plt.figure(figsize=(10, 6))
    plt.barh(labels, sizes, color=colors)
    plt.title('Share of Net Foreign US Treasury Purchases (2025)', fontsize=16, fontweight='bold')
    plt.xlabel('Percentage (%)', fontsize=12)
    
    for i, v in enumerate(sizes):
        plt.text(v + 1, i, f'{v}%', va='center', fontweight='bold')
        
    plt.xlim(0, 100)
    save_chart('treasury_buying.png')

# 5. Refinancing Supply Shock
def chart_refinancing_shock():
    categories = ['US Debt to Refinance (2026)', 'Total US GDP']
    values = [8, 28]
    colors = ['#b21f1f', '#1a2a6c']
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(categories, values, color=colors, width=0.5)
    plt.title('The 2026 Refinancing Wall', fontsize=16, fontweight='bold')
    plt.ylabel('Amount (Trillion USD)', fontsize=12)
    
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 0.5, f'${yval}T', ha='center', fontweight='bold')
        
    plt.ylim(0, 35)
    plt.annotate('25% of GDP needs re-issuance', xy=(0, 8), xytext=(0.5, 15),
                 arrowprops=dict(facecolor='black', shrink=0.05), fontsize=12, fontweight='bold', color='#b21f1f')
    
    save_chart('refinancing_shock.png')

# 6. Central Bank Gold vs Treasuries
def chart_gold_vs_treasuries():
    years = [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
    # Trends normalized to 100 for visual clarity of the divergence
    treasuries = [100, 98, 97, 95, 96, 94, 92, 88, 85, 82, 80]
    gold = [100, 102, 105, 110, 118, 125, 130, 145, 160, 185, 210]
    
    plt.figure(figsize=(12, 7))
    plt.plot(years, treasuries, label='US Treasury Reserves', color='#4b6584', linewidth=3, marker='v')
    plt.plot(years, gold, label='Gold Reserves', color='#fdbb2d', linewidth=4, marker='o')
    
    plt.fill_between(years, gold, treasuries, color='#fdbb2d', alpha=0.1)
    
    plt.title('The Great Diversification: Global Central Bank Reserves (Index 2015=100)', fontsize=16, fontweight='bold')
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Asset Index Value', fontsize=12)
    plt.legend(fontsize=12)
    
    plt.annotate('Flight to Hard Assets', xy=(2025, 210), xytext=(2021, 180),
                 arrowprops=dict(facecolor='black', shrink=0.05), fontsize=12, color='#1a2a6c', fontweight='bold')
    
    save_chart('gold_vs_treasuries.png')

if __name__ == "__main__":
    print("Generating charts...")
    chart_asset_gap()
    print("1/6: Asset Gap completed.")
    chart_treasury_holdings()
    print("2/6: Treasury Holdings Trend completed.")
    chart_eu_holdings()
    print("3/6: EU Holdings completed.")
    chart_treasury_buying()
    print("4/6: Treasury Buying completed.")
    chart_refinancing_shock()
    print("5/6: Refinancing Shock completed.")
    chart_gold_vs_treasuries()
    print("6/6: Gold vs Treasuries completed.")
    print("All charts generated in assets/ folder.")
