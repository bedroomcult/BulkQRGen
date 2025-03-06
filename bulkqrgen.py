import os
import argparse
import pandas as pd
import qrcode
import qrcode.image.svg
import cairosvg
import shutil
import sys
import time
import random
import threading

# --- Argument Parsing ---
parser = argparse.ArgumentParser(description="Generate QR codes from a CSV file.")
parser.add_argument("-i", "--input", default="data.csv", help="CSV file containing QR data (default: data.csv)")
parser.add_argument("-logo", "--logo", help="Logo image file (PNG format, optional)")
parser.add_argument("-o", "--output", default="svg,pdf,png", help="Output format: svg, pdf, png (default: all)")
parser.add_argument("-size", "--size", type=int, default=500, help="QR code size in pixels (default: 500)")
parser.add_argument("-m", "--margin", type=int, default=20, help="Margin size around QR code (default: 20px)")
parser.add_argument("-ani", "--animate", action="store_true", help="Show animated 10x10 QR code cycling in terminal")
args = parser.parse_args()

# --- Parse Arguments ---
csv_filename = args.input
logo_path = args.logo
output_formats = args.output.split(",")
qr_size = args.size
margin_size = args.margin
show_animation = args.animate

# --- Validate Output Formats ---
valid_formats = {"svg", "pdf", "png"}
if not set(output_formats).issubset(valid_formats):
    print("Invalid output format! Use -o svg,pdf,png")
    exit(1)

# --- Set Up Output Directories ---
output_dirs = {"svg": "qr_svgs", "pdf": "qr_pdfs", "png": "qr_pngs"}
for fmt in valid_formats:
    os.makedirs(output_dirs[fmt], exist_ok=True)

# --- Read CSV File ---
try:
    df = pd.read_csv(csv_filename, header=None)
except Exception as e:
    print(f"Error reading CSV file: {e}")
    exit()

total_qr = len(df)

# --- Animated 10x10 QR Code in Terminal ---
def generate_random_qr_terminal():
    qr_data = "".join(random.choice("01") for _ in range(10 * 10))
    qr = qrcode.QRCode(version=1, box_size=1, border=0)
    qr.add_data(qr_data)
    qr.make(fit=True)
    qr_matrix = qr.modules

    output = "\033[H"  # Move cursor to the top
    for row in qr_matrix:
        output += "".join("█" if pixel else " " for pixel in row) + "\n"
    
    sys.stdout.write(output)
    sys.stdout.flush()

def animate_qr_terminal():
    try:
        while processing:
            generate_random_qr_terminal()
            time.sleep(0.3)  # Cycle one QR at a time with 0.3s delay
    except KeyboardInterrupt:
        pass

# --- Time Tracking ---
start_time = time.time()
processing = True

# Start animation if enabled
if show_animation:
    print("\033[2J")  # Clear screen
    animation_thread = threading.Thread(target=animate_qr_terminal, daemon=True)
    animation_thread.start()

# --- Generate QR Codes ---
for index, row in df.iterrows():
    data = str(row[0]).strip()
    if data:
        filenames = {
            "svg": os.path.join(output_dirs["svg"], f"qr_{index+1}.svg"),
            "pdf": os.path.join(output_dirs["pdf"], f"qr_{index+1}.pdf"),
            "png": os.path.join(output_dirs["png"], f"qr_{index+1}.png")
        }

        # --- Generate QR Code (SVG first) ---
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_H if logo_path else qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=margin_size // 10
        )
        qr.add_data(data)
        qr.make(fit=True)

        # Always generate SVG
        qr_svg = qr.make_image(image_factory=qrcode.image.svg.SvgImage)
        qr_svg.save(filenames["svg"])

        # Convert to PDF
        if "pdf" in output_formats:
            cairosvg.svg2pdf(url=filenames["svg"], write_to=filenames["pdf"])

        # Convert to PNG
        if "png" in output_formats:
            from PIL import Image

            png_size = 2048  
            qr_size_ratio = 0.9
            qr_size_png = int(png_size * qr_size_ratio)
            margin_png = (png_size - qr_size_png) // 2

            img = Image.new("RGB", (png_size, png_size), "white")
            qr_png = qr.make_image(fill_color="black", back_color="white").convert("RGB")
            qr_png = qr_png.resize((qr_size_png, qr_size_png), Image.Resampling.LANCZOS)
            img.paste(qr_png, (margin_png, margin_png))
            img.save(filenames["png"])

# Stop animation
processing = False

# --- Delete Unwanted SVG Files ---
if "svg" not in output_formats:
    for file in os.listdir(output_dirs["svg"]):
        os.remove(os.path.join(output_dirs["svg"], file))
    os.rmdir(output_dirs["svg"])

# --- Time Tracking ---
end_time = time.time()
total_time = end_time - start_time
average_time = total_time / total_qr if total_qr > 0 else 0

# --- Clear Animation & Print Summary ---
if show_animation:
    print("\033[2J\033[H")  # Clear screen

print(f"QR code generation completed in {total_time:.2f} seconds.")
print(f"Average time per QR code: {average_time:.2f} seconds.")