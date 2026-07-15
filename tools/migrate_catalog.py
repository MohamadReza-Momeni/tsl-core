import pandas as pd

def migrate_actors():
    input_csv = "data/catalogs/TSL-104_Threat_Catalog_v1.csv"
    output_csv = "data/catalogs/TSL-104_Threat_Catalog_v2.csv"
    
    print(f"Loading {input_csv}...")
    try:
        df = pd.read_csv(input_csv).fillna("")
    except FileNotFoundError:
        print("[-] Could not find the input CSV.")
        return

    # MAPPING LOGIC
    # Map your old actor codes to the new 4 Affiliations. 
    # Adjust this dictionary to accurately reflect which old actors belong to which new category.
    # ACT-01: خودی (Self)
    # ACT-02: دوست (Ally)
    # ACT-03: دشمن (Enemy)
    # ACT-04: نامعلوم (Unknown)
    
    actor_mapping = {
        # Assuming Domestic/Internal actors are 'Self'
        "ACT-02": {"code": "ACT-01", "name": "خودی"}, 
        
        # Add any codes here that represent 'Allies'
        "ACT-05": {"code": "ACT-02", "name": "دوست"}, 
        
        # Assuming Foreign States, Terrorists, Intelligence, etc., are 'Enemy'
        "ACT-01": {"code": "ACT-03", "name": "دشمن"}, # Foreign State
        "ACT-03": {"code": "ACT-03", "name": "دشمن"}, # Military Org
        "ACT-04": {"code": "ACT-03", "name": "دشمن"}, # Intelligence Service
        "ACT-06": {"code": "ACT-03", "name": "دشمن"}, # Terrorist
        "ACT-07": {"code": "ACT-03", "name": "دشمن"}, # Proxy
        # ... map the rest of your 12 codes to ACT-03 or others as needed
        
        # Assuming missing or specific codes are 'Unknown'
        "ACT-99": {"code": "ACT-04", "name": "نامعلوم"}, 
    }

    def convert_actor(old_code):
        return actor_mapping.get(old_code, {"code": "ACT-04", "name": "نامعلوم"}) # Default to Unknown

    # Apply the mapping to the dataframe
    print("Migrating Actor columns...")
    
    # We update both the Initiating Actor and the Target Actor if your CSV has both
    for index, row in df.iterrows():
        init_actor_old = row.get("Init Actor Code", "")
        new_init = convert_actor(init_actor_old)
        df.at[index, "Init Actor Code"] = new_init["code"]
        df.at[index, "Init Actor Name"] = new_init["name"]
        
        # If your CSV has a Target Actor column, update it too
        if "Target Actor Code" in df.columns:
            tgt_actor_old = row.get("Target Actor Code", "")
            if tgt_actor_old: # Only convert if it's an actor (not a civilian target, etc)
                new_tgt = convert_actor(tgt_actor_old)
                df.at[index, "Target Actor Code"] = new_tgt["code"]
                df.at[index, "Target Actor Name"] = new_tgt["name"]

    # Save the new file
    df.to_csv(output_csv, index=False, encoding='utf-8-sig')
    print(f"[SUCCESS] Migration complete! Saved as {output_csv}")

if __name__ == "__main__":
    migrate_actors()