"""
Global rendering configuration for TSL-Core.
"""

# Mathematically calculated to avoid all frame borders (especially Diamond) 
# and guarantee zero overlap between multiple mechanisms.
ZONES = {
    "center": {"x": 32, "y": 32, "scale": 0.36}, # Occupies X: 32-68, Y: 32-68
    "north":  {"x": 41, "y": 14, "scale": 0.18}, # Occupies X: 41-59, Y: 14-32
    "south":  {"x": 41, "y": 68, "scale": 0.18}  # Occupies X: 41-59, Y: 68-86
}

# Advanced Halo Stacking: Black dashes start 2px earlier and end 2px later to cap the ends!
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
    1: "#FFFFFF",
    2: "#FFE300",
    3: "#FF8400",
    4: "#FF0000",
    5: "#870000",
    6: "#400000"
}

# Add this mapping to your config.py
# Maps the existing geometry types to their corresponding Persian Domain Letter
DOMAIN_BADGES = {
    "radial_network": "ط",     # DOM-01
    "bar_stack": "س",          # DOM-02
    "connected_chain": "ق",    # DOM-03
    "population_cluster": "د", # DOM-04
    "directed_vectors": "ن",   # DOM-05
    "grid": "ج"                # DOM-06
}

# DOMAIN_BADGES = {
#     "radial_network": "I",     # DOM-01
#     "bar_stack": "C",          # DOM-02
#     "connected_chain": "E",    # DOM-03
#     "population_cluster": "D", # DOM-04
#     "directed_vectors": "M",   # DOM-05
#     "grid": "S"                # DOM-06
# }