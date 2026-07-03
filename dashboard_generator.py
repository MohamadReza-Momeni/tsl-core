import pandas as pd
import os

def generate_dashboard():
    # Setup paths
    csv_path = "data/catalogs/TSL-104_Threat_Catalog_v1.csv"
    output_html = "output/dashboard.html"
    renders_dir = "renders"  # Relative path from dashboard.html to the SVGs

    print(f"Loading catalog: {csv_path}...")
    try:
        # Load data, filling blanks with empty strings
        df = pd.read_csv(csv_path).fillna("")
    except FileNotFoundError:
        print("[-] Catalog not found. Please ensure the CSV is in the correct directory.")
        return

    # 1. HTML Header & CSS (Dark Mode Military/Cyber Aesthetic)
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>TSL-104 Canonical Threat Catalog</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0f172a; color: #e2e8f0; margin: 0; padding: 20px; }
            header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; border-bottom: 1px solid #334155; padding-bottom: 20px; }
            h1 { margin: 0; font-size: 28px; color: #38bdf8; letter-spacing: 1px; }
            #searchBar { width: 350px; padding: 12px 20px; border-radius: 8px; border: 1px solid #334155; background: #1e293b; color: #fff; outline: none; font-size: 16px; transition: border-color 0.3s; }
            #searchBar:focus { border-color: #38bdf8; }
            .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 25px; }
            .card { background: #1e293b; border-radius: 12px; padding: 25px; text-align: center; border: 1px solid #334155; transition: transform 0.2s, border-color 0.2s; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); }
            .card:hover { transform: translateY(-5px); border-color: #38bdf8; box-shadow: 0 10px 15px rgba(0, 0, 0, 0.2); }
            .card img { width: 180px; height: 180px; margin-bottom: 20px; filter: drop-shadow(0 0 8px rgba(0,0,0,0.5)); }
            .card h3 { margin: 0 0 15px 0; font-size: 20px; color: #f8fafc; }
            .badges { display: flex; justify-content: center; gap: 8px; margin-bottom: 15px; flex-wrap: wrap; }
            .badge { padding: 6px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
            .badge-domain { background: rgba(56, 189, 248, 0.1); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.2); }
            .badge-actor { background: rgba(244, 63, 94, 0.1); color: #fb7185; border: 1px solid rgba(244, 63, 94, 0.2); }
            .badge-intent { background: rgba(167, 139, 250, 0.1); color: #c084fc; border: 1px solid rgba(167, 139, 250, 0.2); }
            .desc { font-size: 14px; color: #94a3b8; margin: 0; line-height: 1.5; }
            .hidden { display: none; }
        </style>
    </head>
    <body>
        <header>
            <div>
                <h1>TSL-104 Catalog</h1>
                <p style="margin: 5px 0 0 0; color: #94a3b8; font-size: 14px;">Interactive Standard Symbology Reference</p>
            </div>
            <input type="text" id="searchBar" placeholder="Search by ID, Domain, Actor, or Mechanism..." onkeyup="filterCards()">
        </header>
        <div class="grid" id="threatGrid">
    """

    # 2. Generate Cards dynamically from the CSV
    for index, row in df.iterrows():
        threat_id = row.get("Threat ID", f"UNKNOWN-{index}")
        domain = row.get("Domain Code", "")
        actor = row.get("Init Actor Code", "")
        intent = row.get("Intent Code", "")
        mec_name = row.get("Mec 1 Name", "Unknown Mechanism").title()

        # Path to the generated SVG image
        svg_path = f"{renders_dir}/{threat_id}.svg"
        
        # A searchable string combining all key metadata
        search_data = f"{threat_id} {domain} {actor} {intent} {mec_name}".lower()

        card_html = f"""
            <div class="card" data-search="{search_data}">
                <img src="{svg_path}" alt="{threat_id}" onerror="this.src='data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxMDAgMTAwIj48cmVjdCB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgZmlsbD0iIzMzNDE1NSIvPjx0ZXh0IHg9IjUwJSIgeT0iNTAlIiBkb21pbmFudC1iYXNlbGluZT0ibWlkZGxlIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmaWxsPSIjOTRhM2I4IiBmb250LWZhbWlseT0ic2Fucy1zZXJpZiIgZm9udC1zaXplPSIxMiI+TWlzc2luZzwvdGV4dD48L3N2Zz4='">
                <h3>{threat_id}</h3>
                <div class="badges">
                    <span class="badge badge-domain">{domain}</span>
                    <span class="badge badge-actor">{actor}</span>
                    {f'<span class="badge badge-intent">{intent}</span>' if intent else ''}
                </div>
                <p class="desc"><strong>Primary Method:</strong><br>{mec_name}</p>
            </div>
        """
        html_content += card_html

    # 3. Close HTML and add JavaScript for the search filter
    html_content += """
        </div>
        <script>
            function filterCards() {
                const input = document.getElementById('searchBar').value.toLowerCase();
                const cards = document.querySelectorAll('.card');
                
                cards.forEach(card => {
                    const searchData = card.getAttribute('data-search');
                    if (searchData.includes(input)) {
                        card.classList.remove('hidden');
                    } else {
                        card.classList.add('hidden');
                    }
                });
            }
        </script>
    </body>
    </html>
    """

    # Write file
    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"[SUCCESS] Dashboard generated successfully at: {output_html}")

if __name__ == "__main__":
    generate_dashboard()