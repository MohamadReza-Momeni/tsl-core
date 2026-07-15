import os
import re
import sys

try:
    import fitz  # This is the PyMuPDF library
except ImportError:
    print("[-] Error: PyMuPDF is missing.")
    print("    Please install it using: pip install pymupdf")
    sys.exit(1)

def convert_directory(input_dir, scale=3.0):
    """
    Converts all .svg files in the given directory to .png files with transparent backgrounds
    using the highly robust MuPDF engine.
    """
    # 1. Validate the input directory
    if not os.path.exists(input_dir) or not os.path.isdir(input_dir):
        print(f"[-] Error: Directory '{input_dir}' does not exist.")
        return

    # 2. Create the output directory name
    clean_input_dir = input_dir.rstrip("\\/")
    output_dir = f"{clean_input_dir}_png"

    os.makedirs(output_dir, exist_ok=True)
    print(f"[+] Output directory created: {output_dir}")

    # 3. Find all SVG files
    svg_files = [f for f in os.listdir(clean_input_dir) if f.lower().endswith('.svg')]
    
    if not svg_files:
        print(f"[-] No SVG files found in '{clean_input_dir}'.")
        return

    print(f"[+] Found {len(svg_files)} SVG files. Starting PyMuPDF conversion...")

    # 4. Convert files
    success_count = 0
    fail_count = 0

    # Create a scaling matrix. Scale of 3.0 gives crisp 300x300 PNGs
    zoom_matrix = fitz.Matrix(scale, scale)

    for filename in svg_files:
        svg_path = os.path.join(clean_input_dir, filename)
        png_filename = filename[:-4] + ".png" 
        png_path = os.path.join(output_dir, png_filename)

        try:
            # Step A: Read the SVG as raw text
            with open(svg_path, 'r', encoding='utf-8') as f:
                svg_content = f.read()

            # Step B: CSS Color Hack for MuPDF
            # MuPDF ignores embedded <style> blocks, so we extract your Severity color 
            # and replace the 'currentColor' variables manually before rendering.
            color_match = re.search(r'\.tsl-threat\s*\{\s*color:\s*(#[0-9a-fA-F]{6});\s*\}', svg_content)
            if color_match:
                threat_color = color_match.group(1)
                svg_content = svg_content.replace('currentColor', threat_color)

            # Step C: Load the modified SVG into memory
            svg_bytes = svg_content.encode('utf-8')
            doc = fitz.open(stream=svg_bytes, filetype="svg")
            page = doc[0]
            
            # Step D: Render to PNG (alpha=True ensures transparent background)
            pix = page.get_pixmap(alpha=True, matrix=zoom_matrix)
            pix.save(png_path)
            
            doc.close()
            
            success_count += 1
            if success_count % 50 == 0:
                print(f"    ...converted {success_count}/{len(svg_files)}")
                
        except Exception as e:
            print(f"[-] Failed to convert {filename}: {e}")
            fail_count += 1

    # 5. Final Report
    print("\n=== Conversion Complete ===")
    print(f"Successfully converted: {success_count}")
    if fail_count > 0:
        print(f"Failed to convert: {fail_count}")
    print(f"PNGs saved to: {os.path.abspath(output_dir)}")

if __name__ == "__main__":
    print("=== TSL SVG to PNG Converter (PyMuPDF Engine) ===")
    user_input = input("Enter the path to the SVG folder (e.g., output/renders): ").strip()
    
    # Using a scale of 3.0 gives beautiful, high-res PNGs suitable for presentations
    convert_directory(user_input, scale=3.0)