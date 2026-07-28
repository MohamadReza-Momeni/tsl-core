# src/renderer/config.py

"""
Global rendering configuration for TSL-Core.
"""

# Dynamic zone layouts based on the number of mechanisms (glyphs) present.
# Mathematically aligned to avoid the Diamond frame borders with zero overlap.
# Dynamic zone layouts based on the number of mechanisms (glyphs) present.
# Mathematically aligned to avoid the Diamond frame borders with zero overlap.
ZONES_BY_COUNT = {
    1: {
        # 1 MEC: Massive 40x40 perfectly centered.
        "center": {"x": 30, "y": 30, "scale": 0.40}, 
        "north":  {"x": 30, "y": 30, "scale": 0.40}, # Fallback
        "south":  {"x": 30, "y": 30, "scale": 0.40}  # Fallback
    },
    2: {
        # 2 MECs: Primary is visibly larger (34px) and anchors the bottom. 
        # Secondary is smaller (26px) and sits perfectly on top of it.
        "center": {"x": 33, "y": 44, "scale": 0.34}, # Occupies X: 33-67, Y: 44-78
        "north":  {"x": 37, "y": 18, "scale": 0.26}, # Occupies X: 37-63, Y: 18-44
        "south":  {"x": 33, "y": 44, "scale": 0.34}  # Fallback
    },
    3: {
        # 3 MECs: Pushed to absolute limits. 24x24 center, 22x22 extremities.
        "center": {"x": 38, "y": 38, "scale": 0.24}, 
        "north":  {"x": 39, "y": 16, "scale": 0.22}, 
        "south":  {"x": 39, "y": 62, "scale": 0.22}  
    }
}

BORDER_STYLES = {
    "solid": {
        "black": "",
        "white": ""
    },
    "dashed": {
        "black": 'stroke-dasharray="12 4" stroke-dashoffset="2"',
        "white": 'stroke-dasharray="8 8"'
    },
    "dash-dot": {
        "black": 'stroke-dasharray="12 2 6 2" stroke-dashoffset="2"',
        "white": 'stroke-dasharray="8 6 2 6"'
    }
}

SEVERITY_COLORS = {
    1: "#FFFFFF", 2: "#FFE300", 3: "#FF8400",
    4: "#FF0000", 5: "#870000", 6: "#400000"
}

DOMAIN_BADGES = {
    "radial_network": "ط",     # DOM-01
    "bar_stack": "س",          # DOM-02
    "connected_chain": "ق",    # DOM-03
    "population_cluster": "د", # DOM-04
    "directed_vectors": "ن",   # DOM-05
    "grid": "ج"                # DOM-06
}