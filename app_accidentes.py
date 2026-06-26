import streamlit as st
import pandas as pd
import numpy as np
try:
    import matplotlib.pyplot as plt
    import seaborn as sns
except Exception as e:
    st.warning(f"Matplotlib/Seaborn could not be loaded: {e}. Some visualizations may be unavailable.")
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import xgboost as xgb
import joblib
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import base64
import os
import warnings
import streamlit.components.v1 as components
warnings.filterwarnings('ignore')

# ─── CONFIGURACIÓN ────────────────────────────────────────────
st.set_page_config(
    page_title="Seguridad Vial · Sabana Occidente",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded"
)

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

@st.cache_data
def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except Exception:
        return ""

img_b64 = get_base64_of_bin_file("imagen_principal.jpeg")
if img_b64:
    banner_bg = f"url('data:image/jpeg;base64,{img_b64}')"
else:
    banner_bg = "#1E293B"

map_b64 = get_base64_of_bin_file("image_33ea3a.png")
if map_b64:
    map_bg = f"url('data:image/png;base64,{map_b64}')"
else:
    map_bg = 'url("image_33ea3a.png")'

# ─── ESTADO GLOBAL DEL GLOW ────────────────────────────────────
if 'risk_color' not in st.session_state:
    st.session_state.risk_color = '#4ADE80'  # Verde por defecto

risk_color = st.session_state.risk_color

# ─── ESTILOS CSS ──────────────────────────────────────────────
tema_actual = st.session_state.get('tema', 'Automático')

if tema_actual == "Modo Claro":
    theme_vars = """
    :root {
        --bg-color: #F4F4F0;
        --sidebar-bg: #ffffff;
        --sidebar-text: #002855;
        --card-bg: #ffffff;
        --card-border: #E2E8F0;
        --text-color: #002855;
        --title-color: #4A703C;
        --card-shadow: 0px 4px 10px rgba(0,0,0,0.05);
        --glow-bajo-shadow: 0px 4px 15px rgba(74, 222, 128, 0.3);
        --glow-bajo-border: 1px solid rgba(74, 222, 128, 0.4);
        --glow-medio-shadow: 0px 4px 15px rgba(251, 192, 45, 0.3);
        --glow-medio-border: 1px solid rgba(251, 192, 45, 0.4);
        --glow-alto-shadow: 0px 4px 18px rgba(211, 47, 47, 0.35);
        --glow-alto-border: 1px solid rgba(211, 47, 47, 0.45);
    }
    """
elif tema_actual == "Modo Oscuro":
    theme_vars = """
    :root {
        --bg-color: #0B132B;
        --sidebar-bg: #1E293B;
        --sidebar-text: #F8FAFC;
        --card-bg: #1E293B;
        --card-border: rgba(255, 255, 255, 0.08);
        --text-color: #F8FAFC;
        --title-color: #F8FAFC;
        --card-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        --glow-bajo-shadow: 0px 0px 25px #4ADE80;
        --glow-bajo-border: 2px solid #4ADE80;
        --glow-medio-shadow: 0px 0px 25px #FBC02D;
        --glow-medio-border: 2px solid #FBC02D;
        --glow-alto-shadow: 0px 0px 30px #FF1744;
        --glow-alto-border: 2px solid #FF1744;
    }
    """
else:
    theme_vars = """
    :root {
        --bg-color: #F4F4F0;
        --sidebar-bg: #ffffff;
        --sidebar-text: #002855;
        --card-bg: #ffffff;
        --card-border: #E2E8F0;
        --text-color: #002855;
        --title-color: #4A703C;
        --card-shadow: 0px 4px 10px rgba(0,0,0,0.05);
        --glow-bajo-shadow: 0px 4px 15px rgba(74, 222, 128, 0.3);
        --glow-bajo-border: 1px solid rgba(74, 222, 128, 0.4);
        --glow-medio-shadow: 0px 4px 15px rgba(251, 192, 45, 0.3);
        --glow-medio-border: 1px solid rgba(251, 192, 45, 0.4);
        --glow-alto-shadow: 0px 4px 18px rgba(211, 47, 47, 0.35);
        --glow-alto-border: 1px solid rgba(211, 47, 47, 0.45);
    }
    @media (prefers-color-scheme: dark) {
        :root {
            --bg-color: #0B132B;
            --sidebar-bg: #1E293B;
            --sidebar-text: #F8FAFC;
            --card-bg: #1E293B;
            --card-border: rgba(255, 255, 255, 0.08);
            --text-color: #F8FAFC;
            --title-color: #F8FAFC;
            --card-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            --glow-bajo-shadow: 0px 0px 25px #4ADE80;
            --glow-bajo-border: 2px solid #4ADE80;
            --glow-medio-shadow: 0px 0px 25px #FBC02D;
            --glow-medio-border: 2px solid #FBC02D;
            --glow-alto-shadow: 0px 0px 30px #FF1744;
            --glow-alto-border: 2px solid #FF1744;
        }
    }
    """

st.markdown(f"""
<style>
    /* Ocultar elementos predeterminados de Streamlit */
    header, footer, [data-testid="stToolbar"], #MainMenu {{
        display: none !important;
    }}

    /* === VARIABLES DE TEMA === */
    {theme_vars}

    /* Aplicar colores de fondo */
    .stApp {{
        background: var(--bg-color) !important;
    }}
    .stApp::before {{
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        background-image: {map_bg};
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        opacity: {'0.08' if tema_actual == 'Modo Oscuro' else '0.12'};
        z-index: -1;
        pointer-events: none;
    }}
    
    [data-testid="stSidebar"] {{
        background: var(--sidebar-bg) !important;
        border-right: 1px solid var(--card-border) !important;
    }}

    /* Textos del sidebar: asegurando visibilidad en Modo Oscuro */
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stSlider label,
    [data-testid="stSidebar"] .stRadio label {{
        color: var(--sidebar-text) !important;
        font-weight: 600 !important;
    }}

    /* Corrección de Inputs para contraste claro/oscuro (Filtros) */
    div[data-baseweb="select"] > div {{
        background-color: var(--card-bg) !important;
        color: var(--text-color) !important;
        border-color: var(--card-border) !important;
    }}
    div[data-baseweb="select"] > div span {{
        color: var(--text-color) !important;
    }}
    div[data-baseweb="popover"] ul {{
        background-color: var(--card-bg) !important;
        color: var(--text-color) !important;
    }}
    div[data-baseweb="popover"] li {{
        color: var(--text-color) !important;
    }}

    /* Forzar visibilidad y color adecuado en el panel principal */
    [data-testid="stMain"] h1,
    [data-testid="stMain"] h2,
    [data-testid="stMain"] h3,
    [data-testid="stMain"] p,
    [data-testid="stMain"] label,
    [data-testid="stMain"] span {{
        color: var(--text-color) !important;
    }}

    /* Burbuja SENA inferior en Sidebar limpia y sutil */
    .sena-bubble {{
        background: rgba(150, 150, 150, 0.1);
        color: var(--sidebar-text);
        padding: 15px;
        border-radius: 16px;
        text-align: center;
        margin-top: 20px;
        border: 1px solid rgba(150, 150, 150, 0.2);
    }}

    /* Banner Principal (Ajustes de padding y cover) */
    .banner-container {{
        background-image: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)), {banner_bg};
        background-size: cover;
        background-position: center;
        border-radius: 16px;
        padding: 40px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
        width: 100%;
        margin: 0 !important;
    }}
    .block-container {{
        padding-top: 1rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }}
    [data-testid="stMain"] .banner-title,
    div.banner-container h1.banner-title,
    .banner-title {{
        color: #ffffff !important;
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        margin-bottom: 1rem !important;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.8) !important;
        line-height: 1.2 !important;
    }}
    [data-testid="stMain"] .banner-subtitle,
    div.banner-container p.banner-subtitle,
    .banner-subtitle {{
        color: #F59E0B !important;
        font-size: 1.3rem !important;
        font-weight: 700 !important;
        text-shadow: 1px 1px 5px rgba(0,0,0,0.9) !important;
        margin: 0 !important;
    }}

    /* Cajas Independientes (Contenedores) - Tema original */
    div[data-testid="stVerticalBlockBorderWrapper"] {{
        background-color: var(--card-bg) !important;
        border: 1px solid var(--card-border) !important;
        border-radius: 12px !important;
        box-shadow: var(--card-shadow) !important;
        padding: 1.5rem !important;
        transition: all 0.5s ease;
    }}
    div[data-testid="stVerticalBlockBorderWrapper"]:hover {{
        transform: translateY(-2px);
    }}

    /* Títulos de los bloques */
    .block-title {{
        color: var(--title-color) !important;
        font-size: 1.15rem !important;
        font-weight: 800 !important;
        margin-bottom: 1rem !important;
        margin-top: 0 !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}

    /* Contenedor principal de cada tarjeta del resumen */
    /* Contenedor principal adaptable */
    [data-testid="stMain"] .tarjeta-resumen,
    div.tarjeta-resumen {{
        background-color: var(--secondary-background-color) !important;
        border: 1px solid rgba(0, 210, 255, 0.15) !important;
        border-bottom: 4px solid #00D2FF !important; /* Línea inferior azul neón */
        border-radius: 12px !important;
        box-shadow: 0px 6px 15px -8px rgba(0, 210, 255, 0.25) !important;
        padding: 15px !important; /* Un poco más compacto para pantallas chicas */
        margin-bottom: 15px !important;
        text-align: left;
        width: 100% !important;
        box-sizing: border-box !important;
    }}
    
    /* 1. COLOR FIJO PARA EL TÍTULO (Cyan Vibrante - Visible en ambos temas) */
    [data-testid="stMain"] .tarjeta-resumen h4,
    div.tarjeta-resumen h4 {{
        color: #00B4D8 !important; 
        font-size: 12px !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        margin-bottom: 5px !important;
        margin-top: 0 !important;
        display: flex !important;
        align-items: center !important;
        gap: 6px !important;
    }}
    
    /* 2. COLOR FIJO PARA EL DATO PRINCIPAL (Cyan Neón - Visible siempre) */
    [data-testid="stMain"] .tarjeta-resumen h2,
    div.tarjeta-resumen h2 {{
        color: #00D2FF !important; 
        font-size: 24px !important;
        font-weight: bold !important;
        margin: 0 !important;
        text-shadow: 0 0 8px rgba(0, 210, 255, 0.3) !important;
    }}
    
    /* 3. COLOR FIJO PARA EL SUBTÍTULO / TEXTO DESCRIPTIVO (Gris Neutro - Visible siempre) */
    [data-testid="stMain"] .tarjeta-resumen p,
    div.tarjeta-resumen p {{
        color: #94A3B8 !important; 
        font-size: 11px !important;
        margin-top: 5px !important;
        margin-bottom: 0 !important;
    }}
    
    /* Garantizar que el emoji mantenga su color nativo original */
    [data-testid="stMain"] .tarjeta-resumen span.emoji,
    div.tarjeta-resumen span.emoji {{
        color: initial !important;
        font-style: normal !important;
    }}

    /* REGLAS ESPECÍFICAS PARA CELULARES (Pantallas menores a 768px) */
    @media (max-width: 768px) {{
        /* Forzar a Streamlit a que muestre las columnas de forma limpia y ordenada */
        [data-testid="stMain"] div[data-testid="column"] {{
            width: 100% !important;
            flex: 1 1 100% !important;
            display: block !important;
            margin-bottom: 10px !important;
        }}
        
        [data-testid="stMain"] .tarjeta-resumen h2,
        div.tarjeta-resumen h2 {{
            font-size: 22px !important; /* Optimiza el tamaño en celulares */
        }}
    }}

    /* Ocultar el botón verde nativo del slider y poner el Pin 📍 */
    div[data-testid="stSlider"] [role="slider"] {{
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }}
    div[data-testid="stSlider"] [role="slider"]::before {{
        content: "📍" !important;
        font-size: 22px !important;
        display: block;
        position: absolute;
        top: -12px;
        left: -6px;
    }}

    /* Scrollbar */
    ::-webkit-scrollbar {{ width: 6px; height: 6px; }}
    ::-webkit-scrollbar-track {{ background: transparent; }}
    ::-webkit-scrollbar-thumb {{ background: rgba(150,150,150,0.3); border-radius: 3px; }}
</style>
""", unsafe_allow_html=True)

# ─── INYECCIÓN DEL SCRIPT NEÓN (EXTRAE SOLO EL SCRIPT) ────────
# neon_script.html contiene la app standalone completa + el script neón.
# Aquí extraemos SOLO el <script id="neon-streamlit">...</script>
# para inyectarlo en Streamlit sin romper la interfaz.
import re
try:
    neon_html_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "neon_script.html")
    if os.path.exists(neon_html_path):
        with open(neon_html_path, "r", encoding="utf-8") as f:
            neon_raw = f.read()
        # Extraer solo el script con id="neon-streamlit"
        match = re.search(r'(<script id="neon-streamlit">.*?</script>)', neon_raw, re.DOTALL)
        if match:
            neon_script = match.group(1)
            neon_script = neon_script.replace("COLOR_PLACEHOLDER", risk_color)
            neon_script = neon_script.replace("THEME_PLACEHOLDER", "true" if tema_actual == "Modo Oscuro" else "false")
            st.markdown(neon_script, unsafe_allow_html=True)
except Exception:
    pass  # Silencioso: el script neón es cosmético, no crítico


def plotly_layout(fig):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif"),
        margin=dict(l=8, r=8, t=40, b=8),
        hoverlabel=dict(bgcolor="rgba(30,41,59,0.9)", font=dict(color="#ffffff", size=12))
    )
    return fig

# ─── CARGA DE DATOS ───────────────────────────────────────────
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('Archivo_Accidentes.csv', sep=None, engine='python')
        # Estandarizar columnas a minúsculas para fácil acceso
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
        # Identificar y parsear columna de fechas robustamente
        col_fecha = None
        for c in df.columns:
            if 'fecha' in c:
                col_fecha = c
                break
        if col_fecha:
            df[col_fecha] = pd.to_datetime(df[col_fecha], errors='coerce')
            # Renombrar obligatoriamente a fecha_hecho para evitar que las gráficas fallen
            if col_fecha != 'fecha_hecho':
                df.rename(columns={col_fecha: 'fecha_hecho'}, inplace=True)
        return df
    except Exception as e:
        st.error(f"⚠️ Error al cargar datos: {e}")
        return None

@st.cache_resource
def load_model():
    try:
        return joblib.load('modelo_accidentes.pkl')
    except:
        return None

df_full = load_data()
modelo = load_model()

if df_full is None:
    st.error("🚨 No se encontró 'Archivo_Accidentes.csv'.")
    st.stop()

# Detectar columnas estandarizadas
COL_EDAD = find_col(df_full, 'edad', 'age')
COL_MUN = find_col(df_full, 'municipio', 'ciudad')
COL_ZONA = find_col(df_full, 'zona', 'zone', 'area')
COL_GENERO = find_col(df_full, 'genero', 'sexo', 'gender')
COL_ACTOR = find_col(df_full, 'actor_vial', 'actor')
COL_EVENTO = find_col(df_full, 'tipo_evento', 'gravedad')
COL_CANT = find_col(df_full, 'cantidad')


# ─── SIDEBAR ─────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding: 10px 0 20px;">
        <div style="display: flex; align-items: center; gap: 12px;">
            <div style="width: 40px; height: 40px; border-radius: 12px;
                        background: linear-gradient(135deg, #4f8cf7, #7c6df0);
                        display: flex; align-items: center; justify-content: center;
                        font-size: 20px; flex-shrink: 0; color: white;">
                🛣️
            </div>
            <div>
                <div style="font-weight: 800; font-size: 18px; color: var(--text-color);">VialAnalytics</div>
                <div style="font-size: 11px; color: #64748B; font-weight: 600;">SABANA OCCIDENTE - \nFACATATIVÁ, FUNZA, MADRID Y MOSQUERA</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    pagina = st.radio(
        "Navegación",
        ["🏠 Inicio - Predictor", "📊 Análisis Visual"],
        label_visibility="collapsed"
    )

    # Espacio flexible y Burbuja inferior SENA (ajustado para dar espacio al QR)
    st.markdown('<div style="flex-grow: 1; height: 10vh;"></div>', unsafe_allow_html=True)
    
    # Selector de tema manual integrado estéticamente antes de los créditos
    st.selectbox("🌓 Tema Visual", ["Automático", "Modo Claro", "Modo Oscuro"], key='tema')
    
    # Logo oficial del SENA
    st.markdown("""
    <div style="display: flex; justify-content: center; margin-bottom: 8px;">
        <img src="https://upload.wikimedia.org/wikipedia/commons/8/83/Sena_Colombia_logo.svg" 
             alt="Logo SENA" width="90" 
             style="filter: drop-shadow(0 2px 4px rgba(0,0,0,0.15)); transition: transform 0.3s ease;"
             onmouseover="this.style.transform='scale(1.08)'" 
             onmouseout="this.style.transform='scale(1)'">
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="sena-bubble">
        <div style="font-size: 13px; font-weight: 700;">Proyecto SENA 2026</div>
        <div style="font-size: 11px; opacity: 0.7;">Análisis de Accidentalidad Vial</div>
    </div>
    """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════
#  PÁGINA INICIO · PREDICTOR
# ════════════════════════════════════════════════════════════════
if "Inicio" in pagina:
    # ── BANNER PRINCIPAL ───────────────────────────────────────
    st.markdown(f"""
    <div class="banner-container">
        <h1 class="banner-title" style="color: #ffffff !important; font-size: 2.5rem !important; font-weight: 800 !important; margin-bottom: 1rem !important; text-shadow: 2px 2px 8px rgba(0,0,0,0.8) !important; line-height: 1.2 !important; text-align: center !important;">Análisis de la accidentalidad vial en los municipios de Facatativá, Funza, Madrid y Mosquera durante el periodo 2021–2026.</h1>
        <p class="banner-subtitle" style="color: #F59E0B !important; font-size: 1.3rem !important; font-weight: 700 !important; text-shadow: 1px 1px 5px rgba(0,0,0,0.9) !important; margin: 0 !important; text-align: center !important;">🛣️ Conocer los riesgos hoy para prevenir los accidentes de mañana.</p>
    </div>
    """, unsafe_allow_html=True)

    # ── KPIs GLOBALES (Sin filtros del predictor) ──────────────
    kpi_incidentes = f"{df_full[COL_CANT].sum() if COL_CANT else len(df_full):,.0f}".replace(',', '.')
    kpi_edad = f"{df_full[COL_EDAD].mean():.1f}" if COL_EDAD else "N/D"
    kpi_mun = df_full[COL_MUN].mode()[0] if COL_MUN else "N/D"
    kpi_actor = df_full[COL_ACTOR].mode()[0] if COL_ACTOR else "N/D"

    st.subheader("📊 Resumen Estadístico Global")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
            <div class='tarjeta-resumen'>
                <h4><span class='emoji'>🚨</span> Total Accidentes</h4>
                <h2>{kpi_incidentes}</h2>
                <p>Registros acumulados</p>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class='tarjeta-resumen'>
                <h4><span class='emoji'>🎂</span> Edad Promedio</h4>
                <h2>{kpi_edad} años</h2>
                <p>Datos de involucrados</p>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <div class='tarjeta-resumen'>
                <h4><span class='emoji'>📍</span> Municipio Crítico</h4>
                <h2>{kpi_mun}</h2>
                <p>Mayor frecuencia</p>
            </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
            <div class='tarjeta-resumen'>
                <h4><span class='emoji'>👤</span> Actor Vulnerable</h4>
                <h2>{kpi_actor}</h2>
                <p>Más involucrado</p>
            </div>
        """, unsafe_allow_html=True)

    # ── PREDICTOR DE RIESGO ─────────────────────────────────────
    p1, p2 = st.columns([1, 1], gap="large")
    
    with p1:
        with st.container(border=True):
            st.markdown('<div class="block-title">⚙️ Parámetros del Escenario</div>', unsafe_allow_html=True)
            edad = st.slider("Edad del actor vial", 0, 100, 30)
            
            def limpiar_opciones(col_name):
                opciones = sorted(df_full[col_name].dropna().unique())
                return [o for o in opciones if str(o) != 'Sin información']

            mun_sel = st.selectbox("Municipio", limpiar_opciones(COL_MUN)) if COL_MUN else None
            zon_sel = st.selectbox("Zona del incidente", limpiar_opciones(COL_ZONA)) if COL_ZONA else None
            gen_sel = st.selectbox("Género", limpiar_opciones(COL_GENERO)) if COL_GENERO else None
            act_sel = st.selectbox("Tipo de actor vial", limpiar_opciones(COL_ACTOR)) if COL_ACTOR else None
    
    with p2:
        with st.container(border=True):
            st.markdown('<div class="block-title">🔮 Predicción de Riesgo</div>', unsafe_allow_html=True)
            
            if modelo is not None:
                try:
                    cols_mod = list(modelo.feature_names_in_)
                    inp = pd.DataFrame(0, index=[0], columns=cols_mod)
        
                    # Asignar edad
                    for col in ['Edad', 'edad', 'age']:
                        if col in inp.columns:
                            inp.at[0, col] = edad
                            break
        
                    # Función de mapeo limpio
                    def set_feature(prefix, val):
                        if not val:
                            return
                        # Normalizar el valor seleccionado
                        val_norm = str(val).lower()
                        for c, r in [('á','a'), ('é','e'), ('í','i'), ('ó','o'), ('ú','u'), ('ñ','n')]:
                            val_norm = val_norm.replace(c, r)
                            
                        for col in inp.columns:
                            # Limpiar nombre de columna del modelo (ej: 'Municipio_Facatativ' -> 'Municipio_Facatativa')
                            col_clean = col
                            if 'Facatativ' in col_clean:
                                col_clean = col_clean.replace('Facatativ', 'Facatativa').replace('Facatativ', 'Facatativa')
                            if 'informacin' in col_clean or 'informacin' in col_clean:
                                col_clean = col_clean.replace('informacin', 'informacion').replace('informacin', 'informacion')
                                
                            col_norm = col_clean.lower()
                            for c, r in [('á','a'), ('é','e'), ('í','i'), ('ó','o'), ('ú','u'), ('ñ','n')]:
                                col_norm = col_norm.replace(c, r)
                                
                            if col_norm.startswith(f"{prefix.lower()}_"):
                                feat_val = col_norm[len(prefix.lower())+1:]
                                if feat_val == val_norm or val_norm in feat_val or feat_val in val_norm:
                                    inp.at[0, col] = 1
                                    return
        
                    set_feature('Municipio', mun_sel)
                    set_feature('Zona', zon_sel)
                    set_feature('Genero', gen_sel)
        
                    # Mapear actor a arma
                    arma_val = 'No Reportado'
                    if act_sel:
                        act_lower = act_sel.lower()
                        if 'moto' in act_lower:
                            arma_val = 'Moto'
                        elif 'bicicleta' in act_lower or 'ciclista' in act_lower:
                            arma_val = 'Bicicleta'
                        elif 'vehiculo' in act_lower or 'vehículo' in act_lower:
                            arma_val = 'Vehiculo'
                        elif 'peaton' in act_lower or 'peatón' in act_lower:
                            arma_val = 'Sin empleo de armas'
                    set_feature('Armas_medios', arma_val)
        
                    # Grupo etario
                    grupo_val = 'No Reportado'
                    if edad < 12:
                        grupo_val = 'Menores'
                    elif edad < 18:
                        grupo_val = 'Adolescentes'
                    else:
                        grupo_val = 'Adultos'
                    set_feature('Grupo_etario', grupo_val)
        
                    # Predicción
                    pred = modelo.predict(inp)[0]
                    probs = modelo.predict_proba(inp)[0]
                    conf = max(probs)
                    riesgo_pct = round(conf * 100, 1)
        
                    # === LOGICA DE SEMAFORO CON GLOW INLINE ===
                    is_dark = tema_actual == "Modo Oscuro"
                    
                    # 1. Lógica del Semáforo de Riesgo (color del aro y líneas cambia según el riesgo)
                    if riesgo_pct < 50:
                        color = "#4ADE80"
                        color_riesgo = "#4ADE80"  # Verde Neón (Riesgo Bajo)
                        label = "🟢 RIESGO BAJO - CONTROLADO"
                        bg = "rgba(74, 222, 128, 0.08)"
                        glow_shadow = "0px 0px 25px #4ADE80"
                        glow_border = "2px solid #4ADE80"
                    elif riesgo_pct < 70:
                        color = "#FBC02D"
                        color_riesgo = "#FBC02D"  # Amarillo/Naranja (Riesgo Medio)
                        label = "🟠 RIESGO MEDIO - PRECAUCIÓN"
                        bg = "rgba(251, 192, 45, 0.08)"
                        glow_shadow = "0px 0px 25px #FBC02D"
                        glow_border = "2px solid #FBC02D"
                    else:
                        color = "#FF1744"
                        color_riesgo = "#FF1744"  # Rojo Neón (Riesgo Alto)
                        label = "🔴 RIESGO ALTO - CRÍTICO"
                        bg = "rgba(255, 23, 68, 0.08)"
                        glow_shadow = "0px 0px 30px #FF1744"
                        glow_border = "2px solid #FF1744"
        
                    # Render del resultado con estilos INLINE
                    import math

                    # Usar color_riesgo como color del arco (dinámico)
                    color_neon = color_riesgo

                    st.markdown(f"""
                    <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; min-height: 280px; width: 100%;">
                        <div style="position: relative; width: 220px; height: 200px; display: inline-block;">
                            <svg width="220" height="200" viewBox="0 0 220 200" style="position: absolute; top:0; left:0; filter: drop-shadow(0px 0px 8px {color_riesgo}80);">
                                <circle cx="110" cy="100" r="80" stroke="rgba(150,150,150,0.2)" stroke-width="12" fill="transparent" stroke-dasharray="335 168" stroke-linecap="round" style="transform: rotate(150deg); transform-origin: 110px 100px;" />
                                <circle cx="110" cy="100" r="80" stroke="{color_riesgo}" stroke-width="14" fill="transparent" stroke-dasharray="{335 * (riesgo_pct/100)} 503" stroke-linecap="round" style="transform: rotate(150deg); transform-origin: 110px 100px; filter: drop-shadow(0px 0px 6px {color_riesgo}); transition: stroke-dasharray 0.5s ease-in-out, stroke 0.5s ease;" />
                            </svg>
                            <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; display: flex; flex-direction: column; align-items: center; justify-content: center; padding-top: 20px;">
                                <div style="font-size: 2.5rem; font-weight: 800; color: {color_riesgo}; line-height: 1; text-shadow: 0px 0px 15px {color_riesgo};">{riesgo_pct}%</div>
                            </div>
                        </div>
                        <div style="background: {bg}; box-shadow: {glow_shadow}; border: {glow_border}; border-radius: 10px; padding: 14px 24px; width: 100%; display: block; margin-top: 20px; text-align: center;">
                            <div style="font-size: 1.15rem; font-weight: 800; color: {color_riesgo}; letter-spacing: 0.05em; text-shadow: 0px 0px 8px {color_riesgo}80;">{label}</div>
                            <div style="font-size: 0.8rem; color: var(--text-color); opacity: 0.8; margin-top: 4px;">Índice de riesgo estimado para el escenario</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    # Guardar color de riesgo en session_state para glow global
                    st.session_state.risk_color = color_riesgo

                    pass
        
                except Exception as e:
                    st.error(f"Error en predicción: {e}")
            else:
                st.warning("Modelo no disponible. Por favor asegúrate de que 'modelo_accidentes.pkl' exista.")


# ════════════════════════════════════════════════════════════════
#  PÁGINA ANÁLISIS VISUAL
# ════════════════════════════════════════════════════════════════
else:
    st.markdown("""
    <div style="margin-bottom: 2rem;">
        <h1 style="color: var(--title-color) !important; font-weight: 800; font-size: 2.2rem; margin-bottom: 0;">📈 Análisis de Datos del Notebook (.ipynb)</h1>
        <p style="color: #64748B !important; font-size: 1.1rem; margin-top: 5px;">Exploración detallada de la accidentalidad vial</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Aquí inyectamos el HTML que lee el archivo de las gráficas
    import streamlit.components.v1 as components
    import os
    
    neon_html_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "neon_script.html")
    if os.path.exists(neon_html_path):
        with open(neon_html_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        components.html(html_content, height=1200, scrolling=True)
    else:
        st.warning("El archivo neon_script.html no fue encontrado.")