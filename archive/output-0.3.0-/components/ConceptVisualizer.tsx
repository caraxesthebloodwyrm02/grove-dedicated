import React, { useMemo } from 'react';
import { LogicResponse, DiagramNode } from '../types';

interface Props {
  data: LogicResponse;
}

export const ConceptVisualizer: React.FC<Props> = ({ data }) => {
  return (
    <div className="flex flex-col gap-4 w-full">
      {data.diagram && <DiagramRenderer diagram={data.diagram} />}
      {data.chart && <ChartRenderer chart={data.chart} />}
    </div>
  );
};

// --- Sub-Renderers ---

const DiagramRenderer = ({ diagram }: { diagram: LogicResponse['diagram'] }) => {
    if (!diagram || !diagram.nodes.length) return null;

    // Simple layout logic: if no coords, arrange in circle or levels
    const nodesWithCoords = useMemo(() => {
        const center = { x: 200, y: 150 };
        const nodeCount = diagram.nodes.length;
        
        // Check if hierarchical (edges go mostly one way)
        const isFlow = diagram.type === 'flow' || diagram.type === 'tree';
        
        return diagram.nodes.map((n, i) => {
            if (n.x !== undefined && n.y !== undefined) return n;
            
            if (isFlow) {
                 // Simple Vertical Layout for Flowcharts
                 // Assumes model provides nodes in roughly topological order which we request in prompt
                 return {
                     ...n,
                     x: center.x,
                     y: 40 + i * 65 
                 }
            }

            // Radial Layout default
            const angle = (i / nodeCount) * Math.PI * 2;
            const r = 90 + (i % 2) * 20; // Vary radius slightly
            return {
                ...n,
                x: center.x + Math.cos(angle) * r,
                y: center.y + Math.sin(angle) * r
            };
        });
    }, [diagram]);

    const renderNodeShape = (n: DiagramNode) => {
        switch (n.type) {
            case 'decision':
                // Diamond - Increased size
                const dSize = 30;
                return (
                    <polygon 
                        points={`${n.x},${(n.y||0)-dSize*0.7} ${(n.x||0)+dSize},${n.y} ${n.x},${(n.y||0)+dSize*0.7} ${(n.x||0)-dSize},${n.y}`}
                        className="fill-neutral-900 stroke-yellow-500 hover:stroke-yellow-300 transition-colors"
                        strokeWidth="1.5"
                    />
                );
            case 'process':
            case 'package':
                // Rectangle
                return (
                    <rect 
                        x={(n.x||0)-30} y={(n.y||0)-12} 
                        width="60" height="24" rx="2"
                        className={`fill-neutral-900 transition-colors strokeWidth="1.5" ${n.type === 'package' ? 'stroke-emerald-600 hover:stroke-emerald-400' : 'stroke-blue-600 hover:stroke-blue-400'}`}
                        strokeWidth="1.5"
                    />
                );
            case 'start':
            case 'end':
                // Capsule
                return (
                    <rect 
                        x={(n.x||0)-25} y={(n.y||0)-12} 
                        width="50" height="24" rx="12"
                        className="fill-neutral-800 stroke-neutral-400"
                        strokeWidth="1.5"
                    />
                );
            case 'concept':
                // Hexagon for concepts
                return (
                    <polygon
                        points={`${(n.x||0)-18},${n.y} ${(n.x||0)-9},${(n.y||0)-15} ${(n.x||0)+9},${(n.y||0)-15} ${(n.x||0)+18},${n.y} ${(n.x||0)+9},${(n.y||0)+15} ${(n.x||0)-9},${(n.y||0)+15}`}
                        className="fill-neutral-900 stroke-cyan-500 hover:stroke-cyan-300 transition-colors"
                        strokeWidth="1.5"
                    />
                );
            default:
                // Circle (default state)
                return (
                    <circle 
                        cx={n.x} cy={n.y} r="16" 
                        className="fill-neutral-900 stroke-purple-500 hover:stroke-purple-300 transition-colors" 
                        strokeWidth="1.5"
                    />
                );
        }
    };

    return (
        <div className="w-full bg-neutral-950/80 rounded border border-neutral-800 relative group overflow-hidden">
             <div className="absolute top-2 right-2 text-[9px] text-neutral-600 font-mono uppercase z-10">
                {diagram.type || 'Structure'} View
            </div>
            {/* Background Grid */}
            <svg className="absolute inset-0 w-full h-full opacity-10 pointer-events-none">
                 <defs>
                     <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
                         <path d="M 20 0 L 0 0 0 20" fill="none" stroke="currentColor" strokeWidth="0.5"/>
                     </pattern>
                 </defs>
                 <rect width="100%" height="100%" fill="url(#grid)" className="text-blue-500" />
            </svg>

            <svg viewBox="0 0 400 300" className="w-full h-auto relative z-0 min-h-[300px]">
                <defs>
                    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="28" refY="3.5" orient="auto">
                        <polygon points="0 0, 10 3.5, 0 7" fill="#525252" />
                    </marker>
                </defs>
                {diagram.edges.map((e, i) => {
                    const source = nodesWithCoords.find(n => n.id === e.from);
                    const target = nodesWithCoords.find(n => n.id === e.to);
                    if (!source || !target) return null;
                    return (
                        <g key={i}>
                            <line 
                                x1={source.x} y1={source.y} 
                                x2={target.x} y2={target.y} 
                                stroke="#404040" 
                                strokeWidth="1"
                                markerEnd="url(#arrowhead)"
                                className="transition-all duration-500"
                            />
                            {e.label && (
                                <g>
                                    <rect 
                                        x={((source.x || 0) + (target.x || 0)) / 2 - (e.label.length * 2.5)}
                                        y={((source.y || 0) + (target.y || 0)) / 2 - 8}
                                        width={e.label.length * 5}
                                        height={10}
                                        fill="#0a0a0a"
                                        opacity="0.8"
                                    />
                                    <text 
                                        x={((source.x || 0) + (target.x || 0)) / 2} 
                                        y={((source.y || 0) + (target.y || 0)) / 2}
                                        textAnchor="middle"
                                        dominantBaseline="middle"
                                        className="fill-neutral-500 text-[8px] font-mono uppercase tracking-tighter"
                                    >
                                        {e.label}
                                    </text>
                                </g>
                            )}
                        </g>
                    );
                })}
                {nodesWithCoords.map((n, i) => (
                    <g key={n.id} className="cursor-default transition-all duration-500 hover:scale-105 origin-center">
                        {renderNodeShape(n)}
                        <text x={n.x} y={n.y} dy="2" textAnchor="middle" className="fill-neutral-200 text-[8px] font-bold font-mono select-none pointer-events-none">{n.label.slice(0, 15)}</text>
                        {n.type && n.type !== 'state' && (
                             <text x={n.x} y={(n.y || 0) + 26} textAnchor="middle" className="fill-neutral-600 text-[6px] font-mono uppercase tracking-widest">{n.type}</text>
                        )}
                    </g>
                ))}
            </svg>
        </div>
    );
};

const ChartRenderer = ({ chart }: { chart: LogicResponse['chart'] }) => {
    if (!chart || !chart.datasets.length) return null;

    const data = chart.datasets[0].data;
    const maxVal = Math.max(...data) * 1.1 || 1;
    const height = 150;
    const width = 300;
    const barWidth = (width / data.length) * 0.6;
    const gap = (width / data.length) * 0.4;

    return (
        <div className="w-full bg-neutral-950/80 rounded border border-neutral-800 p-4 relative overflow-hidden">
             <div className="absolute top-2 right-2 text-[9px] text-neutral-600 font-mono uppercase z-10">
                {chart.type} Analysis
            </div>
            <div className="text-xs text-neutral-400 font-mono mb-4 text-center">{chart.title}</div>
            
            <div className="flex justify-center">
                <svg width={width} height={height + 20} className="overflow-visible">
                     {/* Y-Axis lines */}
                     <line x1="0" y1={height} x2={width} y2={height} stroke="#333" strokeWidth="1" />
                     <line x1="0" y1={0} x2={0} y2={height} stroke="#333" strokeWidth="1" />
                     
                     {data.map((val, i) => {
                         const barH = (val / maxVal) * height;
                         const x = i * (barWidth + gap) + gap/2;
                         return (
                             <g key={i} className="group">
                                 <rect 
                                    x={x} 
                                    y={height - barH} 
                                    width={barWidth} 
                                    height={barH} 
                                    className="fill-blue-900/50 stroke-blue-500/50 hover:fill-blue-600 hover:stroke-blue-300 transition-all duration-300"
                                    rx="2"
                                 />
                                 <text 
                                    x={x + barWidth/2} 
                                    y={height + 15} 
                                    textAnchor="middle" 
                                    className="fill-neutral-500 text-[8px] font-mono uppercase"
                                 >
                                     {chart.labels[i]?.slice(0, 8)}
                                 </text>
                                 <text 
                                    x={x + barWidth/2} 
                                    y={height - barH - 5} 
                                    textAnchor="middle" 
                                    className="fill-white text-[8px] font-mono opacity-0 group-hover:opacity-100 transition-opacity"
                                 >
                                     {val}
                                 </text>
                             </g>
                         )
                     })}
                </svg>
            </div>
            <div className="mt-2 text-[8px] text-neutral-600 text-center font-mono">
                DATASET: {chart.datasets[0].label}
            </div>
        </div>
    );
};