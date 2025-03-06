# BulkQRGen

A QR Code Generator with SVG, PDF, and PNG Support based in Python

This script generates **QR codes** from a CSV file, supports **SVG, PDF, and PNG formats**, and includes optional **logo embedding**. It features a **progress bar that dynamically adjusts to your terminal width** and tracks the **total & average processing time**.

## 📌 Features  
✔️ **Generates QR codes from a CSV file**  
✔️ **Supports SVG, PDF, and (optional) PNG output**  
✔️ **Optional logo overlay on PNGs**  
✔️ **High-resolution PNG output (2048x2048 px)**  
✔️ **Dynamically adjusting progress bar**  
✔️ **Time tracking for total and per QR code processing**  

## 📂 CSV File Format
The script reads a CSV file (data.csv) where each row contains a single value (the QR code content).
Example:
```csv
https://example.com
Hello, World!
1234567890
```

## 🛠️ Requirements  
Ensure you have the required dependencies installed:  

```sh
pip install qrcode[pil] pandas cairosvg pillow
```
## 🚀 How to Use
Run the script and follow the prompts:

```sh
python bulkqrgen.py
```

## 🖼️ Logo Support (PNG Only)
Logos are centered on PNG QR codes if enabled.
A white contour (border) is automatically added around the logo.
Ensure logo.png is in the script folder before running.

