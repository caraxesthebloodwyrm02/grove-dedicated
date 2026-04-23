import React, { useState, useEffect } from 'react';
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';
import { Band } from '../types';

interface ResonanceChartProps {
  data: Band[];
  color: string;
}

export const ResonanceChart: React.FC<ResonanceChartProps> = ({ data, color }) => {
  const [isPulsing, setIsPulsing] = useState(false);

  useEffect(() => {
    setIsPulsing(true);
    const timer = setTimeout(() => setIsPulsing(false), 800);
    return () => clearTimeout(timer);
  }, [data]);

  return (
    <div className="w-full h-full min-h-[150px] relative">
       {/* Ambient Resonance Overlay */}
       <div 
         className="absolute inset-0 pointer-events-none z-0 transition-opacity duration-1000"
         style={{
           background: `radial-gradient(circle at 50% 100%, ${color}20 0%, transparent 70%)`,
           opacity: isPulsing ? 0.8 : 0.3
         }}
       />
       
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={data} margin={{top: 20, right: 10, bottom: 0, left: -20}}>
          <defs>
            <linearGradient id="mistGradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor={color} stopOpacity={0.4}/>
              <stop offset="50%" stopColor={color} stopOpacity={0.1}/>
              <stop offset="100%" stopColor={color} stopOpacity={0}/>
            </linearGradient>
            <filter id="energyBlur" x="-20%" y="-20%" width="140%" height="140%">
               <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
               <feComposite in="SourceGraphic" in2="coloredBlur" operator="over"/>
            </filter>
          </defs>
          
          <CartesianGrid strokeDasharray="1 5" stroke="#ffffff" strokeOpacity={0.05} vertical={false} />
          
          <XAxis 
            dataKey="label" 
            stroke="#475569" 
            fontSize={9}
            fontFamily="Space Grotesk"
            tickLine={false}
            axisLine={false}
            interval={0}
            dy={10}
            tick={{ fill: '#64748b' }}
          />
          <YAxis 
            stroke="#475569" 
            fontSize={9} 
            fontFamily="Space Grotesk"
            tickLine={false}
            axisLine={false}
            tick={{ fill: '#64748b' }}
          />
          
          <Tooltip 
             cursor={{ stroke: color, strokeWidth: 1, strokeDasharray: '2 2', opacity: 0.5 }}
             content={({ active, payload }) => {
                if (active && payload && payload.length) {
                  return (
                    <div className="bg-slate-900/90 border-t border-slate-700 px-3 py-2 shadow-xl backdrop-blur">
                      <span className="font-mono text-xs" style={{ color: color }}>
                        {payload[0].value} Hz
                      </span>
                    </div>
                  );
                }
                return null;
             }}
          />
          
          <Area 
            type="monotone" 
            dataKey="value" 
            stroke={color} 
            strokeWidth={2}
            fillOpacity={1} 
            fill="url(#mistGradient)" 
            style={{ filter: 'url(#energyBlur)' }}
            animationDuration={1000}
            animationEasing="cubic-bezier(0.4, 0, 0.2, 1)"
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
};