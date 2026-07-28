import json
import os
from .asset_processor import AssetProcessor
from .config import ZONES_BY_COUNT, BORDER_STYLES, SEVERITY_COLORS, DOMAIN_BADGES

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
        
        # 1. Initialize Canvas (Standard 100x100 viewBox)
        final_svg = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="400" height="400" overflow="visible">',
            f'  <defs><style>.tsl-threat {{ color: {threat_color}; }}</style></defs>',
            '  <g class="tsl-threat">' 
        ]

        # 2. Actor Frame (Multi-layer for Halo Dashes)
        frame_shape = ris.get("frame", {}).get("shape", "rectangle")
        border_type = ris.get("frame", {}).get("border", "solid")
        dash_styles = BORDER_STYLES.get(border_type, BORDER_STYLES["solid"])
        
        frame_path = os.path.join(self.assets_dir, "frames", f"frame_{frame_shape}.svg")
        frame_fill = AssetProcessor.extract_and_restyle(frame_path, fill_override="currentColor", stroke_override="none")
        frame_outline = AssetProcessor.extract_and_restyle(frame_path, stroke_override="#000000", width_modifier=4, fill_override="none")
        frame_core = AssetProcessor.extract_and_restyle(frame_path, stroke_override="#FFFFFF", width_modifier=0, fill_override="none")
        
        if frame_fill and frame_outline and frame_core:
            final_svg.extend([
                '    ', f'    <g>', f'      {frame_fill}', '    </g>',
                f'    <g {dash_styles["black"]}>', f'      {frame_outline}', '    </g>',
                f'    <g {dash_styles["white"]}>', f'      {frame_core}', '    </g>'
            ])

        # 3. Domain Indicator Badge (Top Right)
        geometry_type = ris.get("geometry", {}).get("type")
        if geometry_type and geometry_type in DOMAIN_BADGES:
            domain_letter = DOMAIN_BADGES[geometry_type]
            
            final_svg.extend([
                '    ',
                '    <!-- Domain Indicator Badge -->',
                '    <g transform="translate(85, 15)">',
                '      <circle cx="0" cy="0" r="14" fill="#FFFFFF" stroke="#000000" stroke-width="4"/>',
                f'      <text x="0" y="5" font-family="Tahoma, Arial, sans-serif" font-size="16" font-weight="bold" fill="#000000" text-anchor="middle">{domain_letter}</text>',
                '    </g>'
            ])

        # 4. Mechanism Glyphs (Dynamically Scaled based on count)
        final_svg.append('    ')
        glyphs = sorted(ris.get("glyphs", []), key=lambda x: x.get("priority", 99))
        glyph_count = max(1, min(len(glyphs), 3)) # Ensure it maps to 1, 2, or 3
        active_zones = ZONES_BY_COUNT[glyph_count]
        
        for glyph in glyphs:
            glyph_path = os.path.join(self.assets_dir, "glyphs", f"{glyph.get('type')}.svg")
            glyph_outline = AssetProcessor.extract_and_restyle(glyph_path, "#000000", 4)
            glyph_core = AssetProcessor.extract_and_restyle(glyph_path, "#FFFFFF", -1)
            
            if glyph_outline and glyph_core:
                z = active_zones.get(glyph.get("zone", "center"))
                transform = f"translate({z['x']}, {z['y']}) scale({z['scale']})"
                final_svg.extend([
                    f'    <g transform="{transform}">',
                    f'      {glyph_outline}',
                    f'      {glyph_core}',
                    '    </g>'
                ])

        # 5. Intent Modifier
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