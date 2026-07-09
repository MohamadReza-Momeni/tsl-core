import os

# Define the 12 Strategic Intent Modifiers
# Overlays are designed to sit inside or slightly outside the 100x100 viewBox without obscuring the core.
MODIFIERS = {
    # INT-01 Destabilize: Jagged "fault line" across the bottom edge
    "position_jitter": '<path d="M 20,85 L 40,75 L 50,90 L 70,75 L 80,85" fill="none" stroke="currentColor" stroke-width="3"/>',
    
    # INT-02 Influence: Expanding dashed rings
    "outward_ripple": '<circle cx="50" cy="50" r="55" fill="none" stroke="currentColor" stroke-width="2" stroke-dasharray="4 4" opacity="0.5"/><circle cx="50" cy="50" r="62" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="2 6" opacity="0.3"/>',
    
    # INT-03 Control: Inward pointing brackets from the outer corners
    "inward_compression": '<g fill="none" stroke="currentColor" stroke-width="4"><path d="M -10,-10 L 10,10 M 0,10 L 10,10 L 10,0"/><path d="M 110,110 L 90,90 M 100,90 L 90,90 L 90,100"/><path d="M 110,-10 L 90,10 M 100,10 L 90,10 L 90,0"/><path d="M -10,110 L 10,90 M 0,90 L 10,90 L 10,100"/></g>',
    
    # INT-04 Divide: A cracked line breaking through the frame
    "structural_fracture": '<path d="M 20,0 L 40,30 L 30,50 L 70,80 L 60,100" fill="none" stroke="currentColor" stroke-width="3" stroke-dasharray="6 2" opacity="0.8"/>',
    
    # INT-05 Deceive: Wavy lines across the top and bottom
    "wave_distortion": '<path d="M 0,20 Q 25,0 50,20 T 100,20 M 0,80 Q 25,100 50,80 T 100,80" fill="none" stroke="currentColor" stroke-width="2" opacity="0.5"/>',
    
    # INT-06 Delay: "Pause Brackets" hugging the left and right edges
    "clockwise_rotation_offset": '<g fill="none" stroke="currentColor" stroke-width="5"><line x1="15" y1="30" x2="15" y2="70"/><line x1="85" y1="30" x2="85" y2="70"/></g>',
    
    # INT-07 Intimidate: Heavy "Armor Corners" (thick L-brackets at the 4 inner corners)
    "heavy_outline": '<g fill="none" stroke="currentColor" stroke-width="6"><path d="M 20,40 L 20,20 L 40,20 M 80,40 L 80,20 L 60,20 M 20,60 L 20,80 L 40,80 M 80,60 L 80,80 L 60,80"/></g>',
    
    # INT-08 Steal: "Corner Bites" at top-left and bottom-right with extended outward extraction arrows
    "extraction_arrow": '<g fill="none" stroke="currentColor" stroke-width="4"><path d="M 20,0 L 0,0 L 0,20 M 10,10 L 0,0 M 100,80 L 100,100 L 80,100 M 90,90 L 100,100"/></g>',
    
    # INT-09 Destroy: Kinetic impact lines hitting the perimeter
    "radial_burst": '<g fill="none" stroke="currentColor" stroke-width="3" opacity="0.7"><line x1="50" y1="-10" x2="50" y2="10"/><line x1="50" y1="110" x2="50" y2="90"/><line x1="-10" y1="50" x2="10" y2="50"/><line x1="110" y1="50" x2="90" y2="50"/><line x1="8" y1="8" x2="22" y2="22"/><line x1="92" y1="92" x2="78" y2="78"/><line x1="92" y1="8" x2="78" y2="22"/><line x1="8" y1="92" x2="22" y2="78"/></g>',
    
    # INT-10 Exploit: Dotted extension vectors pulling outward from the corners
    "extension_vectors": '<g fill="none" stroke="currentColor" stroke-width="2" stroke-dasharray="3 3"><line x1="85" y1="15" x2="110" y2="-10"/><line x1="15" y1="85" x2="-10" y2="110"/></g>',
    
    # INT-11 Exhaust: A stark corner-to-corner X denoting denial/exhaustion
    "progressive_fading": '<path d="M 15,15 L 85,85 M 85,15 L 15,85" fill="none" stroke="currentColor" stroke-width="4" opacity="0.6"/>',
    
    # INT-12 Isolate: A dashed boundary ring circling the entire frame
    "boundary_ring": '<circle cx="50" cy="50" r="48" fill="none" stroke="currentColor" stroke-width="3" stroke-dasharray="8 4"/>'
}

def generate_modifier(name, svg_content, output_dir):
    # overflow="visible" ensures elements breaking the 100x100 frame (like outward ripples) render correctly
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