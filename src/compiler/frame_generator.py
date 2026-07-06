import os

# Define the 12 standard Actor frames
FRAMES = {
    "frame_rectangle": '<rect x="5" y="5" width="90" height="90" fill="none" stroke="currentColor" stroke-width="4" vector-effect="non-scaling-stroke"/>',
    "frame_rounded_rectangle": '<rect x="5" y="5" width="90" height="90" rx="15" ry="15" fill="none" stroke="currentColor" stroke-width="4" vector-effect="non-scaling-stroke"/>',
    "frame_hexagon": '<polygon points="50,5 90,25 90,75 50,95 10,75 10,25" fill="none" stroke="currentColor" stroke-width="4" vector-effect="non-scaling-stroke"/>',
    "frame_diamond": '<polygon points="50,5 95,50 50,95 5,50" fill="none" stroke="currentColor" stroke-width="4" vector-effect="non-scaling-stroke"/>',
    "frame_pentagon": '<polygon points="50,5 95,38 78,95 22,95 5,38" fill="none" stroke="currentColor" stroke-width="4" vector-effect="non-scaling-stroke"/>',
    "frame_inverted_triangle": '<polygon points="5,5 95,5 50,95" fill="none" stroke="currentColor" stroke-width="4" vector-effect="non-scaling-stroke"/>',
    "frame_octagon": '<polygon points="30,5 70,5 95,30 95,70 70,95 30,95 5,70 5,30" fill="none" stroke="currentColor" stroke-width="4" vector-effect="non-scaling-stroke"/>',
    "frame_rounded_hexagon": '<path d="M 50,5 L 85,25 Q 90,28 90,35 L 90,65 Q 90,72 85,75 L 50,95 L 15,75 Q 10,72 10,65 L 10,35 Q 10,28 15,25 Z" fill="none" stroke="currentColor" stroke-width="4" vector-effect="non-scaling-stroke"/>',
    "frame_circle": '<circle cx="50" cy="50" r="45" fill="none" stroke="currentColor" stroke-width="4" vector-effect="non-scaling-stroke"/>',
    "frame_shield": '<path d="M 10,10 L 90,10 L 90,40 C 90,75 50,95 50,95 C 50,95 10,75 10,40 Z" fill="none" stroke="currentColor" stroke-width="4" vector-effect="non-scaling-stroke"/>',
    "frame_double_circle": '<circle cx="50" cy="50" r="45" fill="none" stroke="currentColor" stroke-width="4"/><circle cx="50" cy="50" r="35" fill="none" stroke="currentColor" stroke-width="4"/>',
    "frame_dashed_diamond": '<polygon points="50,5 95,50 50,95 5,50" fill="none" stroke="currentColor" stroke-width="4" stroke-dasharray="8 4" vector-effect="non-scaling-stroke"/>'
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
    print("Successfully generated all 12 Actor Frames.")