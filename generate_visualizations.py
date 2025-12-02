#!/usr/bin/env python3
"""
Vietnam DOOH Advertising Analysis - Visualization Generator
Generates charts for research document visualization
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
import seaborn as sns

# Set professional styling
rcParams['font.family'] = 'Arial'
rcParams['font.size'] = 10
rcParams['axes.labelsize'] = 11
rcParams['axes.titlesize'] = 12
rcParams['xtick.labelsize'] = 9
rcParams['ytick.labelsize'] = 9
rcParams['legend.fontsize'] = 9
rcParams['figure.titlesize'] = 13

# Professional color palette
COLORS = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#6A994E', '#BC4B51', '#8B8C89', '#5C7457']
sns.set_palette(sns.color_palette(COLORS))

# Output directory
OUTPUT_DIR = '/Users/nntrvy/os-adtech-project/'

def create_market_share_chart():
    """Chart 1: Industry Market Share by Spending Volume"""

    industries = ['Retail &\nConsumer Goods', 'FMCG', 'Automotive', 'Telecom &\nTechnology', 'BFSI', 'Healthcare', 'Entertainment\n& Media']
    market_shares = [44.49, 33.71, 12.0, 1.93, 4.5, 2.0, 1.37]  # Estimated values, with key ones from document

    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)

    bars = ax.bar(industries, market_shares, color=COLORS[:len(industries)], edgecolor='white', linewidth=1.5)

    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%',
                ha='center', va='bottom', fontsize=10, fontweight='bold')

    ax.set_ylabel('Market Share (%)', fontweight='bold')
    ax.set_title('Vietnam DOOH Industry Spending Distribution by Market Share (2024)',
                 fontweight='bold', pad=20)
    ax.set_ylim(0, 50)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}chart1_market_share.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("✓ Chart 1 created: Industry Market Share")

def create_growth_rates_chart():
    """Chart 2: Sector Growth Rates Comparison (CAGR)"""

    sectors = ['Telecom &\nTechnology', 'Digital\nDOOH', 'Mall/Retail\nInterior', 'Programmatic\nDOOH (SEA)', 'Total OOH\nMarket']
    cagr_rates = [7.04, 12.54, 7.70, 7.19, 5.74]

    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)

    bars = ax.barh(sectors, cagr_rates, color=COLORS[:len(sectors)], edgecolor='white', linewidth=1.5)

    # Add value labels on bars
    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax.text(width, bar.get_y() + bar.get_height()/2.,
                f'  {width:.2f}%',
                ha='left', va='center', fontsize=10, fontweight='bold')

    ax.set_xlabel('CAGR (Compound Annual Growth Rate %)', fontweight='bold')
    ax.set_title('Vietnam DOOH Sector Growth Rates: CAGR Comparison (2024-2030)',
                 fontweight='bold', pad=20)
    ax.set_xlim(0, 14)
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}chart2_growth_rates.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("✓ Chart 2 created: Sector Growth Rates")

def create_market_size_projections():
    """Chart 3: Market Size Projections (2024-2030)"""

    years = np.array([2024, 2025, 2026, 2027, 2028, 2029, 2030])

    # Conservative projection (5.74% CAGR)
    conservative_base = 107.50
    conservative = conservative_base * (1.0574 ** (years - 2024))

    # Digital DOOH projection (12.54% CAGR)
    digital_dooh = conservative_base * (1.1254 ** (years - 2024))

    # Total market (combining static and digital growth)
    total_market_2024 = 500  # Total OOH market 2024
    total_market = total_market_2024 * (1.0574 ** (years - 2024))

    fig, ax = plt.subplots(figsize=(11, 6), dpi=300)

    ax.plot(years, conservative, marker='o', linewidth=2.5, label='Conservative Projection (5.74% CAGR)',
            color=COLORS[0], markersize=7)
    ax.plot(years, digital_dooh, marker='s', linewidth=2.5, label='Digital DOOH Growth (12.54% CAGR)',
            color=COLORS[1], markersize=7)
    ax.plot(years, total_market, marker='^', linewidth=2.5, label='Total OOH Market (Static + Digital)',
            color=COLORS[2], markersize=7)

    # Add value labels for 2024 and 2030
    for data, label_offset in [(conservative, 10), (digital_dooh, -15), (total_market, 10)]:
        ax.text(2024, data[0], f'${data[0]:.1f}M', ha='right', va='center', fontsize=8)
        ax.text(2030, data[-1], f'${data[-1]:.1f}M', ha='left', va='center', fontsize=8)

    ax.set_xlabel('Year', fontweight='bold')
    ax.set_ylabel('Market Size (USD Million)', fontweight='bold')
    ax.set_title('Vietnam DOOH Market Size Projections (2024-2030)',
                 fontweight='bold', pad=20)
    ax.legend(loc='upper left', framealpha=0.95)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}chart3_market_projections.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("✓ Chart 3 created: Market Size Projections")

def create_geographic_distribution():
    """Chart 4: Geographic Spending Distribution - HCMC vs Hanoi"""

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), dpi=300)

    # Chart 4a: Spending Volume Distribution
    cities = ['HCMC +\nHanoi', 'Secondary\nCities']
    spending_share = [65, 35]  # Estimated 60-70% for tier 1, using 65% midpoint
    colors_geo = [COLORS[0], COLORS[4]]

    wedges, texts, autotexts = ax1.pie(spending_share, labels=cities, autopct='%1.1f%%',
                                         colors=colors_geo, startangle=90,
                                         textprops={'fontsize': 11, 'fontweight': 'bold'},
                                         wedgeprops={'edgecolor': 'white', 'linewidth': 2})

    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(12)
        autotext.set_fontweight('bold')

    ax1.set_title('Geographic Spending\nDistribution (2024)', fontweight='bold', pad=15)

    # Chart 4b: HCMC vs Hanoi Consumer Behavior
    categories = ['Online Time\n(hours/day)', 'Population\n(millions)', 'Market\nPriority']
    hcmc_values = [2.6, 9.4, 10]
    hanoi_values = [3.1, 8.0, 8]

    x = np.arange(len(categories))
    width = 0.35

    bars1 = ax2.bar(x - width/2, hcmc_values, width, label='HCMC', color=COLORS[0], edgecolor='white', linewidth=1.5)
    bars2 = ax2.bar(x + width/2, hanoi_values, width, label='Hanoi', color=COLORS[1], edgecolor='white', linewidth=1.5)

    # Add value labels
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}',
                    ha='center', va='bottom', fontsize=9)

    ax2.set_xticks(x)
    ax2.set_xticklabels(categories)
    ax2.set_ylabel('Value', fontweight='bold')
    ax2.set_title('HCMC vs Hanoi:\nKey Metrics Comparison', fontweight='bold', pad=15)
    ax2.legend()
    ax2.grid(axis='y', alpha=0.3, linestyle='--')
    ax2.set_axisbelow(True)

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}chart4_geographic_distribution.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("✓ Chart 4 created: Geographic Distribution")

def create_format_breakdown():
    """Chart 5: Static vs Digital OOH Format Breakdown"""

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), dpi=300)

    # Chart 5a: Current Market Share (2024)
    formats = ['Static OOH', 'Digital DOOH']
    market_share_2024 = [75.24, 24.76]
    colors_format = [COLORS[5], COLORS[0]]

    wedges, texts, autotexts = ax1.pie(market_share_2024, labels=formats, autopct='%1.1f%%',
                                         colors=colors_format, startangle=90,
                                         textprops={'fontsize': 11, 'fontweight': 'bold'},
                                         wedgeprops={'edgecolor': 'white', 'linewidth': 2},
                                         explode=(0, 0.05))

    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(12)
        autotext.set_fontweight('bold')

    ax1.set_title('Static vs Digital Format\nMarket Share (2024)', fontweight='bold', pad=15)

    # Chart 5b: Format Spending Evolution
    years = [2024, 2025, 2026, 2027, 2028, 2029, 2030]

    # Static OOH (slower growth, starting at $376M = 75.24% of $500M)
    static_base = 376
    static_spending = static_base * (1.03 ** np.array(range(len(years))))  # 3% growth

    # Digital DOOH (12.54% CAGR, starting at $124M = 24.76% of $500M)
    digital_base = 124
    digital_spending = digital_base * (1.1254 ** np.array(range(len(years))))

    ax2.plot(years, static_spending, marker='o', linewidth=2.5, label='Static OOH',
            color=COLORS[5], markersize=7)
    ax2.plot(years, digital_spending, marker='s', linewidth=2.5, label='Digital DOOH (12.54% CAGR)',
            color=COLORS[0], markersize=7)

    # Add annotation for crossover point
    ax2.annotate('Digital growing\n2.5x faster', xy=(2027, 180), xytext=(2026, 250),
                arrowprops=dict(arrowstyle='->', color='black', lw=1.5),
                fontsize=9, fontweight='bold', ha='center')

    ax2.set_xlabel('Year', fontweight='bold')
    ax2.set_ylabel('Spending (USD Million)', fontweight='bold')
    ax2.set_title('Format Spending Evolution\n(2024-2030)', fontweight='bold', pad=15)
    ax2.legend()
    ax2.grid(True, alpha=0.3, linestyle='--')
    ax2.set_axisbelow(True)

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}chart5_format_breakdown.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("✓ Chart 5 created: Format Breakdown")

def create_seasonal_spending():
    """Chart 6: Seasonal Spending Patterns"""

    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    # Traditional pattern (Tet-heavy)
    traditional = [180, 200, 110, 90, 85, 90, 95, 85, 90, 100, 110, 120]

    # Modern pattern (year-round optimized, post-2024 shift)
    modern = [130, 140, 115, 110, 115, 120, 125, 115, 120, 125, 130, 135]

    fig, ax = plt.subplots(figsize=(12, 6), dpi=300)

    x = np.arange(len(months))
    width = 0.35

    bars1 = ax.bar(x - width/2, traditional, width, label='Traditional Pattern (Pre-2024)',
                   color=COLORS[3], alpha=0.8, edgecolor='white', linewidth=1)
    bars2 = ax.bar(x + width/2, modern, width, label='Modern Pattern (Post-2024 Shift)',
                   color=COLORS[0], alpha=0.9, edgecolor='white', linewidth=1)

    # Highlight Tet period (Jan-Feb)
    ax.axvspan(-0.5, 1.5, alpha=0.15, color='red', label='Tet Period')

    # Add annotation for 47% decline
    ax.annotate('47% engagement\ndecline (2024)', xy=(0.5, 190), xytext=(3, 210),
                arrowprops=dict(arrowstyle='->', color='darkred', lw=2),
                fontsize=9, fontweight='bold', color='darkred')

    ax.set_xlabel('Month', fontweight='bold')
    ax.set_ylabel('Relative Spending Index', fontweight='bold')
    ax.set_title('Seasonal DOOH Spending Pattern Evolution: Traditional vs Modern Approach',
                 fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(months)
    ax.legend(loc='upper right')
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}chart6_seasonal_spending.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("✓ Chart 6 created: Seasonal Spending Patterns")

def create_advertiser_budget_allocation():
    """Chart 7: Budget Allocation by Industry (Annual Spending)"""

    industries = ['Retail &\nConsumer\nGoods', 'FMCG', 'Automotive', 'Telecom &\nTechnology', 'BFSI', 'Others']

    # Annual spending in USD millions (estimated from percentages and total market)
    # Using $129.58M (2025 market) as base
    base_market = 129.58
    spending = [
        base_market * 0.4449,  # Retail: $57.6M
        base_market * 0.3371,  # FMCG: $43.7M
        base_market * 0.12,    # Automotive: $15.5M (estimated)
        base_market * 0.0193,  # Telecom: $2.5M
        base_market * 0.045,   # BFSI: $5.8M (estimated)
        base_market * 0.0337   # Others: $4.4M
    ]

    fig, ax = plt.subplots(figsize=(10, 7), dpi=300)

    bars = ax.barh(industries, spending, color=COLORS[:len(industries)], edgecolor='white', linewidth=1.5)

    # Add value labels on bars
    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax.text(width, bar.get_y() + bar.get_height()/2.,
                f'  ${width:.1f}M',
                ha='left', va='center', fontsize=10, fontweight='bold')

    ax.set_xlabel('Annual Spending (USD Million)', fontweight='bold')
    ax.set_title('Vietnam DOOH Annual Budget Allocation by Industry (2025)',
                 fontweight='bold', pad=20)
    ax.set_xlim(0, 65)
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)

    # Add total market size annotation
    ax.text(0.95, 0.05, f'Total Market: ${base_market:.1f}M',
            transform=ax.transAxes, ha='right', va='bottom',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
            fontsize=10, fontweight='bold')

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}chart7_budget_allocation.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("✓ Chart 7 created: Budget Allocation by Industry")

def main():
    """Generate all visualizations"""
    print("\n" + "="*60)
    print("Vietnam DOOH Analysis - Visualization Generator")
    print("="*60 + "\n")

    create_market_share_chart()
    create_growth_rates_chart()
    create_market_size_projections()
    create_geographic_distribution()
    create_format_breakdown()
    create_seasonal_spending()
    create_advertiser_budget_allocation()

    print("\n" + "="*60)
    print("All visualizations created successfully!")
    print(f"Output directory: {OUTPUT_DIR}")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
