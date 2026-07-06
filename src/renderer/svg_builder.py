import json
import os
import re

class SVGRenderer:
    """
    Ingests a Render Instruction Set (RIS) JSON file and dynamically composites
    SVGs from the primitive and glyph libraries to generate a final threat symbol.
    """
    
    def __init__(self, assets_dir="assets", output_dir="output/renders"):
        self.assets_dir = assets_dir
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

        self.ZONES = {
            "center": {"x": 25, "y": 25, "scale": 0.5},
            "north":  {"x": 35, "y": 5,  "scale": 0.3},
            "south":  {"x": 35, "y": 65, "scale": 0.3}
        }

        self.BORDER_STYLES = {
            "solid": "",
            "dashed": "stroke-dasharray=\"6 4\"",
            "dash-dot": "stroke-dasharray=\"6 2 2 2\""
        }
        
        self.SEVERITY_COLORS = {
            1: "#FFFFFF", # White (Minimal / Baseline)
            2: "#FDE047", # Yellow Intensity 1 (Soft/Light)
            3: "#EAB308", # Yellow Intensity 2 (Deep/Warning)
            4: "#EF4444", # Red Intensity 1 (Bright/Elevated)
            5: "#DC2626", # Red Intensity 2 (Strong/High)
            6: "#991B1B"  # Red Intensity 3 (Dark/Critical)
        }

    def _extract_svg_content(self, filepath):
        if not os.path.exists(filepath):
            print(f"[WARNING] Asset missing: {filepath}")
            return ""
        with open(filepath, 'r', encoding='utf-8') as f:
            match = re.search(r'<svg[^>]*>(.*?)</svg>', f.read(), re.DOTALL | re.IGNORECASE)
            return match.group(1).strip() if match else ""

    def build_symbol(self, ris_filepath):
        with open(ris_filepath, 'r', encoding='utf-8') as f:
            ris = json.load(f)
            
        threat_id = ris.get("id", "UNKNOWN")
        severity = ris.get("amplifier", {}).get("severity", 1)
        threat_color = self.SEVERITY_COLORS.get(severity, "#E74C3C")
        
        # Initialize the SVG array
        final_svg = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="400" height="400" overflow="visible">',
            '  <defs>',
            '    <style>',
            f'      .tsl-threat {{ color: {threat_color}; }}', 
            '    </style>',
            '  </defs>',
            f'  <g class="tsl-threat">' 
        ]

        # 1. Base Geometry (Background)
        geometry_type = ris.get("geometry", {}).get("type")
        if geometry_type:
            geom_path = os.path.join(self.assets_dir, "geometries", f"{geometry_type}.svg")
            geom_content = self._extract_svg_content(geom_path)
            if geom_content:
                final_svg.append('    ')
                final_svg.append(f'    {geom_content}')

        # 2. Actor Frame
        frame_shape = ris.get("frame", {}).get("shape", "rectangle")
        dash_style = self.BORDER_STYLES.get(ris.get("frame", {}).get("border", "solid"), "")
        frame_content = self._extract_svg_content(os.path.join(self.assets_dir, "frames", f"frame_{frame_shape}.svg"))
        
        final_svg.append('    ')
        final_svg.append(f'    <g {dash_style}>\n      {frame_content}\n    </g>')

        # 3. Mechanism Glyphs
        final_svg.append('    ')
        for glyph in sorted(ris.get("glyphs", []), key=lambda x: x.get("priority", 99)):
            glyph_content = self._extract_svg_content(os.path.join(self.assets_dir, "glyphs", f"{glyph.get('type')}.svg"))
            if glyph_content:
                z_data = self.ZONES.get(glyph.get("zone", "center"))
                transform = f"translate({z_data['x']}, {z_data['y']}) scale({z_data['scale']})"
                final_svg.append(f'    <g transform="{transform}">\n      {glyph_content}\n    </g>')

        # 4. Intent Modifier (Overlay)
        modifier_type = ris.get("modifier", {}).get("type", "none")
        if modifier_type and modifier_type != "none":
            mod_path = os.path.join(self.assets_dir, "modifiers", f"{modifier_type}.svg")
            mod_content = self._extract_svg_content(mod_path)
            if mod_content:
                final_svg.append('    ')
                final_svg.append(f'    <g class="tsl-modifier">\n      {mod_content}\n    </g>')

        # === CRITICAL: Ensure these tags always close! ===
        final_svg.append('  </g>')
        final_svg.append('</svg>')
        
        # Write to file
        output_filepath = os.path.join(self.output_dir, f"{threat_id}.svg")
        with open(output_filepath, 'w', encoding='utf-8') as f:
            f.write("\n".join(final_svg))
            
        print(f"[SUCCESS] Rendered symbol saved to {output_filepath}")

if __name__ == "__main__":
    # Test fallback if run directly
    renderer = SVGRenderer()
    test_json = "output/ris/TH-TEST-01.json"
    if os.path.exists(test_json):
        renderer.build_symbol(test_json)
    else:
        print(f"Cannot find {test_json} to render.")