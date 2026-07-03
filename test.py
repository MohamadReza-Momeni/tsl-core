import os
from src.compiler.tsl_compiler import TSLCompiler
from src.renderer.svg_builder import SVGRenderer

# 1. A dummy threat record from your catalog using assets we KNOW exist
# Foreign State (ACT-01) doing Covert (VIS-02) Disinformation (MEC-102) & Cyber Intrusion (MEC-201)
sample_threat = {
    "Threat ID": "TH-TEST-01",
    "Domain Code": "DOM-01",
    "Init Actor Code": "ACT-01",     # Resolves to 'frame_rectangle'
    "Vis Code": "VIS-02",            # Resolves to 'dashed' border
    "Mec 1 Code": "MEC-102",
    "Mec 1 Name": "disinformation",  # Central glyph
    "Mec 2 Code": "MEC-201",
    "Mec 2 Name": "cyber_intrusion",  # North glyph
    "Intent Code": "INT-08",   # Steal
    "Sev Code": "SEV-4",       # High (will render Red)
}

# 2. Compile to JSON
compiler = TSLCompiler() # Make sure mappings.json is correct!
ris_json_string = compiler.compile(sample_threat)

# Save the JSON so the renderer can find it
os.makedirs("output/ris", exist_ok=True)
json_path = "output/ris/TH-TEST-01.json"
with open(json_path, 'w') as f:
    f.write(ris_json_string)
print(f"Compiled JSON saved to {json_path}")

# 3. Render the SVG
renderer = SVGRenderer()
renderer.build_symbol(json_path)