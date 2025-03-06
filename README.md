# QR Code Generator  

A command-line tool to generate QR codes from a CSV file in **SVG, PDF, and PNG** formats. Now includes **animated QR codes in the terminal!**  

## ðŸš€ Features  
- âœ… **Generate QR codes** from a CSV file  
- âœ… **Supports SVG, PDF, and PNG** formats  
- âœ… **Always generates SVG first, then converts to other formats**  
- âœ… **Automatically deletes SVG files if they are not chosen as output**  
- âœ… **Animated 10x10 QR code in the terminal** when `-ani` is used  
- âœ… **Cycles one QR code at a time** with a **0.3s delay**  
- âœ… **Optional logo support**  
- âœ… **Sets error correction to low if no logo is used for better scanning**  
- âœ… **Custom QR size and margin**  
- âœ… **Dynamically sized progress bar that follows terminal width**  
- âœ… **Performance tracking: total time taken & average time per QR code**  

## ðŸ“¥ Installation  

Ensure you have Python installed along with the required dependencies:  

```bash
pip install qrcode[pil] pandas cairosvg pillow
```

## ðŸ›  Usage  

```bash
python script.py [-i data.csv] [-o svg,pdf,png] [-size 500] [-m 20] [-logo logo.png] [-ani]
```

### ðŸ’¡ Arguments  

| Argument   | Description | Default |
|------------|------------|---------|
| `-i`      | CSV file with QR data | `data.csv` |
| `-o`      | Output formats: `svg`, `pdf`, `png` (comma-separated) | `svg,pdf,png` |
| `-size`   | QR code size in pixels | `500` |
| `-m`      | Margin size around QR code | `20` |
| `-logo`   | Path to logo file (optional) | None |
| `-ani`    | Show **10x10 animated QR codes in terminal**, cycling **one at a time with a 0.3s delay** | Off |

## ðŸŽ¬ Example Commands  

### Generate all formats (SVG, PDF, PNG) from `data.csv`  
```bash
python script.py
```

### Generate only PDF and PNG (skip SVG output)  
```bash
python script.py -o pdf,png
```

### Use a logo in the QR code  
```bash
python script.py -logo logo.png
```

### Set custom QR code size and margin  
```bash
python script.py -size 300 -m 10
```

### Show animated QR codes in terminal while processing  
```bash
python script.py -ani
```

## ðŸŽ¥ Animated Terminal QR Code  
When using the `-ani` flag, the script will display a **10x10 animated QR code** in the terminal, cycling **one at a time** with a **0.3s delay**. The animation disappears once the process completes.  

## ðŸ“Š Performance Tracking  
At the end of the process, the script will display:  
- âœ… **Total time taken**  
- âœ… **Average time per QR code**  

## ðŸ“ How It Works  
1. The script reads **each line** of the CSV file and generates a **QR code**.  
2. It **always generates SVG first**, then converts to other formats if needed.  
3. If SVG is not chosen as an output format, **it gets deleted** after processing.  
4. The **progress bar dynamically adjusts** based on terminal width.  
5. If `-ani` is used, a **10x10 animated QR code** cycles in the terminal during processing.  
6. After completion, it displays **total time used and average time per QR code**.  