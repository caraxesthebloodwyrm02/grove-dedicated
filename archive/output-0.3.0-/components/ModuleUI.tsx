import React, { useState, useRef, useEffect } from 'react';
import { Mic, Image as ImageIcon, Wand2, Brain, Play, StopCircle, Loader2, Settings2, Video, VideoOff, Aperture, ChevronDown, Save, Trash2, Network, Box, Package, Globe, Search, Sparkles, AlertTriangle, ShieldAlert, CheckCircle2, Scale, Code2, ScanLine, Radar, HardDrive, Wifi, WifiOff, FileText, Database, FlaskConical, History, Terminal, Activity, GitBranch, Zap, CircuitBoard, Youtube } from 'lucide-react';
import { AspectRatio, ImageSize, LogItem, VoiceName, Preset, LogicLevel, LogicStyle, CognitiveLoad, GridNode, LogicResponse, DiagramType, PulseItem } from '../types';
import * as GeminiService from '../services/geminiService';
import { LiveClient } from '../services/liveClient';
import { LiveServerMessage } from '@google/genai';
import CodeContextVisualizer from './CodeContextVisualizer';
import { ConceptVisualizer } from './ConceptVisualizer';

// --- VIBE ASSETS ---
const VIBE_IMAGES = [
    { id: 'city', src: 'https://images.unsplash.com/photo-1565626424178-c599f697bc59?q=80&w=600&auto=format&fit=crop', prompt: 'A futuristic rainy city street with green neon lights and reflections' },
    { id: 'field', src: 'https://images.unsplash.com/photo-1623164835824-2c672d9f4300?q=80&w=600&auto=format&fit=crop', prompt: 'Golden hour landscape with rolling hills and autumn trees' },
    { id: 'botanical', src: 'https://images.unsplash.com/photo-1518173946687-a4c8892bbd9f?q=80&w=600&auto=format&fit=crop', prompt: 'Vintage botanical illustration of lush green forest and plants' },
    { id: 'desk', src: 'https://images.unsplash.com/photo-1555099962-4199c345e5dd?q=80&w=600&auto=format&fit=crop', prompt: 'Dark modern coding workspace with screens displaying code and coffee' },
    { id: 'nebula', src: 'https://images.unsplash.com/photo-1419242902214-272b3f66ee7a?q=80&w=600&auto=format&fit=crop', prompt: 'Vibrant cosmic nebula with purple and green gas clouds' },
    { id: 'park', src: 'https://images.unsplash.com/photo-1486328228599-85db4443971f?q=80&w=600&auto=format&fit=crop', prompt: 'Sunny park pathway lined with trees and flowers' },
    { id: 'fantasy', src: 'https://images.unsplash.com/photo-1518709268805-4e9042af9f23?q=80&w=600&auto=format&fit=crop', prompt: 'Epic fantasy dragon perched on a cliff edge in a storm' },
    { id: 'tech', src: 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?q=80&w=600&auto=format&fit=crop', prompt: 'Complex data visualization dashboard with network graphs' }
];

// --- GRID NODES (LOGIC LAB PRESETS) ---
const GRID_NODES: GridNode[] = [
    {
        id: 'bool_logic',
        title: 'Boolean Logic Identities',
        domain: 'Computer Science',
        description: 'Visual network of fundamental Boolean identities (Idempotent, Associative, etc).',
        defaultParams: {
            question: "Explain the fundamental identities of Boolean Algebra (Idempotent, Associative, Commutative, Distributive, etc.) and how they relate.",
            level: 'intermediate',
            style: 'step_by_step',
            load: 'medium',
            diagramType: 'network'
        }
    },
    {
        id: 'nfa_playground',
        title: 'NFA String Recognizer',
        domain: 'Automata Theory',
        description: 'Design a Non-Deterministic Finite Automaton for strings ending in "abb".',
        defaultParams: {
            question: "Design a Non-Deterministic Finite Automaton (NFA) that recognizes strings ending in 'abb' over alphabet {a,b}. Explain the state transitions.",
            level: 'advanced',
            style: 'step_by_step',
            load: 'high',
            diagramType: 'automata'
        }
    },
    {
        id: 'cog_load',
        title: 'Cognitive Load Theory',
        domain: 'Psychology / UX',
        description: 'Comparison of Intrinsic, Extraneous, and Germane cognitive load.',
        defaultParams: {
            question: "Compare Intrinsic, Extraneous, and Germane cognitive load. How do they interact during learning?",
            level: 'intermediate',
            style: 'summary',
            load: 'low',
            diagramType: 'tree'
        }
    }
];

// --- Helper Hook for Presets ---
function usePresets<T>(key: string, currentData: T, onLoad: (data: T) => void) {
  const [presets, setPresets] = useState<Preset<T>[]>([]);
  const [newPresetName, setNewPresetName] = useState('');

  useEffect(() => {
    const saved = localStorage.getItem(key);
    if (saved) {
      try {
        setPresets(JSON.parse(saved));
      } catch (e) {
        console.error("Failed to parse presets", e);
      }
    }
  }, [key]);

  const savePreset = () => {
    if (!newPresetName.trim()) return;
    const newPreset: Preset<T> = { name: newPresetName.trim(), data: currentData };
    const updated = [...presets, newPreset];
    setPresets(updated);
    localStorage.setItem(key, JSON.stringify(updated));
    setNewPresetName('');
  };

  const deletePreset = (index: number) => {
    const updated = presets.filter((_, i) => i !== index);
    setPresets(updated);
    localStorage.setItem(key, JSON.stringify(updated));
  };

  return { presets, newPresetName, setNewPresetName, savePreset, deletePreset, loadPreset: onLoad };
}

// --- Shared UI Components ---

const Button = ({ children, onClick, active, disabled, className = "", variant="default" }: any) => {
    const baseClass = "px-4 py-2 rounded-sm text-sm font-medium transition-all duration-200 uppercase tracking-wider flex items-center justify-center gap-2";
    const variants: any = {
        default: active 
            ? 'bg-blue-600 text-white shadow-[0_0_10px_rgba(37,99,235,0.5)] border border-blue-400' 
            : 'bg-neutral-800 text-neutral-400 border border-neutral-700 hover:bg-neutral-700 hover:text-white',
        danger: active
            ? 'bg-red-900/50 border-red-500 text-red-100'
            : 'bg-neutral-800 text-neutral-400 border border-neutral-700 hover:text-red-400 hover:border-red-900',
        icon: "p-2 aspect-square hover:bg-neutral-700 text-neutral-400",
        python: active
            ? 'bg-[#3776ab] text-[#ffd343] border border-[#ffd343] shadow-[0_0_10px_rgba(255,211,67,0.3)]'
            : 'bg-neutral-800 text-[#3776ab] border border-neutral-700 hover:border-[#ffd343] hover:text-[#ffd343]',
        orange: active
             ? 'bg-orange-600 text-white border border-orange-400'
             : 'bg-neutral-800 text-orange-400 border border-neutral-700 hover:text-orange-200'
    };

    return (
        <button
            onClick={onClick}
            disabled={disabled}
            className={`
                ${baseClass}
                ${variants[variant] || variants.default}
                ${disabled ? 'opacity-50 cursor-not-allowed' : ''}
                ${className}
            `}
        >
            {children}
        </button>
    );
};

const Input = ({ value, onChange, placeholder, onKeyDown, className = "" }: any) => (
  <input
    type="text"
    value={value}
    onChange={onChange}
    onKeyDown={onKeyDown}
    placeholder={placeholder}
    className={`w-full bg-neutral-900/80 border-b border-neutral-700 text-white px-3 py-3 focus:outline-none focus:border-blue-500 font-mono text-sm transition-colors ${className}`}
  />
);

const TextArea = ({ value, onChange, placeholder }: any) => (
  <textarea
    value={value}
    onChange={onChange}
    placeholder={placeholder}
    className="w-full h-32 bg-neutral-900/80 border-b border-neutral-700 text-white px-3 py-3 focus:outline-none focus:border-blue-500 font-mono text-xs transition-colors resize-none custom-scrollbar"
  />
);

const Select = ({ value, onChange, options, label }: { value: string, onChange: (v: string) => void, options: string[], label?: string }) => (
    <div className="flex flex-col gap-1">
        {label && <label className="text-[10px] text-neutral-500 font-mono uppercase tracking-wider">{label}</label>}
        <div className="flex flex-wrap gap-1 bg-neutral-900 p-1 rounded border border-neutral-800">
            {options.map(opt => (
                <button
                    key={opt}
                    onClick={() => onChange(opt)}
                    className={`px-2 py-1 text-[10px] rounded-sm font-mono transition-colors ${value === opt ? 'bg-neutral-700 text-white shadow-sm' : 'text-neutral-500 hover:text-neutral-300'}`}
                >
                    {opt}
                </button>
            ))}
        </div>
    </div>
);

const Range = ({ value, min, max, step, onChange, label, formatValue }: any) => (
    <div className="flex flex-col gap-2">
         <div className="flex justify-between items-center">
            {label && <label className="text-[10px] text-neutral-500 font-mono uppercase tracking-wider">{label}</label>}
            <span className="text-[10px] font-mono text-blue-400">{formatValue ? formatValue(value) : value}</span>
         </div>
         <input 
            type="range" 
            min={min} 
            max={max} 
            step={step} 
            value={value} 
            onChange={(e) => onChange(Number(e.target.value))}
            className="w-full h-1 bg-neutral-800 rounded-lg appearance-none cursor-pointer accent-blue-600"
         />
    </div>
);

const SettingsPanel = ({ isOpen, children }: { isOpen: boolean, children?: React.ReactNode }) => (
    <div className={`overflow-hidden transition-all duration-300 ease-in-out ${isOpen ? 'max-h-[500px] opacity-100 mb-4' : 'max-h-0 opacity-0 mb-0'}`}>
        <div className="bg-neutral-950/50 rounded-lg p-4 border border-neutral-800 space-y-4 shadow-inner">
            {children}
        </div>
    </div>
);

const SettingsHeader = ({ title, isOpen, onToggle }: { title: string, isOpen: boolean, onToggle: () => void }) => (
    <div className="flex items-center justify-between mb-2">
        <h3 className="text-xs font-mono text-neutral-500 uppercase tracking-widest">{title}</h3>
        <button onClick={onToggle} className={`text-neutral-500 hover:text-blue-400 transition-colors ${isOpen ? 'text-blue-400' : ''}`}>
            <Settings2 className="w-4 h-4" />
        </button>
    </div>
);

const PresetControl = ({ 
    presets, 
    newPresetName, 
    setNewPresetName, 
    savePreset, 
    deletePreset, 
    loadPreset 
}: any) => (
    <div className="border-t border-neutral-800 pt-3 mt-3">
         <div className="flex justify-between items-center mb-2">
            <div className="text-[10px] text-neutral-500 font-mono uppercase tracking-wider">Presets</div>
         </div>
         <div className="flex gap-2 mb-2">
             <input 
                className="flex-1 bg-neutral-900 border border-neutral-800 rounded-sm px-2 text-[10px] font-mono py-1 focus:outline-none focus:border-blue-500 text-neutral-300 placeholder-neutral-600"
                placeholder="SAVE PRESET AS..."
                value={newPresetName}
                onChange={(e) => setNewPresetName(e.target.value)}
             />
             <button onClick={savePreset} disabled={!newPresetName} className="bg-neutral-800 hover:bg-blue-900 text-neutral-400 hover:text-blue-200 border border-neutral-700 rounded-sm px-2 py-1 text-[10px] disabled:opacity-50 transition-colors">
                 <Save className="w-3 h-3" />
             </button>
         </div>
         {presets.length > 0 && (
             <div className="grid grid-cols-1 gap-1 max-h-32 overflow-y-auto pr-1 custom-scrollbar">
                 {presets.map((p: any, i: number) => (
                     <div key={i} className="flex items-center justify-between bg-neutral-900/50 border border-neutral-800/50 rounded-sm px-2 py-1 group hover:border-neutral-700 transition-colors">
                         <button onClick={() => loadPreset(p.data)} className="text-[10px] font-mono text-neutral-400 hover:text-blue-400 truncate flex-1 text-left">
                            {p.name}
                         </button>
                         <button onClick={() => deletePreset(i)} className="text-neutral-700 hover:text-red-400 opacity-0 group-hover:opacity-100 transition-opacity ml-2">
                            <Trash2 className="w-3 h-3" />
                         </button>
                     </div>
                 ))}
             </div>
         )}
    </div>
);

// --- Sub-Modules ---

export const OpenSourceRadarModule = ({ onLog }: { onLog: (l: LogItem) => void }) => {
    const [pulseData, setPulseData] = useState<PulseItem[]>([]);
    const [loading, setLoading] = useState(false);
    const [analyzing, setAnalyzing] = useState(false);
    const [activeSource, setActiveSource] = useState<'ALL' | 'GITHUB' | 'HUGGINGFACE' | 'MISTRAL'>('ALL');

    const fetchPulse = async () => {
        setLoading(true);
        try {
            // Updated to port 8080 based on user confirmation
            const res = await fetch('http://127.0.0.1:8080/community/pulse');
            if (res.ok) {
                const data = await res.json();
                
                // Add the requested integration point
                const irfanNode: PulseItem = {
                    id: 'irfan_kabir',
                    source: 'GITHUB', // Mapping to generic source or add YOUTUBE if type allows, using GITHUB for now as standard pulse
                    title: '@irfankabir02 (Partner Node)',
                    description: 'YouTube Intelligence Uplink Established. Monitoring channel frequency.',
                    metric: 'Live Uplink',
                    url: 'https://youtube.com/@irfankabir02?si=7qdU7ZCz6LSa42ok'
                };
                
                setPulseData([irfanNode, ...data]);
                onLog({ id: Date.now().toString(), timestamp: new Date(), sender: 'system', content: `Uplink established. Received ${data.length + 1} telemetry packets from Open Source Radar.`, type: 'info' });
            } else {
                throw new Error("Failed to fetch pulse data");
            }
        } catch (e: any) {
            onLog({ id: Date.now().toString(), timestamp: new Date(), sender: 'system', content: `Radar Offline: ${e.message}`, type: 'error' });
        }
        setLoading(false);
    };

    const handleAnalyze = async () => {
        if (pulseData.length === 0) return;
        setAnalyzing(true);
        onLog({ id: Date.now().toString(), timestamp: new Date(), sender: 'user', content: "Synthesizing SineWaveform Intelligence...", type: 'text' });
        
        try {
            const analysis = await GeminiService.analyzeOpenSourcePulse(pulseData);
            
            const WaveformOutput = () => (
                <div className="space-y-2 font-mono">
                    <div className="flex items-center gap-2 border-b border-orange-500/30 pb-2 mb-2">
                        <Activity className="w-4 h-4 text-orange-400" />
                        <span className="text-xs text-orange-300 uppercase tracking-widest">SineWaveform Intelligence</span>
                    </div>
                    <p className="text-sm text-neutral-300 leading-relaxed">{analysis}</p>
                </div>
            );

            onLog({ 
                id: Date.now().toString() + '_pulse_analysis', 
                timestamp: new Date(), 
                sender: 'model', 
                content: <WaveformOutput />, 
                type: 'info' 
            });

        } catch (e: any) {
             onLog({ id: Date.now().toString(), timestamp: new Date(), sender: 'system', content: `Analysis Failed: ${e.message}`, type: 'error' });
        }
        setAnalyzing(false);
    };

    const filteredData = activeSource === 'ALL' ? pulseData : pulseData.filter(p => p.source === activeSource);

    return (
        <div className="space-y-4">
             <CodeContextVisualizer mode={analyzing ? 'processing' : 'text'} intensity={analyzing ? 1 : 0.2} />
             
             {/* Controls */}
             <div className="flex gap-2">
                 <Button onClick={fetchPulse} disabled={loading} active={loading} className="flex-1" variant="orange">
                    {loading ? <Loader2 className="animate-spin w-4 h-4"/> : <><Radar className="w-4 h-4"/> SCAN NETWORK</>}
                 </Button>
                 <Button onClick={handleAnalyze} disabled={analyzing || pulseData.length === 0} active={analyzing} className="flex-1" variant="default">
                    {analyzing ? <Loader2 className="animate-spin w-4 h-4"/> : <><Activity className="w-4 h-4"/> SYNTHESIZE WAVE</>}
                 </Button>
             </div>

             {/* Filter Tabs */}
             <div className="flex bg-neutral-900 rounded p-1 gap-1">
                {['ALL', 'GITHUB', 'HUGGINGFACE', 'MISTRAL'].map((src) => (
                    <button
                        key={src}
                        onClick={() => setActiveSource(src as any)}
                        className={`
                            flex-1 py-1 text-[9px] font-mono uppercase rounded transition-colors 
                            ${activeSource === src 
                                ? 'bg-orange-900/40 text-orange-200 border border-orange-900' 
                                : 'text-neutral-500 hover:text-orange-400'}
                        `}
                    >
                        {src}
                    </button>
                ))}
            </div>

             {/* Feed Display */}
             <div className="bg-neutral-900/50 rounded border border-neutral-800 p-2 min-h-[200px] max-h-[300px] overflow-y-auto custom-scrollbar space-y-2">
                 {filteredData.length === 0 && !loading && (
                     <div className="text-center text-xs text-neutral-600 mt-10">
                         No signals detected. Initiate Scan.
                     </div>
                 )}
                 {filteredData.map((item) => (
                     <div key={item.id} className="bg-neutral-950 border border-neutral-800 p-2 rounded group hover:border-orange-900/50 transition-colors">
                         <div className="flex justify-between items-start mb-1">
                             <div className="flex items-center gap-2">
                                 {item.id === 'irfan_kabir' && <Youtube className="w-3 h-3 text-red-500" />}
                                 {item.source === 'GITHUB' && item.id !== 'irfan_kabir' && <GitBranch className="w-3 h-3 text-neutral-500"/>}
                                 {item.source === 'HUGGINGFACE' && <Brain className="w-3 h-3 text-yellow-600"/>}
                                 {item.source === 'MISTRAL' && <Zap className="w-3 h-3 text-purple-400"/>}
                                 <span className="text-[10px] font-bold text-neutral-300">{item.title}</span>
                             </div>
                             <span className="text-[9px] font-mono text-orange-400 bg-orange-900/20 px-1 rounded">{item.metric}</span>
                         </div>
                         <p className="text-[10px] text-neutral-500 line-clamp-2">{item.description}</p>
                         <a href={item.url} target="_blank" rel="noreferrer" className="text-[9px] text-blue-500 hover:text-blue-400 mt-1 inline-block opacity-0 group-hover:opacity-100 transition-opacity">
                             View Source {'->'}
                         </a>
                     </div>
                 ))}
             </div>
        </div>
    );
};

export const MissionControlModule = ({ logs, onLog }: { logs: LogItem[], onLog: (l: LogItem) => void }) => {
    const [loading, setLoading] = useState(false);

    const handleGuidance = async () => {
        setLoading(true);
        // Add a "Ping" log to show user interaction
        onLog({ id: Date.now().toString(), timestamp: new Date(), sender: 'user', content: "Requesting Flight Director Oversight...", type: 'text' });
        
        try {
            const response = await GeminiService.getMissionGuidance(logs);
            
            const GuidanceOutput = () => (
                <div className="space-y-4 font-mono">
                    <div className="flex items-center justify-between border-b border-neutral-700 pb-2">
                         <div className="flex items-center gap-2">
                            <Radar className="w-5 h-5 text-indigo-400 animate-spin-slow" />
                            <span className="text-xs text-indigo-300 uppercase tracking-widest">Flight Director</span>
                         </div>
                         <div className="bg-neutral-900 px-2 py-0.5 rounded text-[10px] border border-neutral-800">
                             COHERENCE: <span className="text-white font-bold">{response.coherence_score}%</span>
                         </div>
                    </div>
                    
                    <div className="p-3 bg-indigo-950/20 border border-indigo-900/50 rounded-lg">
                        <div className="text-[10px] text-indigo-400 uppercase tracking-wider mb-1">Mission Status</div>
                        <div className="text-sm text-indigo-100 font-bold">{response.mission_status}</div>
                    </div>

                    <div className="text-sm italic text-neutral-400 border-l-2 border-neutral-700 pl-3 py-1">
                        "{response.analogy}"
                    </div>

                    <div className="space-y-2">
                        <div className="text-[10px] text-neutral-500 uppercase tracking-wider">Strategic Guidance</div>
                        <p className="text-xs text-neutral-300 leading-relaxed">{response.guidance}</p>
                    </div>

                    <div className="space-y-1">
                         <div className="text-[10px] text-neutral-500 uppercase tracking-wider">Projected Trajectory</div>
                         {response.next_steps.map((step, i) => (
                             <div key={i} className="flex items-center gap-2 text-xs text-neutral-400">
                                 <div className="w-1 h-1 bg-indigo-500 rounded-full"></div>
                                 {step}
                             </div>
                         ))}
                    </div>
                </div>
            );

            onLog({ 
                id: Date.now().toString() + '_guidance', 
                timestamp: new Date(), 
                sender: 'model', 
                content: <GuidanceOutput />, 
                type: 'info' 
            });

        } catch (e: any) {
             onLog({ id: Date.now().toString(), timestamp: new Date(), sender: 'system', content: `Error: ${e.message}`, type: 'error' });
        }
        setLoading(false);
    };

    return (
        <div className="space-y-4">
            <CodeContextVisualizer mode={loading ? 'processing' : 'text'} intensity={loading ? 1 : 0} />
            
            <div className="p-4 bg-neutral-900/40 rounded border border-neutral-800 text-center space-y-2">
                <h3 className="text-sm font-mono text-neutral-400 uppercase tracking-widest">Oversight Uplink</h3>
                <p className="text-[10px] text-neutral-500">
                    Scanning {logs.length} mission logs for context convergence.
                </p>
            </div>

            <Button onClick={handleGuidance} disabled={loading} active={loading} className="w-full h-12 text-indigo-200 bg-indigo-900/20 border-indigo-800 hover:bg-indigo-900/40">
                {loading ? <Loader2 className="animate-spin w-4 h-4" /> : <><Radar className="w-4 h-4"/> REQUEST FLIGHT GUIDANCE</>}
            </Button>
        </div>
    );
};

export const CodeReviewModule = ({ onLog }: { onLog: (l: LogItem) => void }) => {
    const [code, setCode] = useState('');
    const [grepQuery, setGrepQuery] = useState('');
    const [loading, setLoading] = useState(false);

    const handleAudit = async () => {
        if (!code) return;
        setLoading(true);
        onLog({ id: Date.now().toString(), timestamp: new Date(), sender: 'user', content: `Auditing Code (${code.length} chars). Query: ${grepQuery || 'Standard'}`, type: 'text' });
        
        try {
            const response = await GeminiService.performCodeAudit(code, grepQuery || "Find potential bugs and anti-patterns");
            
            const AuditOutput = () => {
                const getSeverityColor = (level: string) => {
                     switch(level) {
                        case 'critical': return 'text-red-500 bg-red-950/50 border-red-900';
                        case 'high': return 'text-orange-500 bg-orange-950/50 border-orange-900';
                        case 'medium': return 'text-yellow-500 bg-yellow-950/50 border-yellow-900';
                        default: return 'text-blue-400 bg-blue-950/50 border-blue-900';
                    }
                };

                return (
                    <div className="space-y-4 font-mono">
                        {/* Header Scorecard */}
                        <div className="flex items-center gap-4 border-b border-neutral-700 pb-3">
                            <div className="relative w-16 h-16 flex items-center justify-center">
                                <svg className="w-full h-full transform -rotate-90">
                                    <circle cx="32" cy="32" r="28" className="stroke-neutral-800" strokeWidth="6" fill="transparent" />
                                    <circle 
                                        cx="32" cy="32" r="28" 
                                        className={`${response.quality_score > 80 ? 'stroke-emerald-500' : response.quality_score > 50 ? 'stroke-yellow-500' : 'stroke-red-500'} transition-all duration-1000`} 
                                        strokeWidth="6" 
                                        fill="transparent" 
                                        strokeDasharray={175} 
                                        strokeDashoffset={175 - (175 * response.quality_score) / 100} 
                                    />
                                </svg>
                                <span className="absolute text-sm font-bold text-white">{response.quality_score}</span>
                            </div>
                            <div className="flex-1">
                                <h3 className="text-sm font-bold text-white uppercase tracking-wider">Audit Summary</h3>
                                <p className="text-xs text-neutral-400 leading-tight mt-1">{response.summary}</p>
                            </div>
                        </div>

                        {/* Semantic Grep Hits */}
                        {response.semantic_grep.matches.length > 0 && (
                            <div className="bg-neutral-900/50 rounded border border-neutral-800 overflow-hidden">
                                <div className="bg-neutral-950 px-3 py-1 text-[10px] font-bold text-neutral-500 uppercase flex items-center gap-2 border-b border-neutral-800">
                                    <ScanLine className="w-3 h-3 text-purple-400" />
                                    Semantic Grep: "{response.semantic_grep.query}"
                                </div>
                                <div className="divide-y divide-neutral-800/50">
                                    {response.semantic_grep.matches.map((m, i) => (
                                        <div key={i} className="p-2 hover:bg-neutral-800/20 transition-colors">
                                            <div className="flex justify-between items-start mb-1">
                                                <span className="text-purple-300 font-bold text-xs">Line {m.line}</span>
                                                <span className="text-[9px] text-neutral-500 bg-neutral-900 px-1 rounded">MATCH</span>
                                            </div>
                                            <div className="text-neutral-400 text-xs font-mono bg-black/30 p-1 rounded mb-1 border-l-2 border-purple-500/50">
                                                {m.content}
                                            </div>
                                            <div className="text-[10px] text-neutral-500 italic">{m.note}</div>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}

                        {/* Structured Audit Findings */}
                        <div className="space-y-2">
                             <div className="text-[10px] font-bold text-neutral-500 uppercase">Findings</div>
                             {response.structured_audit.map((issue, i) => (
                                 <div key={i} className={`p-3 rounded border ${getSeverityColor(issue.severity)}`}>
                                     <div className="flex justify-between items-start mb-1">
                                         <span className="font-bold text-xs flex items-center gap-2">
                                             <ShieldAlert className="w-3 h-3" />
                                             {issue.category.toUpperCase()}
                                         </span>
                                         <span className="text-[9px] uppercase font-bold px-1.5 py-0.5 rounded bg-black/20 border border-white/10">
                                             {issue.severity}
                                         </span>
                                     </div>
                                     <div className="text-xs opacity-90 mb-2">{issue.description}</div>
                                     {issue.line && <div className="text-[10px] bg-black/20 inline-block px-1 rounded mb-2 font-mono">Line {issue.line}</div>}
                                     <div className="text-[10px] opacity-70 border-t border-white/10 pt-2 flex gap-1">
                                         <span className="font-bold">FIX:</span> {issue.suggestion}
                                     </div>
                                 </div>
                             ))}
                        </div>
                    </div>
                );
            };

            onLog({ 
                id: Date.now().toString() + '_audit', 
                timestamp: new Date(), 
                sender: 'model', 
                content: <AuditOutput />, 
                type: 'info' 
            });

        } catch (e: any) {
             onLog({ id: Date.now().toString(), timestamp: new Date(), sender: 'system', content: `Error: ${e.message}`, type: 'error' });
        }
        setLoading(false);
    };

    return (
        <div className="space-y-4">
             <CodeContextVisualizer mode={loading ? 'processing' : 'text'} intensity={loading ? 1 : 0.2} />
             
             <div className="bg-neutral-900/50 rounded-lg p-2 border border-neutral-800">
                 <div className="flex justify-between items-center mb-2 px-1">
                    <span className="text-[10px] text-neutral-500 font-mono uppercase tracking-widest">Target Source Code</span>
                 </div>
                 <TextArea 
                    value={code}
                    onChange={(e: any) => setCode(e.target.value)}
                    placeholder="// Paste code here for analysis..."
                 />
             </div>

             <div className="bg-neutral-900/50 rounded-lg p-2 border border-neutral-800">
                 <Input 
                    value={grepQuery}
                    onChange={(e: any) => setGrepQuery(e.target.value)}
                    placeholder="Semantic Grep (Optional): e.g. 'Find memory leaks'"
                    onKeyDown={(e: any) => e.key === 'Enter' && handleAudit()}
                 />
             </div>
             
             <Button onClick={handleAudit} disabled={loading} active={loading} className="w-full text-purple-200 bg-purple-900/20 border-purple-800 hover:bg-purple-900/40">
                {loading ? <Loader2 className="animate-spin w-4 h-4" /> : <><ScanLine className="w-4 h-4"/> RUN AUDIT INTELLIGENCE</>}
             </Button>
        </div>
    );
};

export const DecisionModule = ({ onLog }: { onLog: (l: LogItem) => void }) => {
    const [context, setContext] = useState('');
    const [loading, setLoading] = useState(false);

    const handleConsult = async () => {
        if (!context) return;
        setLoading(true);
        onLog({ id: Date.now().toString(), timestamp: new Date(), sender: 'user', content: "SitRep: " + context, type: 'text' });
        
        try {
            const response = await GeminiService.consultArchitect(context);
            
             // Format Content - Heads Up Display Style
            const DecisionOutput = () => {
                const getRiskColor = (level: string) => {
                    switch(level) {
                        case 'critical': return 'text-red-500 border-red-900 bg-red-900/20';
                        case 'high': return 'text-orange-500 border-orange-900 bg-orange-900/20';
                        case 'medium': return 'text-yellow-500 border-yellow-900 bg-yellow-900/20';
                        default: return 'text-emerald-500 border-emerald-900 bg-emerald-900/20';
                    }
                };

                return (
                    <div className="space-y-4 font-mono">
                         {/* Main Recommendation Header */}
                         <div className="flex items-center justify-between border-b border-neutral-700 pb-2">
                             <div className="flex items-center gap-2">
                                <Scale className="w-5 h-5 text-blue-400" />
                                <span className="text-xs text-neutral-500 uppercase tracking-widest">Architect Recommendation</span>
                             </div>
                             <div className="flex items-center gap-2">
                                <span className="text-[10px] text-neutral-500 uppercase">Confidence</span>
                                <div className="h-2 w-16 bg-neutral-800 rounded-full overflow-hidden">
                                    <div className="h-full bg-blue-500 transition-all duration-1000" style={{width: `${response.confidence}%`}}></div>
                                </div>
                                <span className="text-xs text-blue-400">{response.confidence}%</span>
                             </div>
                         </div>

                         {/* The Big Decision */}
                         <div className="bg-neutral-900/50 p-4 border-l-4 border-blue-500 rounded-r">
                             <div className="text-xl font-bold text-white mb-1 tracking-tight">{response.recommendation}</div>
                             <div className="text-sm text-neutral-300">{response.reasoning}</div>
                         </div>

                         {/* Arkhipov Checks */}
                         <div className="grid grid-cols-3 gap-2">
                            <div className="bg-neutral-900 p-2 rounded border border-neutral-800">
                                <div className="text-[9px] text-neutral-500 uppercase mb-1">Emotion Check</div>
                                <div className="text-[10px] text-neutral-300 leading-tight">{response.arkhipov_check.emotional_state}</div>
                            </div>
                             <div className="bg-neutral-900 p-2 rounded border border-neutral-800">
                                <div className="text-[9px] text-neutral-500 uppercase mb-1">Verification</div>
                                <div className="text-[10px] text-neutral-300 leading-tight">{response.arkhipov_check.verification_needed}</div>
                            </div>
                             <div className="bg-neutral-900 p-2 rounded border border-neutral-800">
                                <div className="text-[9px] text-neutral-500 uppercase mb-1">Reversibility</div>
                                <div className="text-[10px] text-neutral-300 leading-tight">{response.arkhipov_check.reversibility}</div>
                            </div>
                         </div>

                         {/* Options Matrix */}
                         <div className="space-y-2 mt-4">
                             <div className="text-[10px] text-neutral-500 uppercase tracking-wider">Strategic Options</div>
                             {response.options.map((opt, i) => (
                                 <div key={i} className={`p-2 rounded border text-xs ${getRiskColor(opt.risk_level)} bg-opacity-10`}>
                                     <div className="flex justify-between font-bold mb-1">
                                         <span>{opt.label}</span>
                                         <span className="uppercase text-[9px] opacity-70 border px-1 rounded">{opt.risk_level} RISK</span>
                                     </div>
                                     <div className="grid grid-cols-2 gap-2 opacity-80">
                                         <div><span className="font-bold mr-1">+</span>{opt.pros}</div>
                                         <div><span className="font-bold mr-1">-</span>{opt.cons}</div>
                                     </div>
                                 </div>
                             ))}
                         </div>
                    </div>
                );
            };

            onLog({ 
                id: Date.now().toString() + '_dec', 
                timestamp: new Date(), 
                sender: 'model', 
                content: <DecisionOutput />, 
                type: 'info' 
            });

        } catch (e: any) {
             onLog({ id: Date.now().toString(), timestamp: new Date(), sender: 'system', content: `Error: ${e.message}`, type: 'error' });
        }
        setLoading(false);
    };

    return (
        <div className="space-y-4">
             <CodeContextVisualizer mode={loading ? 'processing' : 'text'} intensity={loading ? 1 : 0.2} />
             
             <div className="bg-neutral-900/50 rounded-lg p-2 border border-neutral-800">
                 <div className="flex justify-between items-center mb-2 px-1">
                    <span className="text-[10px] text-neutral-500 font-mono uppercase tracking-widest">Situation Report (SitRep)</span>
                 </div>
                 <TextArea 
                    value={context}
                    onChange={(e: any) => setContext(e.target.value)}
                    placeholder="Briefly describe the incident. E.g., 'Prod DB CPU at 99%, started after deployment X. Staging is stable. Users reporting 504s.'"
                 />
             </div>
             
             <Button onClick={handleConsult} disabled={loading} active={loading} className="w-full h-12 text-blue-200 bg-blue-900/20 border-blue-800 hover:bg-blue-900/40">
                {loading ? <Loader2 className="animate-spin w-4 h-4" /> : <><Scale className="w-4 h-4"/> CONSULT ARCHITECT</>}
             </Button>
        </div>
    );
};

export const ResearchModule = ({ onLog }: { onLog: (l: LogItem) => void }) => {
    const [query, setQuery] = useState('');
    const [loading, setLoading] = useState(false);

    const handleResearch = async () => {
        if (!query) return;
        setLoading(true);
        onLog({ id: Date.now().toString(), timestamp: new Date(), sender: 'user', content: "Researching: " + query, type: 'text' });
        
        try {
            const response = await GeminiService.performResearch(query);
            
             // Format Content
            const ResearchOutput = () => (
                <div className="space-y-4">
                     <div className="flex gap-2 mb-2 items-center">
                         <span className="text-[10px] bg-emerald-900/30 text-emerald-300 px-2 py-0.5 rounded border border-emerald-900/50 font-mono uppercase">LIVE REPORT</span>
                         {response.groundingUrls && (
                             <div className="flex gap-2">
                                 {response.groundingUrls.slice(0,3).map((url, i) => (
                                     <a key={i} href={url} target="_blank" rel="noreferrer" className="text-[9px] text-blue-400 hover:text-blue-300 flex items-center gap-1 bg-neutral-900 px-1 rounded">
                                         <Globe className="w-3 h-3" /> {new URL(url).hostname}
                                     </a>
                                 ))}
                             </div>
                         )}
                     </div>
                     <div className="prose prose-invert prose-sm max-w-none text-neutral-300">
                         {response.explanation.split('\n').map((line, i) => (
                             <p key={i} className="mb-2">{line}</p>
                         ))}
                     </div>
                </div>
            );

            onLog({ 
                id: Date.now().toString() + '_res', 
                timestamp: new Date(), 
                sender: 'model', 
                content: <ResearchOutput />, 
                type: 'info' 
            });

        } catch (e: any) {
             onLog({ id: Date.now().toString(), timestamp: new Date(), sender: 'system', content: `Error: ${e.message}`, type: 'error' });
        }
        setLoading(false);
    };

    return (
        <div className="space-y-4">
             <CodeContextVisualizer mode={loading ? 'processing' : 'text'} intensity={loading ? 1 : 0.2} />
             
             <div className="bg-neutral-900/50 rounded-lg p-2 border border-neutral-800">
                 <div className="flex justify-between items-center mb-2 px-1">
                    <span className="text-[10px] text-neutral-500 font-mono uppercase tracking-widest">Global Network Query</span>
                 </div>
                 <Input 
                    value={query}
                    onChange={(e: any) => setQuery(e.target.value)}
                    placeholder="Search query (e.g. latest python security vulnerabilities)..."
                 />
             </div>
             
             <Button onClick={handleResearch} disabled={loading} active={loading} className="w-full">
                {loading ? <Loader2 className="animate-spin w-4 h-4" /> : <><Search className="w-4 h-4"/> INITIATE SCAN</>}
             </Button>
        </div>
    );
};

export const DependencyModule = ({ onLog }: { onLog: (l: LogItem) => void }) => {
    const [reqs, setReqs] = useState('');
    const [loading, setLoading] = useState(false);

    const handleAnalyze = async () => {
        if (!reqs) return;
        setLoading(true);
        onLog({ id: Date.now().toString(), timestamp: new Date(), sender: 'user', content: "Analyze Dependencies:\n" + reqs, type: 'text' });
        
        try {
            const response = await GeminiService.analyzeDependencies(reqs);
            
             // Format Content
            const AnalysisOutput = () => (
                <div className="space-y-4">
                     <div className="flex gap-2 mb-2">
                         <span className="text-[10px] bg-emerald-900/30 text-emerald-300 px-2 py-0.5 rounded border border-emerald-900/50 font-mono uppercase">ANALYSIS REPORT</span>
                     </div>
                     <div className="prose prose-invert prose-sm max-w-none text-neutral-300">
                         {response.explanation.split('\n').map((line, i) => (
                             <p key={i} className="mb-2">{line}</p>
                         ))}
                     </div>
                     <ConceptVisualizer data={response} />
                </div>
            );

            onLog({ 
                id: Date.now().toString() + '_res', 
                timestamp: new Date(), 
                sender: 'model', 
                content: <AnalysisOutput />, 
                type: 'info' 
            });

        } catch (e: any) {
             onLog({ id: Date.now().toString(), timestamp: new Date(), sender: 'system', content: `Error: ${e.message}`, type: 'error' });
        }
        setLoading(false);
    };

    return (
        <div className="space-y-4">
             <CodeContextVisualizer mode={loading ? 'processing' : 'text'} intensity={loading ? 1 : 0.2} />
             
             <div className="bg-neutral-900/50 rounded-lg p-2 border border-neutral-800">
                 <div className="flex justify-between items-center mb-2 px-1">
                    <span className="text-[10px] text-neutral-500 font-mono uppercase tracking-widest">Requirements.txt / Package List</span>
                 </div>
                 <TextArea 
                    value={reqs}
                    onChange={(e: any) => setReqs(e.target.value)}
                    placeholder="Paste requirements.txt, package-lock.json, poetry.lock or list of packages..."
                 />
             </div>
             
             <Button onClick={handleAnalyze} disabled={loading} active={loading} className="w-full">
                {loading ? <Loader2 className="animate-spin w-4 h-4" /> : <><Package className="w-4 h-4"/> ANALYZE DEPENDENCIES</>}
             </Button>
        </div>
    );
};

export const ImageGenModule = ({ onLog }: { onLog: (l: LogItem) => void }) => {
  const [prompt, setPrompt] = useState('');
  const [aspectRatio, setAspectRatio] = useState<AspectRatio>('1:1');
  const [imageSize, setImageSize] = useState<ImageSize>('1K');
  const [loading, setLoading] = useState(false);

  const handleGenerate = async () => {
    if (!prompt) return;
    setLoading(true);
    onLog({ id: Date.now().toString(), timestamp: new Date(), sender: 'user', content: `Generate Image: ${prompt}`, type: 'text' });

    try {
      const images = await GeminiService.generateImagePro(prompt, aspectRatio, imageSize);
      if (images && images.length > 0) {
        onLog({
          id: Date.now().toString() + '_img',
          timestamp: new Date(),
          sender: 'model',
          content: <img src={images[0]} alt="Generated" className="rounded-lg border border-neutral-700 max-w-full" />,
          type: 'image'
        });
      }
    } catch (e: any) {
      onLog({ id: Date.now().toString(), timestamp: new Date(), sender: 'system', content: `Error: ${e.message}`, type: 'error' });
    }
    setLoading(false);
  };

  return (
    <div className="space-y-4">
       <div className="bg-neutral-900/50 rounded-lg p-2 border border-neutral-800">
           <TextArea value={prompt} onChange={(e: any) => setPrompt(e.target.value)} placeholder="Describe the image..." />
       </div>
       <div className="flex gap-2">
          <Select value={aspectRatio} onChange={(v: any) => setAspectRatio(v)} options={['1:1', '16:9', '9:16', '4:3', '3:4']} label="Ratio" />
          <Select value={imageSize} onChange={(v: any) => setImageSize(v)} options={['1K', '2K']} label="Size" />
       </div>
       <Button onClick={handleGenerate} disabled={loading} active={loading} className="w-full">
          {loading ? <Loader2 className="animate-spin w-4 h-4" /> : <><ImageIcon className="w-4 h-4"/> GENERATE</>}
       </Button>
    </div>
  );
};

export const ImageEditModule = ({ onLog }: { onLog: (l: LogItem) => void }) => {
  const [prompt, setPrompt] = useState('');
  const [image, setImage] = useState<string | null>(null);
  const [mimeType, setMimeType] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        const result = reader.result as string;
        // Strip prefix for API but keep for preview
        const base64Data = result.split(',')[1];
        setImage(base64Data);
        setMimeType(file.type);
        onLog({ id: Date.now().toString(), timestamp: new Date(), sender: 'user', content: <img src={result} className="max-w-[100px] rounded" alt="Upload"/>, type: 'image' });
      };
      reader.readAsDataURL(file);
    }
  };

  const handleEdit = async () => {
    if (!prompt || !image) return;
    setLoading(true);
    onLog({ id: Date.now().toString(), timestamp: new Date(), sender: 'user', content: `Edit Image: ${prompt}`, type: 'text' });

    try {
      const images = await GeminiService.editImage(image, mimeType, prompt);
      if (images && images.length > 0) {
        onLog({
          id: Date.now().toString() + '_edit',
          timestamp: new Date(),
          sender: 'model',
          content: <img src={images[0]} alt="Edited" className="rounded-lg border border-neutral-700 max-w-full" />,
          type: 'image'
        });
      }
    } catch (e: any) {
      onLog({ id: Date.now().toString(), timestamp: new Date(), sender: 'system', content: `Error: ${e.message}`, type: 'error' });
    }
    setLoading(false);
  };

  return (
    <div className="space-y-4">
       <div className="bg-neutral-900/50 rounded-lg p-2 border border-neutral-800">
           <input type="file" ref={fileInputRef} onChange={handleFileChange} className="hidden" accept="image/*" />
           <Button onClick={() => fileInputRef.current?.click()} className="w-full mb-2" variant="default">
              <ImageIcon className="w-4 h-4" /> {image ? "CHANGE IMAGE" : "UPLOAD SOURCE"}
           </Button>
           <TextArea value={prompt} onChange={(e: any) => setPrompt(e.target.value)} placeholder="Describe the edit..." />
       </div>
       <Button onClick={handleEdit} disabled={loading || !image} active={loading} className="w-full">
          {loading ? <Loader2 className="animate-spin w-4 h-4" /> : <><Wand2 className="w-4 h-4"/> EDIT IMAGE</>}
       </Button>
    </div>
  );
};

export const ThinkingModule = ({ onLog }: { onLog: (l: LogItem) => void }) => {
  const [prompt, setPrompt] = useState('');
  const [budget, setBudget] = useState(4096);
  const [loading, setLoading] = useState(false);

  const handleThink = async () => {
    if (!prompt) return;
    setLoading(true);
    onLog({ id: Date.now().toString(), timestamp: new Date(), sender: 'user', content: prompt, type: 'text' });

    try {
      const text = await GeminiService.thinkDeeply(prompt, budget);
      onLog({
          id: Date.now().toString() + '_think',
          timestamp: new Date(),
          sender: 'model',
          content: text,
          type: 'text'
      });
    } catch (e: any) {
      onLog({ id: Date.now().toString(), timestamp: new Date(), sender: 'system', content: `Error: ${e.message}`, type: 'error' });
    }
    setLoading(false);
  };

  return (
    <div className="space-y-4">
       <CodeContextVisualizer mode={loading ? 'processing' : 'text'} intensity={loading ? 1 : 0.2} />
       <div className="bg-neutral-900/50 rounded-lg p-2 border border-neutral-800">
           <TextArea value={prompt} onChange={(e: any) => setPrompt(e.target.value)} placeholder="Complex problem to solve..." />
       </div>
       <Range value={budget} min={1024} max={32768} step={1024} onChange={setBudget} label="Thinking Budget" formatValue={(v: number) => `${v} Tokens`} />
       <Button onClick={handleThink} disabled={loading} active={loading} className="w-full">
          {loading ? <Loader2 className="animate-spin w-4 h-4" /> : <><Brain className="w-4 h-4"/> REASON</>}
       </Button>
    </div>
  );
};

export const TTSModule = ({ onLog, onAudioData }: { onLog: (l: LogItem) => void, onAudioData: (buffer: AudioBuffer) => void }) => {
    const [text, setText] = useState('');
    const [voice, setVoice] = useState<VoiceName>('Kore');
    const [loading, setLoading] = useState(false);

    const handleSpeak = async () => {
        if (!text) return;
        setLoading(true);
        onLog({ id: Date.now().toString(), timestamp: new Date(), sender: 'user', content: `Say: "${text}"`, type: 'text' });
        
        try {
            const buffer = await GeminiService.generateSpeech(text, voice);
            if (buffer) {
                onAudioData(buffer);
                onLog({ id: Date.now().toString() + '_tts', timestamp: new Date(), sender: 'model', content: "Audio playing...", type: 'info' });
            }
        } catch (e: any) {
             onLog({ id: Date.now().toString(), timestamp: new Date(), sender: 'system', content: `Error: ${e.message}`, type: 'error' });
        }
        setLoading(false);
    };

    return (
        <div className="space-y-4">
             <CodeContextVisualizer mode={loading ? 'voice' : 'text'} intensity={loading ? 1 : 0.2} />
             <div className="bg-neutral-900/50 rounded-lg p-2 border border-neutral-800">
                <TextArea value={text} onChange={(e: any) => setText(e.target.value)} placeholder="Text to speech..." />
             </div>
             <Select value={voice} onChange={(v: any) => setVoice(v)} options={['Puck', 'Charon', 'Kore', 'Fenrir', 'Zephyr']} label="Voice" />
             <Button onClick={handleSpeak} disabled={loading} active={loading} className="w-full">
                {loading ? <Loader2 className="animate-spin w-4 h-4" /> : <><Play className="w-4 h-4"/> SPEAK</>}
             </Button>
        </div>
    );
};

export const LiveVoiceModule = ({ onLog, onAudioData }: { onLog: (l: LogItem) => void, onAudioData: (buffer: AudioBuffer) => void }) => {
    const [connected, setConnected] = useState(false);
    const [voice, setVoice] = useState<VoiceName>('Zephyr');
    const clientRef = useRef<LiveClient | null>(null);

    const toggleConnection = () => {
        if (connected) {
            clientRef.current?.disconnect();
            setConnected(false);
            onLog({ id: Date.now().toString(), timestamp: new Date(), sender: 'system', content: "Live session disconnected.", type: 'info' });
        } else {
            const client = new LiveClient({
                voiceName: voice,
                onOpen: () => {
                    setConnected(true);
                    onLog({ id: Date.now().toString(), timestamp: new Date(), sender: 'system', content: "Live session connected.", type: 'info' });
                },
                onMessage: (msg: LiveServerMessage) => {
                     // Handle text turns if needed
                     if (msg.serverContent?.turnComplete) {
                         // Optional: log turn completion
                     }
                },
                onError: (e) => {
                    onLog({ id: Date.now().toString(), timestamp: new Date(), sender: 'system', content: "Live Error", type: 'error' });
                    setConnected(false);
                },
                onClose: () => {
                    setConnected(false);
                    onLog({ id: Date.now().toString(), timestamp: new Date(), sender: 'system', content: "Live session closed.", type: 'info' });
                },
                onAudioData: (buffer) => {
                    onAudioData(buffer);
                }
            });
            client.connect();
            clientRef.current = client;
        }
    };

    return (
        <div className="space-y-4">
             <CodeContextVisualizer mode={connected ? 'voice' : 'idle'} intensity={connected ? 1 : 0} />
             <Select value={voice} onChange={(v: any) => setVoice(v)} options={['Puck', 'Charon', 'Kore', 'Fenrir', 'Zephyr']} label="Voice" />
             <Button onClick={toggleConnection} active={connected} variant={connected ? 'danger' : 'default'} className="w-full h-12">
                {connected ? <><StopCircle className="w-4 h-4"/> DISCONNECT LIVE</> : <><Mic className="w-4 h-4"/> CONNECT LIVE</>}
             </Button>
        </div>
    );
};

export const LogicLabModule = ({ onLog }: { onLog: (l: LogItem) => void }) => {
    const [question, setQuestion] = useState('');
    const [level, setLevel] = useState<LogicLevel>('intermediate');
    const [style, setStyle] = useState<LogicStyle>('step_by_step');
    const [diagramType, setDiagramType] = useState<DiagramType>('auto');
    const [loading, setLoading] = useState(false);

    const handleAsk = async () => {
        if (!question) return;
        setLoading(true);
        onLog({ id: Date.now().toString(), timestamp: new Date(), sender: 'user', content: question, type: 'text' });
        
        try {
            const response = await GeminiService.askLogicLab(question, level, style, 'medium', diagramType);
            
            const Output = () => (
                <div className="space-y-4">
                     <div className="prose prose-invert prose-sm max-w-none text-neutral-300">
                         {response.explanation.split('\n').map((line, i) => (
                             <p key={i} className="mb-2">{line}</p>
                         ))}
                     </div>
                     <ConceptVisualizer data={response} />
                </div>
            );

            onLog({ 
                id: Date.now().toString() + '_logic', 
                timestamp: new Date(), 
                sender: 'model', 
                content: <Output />, 
                type: 'info' 
            });

        } catch (e: any) {
             onLog({ id: Date.now().toString(), timestamp: new Date(), sender: 'system', content: `Error: ${e.message}`, type: 'error' });
        }
        setLoading(false);
    };

    const loadGridNode = (node: GridNode) => {
        setQuestion(node.defaultParams.question);
        setLevel(node.defaultParams.level);
        setStyle(node.defaultParams.style);
        setDiagramType(node.defaultParams.diagramType);
    };

    return (
        <div className="space-y-4">
             <CodeContextVisualizer mode={loading ? 'processing' : 'text'} intensity={loading ? 1 : 0.2} />
             
             {/* Grid Node Presets */}
             <div className="grid grid-cols-1 gap-2 mb-2">
                 <div className="text-[10px] text-neutral-500 font-mono uppercase tracking-widest">Load Grid Node</div>
                 <div className="flex gap-2 overflow-x-auto pb-1 custom-scrollbar">
                     {GRID_NODES.map(node => (
                         <button 
                            key={node.id} 
                            onClick={() => loadGridNode(node)}
                            className="bg-neutral-900 border border-neutral-800 rounded p-2 min-w-[140px] text-left hover:border-blue-500/50 hover:bg-neutral-800 transition-all group"
                         >
                             <div className="flex items-center gap-1.5 mb-1 text-blue-400 group-hover:text-blue-300">
                                <CircuitBoard className="w-3 h-3" />
                                <span className="text-[10px] font-bold truncate w-24">{node.title}</span>
                             </div>
                             <div className="text-[9px] text-neutral-500 truncate">{node.domain}</div>
                         </button>
                     ))}
                 </div>
             </div>

             <div className="bg-neutral-900/50 rounded-lg p-2 border border-neutral-800">
                 <TextArea value={question} onChange={(e: any) => setQuestion(e.target.value)} placeholder="Concept to explain..." />
             </div>
             
             <div className="space-y-2">
                 <div className="flex gap-2">
                     <Select value={level} onChange={(v: any) => setLevel(v)} options={['beginner', 'intermediate', 'advanced']} label="Level" />
                     <Select value={style} onChange={(v: any) => setStyle(v)} options={['step_by_step', 'summary']} label="Style" />
                 </div>
                 <Select value={diagramType} onChange={(v: any) => setDiagramType(v as DiagramType)} options={['auto', 'flow', 'automata', 'network', 'tree']} label="Diagram Type" />
             </div>

             <Button onClick={handleAsk} disabled={loading} active={loading} className="w-full">
                {loading ? <Loader2 className="animate-spin w-4 h-4" /> : <><Network className="w-4 h-4"/> EXPLAIN & VISUALIZE</>}
             </Button>
        </div>
    );
};

export const LocalBridgeModule = ({ onLog }: { onLog: (l: LogItem) => void }) => {
    const [serverUrl, setServerUrl] = useState('http://127.0.0.1:8080');
    const [status, setStatus] = useState<'disconnected' | 'connecting' | 'connected' | 'error'>('disconnected');
    const [activeTab, setActiveTab] = useState<'context' | 'daily' | 'experiments'>('context');
    const [query, setQuery] = useState('');
    const [loading, setLoading] = useState(false);

    const checkConnection = async () => {
        setStatus('connecting');
        onLog({ id: Date.now().toString(), timestamp: new Date(), sender: 'system', content: `Checking Uplink: ${serverUrl}...`, type: 'info' });
        
        try {
            const res = await fetch(`${serverUrl}/`);
            if (res.ok) {
                const data = await res.json();
                setStatus('connected');
                onLog({ id: Date.now().toString(), timestamp: new Date(), sender: 'system', content: `Connected to ${data.system} (${data.status}).`, type: 'info' });
            } else {
                throw new Error("Backend responded with error");
            }
        } catch (e: any) {
            setStatus('error');
            onLog({ id: Date.now().toString(), timestamp: new Date(), sender: 'system', content: `Connection Failed: Ensure backend/server.py is running on ${serverUrl}.`, type: 'error' });
        }
    };

    const handleAction = async (action: string, payload: any = {}) => {
        if (!query && action === 'query') return;
        setLoading(true);
        
        const endpointMap: any = {
            'INDEX_REPO': '/context/index',
            'query': '/context/query',
            'READ_LATEST': '/daily/latest',
            'SYNC_LOGS': '/daily/sync',
            'VIEW_HISTORY': '/experiments/history',
            'NEW_RUN': '/experiments/new'
        };

        const endpoint = endpointMap[action] || action;
        const fullUrl = `${serverUrl}${endpoint}`;
        
        let body = payload;
        if (action === 'query') body = { query };
        if (action === 'SYNC_LOGS') body = { content: query || "Manual sync trigger", tags: ["manual"] };
        
        onLog({ id: Date.now().toString(), timestamp: new Date(), sender: 'user', content: `[LOCAL_${activeTab.toUpperCase()}] ${action}`, type: 'text' });

        try {
            const method = action.includes('READ') || action.includes('VIEW') ? 'GET' : 'POST';
            const options: any = { method };
            if (method === 'POST') {
                options.headers = { 'Content-Type': 'application/json' };
                options.body = JSON.stringify(body);
            }

            const res = await fetch(fullUrl, options);
            const data = await res.json();
            
            onLog({ 
                id: Date.now().toString() + '_local_res', 
                timestamp: new Date(), 
                sender: 'model', 
                content: <pre className="text-xs font-mono overflow-x-auto">{JSON.stringify(data, null, 2)}</pre>, 
                type: 'info' 
            });

        } catch (e: any) {
             onLog({ id: Date.now().toString(), timestamp: new Date(), sender: 'system', content: `Action Failed: ${e.message}`, type: 'error' });
        }
        setLoading(false);
    };

    return (
        <div className="space-y-4">
            <CodeContextVisualizer mode={status === 'connected' ? 'processing' : 'idle'} intensity={status === 'connected' ? 0.5 : 0} />
            
            {/* Connection Header */}
            <div className="flex items-center gap-2 bg-neutral-900 p-2 rounded border border-neutral-800">
                <div className={`w-2 h-2 rounded-full ${status === 'connected' ? 'bg-[#3776ab]' : status === 'error' ? 'bg-red-500' : status === 'connecting' ? 'bg-[#ffd343] animate-bounce' : 'bg-neutral-600'}`}></div>
                <Input 
                    value={serverUrl} 
                    onChange={(e: any) => setServerUrl(e.target.value)} 
                    placeholder="http://127.0.0.1:8080" 
                    className="flex-1 bg-transparent border-none text-xs font-mono py-1"
                />
                <button onClick={checkConnection} className="p-1 hover:bg-neutral-800 rounded text-neutral-400 hover:text-white">
                    {status === 'connected' ? <Wifi className="w-4 h-4 text-[#3776ab]"/> : <WifiOff className="w-4 h-4"/>}
                </button>
            </div>

            {/* Mode Tabs */}
            <div className="flex bg-neutral-900 rounded p-1 gap-1">
                {['context', 'daily', 'experiments'].map((tab) => (
                    <button
                        key={tab}
                        onClick={() => setActiveTab(tab as any)}
                        className={`
                            flex-1 py-1 text-[10px] font-mono uppercase rounded transition-colors 
                            ${activeTab === tab 
                                ? 'bg-[#3776ab] text-white shadow-sm' 
                                : 'text-neutral-500 hover:text-[#ffd343]'}
                        `}
                    >
                        {tab}
                    </button>
                ))}
            </div>

            {/* Content Area */}
            <div className="bg-neutral-900/50 rounded border border-neutral-800 p-3 min-h-[120px] flex flex-col justify-between">
                {activeTab === 'context' && (
                    <div className="space-y-2">
                        <div className="text-[10px] text-[#ffd343] uppercase font-mono flex items-center gap-2"><Database className="w-3 h-3"/> Codebase Logic</div>
                        <p className="text-xs text-neutral-400">RAG interface for local repositories. Query logic, architecture, and definitions.</p>
                        <div className="grid grid-cols-2 gap-2">
                            <Button variant="python" onClick={() => handleAction('INDEX_REPO')} className="text-[10px] h-8">RE-INDEX</Button>
                            <Button variant="python" onClick={() => handleAction('query')} className="text-[10px] h-8">QUERY</Button>
                        </div>
                    </div>
                )}
                {activeTab === 'daily' && (
                    <div className="space-y-2">
                        <div className="text-[10px] text-[#ffd343] uppercase font-mono flex items-center gap-2"><FileText className="w-3 h-3"/> Daily Logs</div>
                        <p className="text-xs text-neutral-400">Sync daily standups and work logs to local filesystem markdown.</p>
                        <div className="grid grid-cols-2 gap-2">
                            <Button variant="python" onClick={() => handleAction('SYNC_LOGS', { content: query, tags: ["manual"] })} className="text-[10px] h-8">SYNC DISK</Button>
                            <Button variant="python" onClick={() => handleAction('READ_LATEST')} className="text-[10px] h-8">READ LATEST</Button>
                        </div>
                    </div>
                )}
                {activeTab === 'experiments' && (
                    <div className="space-y-2">
                        <div className="text-[10px] text-[#ffd343] uppercase font-mono flex items-center gap-2"><FlaskConical className="w-3 h-3"/> Research Lab</div>
                        <p className="text-xs text-neutral-400">Track experiment parameters and results in local JSON/CSV datasets.</p>
                        <div className="grid grid-cols-2 gap-2">
                            <Button variant="python" onClick={() => handleAction('NEW_RUN', { name: "New Experiment", parameters: { prompt: query } })} className="text-[10px] h-8">NEW RUN</Button>
                            <Button variant="python" onClick={() => handleAction('VIEW_HISTORY')} className="text-[10px] h-8">HISTORY</Button>
                        </div>
                    </div>
                )}
            </div>

            {/* Query Input */}
            <div className="flex gap-2">
                <Input 
                    value={query} 
                    onChange={(e: any) => setQuery(e.target.value)} 
                    placeholder={`Query local ${activeTab}...`} 
                    onKeyDown={(e: any) => e.key === 'Enter' && handleAction('query')}
                />
                <Button onClick={() => handleAction('query')} disabled={loading || !query} active={loading} className="w-20" variant="python">
                    {loading ? <Loader2 className="animate-spin w-4 h-4"/> : 'SEND'}
                </Button>
            </div>
        </div>
    );
};