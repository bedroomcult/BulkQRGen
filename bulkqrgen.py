import os
import pandas as pd
import qrcode
import qrcode.image.svg
import cairosvg
from PIL import Image
import sys
import time
import shutil  # <-- Added to detect terminal size

# --- User Inputs ---
try:
    generate_png = input("Do you want to generate PNG images? (y/n): ").strip().lower() == 'y'

    if generate_png:
        use_logo = input("Do you want to add a logo? (y/n): ").strip().lower() == 'y'
    
    qr_size_input = int(input("Enter QR code size in pixels for SVG/PDF (e.g., 1000): ").strip())

except ValueError:
    print("Invalid input. Please enter a valid number for the QR code size.")
    exit()

# Input CSV file
csv_filename = "data.csv"
logo_path = "logo.png"

# Output directories
svg_dir = "qr_svgs"
pdf_dir = "qr_pdfs"
png_dir = "qr_pngs"
os.makedirs(svg_dir, exist_ok=True)
os.makedirs(pdf_dir, exist_ok=True)
if generate_png:
    os.makedirs(png_dir, exist_ok=True)

# SVG/PDF QR Code Size (user-defined)
qr_size_svg_pdf = qr_size_input

# PNG Settings (Only if enabled)
if generate_png:
    png_size = 2048  # Fixed PNG output size
    qr_size_ratio = 0.9  # QR code occupies 90% of the image
    qr_size_png = int(png_size * qr_size_ratio)
    margin_png = (png_size - qr_size_png) // 2

    # Logo Settings (Only if PNG is enabled)
    if use_logo:
        logo_size_ratio = 0.2
        logo_size_png = int(qr_size_png * logo_size_ratio)
        border_ratio = 0.05
        border_size = int(logo_size_png * border_ratio)

        if os.path.exists(logo_path):
            logo = Image.open(logo_path).convert("RGBA")
            logo = logo.resize((logo_size_png, logo_size_png), Image.Resampling.LANCZOS)

            # Create a white border
            logo_with_border_size = logo_size_png + 2 * border_size
            logo_with_border = Image.new("RGBA", (logo_with_border_size, logo_with_border_size), "white")
            logo_with_border.paste(logo, (border_size, border_size), logo)
        else:
            print("\nWarning: Logo file not found. Continuing without a logo.")
            use_logo = False
    else:
        logo_with_border = None

# Read CSV file
try:
    df = pd.read_csv(csv_filename, header=None)
except Exception as e:
    print(f"Error reading CSV file: {e}")
    exit()

total_qr = len(df)

# Function to update progress bar dynamically
def update_progress(current, total):
    terminal_width = shutil.get_terminal_size((80, 20)).columns  # Get terminal width
    bar_length = max(20, terminal_width - 30)  # Adjust bar size
    progress = int((current / total) * bar_length)
    bar = "█" * progress + "-" * (bar_length - progress)
    sys.stdout.write(f"\rGenerating QR Codes: [{bar}] {current}/{total}")
    sys.stdout.flush()

# Start time tracking
start_time = time.time()

# Generate QR codes
for index, row in df.iterrows():
    data = str(row[0]).strip()
    if data:
        svg_filename = os.path.join(svg_dir, f"qr_{index+1}.svg")
        pdf_filename = os.path.join(pdf_dir, f"qr_{index+1}.pdf")

        # --- Generate QR Code ---
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4
        )
        qr.add_data(data)
        qr.make(fit=True)

        # Generate SVG QR code
        qr_svg = qr.make_image(image_factory=qrcode.image.svg.SvgImage)
        qr_svg.save(svg_filename)

        # Convert SVG to PDF
        cairosvg.svg2pdf(url=svg_filename, write_to=pdf_filename)

        # --- Generate PNG (if enabled) ---
        if generate_png:
            png_filename = os.path.join(png_dir, f"qr_{index+1}.png")

            # Create a white background image
            img = Image.new("RGB", (png_size, png_size), "white")

            # Generate high-res QR code
            qr_png = qr.make_image(fill_color="black", back_color="white").convert("RGB")
            qr_png = qr_png.resize((qr_size_png, qr_size_png), Image.Resampling.LANCZOS)

            # Paste QR code onto the white background
            img.paste(qr_png, (margin_png, margin_png))

            # Overlay logo with contour (if selected)
            if use_logo and logo_with_border:
                logo_position = ((png_size - logo_with_border_size) // 2, (png_size - logo_with_border_size) // 2)
                img.paste(logo_with_border, logo_position, logo_with_border)

            # Save PNG
            img.save(png_filename)

        # Update progress bar
        update_progress(index + 1, total_qr)

# Finish time tracking
end_time = time.time()
total_time = end_time - start_time
average_time = total_time / total_qr if total_qr > 0 else 0

# Finish progress bar
print(f"\nQR code generation completed in {total_time:.2f} seconds.")
print(f"Average time per QR code: {average_time:.2f} seconds.")
