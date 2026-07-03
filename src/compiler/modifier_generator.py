import os

# Define the 12 Strategic Intent Modifiers
# These overlays are designed to sit on top of the 100x100 viewBox
MODIFIERS = {
    "position_jitter": '<path d="M 0,0 L 5,10 L -5,20 L 5,30" stroke="currentColor" stroke-width="2" fill="none" opacity="0.6"/>', # INT-01 Destabilize
    "outward_ripple": '<circle cx="50" cy="50" r="55" fill="none" stroke="currentColor" stroke-width="2" stroke-dasharray="4 4" opacity="0.5"/><circle cx="50" cy="50" r="62" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="2 6" opacity="0.3"/>', # INT-02 Influence
    "inward_compression": '<g fill="none" stroke="currentColor" stroke-width="4"><path d="M -10,-10 L 10,10 M 0,10 L 10,10 L 10,0"/><path d="M 110,110 L 90,90 M 100,90 L 90,90 L 90,100"/><path d="M 110,-10 L 90,10 M 100,10 L 90,10 L 90,0"/><path d="M -10,110 L 10,90 M 0,90 L 10,90 L 10,100"/></g>', # INT-03 Control
    "structural_fracture": '<path d="M 20,0 L 40,30 L 30,50 L 70,80 L 60,100" fill="none" stroke="currentColor" stroke-width="3" stroke-dasharray="6 2" opacity="0.8"/>', # INT-04 Divide
    "wave_distortion": '<path d="M 0,20 Q 25,0 50,20 T 100,20 M 0,80 Q 25,100 50,80 T 100,80" fill="none" stroke="currentColor" stroke-width="2" opacity="0.5"/>', # INT-05 Deceive
    "clockwise_rotation_offset": '<path d="M 20,20 A 40,40 0 0,1 80,20 M 70,10 L 80,20 L 90,10" fill="none" stroke="currentColor" stroke-width="3"/>', # INT-06 Delay
    "heavy_outline": '<rect x="-5" y="-5" width="110" height="110" fill="none" stroke="currentColor" stroke-width="6" opacity="0.4"/>', # INT-07 Intimidate
    "extraction_arrow": '<g fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"><line x1="50" y1="5" x2="50" y2="-25"/><polyline points="35,-10 50,-25 65,-10"/></g>', # INT-08 Steal
    "radial_burst": '<g fill="none" stroke="currentColor" stroke-width="3" opacity="0.7"><line x1="50" y1="-10" x2="50" y2="10"/><line x1="50" y1="110" x2="50" y2="90"/><line x1="-10" y1="50" x2="10" y2="50"/><line x1="110" y1="50" x2="90" y2="50"/><line x1="8" y1="8" x2="22" y2="22"/><line x1="92" y1="92" x2="78" y2="78"/><line x1="92" y1="8" x2="78" y2="22"/><line x1="8" y1="92" x2="22" y2="78"/></g>', # INT-09 Destroy
    "extension_vectors": '<g fill="none" stroke="currentColor" stroke-width="2" stroke-dasharray="3 3"><line x1="85" y1="15" x2="110" y2="-10"/><line x1="15" y1="85" x2="-10" y2="110"/></g>', # INT-10 Exploit
    "progressive_fading": '<rect x="0" y="0" width="100" height="100" fill="url(#fadeGradient)" opacity="0.5"/>', # INT-11 Exhaust (Requires a defs gradient, we will handle this via script overlay easily)
    "boundary_ring": '<circle cx="50" cy="50" r="48" fill="none" stroke="currentColor" stroke-width="3" stroke-dasharray="8 4"/>' # INT-12 Isolate
}

def generate_modifier(name, svg_content, output_dir):
    # Notice we set overflow="visible" so arrows can burst outside the 100x100 frame
    full_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" overflow="visible">\n  {svg_content}\n</svg>'''
    filepath = os.path.join(output_dir, f"{name}.svg")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(full_svg)
    print(f"[+] Generated Modifier: {filepath}")

if __name__ == "__main__":
    target_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../assets/modifiers"))
    os.makedirs(target_dir, exist_ok=True)
    
    for name, svg in MODIFIERS.items():
        generate_modifier(name, svg, target_dir)