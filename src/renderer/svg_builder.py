# src/renderer/svg_builder.py

import json
import os
from .asset_processor import AssetProcessor
from .config import ZONES, BORDER_STYLES, SEVERITY_COLORS

class SVGRenderer:
    """
    Ingests a Render Instruction Set (RIS) JSON file and dynamically composites
    SVGs from the primitive and glyph libraries to generate a final threat symbol.
    """
    
    def __init__(self, assets_dir="assets", output_dir="output/renders"):
        self.assets_dir = assets_dir
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def build_symbol(self, ris_filepath):
        with open(ris_filepath, 'r', encoding='utf-8') as f:
            ris = json.load(f)
            
        threat_id = ris.get("id", "UNKNOWN")
        severity = ris.get("amplifier", {}).get("severity", 1)
        threat_color = SEVERITY_COLORS.get(severity, "#FFFFFF")
        
        final_svg = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="400" height="400" overflow="visible">',
            f'  <defs><style>.tsl-threat {{ color: {threat_color}; }}</style></defs>',
            '  <g class="tsl-threat">' 
        ]

        # 1. Actor Frame
        frame_shape = ris.get("frame", {}).get("shape", "rectangle")
        dash_style = BORDER_STYLES.get(ris.get("frame", {}).get("border", "solid"), "")
        frame_path = os.path.join(self.assets_dir, "frames", f"frame_{frame_shape}.svg")
        frame_content = AssetProcessor.extract_and_restyle(frame_path, "#000000", 0)
        
        final_svg.extend(['    ', f'    <g {dash_style}>\n      {frame_content}\n    </g>'])

        # 2. Base Geometry
        geometry_type = ris.get("geometry", {}).get("type")
        if geometry_type:
            geom_path = os.path.join(self.assets_dir, "geometries", f"{geometry_type}.svg")
            geom_content = AssetProcessor.extract_and_restyle(geom_path, "#FFFFFF", 0)
            if geom_content:
                final_svg.extend(['    ', f'    <g opacity="0.4">\n      {geom_content}\n    </g>'])

        # 3. Mechanism Glyphs
        final_svg.append('    ')
        for glyph in sorted(ris.get("glyphs", []), key=lambda x: x.get("priority", 99)):
            glyph_path = os.path.join(self.assets_dir, "glyphs", f"{glyph.get('type')}.svg")
            glyph_outline = AssetProcessor.extract_and_restyle(glyph_path, "#000000", 4)
            glyph_core = AssetProcessor.extract_and_restyle(glyph_path, "#FFFFFF", -1)
            
            if glyph_outline and glyph_core:
                z = ZONES.get(glyph.get("zone", "center"))
                transform = f"translate({z['x']}, {z['y']}) scale({z['scale']})"
                final_svg.extend([
                    f'    <g transform="{transform}">',
                    f'      {glyph_outline}',
                    f'      {glyph_core}',
                    '    </g>'
                ])

        # 4. Intent Modifier
        modifier_type = ris.get("modifier", {}).get("type", "none")
        if modifier_type and modifier_type != "none":
            mod_path = os.path.join(self.assets_dir, "modifiers", f"{modifier_type}.svg")
            mod_outline = AssetProcessor.extract_and_restyle(mod_path, "#000000", 4)
            mod_core = AssetProcessor.extract_and_restyle(mod_path, "#FFFFFF", -1)
            
            if mod_outline and mod_core:
                final_svg.extend([
                    '    ', '    <g class="tsl-modifier">',
                    f'      {mod_outline}', f'      {mod_core}',
                    '    </g>'
                ])

        final_svg.extend(['  </g>', '</svg>'])
        
        output_filepath = os.path.join(self.output_dir, f"{threat_id}.svg")
        with open(output_filepath, 'w', encoding='utf-8') as f:
            f.write("\n".join(final_svg))

if __name__ == "__main__":
    renderer = SVGRenderer()
    test_json = "output/ris/TH-TEST-01.json"
    if os.path.exists(test_json):
        renderer.build_symbol(test_json)