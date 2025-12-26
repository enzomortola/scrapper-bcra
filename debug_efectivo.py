import pdfplumber

pdf = pdfplumber.open('temp.pdf')
page4_text = pdf.pages[3].extract_text()

# Buscar el patrón exacto
lines = page4_text.split('\n')
for i, line in enumerate(lines):
    if 'Efectivo en ent. financieras en moneda extranjera' in line:
        print(f"Línea {i}: {line}")
        print(f"Siguiente: {lines[i+1] if i+1 < len(lines) else 'N/A'}")
