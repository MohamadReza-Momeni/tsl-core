import json
import os

class TSLCompiler:
    """
    Translates TSL-104 semantic threat records into a Render Instruction Set (RIS).
    Compliant with TSL-201 Symbol Construction Rules. Loads structural rules from mappings.json.
    """
    
    def __init__(self, config_path=None):
        # If no path is provided, dynamically find mappings.json relative to this file's folder
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), "mappings.json")
            
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)

    def _resolve_glyph_name(self, mechanism_code, mechanism_name):
        """Converts human-readable mechanism names to standard lowercase glyph identifiers."""
        if not mechanism_name:
            return mechanism_code.lower()
        return mechanism_name.lower().replace(" ", "_").replace("/", "_").replace("-", "_")

    def compile(self, threat_record):
        """
        Takes a dictionary representing a TSL-104 record and returns the RIS JSON.
        """
        # 1. Resolve Actor -> Frame shape using external config
        actor_code = threat_record.get("Init Actor Code", "ACT-99")
        frame_shape = self.config["frame_map"].get(actor_code, "dashed_diamond")

        # 2. Resolve Visibility -> Border style
        vis_code = threat_record.get("Vis Code", "VIS-01")
        border_style = self.config["visibility_map"].get(vis_code, "solid")

        # 3. Resolve Domain -> Base Geometry
        domain_code = threat_record.get("Domain Code")
        base_geometry = self.config["geometry_map"].get(domain_code, "unknown_geometry")

        # 4. Resolve Mechanisms -> Glyphs
        # Rule: Max 3 visible mechanisms. 1st is Center, 2nd is North, 3rd is South.
        glyphs = []
        zones = ["center", "north", "south"]
        
        for i in range(1, 4):
            mec_code = threat_record.get(f"Mec {i} Code")
            mec_name = threat_record.get(f"Mec {i} Name")
            
            if mec_code and str(mec_code).strip():
                glyphs.append({
                    "type": self._resolve_glyph_name(mec_code, mec_name),
                    "priority": i,
                    "zone": zones[i-1]
                })

        # 5. Resolve Intent -> Modifier
        intent_code = threat_record.get("Intent Code")
        modifier = self.config["intent_map"].get(intent_code, "none")

        # 6. Resolve Severity -> Amplifier
        severity_raw = str(threat_record.get("Sev Code", "SEV-1"))
        severity_level = int(severity_raw.split("-")[1]) if "-" in severity_raw else 1

        # Assemble final Render Instruction Set (RIS)
        ris = {
            "id": threat_record.get("Threat ID"),
            "frame": {
                "shape": frame_shape,
                "border": border_style
            },
            "geometry": {
                "type": base_geometry,
                "seed": threat_record.get("Threat ID")  # Provides procedural determinism
            },
            "glyphs": glyphs,
            "modifier": {
                "type": modifier
            },
            "amplifier": {
                "severity": severity_level
            }
        }

        return json.dumps(ris, indent=2)