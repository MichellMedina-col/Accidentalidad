import React from 'react';
import { ShieldAlert, BarChart3 } from 'lucide-react';

interface HeaderProps {
  activeTab: 'predictor' | 'charts';
}

export default function Header({ activeTab }: HeaderProps) {
  return (
    <header className="border-b border-[#ececf0] dark:border-[#1e2d45] bg-white/70 dark:bg-[#0a0a0f]/80 backdrop-blur-md px-6 py-5 sticky top-0 z-30 transition-all duration-300">
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 className="text-2xl md:text-3xl font-extrabold tracking-tight flex items-center gap-2.5">
            {activeTab === 'predictor' ? (
              <>
                <ShieldAlert className="w-7 h-7 text-neon drop-shadow-[0_0_8px_rgba(0,212,255,0.5)]" />
                <span>
                  Inicio • Predictor de <span className="text-neon neon-text-glow font-black font-display">RIESGO</span>
                </span>
              </>
            ) : (
              <>
                <BarChart3 className="w-7 h-7 text-neon drop-shadow-[0_0_8px_rgba(0,212,255,0.5)]" />
                <span>
                  Análisis • <span className="text-neon neon-text-glow font-black font-display">GRÁFICOS</span> Estadísticos
                </span>
              </>
            )}
          </h1>
          <p className="text-xs md:text-sm text-[#717182] dark:text-[#94a3b8] mt-1 font-medium flex flex-wrap items-center gap-x-2 gap-y-1">
            <span>Seguridad Vial</span>
            <span className="text-slate-300 dark:text-slate-700">•</span>
            <span>Sabana Occidente</span>
            <span className="text-slate-300 dark:text-slate-700">•</span>
            <span className="text-neon font-semibold">Proyecto SENA 2026</span>
          </p>
        </div>
        
        {/* Subtle Neon Badge */}
        <div className="self-start md:self-auto flex items-center gap-2 bg-neon-subtle border border-neon/30 text-neon dark:text-white px-3.5 py-1.5 rounded-full text-xs font-semibold tracking-wide neon-border-glow select-none">
          <span className="w-2.5 h-2.5 rounded-full bg-neon animate-pulse shadow-[0_0_8px_#00D4FF]"></span>
          SISTEMA PREDICTIVO V1.0
        </div>
      </div>
    </header>
  );
}
