# 📊 BCRA Scraper - Monitor Monetario Automático

Scraper automático del **Informe Monetario Diario del BCRA** con actualización vía GitHub Actions.

## 🎯 Funcionalidades

- ✅ Scraping diario automático del PDF del BCRA
- ✅ Extracción de tasas, tipos de cambio, índices, préstamos y depósitos
- ✅ Ejecución automatizada con GitHub Actions
- ✅ Dashboard web interactivo y responsive
- ✅ Datos servidos vía JSON estático (sin backend)

## 🚀 Setup

### 1. Instalar dependencias localmente

```bash
pip install -r requirements.txt
```

### 2. Ejecutar manualmente

```bash
python scrape_bcra.py
```

Esto genera `bcra_data.json` con todos los datos extraídos.

### 3. Configurar GitHub Actions

1. Sube el repo a GitHub
2. El workflow en `.github/workflows/scrape.yml` se ejecutará:
   - **Automáticamente**: Lunes a viernes a las 11 AM (Argentina)
   - **Manualmente**: Desde la pestaña "Actions" → "Run workflow"

### 4. Configurar el sitio web

1. Edita `script.js` líneas 3-4:
   ```javascript
   const REPO_USER = 'tu-usuario-github';
   const REPO_NAME = 'nombre-de-tu-repo';
   ```

2. Sube los archivos HTML/CSS/JS a tu hosting (Filezilla/Netlify/Vercel)

## 📁 Estructura

```
.
├── scrape_bcra.py          # Script de scraping
├── bcra_data.json          # Datos generados (auto-actualizado)
├── index.html              # Dashboard web
├── styles.css              # Estilos premium
├── script.js               # Lógica del frontend
├── requirements.txt        # Dependencias Python
└── .github/
    └── workflows/
        └── scrape.yml      # Automatización GitHub Actions
```

## 🌐 Deploy

**Opción 1: GitHub Pages**
- Settings → Pages → Source: main branch
- URL: `https://tu-usuario.github.io/tu-repo/`

**Opción 2: Netlify/Vercel**
- Conecta el repo y despliega automáticamente

**Opción 3: FTP (Filezilla)**
- Sube `index.html`, `styles.css`, `script.js` manualmente
- El JSON se actualiza solo en GitHub

## 📊 Datos Extraídos

- **Tipos de cambio**: Oficial y Minorista
- **Tasas de interés**: Call, Plazo Fijo, BADLAR, TM20
- **Índices**: CER, UVA, ICL
- **Préstamos**: Desglose por tipo al sector privado
- **Depósitos**: Cuenta corriente, caja de ahorro, plazo fijo
- **Reservas**: Internacionales y pasivos del BCRA

## 🔧 Personalización

- **Horario de ejecución**: Modifica `cron` en `scrape.yml`
- **Estilos**: Edita colores en `:root` de `styles.css`
- **Layout**: Ajusta estructura en `index.html`

## 📝 Notas

- El PDF se actualiza diariamente entre las 10-11 AM Argentina
- GitHub Actions tiene límite de 2000 min/mes (gratis)
- Cada ejecución toma ~30 segundos

## 🤝 Contribuciones

Pull requests y sugerencias bienvenidas!
