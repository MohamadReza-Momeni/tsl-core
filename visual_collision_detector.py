import pandas as pd

def find_visual_duplicates():
    csv_path = "data/catalogs/TSL-104_Threat_Catalog_v2.csv"
    try:
        df = pd.read_csv(csv_path)
        
        # Clean columns and drop empty ghost rows
        df.columns = df.columns.str.strip()
        df = df.dropna(subset=["Threat ID"])
        df = df[df["Threat ID"].astype(str).str.strip() != ""]
        df = df.fillna("")
        
    except FileNotFoundError:
        print("[-] Catalog not found.")
        return

    # These are the exact columns that dictate the visual output of the SVG
    visual_columns = [
        "Init Actor Code",
        "Domain Code",
        "Intent Code",
        "Mec 1 Code",
        "Mec 2 Code",
        "Sev Code"  # Severity dictates color. (Remove this if you want to ignore color)
    ]

    # Verify all columns exist in the CSV
    missing_cols = [col for col in visual_columns if col not in df.columns]
    if missing_cols:
        print(f"[-] WARNING: Missing columns in CSV: {missing_cols}")
        visual_columns = [col for col in visual_columns if col in df.columns]

    # Clean whitespace from the data so we don't get false mismatches
    for col in visual_columns:
        df[col] = df[col].astype(str).str.strip()

    # Group the dataframe by the visual signature and collect the Threat IDs that share it
    duplicates = df.groupby(visual_columns).apply(lambda x: x['Threat ID'].tolist()).reset_index(name='Threat_IDs')
    
    # Filter to only show groups that have MORE THAN ONE Threat ID
    duplicates = duplicates[duplicates['Threat_IDs'].map(len) > 1]

    total_threats = len(df)
    total_collisions = len(duplicates)
    affected_threats = duplicates['Threat_IDs'].map(len).sum()

    print(f"\n=== TSL VISUAL COLLISION REPORT ===")
    print(f"Total Threats Analyzed: {total_threats}")
    print(f"Number of Collisions (Shared Icons): {total_collisions}")
    print(f"Total Threats Affected: {affected_threats}\n")

    if total_collisions == 0:
        print("✅ Excellent: Every single threat has a 100% unique icon.")
        return

    print("--- DETAILED COLLISION LIST ---\n")
    for index, row in duplicates.iterrows():
        print("=" * 50)
        print("Shared Visual Signature:")
        for col in visual_columns:
            print(f"  {col}: {row.get(col, '')}")
        
        print(f"\nIdentical Threats ({len(row['Threat_IDs'])}):")
        for t_id in row['Threat_IDs']:
            # Try to grab the threat name/description to print alongside the ID
            # Adjust 'شرح تهدید' to whatever your name/description column is named
            desc_cols = [c for c in df.columns if 'شرح' in c or 'name' in c.lower()]
            threat_desc = df[df['Threat ID'] == t_id][desc_cols[0]].values[0] if desc_cols else ""
            print(f"  - {t_id} : {threat_desc[:60]}...")
    
    print("=" * 50)

if __name__ == "__main__":
    find_visual_duplicates()