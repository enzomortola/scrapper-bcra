import pdfplumber
import requests
import json
import re
from datetime import datetime

PDF_URL = "https://www.bcra.gob.ar/archivos/Pdfs/PublicacionesEstadisticas/infomondiae.pdf"
OUTPUT_FILE = "bcra_data.json"

def download_pdf():
    """Descarga el PDF del BCRA"""
    response = requests.get(PDF_URL)
    with open("temp.pdf", "wb") as f:
        f.write(response.content)
    return "temp.pdf"

def clean_numeric(value):
    """Limpia y convierte valores numéricos, detecta formato automáticamente"""
    if not value or value == "-" or value == "":
        return None
    
    cleaned = str(value).strip()
    
    # Si tiene coma, es formato argentino: 1.450,42 -> remueve puntos y cambia coma por punto
    if "," in cleaned:
        cleaned = cleaned.replace(".", "").replace(",", ".")
    # sino, es formato internacional: 1450.42 -> mantener como está
    
    try:
        return float(cleaned)
    except:
        return None

def extract_data(pdf_path):
    """Extrae todos los datos del PDF"""
    data = {
        "fecha_actualizacion": datetime.now().isoformat(),
        "fecha_informe": None,
        "tasas_interes": {},
        "tipos_cambio": {},
        "indices": {},
        "reservas": {},
        "prestamos": [],
        "depositos": []
    }
    
    with pdfplumber.open(pdf_path) as pdf:
        # Extraer texto de la página 4 (índice 3)
        page4_text = pdf.pages[3].extract_text()
        
        # Fecha del informe (primera línea)
        date_match = re.search(r'(\d{1,2})\s+de\s+(\w+)\s+de\s+(\d{4})', page4_text)
        if date_match:
            data["fecha_informe"] = f"{date_match.group(1)} de {date_match.group(2)} de {date_match.group(3)}"
        
        # TIPOS DE CAMBIO
        # Patrón: "Tipo de cambio de referencia ($/USD Com. A 3500) VALOR1 VALOR2 VALOR3"
        tc_pattern = r'Tipo de cambio de referencia.*?3500\)\s+([\d.,]+)\s+([\d.,]+)\s+([\d.,]+)'
        tc_match = re.search(tc_pattern, page4_text)
        if tc_match:
            data["tipos_cambio"]["Dólar Oficial (Com. A 3500)"] = clean_numeric(tc_match.group(1))
        
        # Patrón: "Tipo de cambio minorista ($/USD Com. B 9791) VALOR1 VALOR2 VALOR3"
        tc_min_pattern = r'Tipo de cambio minorista.*?9791\)\s+([\d.,]+)\s+([\d.,]+)\s+([\d.,]+)'
        tc_min_match = re.search(tc_min_pattern, page4_text)
        if tc_min_match:
            data["tipos_cambio"]["Dólar Minorista (Com. B 9791)"] = clean_numeric(tc_min_match.group(1))
        
        # TASAS DE INTERÉS
        # Call en pesos - Patrón: "Call en pesos - Operaciones h/15 días VALOR1 VALOR2 VALOR3"
        call_pattern = r'Call en pesos\s+-\s+Operaciones h/15 días\s+([\d.,]+)\s+([\d.,]+)\s+([\d.,]+)'
        call_match = re.search(call_pattern, page4_text)
        if call_match:
            data["tasas_interes"]["Call en pesos (%)"] = clean_numeric(call_match.group(1))
        
        # BADLAR Total - Patrón: "BADLAR ... Total VALOR1 VALOR2 VALOR3"
        badlar_pattern = r'BADLAR.*?Total\s+([\d.,]+)\s+([\d.,]+)\s+([\d.,]+)'
        badlar_match = re.search(badlar_pattern, page4_text, re.DOTALL)
        if badlar_match:
            data["tasas_interes"]["BADLAR Total (%)"] = clean_numeric(badlar_match.group(1))
        
        # TM20 Total
        tm20_pattern = r'TM20.*?Total\s+([\d.,]+)\s+([\d.,]+)\s+([\d.,]+)'
        tm20_match = re.search(tm20_pattern, page4_text, re.DOTALL)
        if tm20_match:
            data["tasas_interes"]["TM20 Total (%)"] = clean_numeric(tm20_match.group(1))
        
        # Plazo Fijo 30 días en Pesos
        pf_pattern = r'Plazo Fijo 30 días.*?Pesos\s+([\d.,]+)\s+([\d.,]+)\s+([\d.,]+)'
        pf_match = re.search(pf_pattern, page4_text, re.DOTALL)
        if pf_match:
            data["tasas_interes"]["Plazo Fijo 30 días Pesos (%)"] = clean_numeric(pf_match.group(1))
        
        # ÍNDICES
        # CER - Patrón: "... (C.E.R.) ... Base 2.2.2002 = 1 VALOR1 VALOR2 VALOR3"
        cer_pattern = r'C\.E\.R\..*?Base\s+2\.2\.2002\s*=\s*1\s+([\d.,]+)\s+([\d.,]+)\s+([\d.,]+)'
        cer_match = re.search(cer_pattern, page4_text, re.DOTALL)
        if cer_match:
            data["indices"]["CER"] = clean_numeric(cer_match.group(1))
        
        # UVA - Patrón: "... (U.V.A.) ... Base 31.3.2016 = 14.05 VALOR1 VALOR2 VALOR3"
        uva_pattern = r'U\.V\.A\..*?Base\s+31\.3\.2016\s*=\s*[\d.,]+\s+([\d.,]+)\s+([\d.,]+)\s+([\d.,]+)'
        uva_match = re.search(uva_pattern, page4_text, re.DOTALL)
        if uva_match:
            data["indices"]["UVA"] = clean_numeric(uva_match.group(1))
        
        # ICL - Patrón: "... (I.C.L.) ... Base 30.6.2020 = 1 VALOR1 VALOR2 VALOR3"
        icl_pattern = r'I\.C\.L\..*?Base\s+30\.6\.2020\s*=\s*1\s+([\d.,]+)\s+([\d.,]+)\s+([\d.,]+)'
        icl_match = re.search(icl_pattern, page4_text, re.DOTALL)
        if icl_match:
            data["indices"]["ICL"] = clean_numeric(icl_match.group(1))
        
        # RESERVAS INTERNACIONALES
        # Patrón: "En dólares 5 42,326 40,622 32,255" (el 5 es una nota al pie)
        reservas_pattern = r'Reservas internacionales del BCRA.*?En dólares\s+\d+\s+([\d.,]+)'
        res_match = re.search(reservas_pattern, page4_text, re.DOTALL)
        if res_match:
            data["reservas"]["Total en USD (millones)"] = clean_numeric(res_match.group(1))
        
        # Efectivo en entidades financieras en moneda extranjera
        # Patrón: "Efectivo en ent. financieras en moneda extranjera 4 5 5,273 5,239..."
        # El valor que queremos es el tercero (5,273)
        efectivo_pattern = r'Efectivo en ent\. financieras en moneda extranjera\s+\d+\s+\d+\s+([\d.,]+)'
        efectivo_match = re.search(efectivo_pattern, page4_text)
        if efectivo_match:
            data["reservas"]["Efectivo en entidades (millones USD)"] = clean_numeric(efectivo_match.group(1))
        
        # Reservas en pesos
        reservas_pesos_pattern = r'Reservas internacionales del BCRA.*?En pesos\s+([\d.,]+)'
        res_pesos_match = re.search(reservas_pesos_pattern, page4_text, re.DOTALL)
        if res_pesos_match:
            data["reservas"]["Total en pesos (millones)"] = clean_numeric(res_pesos_match.group(1))
    
    return data

def main():
    print("📥 Descargando PDF del BCRA...")
    pdf_path = download_pdf()
    
    print("📊 Extrayendo datos...")
    data = extract_data(pdf_path)
    
    print("💾 Guardando datos en JSON...")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Datos guardados en {OUTPUT_FILE}")
    print(f"📈 Tasas: {len(data['tasas_interes'])}")
    print(f"💵 Tipos de cambio: {len(data['tipos_cambio'])}")
    print(f"📊 Índices: {len(data['indices'])}")
    print(f"🏦 Reservas: {len(data['reservas'])}")
    print(f"💰 Préstamos: {len(data['prestamos'])}")
    print(f"💳 Depósitos: {len(data['depositos'])}")

if __name__ == "__main__":
    main()
