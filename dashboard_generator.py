import pandas as pd
import os

def generate_dashboard():
    # Setup paths
    csv_path = "data/catalogs/TSL-104_Threat_Catalog_v2.csv"
    output_html = "output/dashboard.html"
    renders_dir = "renders"  

    print(f"Loading catalog: {csv_path}...")
    try:
        df = pd.read_csv(csv_path).fillna("")
    except FileNotFoundError:
        print("[-] Catalog not found. Please ensure the CSV is in the correct directory.")
        return

    # 1. HTML Header & CSS with Light/Dark Theme Variables
    html_content = """
    <!DOCTYPE html>
    <html lang="en" data-theme="dark">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>TSL-104 Canonical Threat Catalog</title>
        <style>
            /* --- Theme Variables --- */
            :root[data-theme="dark"] {
                --bg-main: #0f172a;
                --bg-card: #1e293b;
                --text-main: #e2e8f0;
                --text-muted: #94a3b8;
                --border-color: #334155;
                --accent: #38bdf8;
                --shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
                --shadow-hover: 0 10px 15px rgba(0, 0, 0, 0.5);
                --svg-filter: drop-shadow(0 0 8px rgba(0,0,0,0.5));
            }
            :root[data-theme="light"] {
                --bg-main: #f8fafc;
                --bg-card: #ffffff;
                --text-main: #0f172a;
                --text-muted: #64748b;
                --border-color: #e2e8f0;
                --accent: #0284c7;
                --shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
                --shadow-hover: 0 10px 15px rgba(0, 0, 0, 0.1);
                --svg-filter: drop-shadow(0 4px 6px rgba(0,0,0,0.1));
            }

            /* --- Base Styles --- */
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: var(--bg-main); color: var(--text-main); margin: 0; padding: 20px; transition: background-color 0.3s, color 0.3s; }
            header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; border-bottom: 1px solid var(--border-color); padding-bottom: 20px; transition: border-color 0.3s; }
            h1 { margin: 0; font-size: 28px; color: var(--accent); letter-spacing: 1px; }
            .header-controls { display: flex; gap: 15px; align-items: center; }
            
            #searchBar { width: 300px; padding: 12px 20px; border-radius: 8px; border: 1px solid var(--border-color); background: var(--bg-card); color: var(--text-main); outline: none; font-size: 16px; transition: border-color 0.3s, background-color 0.3s, color 0.3s; }
            #searchBar:focus { border-color: var(--accent); }
            
            #themeToggle { background: var(--bg-card); border: 1px solid var(--border-color); color: var(--text-main); padding: 10px 15px; border-radius: 8px; cursor: pointer; font-weight: bold; transition: all 0.3s; }
            #themeToggle:hover { border-color: var(--accent); color: var(--accent); }

            .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 25px; }
            .card { background: var(--bg-card); border-radius: 12px; padding: 25px; text-align: center; border: 1px solid var(--border-color); transition: transform 0.2s, border-color 0.2s, background-color 0.3s, box-shadow 0.3s; box-shadow: var(--shadow); display: flex; flex-direction: column; }
            .card:hover { transform: translateY(-5px); border-color: var(--accent); box-shadow: var(--shadow-hover); }
            .card img { width: 180px; height: 180px; margin-bottom: 20px; filter: var(--svg-filter); transition: filter 0.3s; align-self: center; }
            .card h3 { margin: 0 0 15px 0; font-size: 20px; color: var(--text-main); }
            
            .badges { display: flex; justify-content: center; gap: 8px; margin-bottom: 15px; flex-wrap: wrap; }
            .badge { padding: 6px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
            .badge-domain { background: rgba(56, 189, 248, 0.1); color: #0284c7; border: 1px solid rgba(56, 189, 248, 0.2); }
            .badge-actor { background: rgba(244, 63, 94, 0.1); color: #e11d48; border: 1px solid rgba(244, 63, 94, 0.2); }
            .badge-intent { background: rgba(167, 139, 250, 0.1); color: #9333ea; border: 1px solid rgba(167, 139, 250, 0.2); }
            
            :root[data-theme="dark"] .badge-domain { color: #38bdf8; }
            :root[data-theme="dark"] .badge-actor { color: #fb7185; }
            :root[data-theme="dark"] .badge-intent { color: #c084fc; }

            .desc-container { margin-top: auto; padding-top: 15px; border-top: 1px solid var(--border-color); }
            .desc { font-size: 13px; color: var(--text-muted); margin: 0 0 8px 0; line-height: 1.4; }
            .desc:last-child { margin-bottom: 0; }
            .desc strong { color: var(--text-main); font-weight: 600; }
            .hidden { display: none; }
        </style>
    </head>
    <body>
        <header>
            <div>
                <h1>TSL-104 Catalog</h1>
                <p style="margin: 5px 0 0 0; color: var(--text-muted); font-size: 14px; transition: color 0.3s;">Interactive Standard Symbology Reference</p>
            </div>
            <div class="header-controls">
                <input type="text" id="searchBar" placeholder="Search by ID, Domain, Actor, or Mechanism..." onkeyup="filterCards()">
                <button id="themeToggle" onclick="toggleTheme()">☀️ Light Mode</button>
            </div>
        </header>
        <div class="grid" id="threatGrid">
    """

    # 2. Generate Cards dynamically
    for index, row in df.iterrows():
        threat_id = row.get("Threat ID", f"UNKNOWN-{index}")
        domain = row.get("Domain Code", "")
        actor = row.get("Init Actor Code", "")
        intent = row.get("Intent Code", "")
        mec1_name = str(row.get("Mec 1 Name", "")).strip().title()
        mec2_name = str(row.get("Mec 2 Name", "")).strip().title()

        if not mec1_name:
            mec1_name = "Unknown Mechanism"

        svg_path = f"{renders_dir}/{threat_id}.svg"
        
        # Include mec2 in the search string so users can filter by secondary mechanisms
        search_data = f"{threat_id} {domain} {actor} {intent} {mec1_name} {mec2_name}".lower()

        # Conditionally format the secondary mechanism HTML
        mec2_html = f'<p class="desc"><strong>Secondary:</strong><br>{mec2_name}</p>' if mec2_name else ''

        card_html = f"""
            <div class="card" data-search="{search_data}">
                <img src="{svg_path}" alt="{threat_id}" onerror="this.src='data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxMDAgMTAwIj48cmVjdCB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgZmlsbD0iIzMzNDE1NSIvPjx0ZXh0IHg9IjUwJSIgeT0iNTAlIiBkb21pbmFudC1iYXNlbGluZT0ibWlkZGxlIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmaWxsPSIjOTRhM2I4IiBmb250LWZhbWlseT0ic2Fucy1zZXJpZiIgZm9udC1zaXplPSIxMiI+TWlzc2luZzwvdGV4dD48L3N2Zz4='">
                <h3>{threat_id}</h3>
                <div class="badges">
                    <span class="badge badge-domain">{domain}</span>
                    <span class="badge badge-actor">{actor}</span>
                    {f'<span class="badge badge-intent">{intent}</span>' if intent else ''}
                </div>
                <div class="desc-container">
                    <p class="desc"><strong>Primary Method:</strong><br>{mec1_name}</p>
                    {mec2_html}
                </div>
            </div>
        """
        html_content += card_html

    # 3. Close HTML and add JavaScript
    html_content += """
        </div>
        <script>
            // Search Filtering
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

            // Theme Toggling
            function toggleTheme() {
                const htmlElement = document.documentElement;
                const toggleBtn = document.getElementById('themeToggle');
                
                if (htmlElement.getAttribute('data-theme') === 'dark') {
                    htmlElement.setAttribute('data-theme', 'light');
                    toggleBtn.innerHTML = '🌙 Dark Mode';
                    localStorage.setItem('tsl-theme', 'light');
                } else {
                    htmlElement.setAttribute('data-theme', 'dark');
                    toggleBtn.innerHTML = '☀️ Light Mode';
                    localStorage.setItem('tsl-theme', 'dark');
                }
            }

            // Load saved theme on startup
            window.onload = function() {
                const savedTheme = localStorage.getItem('tsl-theme') || 'dark';
                document.documentElement.setAttribute('data-theme', savedTheme);
                
                const toggleBtn = document.getElementById('themeToggle');
                if (savedTheme === 'light') {
                    toggleBtn.innerHTML = '🌙 Dark Mode';
                } else {
                    toggleBtn.innerHTML = '☀️ Light Mode';
                }
            };
        </script>
    </body>
    </html>
    """

    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"[SUCCESS] Dashboard generated successfully at: {output_html}")

if __name__ == "__main__":
    generate_dashboard()