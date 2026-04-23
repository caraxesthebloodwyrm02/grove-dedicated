import React, { useState, useRef, useEffect } from 'react';
import { ModuleType, LogItem } from './types';
import { 
  Wand2, 
  Image as ImageIcon, 
  Brain, 
  AudioWaveform, 
  Mic, 
  Terminal,
  Settings2,
  Trash2,
  Volume2,
  Network,
  Package,
  Globe,
  Scale,
  ScanLine,
  Radar,
  HardDrive,
  Activity
} from 'lucide-react';
import Visualizer from './components/Visualizer';
import { 
    ImageGenModule, 
    ImageEditModule, 
    ThinkingModule, 
    TTSModule, 
    LiveVoiceModule,
    LogicLabModule,
    DependencyModule,
    ResearchModule,
    DecisionModule,
    CodeReviewModule,
    MissionControlModule,
    LocalBridgeModule,
    OpenSourceRadarModule
} from './components/ModuleUI';

const App: React.FC = () => {
  const [activeModule, setActiveModule] = useState<ModuleType>(ModuleType.THINKING);
  const [logs, setLogs] = useState<LogItem[]>([]);
  const [audioContext, setAudioContext] = useState<AudioContext | null>(null);
  const [analyser, setAnalyser] = useState<AnalyserNode | null>(null);
  
  const logContainerRef = useRef<HTMLDivElement>(null);
  const nextAudioTimeRef = useRef<number>(0);

  // Initialize Audio Engine
  useEffect(() => {
    const ctx = new (window.AudioContext || (window as any).webkitAudioContext)({ sampleRate: 24000 });
    const ana = ctx.createAnalyser();
    ana.fftSize = 256;
    ana.smoothingTimeConstant = 0.5;
    
    // Create a compressor to avoid clipping
    const compressor = ctx.createDynamicsCompressor();
    compressor.connect(ctx.destination);
    ana.connect(compressor);

    setAudioContext(ctx);
    setAnalyser(ana);

    return () => { ctx.close(); };
  }, []);

  // Handle Audio Queuing
  const playAudioBuffer = (buffer: AudioBuffer) => {
    if (!audioContext || !analyser) return;

    const source = audioContext.createBufferSource();
    source.buffer = buffer;
    source.connect(analyser);

    const currentTime = audioContext.currentTime;
    // Schedule next
    const start = Math.max(currentTime, nextAudioTimeRef.current);
    source.start(start);
    nextAudioTimeRef.current = start + buffer.duration;
  };

  const addLog = (log: LogItem) => {
    setLogs(prev => [...prev, log]);
    setTimeout(() => {
        if (logContainerRef.current) {
            logContainerRef.current.scrollTop = logContainerRef.current.scrollHeight;
        }
    }, 100);
  };

  const readText = (text: string) => {
      if ('speechSynthesis' in window) {
          const utterance = new SpeechSynthesisUtterance(text);
          utterance.rate = 1.0;
          utterance.pitch = 1.0;
          window.speechSynthesis.speak(utterance);
      }
  };

  const renderModuleIcon = (type: ModuleType) => {
      switch(type) {
          case ModuleType.IMAGE_GEN: return <ImageIcon className="w-5 h-5" />;
          case ModuleType.IMAGE_EDIT: return <Wand2 className="w-5 h-5" />;
          case ModuleType.THINKING: return <Brain className="w-5 h-5" />;
          case ModuleType.LIVE_VOICE: return <Mic className="w-5 h-5" />;
          case ModuleType.TTS: return <AudioWaveform className="w-5 h-5" />;
          case ModuleType.LOGIC_LAB: return <Network className="w-5 h-5" />;
          case ModuleType.DEPENDENCY_MANAGER: return <Package className="w-5 h-5" />;
          case ModuleType.RESEARCH: return <Globe className="w-5 h-5" />;
          case ModuleType.DECISION_HELPER: return <Scale className="w-5 h-5" />;
          case ModuleType.CODE_REVIEW: return <ScanLine className="w-5 h-5" />;
          case ModuleType.MISSION_CONTROL: return <Radar className="w-5 h-5" />;
          case ModuleType.LOCAL_BRIDGE: return <HardDrive className="w-5 h-5" />;
          case ModuleType.SINE_WAVEFORM: return <Activity className="w-5 h-5" />;
      }
  };

  const navItems = [
      { type: ModuleType.LOGIC_LAB, label: "Logic Lab", desc: "Interactive Logic & Network Diagrams" },
      { type: ModuleType.THINKING, label: "Deep Think", desc: "Advanced Reasoning & Problem Solving" },
      { type: ModuleType.IMAGE_GEN, label: "Generator", desc: "High-Fidelity Image Creation" },
      { type: ModuleType.IMAGE_EDIT, label: "Editor", desc: "Context-Aware Image Modification" },
      { type: ModuleType.TTS, label: "Synthesizer", desc: "Neural Text-to-Speech" },
      { type: ModuleType.LIVE_VOICE, label: "Live Voice", desc: "Real-time Multimodal Conversation" },
      { type: ModuleType.DEPENDENCY_MANAGER, label: "Dep. Manager", desc: "Library & Lockfile Analysis" },
      { type: ModuleType.RESEARCH, label: "Research", desc: "Live Search & Grounding" },
      { type: ModuleType.DECISION_HELPER, label: "Decision", desc: "Arkhipov-style Strategic Support" },
      { type: ModuleType.CODE_REVIEW, label: "Code Audit", desc: "Semantic Grep & Structured Audit" },
      { type: ModuleType.MISSION_CONTROL, label: "Mission Ctrl", desc: "Session Oversight & Flight Guidance" },
      { type: ModuleType.LOCAL_BRIDGE, label: "Local Bridge", desc: "Backend Integration & File System" },
      { type: ModuleType.SINE_WAVEFORM, label: "SineWaveform", desc: "Open Source Intelligence Radar" },
  ];

  return (
    <div className="w-screen h-screen bg-neutral-950 text-neutral-200 flex flex-col overflow-hidden font-sans">
      
      {/* Visual Layer Background */}
      <div className="absolute inset-0 z-0 opacity-40">
        <Visualizer 
            type={activeModule} 
            isActive={true} 
            audioAnalyser={analyser || undefined} 
        />
      </div>

      {/* Header */}
      <header className="z-10 h-16 border-b border-neutral-800 bg-neutral-900/80 backdrop-blur-sm flex items-center justify-between px-6 flex-shrink-0">
        <div className="flex items-center gap-3">
            <div className="w-8 h-8 bg-blue-600 rounded flex items-center justify-center shadow-[0_0_15px_rgba(37,99,235,0.4)]">
                <Terminal className="text-white w-5 h-5" />
            </div>
            <h1 className="font-bold tracking-tight text-lg text-white">GEMINI <span className="font-light text-neutral-400">STUDIO</span></h1>
        </div>
        <div className="flex gap-1 bg-neutral-950 p-1 rounded-lg border border-neutral-800 overflow-x-auto max-w-[calc(100vw-300px)] custom-scrollbar">
            {navItems.map(item => (
                <button
                    key={item.type}
                    onClick={() => setActiveModule(item.type)}
                    className={`
                        flex items-center gap-2 px-3 py-1.5 rounded text-xs font-medium transition-all duration-300 whitespace-nowrap relative group
                        ${activeModule === item.type 
                            ? 'bg-neutral-800 text-white shadow-sm border border-neutral-700' 
                            : 'text-neutral-500 hover:text-neutral-300 hover:bg-neutral-900 border border-transparent'}
                    `}
                >
                    {renderModuleIcon(item.type)}
                    {item.label}
                    
                    {/* Tooltip */}
                    <div className="absolute top-full mt-2 left-1/2 -translate-x-1/2 w-48 p-2 bg-black border border-neutral-800 rounded shadow-xl text-[10px] text-neutral-400 text-center opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none z-50">
                        {item.desc}
                    </div>
                </button>
            ))}
        </div>
        <div className="w-8 h-8">
            {/* Settings or profile placeholder */}
            <Settings2 className="w-5 h-5 text-neutral-600 hover:text-white cursor-pointer" />
        </div>
      </header>

      {/* Main Workspace */}
      <main className="z-10 flex-1 flex gap-6 p-6 overflow-hidden">
        
        {/* Output/Log Console */}
        <div className="flex-1 bg-neutral-900/60 backdrop-blur-md rounded-xl border border-neutral-800 flex flex-col shadow-2xl overflow-hidden relative">
            <div className="h-10 border-b border-neutral-800 bg-neutral-950/50 flex items-center justify-between px-4">
                <span className="text-xs font-mono text-neutral-500 uppercase tracking-widest">Console Output</span>
                <button onClick={() => setLogs([])} className="text-neutral-600 hover:text-red-400">
                    <Trash2 className="w-4 h-4" />
                </button>
            </div>
            <div ref={logContainerRef} className="flex-1 overflow-y-auto p-4 space-y-4 font-mono text-sm scroll-smooth">
                {logs.length === 0 && (
                    <div className="h-full flex items-center justify-center text-neutral-600 italic">
                        Ready for input...
                    </div>
                )}
                {logs.map((log) => (
                    <div key={log.id} className={`flex flex-col gap-1 ${log.sender === 'user' ? 'items-end' : 'items-start'}`}>
                        <div className={`
                            max-w-[80%] rounded px-4 py-3 border relative group
                            ${log.sender === 'user' 
                                ? 'bg-neutral-800 border-neutral-700 text-neutral-200' 
                                : log.type === 'error' 
                                    ? 'bg-red-900/20 border-red-900/50 text-red-200'
                                    : log.type === 'info'
                                      ? 'bg-neutral-900/80 border-neutral-800 text-neutral-200 shadow-xl w-full max-w-2xl'
                                      : 'bg-black/40 border-neutral-800 text-blue-100 shadow-[0_0_20px_rgba(0,0,0,0.2)]'
                            }
                        `}>
                           {typeof log.content === 'string' ? (
                               <>
                                   <div className="whitespace-pre-wrap leading-relaxed">{log.content}</div>
                                   {/* Quick Text Reader */}
                                   <button 
                                        onClick={() => readText(log.content as string)}
                                        className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity bg-neutral-950/50 p-1.5 rounded-full hover:bg-blue-600/50 text-neutral-400 hover:text-white"
                                        title="Read Aloud"
                                   >
                                       <Volume2 className="w-3 h-3" />
                                   </button>
                               </>
                           ) : (
                               <div className="overflow-hidden w-full">{log.content}</div>
                           )}
                        </div>
                        <span className="text-[10px] text-neutral-600 px-1">{log.timestamp.toLocaleTimeString()}</span>
                    </div>
                ))}
            </div>
        </div>

        {/* Input/Control Rack */}
        <div className="w-[400px] flex-shrink-0 flex flex-col gap-4">
            
            {/* Active Module Panel */}
            <div className="bg-neutral-900/80 backdrop-blur-xl rounded-xl border border-neutral-700/50 shadow-2xl p-1 transition-all duration-300">
                <div className="p-4 border-b border-neutral-800/50 mb-4 bg-gradient-to-r from-neutral-800/50 to-transparent rounded-t-lg">
                    <div className="flex items-center gap-2 text-white">
                        {renderModuleIcon(activeModule)}
                        <h2 className="font-bold tracking-wider text-sm">
                            {navItems.find(n => n.type === activeModule)?.label.toUpperCase()}
                        </h2>
                    </div>
                    <p className="text-xs text-neutral-500 mt-1">Configure parameters and process input.</p>
                </div>
                
                <div className="px-4 pb-6">
                    {activeModule === ModuleType.IMAGE_GEN && <ImageGenModule onLog={addLog} />}
                    {activeModule === ModuleType.IMAGE_EDIT && <ImageEditModule onLog={addLog} />}
                    {activeModule === ModuleType.THINKING && <ThinkingModule onLog={addLog} />}
                    {activeModule === ModuleType.TTS && <TTSModule onLog={addLog} onAudioData={playAudioBuffer} />}
                    {activeModule === ModuleType.LIVE_VOICE && <LiveVoiceModule onLog={addLog} onAudioData={playAudioBuffer} />}
                    {activeModule === ModuleType.LOGIC_LAB && <LogicLabModule onLog={addLog} />}
                    {activeModule === ModuleType.DEPENDENCY_MANAGER && <DependencyModule onLog={addLog} />}
                    {activeModule === ModuleType.RESEARCH && <ResearchModule onLog={addLog} />}
                    {activeModule === ModuleType.DECISION_HELPER && <DecisionModule onLog={addLog} />}
                    {activeModule === ModuleType.CODE_REVIEW && <CodeReviewModule onLog={addLog} />}
                    {activeModule === ModuleType.MISSION_CONTROL && <MissionControlModule logs={logs} onLog={addLog} />}
                    {activeModule === ModuleType.LOCAL_BRIDGE && <LocalBridgeModule onLog={addLog} />}
                    {activeModule === ModuleType.SINE_WAVEFORM && <OpenSourceRadarModule onLog={addLog} />}
                </div>
            </div>

            {/* Info Panel / Status */}
            <div className="flex-1 bg-neutral-900/40 rounded-xl border border-neutral-800 p-4 relative overflow-hidden">
                <div className="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-10"></div>
                <h3 className="text-xs font-mono text-neutral-500 mb-2 uppercase">System Status</h3>
                <div className="grid grid-cols-2 gap-2 text-xs font-mono">
                    <div className="bg-neutral-950 p-2 rounded border border-neutral-800">
                        <div className="text-neutral-500">Audio Ctx</div>
                        <div className={audioContext?.state === 'running' ? 'text-green-500' : 'text-yellow-500'}>
                            {audioContext?.state.toUpperCase() || 'INIT'}
                        </div>
                    </div>
                    <div className="bg-neutral-950 p-2 rounded border border-neutral-800">
                        <div className="text-neutral-500">Model</div>
                        <div className="text-blue-400 truncate">
                            {activeModule === ModuleType.IMAGE_GEN && 'Gemini 3 Pro Img'}
                            {activeModule === ModuleType.IMAGE_EDIT && 'Gemini 2.5 Flash'}
                            {activeModule === ModuleType.THINKING && 'Gemini 3 Pro'}
                            {activeModule === ModuleType.TTS && 'Gemini 2.5 Flash TTS'}
                            {activeModule === ModuleType.LIVE_VOICE && 'Gemini 2.5 Live'}
                            {activeModule === ModuleType.LOGIC_LAB && 'Gemini 3 Pro + Vis'}
                            {activeModule === ModuleType.DEPENDENCY_MANAGER && 'Gemini 3 Pro + Deps'}
                            {activeModule === ModuleType.RESEARCH && 'Gemini 2.5 Flash'}
                            {activeModule === ModuleType.DECISION_HELPER && 'Gemini 3 Pro + Search'}
                            {activeModule === ModuleType.CODE_REVIEW && 'Gemini 3 Pro + Grep'}
                            {activeModule === ModuleType.MISSION_CONTROL && 'Gemini 3 Pro (Oversight)'}
                            {activeModule === ModuleType.LOCAL_BRIDGE && 'Gemini 3 Pro (Bridge)'}
                            {activeModule === ModuleType.SINE_WAVEFORM && 'Gemini 3 Pro (Wave)'}
                        </div>
                    </div>
                </div>
                
                <div className="mt-4 text-[10px] text-neutral-600 leading-normal">
                    <p>Mothership Cockpit Online.</p>
                    <p>Select a module to begin.</p>
                </div>
            </div>
        </div>

      </main>
    </div>
  );
};

export default App;