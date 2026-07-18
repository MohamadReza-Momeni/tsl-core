# src/renderer/config.py

"""
Global rendering configuration for TSL-Core.
Modify these values to adjust symbol placement, borders, and severity colors.
"""

ZONES = {
    "center": {"x": 25, "y": 25, "scale": 0.5},
    "north":  {"x": 35, "y": 0,  "scale": 0.3},
    "south":  {"x": 35, "y": 65, "scale": 0.3}
}

BORDER_STYLES = {
    "solid": "",
    "dashed": 'stroke-dasharray="6 4"',
    "dash-dot": 'stroke-dasharray="6 2 2 2"'
}

SEVERITY_COLORS = {
    1: "#FFFFFF",
    2: "#FFE300",
    3: "#FF8400",
    4: "#FF0000",
    5: "#870000",
    6: "#400000"
}