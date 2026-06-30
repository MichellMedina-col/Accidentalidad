import streamlit as st
import streamlit.components.v1 as components
import os

# 1. Configurar la página de Streamlit en modo ancho y ocultar márgenes nativos
st.set_page_config(page_title="Seguridad Vial - SENA", layout="wide", initial_sidebar_state="collapsed")

# Ocultar por completo la barra superior de Streamlit y el menú lateral para que solo se vea nuestro diseño
ocultar_elementos_streamlit = """
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    div[data-testid="stSidebarCollapse"] {display: none !important;}
    .block-container {padding-top: 0rem !important; padding-bottom: 0rem !important; padding-left: 0rem !important; padding-right: 0rem !important;}
</style>
"""
st.markdown(ocultar_elementos_streamlit, unsafe_allow_html=True)

# 2. Cargar y proyectar nuestro archivo HTML como la app principal
archivo_html = "analisis_accidentalidad.html"

if os.path.exists(archivo_html):
    with open(archivo_html, "r", encoding="utf-8") as f:
        contenido_html = f.read()
    
    # Proyectar el HTML en pantalla completa sin bordes nativos
    components.html(contenido_html, height=2000, scrolling=True)
else:
    st.error(f" Error: No se encontró el archivo '{archivo_html}' en la raíz del repositorio.")
