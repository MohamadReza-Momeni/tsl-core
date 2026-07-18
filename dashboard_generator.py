import pandas as pd
import os
import html

def generate_dashboard():
    # Setup paths
    csv_path = "data/catalogs/TSL-104_Threat_Catalog_v3.csv"
    template_path = "templates/dashboard_template.html"
    output_html = "output/dashboard.html"
    renders_dir = "renders"  

    print(f"Loading catalog: {csv_path}...")
    try:
        df = pd.read_csv(csv_path).fillna("")
        with open(template_path, 'r', encoding='utf-8') as f:
            html_template = f.read()
    except FileNotFoundError as e:
        print(f"[-] Missing file: {e}")
        return

    cards_html = ""

    # Generate Cards dynamically
    for index, row in df.iterrows():
        # Core details
        threat_id = row.get("Threat ID", f"UNKNOWN-{index}")
        threat_name = str(row.get("Threat Name", "")).strip()
        description = str(row.get("Original Description", "")).strip()
        
        # Badge Codes and Names
        domain = row.get("Domain Code", "")
        domain_name = str(row.get("Domain Name", "")).strip()
        
        actor = row.get("Init Actor Code", "")
        actor_name = str(row.get("Init Actor Name", "")).strip()
        
        intent = row.get("Intent Code", "")
        intent_name = str(row.get("Intent Name", "")).strip()
        
        # Mechanisms
        mec1_name = str(row.get("Mec 1 Name", "")).strip().title() or "Unknown Mechanism"
        mec2_name = str(row.get("Mec 2 Name", "")).strip().title()
        mec3_name = str(row.get("Mec 3 Name", "")).strip().title()

        # Safely escape text for HTML injection
        safe_threat_name = html.escape(threat_name)
        safe_description = html.escape(description)
        safe_domain_name = html.escape(domain_name)
        safe_actor_name = html.escape(actor_name)
        safe_intent_name = html.escape(intent_name)

        svg_path = f"{renders_dir}/{threat_id}.svg"
        
        # Include all text in the search string for robust filtering
        search_data = f"{threat_id} {threat_name} {domain} {domain_name} {actor} {actor_name} {intent} {intent_name} {mec1_name} {mec2_name} {mec3_name}".lower()

        # Conditionally format secondary/tertiary HTML
        mec2_html = f'<p class="desc"><strong>Secondary:</strong><br>{mec2_name}</p>' if mec2_name else ''
        mec3_html = f'<p class="desc"><strong>Tertiary:</strong><br>{mec3_name}</p>' if mec3_name else ''
        
        # Build the intent badge (only if an intent exists)
        intent_badge = f'<span class="badge badge-intent" title="{safe_intent_name}">{intent}</span>' if intent else ''

        card_html = f"""
            <div class="card" data-search="{search_data}">
                <div class="icon-container">
                    <img src="{svg_path}" alt="{threat_id}" onerror="this.src='data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxMDAgMTAwIj48cmVjdCB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgZmlsbD0iIzMzNDE1NSIvPjx0ZXh0IHg9IjUwJSIgeT0iNTAlIiBkb21pbmFudC1iYXNlbGluZT0ibWlkZGxlIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmaWxsPSIjOTRhM2I4IiBmb250LWZhbWlseT0ic2Fucy1zZXJpZiIgZm9udC1zaXplPSIxMiI+TWlzc2luZzwvdGV4dD48L3N2Zz4='">
                    <div class="tooltip">
                        <h4 dir="auto">{safe_threat_name}</h4>
                        <p dir="rtl" style="text-align: right; font-family: Tahoma, Arial, sans-serif; line-height: 1.6; margin-top: 5px;">{safe_description}</p>
                    </div>
                </div>
                <h3>{threat_id}</h3>
                <div class="badges">
                    <span class="badge badge-domain" title="{safe_domain_name}">{domain}</span>
                    <span class="badge badge-actor" title="{safe_actor_name}">{actor}</span>
                    {intent_badge}
                </div>
                <div class="desc-container">
                    <p class="desc"><strong>Primary Method:</strong><br>{mec1_name}</p>
                    {mec2_html}
                    {mec3_html}
                </div>
            </div>
        """
        cards_html += card_html

    # Inject cards into the template
    final_html = html_template.replace("<!-- THREAT_CARDS_PLACEHOLDER -->", cards_html)

    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(final_html)
    
    print(f"[SUCCESS] Dashboard generated successfully at: {output_html}")

if __name__ == "__main__":
    generate_dashboard()