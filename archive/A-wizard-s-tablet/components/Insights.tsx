import React from 'react';
import { Sparkles, AlertTriangle, CheckCircle, Info, Scroll } from 'lucide-react';

interface InsightData {
  title: string;
  description: string;
  type: 'warning' | 'info' | 'success';
}

interface AnalysisResult {
  summary: string;
  status: 'STABLE' | 'VOLATILE' | 'CRITICAL';
  insights: InsightData[];
}

interface InsightsProps {
  data: AnalysisResult | null;
  loading: boolean;
  onAnalyze: () => void;
  color: string;
}

export const Insights: React.FC<InsightsProps> = ({ data, loading, onAnalyze, color }) => {
  return (
    <div 
      className="arcane-card rounded-none border-l-2 h-full flex flex-col relative overflow-hidden group"
      style={{ borderLeftColor: color, '--accent-color': color } as React.CSSProperties}
    >
      {/* Background Rune Texture */}
      <div className="absolute inset-0 opacity-[0.03] bg-[url('https://www.transparenttextures.com/patterns/black-scales.png')] mix-blend-overlay pointer-events-none" />

      <div className="p-6 flex-1 flex flex-col relative z-10">
        <div className="flex justify-between items-start mb-8">
          <div>
            <h2 className="text-2xl font-serif font-bold text-slate-200 tracking-wide flex items-center gap-2">
              <Scroll className="w-5 h-5 opacity-50" />
              Prophecy Log
            </h2>
            <p className="text-xs text-slate-500 font-mono mt-1 uppercase tracking-widest">A.I. Divination Engine</p>
          </div>
          
          <button
            onClick={onAnalyze}
            disabled={loading}
            className="relative px-6 py-2 group/btn overflow-hidden"
          >
            <div className="absolute inset-0 border border-current opacity-30 skew-x-12 transition-transform group-hover/btn:skew-x-0" style={{ color: color }}></div>
            <div className="absolute inset-0 bg-current opacity-10 transform -translate-x-full transition-transform group-hover/btn:translate-x-0" style={{ backgroundColor: color }}></div>
            <span className="relative font-serif text-xs font-bold tracking-widest uppercase" style={{ color: loading ? '#64748b' : color }}>
              {loading ? 'Divining...' : 'Consult'}
            </span>
          </button>
        </div>

        {!data && !loading && (
          <div className="flex-1 flex flex-col items-center justify-center text-slate-600 text-center p-8 border border-dashed border-slate-800/50 bg-slate-950/20">
            <Sparkles className="w-8 h-8 mb-4 opacity-20" />
            <p className="font-serif italic text-sm opacity-60">"The numbers speak to those who listen."</p>
            <p className="text-xs font-mono mt-2 opacity-40">Awaiting Signature Input</p>
          </div>
        )}

        {loading && (
          <div className="flex-1 flex flex-col items-center justify-center">
             <div className="relative w-16 h-16 mb-4">
                <div className="absolute inset-0 border-t-2 border-r-2 rounded-full animate-spin" style={{ borderColor: color }}></div>
                <div className="absolute inset-2 border-b-2 border-l-2 rounded-full animate-spin direction-reverse opacity-50" style={{ borderColor: color }}></div>
             </div>
             <p className="text-xs font-mono uppercase tracking-widest animate-pulse" style={{ color: color }}>Interpreting Signs...</p>
          </div>
        )}

        {data && !loading && (
          <div className="space-y-6 animate-in fade-in slide-in-from-bottom-2 duration-700">
            {/* Status Header */}
            <div className="pb-4 border-b border-slate-800/50">
               <div className="flex items-center gap-3 mb-2">
                 <div className={`w-2 h-2 rounded-full shadow-[0_0_10px_currentColor] ${
                     data.status === 'CRITICAL' ? 'text-red-500 bg-red-500' : 
                     data.status === 'VOLATILE' ? 'text-amber-500 bg-amber-500' : 
                     'text-emerald-500 bg-emerald-500'
                 }`} />
                 <span className="font-serif font-bold text-lg text-slate-200">{data.status}</span>
               </div>
               <p className="font-mono text-xs text-slate-400 leading-relaxed pl-5 border-l border-slate-800 ml-1">
                 {data.summary}
               </p>
            </div>

            {/* Insights List */}
            <div className="space-y-4">
              {data.insights.map((insight, idx) => (
                <div key={idx} className="group/item relative pl-4">
                  <div className="absolute left-0 top-0 bottom-0 w-[2px] bg-slate-800 group-hover/item:bg-slate-600 transition-colors"></div>
                  {insight.type === 'warning' && <div className="absolute left-[-4px] top-1 w-2 h-2 rounded-full bg-amber-500 shadow-[0_0_8px_rgba(245,158,11,0.5)]"></div>}
                  
                  <h4 className={`font-bold text-sm mb-1 ${
                    insight.type === 'warning' ? 'text-amber-400' : 
                    insight.type === 'success' ? 'text-emerald-400' : 'text-blue-400'
                  }`}>
                    {insight.title}
                  </h4>
                  <p className="text-slate-500 text-xs leading-relaxed group-hover/item:text-slate-300 transition-colors">
                    {insight.description}
                  </p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
      
      {/* Decorative Footer */}
      <div className="h-1 w-full bg-gradient-to-r from-transparent via-slate-800 to-transparent opacity-50" />
    </div>
  );
};