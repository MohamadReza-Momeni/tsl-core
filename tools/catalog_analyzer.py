import pandas as pd

def analyze_catalog_overlaps(csv_path="data/catalogs/6.csv"):
    print(f"Loading catalog from: {csv_path}...\n")
    try:
        # Fill NaN values with "NONE" so empty mechanisms/intents can be grouped together properly
        df = pd.read_csv(csv_path).fillna("NONE")
    except FileNotFoundError:
        print("[-] Catalog not found. Please verify the file path.")
        return

    # --- CRITERIA 1 ---
    # Domain, Actor, Visibility, Mechanisms (1, 2, 3), and Intent
    group_1_cols = [
        'Domain Code', 'Init Actor Code', 'Vis Code', 
        'Mec 1 Code', 'Mec 2 Code', 'Mec 3 Code', 'Intent Code'
    ]

    # --- CRITERIA 2 ---
    # Domain, Actor, Visibility, and Mechanisms (1, 2, 3) (Excludes Intent)
    group_2_cols = [
        'Domain Code', 'Init Actor Code', 'Vis Code', 
        'Mec 1 Code', 'Mec 2 Code', 'Mec 3 Code'
    ]

    print("=" * 80)
    print("ANALYSIS 1: Matching Domain, Actor, Visibility, Mechanisms, AND Intent")
    print("=" * 80)
    
    # Group the dataframe by the first criteria, count the IDs, and collect them into a list
    group_1_results = df.groupby(group_1_cols)['Threat ID'].agg(
        Count='count', 
        Threat_IDs=list
    ).reset_index()
    
    # Filter for entries that actually share attributes (Count > 1)
    shared_1 = group_1_results[group_1_results['Count'] > 1]
    
    if shared_1.empty:
        print("[!] No icons share all of these exact attributes.\n")
    else:
        for index, row in shared_1.iterrows():
            print(f"Count: {row['Count']} icons")
            print(f"IDs:   {', '.join(row['Threat_IDs'])}")
            print(f"Shared Attributes: DOM: {row['Domain Code']} | ACT: {row['Init Actor Code']} | VIS: {row['Vis Code']} | INT: {row['Intent Code']}")
            print(f"                   MEC1: {row['Mec 1 Code']} | MEC2: {row['Mec 2 Code']} | MEC3: {row['Mec 3 Code']}\n")

    print("=" * 80)
    print("ANALYSIS 2: Matching Domain, Actor, Visibility, and Mechanisms (Ignoring Intent)")
    print("=" * 80)
    
    # Group the dataframe by the second criteria
    group_2_results = df.groupby(group_2_cols)['Threat ID'].agg(
        Count='count', 
        Threat_IDs=list
    ).reset_index()
    
    # Filter for entries that actually share attributes (Count > 1)
    shared_2 = group_2_results[group_2_results['Count'] > 1]
    
    if shared_2.empty:
        print("[!] No icons share all of these exact attributes.\n")
    else:
        for index, row in shared_2.iterrows():
            print(f"Count: {row['Count']} icons")
            print(f"IDs:   {', '.join(row['Threat_IDs'])}")
            print(f"Shared Attributes: DOM: {row['Domain Code']} | ACT: {row['Init Actor Code']} | VIS: {row['Vis Code']}")
            print(f"                   MEC1: {row['Mec 1 Code']} | MEC2: {row['Mec 2 Code']} | MEC3: {row['Mec 3 Code']}\n")

if __name__ == "__main__":
    # You can update this string if your file path is different
    analyze_catalog_overlaps("data/catalogs/TSL-104_Threat_Catalog_v6.csv")

# import pandas as pd

# def patch_threat_catalog(input_csv="data/catalogs/TSL-104_Threat_Catalog_v3.csv", 
#                          output_csv="data/catalogs/TSL-104_Threat_Catalog_v4.csv"):
    
#     print(f"Loading catalog: {input_csv}...")
#     try:
#         # Load the CSV. We use fillna("") so empty cells are handled properly.
#         df = pd.read_csv(input_csv).fillna("")
#     except FileNotFoundError:
#         print("[-] Missing file. Please check your path.")
#         return

#     # --- 1. SECONDARY MECHANISM UPDATES ---
#     updates_secondary = {
#         "TH-0108": ("MEC-104", "Narrative Manipulation"),
#         "TH-0141": ("MEC-405", "Crisis Exploitation"),
#         "TH-0174": ("MEC-110", "Rumor Propagation"),
#         "TH-0178": ("MEC-306", "Trade Restriction"),
#         "TH-0179": ("MEC-404", "Legal Manipulation"),
#         "TH-0204": ("MEC-110", "Rumor Propagation"),
#         "TH-0205": ("MEC-606", "Violence & Riot Incitement"),
#         "TH-0276": ("MEC-304", "Resource Denial"),
#         "TH-0292": ("MEC-309", "Policy Sabotage"),
#         "TH-0304": ("MEC-609", "Public Health Degradation"),
#     }

#     # --- 2. TERTIARY MECHANISM UPDATES ---
#     updates_tertiary = {
#         "TH-0031": ("MEC-108", "Information Suppression"),
#         "TH-0034": ("MEC-110", "Rumor Propagation"),
#         "TH-0012": ("MEC-112", "Demoralization"),
#         "TH-0021": ("MEC-503", "Espionage"),
#         "TH-0018": ("MEC-113", "Educational Co-optation"),
#         "TH-0273": ("MEC-308", "Subversion Funding"),
#         "TH-0086": ("MEC-503", "Espionage"),
#         "TH-0224": ("MEC-207", "Data Harvesting & Microtargeting"),
#         "TH-0073": ("MEC-102", "Disinformation"),
#         "TH-0091": ("MEC-104", "Narrative Manipulation"),
#         "TH-0044": ("MEC-304", "Resource Denial"),
#         "TH-0265": ("MEC-309", "Policy Sabotage"),
#         "TH-0049": ("MEC-305", "Investment Influence"),
#         "TH-0050": ("MEC-307", "Strategic Asset Acquisition"),
#         "TH-0111": ("MEC-403", "Institutional Capture"),
#         "TH-0122": ("MEC-405", "Crisis Exploitation"),
#         "TH-0115": ("MEC-407", "Border Provocation"),
#         "TH-0172": ("MEC-105", "Psychological Operations"),
#         "TH-0262": ("MEC-507", "Proxy Warfare Support"),
#         "TH-0181": ("MEC-403", "Institutional Capture"),
#         "TH-0282": ("MEC-309", "Policy Sabotage"),
#         "TH-0225": ("MEC-302", "Market Manipulation"),
#         "TH-0228": ("MEC-205", "Credential Theft"),
#         "TH-0213": ("MEC-608", "Extremist Radicalization"),
#         "TH-0296": ("MEC-609", "Public Health Degradation"),
#         "TH-0212": ("MEC-601", "Social Polarization"),
#         "TH-0220": ("MEC-112", "Demoralization"),
#         "TH-0230": ("MEC-506", "Undeclared Gray-Zone Action"),
#         "TH-0236": ("MEC-105", "Psychological Operations"),
#         "TH-0257": ("MEC-304", "Resource Denial"),
#         "TH-0243": ("MEC-308", "Subversion Funding"),
#         "TH-0261": ("MEC-507", "Proxy Warfare Support"),
#         "TH-0253": ("MEC-403", "Institutional Capture"),
#         "TH-0274": ("MEC-203", "Data Exfiltration"),
#         "TH-0056": ("MEC-304", "Resource Denial"),
#         "TH-0297": ("MEC-609", "Public Health Degradation"),
#     }

#     # Initialize counters for the console output
#     sec_count = 0
#     ter_count = 0

#     # Iterate through the DataFrame and apply the patches
#     for index, row in df.iterrows():
#         tid = row['Threat ID']
        
#         # Check and apply Secondary updates
#         if tid in updates_secondary:
#             mech_code, mech_name = updates_secondary[tid]
#             df.at[index, 'Mec 2 Code'] = mech_code
#             df.at[index, 'Mec 2 Name'] = mech_name
#             sec_count += 1
            
#         # Check and apply Tertiary updates
#         if tid in updates_tertiary:
#             mech_code, mech_name = updates_tertiary[tid]
#             df.at[index, 'Mec 3 Code'] = mech_code
#             df.at[index, 'Mec 3 Name'] = mech_name
#             ter_count += 1

#     # Save the updated DataFrame to a new v4 file
#     df.to_csv(output_csv, index=False)
    
#     print(f"[SUCCESS] Applied {sec_count} Secondary Mechanism updates.")
#     print(f"[SUCCESS] Applied {ter_count} Tertiary Mechanism updates.")
#     print(f"[SUCCESS] Updated catalog saved to: {output_csv}")
#     print("You can now point your dashboard_generator.py and batch renderer to the new v4 CSV.")

# if __name__ == "__main__":
#     patch_threat_catalog()