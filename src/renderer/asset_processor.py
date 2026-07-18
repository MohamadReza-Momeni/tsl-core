import os
import re

class AssetProcessor:
    """Handles the extraction and dynamic restyling of raw SVG assets."""
    
    @staticmethod
    def extract_and_restyle(filepath, new_color="#000000", width_modifier=0, fill_override=None, stroke_override=None):
        if not os.path.exists(filepath):
            print(f"[WARNING] Asset missing: {filepath}")
            return ""
        
        with open(filepath, 'r', encoding='utf-8') as f:
            match = re.search(r'<svg[^>]*>(.*?)</svg>', f.read(), re.DOTALL | re.IGNORECASE)
            if not match:
                return ""
                
            content = match.group(1).strip()
            
            # 1. Override fill if requested
            if fill_override is not None:
                content = re.sub(r'fill="[^"]*"', f'fill="{fill_override}"', content)
                
            # 2. Override stroke if requested
            if stroke_override is not None:
                content = re.sub(r'stroke="[^"]*"', f'stroke="{stroke_override}"', content)
            else:
                content = content.replace("#000000", new_color)
            
            # 3. Dynamically adjust the stroke-width
            if width_modifier != 0:
                def adjust_width(m):
                    current_width = float(m.group(1))
                    new_width = max(0.0, current_width + width_modifier)
                    return f'stroke-width="{new_width}"'
                
                content = re.sub(r'stroke-width="([0-9.]+)"', adjust_width, content)
                
            return content