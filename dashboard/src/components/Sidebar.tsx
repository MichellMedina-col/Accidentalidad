import React from 'react';
import { Home, BarChart3, Sun, Moon, ShieldAlert } from 'lucide-react';

interface SidebarProps {
  activeTab: 'predictor' | 'charts';
  setActiveTab: (tab: 'predictor' | 'charts') => void;
  darkMode: boolean;
  setDarkMode: (dark: boolean) => void;
}

export default function Sidebar({ activeTab, setActiveTab, darkMode, setDarkMode }: SidebarProps) {
  return (
    <aside className="w-full md:w-64 border-b md:border-b-0 md:border-r border-[#ececf0] dark:border-[#1e2d45] bg-[#fcfcfd] dark:bg-[#07070a]/90 flex flex-col justify-between shrink-0 transition-all duration-300">
      <div>
        {/* Logo and Brand */}
        <div className="p-6 flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-neon to-[#0099CC] flex items-center justify-center text-white text-xl font-bold shadow-[0_0_15px_rgba(0,212,255,0.4)]">
            🚦
          </div>
          <div>
            <div className="font-extrabold text-base tracking-tight text-[#030213] dark:text-white flex items-center gap-1 font-display">
              Vial<span className="text-neon neon-text-glow">Analytics</span>
            </div>
            <div className="text-[10px] text-[#717182] dark:text-[#475569] uppercase font-bold tracking-widest">
              Sabana Occidente
            </div>
          </div>
        </div>

        {/* Navigation Section */}
        <div className="px-4 py-6">
          <div className="text-[10px] text-[#717182] dark:text-[#475569] uppercase font-extrabold tracking-widest px-3 mb-3">
            Navegación
          </div>
          
          <nav className="space-y-1.5">
            <button
              onClick={() => setActiveTab('predictor')}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-semibold tracking-wide transition-all duration-200 ${
                activeTab === 'predictor'
                  ? 'bg-neon-subtle text-neon border border-neon/20 shadow-[0_0_15px_rgba(0,212,255,0.08)]'
                  : 'text-[#717182] hover:text-[#030213] dark:hover:text-white hover:bg-slate-100 dark:hover:bg-slate-900 border border-transparent'
              }`}
            >
              <Home className={`w-4 h-4 ${activeTab === 'predictor' ? 'text-neon' : ''}`} />
              <span>Inicio · Predictor</span>
            </button>

            <button
              onClick={() => setActiveTab('charts')}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-semibold tracking-wide transition-all duration-200 ${
                activeTab === 'charts'
                  ? 'bg-neon-subtle text-neon border border-neon/20 shadow-[0_0_15px_rgba(0,212,255,0.08)]'
                  : 'text-[#717182] hover:text-[#030213] dark:hover:text-white hover:bg-slate-100 dark:hover:bg-slate-900 border border-transparent'
              }`}
            >
              <BarChart3 className={`w-4 h-4 ${activeTab === 'charts' ? 'text-neon' : ''}`} />
              <span>Análisis Visual</span>
            </button>
          </nav>
        </div>
      </div>

      {/* Footer & Theme Toggle */}
      <div className="p-4 space-y-4">
        {/* Theme Toggle Button */}
        <button
          onClick={() => setDarkMode(!darkMode)}
          className="w-full flex items-center justify-between px-4 py-2.5 rounded-xl border border-[#ececf0] dark:border-[#1e2d45] bg-white dark:bg-[#12121e] hover:bg-slate-50 dark:hover:bg-slate-800 text-sm font-medium transition-all duration-200 shadow-sm"
        >
          <div className="flex items-center gap-2 text-[#717182] dark:text-[#94a3b8]">
            {darkMode ? <Sun className="w-4 h-4 text-amber-500" /> : <Moon className="w-4 h-4 text-indigo-500" />}
            <span>{darkMode ? 'Modo Claro' : 'Modo Oscuro'}</span>
          </div>
          <span className="text-[10px] bg-slate-100 dark:bg-slate-800 px-2 py-0.5 rounded text-slate-500">
            THEME
          </span>
        </button>

        {/* SENA Footer Box */}
        <div className="border border-[#ececf0] dark:border-[#1e2d45] rounded-2xl bg-white dark:bg-[#12121e]/60 p-4 text-center relative overflow-hidden transition-all duration-300">
          {/* Neon decorative line */}
          <div className="absolute top-0 left-0 right-0 h-0.5 bg-gradient-to-r from-transparent via-neon to-transparent opacity-70"></div>
          
          <div className="text-[10px] text-[#717182] dark:text-[#475569] uppercase font-bold tracking-widest">
            Proyecto SENA
          </div>
          <div className="text-xl font-black text-neon dark:text-white tracking-wider font-display mt-0.5 shadow-neon">
            2026
          </div>
        </div>
      </div>
    </aside>
  );
}
