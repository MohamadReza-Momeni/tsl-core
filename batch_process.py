import pandas as pd
import os
import json
from src.compiler.tsl_compiler import TSLCompiler
from src.renderer.svg_builder import SVGRenderer

def run_batch():
    # Setup
    csv_path = "data/catalogs/TSL-104_Threat_Catalog_v1.csv"
    compiler = TSLCompiler()
    renderer = SVGRenderer()
    
    # Load Catalog
    print(f"Loading catalog: {csv_path}...")
    
    # FIX: .fillna("") ensures blank cells are treated as empty text, not floats
    df = pd.read_csv(csv_path).fillna("")
    
    # Process each row
    total = len(df)
    print(f"Processing {total} threats...")
    
    for index, row in df.iterrows():
        # Convert row to dictionary
        threat_record = row.to_dict()
        
        # 1. Compile
        try:
            ris_json = compiler.compile(threat_record)
            
            # Save RIS file
            ris_dir = "output/ris"
            os.makedirs(ris_dir, exist_ok=True)
            ris_path = os.path.join(ris_dir, f"{threat_record['Threat ID']}.json")
            with open(ris_path, 'w', encoding='utf-8') as f:
                f.write(ris_json)
                
            # 2. Render
            renderer.build_symbol(ris_path)
            
            print(f"[{index+1}/{total}] Finished: {threat_record.get('Threat ID', 'UNKNOWN')}")
            
        except Exception as e:
            print(f"[-] Error processing {threat_record.get('Threat ID', 'UNKNOWN')}: {e}")

if __name__ == "__main__":
    run_batch()