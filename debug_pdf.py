import pdfplumber

# Debug script para ver estructura del PDF
pdf_path = "temp.pdf"

with pdfplumber.open(pdf_path) as pdf:
    print(f"Total páginas: {len(pdf.pages)}\n")
    
    # Página 4 (índice 3)
    print("=" * 80)
    print("PÁGINA 4 - TASAS Y TIPOS DE CAMBIO")
    print("=" * 80)
    page = pdf.pages[3]
    
    print("\n--- TEXTO COMPLETO ---")
    text = page.extract_text()
    lines = text.split('\n')
    for i, line in enumerate(lines[:30]):  # Primeras 30 líneas
        print(f"{i:3d}: {line}")
    
    print("\n--- TABLAS EXTRAÍDAS ---")
    tables = page.extract_tables()
    for i, table in enumerate(tables):
        print(f"\nTabla {i} ({len(table)} filas):")
        for j, row in enumerate(table[:10]):  # Primeras 10 filas
            print(f"  Fila {j}: {row}")
