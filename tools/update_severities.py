import pandas as pd

def cycle_severities():
    # Adjust this path if you want to use v2 instead of v3
    csv_path = "data/catalogs/TSL-104_Threat_Catalog_v3.csv"
    
    print(f"Loading {csv_path}...")
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        print("[-] Could not find the CSV file. Please check the path.")
        return

    # A standard dictionary to map the number to a name. 
    # You can change these names to match your exact standard if needed.
    severity_names = {
        1: "Minimal",
        2: "Low",
        3: "Moderate",
        4: "High",
        5: "Severe",
        6: "Critical"
    }

    # df.index is the row number (starting at 0).
    # (df.index % 6) gives us 0, 1, 2, 3, 4, 5, 0, 1, 2...
    # Adding +1 shifts it to 1, 2, 3, 4, 5, 6, 1, 2, 3...
    new_severity_numbers = (df.index % 6) + 1

    # Apply the new codes and names to the DataFrame
    df["Sev Code"] = new_severity_numbers.map(lambda x: f"SEV-{x}")
    df["Sev Name"] = new_severity_numbers.map(severity_names)

    # Save the file back
    df.to_csv(csv_path, index=False, encoding='utf-8-sig')
    
    print(f"[SUCCESS] Severities updated! Cycled 1 through 6 across {len(df)} rows.")

if __name__ == "__main__":
    cycle_severities()