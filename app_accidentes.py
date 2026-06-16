import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go

# ─── CONFIGURACIÓN ────────────────────────────────────────────
st.set_page_config(
    page_title="Seguridad Vial · Sabana Occidente",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── TOKENS DE DISEÑO ─────────────────────────────────────────
BG_BASE    = "#0B1120"
BG_CARD    = "#111827"
BG_CARD2   = "#1a2236"
BORDER     = "#1E2D45"
ACCENT     = "#3B82F6"
ACCENT2    = "#6366F1"
SUCCESS    = "#10B981"
WARNING    = "#F59E0B"
DANGER     = "#EF4444"
TEXT_PRI   = "#F1F5F9"
TEXT_SEC   = "#94A3B8"
TEXT_MUT   = "#475569"

# ─── CSS PREMIUM ──────────────────────────────────────────────
st.markdown(f"""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
/* ── Reset global ── */
*, *::before, *::after {{ box-sizing: border-box; }}

html, body, .stApp, [data-testid="stAppViewContainer"] {{
    background-color: {BG_BASE} !important;
    font-family: 'Inter', sans-serif;
    color: {TEXT_PRI};
}}

/* ── Sidebar ── */
[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, #0d1526 0%, #0B1120 100%) !important;
    border-right: 1px solid {BORDER} !important;
}}
[data-testid="stSidebar"] * {{ color: {TEXT_PRI} !important; }}
[data-testid="stSidebarNav"] {{ display: none; }}

/* ── Ocultar toolbar de Streamlit ── */
[data-testid="stToolbar"], header {{ visibility: hidden; }}
#MainMenu {{ visibility: hidden; }}
footer {{ display: none !important; }}

/* ── Scrollbar ── */
::-webkit-scrollbar {{ width: 6px; }}
::-webkit-scrollbar-track {{ background: {BG_BASE}; }}
::-webkit-scrollbar-thumb {{ background: {BORDER}; border-radius: 3px; }}

/* ── Inputs & Selectbox ── */
[data-testid="stSelectbox"] > div > div,
[data-testid="stSlider"] {{
    background: {BG_CARD2} !important;
    border-radius: 10px;
}}
.stSelectbox label, .stSlider label {{
    color: {TEXT_SEC} !important;
    font-size: 12px !important;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}}
[data-baseweb="select"] > div {{
    background: {BG_CARD2} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 10px !important;
    color: {TEXT_PRI} !important;
}}

/* ── Botón ── */
.stButton > button {{
    background: linear-gradient(135deg, {ACCENT}, {ACCENT2});
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: 600;
    padding: 0.6rem 1.5rem;
    width: 100%;
    transition: all 0.2s ease;
    font-family: 'Inter', sans-serif;
}}
.stButton > button:hover {{
    transform: translateY(-1px);
    box-shadow: 0 8px 20px rgba(59,130,246,0.35);
}}

/* ── Métricas ── */
[data-testid="stMetricValue"] {{
    font-size: 2rem !important;
    font-weight: 700 !important;
    color: {TEXT_PRI} !important;
}}
[data-testid="stMetricLabel"] {{
    color: {TEXT_SEC} !important;
    font-size: 0.78rem !important;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}}
[data-testid="stMetricDelta"] {{ font-size: 0.82rem !important; }}

/* ── Expander ── */
[data-testid="stExpander"] {{
    background: {BG_CARD} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 12px !important;
}}

/* ── Alertas ── */
[data-testid="stAlert"] {{
    background: {BG_CARD2} !important;
    border-radius: 12px !important;
    border-left: 4px solid {ACCENT} !important;
}}

/* ── Separadores ── */
hr {{ border-color: {BORDER} !important; }}

/* ── Tarjetas custom ── */
.kpi-card {{
    background: {BG_CARD};
    border: 1px solid {BORDER};
    border-radius: 16px;
    padding: 24px 28px;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}}
.kpi-card:hover {{
    transform: translateY(-2px);
    box-shadow: 0 12px 32px rgba(0,0,0,0.4);
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
    font-size: 11px;
    font-weight: 600;
    color: {TEXT_MUT};
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 8px;
}}
.kpi-value {{
    font-size: 2.2rem;
    font-weight: 700;
    color: {TEXT_PRI};
    line-height: 1;
    margin-bottom: 6px;
}}
.kpi-sub {{
    font-size: 13px;
    color: {TEXT_SEC};
}}
.kpi-icon {{
    position: absolute;
    top: 20px; right: 20px;
    font-size: 28px;
    opacity: 0.25;
}}

.section-title {{
    font-size: 1.1rem;
    font-weight: 600;
    color: {TEXT_PRI};
    margin-bottom: 4px;
}}
.section-sub {{
    font-size: 0.82rem;
    color: {TEXT_SEC};
    margin-bottom: 20px;
}}

.chart-card {{
    background: {BG_CARD};
    border: 1px solid {BORDER};
    border-radius: 16px;
    padding: 20px;
}}

.predictor-card {{
    background: {BG_CARD};
    border: 1px solid {BORDER};
    border-radius: 16px;
    padding: 28px;
    height: 100%;
}}

.result-badge {{
    border-radius: 16px;
    padding: 28px 24px;
    text-align: center;
    margin-top: 16px;
}}

/* ── Sidebar nav items ── */
.nav-item {{
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 14px;
    border-radius: 10px;
    cursor: pointer;
    font-size: 14px;
    font-weight: 500;
    color: {TEXT_SEC};
    transition: all 0.15s ease;
    margin-bottom: 4px;
}}
.nav-item.active {{
    background: rgba(59,130,246,0.15);
    color: {ACCENT};
    border: 1px solid rgba(59,130,246,0.2);
}}
.nav-item:hover {{ background: rgba(255,255,255,0.04); color: {TEXT_PRI}; }}

.divider-label {{
    font-size: 10px;
    font-weight: 600;
    color: {TEXT_MUT};
    text-transform: uppercase;
    letter-spacing: 0.12em;
    padding: 16px 14px 6px;
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

def plotly_dark_layout(fig, title_color=ACCENT):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color=TEXT_SEC),
        title_font=dict(color=title_color, size=14, family="Inter"),
        margin=dict(l=10, r=10, t=40, b=10),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            bordercolor=BORDER,
            font=dict(color=TEXT_SEC)
        ),
        xaxis=dict(
            gridcolor=BORDER,
            linecolor=BORDER,
            tickfont=dict(color=TEXT_MUT)
        ),
        yaxis=dict(
            gridcolor=BORDER,
            linecolor=BORDER,
            tickfont=dict(color=TEXT_MUT)
        ),
    )
    return fig


# ─── CARGA DE DATOS ───────────────────────────────────────────
@st.cache_data
def load_clean_data():
    try:
        df = pd.read_csv('transito_sabana_occidente.csv', sep=None, engine='python')
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

df   = load_clean_data()
modelo = load_trained_model()

if df is None:
    st.error("🚨 No se encontró 'transito_sabana_occidente.csv'.")
    st.stop()

# Detectar columnas
COL_EDAD   = find_col(df, 'edad', 'age')
COL_MUN    = find_col(df, 'municipio', 'ciudad', 'municipality')
COL_ZONA   = find_col(df, 'zona', 'zone', 'area')
COL_GENERO = find_col(df, 'genero', 'sexo', 'gender', 'sex')
COL_ACTOR  = find_col(df, 'actor_vial', 'actor', 'tipo_actor', 'clase_actor', 'victima', 'rol')
COL_FECHA  = find_col(df, 'fecha', 'date', 'año', 'anio', 'year')
COL_GRAVE  = find_col(df, 'gravedad', 'severity', 'clase', 'tipo_accidente')


# ═══════════════════════════════════════════════════════════════
#  SIDEBAR
# ═══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown(f"""
    <div style="padding: 20px 14px 24px;">
        <div style="display:flex; align-items:center; gap:10px; margin-bottom:6px;">
            <div style="width:36px; height:36px; border-radius:10px;
                        background: linear-gradient(135deg,{ACCENT},{ACCENT2});
                        display:flex; align-items:center; justify-content:center; font-size:18px;">
                🛡️
            </div>
            <div>
                <div style="font-weight:700; font-size:15px; color:{TEXT_PRI};">VialAnalytics</div>
                <div style="font-size:11px; color:{TEXT_MUT};">Sabana Occidente</div>
            </div>
        </div>
    </div>
    <div class="divider-label">Navegación</div>
    <div class="nav-item active">📊 &nbsp; Dashboard General</div>
    <div class="nav-item">🔮 &nbsp; Predictor de Riesgo</div>
    <div class="nav-item">📈 &nbsp; Análisis Visual</div>
    <div class="divider-label" style="margin-top:16px;">Datos</div>
    <div class="nav-item">📁 &nbsp; Dataset</div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Filtro de municipio en sidebar
    if COL_MUN:
        opciones_mun = ["Todos"] + sorted(df[COL_MUN].dropna().unique().tolist())
        filtro_mun = st.selectbox("Filtrar por municipio", opciones_mun)
        if filtro_mun != "Todos":
            df = df[df[COL_MUN] == filtro_mun]

    st.markdown(f"""
    <div style="position:absolute; bottom:20px; left:0; right:0; padding:0 14px;">
        <div style="background:{BG_CARD2}; border:1px solid {BORDER}; border-radius:12px; padding:14px;">
            <div style="font-size:11px; color:{TEXT_MUT}; margin-bottom:4px;">Total registros</div>
            <div style="font-size:22px; font-weight:700; color:{ACCENT};">{len(df):,}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
#  ENCABEZADO
# ═══════════════════════════════════════════════════════════════
st.markdown(f"""
<div style="padding: 8px 0 28px;">
    <h1 style="font-size:1.9rem; font-weight:700; color:{TEXT_PRI}; margin:0 0 6px;">
        Centro de Inteligencia de Seguridad Vial
    </h1>
    <p style="color:{TEXT_SEC}; font-size:0.95rem; margin:0;">
        Análisis de accidentalidad · Funza &nbsp;•&nbsp; Mosquera &nbsp;•&nbsp; Facatativá &nbsp;•&nbsp; Madrid
    </p>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
#  KPI CARDS
# ═══════════════════════════════════════════════════════════════
k1, k2, k3, k4 = st.columns(4)

val_edad  = f"{df[COL_EDAD].mean():.1f} años" if COL_EDAD else "N/D"
val_mun   = df[COL_MUN].mode()[0]             if COL_MUN  else "N/D"
val_actor = df[COL_ACTOR].mode()[0]           if COL_ACTOR else "N/D"

with k1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon">🚨</div>
        <div class="kpi-label">Incidentes registrados</div>
        <div class="kpi-value">{len(df):,}</div>
        <div class="kpi-sub" style="color:{SUCCESS};">● Dataset activo</div>
    </div>""", unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon">🎂</div>
        <div class="kpi-label">Edad media crítica</div>
        <div class="kpi-value">{val_edad}</div>
        <div class="kpi-sub">Promedio de involucrados</div>
    </div>""", unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon">📍</div>
        <div class="kpi-label">Mayor siniestralidad</div>
        <div class="kpi-value" style="font-size:1.5rem;">{val_mun}</div>
        <div class="kpi-sub">Municipio de mayor riesgo</div>
    </div>""", unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon">🚶</div>
        <div class="kpi-label">Actor más vulnerable</div>
        <div class="kpi-value" style="font-size:1.4rem;">{val_actor}</div>
        <div class="kpi-sub">Tipo de actor vial</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
#  FILA 2: GRÁFICAS PRINCIPALES
# ═══════════════════════════════════════════════════════════════
ch1, ch2 = st.columns([1.4, 1])

with ch1:
    st.markdown(f"""
    <div class="section-title">📈 Distribución por Municipio</div>
    <div class="section-sub">Cantidad de incidentes registrados por localidad</div>
    """, unsafe_allow_html=True)

    if COL_MUN:
        vc = df[COL_MUN].value_counts().reset_index()
        vc.columns = ['Municipio', 'Incidentes']
        fig = go.Figure(go.Bar(
            x=vc['Municipio'], y=vc['Incidentes'],
            marker=dict(
                color=vc['Incidentes'],
                colorscale=[[0, "#1E3A5F"], [0.5, ACCENT], [1, ACCENT2]],
                line=dict(width=0)
            ),
            hovertemplate="<b>%{x}</b><br>Incidentes: %{y:,}<extra></extra>"
        ))
        fig = plotly_dark_layout(fig)
        fig.update_layout(showlegend=False, height=300)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    else:
        st.info("Columna de municipio no detectada.")

with ch2:
    st.markdown(f"""
    <div class="section-title">📊 Perfil de Edad</div>
    <div class="section-sub">Distribución de edades de los involucrados</div>
    """, unsafe_allow_html=True)

    if COL_EDAD:
        edad_vals = df[COL_EDAD].dropna()
        fig2 = go.Figure()
        fig2.add_trace(go.Histogram(
            x=edad_vals,
            nbinsx=25,
            marker=dict(
                color=ACCENT,
                opacity=0.85,
                line=dict(width=0)
            ),
            hovertemplate="Rango: %{x}<br>Frecuencia: %{y}<extra></extra>"
        ))
        # Área con gradiente simulado
        counts, bins = np.histogram(edad_vals, bins=25)
        bin_centers = (bins[:-1] + bins[1:]) / 2
        fig2.add_trace(go.Scatter(
            x=bin_centers, y=counts,
            fill='tozeroy',
            fillcolor=f"rgba(99,102,241,0.15)",
            line=dict(color=ACCENT2, width=2),
            hoverinfo='skip'
        ))
        fig2 = plotly_dark_layout(fig2)
        fig2.update_layout(showlegend=False, height=300, barmode='overlay')
        st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})
    else:
        st.info("Columna de edad no detectada.")


# ═══════════════════════════════════════════════════════════════
#  FILA 3: ACTOR VIAL + GÉNERO
# ═══════════════════════════════════════════════════════════════
ch3, ch4 = st.columns(2)

with ch3:
    st.markdown(f"""
    <div class="section-title">🚗 Actores Viales</div>
    <div class="section-sub">Participación por tipo de actor</div>
    """, unsafe_allow_html=True)

    if COL_ACTOR:
        vc_actor = df[COL_ACTOR].value_counts().head(8).reset_index()
        vc_actor.columns = ['Actor', 'Cantidad']
        fig3 = go.Figure(go.Bar(
            x=vc_actor['Cantidad'], y=vc_actor['Actor'],
            orientation='h',
            marker=dict(
                color=vc_actor['Cantidad'],
                colorscale=[[0, "#1a2236"], [1, SUCCESS]],
                line=dict(width=0)
            ),
            hovertemplate="<b>%{y}</b>: %{x:,}<extra></extra>"
        ))
        fig3 = plotly_dark_layout(fig3)
        fig3.update_layout(showlegend=False, height=300,
                           yaxis=dict(autorange='reversed'))
        st.plotly_chart(fig3, use_container_width=True, config={'displayModeBar': False})

with ch4:
    st.markdown(f"""
    <div class="section-title">⚧ Distribución por Género</div>
    <div class="section-sub">Proporción de involucrados</div>
    """, unsafe_allow_html=True)

    if COL_GENERO:
        vc_gen = df[COL_GENERO].value_counts().reset_index()
        vc_gen.columns = ['Genero', 'Cantidad']
        fig4 = go.Figure(go.Pie(
            labels=vc_gen['Genero'],
            values=vc_gen['Cantidad'],
            hole=0.6,
            marker=dict(
                colors=[ACCENT, ACCENT2, SUCCESS, WARNING, DANGER],
                line=dict(color=BG_BASE, width=3)
            ),
            hovertemplate="<b>%{label}</b><br>%{value:,} casos (%{percent})<extra></extra>"
        ))
        fig4 = plotly_dark_layout(fig4)
        fig4.update_layout(
            showlegend=True, height=300,
            legend=dict(orientation="v", x=1, y=0.5)
        )
        st.plotly_chart(fig4, use_container_width=True, config={'displayModeBar': False})
    else:
        st.info("Columna de género no detectada.")


# ═══════════════════════════════════════════════════════════════
#  PREDICTOR DE RIESGO
# ═══════════════════════════════════════════════════════════════
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(f"""
<div style="display:flex; align-items:center; gap:10px; margin-bottom:20px;">
    <div style="width:4px; height:28px; background:linear-gradient(180deg,{ACCENT},{ACCENT2}); border-radius:2px;"></div>
    <div>
        <div style="font-size:1.15rem; font-weight:600; color:{TEXT_PRI};">Predictor de Escenario de Riesgo</div>
        <div style="font-size:0.82rem; color:{TEXT_SEC};">Configura los parámetros del actor vial para obtener una predicción</div>
    </div>
</div>
""", unsafe_allow_html=True)

p1, p2 = st.columns([1, 1.1])

with p1:
    st.markdown(f'<div style="background:{BG_CARD}; border:1px solid {BORDER}; border-radius:16px; padding:24px;">', unsafe_allow_html=True)
    st.markdown(f'<div style="font-size:13px; font-weight:600; color:{TEXT_SEC}; text-transform:uppercase; letter-spacing:.08em; margin-bottom:20px;">⚙️ Parámetros del escenario</div>', unsafe_allow_html=True)

    edad = st.slider("Edad del actor vial", 0, 100, 30)
    mun  = st.selectbox("Municipio", sorted(df[COL_MUN].dropna().unique())) if COL_MUN else None
    zon  = st.selectbox("Zona del incidente", sorted(df[COL_ZONA].dropna().unique())) if COL_ZONA else None
    gen  = st.selectbox("Género", sorted(df[COL_GENERO].dropna().unique())) if COL_GENERO else None
    act  = st.selectbox("Tipo de actor vial", sorted(df[COL_ACTOR].dropna().unique())) if COL_ACTOR else None

    st.markdown("</div>", unsafe_allow_html=True)

with p2:
    st.markdown(f'<div style="background:{BG_CARD}; border:1px solid {BORDER}; border-radius:16px; padding:24px; min-height:380px;">', unsafe_allow_html=True)
    st.markdown(f'<div style="font-size:13px; font-weight:600; color:{TEXT_SEC}; text-transform:uppercase; letter-spacing:.08em; margin-bottom:20px;">🔮 Resultado del análisis</div>', unsafe_allow_html=True)

    if modelo is not None:
        try:
            cols_mod  = list(modelo.feature_names_in_)
            input_df  = pd.DataFrame(0, index=[0], columns=cols_mod)

            for possible in ['edad', 'Edad', 'age']:
                if possible in input_df.columns:
                    input_df.at[0, possible] = edad
                    break

            candidates = []
            if mun: candidates += [f'{COL_MUN}_{mun}', f'municipio_{mun}']
            if zon: candidates += [f'{COL_ZONA}_{zon}', f'zona_{zon}']
            if gen: candidates += [f'{COL_GENERO}_{gen}', f'genero_{gen}']
            if act: candidates += [f'{COL_ACTOR}_{act}', f'actor_vial_{act}']
            for val in candidates:
                if val in input_df.columns:
                    input_df.at[0, val] = 1

            pred      = modelo.predict(input_df)[0]
            probs     = modelo.predict_proba(input_df)[0]
            confianza = max(probs)

            is_danger = pred != 0
            color_res = DANGER  if is_danger else SUCCESS
            icon_res  = "🔴"    if is_danger else "🟢"
            label_res = "RIESGO ALTO · CRÍTICO" if is_danger else "RIESGO BAJO · CONTROLADO"
            bg_res    = "rgba(239,68,68,0.08)"  if is_danger else "rgba(16,185,129,0.08)"

            # Gauge de confianza
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=round(confianza * 100, 1),
                number=dict(suffix="%", font=dict(size=28, color=TEXT_PRI, family="Inter")),
                gauge=dict(
                    axis=dict(range=[0, 100], tickcolor=TEXT_MUT,
                              tickfont=dict(color=TEXT_MUT)),
                    bar=dict(color=color_res, thickness=0.25),
                    bgcolor="rgba(0,0,0,0)",
                    bordercolor=BORDER,
                    steps=[
                        dict(range=[0, 50],  color="rgba(16,185,129,0.08)"),
                        dict(range=[50, 75], color="rgba(245,158,11,0.08)"),
                        dict(range=[75, 100],color="rgba(239,68,68,0.08)")
                    ],
                    threshold=dict(line=dict(color=color_res, width=3), value=confianza*100)
                )
            ))
            fig_gauge.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter", color=TEXT_SEC),
                height=200, margin=dict(l=20, r=20, t=20, b=0)
            )
            st.plotly_chart(fig_gauge, use_container_width=True, config={'displayModeBar': False})

            st.markdown(f"""
            <div style="background:{bg_res}; border:1px solid {color_res}40;
                        border-radius:14px; padding:20px; text-align:center; margin-top:8px;">
                <div style="font-size:24px; margin-bottom:8px;">{icon_res}</div>
                <div style="font-size:1rem; font-weight:700; color:{color_res};
                            letter-spacing:0.04em;">{label_res}</div>
                <div style="font-size:12px; color:{TEXT_MUT}; margin-top:6px;">
                    Confianza estadística: <b style="color:{TEXT_SEC};">{confianza:.1%}</b>
                </div>
            </div>
            """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error en predicción: {e}")
    else:
        st.markdown(f"""
        <div style="text-align:center; padding:40px 20px;">
            <div style="font-size:40px; margin-bottom:12px;">📦</div>
            <div style="color:{TEXT_SEC}; font-size:14px;">
                Modelo no disponible.<br>
                Sube <code>modelo_accidentes.pkl</code> al repositorio.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
#  FOOTER
# ═══════════════════════════════════════════════════════════════
st.markdown(f"""
<br>
<div style="border-top:1px solid {BORDER}; padding:20px 0; text-align:center;">
    <span style="color:{TEXT_MUT}; font-size:12px;">
        🛡️ &nbsp; VialAnalytics · Estrategia de Seguridad Vial Sabana Occidente &nbsp;·&nbsp;
        Desarrollado con Streamlit &nbsp;·&nbsp; 2026
    </span>
</div>
""", unsafe_allow_html=True)

# ─── DIAGNÓSTICO DE COLUMNAS (al final para no interrumpir) ───
cols_faltantes = {k: v for k, v in {
    'Edad': COL_EDAD, 'Municipio': COL_MUN, 'Zona': COL_ZONA,
    'Género': COL_GENERO, 'Actor Vial': COL_ACTOR
}.items() if v is None}

if cols_faltantes:
    with st.expander("⚠️ Diagnóstico de columnas"):
        st.warning(f"No detectadas: **{', '.join(cols_faltantes.keys())}**")
        st.write("Columnas en el CSV:")
        st.code(str(list(df.columns)))
