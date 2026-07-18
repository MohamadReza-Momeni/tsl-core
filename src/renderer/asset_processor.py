import os
import re

class AssetProcessor:
    """Handles the extraction and dynamic restyling of raw SVG assets."""
    
    @staticmethod
    def extract_and_restyle(filepath, new_color="#000000", width_modifier=0):
        """Extracts inner SVG content and dynamically changes its color and stroke width."""
        if not os.path.exists(filepath):
            print(f"[WARNING] Asset missing: {filepath}")
            return ""
        
        with open(filepath, 'r', encoding='utf-8') as f:
            match = re.search(r'<svg[^>]*>(.*?)</svg>', f.read(), re.DOTALL | re.IGNORECASE)
            if not match:
                return ""
                
            content = match.group(1).strip()
            
            # 1. Swap color
            content = content.replace("#000000", new_color)
            
            # 2. Adjust stroke width dynamically
            if width_modifier != 0:
                def adjust_width(m):
                    current_width = float(m.group(1))
                    new_width = max(1.0, current_width + width_modifier)
                    return f'stroke-width="{new_width}"'
                
                content = re.sub(r'stroke-width="([0-9.]+)"', adjust_width, content)
                
            return content