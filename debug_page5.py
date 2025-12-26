import pdfplumber

pdf = pdfplumber.open('temp.pdf')

# Página 5
print("=" * 80)
print("PÁGINA 5")
print("=" * 80)
text = pdf.pages[4].extract_text()
lines = text.split('\n')
for i, line in enumerate(lines):
    if "reserva" in line.lower() or "oro" in line.lower() or "divisa" in line.lower():
        print(f"{i:3d}: {line}")

# También imprimir todo para ver estructura
print("\n\nPRIMERAS 50 LÍNEAS:")
for i, line in enumerate(lines[:50]):
    print(f"{i:3d}: {line}")
