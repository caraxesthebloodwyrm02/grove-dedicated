import React, { useState, useEffect } from 'react';
import { 
  AppState, 
  House, 
  HOUSE_COLORS, 
} from './types';
import { calculateSpectrum } from './services/simulation';
import { analyzeMagicalSignature } from './services/geminiService';
import { Knob } from './components/Knob';
import { RadialChart } from './components/RadialChart';
import { ResonanceChart } from './components/ResonanceChart';
import { Insights } from './components/Insights';
import { 
  Settings, 
  Sparkles,
  Wand2,
  Shield,
  Activity,
  Zap,
  Menu,
  Hexagon
} from 'lucide-react';

const INITIAL_STATE: AppState = {
  app: {
    name: "hogwarts-visualizer",
    version: "2.0.0"
  },
  dataset: {
    id: "hogwarts_lore",
    kind: "hogwarts_lore",
    name: "Standard Lore",
    description: "Patronus presets + house palettes"
  },
  knobs: {
    canon_tightness: 60,
    signal_clarity: 75,
    noise: 40,
    auth: 70,
    bandwidth: 55,
    emotion_gain: 65,
    mystery: 45,
    practicality: 50
  },
  analyzer: {
    bands: [],
    note: "Analyzer output influenced by House Resonance"
  },
  at: new Date().toISOString()
};

function App() {
  const [state, setState] = useState<AppState>(INITIAL_STATE);
  const [selectedHouse, setSelectedHouse] = useState<House>(House.Ravenclaw);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState<any>(null);

  const colors = HOUSE_COLORS[selectedHouse];

  useEffect(() => {
    const bands = calculateSpectrum(state.knobs, selectedHouse);
    setState(prev => ({
      ...prev,
      analyzer: { ...prev.analyzer, bands }
    }));
  }, [state.knobs, selectedHouse]); 

  const updateKnob = (key: string, value: number) => {
    setState(prev => ({
      ...prev,
      knobs: { ...prev.knobs, [key]: value },
      at: new Date().toISOString()
    }));
  };

  const handleAnalyze = async () => {
    setIsAnalyzing(true);
    const result = await analyzeMagicalSignature(state, selectedHouse);
    setAnalysisResult(result);
    setIsAnalyzing(false);
  };

  return (
    <div className="min-h-screen text-slate-300 selection:bg-white/10 selection:text-white relative overflow-hidden bg-black font-sans">
      
      {/* Cinematic Background Layer */}
      <div 
        className="fixed inset-0 transition-colors duration-1000 ease-in-out z-0"
        style={{
          background: `
            radial-gradient(circle at 15% 50%, ${colors.primary} 0%, #000000 50%),
            radial-gradient(circle at 85% 30%, ${colors.secondary} 0%, #000000 60%)
          `
        }}
      >
        <div className="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/stardust.png')] opacity-20 animate-pulse"></div>
      </div>

      {/* Navigation HUD */}
      <nav className="fixed top-0 left-0 right-0 z-50 border-b border-white/5 bg-black/80 backdrop-blur-md h-20">
        <div className="max-w-[1600px] mx-auto px-6 h-full flex items-center justify-between">
          
          <div className="flex items-center gap-4">
             <div className="w-10 h-10 flex items-center justify-center rounded-sm border border-white/10 bg-white/5 shadow-[0_0_15px_rgba(0,0,0,0.5)]">
                <Hexagon className="w-6 h-6" style={{ color: colors.accent }} />
             </div>
             <div>
               <h1 className="font-serif font-bold text-xl tracking-wider text-slate-100 uppercase">
                 Arithmancy <span style={{ color: colors.accent }}>Engine</span>
               </h1>
               <div className="flex items-center gap-2 text-[10px] text-slate-500 font-mono tracking-[0.2em] uppercase">
                  <span>Build {state.app.version}</span>
                  <span className="w-1 h-1 rounded-full bg-slate-700"></span>
                  <span>System Active</span>
               </div>
             </div>
          </div>
          
          <div className="flex items-center gap-8">
            <div className="hidden md:flex items-center bg-black/40 rounded-full p-1 border border-white/10">
              {Object.values(House).map((house) => (
                <button
                  key={house}
                  onClick={() => setSelectedHouse(house)}
                  className={`relative px-6 py-2 rounded-full text-xs font-serif font-bold tracking-widest transition-all duration-500 ${
                    selectedHouse === house 
                      ? 'text-black shadow-[0_0_20px_rgba(255,255,255,0.2)]' 
                      : 'text-slate-500 hover:text-slate-300'
                  }`}
                  style={{
                    backgroundColor: selectedHouse === house ? colors.accent : 'transparent'
                  }}
                >
                  {house}
                </button>
              ))}
            </div>
            
            <button className="p-3 hover:bg-white/5 rounded-full transition-colors text-slate-400 hover:text-white border border-transparent hover:border-white/10">
               <Menu className="w-5 h-5" />
            </button>
          </div>
        </div>
      </nav>

      {/* Main Dashboard Layout */}
      <main className="max-w-[1600px] mx-auto pt-28 pb-12 px-6 grid grid-cols-1 lg:grid-cols-12 gap-8 relative z-10">
        
        {/* Left Panel: Controls */}
        <div className="lg:col-span-3 flex flex-col gap-6">
          <div 
            className="arcane-card p-8 rounded-sm relative overflow-hidden"
            style={{ '--accent-color': colors.accent } as React.CSSProperties}
          >
            <div className="flex items-center justify-between mb-8 pb-4 border-b border-white/5">
              <h2 className="text-sm font-serif font-bold uppercase tracking-[0.2em] text-slate-400">Parameter Input</h2>
              <Settings className="w-4 h-4 text-slate-600" />
            </div>
            
            <div className="space-y-2">
              {Object.entries(state.knobs).map(([key, value]) => (
                <Knob 
                  key={key}
                  label={key}
                  value={value}
                  onChange={(val) => updateKnob(key, val)}
                  color={colors.accent}
                />
              ))}
            </div>
          </div>

          <div className="arcane-card p-6 rounded-sm flex flex-col gap-4">
             <div className="flex justify-between items-center text-xs font-mono text-slate-500 uppercase tracking-widest">
                <span>Magical Context</span>
                <span className="w-2 h-2 rounded-full animate-pulse" style={{ backgroundColor: colors.accent }}></span>
             </div>
             <div className="text-3xl font-serif font-bold text-white tracking-wide" style={{ textShadow: `0 0 20px ${colors.glow}` }}>
                {selectedHouse}
             </div>
             <div className="h-1 w-full bg-slate-800 rounded-full overflow-hidden">
                <div className="h-full w-2/3 animate-[pulse_4s_infinite]" style={{ backgroundColor: colors.secondary }}></div>
             </div>
          </div>
        </div>

        {/* Center Panel: Visualization */}
        <div className="lg:col-span-6 flex flex-col gap-6">
           {/* Main Star Chart */}
           <div 
             className="arcane-card relative flex-1 min-h-[500px] flex flex-col rounded-sm p-1"
             style={{ '--accent-color': colors.accent } as React.CSSProperties}
           >
              <div className="absolute top-0 left-0 w-4 h-4 border-t border-l border-white/20"></div>
              <div className="absolute top-0 right-0 w-4 h-4 border-t border-r border-white/20"></div>
              <div className="absolute bottom-0 left-0 w-4 h-4 border-b border-l border-white/20"></div>
              <div className="absolute bottom-0 right-0 w-4 h-4 border-b border-r border-white/20"></div>

              <div className="absolute top-6 left-6 z-20">
                 <h2 className="text-2xl font-serif font-bold text-white tracking-widest drop-shadow-md">Signature Matrix</h2>
                 <p className="text-xs font-mono text-slate-500 mt-2 uppercase tracking-[0.1em]">Real-time Arithmancy</p>
              </div>

              <div className="absolute top-6 right-6 z-20 flex flex-col items-end gap-1">
                 <span className="text-xs font-mono text-slate-500">{state.at.split('T')[1].replace('Z','')}</span>
                 <Activity className="w-4 h-4" style={{ color: colors.accent }} />
              </div>
              
              <div className="flex-1 w-full min-h-0 relative z-10 mt-8">
                 <RadialChart data={state.analyzer.bands} color={colors.accent} />
              </div>
              
              {/* Metrics Bar */}
              <div className="p-6 grid grid-cols-3 gap-1 border-t border-white/5 bg-black/20">
                 {[
                   { label: 'Purity', val: state.knobs.signal_clarity, icon: Shield },
                   { label: 'Authority', val: state.knobs.auth, icon: Wand2 },
                   { label: 'Entropy', val: state.knobs.mystery, icon: Zap }
                 ].map((metric) => (
                   <div key={metric.label} className="py-2 px-4 flex flex-col items-center justify-center border-r border-white/5 last:border-0 hover:bg-white/5 transition-colors group cursor-default">
                      <div className="flex items-center gap-2 mb-1 text-slate-500 group-hover:text-slate-300">
                         <metric.icon className="w-3 h-3" />
                         <span className="text-[10px] font-mono uppercase tracking-widest">{metric.label}</span>
                      </div>
                      <div className="text-xl font-sans font-bold text-slate-200 group-hover:scale-110 transition-transform">
                        {metric.val}%
                      </div>
                   </div>
                 ))}
              </div>
           </div>

           {/* Resonance Waveform */}
           <div className="arcane-card h-[250px] flex flex-col rounded-sm p-6 relative overflow-hidden">
              <div className="flex justify-between items-center mb-4 z-10">
                <h3 className="text-xs font-serif font-bold text-slate-400 uppercase tracking-widest flex items-center gap-2">
                   Harmonic Resonance
                </h3>
                <div className="flex gap-1">
                   {[1,2,3].map(i => <div key={i} className="w-1 h-1 rounded-full bg-slate-600"></div>)}
                </div>
              </div>
              <div className="flex-1 w-full min-h-0 -ml-2 relative z-10">
                <ResonanceChart data={state.analyzer.bands} color={colors.accent} />
              </div>
           </div>
        </div>

        {/* Right Panel: AI & Export */}
        <div className="lg:col-span-3 flex flex-col gap-6">
           <Insights 
              data={analysisResult} 
              loading={isAnalyzing} 
              onAnalyze={handleAnalyze} 
              color={colors.accent}
           />
        </div>
      </main>
    </div>
  );
}

export default App;