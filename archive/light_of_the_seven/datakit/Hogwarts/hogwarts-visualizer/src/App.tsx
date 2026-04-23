import React, { useMemo, useState } from 'react';
import {
  Activity,
  BookOpen,
  Brain,
  Database,
  Download,
  Snowflake,
  Wand2,
} from 'lucide-react';
import hogwartsLore from './datasets/hogwarts_lore.json';
import greatHallReceipt from './datasets/great_hall_receipt.json';
import greatHallTable from './datasets/great_hall_discussion_table.json';
import type { AiResponse, AnalyzerFrame, Dataset, MacroKnobs } from './lib/types';
import { mockAiRespond } from './lib/mockAi';
import { usePresets } from './lib/usePresets';

const DEFAULT_KNOBS: MacroKnobs = {
  canon_tightness: 60,
  signal_clarity: 75,
  noise: 40,
  auth: 70,
  bandwidth: 55,
  emotion_gain: 65,
  mystery: 45,
  practicality: 50,
};

type BuiltInDatasetId = 'hogwarts_lore' | 'great_hall';

type DatasetState =
  | { kind: 'built_in'; id: BuiltInDatasetId }
  | { kind: 'user_json'; name: string; data: unknown };

function clamp01(x: number): number {
  return Math.max(0, Math.min(1, x));
}

function pct(x: number): number {
  return Math.max(0, Math.min(100, Math.round(x)));
}

function computeAnalyzerFrame(args: { dataset: Dataset; knobs: MacroKnobs }): AnalyzerFrame {
  const k = args.knobs;

  let baseClarity = 0.55;
  let baseNoise = 0.45;
  let baseAuth = 0.55;
  let baseBandwidth = 0.5;
  let baseMystery = 0.5;

  if (args.dataset.meta.kind === 'hogwarts_lore') {
    const d = args.dataset.data as any;
    const presetsCount = d?.patronus_presets ? Object.keys(d.patronus_presets).length : 0;
    const housesCount = d?.houses ? Object.keys(d.houses).length : 0;

    baseClarity = clamp01(0.35 + presetsCount * 0.08);
    baseNoise = clamp01(0.25 + (k.noise / 100) * 0.5);
    baseAuth = clamp01(0.4 + (k.auth / 100) * 0.5);
    baseBandwidth = clamp01(0.3 + presetsCount * 0.06);
    baseMystery = clamp01(0.3 + housesCount * 0.12);
  }

  if (args.dataset.meta.kind === 'great_hall') {
    const d = args.dataset.data as any;
    const rows = Array.isArray(d?.table) ? d.table.length : 0;
    const decisions = Array.isArray(d?.receipt?.decisions) ? d.receipt.decisions.length : 0;

    baseClarity = clamp01(0.25 + (k.signal_clarity / 100) * 0.6);
    baseNoise = clamp01(0.2 + rows * 0.04 + (k.noise / 100) * 0.2);
    baseAuth = clamp01(0.25 + decisions * 0.25 + (k.auth / 100) * 0.3);
    baseBandwidth = clamp01(0.35 + (k.bandwidth / 100) * 0.4);
    baseMystery = clamp01(0.25 + (k.mystery / 100) * 0.45);
  }

  const clarity = clamp01(baseClarity * (0.5 + (k.signal_clarity / 100) * 0.9));
  const noise = clamp01(baseNoise * (0.4 + (k.noise / 100) * 1.1));
  const auth = clamp01(baseAuth * (0.5 + (k.auth / 100) * 0.9));
  const density = clamp01(baseBandwidth * (0.5 + (k.bandwidth / 100) * 0.9));
  const mystery = clamp01(baseMystery * (0.5 + (k.mystery / 100) * 0.9));

  const collision = clamp01(noise * 0.6 + density * 0.3 - clarity * 0.2);
  const emotion = clamp01((k.emotion_gain / 100) * 0.9 + clarity * 0.2 - collision * 0.4);

  return {
    bands: [
      { id: 'clarity', label: 'Clarity', value: pct(clarity * 100), color: '#60a5fa' },
      { id: 'noise', label: 'Noise', value: pct(noise * 100), color: '#f87171' },
      { id: 'auth', label: 'Auth', value: pct(auth * 100), color: '#34d399' },
      { id: 'density', label: 'Bandwidth', value: pct(density * 100), color: '#fbbf24' },
      { id: 'mystery', label: 'Mystery', value: pct(mystery * 100), color: '#a78bfa' },
      { id: 'collision', label: 'Masking', value: pct(collision * 100), color: '#fb7185' },
      { id: 'emotion', label: 'Emotion', value: pct(emotion * 100), color: '#f472b6' },
    ],
    note: 'Analyzer output is mock-first: dataset + macro knobs -> spectrum bands.',
  };
}

function BarSpectrum({ frame }: { frame: AnalyzerFrame }) {
  return (
    <div className="bg-zinc-950/50 border border-zinc-800/60 rounded-xl p-4 shadow-sm shadow-black/30">
      <div className="flex items-center justify-between mb-3">
        <div className="text-[10px] font-mono text-neutral-500 uppercase tracking-widest">
          Analyzer
        </div>
        <div className="text-[10px] font-mono text-neutral-600">SPECTRUM</div>
      </div>

      <div className="grid grid-cols-7 gap-2 items-end h-44">
        {frame.bands.map((b) => (
          <div key={b.id} className="flex flex-col items-center gap-2">
            <div className="w-full flex-1 flex items-end">
              <div
                className="w-full rounded-sm border border-zinc-800/70"
                style={{ height: `${b.value}%`, backgroundColor: `${b.color}33` }}
              />
            </div>
            <div className="text-[9px] font-mono text-neutral-400 uppercase tracking-tight">
              {b.label}
            </div>
            <div className="text-[10px] font-mono" style={{ color: b.color }}>
              {b.value}
            </div>
          </div>
        ))}
      </div>

      {frame.note && (
        <div className="mt-3 text-[10px] font-mono text-neutral-600">{frame.note}</div>
      )}
    </div>
  );
}

function MacroRack({
  knobs,
  onChange,
}: {
  knobs: MacroKnobs;
  onChange: (k: MacroKnobs) => void;
}) {
  const set = (id: keyof MacroKnobs, v: number) => {
    onChange({ ...knobs, [id]: v });
  };

  const knobDefs: Array<{ id: keyof MacroKnobs; label: string; accent: string }> = [
    { id: 'canon_tightness', label: 'Canon', accent: '#9ca3af' },
    { id: 'signal_clarity', label: 'Clarity', accent: '#60a5fa' },
    { id: 'noise', label: 'Noise', accent: '#f87171' },
    { id: 'auth', label: 'Auth', accent: '#34d399' },
    { id: 'bandwidth', label: 'Bandwidth', accent: '#fbbf24' },
    { id: 'emotion_gain', label: 'Emotion', accent: '#f472b6' },
    { id: 'mystery', label: 'Mystery', accent: '#a78bfa' },
    { id: 'practicality', label: 'Practicality', accent: '#22c55e' },
  ];

  return (
    <div className="bg-zinc-950/30 border border-zinc-800/60 rounded-xl p-4 shadow-sm shadow-black/30">
      <div className="flex items-center justify-between mb-3">
        <div className="text-[10px] font-mono text-neutral-500 uppercase tracking-widest">
          Macro Rack
        </div>
        <div className="text-[10px] font-mono text-neutral-600">KNOBS</div>
      </div>

      <div className="space-y-3">
        {knobDefs.map((k) => (
          <div key={k.id} className="space-y-1">
            <div className="flex items-center justify-between">
              <div className="text-[10px] font-mono text-neutral-400 uppercase tracking-wider">
                {k.label}
              </div>
              <div className="text-[10px] font-mono" style={{ color: k.accent }}>
                {knobs[k.id]}
              </div>
            </div>
            <input
              type="range"
              min={0}
              max={100}
              value={knobs[k.id]}
              onChange={(e) => set(k.id, Number(e.target.value))}
              className="w-full h-1 bg-neutral-800 rounded-lg appearance-none cursor-pointer"
              style={{ accentColor: k.accent }}
            />
          </div>
        ))}
      </div>
    </div>
  );
}

function DatasetPanel({
  datasetState,
  onSetBuiltIn,
  onLoadFile,
}: {
  datasetState: DatasetState;
  onSetBuiltIn: (id: BuiltInDatasetId) => void;
  onLoadFile: (name: string, data: unknown) => void;
}) {
  const [error, setError] = useState<string | null>(null);

  return (
    <div className="bg-zinc-950/30 border border-zinc-800/60 rounded-xl p-4 shadow-sm shadow-black/30">
      <div className="flex items-center justify-between mb-3">
        <div className="text-[10px] font-mono text-neutral-500 uppercase tracking-widest">
          Data
        </div>
        <div className="text-[10px] font-mono text-neutral-600">DATASETS</div>
      </div>

      <div className="grid grid-cols-2 gap-2">
        <button
          onClick={() => onSetBuiltIn('hogwarts_lore')}
          className={`px-3 py-2 rounded border text-left transition-colors ${
            datasetState.kind === 'built_in' && datasetState.id === 'hogwarts_lore'
              ? 'bg-white/5 border-zinc-700/70 text-white'
              : 'bg-transparent border-zinc-800/60 text-zinc-300 hover:bg-white/5 hover:text-white'
          }`}
        >
          <div className="flex items-center gap-2">
            <Wand2 className="w-4 h-4 text-sky-400" />
            <div>
              <div className="text-xs font-semibold">Hogwarts Lore</div>
              <div className="text-[10px] text-neutral-500">Presets + houses</div>
            </div>
          </div>
        </button>

        <button
          onClick={() => onSetBuiltIn('great_hall')}
          className={`px-3 py-2 rounded border text-left transition-colors ${
            datasetState.kind === 'built_in' && datasetState.id === 'great_hall'
              ? 'bg-white/5 border-zinc-700/70 text-white'
              : 'bg-transparent border-zinc-800/60 text-zinc-300 hover:bg-white/5 hover:text-white'
          }`}
        >
          <div className="flex items-center gap-2">
            <BookOpen className="w-4 h-4 text-sky-400" />
            <div>
              <div className="text-xs font-semibold">Great Hall</div>
              <div className="text-[10px] text-neutral-500">Ledger + receipt</div>
            </div>
          </div>
        </button>
      </div>

      <div className="mt-3">
        <label className="block text-[10px] font-mono text-neutral-500 uppercase tracking-widest mb-2">
          Import JSON
        </label>
        <input
          type="file"
          accept="application/json"
          className="block w-full text-xs text-neutral-400 file:mr-4 file:py-2 file:px-3 file:rounded file:border-0 file:text-xs file:font-semibold file:bg-neutral-800 file:text-neutral-100 hover:file:bg-neutral-700"
          onChange={(e) => {
            setError(null);
            const file = e.target.files?.[0];
            if (!file) return;
            const reader = new FileReader();
            reader.onload = () => {
              try {
                const raw = String(reader.result ?? '');
                const json = JSON.parse(raw);
                onLoadFile(file.name, json);
              } catch (err) {
                setError(err instanceof Error ? err.message : 'Failed to parse JSON');
              }
            };
            reader.readAsText(file);
          }}
        />
        {error && <div className="mt-2 text-xs text-red-400">{error}</div>}
      </div>
    </div>
  );
}

function jsonPreview(value: unknown, maxChars: number): string {
  try {
    const s = JSON.stringify(value, null, 2);
    if (s.length <= maxChars) return s;
    return `${s.slice(0, maxChars)}\n...`;
  } catch {
    return '[unserializable]';
  }
}

export default function App() {
  const [datasetState, setDatasetState] = useState<DatasetState>({
    kind: 'built_in',
    id: 'hogwarts_lore',
  });

  const dataset: Dataset = useMemo(() => {
    if (datasetState.kind === 'built_in') {
      if (datasetState.id === 'hogwarts_lore') {
        return {
          meta: {
            id: 'hogwarts_lore',
            kind: 'hogwarts_lore',
            name: 'Hogwarts Lore',
            description: 'Patronus presets + house palettes',
          },
          data: hogwartsLore,
        };
      }

      return {
        meta: {
          id: 'great_hall',
          kind: 'great_hall',
          name: 'Great Hall',
          description: 'Discussion table + receipt',
        },
        data: {
          table: greatHallTable,
          receipt: greatHallReceipt,
        },
      };
    }

    return {
      meta: {
        id: 'user_json',
        kind: 'user_json',
        name: datasetState.name,
        description: 'User imported JSON',
      },
      data: datasetState.data,
    };
  }, [datasetState]);

  const [knobs, setKnobs] = useState<MacroKnobs>(DEFAULT_KNOBS);
  const [freeze, setFreeze] = useState(false);
  const [frozenFrame, setFrozenFrame] = useState<AnalyzerFrame | null>(null);

  const frame = useMemo(() => {
    if (freeze && frozenFrame) return frozenFrame;
    return computeAnalyzerFrame({ dataset, knobs });
  }, [dataset, knobs, freeze, frozenFrame]);

  const { presets, newPresetName, setNewPresetName, savePreset, deletePreset, loadPreset } =
    usePresets<MacroKnobs>('hogwarts-visualizer:macro-presets', knobs, (data) => setKnobs(data));

  const [assistantQuery, setAssistantQuery] = useState('');
  const [assistantResponse, setAssistantResponse] = useState<AiResponse>(() =>
    mockAiRespond({ query: '', dataset, knobs }),
  );

  const applyAiAction = (id: string) => {
    if (id === 'dataset:great_hall') setDatasetState({ kind: 'built_in', id: 'great_hall' });
    if (id === 'dataset:hogwarts_lore') setDatasetState({ kind: 'built_in', id: 'hogwarts_lore' });

    if (id === 'demo:set_knobs_signal') {
      setKnobs({
        canon_tightness: 75,
        signal_clarity: 85,
        noise: 45,
        auth: 90,
        bandwidth: 60,
        emotion_gain: 70,
        mystery: 55,
        practicality: 50,
      });
    }

    if (id === 'demo:set_knobs_balanced') {
      setKnobs(DEFAULT_KNOBS);
    }

    if (id === 'demo:freeze') {
      const current = computeAnalyzerFrame({ dataset, knobs });
      setFrozenFrame(current);
      setFreeze(true);
    }
  };

  const exportReceipt = () => {
    const receipt = {
      app: {
        name: 'hogwarts-visualizer',
        version: '0.1.0',
      },
      dataset: dataset.meta,
      knobs,
      analyzer: frame,
      at: new Date().toISOString(),
    };

    const blob = new Blob([JSON.stringify(receipt, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `hogwarts_visualizer_receipt_${Date.now()}.json`;
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="h-screen w-screen overflow-hidden">
      <div className="h-full w-full grid grid-rows-[56px_1fr]">
        <header className="flex items-center justify-between px-4 border-b border-zinc-800/60 bg-zinc-950/70 backdrop-blur-md">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-white/5 border border-zinc-800/70 flex items-center justify-center shadow-sm shadow-black/30">
              <Database className="w-5 h-5 text-sky-400" />
            </div>
            <div className="leading-tight">
              <div className="text-sm font-semibold">Hogwarts Visualizer</div>
              <div className="text-[10px] font-mono text-neutral-500">data analysis workbench</div>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <div className="hidden md:flex items-center gap-2 text-xs">
              <span className="px-2 py-1 rounded border border-zinc-800/60 bg-white/5 text-zinc-200">
                {dataset.meta.name}
              </span>
            </div>

            <button
              onClick={() => {
                if (!freeze) {
                  setFrozenFrame(frame);
                  setFreeze(true);
                } else {
                  setFreeze(false);
                  setFrozenFrame(null);
                }
              }}
              className={`px-3 py-2 rounded border text-xs flex items-center gap-2 ${
                freeze
                  ? 'bg-white/5 border-zinc-700/70 text-white'
                  : 'bg-transparent border-zinc-800/60 text-zinc-300 hover:bg-white/5 hover:text-white'
              }`}
            >
              <Snowflake className="w-4 h-4" />
              {freeze ? 'Frozen' : 'Freeze'}
            </button>

            <button
              onClick={exportReceipt}
              className="px-3 py-2 rounded border bg-transparent border-zinc-800/60 text-zinc-300 hover:bg-white/5 hover:text-white text-xs flex items-center gap-2"
            >
              <Download className="w-4 h-4" />
              Export receipt
            </button>
          </div>
        </header>

        <main className="grid grid-cols-[1fr_420px] gap-3 p-3">
          <div className="min-w-0 grid grid-rows-[auto_1fr] gap-3">
            <BarSpectrum frame={frame} />

            <div className="min-h-0 bg-zinc-950/30 border border-zinc-800/60 rounded-xl overflow-hidden shadow-sm shadow-black/30">
              <div className="flex items-center justify-between px-4 py-3 border-b border-zinc-800/60">
                <div className="flex items-center gap-2">
                  <Activity className="w-4 h-4 text-neutral-400" />
                  <div className="text-xs font-semibold">Dataset Inspector</div>
                </div>
                <div className="text-[10px] font-mono text-neutral-600">RAW</div>
              </div>
              <pre className="p-4 text-[11px] font-mono text-neutral-300 overflow-auto h-full">
{jsonPreview(dataset.data, 12000)}
              </pre>
            </div>
          </div>

          <aside className="min-w-0 flex flex-col gap-3">
            <DatasetPanel
              datasetState={datasetState}
              onSetBuiltIn={(id) => setDatasetState({ kind: 'built_in', id })}
              onLoadFile={(name, data) => setDatasetState({ kind: 'user_json', name, data })}
            />

            <MacroRack knobs={knobs} onChange={setKnobs} />

            <div className="bg-zinc-950/30 border border-zinc-800/60 rounded-xl p-4 shadow-sm shadow-black/30">
              <div className="flex items-center justify-between mb-3">
                <div className="text-[10px] font-mono text-neutral-500 uppercase tracking-widest">
                  Presets
                </div>
                <div className="text-[10px] font-mono text-neutral-600">LOCAL</div>
              </div>

              <div className="flex gap-2 mb-3">
                <input
                  value={newPresetName}
                  onChange={(e) => setNewPresetName(e.target.value)}
                  placeholder="Preset name"
                  className="flex-1 px-3 py-2 rounded bg-white/5 border border-zinc-800/60 text-xs text-neutral-100 placeholder:text-neutral-500"
                />
                <button
                  onClick={savePreset}
                  className="px-3 py-2 rounded border bg-transparent border-zinc-800/60 text-zinc-300 hover:bg-white/5 hover:text-white text-xs"
                >
                  Save
                </button>
              </div>

              <div className="space-y-2 max-h-40 overflow-auto">
                {presets.length === 0 && (
                  <div className="text-xs text-neutral-500">No presets saved yet.</div>
                )}
                {presets.map((p, i) => (
                  <div
                    key={`${p.name}-${i}`}
                    className="flex items-center justify-between gap-2 px-3 py-2 rounded border border-zinc-800/60 bg-white/5"
                  >
                    <div className="text-xs text-neutral-200 truncate">{p.name}</div>
                    <div className="flex gap-2">
                      <button
                        onClick={() => loadPreset(p.data)}
                        className="px-2 py-1 rounded border border-zinc-800/60 text-xs text-zinc-200 hover:bg-white/5"
                      >
                        Load
                      </button>
                      <button
                        onClick={() => deletePreset(i)}
                        className="px-2 py-1 rounded border border-zinc-800/60 text-xs text-neutral-400 hover:bg-white/5 hover:text-red-200"
                      >
                        Delete
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="bg-zinc-950/30 border border-zinc-800/60 rounded-xl p-4 flex-1 min-h-0 shadow-sm shadow-black/30">
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-2">
                  <Brain className="w-4 h-4 text-neutral-400" />
                  <div className="text-[10px] font-mono text-neutral-500 uppercase tracking-widest">
                    IDE Assistant
                  </div>
                </div>
                <div className="text-[10px] font-mono text-neutral-600">MOCK</div>
              </div>

              <div className="flex gap-2 mb-3">
                <input
                  value={assistantQuery}
                  onChange={(e) => setAssistantQuery(e.target.value)}
                  placeholder="Ask: tone distribution, snape communication, compare..."
                  className="flex-1 px-3 py-2 rounded bg-white/5 border border-zinc-800/60 text-xs text-neutral-100 placeholder:text-neutral-500"
                />
                <button
                  onClick={() => {
                    const resp = mockAiRespond({ query: assistantQuery, dataset, knobs });
                    setAssistantResponse(resp);
                  }}
                  className="px-3 py-2 rounded border bg-transparent border-zinc-800/60 text-zinc-300 hover:bg-white/5 hover:text-white text-xs"
                >
                  Run
                </button>
              </div>

              <div className="min-h-0 overflow-auto">
                <div className="text-xs text-neutral-300 whitespace-pre-wrap">
                  {assistantResponse.summary}
                </div>

                <div className="mt-3 space-y-2">
                  {assistantResponse.actions.map((a) => (
                    <button
                      key={a.id}
                      onClick={() => applyAiAction(a.id)}
                      className="w-full text-left px-3 py-2 rounded border border-zinc-800/60 bg-white/5 hover:bg-white/10"
                    >
                      <div className="text-xs font-semibold text-neutral-100">{a.title}</div>
                      <div className="text-[10px] text-neutral-500">{a.description}</div>
                    </button>
                  ))}
                </div>

                <div className="mt-4 pt-4 border-t border-zinc-800/60 flex items-center gap-2 text-[10px] font-mono text-neutral-600">
                  <BookOpen className="w-3 h-3" />
                  Context: {dataset.meta.name}
                </div>
              </div>
            </div>
          </aside>
        </main>
      </div>
    </div>
  );
}
