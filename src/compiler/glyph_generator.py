import os

# Base styling wrapper for all glyphs to ensure consistency
# stroke="currentColor" ensures they automatically adopt the Severity Color (Red, Yellow, etc.)
WRAPPER_START = '<g fill="none" stroke="#000000" stroke-width="5" stroke-linecap="round" stroke-linejoin="round">'
WRAPPER_END = '</g>'

# The complete library of 47 Mechanism Glyphs
RAW_GLYPHS = {
    # === DOMAIN 1: INFORMATION & COGNITIVE ===
    "propaganda": '<path d="M 20,45 L 40,45 L 60,20 L 60,80 L 40,55 L 20,55 Z"/><path d="M 70,30 Q 80,50 70,70 M 80,20 Q 95,50 80,80"/>', # Megaphone facing right with waves
    "disinformation": '<circle cx="50" cy="50" r="30"/><line x1="25" y1="25" x2="75" y2="75"/>', # Crossed-out circle
    "misinformation": '<circle cx="50" cy="50" r="30"/><path d="M 40,40 C 40,30 60,30 60,40 C 60,50 50,50 50,60"/><circle cx="50" cy="70" r="2" fill="currentColor"/>', # Question mark in circle
    "narrative_manipulation": '<path d="M 20,20 Q 50,80 80,20"/><path d="M 20,80 Q 50,20 80,80"/>', # Twisted / crossing lines
    "psychological_operations": '<circle cx="50" cy="50" r="20"/><path d="M 20,50 Q 50,10 80,50 Q 50,90 20,50 Z"/>', # Eye / Mind symbol
    "deepfake_distribution": '<rect x="20" y="20" width="40" height="40" rx="10"/><rect x="40" y="40" width="40" height="40" rx="10" stroke-dasharray="4 4"/>', # Overlapping masked frames
    "censorship": '<rect x="20" y="40" width="60" height="40" rx="5"/><path d="M 35,40 L 35,25 Q 50,10 65,25 L 65,40"/>', # Padlock
    "information_suppression": '<line x1="20" y1="80" x2="80" y2="80"/><line x1="50" y1="20" x2="50" y2="70"/><polyline points="35,55 50,70 65,55"/>', # Heavy downward arrow hitting a barrier
    "influence_campaign": '<g transform="translate(10, 10) scale(0.8)"><circle cx="50" cy="50" r="10"/><path d="M 30,30 Q 50,10 70,30 M 20,20 Q 50,-10 80,20 M 30,70 Q 50,90 70,70 M 20,80 Q 50,110 80,80"/></g>', # Scaled down broadcast waves
    "rumor_propagation": '<circle cx="50" cy="50" r="10"/><polyline points="50,40 20,20 20,40 M 20,20 L 40,20"/><polyline points="60,60 80,80 60,80 M 80,80 L 80,60"/>', # Branching viral spread
    "character_assassination": '<g><circle cx="50" cy="30" r="15"/><path d="M 25,80 C 25,50 75,50 75,80"/></g><g stroke-dasharray="4 4"><circle cx="50" cy="45" r="25"/><line x1="50" y1="10" x2="50" y2="80"/><line x1="15" y1="45" x2="85" y2="45"/></g>', # Person silhouette with dashed crosshairs
    "demoralization": '<path d="M 50,30 C 50,10 20,10 20,40 Q 20,60 50,85 Q 80,60 80,40 C 80,10 50,10 50,30 Z"/><polyline points="50,20 40,50 60,60 50,85"/>', # Broken heart
    "educational_co_optation": '<polygon points="50,25 20,40 50,55 80,40"/><line x1="50" y1="55" x2="50" y2="80"/><line x1="80" y1="40" x2="80" y2="70"/>', # Graduation cap / Institution

    # === DOMAIN 2: CYBER & INFRASTRUCTURE ===
    "cyber_intrusion": '<path d="M 20,20 L 80,20 L 80,50 Q 50,90 20,50 Z"/><polyline points="50,10 50,60 30,40 M 50,60 L 70,40"/>', # Arrow breaching a shield
    "data_exfiltration": '<rect x="20" y="30" width="60" height="50"/><polyline points="20,30 35,15 55,15 65,30"/><polyline points="50,70 50,30 35,45 M 50,30 L 65,45"/>', # Folder with arrow OUT
    "denial_of_service": '<rect x="25" y="15" width="50" height="20"/><rect x="25" y="40" width="50" height="20"/><rect x="25" y="65" width="50" height="20"/><line x1="15" y1="15" x2="85" y2="85"/>', # Slashed server rack
    "credential_theft": '<circle cx="35" cy="50" r="15"/><line x1="50" y1="50" x2="85" y2="50"/><line x1="65" y1="50" x2="65" y2="65"/><line x1="80" y1="50" x2="80" y2="65"/>', # Key icon
    "supply_chain_compromise": '<rect x="15" y="40" width="20" height="20"/><rect x="40" y="40" width="20" height="20" stroke-dasharray="2 2"/><rect x="65" y="40" width="20" height="20"/><line x1="35" y1="50" x2="40" y2="50"/><line x1="60" y1="50" x2="65" y2="50"/>', # Linked boxes, center compromised
    "data_harvesting_&_microtargeting": '<circle cx="50" cy="50" r="30" stroke-dasharray="4 4"/><circle cx="50" cy="50" r="10"/><line x1="50" y1="10" x2="50" y2="90"/><line x1="10" y1="50" x2="90" y2="50"/>', # Crosshair grid

    # === DOMAIN 3: ECONOMIC ===
    "economic_sanctions": '<circle cx="50" cy="50" r="35"/><path d="M 40,25 Q 60,25 60,40 Q 40,60 40,75 Q 60,75 60,75"/><line x1="50" y1="15" x2="50" y2="85"/><line x1="15" y1="15" x2="85" y2="85"/>', # Currency slashed
    "market_manipulation": '<polyline points="15,80 40,60 60,70 85,30"/><polyline points="70,30 85,30 85,45"/><line x1="85" y1="30" x2="65" y2="10"/>', # Artificial chart spike
    "currency_manipulation": '<circle cx="35" cy="50" r="20"/><circle cx="65" cy="50" r="20"/><line x1="35" y1="20" x2="35" y2="80"/><line x1="65" y1="20" x2="65" y2="80"/>', # Linked coins / exchange warp
    "resource_denial": '<path d="M 50,15 C 80,45 80,85 50,85 C 20,85 20,45 50,15 Z"/><line x1="25" y1="25" x2="75" y2="75"/>', # Droplet (resource) slashed
    "investment_influence": '<polyline points="20,70 50,40 80,50"/><circle cx="80" cy="50" r="5"/><path d="M 10,90 Q 50,90 90,70"/>', # Chart line hovering over a hand/base
    "trade_restriction": '<rect x="20" y="30" width="60" height="40"/><line x1="20" y1="50" x2="80" y2="50"/><line x1="10" y1="10" x2="90" y2="90"/>', # Shipping box slashed
    "strategic_asset_acquisition": '<rect x="25" y="45" width="50" height="40"/><polyline points="25,45 50,20 75,45"/><rect x="40" y="65" width="20" height="20"/><circle cx="50" cy="35" r="5"/>', # Factory/Building marked
    "subversion_funding": '<path d="M 30,85 Q 10,85 20,50 C 30,20 40,20 50,20 C 60,20 70,20 80,50 Q 90,85 70,85 Z"/><line x1="45" y1="40" x2="45" y2="60"/><line x1="55" y1="40" x2="55" y2="60"/>', # Money bag
    "policy_sabotage": '<rect x="25" y="15" width="50" height="70"/><line x1="35" y1="35" x2="65" y2="35"/><line x1="35" y1="50" x2="65" y2="50"/><line x1="15" y1="75" x2="85" y2="25"/>', # Document slashed

    # === DOMAIN 4: DIPLOMATIC & POLITICAL ===
    "diplomatic_pressure": '<rect x="20" y="35" width="30" height="30" rx="5"/><rect x="50" y="35" width="30" height="30" rx="5"/><line x1="50" y1="35" x2="50" y2="65" stroke-dasharray="4 4"/>', # Forced block meeting
    "election_interference": '<rect x="20" y="30" width="60" height="50"/><line x1="20" y1="30" x2="40" y2="10"/><line x1="80" y1="30" x2="60" y2="10"/><line x1="40" y1="10" x2="60" y2="10"/><path d="M 40,55 L 60,55 M 50,45 L 50,65"/>', # Ballot box being altered
    "institutional_capture": '<polyline points="15,40 50,15 85,40"/><rect x="25" y="40" width="10" height="40"/><rect x="45" y="40" width="10" height="40"/><rect x="65" y="40" width="10" height="40"/><line x1="15" y1="80" x2="85" y2="80"/><circle cx="50" cy="50" r="40" stroke-dasharray="4 4"/>', # Govt building inside a net
    "legal_manipulation": '<line x1="50" y1="20" x2="50" y2="80"/><line x1="20" y1="40" x2="80" y2="25"/><polyline points="20,40 10,60 30,60 Z"/><polyline points="80,25 70,45 90,45 Z"/>', # Tipped scales of justice
    "crisis_exploitation": '<polyline points="50,15 15,80 85,80 Z"/><line x1="50" y1="40" x2="50" y2="60"/><circle cx="50" cy="70" r="2" fill="currentColor"/><polyline points="85,15 100,15 100,30 M 100,15 L 70,45"/>', # Warning sign + Upward graph
    "international_forum_manipulation": '<circle cx="50" cy="50" r="35"/><ellipse cx="50" cy="50" rx="35" ry="15"/><line x1="50" y1="15" x2="50" y2="85"/><rect x="35" y="35" width="30" height="30" fill="currentColor"/>', # Globe corrupted
    "border_provocation": '<line x1="20" y1="50" x2="80" y2="50" stroke-dasharray="6 6"/><polyline points="40,20 50,35 60,20"/><polyline points="40,80 50,65 60,80"/>', # Opposing arrows at a dashed border

    # === DOMAIN 5: MILITARY & PHYSICAL ===
    "kinetic_strike": '<path d="M 20,80 L 80,20 M 60,20 L 80,20 L 80,40"/><path d="M 30,70 L 15,85 L 25,95 L 40,80 Z"/>', # Missile impact
    "sabotage": '<path d="M 30,30 L 70,70 M 70,30 L 30,70"/>', # Simple Cross / X (tactical)
    "espionage": '<path d="M 15,50 Q 50,20 85,50 Q 50,80 15,50 Z"/><circle cx="50" cy="50" r="12"/>', # Eye
    "force_projection": '<polyline points="20,20 60,50 20,80"/><polyline points="40,20 80,50 40,80"/>', # Double chevrons forward
    "undeclared_gray_zone_action": '<rect x="20" y="20" width="60" height="60" stroke-dasharray="4 4"/><path d="M 40,40 C 40,30 60,30 60,40 C 60,50 50,50 50,60"/><circle cx="50" cy="70" r="2" fill="currentColor"/>', # Question mark in dashed box
    "proxy_warfare_support": '<circle cx="35" cy="50" r="10"/><circle cx="65" cy="50" r="10"/><line x1="35" y1="20" x2="35" y2="40" stroke-dasharray="2 2"/><line x1="65" y1="20" x2="65" y2="40" stroke-dasharray="2 2"/>', # Two actors on puppet strings

    # === DOMAIN 6: SOCIAL ===
    "social_polarization": '<line x1="50" y1="15" x2="50" y2="85"/><polyline points="35,35 15,50 35,65 M 15,50 L 45,50"/><polyline points="65,35 85,50 65,65 M 85,50 L 55,50"/>', # Arrows pushing away from center wall
    "identity_manipulation": '<circle cx="50" cy="50" r="35"/><circle cx="50" cy="50" r="20"/><circle cx="50" cy="50" r="5"/><line x1="15" y1="50" x2="85" y2="50"/>', # Fingerprint / Target slashed
    "cultural_influence": '<polyline points="20,80 50,20 80,80"/><rect x="35" y="80" width="30" height="10"/><circle cx="50" cy="40" r="8"/>', # Monument/Temple symbol
    "protest_mobilization": '<path d="M 35,70 L 35,40 C 35,30 45,30 45,40 L 45,70 M 45,45 C 45,35 55,35 55,45 L 55,70 M 55,50 C 55,40 65,40 65,50 L 65,70 C 65,85 35,85 35,70 Z"/><line x1="50" y1="70" x2="50" y2="95"/>', # Raised Fist
    "migration_pressure": '<polyline points="20,35 80,35 80,50"/><polyline points="20,65 80,65 80,50"/><line x1="80" y1="20" x2="80" y2="80" stroke-dasharray="4 4"/>', # Flow lines hitting a dashed border
    "violence_&_riot_incitement": '<path d="M 50,15 C 20,40 20,85 50,85 C 80,85 80,40 50,15 Z"/><path d="M 50,45 C 40,60 40,85 50,85"/>', # Flame
    "weaponized_migration": '<polyline points="20,70 50,40 80,70"/><line x1="50" y1="80" x2="50" y2="15"/><polyline points="35,30 50,15 65,30"/>', # Migration flow converging into a spearhead
    "extremist_radicalization": '<path d="M 50,50 L 20,20 M 50,50 L 80,20 M 50,50 L 20,80 M 50,50 L 80,80"/><circle cx="50" cy="50" r="15"/>', # Radical fracture / sharp spiral

    # === NEW: MECHANISMS ADDED TO RESOLVE VISUAL COLLISIONS ===
    "illicit_trade_&_smuggling": '<path d="M 20,40 L 80,40 L 80,70 L 20,70 Z" stroke-dasharray="4 4"/><path d="M 30,40 L 50,20 L 70,40"/><line x1="50" y1="40" x2="50" y2="70"/>', # Dashed stealth crate
    "public_health_degradation": '<path d="M 40,20 L 60,20 L 60,40 L 80,40 L 80,60 L 60,60 L 60,80 L 40,80 L 40,60 L 20,60 L 20,40 L 40,40 Z"/><line x1="20" y1="20" x2="80" y2="80"/>', # Medical cross slashed
    "separatist_incitement": '<path d="M 35,20 L 35,80 M 65,20 L 65,80"/><path d="M 50,10 L 50,90" stroke-dasharray="4 4"/><polyline points="20,40 35,50 20,60"/><polyline points="80,40 65,50 80,60"/>' # Entity splitting apart
}

def generate_glyphs(output_dir):
    os.makedirs(output_dir, exist_ok=True)
    count = 0
    for name, path_data in RAW_GLYPHS.items():
        # Cleanly format the filename based on the dictionary key
        filename = f"{name}.svg"
        
        # Assemble the full SVG file
        full_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">\n  {WRAPPER_START}\n    {path_data}\n  {WRAPPER_END}\n</svg>'''
        
        # Write to disk
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(full_svg)
        count += 1
        
    print(f"[SUCCESS] Generated {count} unique mechanism glyphs in '{output_dir}'.")

if __name__ == "__main__":
    # Assuming this script is run from the root or src directory, route to assets
    target_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../assets/glyphs"))
    generate_glyphs(target_dir)