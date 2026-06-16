import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Centro de Control: Seguridad Vial Sabana",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- PALETA DE COLORES PREMIUM ---
fondo = '#1E293B'
azul = '#38BDF8'
naranja = '#F59E0B'
verde = '#34D399'
rojo = '#F87171'
morado = '#A78BFA'
palette = [azul, naranja, verde, morado, rojo]

# --- ESTILO CSS AVANZADO (TEMÁTICA TRÁNSITO) ---
st.markdown(f"""
<style>
    .main {{ background-color: {fondo}; color: white; }}
    .stApp {{ background-color: {fondo}; }}
    
    /* Estilo para las métricas de Dashboard */
    [data-testid="stMetricValue"] {{ color: {azul}; font-size: 38px; font-weight: bold; }}
    [data-testid="stMetricLabel"] {{ color: #CBD5E1; font-size: 18px; }}
    
    /* Contenedores de Tarjetas */
    .stMetric {{
        background-color: #2D3748;
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #4A5568;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }}
    
    /* Botones y Sliders */
    .stButton>button {{ 
        background-color: {azul}; 
        color: white; 
        border-radius: 10px; 
        width: 100%; 
        font-weight: bold;
        height: 3em;
    }}
    .stSlider>div>div>div {{ background-color: {azul} !important; }}
    
    /* Títulos con tipografía moderna */
    h1, h2, h3 {{ 
        color: {azul}; 
        font-family: 'Inter', sans-serif;
        letter-spacing: -0.5px;
    }}
    
    /* Sidebar personalizado */
    .css-1d391kg {{ background-color: #1E293B; }}
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------
# UTILIDAD: Buscar columna por palabras clave (case-insensitive)
# ---------------------------------------------------------------
def find_col(df, *keywords):
    """
    Devuelve el nombre real de la primera columna que contenga
    alguna de las palabras clave (sin distinguir mayúsculas).
    Retorna None si no encuentra ninguna.
    """
    cols_lower = {c.lower(): c for c in df.columns}
    for kw in keywords:
        kw_l = kw.lower()
        # Coincidencia exacta
        if kw_l in cols_lower:
            return cols_lower[kw_l]
        # Coincidencia parcial
        for cl, cr in cols_lower.items():
            if kw_l in cl:
                return cr
    return None


# --- CARGA DE DATOS Y MODELO ---
@st.cache_data
def load_clean_data():
    try:
        df = pd.read_csv('transito_sabana_occidente.csv', sep=None, engine='python')
        # Normalización robusta: lowercase, sin espacios al borde, espacios → _
        df.columns = (
            df.columns
            .str.strip()
            .str.lower()
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
    except Exception as e:
        st.warning(f"Modelo no disponible: {e}")
        return None

df = load_clean_data()
modelo = load_trained_model()

# --- VERIFICACIÓN DE ARCHIVOS ---
if df is None:
    st.error("🚨 Error Crítico: No se encontró 'transito_sabana_occidente.csv'.")
    st.stop()

# Detectar columnas automáticamente
COL_EDAD     = find_col(df, 'edad', 'age')
COL_MUN      = find_col(df, 'municipio', 'ciudad', 'municipality')
COL_ZONA     = find_col(df, 'zona', 'zone', 'area')
COL_GENERO   = find_col(df, 'genero', 'sexo', 'gender', 'sex')
COL_ACTOR    = find_col(df, 'actor_vial', 'actor', 'tipo_actor', 'clase_actor', 'victima', 'rol')

# Mostrar diagnóstico si alguna columna no se encuentra
cols_faltantes = {k: v for k, v in {
    'Edad': COL_EDAD, 'Municipio': COL_MUN, 'Zona': COL_ZONA,
    'Género': COL_GENERO, 'Actor Vial': COL_ACTOR
}.items() if v is None}

if cols_faltantes:
    with st.expander("⚠️ Diagnóstico de columnas (expandir para ver)"):
        st.warning(f"No se detectaron las columnas: **{', '.join(cols_faltantes.keys())}**")
        st.write("Columnas disponibles en el CSV:")
        st.code(str(list(df.columns)))

# --- HEADER PRINCIPAL ---
st.title("🛡️ Centro de Inteligencia de Seguridad Vial")
st.markdown("#### Análisis de Accidentalidad: Funza • Mosquera • Facatativá • Madrid")
st.write("---")

# --- DASHBOARD DE CONTROL (KPIs) ---
st.subheader("📊 Indicadores de Movilidad")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Incidentes Registrados", f"{len(df):,}")
with col2:
    val_edad = f"{df[COL_EDAD].mean():.1f} años" if COL_EDAD else "N/D"
    st.metric("Edad Media Crítica", val_edad)
with col3:
    val_mun = df[COL_MUN].mode()[0] if COL_MUN else "N/D"
    st.metric("Municipio con Mayor Riesgo", val_mun)
with col4:
    val_actor = df[COL_ACTOR].mode()[0] if COL_ACTOR else "N/D"
    st.metric("Actor Vial más Vulnerable", val_actor)

st.write("---")

# --- SIMULADOR DE ESCENARIOS DE RIESGO ---
col_sim, col_res = st.columns([1, 1.2])

with col_sim:
    st.subheader("🚦 Configuración del Escenario")
    st.info("Ajusta los parámetros para evaluar la probabilidad de riesgo vial.")

    edad = st.slider("Edad del Actor Vial", 0, 100, 30)

    if COL_MUN:
        mun = st.selectbox("Municipio de Ocurrencia", sorted(df[COL_MUN].dropna().unique()))
    else:
        mun = None

    if COL_ZONA:
        zon = st.selectbox("Zona del Incidente", sorted(df[COL_ZONA].dropna().unique()))
    else:
        zon = None

    if COL_GENERO:
        gen = st.selectbox("Género del Involucrado", sorted(df[COL_GENERO].dropna().unique()))
    else:
        gen = None

    if COL_ACTOR:
        act = st.selectbox("Tipo de Actor Vial", sorted(df[COL_ACTOR].dropna().unique()))
    else:
        act = None

with col_res:
    st.subheader("🔮 Predicción de Riesgo Predictivo")

    if modelo is not None:
        try:
            cols_mod = list(modelo.feature_names_in_)
            input_df = pd.DataFrame(0, index=[0], columns=cols_mod)

            # Asignar edad (buscar nombre de columna flexible)
            for possible in ['edad', 'Edad', 'age', 'Age']:
                if possible in input_df.columns:
                    input_df.at[0, possible] = edad
                    break

            # Activar variables One-Hot
            candidates = []
            if mun:
                candidates.append(f'{COL_MUN}_{mun}')
                candidates.append(f'Municipio_{mun}')
            if zon:
                candidates.append(f'{COL_ZONA}_{zon}')
                candidates.append(f'Zona_{zon}')
            if gen:
                candidates.append(f'{COL_GENERO}_{gen}')
                candidates.append(f'Genero_{gen}')
            if act:
                candidates.append(f'{COL_ACTOR}_{act}')
                candidates.append(f'Actor_vial_{act}')

            for val in candidates:
                if val in input_df.columns:
                    input_df.at[0, val] = 1

            pred = modelo.predict(input_df)[0]
            probs = modelo.predict_proba(input_df)[0]
            confianza = max(probs)

            color_alerta = verde if pred == 0 else rojo
            status_text = "RIESGO BAJO / CONTROLADO" if pred == 0 else "RIESGO ALTO / CRÍTICO"

            st.markdown(f"""
            <div style="background-color: #2D3748; padding: 35px; border-radius: 20px; border-left: 12px solid {color_alerta};">
                <h4 style="color: #CBD5E1; margin-bottom: 10px;">ESTADO DEL ESCENARIO:</h4>
                <h2 style="color: {color_alerta}; margin: 0;">{status_text}</h2>
                <hr style="border: 0.5px solid #4A5568; margin: 20px 0;">
                <p style="font-size: 22px; color: {azul}; font-weight: bold;">Confianza Estadística: {confianza:.2%}</p>
                <p style="font-size: 14px; color: #94A3B8;">*Resultado basado en patrones históricos de la Sabana de Occidente.</p>
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error en predicción: {e}")
    else:
        st.warning("⚠️ Modelo no disponible. Asegúrate de subir 'modelo_accidentes.pkl' al repositorio.")

st.write("---")

# --- ANÁLISIS VISUAL ESTRATÉGICO ---
st.subheader("📈 Análisis Geográfico y Demográfico")
g1, g2 = st.columns(2)

with g1:
    if COL_MUN:
        vc_mun = df[COL_MUN].value_counts().reset_index()
        vc_mun.columns = ['Municipio', 'N_Incidentes']
        fig_mun = px.bar(vc_mun,
                         x='Municipio', y='N_Incidentes',
                         title="Distribución de Siniestralidad por Municipio",
                         labels={'Municipio': 'Municipio', 'N_Incidentes': 'N° Incidentes'},
                         color_discrete_sequence=[azul])
        fig_mun.update_layout(paper_bgcolor=fondo, plot_bgcolor=fondo,
                              font_color="white", title_font_color=azul)
        st.plotly_chart(fig_mun, use_container_width=True)
    else:
        st.info("Columna de Municipio no detectada.")

with g2:
    if COL_EDAD:
        fig_edad = px.histogram(df, x=COL_EDAD,
                                title="Perfil de Edad de los Involucrados",
                                labels={COL_EDAD: 'Rango de Edad', 'count': 'Frecuencia'},
                                color_discrete_sequence=[naranja], nbins=30)
        fig_edad.update_layout(paper_bgcolor=fondo, plot_bgcolor=fondo,
                               font_color="white", title_font_color=naranja, bargap=0.1)
        st.plotly_chart(fig_edad, use_container_width=True)
    else:
        st.info("Columna de Edad no detectada.")

# --- FOOTER ESTRATÉGICO ---
st.markdown(f"""
<br><hr>
<div style="text-align: center; color: #64748B; font-size: 14px;">
    <b>Estrategia de Seguridad Vial Sabana Occidente</b><br>
    Desarrollado por Senior Data Scientist • 2026
</div>
""", unsafe_allow_html=True)
