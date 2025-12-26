import pdfplumber

pdf = pdfplumber.open('temp.pdf')

# Página 6 - Reservas
print("=" * 80)
print("PÁGINA 6 - RESERVAS")
print("=" * 80)
text = pdf.pages[5].extract_text()
lines = text.split('\n')
for i, line in enumerate(lines[:40]):
    print(f"{i:3d}: {line}")
