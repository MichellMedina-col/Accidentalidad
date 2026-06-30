// app.js - Frontend logic for VialAnalytics

// URL of the backend API (adjust if you run on a different host/port)
const API_BASE = "http://127.0.0.1:8000";

// Elements
const kpiIncidentes = document.getElementById("kpi_incidentes");
const kpiEdad = document.getElementById("kpi_edad");
const kpiMun = document.getElementById("kpi_mun");
const kpiActor = document.getElementById("kpi_actor");

const edadInput = document.getElementById("edad");
const edadVal = document.getElementById("edad-val");
const municipioSel = document.getElementById("municipio");
const zonaSel = document.getElementById("zona");
const generoSel = document.getElementById("genero");
const actorSel = document.getElementById("actor");

const gaugeBar = document.getElementById("gauge-bar");
const gaugeValue = document.getElementById("riesgo_val");
const statusLabel = document.getElementById("status-label");
const pin = document.getElementById("pin");

// Helper: fetch global stats and populate KPI cards
async function loadStats() {
    try {
        const res = await fetch(`${API_BASE}/api/stats`);
        if (!res.ok) throw new Error("Failed to fetch stats");
        const data = await res.json();
        kpiIncidentes.textContent = data.kpi_incidentes;
        kpiEdad.textContent = data.kpi_edad;
        kpiMun.textContent = data.kpi_mun;
        kpiActor.textContent = data.kpi_actor;
    } catch (e) {
        console.error(e);
    }
}

// Helper: send prediction request
async function predict() {
    const payload = {
        edad: Number(edadInput.value),
        municipio: municipioSel.value,
        zona: zonaSel.value,
        genero: generoSel.value,
        actor: actorSel.value
    };
    try {
        const res = await fetch(`${API_BASE}/api/predict`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        if (!res.ok) throw new Error("Prediction failed");
        const data = await res.json();
        updateGauge(data.riesgo_pct, data.color);
        statusLabel.textContent = data.label;
    } catch (e) {
        console.error(e);
        statusLabel.textContent = "ERROR";
    }
}

// Update gauge visual
function updateGauge(percent, color) {
    const radius = 80; // matches SVG circle radius
    const circumference = 2 * Math.PI * radius; // ~502.65
    const dash = (percent / 100) * circumference;
    gaugeBar.setAttribute("stroke-dasharray", `${dash} ${circumference}`);
    gaugeBar.style.stroke = color;
    gaugeValue.textContent = `${percent}%`;
    // glow effect for pin
    pin.style.color = color;
    pin.style.filter = `drop-shadow(0 0 6px ${color})`;
    // also adjust status label colour for dark mode consistency
    statusLabel.style.color = color;
}

// Event listeners – any change triggers a new prediction
function attachListeners() {
    edadInput.addEventListener("input", () => {
        edadVal.textContent = edadInput.value;
        predict();
    });
    [municipioSel, zonaSel, generoSel, actorSel].forEach(el => {
        el.addEventListener("change", predict);
    });
}

// Initialise page
function init() {
    loadStats();
    attachListeners();
    // Initial prediction with default values
    predict();
}

window.addEventListener("DOMContentLoaded", init);
