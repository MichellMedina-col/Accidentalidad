export interface DecisionNode {
  f?: number; // feature index
  t?: number; // threshold
  l?: DecisionNode; // left child
  r?: DecisionNode; // right child
  v?: number[]; // leaf values (probabilities)
}

export interface ModelData {
  features: string[];
  classes: string[];
  trees: DecisionNode[];
}

export interface PredictorInput {
  edad: number;
  municipio: string;
  zona: string;
  genero: string;
  actor: string;
}

export interface PredictionResult {
  riesgoPct: number;
  classProbabilities: { [className: string]: number };
  predictedClass: string;
  riesgoLabel: string;
  riesgoColor: string; // Text color code
  riesgoBg: string; // Background styling
  riesgoBorder: string; // Border style
  riesgoIcon: string;
}

function evaluateNode(node: DecisionNode, x: number[]): number[] {
  if (node.v !== undefined) {
    return node.v;
  }
  const val = x[node.f!];
  if (val <= node.t!) {
    return evaluateNode(node.l!, x);
  } else {
    return evaluateNode(node.r!, x);
  }
}

export function predictRisk(model: ModelData, input: PredictorInput): PredictionResult {
  // Construct feature vector based on model features
  // Feature order:
  // 0: Edad
  // 1: Municipio_Facatativá
  // 2: Municipio_Funza
  // 3: Municipio_Madrid
  // 4: Municipio_Mosquera
  // 5: Genero_Femenino
  // 6: Genero_Masculino
  // 7: Genero_No Reportado
  // 8: Zona_No Reportado
  // 9: Zona_Rural
  // 10: Zona_Sin información
  // 11: Zona_Urbana
  // 12: Armas_medios_Bicicleta
  // 13: Armas_medios_Moto
  // 14: Armas_medios_No Reportado
  // 15: Armas_medios_Sin empleo de armas
  // 16: Armas_medios_Tren
  // 17: Armas_medios_Vehiculo
  // 18: Grupo_etario_Adolescentes
  // 19: Grupo_etario_Adultos
  // 20: Grupo_etario_Menores
  // 21: Grupo_etario_No Reportado

  const x = new Array(model.features.length).fill(0);
  
  // Set Age
  const edadIndex = model.features.indexOf("Edad");
  if (edadIndex !== -1) {
    x[edadIndex] = input.edad;
  }

  // Set Municipio
  const munFeatureName = `Municipio_${input.municipio}`;
  const munIndex = model.features.indexOf(munFeatureName);
  if (munIndex !== -1) {
    x[munIndex] = 1;
  }

  // Set Genero
  const genFeatureName = `Genero_${input.genero}`;
  const genIndex = model.features.indexOf(genFeatureName);
  if (genIndex !== -1) {
    x[genIndex] = 1;
  }

  // Set Zona
  const zonFeatureName = `Zona_${input.zona}`;
  const zonIndex = model.features.indexOf(zonFeatureName);
  if (zonIndex !== -1) {
    x[zonIndex] = 1;
  }

  // Map Actor Vial to Armas_medios_
  // 'Usuario de moto' -> Armas_medios_Moto
  // 'Usuario de bicicleta' -> Armas_medios_Bicicleta
  // 'Usuario de vehículo' -> Armas_medios_Vehiculo
  // 'Peatón' -> Armas_medios_Sin empleo de armas
  // Other / Sin información / No Reportado -> Armas_medios_No Reportado
  let armaMedio = "No Reportado";
  if (input.actor === "Usuario de moto") armaMedio = "Moto";
  else if (input.actor === "Usuario de bicicleta") armaMedio = "Bicicleta";
  else if (input.actor === "Usuario de vehículo") armaMedio = "Vehiculo";
  else if (input.actor === "Peatón") armaMedio = "Sin empleo de armas";

  const armaFeatureName = `Armas_medios_${armaMedio}`;
  const armaIndex = model.features.indexOf(armaFeatureName);
  if (armaIndex !== -1) {
    x[armaIndex] = 1;
  }

  // Set Grupo etario
  let grupoEtario = "No Reportado";
  if (input.edad < 12) grupoEtario = "Menores";
  else if (input.edad >= 12 && input.edad < 18) grupoEtario = "Adolescentes";
  else if (input.edad >= 18) grupoEtario = "Adultos";

  const grupoFeatureName = `Grupo_etario_${grupoEtario}`;
  const grupoIndex = model.features.indexOf(grupoFeatureName);
  if (grupoIndex !== -1) {
    x[grupoIndex] = 1;
  }

  // Predict
  const nClasses = model.classes.length;
  const sumProbs = new Array(nClasses).fill(0);
  
  for (const tree of model.trees) {
    const probs = evaluateNode(tree, x);
    for (let i = 0; i < probs.length; i++) {
      sumProbs[i] += probs[i];
    }
  }

  // Average probabilities
  const avgProbs = sumProbs.map(v => v / model.trees.length);

  // Find class with highest probability
  let maxIdx = 0;
  for (let i = 1; i < avgProbs.length; i++) {
    if (avgProbs[i] > avgProbs[maxIdx]) {
      maxIdx = i;
    }
  }

  const predictedClass = model.classes[maxIdx];
  const conf = avgProbs[maxIdx];
  const riesgoPct = Math.round(conf * 1000) / 10; // 1 decimal place

  // Map probabilities back to classes
  const classProbabilities: { [key: string]: number } = {};
  for (let i = 0; i < nClasses; i++) {
    classProbabilities[model.classes[i]] = avgProbs[i];
  }

  // Neon color stops for risk gradient (hand-picked for maximum glow effect)
  // 0%   → #00FF88 (neon green)
  // 25%  → #66FF00 (neon lime)
  // 40%  → #FFFF00 (neon yellow)
  // 55%  → #FF8800 (neon orange)
  // 75%  → #FF4400 (neon red-orange)
  // 100% → #FF0044 (neon red)
  type ColorStop = { pct: number; r: number; g: number; b: number };

  const neonStops: ColorStop[] = [
    { pct: 0,   r: 0,   g: 255, b: 136 },  // #00FF88 neon green
    { pct: 25,  r: 102, g: 255, b: 0   },  // #66FF00 neon lime
    { pct: 40,  r: 255, g: 255, b: 0   },  // #FFFF00 neon yellow
    { pct: 55,  r: 255, g: 136, b: 0   },  // #FF8800 neon orange
    { pct: 75,  r: 255, g: 68,  b: 0   },  // #FF4400 neon red-orange
    { pct: 100, r: 255, g: 0,   b: 68  },  // #FF0044 neon red/magenta
  ];

  function interpolateNeonColor(pct: number): { r: number; g: number; b: number } {
    const clamped = Math.max(0, Math.min(100, pct));
    // Find the two stops to interpolate between
    let lower = neonStops[0];
    let upper = neonStops[neonStops.length - 1];
    for (let i = 0; i < neonStops.length - 1; i++) {
      if (clamped >= neonStops[i].pct && clamped <= neonStops[i + 1].pct) {
        lower = neonStops[i];
        upper = neonStops[i + 1];
        break;
      }
    }
    const range = upper.pct - lower.pct || 1;
    const t = (clamped - lower.pct) / range;
    return {
      r: Math.round(lower.r + (upper.r - lower.r) * t),
      g: Math.round(lower.g + (upper.g - lower.g) * t),
      b: Math.round(lower.b + (upper.b - lower.b) * t),
    };
  }

  function getRiskColor(pct: number): string {
    const { r, g, b } = interpolateNeonColor(pct);
    return `rgb(${r}, ${g}, ${b})`;
  }

  function getRiskColorAlpha(pct: number, alpha: number): string {
    const { r, g, b } = interpolateNeonColor(pct);
    return `rgba(${r}, ${g}, ${b}, ${alpha})`;
  }

  const riesgoColor = getRiskColor(riesgoPct);
  const riesgoBg = getRiskColorAlpha(riesgoPct, 0.10);
  const riesgoBorder = getRiskColorAlpha(riesgoPct, 0.4);

  // Determine risk level label and icon based on thresholds
  let riesgoLabel = "RIESGO BAJO • CONTROLADO";
  let riesgoIcon = "🟢";

  if (riesgoPct > 30 && riesgoPct <= 50) {
    riesgoLabel = "RIESGO MODERADO • PRECAUCIÓN";
    riesgoIcon = "🟡";
  } else if (riesgoPct > 50 && riesgoPct <= 70) {
    riesgoLabel = "RIESGO ALTO • PELIGRO";
    riesgoIcon = "🟠";
  } else if (riesgoPct > 70) {
    riesgoLabel = "RIESGO CRÍTICO • EMERGENCIA";
    riesgoIcon = "🔴";
  }

  return {
    riesgoPct,
    classProbabilities,
    predictedClass,
    riesgoLabel,
    riesgoColor,
    riesgoBg,
    riesgoBorder,
    riesgoIcon
  };
}
