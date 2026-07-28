import pandas as pd

def fix_intra_icon_duplicates(input_csv="data/catalogs/TSL-104_Threat_Catalog_v5.csv", 
                              output_csv="data/catalogs/TSL-104_Threat_Catalog_v6.csv"):
    
    print(f"Loading catalog: {input_csv}...")
    try:
        df = pd.read_csv(input_csv).fillna("")
    except FileNotFoundError:
        print("[-] Missing file. Please check your path.")
        return

    # 1. TH-0049: Fix MEC 3
    idx_0049 = df.index[df['Threat ID'] == 'TH-0049'].tolist()
    if idx_0049:
        df.at[idx_0049[0], 'Mec 3 Code'] = 'MEC-306'
        df.at[idx_0049[0], 'Mec 3 Name'] = 'Trade Restriction'

    # 2. TH-0056: Fix MEC 3
    idx_0056 = df.index[df['Threat ID'] == 'TH-0056'].tolist()
    if idx_0056:
        df.at[idx_0056[0], 'Mec 3 Code'] = 'MEC-201'
        df.at[idx_0056[0], 'Mec 3 Name'] = 'Cyber Intrusion'

    # 3. TH-0274: Fix MEC 3
    idx_0274 = df.index[df['Threat ID'] == 'TH-0274'].tolist()
    if idx_0274:
        df.at[idx_0274[0], 'Mec 3 Code'] = 'MEC-206'
        df.at[idx_0274[0], 'Mec 3 Name'] = 'Supply Chain Compromise'

    # 4. TH-0292: Fix MEC 2
    idx_0292 = df.index[df['Threat ID'] == 'TH-0292'].tolist()
    if idx_0292:
        df.at[idx_0292[0], 'Mec 2 Code'] = 'MEC-403'
        df.at[idx_0292[0], 'Mec 2 Name'] = 'Institutional Capture'

    # Save out the clean v6 catalog
    df.to_csv(output_csv, index=False)
    print(f"[SUCCESS] Internal duplicates resolved. Catalog saved to: {output_csv}")

if __name__ == "__main__":
    fix_intra_icon_duplicates()