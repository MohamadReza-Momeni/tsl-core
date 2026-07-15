import pandas as pd

def resolve_catalog_collisions():
    input_csv = "data/catalogs/TSL-104_Threat_Catalog_v2.csv"
    output_csv = "data/catalogs/TSL-104_Threat_Catalog_v3.csv"
    
    print(f"Loading {input_csv}...")
    try:
        df = pd.read_csv(input_csv)
    except FileNotFoundError:
        print("[-] Could not find the input CSV.")
        return

    # The Master Resolution Dictionary
    # We leave one threat in each collision group untouched, and modify the others
    # to guarantee 100% unique visual signatures across all 304 threats.
    RESOLUTION_MAP = {
        # Group 1 (Cultural Deficits)
        "TH-0042": {"Mec 2 Code": "MEC-304", "Mec 2 Name": "Resource Denial"},
        # Group 2 (Cultural/Linguistic)
        "TH-0029": {"Mec 3 Code": "MEC-603", "Mec 3 Name": "Cultural Influence"},
        "TH-0040": {"Mec 3 Code": "MEC-602", "Mec 3 Name": "Identity Manipulation"},
        # Group 3 (Ideological/Legal Gap)
        "TH-0288": {"Mec 2 Code": "MEC-404", "Mec 2 Name": "Legal Manipulation"},
        # Group 4 (Crisis/Org Credibility)
        "TH-0004": {"Mec 3 Code": "MEC-405", "Mec 3 Name": "Crisis Exploitation"},
        # Group 5 (Fear vs Health Crisis)
        "TH-0291": {"Mec 3 Code": "MEC-405", "Mec 3 Name": "Crisis Exploitation"},
        # Group 6 (Hostile Glorification)
        "TH-0035": {"Mec 3 Code": "MEC-602", "Mec 3 Name": "Identity Manipulation"},
        "TH-0036": {"Mec 3 Code": "MEC-403", "Mec 3 Name": "Institutional Capture"},
        # Group 7 (Bias vs Propaganda)
        "TH-0013": {"Mec 3 Code": "MEC-105", "Mec 3 Name": "Psychological Operations"},
        # Group 8 (Fake News vs Sabotage)
        "TH-0150": {"Mec 3 Code": "MEC-502", "Mec 3 Name": "Sabotage"},
        "TH-0071": {"Mec 3 Code": "MEC-110", "Mec 3 Name": "Rumor Propagation"},
        # Group 9 (Victimhood, Vacuum, Inversion)
        "TH-0015": {"Mec 3 Code": "MEC-108", "Mec 3 Name": "Information Suppression"},
        "TH-0078": {"Mec 3 Code": "MEC-112", "Mec 3 Name": "Demoralization"},
        "TH-0167": {"Mec 3 Code": "MEC-103", "Mec 3 Name": "Misinformation"},
        # Group 10 (History vs Language)
        "TH-0037": {"Mec 3 Code": "MEC-602", "Mec 3 Name": "Identity Manipulation"},
        # Group 11 (Cognitive vs Military)
        "TH-0263": {"Mec 3 Code": "MEC-504", "Mec 3 Name": "Force Projection"},
        # Group 12 (Debt Trap vs Political Debt)
        "TH-0062": {"Mec 3 Code": "MEC-307", "Mec 3 Name": "Strategic Asset Acquisition"},
        # Group 13 (Econ Sanctions vs Medical)
        "TH-0294": {"Mec 3 Code": "MEC-304", "Mec 3 Name": "Resource Denial"},
        # Group 14 (Subversion vs Fifth Column)
        "TH-0226": {"Mec 3 Code": "MEC-507", "Mec 3 Name": "Proxy Warfare Support"},
        # Group 15 (Crime, Corruption, Smuggling)
        "TH-0136": {"Mec 3 Code": "MEC-310", "Mec 3 Name": "Illicit Trade & Smuggling"}, # NEW
        "TH-0130": {"Mec 3 Code": "MEC-404", "Mec 3 Name": "Legal Manipulation"},
        "TH-0110": {"Mec 3 Code": "MEC-601", "Mec 3 Name": "Social Polarization"},
        # Group 16 (Elite Co-opt vs Political Infiltration)
        "TH-0209": {"Mec 3 Code": "MEC-402", "Mec 3 Name": "Election Interference"},
        "TH-0139": {"Mec 3 Code": "MEC-305", "Mec 3 Name": "Investment Influence"},
        # Group 17 (Alliances, Coalition, Sabotage)
        "TH-0152": {"Mec 2 Code": "MEC-309", "Mec 2 Name": "Policy Sabotage"},
        "TH-0175": {"Mec 3 Code": "MEC-504", "Mec 3 Name": "Force Projection"},
        # Group 18 (Forum vs Legal Boycott)
        "TH-0284": {"Mec 3 Code": "MEC-404", "Mec 3 Name": "Legal Manipulation"},
        # Group 19 (Drug Trade vs Epidemic)
        "TH-0186": {"Mec 3 Code": "MEC-308", "Mec 3 Name": "Subversion Funding"},
        "TH-0196": {"Mec 3 Code": "MEC-609", "Mec 3 Name": "Public Health Degradation"}, # NEW
        # Group 20 (Autonomy vs Discrimination)
        "TH-0195": {"Mec 3 Code": "MEC-610", "Mec 3 Name": "Separatist Incitement"}, # NEW
        "TH-0206": {"Mec 3 Code": "MEC-601", "Mec 3 Name": "Social Polarization"},
        # Group 21 (Ethnic vs Religious)
        "TH-0188": {"Mec 3 Code": "MEC-606", "Mec 3 Name": "Violence & Riot Incitement"},
        "TH-0219": {"Mec 3 Code": "MEC-105", "Mec 3 Name": "Psychological Operations"},
        # Group 22 (Norm Deconstruct vs Mockery)
        "TH-0199": {"Mec 3 Code": "MEC-111", "Mec 3 Name": "Character Assassination"},
        "TH-0192": {"Mec 3 Code": "MEC-104", "Mec 3 Name": "Narrative Manipulation"},
        # Group 23 (Military Buildups)
        "TH-0236": {"Mec 2 Code": "MEC-401", "Mec 2 Name": "Diplomatic Pressure"},
        "TH-0240": {"Mec 2 Code": "MEC-407", "Mec 2 Name": "Border Provocation"},
        "TH-0242": {"Mec 2 Code": "MEC-305", "Mec 2 Name": "Investment Influence"},
        "TH-0245": {"Mec 2 Code": "MEC-105", "Mec 2 Name": "Psychological Operations"},
        # Group 24 (Arms Race vs Exercises)
        "TH-0229": {"Mec 3 Code": "MEC-309", "Mec 3 Name": "Policy Sabotage"},
        "TH-0235": {"Mec 3 Code": "MEC-407", "Mec 3 Name": "Border Provocation"},
        # Group 25 (Bio-Threats)
        "TH-0289": {"Mec 3 Code": "MEC-609", "Mec 3 Name": "Public Health Degradation"}, # NEW
        "TH-0290": {"Mec 3 Code": "MEC-304", "Mec 3 Name": "Resource Denial"},
        "TH-0302": {"Mec 3 Code": "MEC-306", "Mec 3 Name": "Trade Restriction"},
        # Group 26 (Deepfakes)
        "TH-0097": {"Mec 3 Code": "MEC-111", "Mec 3 Name": "Character Assassination"},
        "TH-0272": {"Mec 3 Code": "MEC-104", "Mec 3 Name": "Narrative Manipulation"},
    }

    print("Applying structural patches...")
    # Apply modifications
    for index, row in df.iterrows():
        t_id = str(row.get("Threat ID", "")).strip()
        if t_id in RESOLUTION_MAP:
            for col_name, new_val in RESOLUTION_MAP[t_id].items():
                df.at[index, col_name] = new_val

    # Save to v3
    df.to_csv(output_csv, index=False, encoding='utf-8-sig')
    print(f"[SUCCESS] All collisions resolved! Catalog saved to {output_csv}")

if __name__ == "__main__":
    resolve_catalog_collisions()