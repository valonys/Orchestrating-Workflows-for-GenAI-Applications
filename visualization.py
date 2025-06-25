"""
Visualization module for DigiTwin Analytics
Contains FPSO layout and plotting functions
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.transforms as transforms
import math
import pandas as pd
from utils import log_execution
from config import (
    clv_modules, clv_racks, clv_flare, clv_living_quarters, 
    clv_hexagons, clv_fwd, module_keywords, rack_keywords, 
    flare_keywords, living_quarters_keywords, hexagons_keywords, fwd_keywords,
    paz_modules, paz_racks, paz_flare, paz_living_quarters, 
    paz_hexagons, paz_fwd
)

# PAZ-specific keywords for the new naming convention
paz_module_keywords = ['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8']
paz_rack_keywords = ['R1', 'R2', 'R3', 'R4', 'R5', 'R6']

# --- FPSO LAYOUT FUNCTIONS ---
@log_execution
def add_rectangle(ax, xy, width, height, **kwargs):
    """Add rectangle to matplotlib axis"""
    rectangle = patches.Rectangle(xy, width, height, **kwargs)
    ax.add_patch(rectangle)

@log_execution
def add_chamfered_rectangle(ax, xy, width, height, chamfer, **kwargs):
    """Add chamfered rectangle to matplotlib axis"""
    x, y = xy
    coords = [
        (x + chamfer, y), (x + width - chamfer, y), (x + width, y + chamfer),
        (x + width, y + height - chamfer), (x + width - chamfer, y + height),
        (x + chamfer, y + height), (x, y + height - chamfer), (x, y + chamfer)
    ]
    polygon = patches.Polygon(coords, closed=True, **kwargs)
    ax.add_patch(polygon)

@log_execution
def add_hexagon(ax, xy, radius, **kwargs):
    """Add hexagon to matplotlib axis"""
    x, y = xy
    vertices = [(x + radius * math.cos(2 * math.pi * n / 6), y + radius * math.sin(2 * math.pi * n / 6)) for n in range(6)]
    hexagon = patches.Polygon(vertices, closed=True, **kwargs)
    ax.add_patch(hexagon)

@log_execution
def add_fwd(ax, xy, width, height, **kwargs):
    """Add FWD (Forward) shape to matplotlib axis"""
    x, y = xy
    top_width = width * 0.80
    coords = [
        (0, 0), (width, 0), (width - (width - top_width) / 2, height),
        ((width - top_width) / 2, height)
    ]
    trapezoid = patches.Polygon(coords, closed=True, **kwargs)
    t = transforms.Affine2D().rotate_deg(90).translate(x, y)
    trapezoid.set_transform(t + ax.transData)
    ax.add_patch(trapezoid)
    text_t = transforms.Affine2D().rotate_deg(90).translate(x + height / 2, y + width / 2)
    ax.text(0, -1, "FWD", ha='center', va='center', fontsize=7, weight='bold', transform=text_t + ax.transData)

@log_execution
def draw_clv(ax, df_selected, notification_type, location_counts):
    """Draw CLV FPSO layout"""
    for module, (row, col) in clv_modules.items():
        height, y_position, text_y = (1.25, row, row + 0.5) if module == 'M110' else (1.25, row - 0.25, row + 0.25) if module == 'M120' else (1, row, row + 0.5)
        add_chamfered_rectangle(ax, (col, y_position), 1, height, 0.1, edgecolor='black', facecolor='white')
        ax.text(col + 0.5, text_y, module, ha='center', va='center', fontsize=7, weight='bold')
        if module in module_keywords and int(location_counts['Modules'].loc[module, 'Count']) > 0:
            ax.text(col + 0.8, row + 0.8, f"{int(location_counts['Modules'].loc[module, 'Count'])}", 
                    ha='center', va='center', fontsize=6, weight='bold', color='red')

    for rack, (row, col) in clv_racks.items():
        add_chamfered_rectangle(ax, (col, row), 1, 0.5, 0.05, edgecolor='black', facecolor='white')
        ax.text(col + 0.5, row + 0.25, rack, ha='center', va='center', fontsize=7, weight='bold')
        if rack in rack_keywords and int(location_counts['Racks'].loc[rack, 'Count']) > 0:
            ax.text(col + 0.7, row + 0.4, f"{int(location_counts['Racks'].loc[rack, 'Count'])}", 
                    ha='center', va='center', fontsize=6, weight='bold', color='red')

    for flare_loc, (row, col) in clv_flare.items():
        add_chamfered_rectangle(ax, (col, row), 1, 0.5, 0.05, edgecolor='black', facecolor='white')
        ax.text(col + 0.5, row + 0.25, flare_loc, ha='center', va='center', fontsize=7, weight='bold')
        if flare_loc in flare_keywords and int(location_counts['Flare'].loc[flare_loc, 'Count']) > 0:
            ax.text(col + 0.7, row + 0.4, f"{int(location_counts['Flare'].loc[flare_loc, 'Count'])}", 
                    ha='center', va='center', fontsize=6, weight='bold', color='red')

    for lq, (row, col) in clv_living_quarters.items():
        add_rectangle(ax, (col, row), 1, 2.5, edgecolor='black', facecolor='white')
        ax.text(col + 0.5, row + 1.25, lq, ha='center', va='center', fontsize=7, rotation=90, weight='bold')
        total_lq_count = sum(df_selected['Extracted_LivingQuarters'].str.contains(keyword, na=False).sum() for keyword in living_quarters_keywords)
        if total_lq_count > 0:
            ax.text(col + 0.7, row + 1.4, f"{total_lq_count}", 
                    ha='center', va='center', fontsize=6, weight='bold', color='red')

    for hexagon, (row, col) in clv_hexagons.items():
        add_hexagon(ax, (col, row), 0.60, edgecolor='black', facecolor='white')
        ax.text(col, row, hexagon, ha='center', va='center', fontsize=7, weight='bold')
        if hexagon in hexagons_keywords and int(location_counts['HeliDeck'].loc[hexagon, 'Count']) > 0:
            ax.text(col + 0.2, row + 0.2, f"{int(location_counts['HeliDeck'].loc[hexagon, 'Count'])}", 
                    ha='center', va='center', fontsize=6, weight='bold', color='red')

    for fwd_loc, (row, col) in clv_fwd.items():
        add_fwd(ax, (col, row), 2.5, -1, edgecolor='black', facecolor='white')
        if fwd_loc in fwd_keywords and int(location_counts['FWD'].loc[fwd_loc, 'Count']) > 0:
            ax.text(col + 0.75, row + 1.4, f"{int(location_counts['FWD'].loc[fwd_loc, 'Count'])}", 
                    ha='center', va='center', fontsize=6, weight='bold', color='red')

    total_ni = df_selected[df_selected['Notifictn type'] == 'NI'].shape[0]
    total_nc = df_selected[df_selected['Notifictn type'] == 'NC'].shape[0]
    ax.text(6, 0.25, f"NI: {total_ni}\nNC: {total_nc}", ha='center', va='center', fontsize=8, weight='bold', color='red')

@log_execution
def draw_paz(ax, df_selected, notification_type, location_counts):
    """Draw PAZ FPSO layout"""
    for module, (row, col) in paz_modules.items():
        height, y_position, text_y = (1.25, row, row + 0.5) if module == 'S1' else (1.25, row - 0.25, row + 0.25) if module == 'P1' else (1, row, row + 0.5)
        add_chamfered_rectangle(ax, (col, y_position), 1, height, 0.1, edgecolor='black', facecolor='white')
        ax.text(col + 0.5, text_y, module, ha='center', va='center', fontsize=7, weight='bold')
        if module in paz_module_keywords and int(location_counts['Modules'].loc[module, 'Count']) > 0:
            ax.text(col + 0.8, row + 0.8, f"{int(location_counts['Modules'].loc[module, 'Count'])}", 
                    ha='center', va='center', fontsize=6, weight='bold', color='red')

    for rack, (row, col) in paz_racks.items():
        add_chamfered_rectangle(ax, (col, row), 1, 0.5, 0.05, edgecolor='black', facecolor='white')
        ax.text(col + 0.5, row + 0.25, rack, ha='center', va='center', fontsize=7, weight='bold')
        if rack in paz_rack_keywords and int(location_counts['Racks'].loc[rack, 'Count']) > 0:
            ax.text(col + 0.7, row + 0.4, f"{int(location_counts['Racks'].loc[rack, 'Count'])}", 
                    ha='center', va='center', fontsize=6, weight='bold', color='red')

    for flare_loc, (row, col) in paz_flare.items():
        add_chamfered_rectangle(ax, (col, row), 1, 0.5, 0.05, edgecolor='black', facecolor='white')
        ax.text(col + 0.5, row + 0.25, flare_loc, ha='center', va='center', fontsize=7, weight='bold')
        if flare_loc in flare_keywords and int(location_counts['Flare'].loc[flare_loc, 'Count']) > 0:
            ax.text(col + 0.7, row + 0.4, f"{int(location_counts['Flare'].loc[flare_loc, 'Count'])}", 
                    ha='center', va='center', fontsize=6, weight='bold', color='red')

    for lq, (row, col) in paz_living_quarters.items():
        add_rectangle(ax, (col, row), 1, 2.5, edgecolor='black', facecolor='white')
        ax.text(col + 0.5, row + 1.25, lq, ha='center', va='center', fontsize=7, rotation=90, weight='bold')
        total_lq_count = sum(df_selected['Extracted_LivingQuarters'].str.contains(keyword, na=False).sum() for keyword in living_quarters_keywords)
        if total_lq_count > 0:
            ax.text(col + 0.7, row + 1.4, f"{total_lq_count}", 
                    ha='center', va='center', fontsize=6, weight='bold', color='red')

    for hexagon, (row, col) in paz_hexagons.items():
        add_hexagon(ax, (col, row), 0.60, edgecolor='black', facecolor='white')
        ax.text(col, row, hexagon, ha='center', va='center', fontsize=7, weight='bold')
        if hexagon in hexagons_keywords and int(location_counts['HeliDeck'].loc[hexagon, 'Count']) > 0:
            ax.text(col + 0.2, row + 0.2, f"{int(location_counts['HeliDeck'].loc[hexagon, 'Count'])}", 
                    ha='center', va='center', fontsize=6, weight='bold', color='red')

    for fwd_loc, (row, col) in paz_fwd.items():
        add_fwd(ax, (col, row), 2.5, -1, edgecolor='black', facecolor='white')
        if fwd_loc in fwd_keywords and int(location_counts['FWD'].loc[fwd_loc, 'Count']) > 0:
            ax.text(col + 0.75, row + 1.4, f"{int(location_counts['FWD'].loc[fwd_loc, 'Count'])}", 
                    ha='center', va='center', fontsize=6, weight='bold', color='red')

    total_ni = df_selected[df_selected['Notifictn type'] == 'NI'].shape[0]
    total_nc = df_selected[df_selected['Notifictn type'] == 'NC'].shape[0]
    ax.text(6, 0.25, f"NI: {total_ni}\nNC: {total_nc}", ha='center', va='center', fontsize=8, weight='bold', color='red')

@log_execution
def draw_fpso_layout(selected_unit, df_selected, notification_type, location_counts):
    """Draw FPSO layout for selected unit"""
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 3.5)
    ax.set_aspect('equal')
    ax.grid(False)
    ax.set_facecolor('#E6F3FF')
    if selected_unit == 'CLV':
        draw_clv(ax, df_selected, notification_type, location_counts)
    elif selected_unit == 'PAZ':
        draw_paz(ax, df_selected, notification_type, location_counts)
    else:
        ax.text(6, 1.75, f"{selected_unit} Layout\n(Implementation work in progress...)", 
                ha='center', va='center', fontsize=16, weight='bold')
    plt.title(f"FPSO Visualization - {selected_unit}", fontsize=16, fontfamily='Tw Cen MT')
    return fig 