# TSL-Core: Threat Symbology Language Engine

**TSL-Core** is an automated rendering engine that translates semantic intelligence data into standardized, NATO APP-6 style military symbology.

Instead of analysts manually drawing threat icons, this pipeline ingests tabular intelligence data (TSL-104), compiles it into a machine-readable Render Instruction Set (RIS), and dynamically composites layered SVG graphics. The result is a mathematically perfect, visually consistent, and **100% collision-free** library of threat symbology generated in milliseconds.

---

## System Architecture

The project is divided into three main operational layers: the **Compiler** (intelligence logic and asset generation), the **Renderer** (SVG compositing), and the **Presentation Layer** (HTML templating).

```text
tsl-core/
├── assets/                  # Generated SVG building blocks
│   ├── frames/              # Actor boundaries (ACT)
│   ├── geometries/          # Domain backgrounds (DOM)
│   ├── glyphs/              # Core mechanisms (MEC)
│   └── modifiers/           # Strategic intents (INT)
├── data/
│   └── catalogs/            # Input intelligence data (TSL-104_Threat_Catalog_v3.csv)
├── output/
│   ├── renders/             # Final generated SVGs
│   ├── ris/                 # Render Instruction Set JSONs
│   └── dashboard.html       # Generated interactive web UI
├── src/
│   ├── compiler/
│   │   ├── mappings.json          # The Visual Dictionary (Single Source of Truth)
│   │   ├── tsl_compiler.py        # Core logic mapping CSV data to RIS JSON
│   │   ├── frame_generator.py     # Generates ACT primitives
│   │   ├── geometry_generator.py  # Generates DOM primitives
│   │   ├── glyph_generator.py     # Generates MEC primitives
│   │   └── modifier_generator.py  # Generates INT primitives
│   └── renderer/
│       └── svg_builder.py         # Composites primitives into final symbols
├── templates/
│   └── dashboard_template.html    # Presentation layer (CSS/HTML UI anchor)
├── batch_process.py         # Runs the end-to-end pipeline on the catalog
├── dashboard_generator.py   # Injects renders and data into the HTML template
├── find_collisions.py       # Audits the catalog for visual overlaps
└── resolve_collisions.py    # Auto-patches data using tertiary mechanisms

```

---

## The Visual Grammar

TSL symbols are read from the outside in. Each dimension of the intelligence data maps strictly to a specific visual layer, ensuring clear, unobstructed communication optimized for Dark Mode dashboards.

1. **Initiating Actor (Shape):** The outer geometric boundary dictates the *type* of adversary (e.g., Rectangle = Foreign State, Diamond = Intelligence Service).
2. **Visibility (Border):** The stroke style of the frame (e.g., Solid = Overt, Dashed = Covert).
3. **Severity (Color):** The global color of the symbol, ranging from White (Minimal) to Deep Red (Critical).
4. **Strategic Intent (Modifier):** Edge-based visual overlays that dictate the actor's goal (e.g., Corner bites = Steal, Slipping foundation = Destabilize). Designed strictly on the outer bounds to prevent inner canvas overlap.
5. **Domain (Background Geometry):** A subtle, low-opacity background pattern indicating the operational theater (e.g., Grid = Cyber, Radial Network = Information).
6. **Mechanisms (Inner Glyphs):** Up to three distinct black icons placed inside the frame detailing the exact methods used.
* **Priority 1:** Center
* **Priority 2:** North (Top edge)
* **Priority 3:** South (Bottom edge) - Heavily utilized to break visual collisions between highly similar threats.



---

## Quick Start Guide

### 1. Setup the Environment

Ensure you have Python 3.x installed along with the required data processing library:

```bash
pip install pandas
```

### 2. Generate the Visual Asset Library

Before rendering threats, you must generate the foundational SVG building blocks. Run these scripts once (or whenever you update a vector design):

```bash
python src/compiler/frame_generator.py
python src/compiler/geometry_generator.py
python src/compiler/modifier_generator.py
python src/compiler/glyph_generator.py
```

*Verify that the `assets/` folder is now populated with SVG files.*

### 3. Audit for Collisions (Optional but Recommended)

If you have updated the underlying CSV data, check for overlapping visual signatures:

```bash
python find_collisions.py
```

If collisions are found, you can manually fix the data or run `python resolve_collisions.py` to automatically deploy tertiary mechanisms to force uniqueness.

### 4. Run the Batch Processor

Ensure your primary intelligence catalog (e.g., `TSL-104_Threat_Catalog_v3.csv`) is in the `data/catalogs/` directory. Run the batch compiler:

```bash
python batch_process.py
```

*The engine will drop blank rows, translate the CSV into JSON instructions, and render hundreds of SVGs into the `output/renders/` folder.*

### 5. Launch the Interactive Dashboard

To view the generated symbology alongside its contextual intelligence data, build the UI:

```bash
python dashboard_generator.py
```

This reads from `templates/dashboard_template.html`, injects the data array in memory (bypassing massive string concatenations), and saves the final file. Open `output/dashboard.html` in any modern web browser to view your completed, searchable threat library.

---

## Extending the Dictionary

To add a new Actor, Intent, Mechanism, or Domain, you **do not** need to edit the core rendering engine.

1. Add the specific SVG path data to the corresponding generator script (e.g., `modifier_generator.py` or `glyph_generator.py`).
2. Run the generator script to bake the new `.svg` asset.
3. Update `src/compiler/mappings.json` to link the new Intelligence Code to the generated asset name.
4. Run `batch_process.py`.