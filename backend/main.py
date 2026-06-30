import os
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="VialAnalytics API")

# Permitir CORS para el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, limita esto al dominio real
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cargar el modelo
try:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    MODEL_PATH = os.path.join(BASE_DIR, 'modelo_accidentes.pkl')
    modelo = joblib.load(MODEL_PATH)
    feature_names = list(modelo.feature_names_in_)
except Exception as e:
    modelo = None
    feature_names = []
    print(f"Error loading model: {e}")

# Modelo de datos de entrada
class PredictionRequest(BaseModel):
    edad: int
    municipio: str
    zona: str
    genero: str
    actor: str

@app.get("/api/stats")
def get_stats():
    # Retorna estadisticas globales (harcodeadas como ejemplo, o puedes leer el CSV real aquí)
    return {
        "kpi_incidentes": "12,450",
        "kpi_edad": "34.5",
        "kpi_mun": "Facatativá",
        "kpi_actor": "Motociclista"
    }

@app.post("/api/predict")
def predict_risk(req: PredictionRequest):
    if modelo is None:
        raise HTTPException(status_code=500, detail="Modelo no disponible")
    
    # Crear dataframe con ceros para las features del modelo
    inp = pd.DataFrame(0, index=[0], columns=feature_names)
    
    # 1. Asignar Edad
    for col in ['Edad', 'edad', 'age']:
        if col in inp.columns:
            inp.at[0, col] = req.edad
            break
            
    # Función auxiliar para mapear el feature
    def set_feature(prefix, val):
        if not val:
            return
        val_norm = str(val).lower()
        for c, r in [('á','a'), ('é','e'), ('í','i'), ('ó','o'), ('ú','u'), ('ñ','n')]:
            val_norm = val_norm.replace(c, r)
            
        for col in inp.columns:
            col_clean = col.replace('Facatativ', 'Facatativa').replace('informacin', 'informacion')
            col_norm = col_clean.lower()
            for c, r in [('á','a'), ('é','e'), ('í','i'), ('ó','o'), ('ú','u'), ('ñ','n')]:
                col_norm = col_norm.replace(c, r)
                
            if col_norm.startswith(f"{prefix.lower()}_"):
                feat_val = col_norm[len(prefix.lower())+1:]
                if feat_val == val_norm or val_norm in feat_val or feat_val in val_norm:
                    inp.at[0, col] = 1
                    return

    # Mapear selecciones
    set_feature('Municipio', req.municipio)
    set_feature('Zona', req.zona)
    set_feature('Genero', req.genero)
    
    # Mapear actor a armas
    arma_val = 'No Reportado'
    if req.actor:
        act_lower = req.actor.lower()
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
    if req.edad < 12:
        grupo_val = 'Menores'
    elif req.edad < 18:
        grupo_val = 'Adolescentes'
    else:
        grupo_val = 'Adultos'
    set_feature('Grupo_etario', grupo_val)
    
    # Realizar predicción
    probs = modelo.predict_proba(inp)[0]
    conf = max(probs)
    riesgo_pct = round(conf * 100, 1)
    
    # Logica de color según riesgo (Escala Azul Tecnológica por defecto)
    if riesgo_pct < 50:
        color = "#00D2FF" # Azul Celeste
        label = "RIESGO BAJO - CONTROLADO"
    elif riesgo_pct < 70:
        color = "#0078FF" # Azul Eléctrico
        label = "RIESGO MEDIO - PRECAUCIÓN"
    else:
        color = "#7000FF" # Violeta/Neón Profundo
        label = "RIESGO ALTO - CRÍTICO"

    return {
        "riesgo_pct": riesgo_pct,
        "color": color,
        "label": label
    }

# Para iniciar servidor: uvicorn backend.main:app --reload
