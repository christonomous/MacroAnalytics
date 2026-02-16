import matplotlib.pyplot as plt
import numpy as np
import os

# Create assets directory if it doesn't exist
assets_dir = 'assets'
if not os.path.exists(assets_dir):
    os.makedirs(assets_dir)

# Set style for premium light mode look
plt.style.use('default')
background_color = '#FFFFFF'
accent_color = '#2E5BFF'     # Modern Royal Blue
secondary_color = '#00D094'  # Emerald Green
text_color = '#1A1A1A'
grid_color = '#F0F0F0'

def apply_light_theme(ax, title):
    ax.set_facecolor(background_color)
    ax.set_title(title, fontsize=18, fontweight='bold', color=text_color, pad=20)
    ax.tick_params(axis='both', colors='#4D4D4D', labelsize=11)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#E0E0E0')
    ax.spines['bottom'].set_color('#E0E0E0')
    ax.grid(True, linestyle='--', alpha=0.5, color='#E0E0E0')

def generate_nomad_growth():
    years = ['2023', '2026']
    nomads = [35, 50] 
    
    fig, ax = plt.subplots(figsize=(10, 6), facecolor=background_color)
    bars = ax.bar(years, nomads, color=[accent_color, '#5E81FF'], alpha=0.9, width=0.6)
    
    apply_light_theme(ax, 'The Global Digital Nomad Explosion')
    ax.set_ylabel('Digital Nomads (Millions)', fontsize=12, color=text_color)
    
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height + 1, f'{height}M', 
                ha='center', va='bottom', fontsize=13, fontweight='bold', color=accent_color)
    
    plt.tight_layout()
    plt.savefig(os.path.join(assets_dir, 'nomad_growth.png'), dpi=300)
    plt.close()

def generate_flag_utility():
    flags = [
        "Citizenship", "Legal Residence", "Business Base", 
        "Asset Haven", "Playgrounds", "Digital Border", "Health Flag"
    ]
    # Representing "Strategic Priority" or "Value Contribution"
    utility_scores = [95, 90, 85, 88, 75, 80, 70]
    
    fig, ax = plt.subplots(figsize=(10, 7), facecolor=background_color)
    y_pos = np.arange(len(flags))
    
    # Use a gradient of colors
    colors = plt.cm.Blues(np.linspace(0.4, 0.9, len(flags)))
    bars = ax.barh(y_pos, utility_scores, color=colors, alpha=0.9)
    
    apply_light_theme(ax, 'The 7 Flags: Strategic Utility (2026)')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(flags, fontsize=12, fontweight='bold')
    ax.set_xlabel('Global Mobility & Protection Score', fontsize=12)
    ax.invert_yaxis() # Highest priority at top
    
    # Add labels on bars
    for i, v in enumerate(utility_scores):
        ax.text(v + 2, i, str(v), color=accent_color, va='center', fontweight='bold')
        
    plt.tight_layout()
    plt.savefig(os.path.join(assets_dir, 'seven_flags.png'), dpi=300)
    plt.close()

def generate_cbi_costs():
    countries = ['Vanuatu', 'St Kitts', 'Turkey', 'Portugal*']
    costs = [130000, 250000, 400000, 540000] # In USD (approx)
    
    fig, ax = plt.subplots(figsize=(10, 6), facecolor=background_color)
    bars = ax.bar(countries, costs, color=secondary_color, alpha=0.8, width=0.6)
    
    apply_light_theme(ax, 'CBI Entry Costs: Minimum Investment (2026)')
    ax.set_ylabel('Minimum Investment (USD)', fontsize=12)
    
    # Format Y axis for currency
    ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, p: format(int(x), ',')))
    
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height + 10000, f'${height/1000:g}k', 
                ha='center', va='bottom', fontsize=12, fontweight='bold', color='#008F68')
    
    plt.annotate('*Portugal: Golden Visa (Investment Fund Route)', xy=(0.02, -0.15), xycoords='axes fraction', fontsize=10, color='grey')
    
    plt.tight_layout()
    plt.savefig(os.path.join(assets_dir, 'cbi_costs.png'), dpi=300)
    plt.close()

def generate_tax_efficiency():
    # Comparing Personal vs Corporate Tax
    # Data represents Max Personal Tax and Corporate Tax rates for 2026
    # Categorized for clearer presentation
    data = {
        'Cayman': [0, 0],
        'Vanuatu': [0, 0],
        'UAE': [0, 9],
        'Andorra': [10, 10],
        'Montenegro': [15, 15],
        'Georgia': [20, 15],
        'Panama': [25, 25],
        'Germany': [45, 30]
    }
    
    labels = list(data.keys())
    personal = [v[0] for v in data.values()]
    corporate = [v[1] for v in data.values()]
    
    x = np.arange(len(labels))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(12, 7), facecolor=background_color)
    rects1 = ax.bar(x - width/2, personal, width, label='Max Personal Tax', color=accent_color, alpha=0.85)
    rects2 = ax.bar(x + width/2, corporate, width, label='Corporate Tax', color='#63D2FF', alpha=0.85)
    
    apply_light_theme(ax, '2026 Tax Sovereignty: From Haven to High-Pressure')
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=11, fontweight='bold', rotation=15)
    ax.set_ylabel('Tax Rate (%)', fontsize=12, fontweight='bold')
    ax.set_ylim(0, 55) # Higher limit for Germany
    
    # Explicitly label 0% and non-zero values
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            label_color = rect.get_facecolor()
            
            if height == 0:
                ax.text(rect.get_x() + rect.get_width()/2, 0.5, '0%', 
                        ha='center', va='bottom', fontsize=9, fontweight='bold', color='#666666')
                ax.plot([rect.get_x(), rect.get_x() + rect.get_width()], [0.1, 0.1], 
                        color=label_color, linewidth=2, alpha=0.4)
            else:
                ax.text(rect.get_x() + rect.get_width()/2, height + 0.5, f'{height}%', 
                        ha='center', va='bottom', fontsize=9, fontweight='bold', color=label_color)

    autolabel(rects1)
    autolabel(rects2)
    
    # Add textual notes for territorial systems
    ax.annotate('*Nations like Panama & Georgia use Territorial taxation', xy=(0.02, -0.18), 
                xycoords='axes fraction', fontsize=10, color='grey', fontstyle='italic')
    
    ax.legend(frameon=False, loc='upper left', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(os.path.join(assets_dir, 'tax_efficiency.png'), dpi=300)
    plt.close()

def generate_e_residency_comparison():
    # Comparing "Sovereignty Scores" (Hypothetical metric based on Tax, Privacy, Lifestyle)
    nations = ['Monaco', 'Switzerland', 'El Salvador', 'Paraguay', 'Malaysia']
    # Scores: Tax Efficiency, Privacy/Safety, Lifestyle/Prestige
    tax_scores = [10, 8, 10, 9, 8]
    privacy_scores = [9, 10, 7, 6, 7]
    lifestyle_scores = [10, 9, 6, 5, 8]
    
    x = np.arange(len(nations))
    width = 0.25
    
    fig, ax = plt.subplots(figsize=(12, 7), facecolor=background_color)
    
    r1 = ax.bar(x - width, tax_scores, width, label='Tax Efficiency', color=accent_color)
    r2 = ax.bar(x, privacy_scores, width, label='Privacy & Safety', color=secondary_color)
    r3 = ax.bar(x + width, lifestyle_scores, width, label='Lifestyle & Prestige', color='#2E5BFF')
    
    apply_light_theme(ax, 'The Sovereignty Stars: Exclusive Jurisdictions (2026)')
    ax.set_xticks(x)
    ax.set_xticklabels(nations, fontsize=11, fontweight='bold')
    ax.set_ylim(0, 12)
    ax.set_ylabel('Sovereignty Score (1-10)', fontsize=12)
    
    ax.legend(frameon=False, loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=3)
    
    # Add annotation for El Salvador
    ax.annotate('Bitcoin\nCitizenship', xy=(2, 10), xytext=(2, 11),
                ha='center', arrowprops=dict(arrowstyle='->', color='gray'))
    
    plt.tight_layout()
    plt.savefig(os.path.join(assets_dir, 'sovereignty_stars.png'), dpi=300)
    plt.close()

if __name__ == "__main__":
    generate_nomad_growth()
    generate_flag_utility()
    generate_cbi_costs()
    generate_tax_efficiency()
    generate_e_residency_comparison()
    print("All charts generated successfully in light mode.")
