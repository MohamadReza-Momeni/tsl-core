
import pandas as pd

def apply_final_surgical_patch(input_csv="data/catalogs/TSL-104_Threat_Catalog_v4.csv", 
                               output_csv="data/catalogs/TSL-104_Threat_Catalog_v5.csv"):
    
    print(f"Loading catalog: {input_csv}...")
    try:
        df = pd.read_csv(input_csv).fillna("")
    except FileNotFoundError:
        print("[-] Missing file. Please check your path.")
        return

    # 1. Update TH-0294 (Medical Sanctions) -> Swap MEC 3 to Public Health Degradation
    idx_0294 = df.index[df['Threat ID'] == 'TH-0294'].tolist()
    if idx_0294:
        df.at[idx_0294[0], 'Mec 3 Code'] = 'MEC-609'
        df.at[idx_0294[0], 'Mec 3 Name'] = 'Public Health Degradation'

    # 2. Update TH-0050 (Political Debt) -> Swap MEC 3 to Policy Sabotage
    idx_0050 = df.index[df['Threat ID'] == 'TH-0050'].tolist()
    if idx_0050:
        df.at[idx_0050[0], 'Mec 3 Code'] = 'MEC-309'
        df.at[idx_0050[0], 'Mec 3 Name'] = 'Policy Sabotage'

    # 3. Update TH-0286 (Travel Restrictions) -> Add MEC 3 to break the tie
    idx_0286 = df.index[df['Threat ID'] == 'TH-0286'].tolist()
    if idx_0286:
        df.at[idx_0286[0], 'Mec 3 Code'] = 'MEC-406'
        df.at[idx_0286[0], 'Mec 3 Name'] = 'International Forum Manipulation'

    # Save out the v5 catalog
    df.to_csv(output_csv, index=False)
    print(f"[SUCCESS] Final 3 overlaps resolved. Catalog saved to: {output_csv}")

if __name__ == "__main__":
    apply_final_surgical_patch()