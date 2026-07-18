import os

# Define the 6 Domain Background Geometries
# These use a 100x100 viewBox and subtle stroke styling
GEOMETRIES = {
    "radial_network": '<g opacity="0.2" stroke="#000000" stroke-width="2"><circle cx="50" cy="50" r="30" fill="none" stroke-dasharray="4 4"/><line x1="50" y1="20" x2="50" y2="80"/><line x1="20" y1="50" x2="80" y2="50"/><line x1="28" y1="28" x2="72" y2="72"/><line x1="28" y1="72" x2="72" y2="28"/></g>',
    "bar_stack": '<g opacity="0.2" fill="#000000"><rect x="20" y="60" width="15" height="20"/><rect x="42" y="40" width="15" height="40"/><rect x="65" y="20" width="15" height="60"/></g>',
    "connected_chain": '<g opacity="0.2" fill="none" stroke="#000000" stroke-width="4"><circle cx="30" cy="50" r="12"/><circle cx="50" cy="50" r="12"/><circle cx="70" cy="50" r="12"/></g>',
    "population_cluster": '<g opacity="0.2" fill="#000000"><circle cx="30" cy="30" r="6"/><circle cx="45" cy="20" r="8"/><circle cx="70" cy="35" r="5"/><circle cx="25" cy="65" r="7"/><circle cx="55" cy="70" r="9"/><circle cx="75" cy="60" r="6"/><circle cx="50" cy="45" r="10"/></g>',
    "directed_vectors": '<g opacity="0.2" fill="none" stroke="#000000" stroke-width="3"><path d="M 20,80 L 80,20 M 65,20 L 80,20 L 80,35 M 40,80 L 90,30 M 75,30 L 90,30 L 90,45 M 10,60 L 60,10 M 45,10 L 60,10 L 60,25"/></g>',
    "grid": '<g opacity="0.15" stroke="#000000" stroke-width="2"><path d="M 20,0 L 20,100 M 40,0 L 40,100 M 60,0 L 60,100 M 80,0 L 80,100 M 0,20 L 100,20 M 0,40 L 100,40 M 0,60 L 100,60 M 0,80 L 100,80"/></g>'
}

def generate_geometry(name, svg_content, output_dir):
    full_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">\n  {svg_content}\n</svg>'''
    filepath = os.path.join(output_dir, f"{name}.svg")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(full_svg)
    print(f"[+] Generated Geometry: {filepath}")

if __name__ == "__main__":
    target_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../assets/geometries"))
    os.makedirs(target_dir, exist_ok=True)
    
    for name, svg in GEOMETRIES.items():
        generate_geometry(name, svg, target_dir)