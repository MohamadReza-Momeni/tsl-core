import pandas as pd

def extract_for_generation():
    csv_path = "data/catalogs/TSL-104_Threat_Catalog_v4.csv"
    try:
        df = pd.read_csv(csv_path).fillna("")
    except FileNotFoundError:
        print("[-] Could not find the CSV. Please ensure the path is correct.")
        return

    # Dictionary to hold unique Code -> Name pairs
    mechanisms = {}

    # Loop through the three possible mechanism columns in your CSV
    for index, row in df.iterrows():
        for i in [1, 2, 3]:
            code = str(row.get(f"Mec {i} Code", "")).strip()
            name = str(row.get(f"Mec {i} Name", "")).strip()
            
            # If it's a valid MEC code, add it to our dictionary
            if code.startswith("MEC") and name:
                mechanisms[code] = name

    print("\n✅ Extraction Complete! Copy the text below and paste it to me in the chat:\n")
    print("-------------------- START COPY --------------------")
    for code in sorted(mechanisms.keys()):
        print(f"{code} : {mechanisms[code]}")
    print("--------------------- END COPY ---------------------")

if __name__ == "__main__":
    extract_for_generation()