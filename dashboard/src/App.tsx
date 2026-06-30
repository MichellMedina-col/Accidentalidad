import React, { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import Header from './components/Header';
import StatsGrid from './components/StatsGrid';
import PredictorCard from './components/PredictorCard';
import ChartsView from './components/ChartsView';
import { ModelData } from './utils/predictor';

export default function App() {
  const [activeTab, setActiveTab] = useState<'predictor' | 'charts'>('predictor');
  const [darkMode, setDarkMode] = useState<boolean>(true);
  const [model, setModel] = useState<ModelData | null>(null);
  const [stats, setStats] = useState<any>(null);
  const [loadingModel, setLoadingModel] = useState<boolean>(true);
  const [loadingStats, setLoadingStats] = useState<boolean>(true);

  // 1. Sync Dark Mode with <html> element
  useEffect(() => {
    const root = window.document.documentElement;
    if (darkMode) {
      root.classList.add('dark');
      root.style.backgroundColor = '#0a0a0f';
    } else {
      root.classList.remove('dark');
      root.style.backgroundColor = '#ffffff';
    }
  }, [darkMode]);

  // 2. Fetch Model & Stats JSON files
  useEffect(() => {
    // Fetch Model Data
    fetch('/model_data.json')
      .then((res) => {
        if (!res.ok) throw new Error('Failed to load model file');
        return res.json();
      })
      .then((data) => {
        setModel(data);
        setLoadingModel(false);
      })
      .catch((err) => {
        console.error('Error loading model data:', err);
        setLoadingModel(false);
      });

    // Fetch Stats Summary
    fetch('/data_summary.json')
      .then((res) => {
        if (!res.ok) throw new Error('Failed to load stats file');
        return res.json();
      })
      .then((data) => {
        setStats(data.stats);
        setLoadingStats(false);
      })
      .catch((err) => {
        console.error('Error loading stats data:', err);
        setLoadingStats(false);
      });
  }, []);

  // 3. Compute Dynamic Stats for KPI Cards
  const totalIncidents = stats?.total_records || 13076;
  const averageAge = stats?.age_mean || 32.1;

  // Find municipality with highest accident count
  let maxMunicipality = 'Funza';
  if (stats?.municipio) {
    const sortedMun = Object.entries(stats.municipio).sort((a: any, b: any) => b[1] - a[1]);
    if (sortedMun.length > 0) {
      maxMunicipality = sortedMun[0][0];
    }
  }

  // Find actor vial with highest accident count (excluding No Reportado)
  let vulnerableActor = 'Motociclista';
  if (stats?.actor_vial) {
    const sortedActor = Object.entries(stats.actor_vial)
      .filter(([key]) => key !== 'No Reportado')
      .sort((a: any, b: any) => b[1] - a[1]);
    if (sortedActor.length > 0) {
      const act = sortedActor[0][0];
      // Format nicely
      let formatted = act.replace('Usuario de ', '').replace('Usuario ', '');
      formatted = formatted.charAt(0).toUpperCase() + formatted.slice(1);
      
      if (formatted.toLowerCase() === 'moto') vulnerableActor = 'Motociclista';
      else if (formatted.toLowerCase() === 'bicicleta') vulnerableActor = 'Ciclista';
      else if (formatted.toLowerCase() === 'vehiculo') vulnerableActor = 'Conductor';
      else if (formatted.toLowerCase() === 'peaton' || formatted.toLowerCase() === 'peatón') vulnerableActor = 'Peatón';
      else vulnerableActor = formatted;
    }
  }

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-[#0a0a0f] flex flex-col md:flex-row text-[#030213] dark:text-slate-100 transition-colors duration-300 antialiased font-sans">
      {/* Sidebar Navigation */}
      <Sidebar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        darkMode={darkMode}
        setDarkMode={setDarkMode}
      />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0">
        <Header activeTab={activeTab} />

        <main className="flex-1 p-6 md:p-8 overflow-y-auto no-scrollbar max-w-7xl mx-auto w-full">
          {activeTab === 'predictor' ? (
            <div className="space-y-6 animate-fade-in">
              {/* KPIs Grid */}
              <StatsGrid
                totalIncidents={totalIncidents}
                averageAge={averageAge}
                maxMunicipality={maxMunicipality}
                vulnerableActor={vulnerableActor}
              />

              {/* Predictor Panel */}
              <PredictorCard model={model} loading={loadingModel} />
            </div>
          ) : (
            <div className="animate-fade-in">
              {/* Visual Analytics Graphs view */}
              <ChartsView stats={stats} />
            </div>
          )}
        </main>
        
        {/* Simple Neon Footer */}
        <footer className="border-t border-[#ececf0] dark:border-[#1e2d45] py-4 text-center text-[10px] text-slate-400 font-bold uppercase tracking-widest bg-white/40 dark:bg-[#0a0a0f]/40 backdrop-blur">
          <div className="flex items-center justify-center gap-2">
            <span>VialAnalytics</span>
            <span className="w-1.5 h-1.5 rounded-full bg-neon shadow-[0_0_6px_#00D4FF]"></span>
            <span>Sabana Occidente</span>
            <span className="w-1.5 h-1.5 rounded-full bg-neon shadow-[0_0_6px_#00D4FF]"></span>
            <span className="text-neon font-black font-display">Proyecto SENA 2026</span>
          </div>
        </footer>
      </div>
    </div>
  );
}
