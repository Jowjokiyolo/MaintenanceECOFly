import pandas as pd
import matplotlib
matplotlib.use('pdf')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import glob
import os
from datetime import datetime, timedelta

# List of aircraft and corresponding CSV files
aircraft_list = ['PH-EFA', 'PH-EFB', 'PH-EFC', 'PH-EFD', 'PH-EFE', 'PH-EFG']
csv_files = [f"AMP/{ac}.csv" for ac in aircraft_list]

# Read and combine all aircraft data
all_data = []
for ac, file in zip(aircraft_list, csv_files):
    if os.path.exists(file):
        df = pd.read_csv(file)
        if 'Aircraft' not in df.columns:
            df['Aircraft'] = ac
        all_data.append(df)
    else:
        print(f"Warning: {file} not found.")

data = pd.concat(all_data, ignore_index=True)

# Convert 'Base' column to boolean if it's not already
if 'Base' in data.columns:
    data['Base'] = data['Base'].astype(str).str.upper() == 'TRUE'
else:
    data['Base'] = False
    
# Add Days Required column if not present
if 'Days Required' not in data.columns:
    data['Days Required'] = 7  # Default to 1-week maintenance periods

# Filter data to only include second year
year_start_day = 1461
year_end_day = 365*5  # 1825
data = data[(data['Day'] >= year_start_day) & (data['Day'] <= year_end_day)]

# Make a copy with adjusted day values (1-365 instead of 366-730)
display_data = data.copy()
display_data['DisplayDay'] = display_data['Day'] - year_start_day + 1

# Create a figure with gridspec for header and main chart
fig = plt.figure(figsize=(15, 6 + len(aircraft_list)*0.5))
gs = plt.GridSpec(2, 1, height_ratios=[1, 5], hspace=0.05)
plt.rcParams['font.family'] = 'monospace'  # Set all fonts to monospace for consistent spacing

# Top subplot for years and quarters
ax_years = plt.subplot(gs[0])
ax_main = plt.subplot(gs[1])

# Set up the years header - 2026 (second year)
years = [2029]
quarters = ['Q1', 'Q2', 'Q3', 'Q4']
year_positions = []
quarter_width = 365 / 4

# Draw year and quarter labels
for i, year in enumerate(years):
    # Year label centered over the year
    year_start = 1  # Start at day 1 (adjusted)
    year_end = 365  # End at day 365 (adjusted)
    year_center = year_start + (year_end - year_start) / 2
    year_positions.append(year_center)
    
    # Add year labels
    ax_years.text(year_center, 0.7, str(year), ha='center', fontsize=10, fontweight='bold')
    
    # Add quarter background and labels
    for q in range(4):
        q_start = year_start + q * quarter_width
        q_end = year_start + (q + 1) * quarter_width
        q_center = (q_start + q_end) / 2
        
        # Alternate background colors for quarters
        color = '#e6f2ff' if q % 2 == 0 else '#d9e6ff'
        ax_years.axvspan(q_start, q_end, facecolor=color, alpha=0.3)
        ax_years.text(q_center, 0.3, quarters[q], ha='center', fontsize=8)

# Remove year axis decorations
ax_years.set_xlim(0, 365 + 30)  # Year days + padding 
ax_years.set_ylim(0, 1)
ax_years.axis('off')

# Ensure PH-EFA is at the top
sorted_aircraft_list = ['PH-EFA'] + [ac for ac in aircraft_list if ac != 'PH-EFA']

# Setup main chart
ax_main.set_xlim(0, 365 + 30)  # Year days + padding
ax_main.set_ylim(-0.5, len(sorted_aircraft_list) - 0.5)

# Group aircraft by type (from registration)
aircraft_groups = {}
for ac in sorted_aircraft_list:
    # Extract aircraft type from registration (e.g., PH-EFA -> EF)
    ac_type = ac[3:5]  # Assuming format is PH-XXx
    if ac_type not in aircraft_groups:
        aircraft_groups[ac_type] = []
    aircraft_groups[ac_type].append(ac)

# Draw background for each aircraft type group
current_y = 0
group_y_positions = {}
group_colors = {'EF': '#e6f7ff'}  # Add more colors for different types

for ac_type, acs in aircraft_groups.items():
    if ac_type in group_colors:
        group_height = len(acs)
        ax_main.axhspan(current_y - 0.5, current_y + group_height - 0.5,
                      facecolor=group_colors[ac_type], alpha=0.3)
        group_y_positions[ac_type] = (current_y, current_y + group_height)
        current_y += group_height

# Plot each aircraft
for i, ac in enumerate(sorted_aircraft_list):
    ac_data = display_data[display_data['Aircraft'] == ac]
    y_pos = i
    
    # Add horizontal line for this aircraft's timeline
    ax_main.axhline(y=y_pos, color='blue', linestyle='-', linewidth=2, alpha=0.8)
    
    # Plot markers for each event
    if not ac_data.empty:
        # Plot base maintenance days as vertical red blocks
        base_days = ac_data[ac_data['Base'] & ac_data['DisplayDay'].notna()]
        for _, row in base_days.iterrows():
            day = row['DisplayDay']  # Use adjusted day value
            ax_main.bar(day, 0.6, bottom=y_pos-0.3, color='red', width=1, alpha=0.8, zorder=10)
        
        # Plot regular checks with less prominence
        checks = ac_data[~ac_data['Base'] & ac_data['DisplayDay'].notna()]
        if not checks.empty:
            ax_main.scatter(checks['DisplayDay'], [y_pos] * len(checks), 
                         marker='D', color='blue', s=20, zorder=3, alpha=0.5)
        
        # Plot routine checks with less prominence
        routine_checks = ac_data[~ac_data['Base'] & ac_data['DisplayDay'].notna() & (ac_data['Day Hours'] < 2)]
        if not routine_checks.empty:
            ax_main.scatter(routine_checks['DisplayDay'], [y_pos] * len(routine_checks),
                         marker='o', color='green', s=15, zorder=2, alpha=0.5)

ax_main.set_xlabel('Day')
ax_main.set_yticks(range(len(sorted_aircraft_list)))
ax_main.set_yticklabels(sorted_aircraft_list, fontfamily='monospace', fontsize=10)
ax_main.tick_params(axis='y', which='major', pad=15)  # Add more padding to y-axis labels
ax_main.set_title('Year 5 (2029) Maintenance Schedule')

# Create legend with custom handles
legend_elements = [
    mpatches.Patch(facecolor='red', alpha=0.8, label='Base Maintenance')
]
ax_main.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=4)

plt.tight_layout()
plt.subplots_adjust(bottom=0.15)  # Make room for the legend
plt.savefig('gantt_chart_2029.png', dpi=300)