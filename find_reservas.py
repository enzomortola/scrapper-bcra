import pdfplumber

pdf = pdfplumber.open('temp.pdf')

print("Buscando RESERVAS en todas las páginas:\n")
for i, page in enumerate(pdf.pages):
    text = page.extract_text()
    lines = text.split('\n')
    for j, line in enumerate(lines):
        if 'reserva' in line.lower() and ('42' in line or '40' in line or '43' in line):
            print(f"Página {i+1}, línea {j}: {line}")
