import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go
import base64, os
from datetime import datetime

# ─── CONFIGURACIÓN ────────────────────────────────────────────
st.set_page_config(
    page_title="Seguridad Vial · Sabana Occidente",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── DETECCIÓN DE TEMA ────────────────────────────────────────
# Toggle manual de tema en session_state
if "tema_oscuro" not in st.session_state:
    st.session_state.tema_oscuro = False

IS_DARK = st.session_state.tema_oscuro

# ─── TOKENS DE DISEÑO (condicionales por tema) ────────────────
if IS_DARK:
    BG_BASE  = "#0B132B"
    BG_CARD  = "#1E293B"
    BG_CARD2 = "#0F172A"
    BORDER   = "#2D3748"
    ACCENT   = "#38BDF8"
    ACCENT2  = "#60A5FA"
    SUCCESS  = "#4ADE80"
    WARNING  = "#F59E0B"
    DANGER   = "#FF1744"
    TEXT_PRI = "#F8FAFC"
    TEXT_SEC = "#94A3B8"
    TEXT_MUT = "#64748B"
    CHART_BG = "#0F172A"
else:
    BG_BASE  = "#FFFFFF"
    BG_CARD  = "#F4F4F0"
    BG_CARD2 = "#E8E8E2"
    BORDER   = "#D1D5DB"
    ACCENT   = "#002855"
    ACCENT2  = "#4A703C"
    SUCCESS  = "#4A703C"
    WARNING  = "#DD6B20"
    DANGER   = "#E57373"
    TEXT_PRI = "#212529"
    TEXT_SEC = "#4A5568"
    TEXT_MUT = "#718096"
    CHART_BG = "#E8E8E2"

# ─── CSS PREMIUM ──────────────────────────────────────────────
# Lema: modo oscuro → gris claro/plata + itálica; modo claro → azul oscuro + normal
LEMA_COLOR = "#94A3B8" if IS_DARK else "#002855"
LEMA_STYLE = "italic" if IS_DARK else "normal"
# Hero overlay: gradiente adaptado al tema
HERO_OVERLAY = (
    "linear-gradient(90deg, rgba(11,19,43,0.95) 0%, rgba(11,19,43,0.7) 60%, rgba(11,19,43,0.2) 100%)"
    if IS_DARK else
    "linear-gradient(90deg, rgba(255,255,255,0.95) 0%, rgba(255,255,255,0.7) 60%, rgba(255,255,255,0.2) 100%)"
)
HERO_TITLE_COLOR = "#F8FAFC" if IS_DARK else "#002855"
HERO_BADGE_BG = "rgba(56,189,248,0.15)" if IS_DARK else "rgba(0,40,85,0.08)"
HERO_BADGE_BORDER = "rgba(56,189,248,0.3)" if IS_DARK else "rgba(0,40,85,0.2)"
SIDEBAR_BG = (
    "linear-gradient(180deg, #0d1526 0%, #0B1120 100%)"
    if IS_DARK else
    "linear-gradient(180deg, #F4F4F0 0%, #E8E8E2 100%)"
)
TITLE_SEC_COLOR = "#4ADE80" if IS_DARK else "#4A703C"

st.markdown(f"""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<style>
*, *::before, *::after {{ box-sizing: border-box; }}
html, body, .stApp, [data-testid="stAppViewContainer"] {{
    background-color: {BG_BASE} !important;
    font-family: 'Inter', sans-serif !important;
    color: {TEXT_PRI};
}}
[data-testid="stSidebar"] {{
    background: {SIDEBAR_BG} !important;
    border-right: 1px solid {BORDER} !important;
    display: flex !important;
    flex-direction: column !important;
}}
[data-testid="stSidebar"] > div:first-child {{
    display: flex !important;
    flex-direction: column !important;
    height: 100vh !important;
}}
[data-testid="stSidebar"] * {{ color: {TEXT_PRI} !important; }}
[data-testid="stSidebarNav"] {{ display: none; }}
[data-testid="stToolbar"], header {{ visibility: hidden; }}
#MainMenu {{ visibility: hidden; }}
footer {{ display: none !important; }}
::-webkit-scrollbar {{ width: 6px; }}
::-webkit-scrollbar-track {{ background: {BG_BASE}; }}
::-webkit-scrollbar-thumb {{ background: {BORDER}; border-radius: 3px; }}

/* Inputs */
[data-baseweb="select"] > div {{
    background: {BG_CARD2} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 10px !important;
    color: {TEXT_PRI} !important;
}}
.stSelectbox label, .stSlider label {{
    color: {TEXT_SEC} !important;
    font-size: 12px !important;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}}

/* Botón */
.stButton > button {{
    background: linear-gradient(135deg, {ACCENT}, {ACCENT2}) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    padding: 0.6rem 1.5rem !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
    font-family: 'Inter', sans-serif !important;
}}
.stButton > button:hover {{
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 20px {"rgba(56,189,248,0.35)" if IS_DARK else "rgba(0,40,85,0.25)"} !important;
}}

/* Expander */
[data-testid="stExpander"] {{
    background: {BG_CARD} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 12px !important;
}}
hr {{ border-color: {BORDER} !important; }}

/* ── KPI Cards ── */
.kpi-card {{
    background: {BG_CARD};
    border: 1px solid {BORDER};
    border-radius: 16px;
    padding: 22px 24px;
    position: relative;
    overflow: hidden;
    transition: transform .2s ease, box-shadow .2s ease;
    height: 130px;
}}
.kpi-card:hover {{
    transform: translateY(-2px);
    box-shadow: 0 12px 32px {"rgba(0,0,0,.25)" if IS_DARK else "rgba(0,0,0,.08)"};
}}
.kpi-card::before {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, {ACCENT}, {ACCENT2});
    border-radius: 16px 16px 0 0;
}}
.kpi-label {{
    font-size: 10px;
    font-weight: 600;
    color: {TEXT_MUT};
    text-transform: uppercase;
    letter-spacing: .1em;
    margin-bottom: 8px;
}}
.kpi-value {{
    font-size: 1.8rem;
    font-weight: 700;
    color: {TEXT_PRI};
    line-height: 1;
    margin-bottom: 4px;
}}
.kpi-sub {{ font-size: 11px; color: {TEXT_SEC}; }}
.kpi-icon {{
    position: absolute;
    top: 18px; right: 18px;
    font-size: 26px; opacity: .2;
}}

/* ── Section title ── */
.sec-title {{
    font-size: 1.1rem;
    font-weight: 700;
    color: {TITLE_SEC_COLOR};
    margin-bottom: 2px;
}}
.sec-sub {{
    font-size: .8rem;
    color: {TEXT_SEC};
    margin-bottom: 16px;
}}

/* ── Hero banner ── */
.hero-banner {{
    border-radius: 20px;
    overflow: hidden;
    position: relative;
    margin-bottom: 28px;
    border: 1px solid {BORDER};
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    min-height: 300px;
    display: flex;
    align-items: center;
    transition: all 0.3s ease;
}}
.hero-banner.fallback {{
    background: {SIDEBAR_BG};
}}
.hero-overlay {{
    position: absolute; inset: 0;
    background: {HERO_OVERLAY};
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 40px 48px;
    transition: all 0.3s ease;
}}
.hero-badge {{
    display: inline-flex; align-items: center; gap: 8px;
    background: {HERO_BADGE_BG};
    border: 1px solid {HERO_BADGE_BORDER};
    border-radius: 100px;
    padding: 6px 16px;
    font-size: 12px; font-weight: 600;
    color: {ACCENT};
    margin-bottom: 16px;
    width: fit-content;
}}
.hero-title {{
    font-size: 1.8rem;
    font-weight: 800;
    color: {HERO_TITLE_COLOR};
    line-height: 1.25;
    margin-bottom: 12px;
    max-width: 85%;
}}
.hero-sub.lema {{
    font-size: 1.05rem;
    font-weight: 500;
    color: {LEMA_COLOR};
    font-style: {LEMA_STYLE};
}}

/* ── Chart card ── */
.chart-card {{
    background: {BG_CARD};
    border: 1px solid {BORDER};
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 20px;
}}

/* ── Nav items ── */
.nav-item {{
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 14px;
    border-radius: 10px;
    font-size: 14px;
    font-weight: 500;
    color: {TEXT_SEC};
    cursor: pointer;
    margin-bottom: 4px;
}}
.nav-item.active {{
    background: {"rgba(56,189,248,.15)" if IS_DARK else "rgba(0,40,85,.10)"};
    color: {ACCENT};
    border: 1px solid {"rgba(56,189,248,.2)" if IS_DARK else "rgba(0,40,85,.15)"};
}}
.divider-label {{
    font-size: 10px;
    font-weight: 600;
    color: {TEXT_MUT};
    text-transform: uppercase;
    letter-spacing: .12em;
    padding: 14px 14px 6px;
}}

/* ── Result Card mejorada ── */
.result-card {{
    background: {BG_CARD};
    border: 1px solid {BORDER};
    border-radius: 16px;
    padding: 24px;
    text-align: center;
    min-height: 420px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    transition: all 0.3s ease;
}}
.result-title {{
    font-size: 12px;
    font-weight: 600;
    color: {TEXT_MUT};
    text-transform: uppercase;
    letter-spacing: .08em;
    margin-bottom: 20px;
}}
.circular-progress {{
    position: relative;
    width: 150px;
    height: 150px;
    margin-bottom: 16px;
}}
.progress-svg {{
    transform: rotate(-90deg);
    width: 100%;
    height: 100%;
}}
.progress-svg circle {{
    fill: none;
    stroke-width: 8;
}}
.progress-svg circle.bg {{
    stroke: {BORDER};
    opacity: 0.3;
}}
.progress-svg circle.meter {{
    stroke: currentColor;
    stroke-linecap: round;
    transition: stroke-dashoffset 0.8s ease-in-out;
}}
.circular-progress.riesgo-bajo {{
    color: {SUCCESS};
}}
.circular-progress.riesgo-medio {{
    color: {WARNING};
}}
.circular-progress.riesgo-alto {{
    color: {DANGER};
}}
.circular-progress .value {{
    position: absolute;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2.2rem;
    font-weight: 800;
    color: {TEXT_PRI};
}}
.result-badge {{
    background: {BG_CARD2};
    border-radius: 100px;
    padding: 6px 20px;
    font-size: 0.95rem;
    font-weight: 700;
    margin: 12px 0;
    display: inline-flex;
    align-items: center;
    gap: 8px;
    border: 1px solid transparent;
}}
.result-badge.riesgo-bajo {{
    color: {SUCCESS};
    border-color: {SUCCESS};
    background: {"rgba(74,222,128,0.08)" if IS_DARK else "rgba(74,112,60,0.08)"};
}}
.result-badge.riesgo-medio {{
    color: {WARNING};
    border-color: {WARNING};
    background: {"rgba(245,158,11,0.08)" if IS_DARK else "rgba(221,107,32,0.08)"};
}}
.result-badge.riesgo-alto {{
    color: {DANGER};
    border-color: {DANGER};
    background: {"rgba(255,23,68,0.08)" if IS_DARK else "rgba(229,115,115,0.08)"};
}}
.result-details {{
    display: flex;
    justify-content: center;
    gap: 12px;
    margin-top: 16px;
    flex-wrap: wrap;
    width: 100%;
}}
.detail-item {{
    background: {BG_CARD2};
    border-radius: 8px;
    padding: 8px 14px;
    flex: 1;
    min-width: 80px;
    border: 1px solid {BORDER};
}}
.detail-label {{
    font-size: 9px;
    color: {TEXT_MUT};
    text-transform: uppercase;
    display: block;
    margin-bottom: 2px;
    letter-spacing: 0.05em;
}}
.detail-val {{
    font-size: 13px;
    font-weight: 600;
    color: {TEXT_PRI};
}}

/* ── Sidebar Estilos Adicionales ── */
/* Ocultar el label del radio */
[data-testid="stSidebar"] .stRadio > label {{
    display: none !important;
}}
/* Estilo de los radio buttons como nav items */
[data-testid="stSidebar"] .stRadio > div {{
    gap: 4px !important;
}}
[data-testid="stSidebar"] .stRadio > div > label {{
    background: transparent !important;
    border: 1px solid transparent !important;
    border-radius: 10px !important;
    padding: 10px 14px !important;
    margin: 0 !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    color: {TEXT_SEC} !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
}}
[data-testid="stSidebar"] .stRadio > div > label:hover {{
    background: {"rgba(56,189,248,.08)" if IS_DARK else "rgba(0,40,85,.06)"} !important;
    color: {TEXT_PRI} !important;
}}
[data-testid="stSidebar"] .stRadio > div > label[data-checked="true"],
[data-testid="stSidebar"] .stRadio > div > label:has(input:checked) {{
    background: {"rgba(56,189,248,.15)" if IS_DARK else "rgba(0,40,85,.10)"} !important;
    color: {ACCENT} !important;
    border: 1px solid {BORDER} !important;
}}
/* Ocultar el circulito del radio */
[data-testid="stSidebar"] .stRadio > div > label > div:first-child {{
    display: none !important;
}}
/* Footer del sidebar */
.sidebar-footer {{
    margin-top: auto !important;
    padding: 20px 14px 24px !important;
}}
.sidebar-footer-box {{
    border: 1px solid {BORDER};
    border-radius: 12px;
    padding: 14px 18px;
    text-align: center;
}}
.sidebar-footer-label {{
    font-size: 10px;
    font-weight: 600;
    color: {TEXT_MUT};
    text-transform: uppercase;
    letter-spacing: .1em;
}}
.sidebar-footer-year {{
    font-size: 18px;
    font-weight: 700;
    color: {ACCENT};
    margin-top: 2px;
}}

/* ── Toggle de tema ── */
.theme-toggle-container {{
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 14px;
    margin-bottom: 8px;
}}
.theme-toggle-label {{
    font-size: 12px;
    font-weight: 500;
    color: {TEXT_SEC};
}}

/* ── Estilos responsivos ── */
@media (max-width: 768px) {{
    .hero-banner {{
        min-height: 220px !important;
        margin-bottom: 20px !important;
    }}
    .hero-overlay {{
        padding: 24px 28px !important;
    }}
    .hero-title {{
        font-size: 1.3rem !important;
        max-width: 100% !important;
    }}
    .hero-sub.lema {{
        font-size: 0.9rem !important;
    }}
    .kpi-card {{
        height: auto !important;
        padding: 16px 20px !important;
    }}
    .kpi-value {{
        font-size: 1.5rem !important;
    }}
    .result-card {{
        min-height: auto !important;
        padding: 16px !important;
    }}
    .circular-progress {{
        width: 120px !important;
        height: 120px !important;
    }}
    .circular-progress .value {{
        font-size: 1.8rem !important;
    }}
    .sec-title {{
        font-size: 1rem !important;
    }}
    .detail-item {{
        min-width: 60px !important;
        padding: 6px 10px !important;
    }}
    .detail-val {{
        font-size: 11px !important;
    }}
}}

/* ── Tablet breakpoint ── */
@media (min-width: 769px) and (max-width: 1024px) {{
    .hero-title {{
        font-size: 1.5rem !important;
    }}
    .kpi-card {{
        padding: 18px 20px !important;
        height: auto !important;
    }}
    .kpi-value {{
        font-size: 1.6rem !important;
    }}
}}

/* ── Footer global ── */
.app-footer {{
    border-top: 1px solid {BORDER};
    padding: 18px 0;
    text-align: center;
}}
.app-footer span {{
    color: {TEXT_MUT};
    font-size: 12px;
}}
</style>
""", unsafe_allow_html=True)


# ─── UTILIDADES ───────────────────────────────────────────────
def find_col(df, *keywords):
    cols_lower = {c.lower(): c for c in df.columns}
    for kw in keywords:
        kw_l = kw.lower()
        if kw_l in cols_lower:
            return cols_lower[kw_l]
        for cl, cr in cols_lower.items():
            if kw_l in cl:
                return cr
    return None

def img_to_b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def dark_layout(fig, title_color=None):
    grid_color = "rgba(128, 128, 128, 0.18)"
    text_color = "rgba(128, 128, 128, 0.8)"
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color=text_color, size=11),
        margin=dict(l=10, r=10, t=20, b=10),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=text_color)),
        xaxis=dict(gridcolor=grid_color, linecolor=grid_color, tickfont=dict(color=text_color)),
        yaxis=dict(gridcolor=grid_color, linecolor=grid_color, tickfont=dict(color=text_color)),
    )
    return fig


# ─── CARGA DE DATOS ───────────────────────────────────────────
@st.cache_data
def load_clean_data():
    try:
        df = pd.read_csv('Archivo_Accidentes.csv', sep=None, engine='python')
        df.columns = (
            df.columns.str.strip().str.lower()
            .str.replace(r'[\s\-]+', '_', regex=True)
            .str.replace(r'[áàä]', 'a', regex=True)
            .str.replace(r'[éèë]', 'e', regex=True)
            .str.replace(r'[íìï]', 'i', regex=True)
            .str.replace(r'[óòö]', 'o', regex=True)
            .str.replace(r'[úùü]', 'u', regex=True)
            .str.replace(r'[ñ]', 'n', regex=True)
        )
        return df
    except Exception as e:
        st.error(f"⚠️ Error al cargar datos: {e}")
        return None

@st.cache_resource
def load_trained_model():
    try:
        return joblib.load('modelo_accidentes.pkl')
    except:
        return None

df_full = load_clean_data()
modelo  = load_trained_model()

if df_full is None:
    st.error("🚨 No se encontró 'Archivo_Accidentes.csv'.")
    st.stop()

# Detectar columnas
COL_EDAD   = find_col(df_full, 'edad', 'age')
COL_MUN    = find_col(df_full, 'municipio', 'ciudad', 'municipality')
COL_ZONA   = find_col(df_full, 'zona', 'zone', 'area')
COL_GENERO = find_col(df_full, 'genero', 'sexo', 'gender', 'sex')
COL_ACTOR  = find_col(df_full, 'actor_vial', 'actor', 'tipo_actor', 'clase_actor', 'victima', 'rol')
COL_GRAVE  = find_col(df_full, 'gravedad', 'severity', 'clase', 'tipo_accidente', 'clase_de_acc')
COL_FECHA  = find_col(df_full, 'fecha', 'date', 'año', 'anio', 'year', 'mes')


# ═══════════════════════════════════════════════════════════════
#  SIDEBAR — navegación (estilo panel de control limpio)
# ═══════════════════════════════════════════════════════════════

with st.sidebar:
    # ── Logo + Título ──
    st.markdown(f"""
    <div style="padding:20px 14px 16px;">
        <div style="display:flex; align-items:center; gap:10px; margin-bottom:6px;">
            <div style="width:38px;height:38px;border-radius:10px;
                        background:linear-gradient(135deg,{ACCENT},{ACCENT2});
                        display:flex;align-items:center;justify-content:center;font-size:18px;">
                🚦
            </div>
            <div>
                <div style="font-weight:700;font-size:15px;color:{TEXT_PRI};">VialAnalytics</div>
                <div style="font-size:11px;color:{TEXT_MUT};">Sabana Occidente</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Navegación (radio buttons estilizados) ──
    pagina = st.radio(
        "Navegación",
        ["🏠  Inicio · Predictor", "📊  Análisis Visual"],
        label_visibility="collapsed"
    )

    # ── Toggle de tema (Modo Claro / Modo Oscuro) ──
    st.markdown("---")
    tema_label = "🌙 Modo Oscuro" if not IS_DARK else "☀️ Modo Claro"
    if st.button(tema_label, key="theme_toggle", use_container_width=True):
        st.session_state.tema_oscuro = not st.session_state.tema_oscuro
        st.rerun()

    # ── Footer: PROYECTO SENA 2026 ──
    st.markdown(f"""
    <div class="sidebar-footer">
        <div class="sidebar-footer-box">
            <div class="sidebar-footer-label">Proyecto SENA</div>
            <div class="sidebar-footer-year">2026</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Filtros ahora en el área principal (ocultos en variables) ──
df = df_full.copy()
sel_mun = "Todos"
sel_gen = "Todos"


# ═══════════════════════════════════════════════════════════════
#  CALCULAR KPIs dinámicos
# ═══════════════════════════════════════════════════════════════
kpi_incidentes = f"{len(df):,}"
kpi_edad  = f"{df[COL_EDAD].mean():.1f}"  if COL_EDAD   else "N/D"
kpi_mun   = df[COL_MUN].mode()[0]               if COL_MUN    else "N/D"
kpi_actor = df[COL_ACTOR].mode()[0]             if COL_ACTOR  else "N/D"


# ════════════════════════════════════════════════════════════════
#  PÁGINA 1 — INICIO · PREDICTOR
# ════════════════════════════════════════════════════════════════
if "Inicio" in pagina:

    # ── HERO BANNER ──────────────────────────────────────────
    img_path = "imagen_principal.jpeg"
    if os.path.exists(img_path):
        b64 = img_to_b64(img_path)
        st.markdown(f"""
        <div class="hero-banner" style="background-image: url('data:image/jpeg;base64,{b64}');">
            <div class="hero-overlay">
                <div class="hero-badge">🚦 Proyecto SENA · 2026</div>
                <div class="hero-title">Análisis de la accidentalidad vial en los municipios de Facatativá, Funza, Madrid y Mosquera durante el periodo 2021–2026.</div>
                <div class="hero-sub lema">🛣️ "Conocer los riesgos hoy para prevenir los accidentes de mañana."</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="hero-banner fallback">
            <div class="hero-overlay">
                <div class="hero-badge">🚦 Proyecto SENA · 2026</div>
                <div class="hero-title">Análisis de la accidentalidad vial en los municipios de Facatativá, Funza, Madrid y Mosquera durante el periodo 2021–2026.</div>
                <div class="hero-sub lema">🛣️ "Conocer los riesgos hoy para prevenir los accidentes de mañana."</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── KPIs DINÁMICOS ───────────────────────────────────────
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">🚨</div>
            <div class="kpi-label">Incidentes filtrados</div>
            <div class="kpi-value">{kpi_incidentes}</div>
            <div class="kpi-sub">Todos los municipios · Todos los géneros</div>
        </div>""", unsafe_allow_html=True)
    with k2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">🎂</div>
            <div class="kpi-label">Edad media crítica</div>
            <div class="kpi-value">{kpi_edad} años</div>
            <div class="kpi-sub">Promedio de involucrados</div>
        </div>""", unsafe_allow_html=True)
    with k3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">📍</div>
            <div class="kpi-label">Mayor siniestralidad</div>
            <div class="kpi-value" style="font-size:1.5rem;">{kpi_mun}</div>
            <div class="kpi-sub">Municipio de mayor riesgo</div>
        </div>""", unsafe_allow_html=True)
    with k4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">🚶</div>
            <div class="kpi-label">Actor más vulnerable</div>
            <div class="kpi-value" style="font-size:1.35rem;">{kpi_actor}</div>
            <div class="kpi-sub">Tipo de actor vial</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── PREDICTOR DE RIESGO ──────────────────────────────────
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:20px;">
        <div style="width:4px;height:28px;background:linear-gradient(180deg,{ACCENT},{ACCENT2});border-radius:2px;"></div>
        <div>
            <div style="font-size:1.1rem;font-weight:700;color:{TITLE_SEC_COLOR};">Predictor de Escenario de Riesgo</div>
            <div style="font-size:.82rem;color:{TEXT_SEC};">Configura los parámetros del actor vial para obtener una predicción de riesgo</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    p1, p2 = st.columns([1, 1.1])

    with p1:
        st.markdown(f"""
        <div style="background:{BG_CARD};border:1px solid {BORDER};
                    border-radius:16px;padding:24px;">
            <div style="font-size:12px;font-weight:600;color:{TEXT_MUT};
                        text-transform:uppercase;letter-spacing:.08em;margin-bottom:20px;">
                ⚙️ Parámetros del escenario
            </div>
        """, unsafe_allow_html=True)

        edad = st.slider("Edad del actor vial", 0, 100, 30)
        mun_sel  = st.selectbox("Municipio", sorted(df_full[COL_MUN].dropna().unique()))   if COL_MUN    else None
        zon_sel  = st.selectbox("Zona del incidente", sorted(df_full[COL_ZONA].dropna().unique()))  if COL_ZONA   else None
        gen_sel  = st.selectbox("Género", sorted(df_full[COL_GENERO].dropna().unique()))   if COL_GENERO else None
        act_sel  = st.selectbox("Tipo de actor vial", sorted(df_full[COL_ACTOR].dropna().unique())) if COL_ACTOR  else None

        st.markdown("</div>", unsafe_allow_html=True)

    with p2:
        if modelo is not None:
            try:
                cols_mod = list(modelo.feature_names_in_)
                inp      = pd.DataFrame(0, index=[0], columns=cols_mod)

                for poss in ['edad', 'Edad', 'age']:
                    if poss in inp.columns:
                        inp.at[0, poss] = edad; break

                cands = []
                if mun_sel:  cands += [f'{COL_MUN}_{mun_sel}',    f'municipio_{mun_sel}']
                if zon_sel:  cands += [f'{COL_ZONA}_{zon_sel}',   f'zona_{zon_sel}']
                if gen_sel:  cands += [f'{COL_GENERO}_{gen_sel}', f'genero_{gen_sel}']
                if act_sel:  cands += [f'{COL_ACTOR}_{act_sel}',  f'actor_vial_{act_sel}']
                for v in cands:
                    if v in inp.columns: inp.at[0, v] = 1

                pred      = modelo.predict(inp)[0]
                probs     = modelo.predict_proba(inp)[0]
                conf      = max(probs)
                
                # Determinar nivel de riesgo (0-100)
                riesgo_pct = round(conf * 100, 1)
                
                # Determinar color, etiqueta y clase según el nivel
                if riesgo_pct < 50:
                    clase_riesgo = "riesgo-bajo"
                    label_riesgo = "RIESGO BAJO - CONTROLADO"
                    icon_riesgo = "🟢"
                elif riesgo_pct < 70:
                    clase_riesgo = "riesgo-medio"
                    label_riesgo = "RIESGO MEDIO - PRECAUCIÓN"
                    icon_riesgo = "🟡"
                else:
                    clase_riesgo = "riesgo-alto"
                    label_riesgo = "RIESGO ALTO - CRÍTICO"
                    icon_riesgo = "🔴"

                dash_offset = round(251.2 - (251.2 * riesgo_pct / 100), 2)

                # Mostrar resultado estilo donas circular SVG
                st.markdown(f"""
                <div class="result-card">
                    <div class="result-title">🔮 Resultado del análisis</div>
                    <div class="circular-progress {clase_riesgo}">
                        <svg viewBox="0 0 100 100" class="progress-svg">
                            <circle class="bg" cx="50" cy="50" r="40"></circle>
                            <circle class="meter" cx="50" cy="50" r="40" style="stroke-dasharray: 251.2; stroke-dashoffset: {dash_offset};"></circle>
                        </svg>
                        <div class="value">{riesgo_pct}%</div>
                    </div>
                    <div style="font-size:0.9rem;font-weight:600;color:var(--text-sec);margin-top:4px;">
                        Índice de riesgo estimado
                    </div>
                    <div class="result-badge {clase_riesgo}">
                        {icon_riesgo} {label_riesgo}
                    </div>
                    <div class="result-details">
                        <div class="detail-item">
                            <span class="detail-label">Actor Vial</span>
                            <span class="detail-val">{act_sel if act_sel else 'N/D'}</span>
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">Municipio</span>
                            <span class="detail-val">{mun_sel if mun_sel else 'N/D'}</span>
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">Confianza</span>
                            <span class="detail-val">{conf:.1%}</span>
                        </div>
                    </div>
                    <div style="margin-top:16px;font-size:11px;color:{TEXT_MUT};">
                        Proyecto SENA · 2026
                    </div>
                </div>
                """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Error en predicción: {e}")
        else:
            st.markdown(f"""
            <div style="background:{BG_CARD};border:1px solid {BORDER};
                        border-radius:16px;padding:24px;min-height:420px;text-align:center;">
                <div style="font-size:12px;font-weight:600;color:{TEXT_MUT};
                            text-transform:uppercase;letter-spacing:.08em;margin-bottom:16px;">
                    🔮 Resultado del análisis
                </div>
                <div style="padding:48px 20px;">
                    <div style="font-size:40px;margin-bottom:12px;">📦</div>
                    <div style="color:{TEXT_SEC};font-size:14px;">
                        Modelo no disponible.<br>
                        Sube <code>modelo_accidentes.pkl</code> al repositorio.
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════
#  PÁGINA 2 — ANÁLISIS VISUAL
# ════════════════════════════════════════════════════════════════
else:

    # Encabezado de sección
    st.markdown(f"""
    <div style="padding:8px 0 24px;">
        <h1 style="font-size:1.7rem;font-weight:700;color:{ACCENT};margin:0 0 4px;">
            📊 Análisis de Accidentalidad
        </h1>
        <p style="color:{TEXT_SEC};font-size:.9rem;margin:0;">
            Facatativá &nbsp;•&nbsp; Funza &nbsp;•&nbsp; Madrid &nbsp;•&nbsp; Mosquera
            &nbsp;·&nbsp; {len(df):,} registros filtrados
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── KPIs (resumen rápido) ─────────────────────────────────
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f"""<div class="kpi-card"><div class="kpi-icon">🚨</div>
            <div class="kpi-label">Incidentes</div>
            <div class="kpi-value">{kpi_incidentes}</div>
            <div class="kpi-sub" style="color:{SUCCESS};">● Dataset activo</div>
        </div>""", unsafe_allow_html=True)
    with k2:
        st.markdown(f"""<div class="kpi-card"><div class="kpi-icon">🎂</div>
            <div class="kpi-label">Edad media</div>
            <div class="kpi-value">{kpi_edad} años</div>
            <div class="kpi-sub">Promedio involucrados</div>
        </div>""", unsafe_allow_html=True)
    with k3:
        st.markdown(f"""<div class="kpi-card"><div class="kpi-icon">📍</div>
            <div class="kpi-label">Mayor riesgo</div>
            <div class="kpi-value" style="font-size:1.4rem;">{kpi_mun}</div>
            <div class="kpi-sub">Municipio</div>
        </div>""", unsafe_allow_html=True)
    with k4:
        st.markdown(f"""<div class="kpi-card"><div class="kpi-icon">🚶</div>
            <div class="kpi-label">Actor vulnerable</div>
            <div class="kpi-value" style="font-size:1.2rem;">{kpi_actor}</div>
            <div class="kpi-sub">Tipo actor vial</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── FILA 1: Municipio + Edad ──────────────────────────────
    c1, c2 = st.columns(2)

    with c1:
        st.markdown(f"""
        <div class="sec-title">🏙️ Siniestralidad por Municipio</div>
        <div class="sec-sub">Cantidad de incidentes registrados por localidad</div>
        """, unsafe_allow_html=True)
        if COL_MUN:
            vc = df[COL_MUN].value_counts().reset_index()
            vc.columns = ['Municipio', 'Incidentes']
            fig = go.Figure(go.Bar(
                x=vc['Municipio'], y=vc['Incidentes'],
                marker=dict(
                    color=vc['Incidentes'],
                    colorscale=[[0,CHART_BG],[.5,ACCENT],[1,ACCENT2]],
                    line=dict(width=0)
                ),
                hovertemplate="<b>%{x}</b><br>Incidentes: %{y:,}<extra></extra>"
            ))
            fig = dark_layout(fig)
            fig.update_layout(showlegend=False, height=320)
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    with c2:
        st.markdown(f"""
        <div class="sec-title">📉 Perfil de Edad de los Involucrados</div>
        <div class="sec-sub">Distribución etaria de los actores viales</div>
        """, unsafe_allow_html=True)
        if COL_EDAD:
            ev = df[COL_EDAD].dropna()
            counts, bins = np.histogram(ev, bins=25)
            centers = (bins[:-1] + bins[1:]) / 2
            fig2 = go.Figure()
            fig2.add_trace(go.Bar(
                x=centers, y=counts,
                marker=dict(color=ACCENT, opacity=.75, line=dict(width=0)),
                hovertemplate="Edad %{x:.0f}: %{y} casos<extra></extra>"
            ))
            fig2.add_trace(go.Scatter(
                x=centers, y=counts,
                fill='tozeroy', fillcolor="rgba(99,102,241,.18)",
                line=dict(color=ACCENT2, width=2), hoverinfo='skip'
            ))
            fig2 = dark_layout(fig2)
            fig2.update_layout(showlegend=False, height=320, barmode='overlay')
            st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})

    # ── FILA 2: Actor vial + Género ───────────────────────────
    c3, c4 = st.columns(2)

    with c3:
        st.markdown(f"""
        <div class="sec-title">🚗 Actores Viales más Frecuentes</div>
        <div class="sec-sub">Top 8 tipos de actor vial involucrado</div>
        """, unsafe_allow_html=True)
        if COL_ACTOR:
            vc_a = df[COL_ACTOR].value_counts().head(8).reset_index()
            vc_a.columns = ['Actor', 'Cantidad']
            fig3 = go.Figure(go.Bar(
                x=vc_a['Cantidad'], y=vc_a['Actor'],
                orientation='h',
                marker=dict(
                    color=vc_a['Cantidad'],
                    colorscale=[[0,CHART_BG],[1,SUCCESS]],
                    line=dict(width=0)
                ),
                hovertemplate="<b>%{y}</b>: %{x:,} casos<extra></extra>"
            ))
            fig3 = dark_layout(fig3)
            fig3.update_layout(showlegend=False, height=340,
                               yaxis=dict(autorange='reversed'))
            st.plotly_chart(fig3, use_container_width=True, config={'displayModeBar': False})

    with c4:
        st.markdown(f"""
        <div class="sec-title">⚧ Distribución por Género</div>
        <div class="sec-sub">Proporción de involucrados por género</div>
        """, unsafe_allow_html=True)
        if COL_GENERO:
            vc_g = df[COL_GENERO].value_counts().reset_index()
            vc_g.columns = ['Genero', 'Cantidad']
            fig4 = go.Figure(go.Pie(
                labels=vc_g['Genero'], values=vc_g['Cantidad'],
                hole=0.58,
                marker=dict(
                    colors=[ACCENT, ACCENT2, SUCCESS, WARNING, DANGER],
                    line=dict(color=BG_BASE, width=3)
                ),
                hovertemplate="<b>%{label}</b><br>%{value:,} casos (%{percent})<extra></extra>"
            ))
            fig4 = dark_layout(fig4)
            fig4.update_layout(showlegend=True, height=340)
            st.plotly_chart(fig4, use_container_width=True, config={'displayModeBar': False})

    # ── FILA 3: Zona + Gravedad ───────────────────────────────
    c5, c6 = st.columns(2)

    with c5:
        if COL_ZONA:
            st.markdown(f"""
            <div class="sec-title">📍 Incidentes por Zona</div>
            <div class="sec-sub">Clasificación urbana vs rural</div>
            """, unsafe_allow_html=True)
            vc_z = df[COL_ZONA].value_counts().reset_index()
            vc_z.columns = ['Zona', 'Cantidad']
            fig5 = go.Figure(go.Bar(
                x=vc_z['Zona'], y=vc_z['Cantidad'],
                marker=dict(color=WARNING, opacity=.85, line=dict(width=0)),
                hovertemplate="<b>%{x}</b>: %{y:,}<extra></extra>"
            ))
            fig5 = dark_layout(fig5, title_color=WARNING)
            fig5.update_layout(showlegend=False, height=300)
            st.plotly_chart(fig5, use_container_width=True, config={'displayModeBar': False})

    with c6:
        if COL_GRAVE:
            st.markdown(f"""
            <div class="sec-title">⚠️ Gravedad de los Accidentes</div>
            <div class="sec-sub">Distribución por nivel de gravedad</div>
            """, unsafe_allow_html=True)
            vc_gr = df[COL_GRAVE].value_counts().reset_index()
            vc_gr.columns = ['Gravedad', 'Cantidad']
            fig6 = go.Figure(go.Bar(
                x=vc_gr['Gravedad'], y=vc_gr['Cantidad'],
                marker=dict(
                    color=vc_gr['Cantidad'],
                    colorscale=[[0, WARNING],[1, DANGER]],
                    line=dict(width=0)
                ),
                hovertemplate="<b>%{x}</b>: %{y:,}<extra></extra>"
            ))
            fig6 = dark_layout(fig6, title_color=DANGER)
            fig6.update_layout(showlegend=False, height=300)
            st.plotly_chart(fig6, use_container_width=True, config={'displayModeBar': False})

    # ── FILA 4: Mapa de calor Municipio x Actor (si hay ambos) ─
    if COL_MUN and COL_ACTOR:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="sec-title">🗺️ Mapa de Calor: Municipio × Actor Vial</div>
        <div class="sec-sub">Concentración de incidentes por combinación de variables</div>
        """, unsafe_allow_html=True)

        pivot = (df.groupby([COL_MUN, COL_ACTOR])
                   .size().reset_index(name='n')
                   .pivot(index=COL_MUN, columns=COL_ACTOR, values='n')
                   .fillna(0))

        fig7 = go.Figure(go.Heatmap(
            z=pivot.values,
            x=[str(c) for c in pivot.columns],
            y=[str(r) for r in pivot.index],
            colorscale=[[0, BG_CARD2],[0.5, ACCENT],[1, ACCENT2]],
            hovertemplate="Municipio: <b>%{y}</b><br>Actor: <b>%{x}</b><br>Casos: %{z:,}<extra></extra>",
            showscale=True,
            colorbar=dict(tickfont=dict(color=TEXT_MUT), bgcolor=BG_CARD)
        ))
        fig7 = dark_layout(fig7)
        fig7.update_layout(height=360)
        st.plotly_chart(fig7, use_container_width=True, config={'displayModeBar': False})


# ─── FOOTER ───────────────────────────────────────────────────
st.markdown(f"""
<br>
<div class="app-footer">
    <span>
        🚦 &nbsp; VialAnalytics · Seguridad Vial Sabana Occidente &nbsp;·&nbsp;
        Proyecto SENA 2026
    </span>
</div>
""", unsafe_allow_html=True)