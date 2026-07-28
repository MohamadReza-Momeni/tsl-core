import pandas as pd

def check_intra_icon_duplicates(csv_path="data/catalogs/TSL-104_Threat_Catalog_v6.csv"):
    print(f"Loading catalog from: {csv_path}...\n")
    try:
        # Load the CSV and handle missing values
        df = pd.read_csv(csv_path).fillna("NONE")
    except FileNotFoundError:
        print("[-] Catalog not found. Please verify the file path.")
        return

    issues_found = 0
    print("=" * 80)
    print("CHECKING FOR INTERNAL MECHANISM DUPLICATIONS (Intra-Icon Overlaps)")
    print("=" * 80)

    for index, row in df.iterrows():
        tid = row['Threat ID']
        m1 = row['Mec 1 Code']
        m2 = row['Mec 2 Code']
        m3 = row['Mec 3 Code']
        
        # Collect the mechanisms, filtering out the "NONE" placeholders
        mechs = [m for m in [m1, m2, m3] if m != "NONE" and str(m).strip() != ""]
        
        # If the length of the list is different from the length of the set, we have a duplicate!
        if len(mechs) != len(set(mechs)):
            issues_found += 1
            name = row['Threat Name']
            print(f"[!] INTERNAL DUPLICATE FOUND: {tid} ({name})")
            print(f"    MEC1: {m1} | MEC2: {m2} | MEC3: {m3}\n")

    if issues_found == 0:
        print("[SUCCESS] No intra-icon mechanism duplicates found. Every glyph on your icons will be unique!")
    else:
        print(f"[-] Found {issues_found} threats with internal duplicates. These need to be patched.")

if __name__ == "__main__":
    # Point this to whatever your latest generated CSV file is!
    check_intra_icon_duplicates()