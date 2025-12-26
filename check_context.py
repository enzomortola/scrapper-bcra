import pdfplumber

pdf = pdfplumber.open('temp.pdf')

page4 = pdf.pages[3]
text = page4.extract_text()
lines = text.split('\n')

print("Líneas 50-70 de página 4:\n")
for i in range(50, min(70, len(lines))):
    print(f"{i:3d}: {lines[i]}")
