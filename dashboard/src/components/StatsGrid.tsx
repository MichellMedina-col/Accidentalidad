import React from 'react';
import { AlertOctagon, Calendar, MapPin, PersonStanding } from 'lucide-react';

interface StatsGridProps {
  totalIncidents: number;
  averageAge: number;
  maxMunicipality: string;
  vulnerableActor: string;
}

export default function StatsGrid({
  totalIncidents,
  averageAge,
  maxMunicipality,
  vulnerableActor
}: StatsGridProps) {
  
  // Format numbers nicely with commas
  const formattedIncidents = totalIncidents.toLocaleString();
  
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-5 mb-6">
      {/* 1. INCIDENTES FILTRADOS */}
      <div className="bg-white dark:bg-[#12121e] border border-slate-100 dark:border-[#1e2d45] rounded-2xl p-5 hover:translate-y-[-2px] transition-all duration-300 relative overflow-hidden group shadow-sm hover:shadow-[0_12px_24px_rgba(0,0,0,0.04)] dark:hover:shadow-[0_12px_32px_rgba(0,0,0,0.4)]">
        {/* Neon bottom accent */}
        <div className="absolute bottom-0 left-0 right-0 h-[3px] bg-[#00D4FF] opacity-80 group-hover:h-[4px] transition-all"></div>
        <div className="flex justify-between items-start">
          <div className="space-y-1">
            <span className="text-[10px] text-[#717182] dark:text-[#475569] uppercase font-bold tracking-widest block">
              Incidentes Filtrados
            </span>
            <h3 className="text-3xl font-extrabold text-[#00D4FF] neon-text-glow font-display">
              {formattedIncidents}
            </h3>
          </div>
          <div className="w-10 h-10 rounded-xl bg-neon-subtle flex items-center justify-center text-neon shadow-inner">
            <AlertOctagon className="w-5 h-5" />
          </div>
        </div>
        <p className="text-[11px] text-[#717182] dark:text-[#717182] mt-3">
          Casos que cumplen con los filtros activos
        </p>
      </div>

      {/* 2. EDAD MEDIA CRÍTICA */}
      <div className="bg-white dark:bg-[#12121e] border border-slate-100 dark:border-[#1e2d45] rounded-2xl p-5 hover:translate-y-[-2px] transition-all duration-300 relative overflow-hidden group shadow-sm hover:shadow-[0_12px_24px_rgba(0,0,0,0.04)] dark:hover:shadow-[0_12px_32px_rgba(0,0,0,0.4)]">
        {/* Neon bottom accent */}
        <div className="absolute bottom-0 left-0 right-0 h-[3px] bg-[#0099CC] opacity-80 group-hover:h-[4px] transition-all"></div>
        <div className="flex justify-between items-start">
          <div className="space-y-1">
            <span className="text-[10px] text-[#717182] dark:text-[#475569] uppercase font-bold tracking-widest block">
              Edad Media Crítica
            </span>
            <h3 className="text-3xl font-extrabold text-[#030213] dark:text-white font-display">
              {averageAge.toFixed(1)} <span className="text-sm font-medium text-slate-400">años</span>
            </h3>
          </div>
          <div className="w-10 h-10 rounded-xl bg-slate-100 dark:bg-slate-800/80 flex items-center justify-center text-slate-500 dark:text-slate-400">
            <Calendar className="w-5 h-5" />
          </div>
        </div>
        <p className="text-[11px] text-[#717182] dark:text-[#717182] mt-3">
          Promedio de edad de los involucrados
        </p>
      </div>

      {/* 3. MAYOR SINIESTRALIDAD */}
      <div className="bg-white dark:bg-[#12121e] border border-slate-100 dark:border-[#1e2d45] rounded-2xl p-5 hover:translate-y-[-2px] transition-all duration-300 relative overflow-hidden group shadow-sm hover:shadow-[0_12px_24px_rgba(0,0,0,0.04)] dark:hover:shadow-[0_12px_32px_rgba(0,0,0,0.4)]">
        {/* Neon bottom accent */}
        <div className="absolute bottom-0 left-0 right-0 h-[3px] bg-[#00D4FF] opacity-80 group-hover:h-[4px] transition-all"></div>
        <div className="flex justify-between items-start">
          <div className="space-y-1">
            <span className="text-[10px] text-[#717182] dark:text-[#475569] uppercase font-bold tracking-widest block">
              Mayor Siniestralidad
            </span>
            <h3 className="text-xl md:text-2xl font-extrabold text-[#030213] dark:text-white truncate max-w-[170px] mt-1 font-display">
              {maxMunicipality}
            </h3>
          </div>
          <div className="w-10 h-10 rounded-xl bg-slate-100 dark:bg-slate-800/80 flex items-center justify-center text-slate-500 dark:text-slate-400">
            <MapPin className="w-5 h-5" />
          </div>
        </div>
        <p className="text-[11px] text-[#717182] dark:text-[#717182] mt-3">
          Municipio con mayor número de incidentes
        </p>
      </div>

      {/* 4. ACTOR MÁS VULNERABLE */}
      <div className="bg-white dark:bg-[#12121e] border border-slate-100 dark:border-[#1e2d45] rounded-2xl p-5 hover:translate-y-[-2px] transition-all duration-300 relative overflow-hidden group shadow-sm hover:shadow-[0_12px_24px_rgba(0,0,0,0.04)] dark:hover:shadow-[0_12px_32px_rgba(0,0,0,0.4)]">
        {/* Neon bottom accent */}
        <div className="absolute bottom-0 left-0 right-0 h-[3px] bg-[#00D4FF] opacity-80 group-hover:h-[4px] transition-all"></div>
        <div className="flex justify-between items-start">
          <div className="space-y-1">
            <span className="text-[10px] text-[#717182] dark:text-[#475569] uppercase font-bold tracking-widest block">
              Actor Más Vulnerable
            </span>
            <div className="mt-1.5">
              <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-bold bg-neon-subtle text-neon border border-neon/30 neon-border-glow uppercase tracking-wider">
                {vulnerableActor}
              </span>
            </div>
          </div>
          <div className="w-10 h-10 rounded-xl bg-slate-100 dark:bg-slate-800/80 flex items-center justify-center text-slate-500 dark:text-slate-400">
            <PersonStanding className="w-5 h-5" />
          </div>
        </div>
        <p className="text-[11px] text-[#717182] dark:text-[#717182] mt-3">
          Rol con mayor cantidad de víctimas registradas
        </p>
      </div>
    </div>
  );
}
