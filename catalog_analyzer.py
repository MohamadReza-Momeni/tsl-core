import pandas as pd

def analyze_catalog_overlaps(csv_path="data/catalogs/TSL-104_Threat_Catalog_v3.csv"):
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
    analyze_catalog_overlaps("data/catalogs/TSL-104_Threat_Catalog_v3.csv")