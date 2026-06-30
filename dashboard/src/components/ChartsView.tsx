import React from 'react';
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  AreaChart,
  Area
} from 'recharts';
import { AlertCircle } from 'lucide-react';

interface ChartsViewProps {
  stats: any;
}

export default function ChartsView({ stats }: ChartsViewProps) {
  if (!stats) {
    return (
      <div className="text-center py-20 bg-slate-50 dark:bg-slate-900/40 rounded-3xl border border-slate-100 dark:border-slate-800">
        <div className="w-12 h-12 rounded-full border-4 border-slate-200 border-t-neon animate-spin mx-auto mb-4"></div>
        <p className="text-sm text-slate-400 font-semibold uppercase tracking-wider">Cargando Estadísticas...</p>
      </div>
    );
  }

  // 1. Prepare Municipio Data
  const municipioData = Object.entries(stats.municipio || {}).map(([key, val]) => ({
    name: key,
    casos: val as number
  }));

  // 2. Prepare Age Distribution Data
  const ageData = (stats.age_distribution || []).map((item: any) => ({
    rango: item.range,
    casos: item.casos
  }));

  // 3. Prepare Gender Data
  const genderData = Object.entries(stats.genero || {}).map(([key, val]) => ({
    name: key === 'No Reportado' ? 'Sin Reportar' : key,
    value: val as number
  }));

  // 4. Prepare Actor Vial Data (Filtering out 'No Reportado' to focus on actual vulnerable roles)
  const actorData = Object.entries(stats.actor_vial || {})
    .filter(([key]) => key !== 'No Reportado')
    .map(([key, val]) => ({
      name: key.replace('Usuario de ', '').replace('Usuario ', ''),
      casos: val as number
    }))
    .sort((a, b) => b.casos - a.casos);

  // Design Colors
  const COLORS = ['#00D4FF', '#0099CC', '#6366F1', '#EC4899', '#10B981'];

  // Custom tooltips for a unified neon style
  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-[#0c0c14]/95 border border-neon/30 text-white px-4 py-2.5 rounded-xl shadow-[0_8px_30px_rgba(0,212,255,0.15)] backdrop-blur-md">
          <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-0.5">{label}</p>
          <p className="text-sm font-extrabold text-neon">
            Casos: <span className="text-white font-display font-medium ml-1">{payload[0].value.toLocaleString()}</span>
          </p>
        </div>
      );
    }
    return null;
  };

  const CustomPieTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-[#0c0c14]/95 border border-neon/30 text-white px-4 py-2.5 rounded-xl shadow-[0_8px_30px_rgba(0,212,255,0.15)] backdrop-blur-md">
          <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-0.5">{data.name}</p>
          <p className="text-sm font-extrabold text-neon">
            Casos: <span className="text-white font-display font-medium ml-1">{data.value.toLocaleString()}</span>
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="space-y-6 matrix-grid dark:matrix-grid-dark min-h-screen pb-12 transition-all">
      
      {/* Informative Alert */}
      <div className="bg-neon-subtle border border-neon/20 text-[#0099CC] dark:text-[#00D4FF] rounded-2xl p-4 flex gap-3 items-start backdrop-blur-sm shadow-sm">
        <AlertCircle className="w-5 h-5 shrink-0 mt-0.5" />
        <div>
          <h4 className="text-xs font-bold uppercase tracking-wider">Visualización Regional Activa</h4>
          <p className="text-[11px] text-slate-500 dark:text-slate-400 mt-1">
            Los datos representados cubren la zona de Sabana Occidente durante el periodo de recolección de estadísticas del Proyecto SENA. Se destaca el alto volumen de registros en el rango de 30-35 años debido a la imputación de la media del dataset original (31.6 años).
          </p>
        </div>
      </div>

      {/* Grid of Main Charts (2x2 Layout) */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* CHART 1: Siniestralidad por Municipio */}
        <div className="bg-white dark:bg-[#12121e] border border-slate-100 dark:border-[#1e2d45] rounded-3xl p-5 md:p-6 shadow-sm relative overflow-hidden group">
          <div className="absolute top-0 left-0 w-1.5 h-12 bg-neon rounded-r"></div>
          <h3 className="text-sm font-extrabold text-slate-800 dark:text-white uppercase tracking-wider mb-1 font-display">
            🏙️ Siniestralidad por Municipio
          </h3>
          <p className="text-[11px] text-[#717182] dark:text-[#717182] mb-6">
            Cantidad total de incidentes reportados en las principales cabeceras municipales.
          </p>
          <div className="h-72 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={municipioData} margin={{ top: 10, right: 10, left: -25, bottom: 0 }}>
                <defs>
                  <linearGradient id="barNeon" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#00D4FF" stopOpacity={0.9} />
                    <stop offset="100%" stopColor="#0099CC" stopOpacity={0.2} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="rgba(113, 113, 130, 0.1)" />
                <XAxis
                  dataKey="name"
                  stroke="#717182"
                  fontSize={10}
                  fontWeight={600}
                  tickLine={false}
                  axisLine={false}
                />
                <YAxis
                  stroke="#717182"
                  fontSize={10}
                  fontWeight={600}
                  tickLine={false}
                  axisLine={false}
                />
                <Tooltip content={<CustomTooltip />} cursor={{ fill: 'rgba(0, 212, 255, 0.05)' }} />
                <Bar
                  dataKey="casos"
                  radius={[8, 8, 0, 0]}
                  fill="url(#barNeon)"
                  maxBarSize={45}
                  style={{
                    filter: 'drop-shadow(0 4px 10px rgba(0, 212, 255, 0.25))'
                  }}
                >
                  {/* Highlight the highest municipality */}
                  {municipioData.map((entry, index) => {
                    const isMax = entry.casos === Math.max(...municipioData.map(d => d.casos));
                    return (
                      <Cell
                        key={`cell-${index}`}
                        fill={isMax ? 'url(#barNeon)' : 'rgba(0, 212, 255, 0.45)'}
                        stroke={isMax ? '#00D4FF' : 'transparent'}
                        strokeWidth={isMax ? 1 : 0}
                      />
                    );
                  })}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* CHART 2: Perfil Etario (Age Distribution Area & Trend Line) */}
        <div className="bg-white dark:bg-[#12121e] border border-slate-100 dark:border-[#1e2d45] rounded-3xl p-5 md:p-6 shadow-sm relative overflow-hidden group">
          <div className="absolute top-0 left-0 w-1.5 h-12 bg-neon rounded-r"></div>
          <h3 className="text-sm font-extrabold text-slate-800 dark:text-white uppercase tracking-wider mb-1 font-display">
            📉 Perfil Etario de los Involucrados
          </h3>
          <p className="text-[11px] text-[#717182] dark:text-[#717182] mb-6">
            Curva de distribución por grupos de edad (segmentada en intervalos de 5 años).
          </p>
          <div className="h-72 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={ageData} margin={{ top: 10, right: 10, left: -25, bottom: 0 }}>
                <defs>
                  <linearGradient id="areaNeon" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#6366F1" stopOpacity={0.25} />
                    <stop offset="100%" stopColor="#6366F1" stopOpacity={0.01} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="rgba(113, 113, 130, 0.1)" />
                <XAxis
                  dataKey="rango"
                  stroke="#717182"
                  fontSize={9}
                  fontWeight={500}
                  tickLine={false}
                  axisLine={false}
                />
                <YAxis
                  stroke="#717182"
                  fontSize={10}
                  fontWeight={600}
                  tickLine={false}
                  axisLine={false}
                />
                <Tooltip content={<CustomTooltip />} />
                <Area
                  type="monotone"
                  dataKey="casos"
                  stroke="#6366F1"
                  strokeWidth={2}
                  fillOpacity={1}
                  fill="url(#areaNeon)"
                />
                {/* Neon Trend Line Overlay */}
                <Line
                  type="monotone"
                  dataKey="casos"
                  stroke="#00D4FF"
                  strokeWidth={2.5}
                  dot={false}
                  style={{
                    filter: 'drop-shadow(0 0 5px rgba(0, 212, 255, 0.8))'
                  }}
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* CHART 3: Distribución por Género */}
        <div className="bg-white dark:bg-[#12121e] border border-slate-100 dark:border-[#1e2d45] rounded-3xl p-5 md:p-6 shadow-sm relative overflow-hidden group">
          <div className="absolute top-0 left-0 w-1.5 h-12 bg-neon rounded-r"></div>
          <h3 className="text-sm font-extrabold text-slate-800 dark:text-white uppercase tracking-wider mb-1 font-display">
            👥 Distribución por Género
          </h3>
          <p className="text-[11px] text-[#717182] dark:text-[#717182] mb-6">
            Proporción de incidentes viales según el género reportado de la víctima.
          </p>
          <div className="h-72 w-full flex flex-col sm:flex-row items-center justify-center gap-6">
            <div className="h-60 w-full sm:w-1/2">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Tooltip content={<CustomPieTooltip />} />
                  <Pie
                    data={genderData}
                    cx="50%"
                    cy="50%"
                    innerRadius={55}
                    outerRadius={75}
                    paddingAngle={4}
                    dataKey="value"
                  >
                    {genderData.map((entry, index) => (
                      <Cell
                        key={`cell-${index}`}
                        fill={COLORS[index % COLORS.length]}
                        style={{
                          filter: `drop-shadow(0 2px 6px ${COLORS[index % COLORS.length]}50)`
                        }}
                      />
                    ))}
                  </Pie>
                </PieChart>
              </ResponsiveContainer>
            </div>
            
            {/* Custom Legend to make it look premium */}
            <div className="w-full sm:w-1/2 space-y-3 px-4">
              {genderData.map((item, index) => {
                const total = genderData.reduce((acc, curr) => acc + curr.value, 0);
                const pct = ((item.value / total) * 100).toFixed(1);
                return (
                  <div key={item.name} className="flex items-center justify-between border-b border-slate-50 dark:border-[#1e2d45]/30 pb-2">
                    <div className="flex items-center gap-2">
                      <span
                        className="w-2.5 h-2.5 rounded-full shrink-0"
                        style={{ backgroundColor: COLORS[index % COLORS.length] }}
                      ></span>
                      <span className="text-xs font-bold text-slate-600 dark:text-slate-300">
                        {item.name}
                      </span>
                    </div>
                    <div className="text-right">
                      <span className="text-xs font-black text-slate-800 dark:text-white font-display">
                        {pct}%
                      </span>
                      <span className="text-[10px] text-slate-400 block">
                        {item.value.toLocaleString()} casos
                      </span>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>

        {/* CHART 4: Actor Vial más Vulnerable */}
        <div className="bg-white dark:bg-[#12121e] border border-slate-100 dark:border-[#1e2d45] rounded-3xl p-5 md:p-6 shadow-sm relative overflow-hidden group">
          <div className="absolute top-0 left-0 w-1.5 h-12 bg-neon rounded-r"></div>
          <h3 className="text-sm font-extrabold text-slate-800 dark:text-white uppercase tracking-wider mb-1 font-display">
            🏍️ Actor Vial Vulnerable (Excl. Sin Reportar)
          </h3>
          <p className="text-[11px] text-[#717182] dark:text-[#717182] mb-6">
            Incidencia de siniestralidad clasificada por el rol del usuario en la vía.
          </p>
          <div className="h-72 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                layout="yaml"
                data={actorData}
                margin={{ top: 10, right: 10, left: 20, bottom: 0 }}
              >
                <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="rgba(113, 113, 130, 0.1)" />
                <XAxis
                  type="number"
                  stroke="#717182"
                  fontSize={10}
                  fontWeight={600}
                  tickLine={false}
                  axisLine={false}
                />
                <YAxis
                  dataKey="name"
                  type="category"
                  stroke="#717182"
                  fontSize={10}
                  fontWeight={600}
                  tickLine={false}
                  axisLine={false}
                  width={75}
                />
                <Tooltip content={<CustomTooltip />} cursor={{ fill: 'rgba(0, 212, 255, 0.03)' }} />
                <Bar
                  dataKey="casos"
                  radius={[0, 6, 6, 0]}
                  fill="#00D4FF"
                  maxBarSize={22}
                  style={{
                    filter: 'drop-shadow(0 2px 5px rgba(0, 212, 255, 0.2))'
                  }}
                >
                  {actorData.map((entry, index) => (
                    <Cell
                      key={`cell-${index}`}
                      fill={index === 0 ? '#00D4FF' : '#0099CC'}
                    />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

      </div>
    </div>
  );
}
