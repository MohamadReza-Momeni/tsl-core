import os

# Define the 12 standard Actor frames
FRAMES = {
    # (Self)
    "frame_rectangle": '<rect x="10" y="10" width="80" height="80" fill="currentColor" stroke="#000000" stroke-width="4"/>',
    
    # (Ally)
    "frame_circle": '<circle cx="50" cy="50" r="45" fill="currentColor" stroke="#000000" stroke-width="4"/>',
    
    # (Enemy)
    "frame_diamond": '<polygon points="50,5 95,50 50,95 5,50" fill="currentColor" stroke="#000000" stroke-width="4"/>',
    
    # (Unknown) - A standard Quatrefoil/Clover shape
    "frame_quatrefoil": '<path d="M 50,5 C 70,5 75,20 75,30 C 85,30 95,35 95,50 C 95,65 85,70 75,70 C 75,80 70,95 50,95 C 30,95 25,80 25,70 C 15,70 5,65 5,50 C 5,35 15,30 25,30 C 25,20 30,5 50,5 Z" fill="currentColor" stroke="#000000" stroke-width="4"/>'
}

def generate_frame(name, inner_svg, output_dir):
    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">\n  {inner_svg}\n</svg>'''
    filepath = os.path.join(output_dir, f"{name}.svg")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(svg_content)
    print(f"[+] Generated: {filepath}")

if __name__ == "__main__":
    target_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../assets/frames"))
    os.makedirs(target_dir, exist_ok=True)
    
    for name, svg in FRAMES.items():
        generate_frame(name, svg, target_dir)
    print("Successfully generated all 4 Actor Frames.")