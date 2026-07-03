import os

# Define the library mapping: Mechanism Name -> SVG Path Data
# All paths are designed for a 100x100 viewBox with a 6px stroke width.
GLYPHS = {
    # DOM-01: Information & Cognitive (MEC-1xx)
    "propaganda": "M 20,50 L 50,20 L 50,80 L 20,50 Z M 50,50 L 80,50",
    "disinformation": "M 50,50 m -30,0 a 30,30 0 1,0 60,0 a 30,30 0 1,0 -60,0 Z M 25,25 L 75,75",
    "narrative_manipulation": "M 20,50 Q 50,10 80,50",
    "psychological_ops": "M 20,50 A 30,30 0 1,0 80,50 A 30,30 0 1,0 20,50 M 50,30 L 50,70",
    
    # DOM-06: Infrastructure & Technology / Cyber (MEC-2xx)
    "cyber_intrusion": "M 50,10 L 30,50 L 50,50 L 30,90 L 70,50 L 50,50 L 70,10 Z",
    "denial_of_service": "M 20,30 L 80,30 L 80,70 L 20,70 Z M 20,50 L 80,50",
    
    # DOM-02: Economic (MEC-3xx)
    "economic_sanctions": "M 50,20 L 50,80 M 30,35 L 70,35 M 30,65 L 70,65 M 20,50 L 80,50 M 50,50 A 20,20 0 1,0 49.9,50",
    "resource_denial": "M 50,20 L 50,80 M 20,50 L 80,50 M 25,25 L 75,75 M 25,75 L 75,25",

    # DOM-03: Political & Diplomatic (MEC-4xx)
    "diplomatic_pressure": "M 30,50 L 70,50 M 50,30 L 50,70 M 20,20 L 80,80",
    "election_interference": "M 20,80 L 40,80 L 40,40 L 20,40 Z M 50,80 L 70,80 L 70,20 L 50,20 Z M 20,60 L 80,60",
    "legal_manipulation": "M 50,20 L 50,80 M 30,40 L 70,40 M 30,60 L 70,60 M 40,20 L 60,20",

    # DOM-05: Military (MEC-5xx)
    "kinetic_strike": "M 50,10 L 50,90 M 10,50 L 90,50 M 20,20 L 80,80 M 20,80 L 80,20",
    "sabotage": "M 20,80 L 80,20 M 20,20 L 80,80",
    "espionage": "M 50,20 C 20,20 10,50 10,50 C 10,50 20,80 50,80 C 80,80 90,50 90,50 C 90,50 80,20 50,20 Z M 50,65 A 15,15 0 1,0 50,35 A 15,15 0 1,0 50,65 Z",
    "force_projection": "M 20,50 L 80,50 M 60,30 L 80,50 L 60,70",
    "proxy_warfare_support": "M 30,80 L 30,20 L 70,50 Z M 10,50 L 30,50 M 10,30 L 30,30 M 10,70 L 30,70",

    # DOM-04: Social (MEC-6xx)
    "social_polarization": "M 50,10 L 50,90 M 20,30 L 40,30 M 20,70 L 40,70 M 60,30 L 80,30 M 60,70 L 80,70",
    "protest_mobilization": "M 30,80 L 30,50 L 20,50 L 20,20 L 40,20 L 40,50 L 30,50 M 70,80 L 70,50 L 60,50 L 60,20 L 80,20 L 80,50 L 70,50",
    "violence_riot_incitement": "M 50,80 L 50,50 L 30,20 M 50,50 L 70,20 M 20,50 L 80,50"
}

def generate_glyph(name, path_data, output_dir):
    """Wraps the path data in a standard TSL SVG container and saves it."""
    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <path d="{path_data}" fill="none" stroke="currentColor" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>
</svg>'''
    
    filepath = os.path.join(output_dir, f"{name}.svg")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(svg_content)
    print(f"[+] Generated: {filepath}")

if __name__ == "__main__":
    # Ensure the target directory exists relative to the script execution
    target_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../assets/glyphs"))
    os.makedirs(target_dir, exist_ok=True)
    
    print(f"Generating TSL-202B Glyphs into: {target_dir}")
    print("-" * 50)
    
    count = 0
    for name, path in GLYPHS.items():
        generate_glyph(name, path, target_dir)
        count += 1
        
    print("-" * 50)
    print(f"Successfully generated {count} mechanism glyphs.")