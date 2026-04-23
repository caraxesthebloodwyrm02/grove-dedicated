import React from 'react';
import {
  Radar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
  Tooltip
} from 'recharts';
import { Band } from '../types';

interface RadialChartProps {
  data: Band[];
  color: string;
}

export const RadialChart: React.FC<RadialChartProps> = ({ data, color }) => {
  return (
    <div className="w-full h-full min-h-[350px] relative z-10">
      <ResponsiveContainer width="100%" height="100%">
        <RadarChart cx="50%" cy="53%" outerRadius="70%" data={data}>
          <defs>
            <filter id="lumosGlow" x="-50%" y="-50%" width="200%" height="200%">
              <feGaussianBlur stdDeviation="4" result="coloredBlur" />
              <feMerge>
                <feMergeNode in="coloredBlur" />
                <feMergeNode in="SourceGraphic" />
              </feMerge>
            </filter>
            <linearGradient id="starChartFill" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor={color} stopOpacity={0.4}/>
              <stop offset="100%" stopColor={color} stopOpacity={0.05}/>
            </linearGradient>
          </defs>
          
          {/* Astrolabe Rings */}
          <PolarGrid 
            gridType="circle" 
            stroke="#ffffff" 
            strokeOpacity={0.1} 
            strokeWidth={1}
            strokeDasharray="2 4" 
          />
          
          <PolarAngleAxis 
            dataKey="label" 
            tick={{ 
              fill: '#94a3b8', 
              fontSize: 10, 
              fontFamily: 'Cinzel', 
              fontWeight: 700, 
              letterSpacing: '0.1em' 
            }} 
          />
          
          <PolarRadiusAxis 
            angle={90} 
            domain={[0, 100]} 
            tick={false} 
            axisLine={false}
          />
          
          <Radar
            name="Signature"
            dataKey="value"
            stroke={color}
            strokeWidth={2}
            fill="url(#starChartFill)"
            fillOpacity={0.8}
            isAnimationActive={true}
            style={{ filter: 'url(#lumosGlow)' }}
          />
          
          <Tooltip 
            cursor={false}
            content={({ active, payload }) => {
              if (active && payload && payload.length) {
                return (
                  <div className="bg-slate-950/90 border border-slate-700 p-3 rounded-none shadow-[0_0_20px_rgba(0,0,0,0.5)] backdrop-blur-md">
                    <p className="font-serif text-xs text-slate-400 uppercase tracking-widest mb-1">{payload[0].payload.label}</p>
                    <p className="font-mono text-xl text-white" style={{ color: color, textShadow: `0 0 10px ${color}` }}>
                      {payload[0].value}%
                    </p>
                  </div>
                );
              }
              return null;
            }}
          />
        </RadarChart>
      </ResponsiveContainer>
      
      {/* Decorative Center */}
      <div className="absolute top-[53%] left-1/2 -translate-x-1/2 -translate-y-1/2 w-2 h-2 rounded-full bg-white/20 pointer-events-none shadow-[0_0_15px_white]" />
    </div>
  );
};