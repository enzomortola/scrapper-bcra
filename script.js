const JSON_URL = './bcra_data.json';

// Función para formatear números
function formatNumber(num) {
    if (num === null || num === undefined) return '-';
    return new Intl.NumberFormat('es-AR', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    }).format(num);
}

// Función para formatear fecha
function formatDate(isoDate) {
    const date = new Date(isoDate);
    return new Intl.DateTimeFormat('es-AR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    }).format(date);
}

// Función para formatear variaciones
function formatVariation(value) {
    if (value === null || value === undefined) return '-';
    const formatted = formatNumber(value);
    const className = value >= 0 ? 'var-positive' : 'var-negative';
    const sign = value >= 0 ? '+' : '';
    return `<span class="${className}">${sign}${formatted}%</span>`;
}

// Cargar y renderizar datos
async function loadData() {
    try {
        const response = await fetch(JSON_URL);
        const data = await response.json();

        // Actualizar fecha
        const fechaDisplay = data.fecha_informe || formatDate(data.fecha_actualizacion);
        document.getElementById('lastUpdate').textContent = fechaDisplay;

        // Reservas Internacionales
        const reservasUSD = data.reservas["Total en USD (millones)"];
        const efectivoEnt = data.reservas["Efectivo en entidades (millones USD)"];
        document.getElementById('reservasUSD').textContent = reservasUSD ? formatNumber(reservasUSD) : '-';
        document.getElementById('efectivoEnt').textContent = efectivoEnt ? formatNumber(efectivoEnt) : '-';

        // Tipos de cambio
        const dolarOficial = data.tipos_cambio["Dólar Oficial (Com. A 3500)"];
        const dolarMinorista = data.tipos_cambio["Dólar Minorista (Com. B 9791)"];
        document.getElementById('dolarOficial').textContent = formatNumber(dolarOficial);
        document.getElementById('dolarMinorista').textContent = formatNumber(dolarMinorista);

        // Índices
        document.getElementById('cer').textContent = formatNumber(data.indices.CER);
        document.getElementById('uva').textContent = formatNumber(data.indices.UVA);
        document.getElementById('icl').textContent = formatNumber(data.indices.ICL);

        // Tasas de interés
        renderTasas(data.tasas_interes);

    } catch (error) {
        console.error('Error cargando datos:', error);
        showError();
    }
}

// Renderizar tasas de interés
function renderTasas(tasas) {
    const container = document.getElementById('tasasContainer');
    container.innerHTML = '';

    for (const [label, value] of Object.entries(tasas)) {
        const card = document.createElement('div');
        card.className = 'rate-card';
        card.innerHTML = `
            <div class="rate-label">${label}</div>
            <div class="rate-value">${formatNumber(value)}%</div>
        `;
        container.appendChild(card);
    }
}

// Mostrar error
function showError() {
    document.body.innerHTML = `
        <div class="container">
            <div class="error-message" style="text-align: center; padding: 4rem;">
                <h1 style="font-size: 3rem; margin-bottom: 1rem;">⚠️</h1>
                <h2>Error al cargar los datos</h2>
                <p style="color: var(--text-secondary); margin-top: 1rem;">
                    No se pudieron cargar los datos del BCRA. Por favor, intenta nuevamente más tarde.
                </p>
                <button onclick="location.reload()" style="
                    margin-top: 2rem;
                    padding: 1rem 2rem;
                    background: var(--primary);
                    border: none;
                    border-radius: 12px;
                    color: white;
                    font-size: 1rem;
                    cursor: pointer;
                    transition: all 0.3s ease;
                ">Reintentar</button>
            </div>
        </div>
    `;
}

// Cargar datos al iniciar
loadData();

// Recargar cada 5 minutos
setInterval(loadData, 300000);
