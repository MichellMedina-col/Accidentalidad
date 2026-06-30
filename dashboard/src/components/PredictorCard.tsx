import React, { useState, useEffect } from 'react';
import { ModelData, predictRisk, PredictorInput, PredictionResult } from '../utils/predictor';
import { Sliders, HelpCircle, Activity } from 'lucide-react';

interface PredictorCardProps {
  model: ModelData | null;
  loading: boolean;
}

export default function PredictorCard({ model, loading }: PredictorCardProps) {
  // 1. Setup default state for inputs
  const [edad, setEdad] = useState<number>(30);
  const [municipio, setMunicipio] = useState<string>('Funza');
  const [zona, setZona] = useState<string>('Urbana');
  const [genero, setGenero] = useState<string>('Masculino');
  const [actor, setActor] = useState<string>('Usuario de moto');

  // 2. State for results
  const [result, setResult] = useState<PredictionResult | null>(null);

  // Lists of options matching features
  const municipios = ['Facatativá', 'Funza', 'Madrid', 'Mosquera'];
  const zonas = ['Urbana', 'Rural', 'Sin información', 'No Reportado'];
  const generos = ['Masculino', 'Femenino', 'No Reportado'];
  const actores = [
    'Usuario de moto',
    'Usuario de bicicleta',
    'Peatón',
    'Usuario de vehículo',
    'Usuario otros',
    'Sin información',
    'No Reportado'
  ];

  // 3. Re-calculate prediction when inputs change
  useEffect(() => {
    if (model) {
      const input: PredictorInput = { edad, municipio, zona, genero, actor };
      const res = predictRisk(model, input);
      setResult(res);
    }
  }, [edad, municipio, zona, genero, actor, model]);

  return (
    <div className="bg-[#fcfcfd] dark:bg-[#12121e]/40 border border-[#ececf0] dark:border-[#1e2d45] rounded-3xl p-6 md:p-8 shadow-sm dark:shadow-[0_16px_48px_rgba(0,0,0,0.3)] backdrop-blur-sm relative overflow-hidden">
      {/* Glow decorative background */}
      <div className="absolute top-0 right-0 w-80 h-80 rounded-full bg-neon/5 blur-[80px] pointer-events-none"></div>
      
      <div className="flex items-center gap-3 mb-6 pb-4 border-b border-[#ececf0] dark:border-[#1e2d45]">
        <div className="w-1.5 h-6 rounded-full bg-gradient-to-b from-neon to-[#0099CC]"></div>
        <div>
          <h2 className="text-lg md:text-xl font-bold tracking-tight text-[#030213] dark:text-white flex items-center gap-2">
            <Sliders className="w-5 h-5 text-neon" />
            Predictor de Escenario de Riesgo
          </h2>
          <p className="text-xs text-[#717182] dark:text-[#94a3b8] mt-0.5">
            Configura los parámetros del actor vial para estimar el índice de severidad y riesgo.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-stretch">
        
        {/* LEFT COLUMN: Controls */}
        <div className="space-y-6">
          <div className="bg-white dark:bg-[#0d0d14] border border-[#ececf0] dark:border-[#1a2638] rounded-2xl p-5 md:p-6 space-y-5">
            <div className="flex justify-between items-center text-xs font-bold text-[#717182] dark:text-[#475569] uppercase tracking-wider">
              <span>⚙️ Parámetros del escenario</span>
              <span className="flex items-center gap-1 text-[10px] bg-slate-100 dark:bg-slate-800 text-slate-500 px-2 py-0.5 rounded">
                INPUTS
              </span>
            </div>

            {/* Edad Input (Slider) */}
            <div className="space-y-2">
              <div className="flex justify-between text-xs font-semibold uppercase tracking-wider text-[#717182] dark:text-[#94a3b8]">
                <span>Edad del Actor Vial</span>
                <span className="text-neon font-black text-sm">{edad} años</span>
              </div>
              <div className="relative flex items-center select-none">
                <input
                  type="range"
                  min="0"
                  max="100"
                  value={edad}
                  onChange={(e) => setEdad(parseInt(e.target.value))}
                  className="neon-slider w-full h-2 rounded-lg bg-slate-200 dark:bg-slate-800 cursor-pointer outline-none focus:ring-1 focus:ring-neon/30 focus:border-neon"
                  style={{
                    background: `linear-gradient(to right, #00D4FF 0%, #00D4FF ${edad}%, ${
                      document.documentElement.classList.contains('dark') ? '#1e293b' : '#cbd5e1'
                    } ${edad}%, ${
                      document.documentElement.classList.contains('dark') ? '#1e293b' : '#cbd5e1'
                    } 100%)`
                  }}
                />
              </div>
              <div className="flex justify-between text-[10px] text-slate-400 font-medium">
                <span>0 años</span>
                <span>50 años</span>
                <span>100 años</span>
              </div>
            </div>

            {/* Grid of selectors */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {/* Municipio Selector */}
              <div className="space-y-1.5">
                <label className="text-[10px] font-bold text-[#717182] dark:text-[#94a3b8] uppercase tracking-wider">
                  Municipio
                </label>
                <select
                  value={municipio}
                  onChange={(e) => setMunicipio(e.target.value)}
                  className="w-full bg-slate-50 dark:bg-[#12121e] border border-[#ececf0] dark:border-[#1e2d45] rounded-xl px-3 py-2.5 text-sm font-medium focus:border-neon focus:ring-2 focus:ring-neon-subtle outline-none transition-all cursor-pointer text-[#030213] dark:text-white"
                >
                  {municipios.map((m) => (
                    <option key={m} value={m} className="bg-white dark:bg-[#12121e]">
                      {m}
                    </option>
                  ))}
                </select>
              </div>

              {/* Zona Selector */}
              <div className="space-y-1.5">
                <label className="text-[10px] font-bold text-[#717182] dark:text-[#94a3b8] uppercase tracking-wider">
                  Zona del incidente
                </label>
                <select
                  value={zona}
                  onChange={(e) => setZona(e.target.value)}
                  className="w-full bg-slate-50 dark:bg-[#12121e] border border-[#ececf0] dark:border-[#1e2d45] rounded-xl px-3 py-2.5 text-sm font-medium focus:border-neon focus:ring-2 focus:ring-neon-subtle outline-none transition-all cursor-pointer text-[#030213] dark:text-white"
                >
                  {zonas.map((z) => (
                    <option key={z} value={z} className="bg-white dark:bg-[#12121e]">
                      {z}
                    </option>
                  ))}
                </select>
              </div>

              {/* Género Selector */}
              <div className="space-y-1.5">
                <label className="text-[10px] font-bold text-[#717182] dark:text-[#94a3b8] uppercase tracking-wider">
                  Género del actor
                </label>
                <select
                  value={genero}
                  onChange={(e) => setGenero(e.target.value)}
                  className="w-full bg-slate-50 dark:bg-[#12121e] border border-[#ececf0] dark:border-[#1e2d45] rounded-xl px-3 py-2.5 text-sm font-medium focus:border-neon focus:ring-2 focus:ring-neon-subtle outline-none transition-all cursor-pointer text-[#030213] dark:text-white"
                >
                  {generos.map((g) => (
                    <option key={g} value={g} className="bg-white dark:bg-[#12121e]">
                      {g}
                    </option>
                  ))}
                </select>
              </div>

              {/* Actor Vial Selector */}
              <div className="space-y-1.5">
                <label className="text-[10px] font-bold text-[#717182] dark:text-[#94a3b8] uppercase tracking-wider">
                  Tipo de actor vial
                </label>
                <select
                  value={actor}
                  onChange={(e) => setActor(e.target.value)}
                  className="w-full bg-slate-50 dark:bg-[#12121e] border border-[#ececf0] dark:border-[#1e2d45] rounded-xl px-3 py-2.5 text-sm font-medium focus:border-neon focus:ring-2 focus:ring-neon-subtle outline-none transition-all cursor-pointer text-[#030213] dark:text-white"
                >
                  {actores.map((a) => (
                    <option key={a} value={a} className="bg-white dark:bg-[#12121e]">
                      {a}
                    </option>
                  ))}
                </select>
              </div>
            </div>
          </div>
        </div>

        {/* RIGHT COLUMN: Results Display */}
        <div className="flex flex-col justify-between">
          <div className="bg-[#0c1220] rounded-2xl p-6 flex flex-col items-center justify-center text-center h-full min-h-[420px] relative overflow-hidden shadow-lg border border-[#1a2540]">

            <span className="text-[10px] text-[#5a6a80] uppercase font-bold tracking-widest block absolute top-5 left-5">
              🔮 Resultado del análisis
            </span>

            {loading ? (
              <div className="space-y-3">
                <div className="w-12 h-12 rounded-full border-4 border-[#1a2540] border-t-neon animate-spin"></div>
                <p className="text-xs text-[#5a6a80] font-semibold uppercase tracking-wider">Cargando Modelo...</p>
              </div>
            ) : model && result ? (
              <div className="space-y-6 w-full flex flex-col items-center justify-center pt-8">
                
                {/* TWO SEMI-CIRCLE GAUGES SIDE BY SIDE */}
                <div className="flex flex-row justify-center gap-6 sm:gap-12 w-full">
                  
                  {/* GAUGE 1: Índice de Riesgo */}
                  <div className="flex flex-col items-center relative w-36 h-24">
                    <svg className="w-full h-full overflow-visible" viewBox="0 0 120 65">
                      <defs>
                        <filter id="neonGlow1" x="-50%" y="-50%" width="200%" height="200%">
                          <feGaussianBlur in="SourceGraphic" stdDeviation="3" result="blur" />
                          <feMerge>
                            <feMergeNode in="blur" />
                            <feMergeNode in="SourceGraphic" />
                          </feMerge>
                        </filter>
                      </defs>
                      {/* Track - Semi Circle */}
                      <circle
                        cx="60" cy="60" r="50"
                        stroke="#1a2540" strokeWidth="10" fill="transparent"
                        strokeDasharray={`${Math.PI * 50} ${Math.PI * 50}`}
                        strokeDashoffset="0"
                        strokeLinecap="round"
                        transform="rotate(180 60 60)"
                      />
                      {/* Progress - Semi Circle */}
                      <circle
                        cx="60" cy="60" r="50"
                        stroke={result.riesgoColor} strokeWidth="10" fill="transparent"
                        strokeDasharray={`${Math.PI * 50} ${Math.PI * 50}`}
                        strokeDashoffset={`${Math.PI * 50 * (1 - result.riesgoPct / 100)}`}
                        strokeLinecap="round"
                        className="transition-all duration-700 ease-out"
                        transform="rotate(180 60 60)"
                        filter="url(#neonGlow1)"
                        style={{ color: result.riesgoColor }}
                      />
                    </svg>
                    <div className="absolute bottom-0 flex flex-col items-center justify-center">
                      <span 
                        className="text-3xl font-black leading-none transition-colors duration-700"
                        style={{ color: result.riesgoColor, textShadow: `0 0 15px ${result.riesgoColor}80` }}
                      >
                        {result.riesgoPct}%
                      </span>
                      <span className="text-[9px] text-[#5a6a80] font-bold uppercase tracking-widest mt-1">
                        Riesgo
                      </span>
                    </div>
                  </div>

                  {/* GAUGE 2: Probabilidad de Lesión (Severidad) */}
                  <div className="flex flex-col items-center relative w-36 h-24">
                    <svg className="w-full h-full overflow-visible" viewBox="0 0 120 65">
                      <defs>
                        <filter id="neonGlow2" x="-50%" y="-50%" width="200%" height="200%">
                          <feGaussianBlur in="SourceGraphic" stdDeviation="3" result="blur" />
                          <feMerge>
                            <feMergeNode in="blur" />
                            <feMergeNode in="SourceGraphic" />
                          </feMerge>
                        </filter>
                      </defs>
                      {/* Track */}
                      <circle
                        cx="60" cy="60" r="50"
                        stroke="#1a2540" strokeWidth="10" fill="transparent"
                        strokeDasharray={`${Math.PI * 50} ${Math.PI * 50}`}
                        strokeDashoffset="0"
                        strokeLinecap="round"
                        transform="rotate(180 60 60)"
                      />
                      {/* Progress: we'll use classProbabilities for LESION or MUERTO */}
                      <circle
                        cx="60" cy="60" r="50"
                        stroke="#00D4FF" strokeWidth="10" fill="transparent"
                        strokeDasharray={`${Math.PI * 50} ${Math.PI * 50}`}
                        strokeDashoffset={`${Math.PI * 50 * (1 - ((result.classProbabilities['LESION'] || 0) + (result.classProbabilities['MUERTO'] || 0)))}`}
                        strokeLinecap="round"
                        className="transition-all duration-700 ease-out"
                        transform="rotate(180 60 60)"
                        filter="url(#neonGlow2)"
                      />
                    </svg>
                    <div className="absolute bottom-0 flex flex-col items-center justify-center">
                      <span 
                        className="text-3xl font-black leading-none transition-colors duration-700 text-[#00D4FF]"
                        style={{ textShadow: `0 0 15px rgba(0, 212, 255, 0.5)` }}
                      >
                        {Math.round(((result.classProbabilities['LESION'] || 0) + (result.classProbabilities['MUERTO'] || 0)) * 100)}%
                      </span>
                      <span className="text-[9px] text-[#5a6a80] font-bold uppercase tracking-widest mt-1">
                        Severidad
                      </span>
                    </div>
                  </div>

                </div>

                {/* Risk Level Badge */}
                <div className="space-y-3 w-full flex flex-col items-center mt-4">
                  <div
                    className="inline-flex items-center px-6 py-2.5 rounded-full border-2 font-extrabold tracking-wider transition-all duration-500 text-xs md:text-sm"
                    style={{
                      backgroundColor: `${result.riesgoColor}15`,
                      borderColor: `${result.riesgoColor}50`,
                      color: result.riesgoColor,
                      boxShadow: `0 0 15px ${result.riesgoColor}20`
                    }}
                  >
                    <span className="mr-2 text-base animate-pulse">{result.riesgoIcon}</span>
                    {result.riesgoLabel}
                  </div>
                  
                  <p className="text-[11px] text-[#5a6a80] max-w-[280px] mx-auto">
                    El modelo predictivo califica este escenario vial con un {result.riesgoPct}% de probabilidad de accidente grave.
                  </p>
                </div>

                {/* Summary Parameters Badges */}
                <div className="flex flex-wrap justify-center gap-2 max-w-[320px] mt-2">
                  <div className="bg-[#0a0f1a] border border-[#1a2540] rounded-xl px-3 py-1.5 text-left text-xs min-w-[70px]">
                    <div className="text-[9px] text-[#4a5568] font-bold uppercase tracking-wide">Actor Vial</div>
                    <div className="font-bold text-slate-200 mt-0.5 truncate max-w-[90px]">{actor}</div>
                  </div>
                  <div className="bg-[#0a0f1a] border border-[#1a2540] rounded-xl px-3 py-1.5 text-left text-xs min-w-[70px]">
                    <div className="text-[9px] text-[#4a5568] font-bold uppercase tracking-wide">Municipio</div>
                    <div className="font-bold text-slate-200 mt-0.5">{municipio}</div>
                  </div>
                  <div className="bg-[#0a0f1a] border border-[#1a2540] rounded-xl px-3 py-1.5 text-left text-xs min-w-[70px]">
                    <div className="text-[9px] text-[#4a5568] font-bold uppercase tracking-wide">Clase Pred.</div>
                    <div className="font-bold text-[#00D4FF] mt-0.5 uppercase tracking-wider">{result.predictedClass}</div>
                  </div>
                </div>
              </div>
            ) : (
              <div className="space-y-2 text-[#5a6a80] p-6">
                <HelpCircle className="w-12 h-12 text-[#2a3548] mx-auto mb-2" />
                <p className="text-sm font-semibold">Modelo No Disponible</p>
                <p className="text-xs text-[#4a5568]">Verifica la exportación del archivo model_data.json en la carpeta public.</p>
              </div>
            )}
          </div>
        </div>

      </div>
    </div>
  );
}
