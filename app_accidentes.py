import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
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

# ─── ESTILOS CSS ──────────────────────────────────────────────
tema_actual = st.session_state.get('tema', 'Automático')

if tema_actual == "Modo Claro":
    theme_vars = """
    :root {
        --bg-color: #FAFAFA;
        --sidebar-bg: #ffffff;
        --sidebar-text: #002855;
        --card-bg: #ffffff;
        --card-border: #E2E8F0;
        --text-color: #002855;
        --title-color: #4A703C;
        --card-shadow: 0px 4px 10px rgba(0,0,0,0.05);
        --glow-bajo-shadow: 0px 4px 12px rgba(16, 185, 129, 0.2);
        --glow-bajo-border: 1px solid rgba(16, 185, 129, 0.3);
        --glow-medio-shadow: 0px 4px 12px rgba(245, 158, 11, 0.2);
        --glow-medio-border: 1px solid rgba(245, 158, 11, 0.3);
        --glow-alto-shadow: 0px 4px 12px rgba(211, 47, 47, 0.2);
        --glow-alto-border: 1px solid rgba(211, 47, 47, 0.3);
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
        --glow-bajo-shadow: 0px 0px 15px rgba(74, 222, 128, 0.5);
        --glow-bajo-border: 1px solid rgba(74, 222, 128, 0.7);
        --glow-medio-shadow: 0px 0px 15px rgba(251, 192, 45, 0.6);
        --glow-medio-border: 1px solid rgba(251, 192, 45, 0.8);
        --glow-alto-shadow: 0px 0px 15px rgba(255, 23, 68, 0.6);
        --glow-alto-border: 1px solid rgba(255, 23, 68, 0.8);
    }
    """
else:
    theme_vars = """
    :root {
        --bg-color: #FAFAFA;
        --sidebar-bg: #ffffff;
        --sidebar-text: #002855;
        --card-bg: #ffffff;
        --card-border: #E2E8F0;
        --text-color: #002855;
        --title-color: #4A703C;
        --card-shadow: 0px 4px 10px rgba(0,0,0,0.05);
        --glow-bajo-shadow: 0px 4px 12px rgba(16, 185, 129, 0.2);
        --glow-bajo-border: 1px solid rgba(16, 185, 129, 0.3);
        --glow-medio-shadow: 0px 4px 12px rgba(245, 158, 11, 0.2);
        --glow-medio-border: 1px solid rgba(245, 158, 11, 0.3);
        --glow-alto-shadow: 0px 4px 12px rgba(211, 47, 47, 0.2);
        --glow-alto-border: 1px solid rgba(211, 47, 47, 0.3);
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
            --glow-bajo-shadow: 0px 0px 15px rgba(74, 222, 128, 0.5);
            --glow-bajo-border: 1px solid rgba(74, 222, 128, 0.7);
            --glow-medio-shadow: 0px 0px 15px rgba(251, 192, 45, 0.6);
            --glow-medio-border: 1px solid rgba(251, 192, 45, 0.8);
            --glow-alto-shadow: 0px 0px 15px rgba(255, 23, 68, 0.6);
            --glow-alto-border: 1px solid rgba(255, 23, 68, 0.8);
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
        margin-left: 0;
        margin-right: 0;
    }}
    .banner-title {{
        color: #ffffff !important;
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        margin-bottom: 1rem !important;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.8);
        line-height: 1.2 !important;
    }}
    .banner-subtitle {{
        color: #F59E0B !important;
        font-size: 1.3rem !important;
        font-weight: 700 !important;
        text-shadow: 1px 1px 5px rgba(0,0,0,0.9);
        margin: 0 !important;
    }}

    /* Cajas Independientes (Contenedores) */
    div[data-testid="stVerticalBlockBorderWrapper"] {{
        background-color: var(--card-bg) !important;
        border: 1px solid var(--card-border) !important;
        border-radius: 12px !important;
        box-shadow: var(--card-shadow) !important;
        padding: 1.5rem !important;
        transition: all 0.3s ease;
    }}
    div[data-testid="stVerticalBlockBorderWrapper"]:hover {{
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1) !important;
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

    /* Efectos Glow Dinámicos */
    .glow-bajo {{
        box-shadow: var(--glow-bajo-shadow) !important;
        border: var(--glow-bajo-border) !important;
    }}
    .glow-medio {{
        box-shadow: var(--glow-medio-shadow) !important;
        border: var(--glow-medio-border) !important;
    }}
    .glow-alto {{
        box-shadow: var(--glow-alto-shadow) !important;
        border: var(--glow-alto-border) !important;
    }}

    /* KPIs */
    .kpi-value {{
        font-size: 2rem;
        font-weight: 800;
        color: var(--text-color);
        line-height: 1.2;
    }}
    .kpi-label {{
        font-size: 0.8rem;
        font-weight: 600;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 4px;
    }}

    /* Scrollbar */
    ::-webkit-scrollbar {{ width: 6px; height: 6px; }}
    ::-webkit-scrollbar-track {{ background: transparent; }}
    ::-webkit-scrollbar-thumb {{ background: rgba(150,150,150,0.3); border-radius: 3px; }}
</style>
""", unsafe_allow_html=True)


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
                🚦
            </div>
            <div>
                <div style="font-weight: 800; font-size: 18px; color: var(--text-color);">VialAnalytics</div>
                <div style="font-size: 11px; color: #64748B; font-weight: 600;">SABANA OCCIDENTE</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    pagina = st.radio(
        "Navegación",
        ["🏠 Inicio - Predictor", "📊 Análisis Visual"],
        label_visibility="collapsed"
    )

    # Espacio flexible y Burbuja inferior SENA
    st.markdown('<div style="flex-grow: 1; height: 35vh;"></div>', unsafe_allow_html=True)
    
    # Selector de tema manual integrado estéticamente antes de los créditos
    st.selectbox("🌓 Tema Visual", ["Automático", "Modo Claro", "Modo Oscuro"], key='tema')
    
    st.markdown("""
    <div class="sena-bubble">
        <div style="font-size: 18px; margin-bottom: 5px;">📘</div>
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
        <h1 class="banner-title">Análisis de la accidentalidad vial en los municipios de la Sabana de Occidente</h1>
        <p class="banner-subtitle">🛣️ Conocer los riesgos hoy para prevenir los accidentes de mañana.</p>
    </div>
    """, unsafe_allow_html=True)

    # ── KPIs GLOBALES (Sin filtros del predictor) ──────────────
    kpi_incidentes = f"{df_full[COL_CANT].sum() if COL_CANT else len(df_full):,.0f}".replace(',', '.')
    kpi_edad = f"{df_full[COL_EDAD].mean():.1f}" if COL_EDAD else "N/D"
    kpi_mun = df_full[COL_MUN].mode()[0] if COL_MUN else "N/D"
    kpi_actor = df_full[COL_ACTOR].mode()[0] if COL_ACTOR else "N/D"

    with st.container(border=True):
        st.markdown('<div class="block-title">Resumen Estadístico Global</div>', unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="kpi-label">Total Accidentes</div>
            <div class="kpi-value">{kpi_incidentes}</div>
            <div style="font-size: 11px; color: #64748B;">Registros acumulados</div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="kpi-label">Edad Promedio</div>
            <div class="kpi-value">{kpi_edad}</div>
            <div style="font-size: 11px; color: #64748B;">Años</div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="kpi-label">Municipio Crítico</div>
            <div class="kpi-value" style="font-size: 1.5rem;">{kpi_mun}</div>
            <div style="font-size: 11px; color: #64748B;">Mayor frecuencia</div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown(f"""
            <div class="kpi-label">Actor Vulnerable</div>
            <div class="kpi-value" style="font-size: 1.3rem;">{kpi_actor}</div>
            <div style="font-size: 11px; color: #64748B;">Más involucrado</div>
            """, unsafe_allow_html=True)

    # ── PREDICTOR DE RIESGO ─────────────────────────────────────
    p1, p2 = st.columns([1, 1], gap="large")
    
    with p1:
        with st.container(border=True):
            st.markdown('<div class="block-title">⚙️ Parámetros del Escenario</div>', unsafe_allow_html=True)
            edad = st.slider("Edad del actor vial", 0, 100, 30)
            
            def limpiar_opciones(col_name):
                opciones = sorted(df_full[col_name].dropna().unique())
                return [o for o in opciones if str(o).lower() not in ['no reportado', 'sin informacion', 'sin información']]

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
        
                    # === LOGICA DE SEMAFORO EXACTA ===
                    if riesgo_pct < 50:
                        color = "#10b981" # Verde - RIESGO BAJO
                        label = "🟢 RIESGO BAJO - CONTROLADO"
                        bg = "rgba(16, 185, 129, 0.1)"
                        glow_class = "glow-bajo"
                    elif riesgo_pct < 70:
                        color = "#F59E0B" # Amarillo Vial - RIESGO MEDIO
                        label = "🟠 RIESGO MEDIO - PRECAUCIÓN"
                        bg = "rgba(245, 158, 11, 0.1)"
                        glow_class = "glow-medio"
                    else:
                        color = "#EF4444" # Rojo Alerta - RIESGO ALTO
                        label = "🔴 RIESGO ALTO - CRÍTICO"
                        bg = "rgba(239, 68, 68, 0.1)"
                        glow_class = "glow-alto"
        
                    # Render del resultado
                    st.markdown(f"""
                    <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; min-height: 250px;">
                        <div style="position: relative; width: 180px; height: 180px;">
                            <svg width="180" height="180" viewBox="0 0 220 200" style="position: absolute; top:0; left:0;">
                                <circle cx="110" cy="100" r="80" stroke="rgba(150,150,150,0.2)" stroke-width="12" fill="transparent" stroke-dasharray="335 168" stroke-linecap="round" style="transform: rotate(150deg); transform-origin: 110px 100px;" />
                                <circle cx="110" cy="100" r="80" stroke="{color}" stroke-width="12" fill="transparent" stroke-dasharray="{335 * (riesgo_pct/100)} 503" stroke-linecap="round" style="transform: rotate(150deg); transform-origin: 110px 100px; transition: stroke-dasharray 0.5s ease-in-out, stroke 0.5s ease;" />
                            </svg>
                            <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; display: flex; flex-direction: column; align-items: center; justify-content: center; padding-top: 50px;">
                                <div style="font-size: 2.5rem; font-weight: 800; color: {color}; line-height: 1; transition: color 0.5s ease;">{riesgo_pct}%</div>
                            </div>
                        </div>
                        <div class="{glow_class}" style="background: {bg}; border-radius: 8px; padding: 12px 20px; width: 100%; margin-top: 20px; text-align: center; transition: all 0.5s ease;">
                            <div style="font-size: 1.1rem; font-weight: 800; color: {color}; letter-spacing: 0.05em;">{label}</div>
                            <div style="font-size: 0.8rem; color: var(--text-color); opacity: 0.8; margin-top: 4px;">Índice de riesgo estimado para el escenario</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
                except Exception as e:
                    st.error(f"Error en predicción: {e}")
            else:
                st.warning("Modelo no disponible. Por favor asegúrate de que 'modelo_accidentes.pkl' exista.")


# ════════════════════════════════════════════════════════════════
#  PÁGINA ANÁLISIS VISUAL
# ════════════════════════════════════════════════════════════════
else:
    # ── TÍTULO DE LA PÁGINA ─────────────────────────────────────
    st.markdown(f"""
    <div style="margin-bottom: 2rem;">
        <h1 style="color: var(--title-color); font-weight: 800; font-size: 2.2rem; margin-bottom: 0;">Análisis Visual Global</h1>
        <p style="color: #64748B; font-size: 1.1rem; margin-top: 5px;">Exploración del dataset completo de Sabana Occidente</p>
    </div>
    """, unsafe_allow_html=True)

    # ── GRÁFICOS (Limpios, sin filtros de predictor) ─────────────
    # Filas de 2 columnas para organizar los gráficos
    
    # FILA 1
    c1, c2 = st.columns(2, gap="large")
    with c1:
        with st.container(border=True):
            st.markdown('<div class="block-title">Accidentes por Municipio</div>', unsafe_allow_html=True)
            acc_mun = df_full.groupby(COL_MUN)[COL_CANT].sum().sort_values(ascending=False).reset_index()
            fig1 = px.bar(acc_mun, x=COL_MUN, y=COL_CANT, 
                          color=COL_CANT, color_continuous_scale=['#38BDF8', '#F59E0B'])
            fig1 = plotly_layout(fig1)
            fig1.update_layout(showlegend=False, xaxis_title="", yaxis_title="Cantidad")
            st.plotly_chart(fig1, use_container_width=True, config={'displayModeBar': False})

    with c2:
        with st.container(border=True):
            st.markdown('<div class="block-title">Distribución de Edades</div>', unsafe_allow_html=True)
            fig2 = px.histogram(df_full, x=COL_EDAD, nbins=20, 
                                color_discrete_sequence=['#38BDF8'])
            fig2 = plotly_layout(fig2)
            fig2.update_layout(showlegend=False, xaxis_title="Edad", yaxis_title="Frecuencia", bargap=0.05)
            st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})

    # FILA 2
    c3, c4 = st.columns(2, gap="large")
    with c3:
        with st.container(border=True):
            st.markdown('<div class="block-title">Accidentes por Mes</div>', unsafe_allow_html=True)
            if 'fecha_hecho' in df_full.columns:
                df_mes = df_full.copy()
                df_mes['Mes'] = df_mes['fecha_hecho'].dt.month
                acc_mes = df_mes.groupby('Mes')[COL_CANT].sum().reset_index()
                meses_nombres = {1:'Ene', 2:'Feb', 3:'Mar', 4:'Abr', 5:'May', 6:'Jun', 
                                 7:'Jul', 8:'Ago', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dic'}
                acc_mes['Nombre_Mes'] = acc_mes['Mes'].map(meses_nombres)
                fig3 = px.bar(acc_mes, x='Nombre_Mes', y=COL_CANT, 
                              color=COL_CANT, color_continuous_scale=['#38BDF8', '#F59E0B'])
                fig3 = plotly_layout(fig3)
                fig3.update_layout(showlegend=False, xaxis_title="", yaxis_title="Cantidad")
                st.plotly_chart(fig3, use_container_width=True, config={'displayModeBar': False})
            else:
                st.info("Columna fecha_hecho no disponible.")

    with c4:
        with st.container(border=True):
            st.markdown('<div class="block-title">Distribución de Tipos de Evento</div>', unsafe_allow_html=True)
            if COL_EVENTO:
                acc_ev = df_full[COL_EVENTO].value_counts().reset_index()
                acc_ev.columns = ['Tipo Evento', 'Cantidad']
                fig4 = px.bar(acc_ev, x='Tipo Evento', y='Cantidad', 
                              color='Cantidad', color_continuous_scale=['#38BDF8', '#F59E0B'])
                fig4 = plotly_layout(fig4)
                fig4.update_layout(showlegend=False, xaxis_title="", yaxis_title="")
                st.plotly_chart(fig4, use_container_width=True, config={'displayModeBar': False})

    # FILA 3
    c5, c6 = st.columns(2, gap="large")
    with c5:
        with st.container(border=True):
            st.markdown('<div class="block-title">Mapa de Calor (Municipio vs Evento)</div>', unsafe_allow_html=True)
            if COL_MUN and COL_EVENTO:
                tabla = df_full.pivot_table(values=COL_CANT, index=COL_MUN, columns=COL_EVENTO, aggfunc='sum', fill_value=0)
                fig5 = px.imshow(tabla, text_auto=True, aspect="auto", color_continuous_scale='Blues')
                fig5 = plotly_layout(fig5)
                fig5.update_layout(xaxis_title="", yaxis_title="")
                st.plotly_chart(fig5, use_container_width=True, config={'displayModeBar': False})

    with c6:
        with st.container(border=True):
            st.markdown('<div class="block-title">Distribución de Edad por Evento</div>', unsafe_allow_html=True)
            if COL_EVENTO and COL_EDAD:
                fig6 = px.box(df_full, x=COL_EVENTO, y=COL_EDAD, color=COL_EVENTO, 
                              color_discrete_sequence=px.colors.qualitative.Pastel)
                fig6 = plotly_layout(fig6)
                fig6.update_layout(showlegend=False, xaxis_title="", yaxis_title="Edad")
                st.plotly_chart(fig6, use_container_width=True, config={'displayModeBar': False})

    # FILA 4
    c7, c8 = st.columns(2, gap="large")
    with c7:
        with st.container(border=True):
            st.markdown('<div class="block-title">Género vs Tipo de Evento</div>', unsafe_allow_html=True)
            if COL_GENERO and COL_EVENTO:
                fig7 = px.histogram(df_full, x=COL_GENERO, color=COL_EVENTO, barmode='group',
                                    color_discrete_sequence=px.colors.qualitative.Set2)
                fig7 = plotly_layout(fig7)
                fig7.update_layout(xaxis_title="Género", yaxis_title="Cantidad")
                st.plotly_chart(fig7, use_container_width=True, config={'displayModeBar': False})

    with c8:
        with st.container(border=True):
            st.markdown('<div class="block-title">Importancia de Variables (Modelo)</div>', unsafe_allow_html=True)
            if modelo is not None:
                try:
                    cols_mod = list(modelo.feature_names_in_)
                    # Limpiamos los nombres para mostrar
                    display_cols = [c.split('_')[0] for c in cols_mod]
                    importances = modelo.feature_importances_
                    # Agrupar importancias por categoría general
                    imp_df = pd.DataFrame({'Variable': display_cols, 'Importancia': importances})
                    imp_grouped = imp_df.groupby('Variable')['Importancia'].sum().sort_values()
                    
                    fig8 = px.bar(x=imp_grouped.values, y=imp_grouped.index, orientation='h',
                                  color=imp_grouped.values, color_continuous_scale=['#38BDF8', '#F59E0B'])
                    fig8 = plotly_layout(fig8)
                    fig8.update_layout(showlegend=False, xaxis_title="Importancia", yaxis_title="")
                    st.plotly_chart(fig8, use_container_width=True, config={'displayModeBar': False})
                except Exception:
                    st.info("Importancia de variables no disponible.")
            else:
                st.info("Modelo no disponible.")

    # FILA 5 (Opcional - Matriz/Árbol)
    with st.container(border=True):
        st.markdown('<div class="block-title">Estructura del Árbol de Decisión (Random Forest)</div>', unsafe_allow_html=True)
        try:
            if os.path.exists("arbol_random_forest.png"):
                st.image("arbol_random_forest.png", use_container_width=True)
            else:
                st.info("Imagen del árbol no encontrada (arbol_random_forest.png)")
        except Exception:
            pass