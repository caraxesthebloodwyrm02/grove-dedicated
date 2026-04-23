import React from 'react';

interface KnobProps {
  label: string;
  value: number;
  onChange: (val: number) => void;
  color: string;
}

export const Knob: React.FC<KnobProps> = ({ label, value, onChange, color }) => {
  return (
    <div className="flex flex-col gap-2 mb-6 group relative">
      <div className="flex justify-between items-end text-xs font-serif tracking-widest text-slate-500 group-hover:text-slate-300 transition-colors">
        <span className="uppercase">{label.replace('_', ' ')}</span>
        <span className="font-mono text-sm" style={{ color: color }}>{value}</span>
      </div>
      
      <div className="relative h-2 flex items-center">
        {/* Ancient Track */}
        <div className="absolute w-full h-[1px] bg-slate-800/50"></div>
        <div className="absolute w-full h-[1px] bg-slate-700/30 transform scale-y-50"></div>
        
        {/* Active Energy Line */}
        <div 
          className="absolute h-[2px] shadow-[0_0_8px_currentColor] transition-all duration-300 ease-out"
          style={{ 
            width: `${value}%`, 
            backgroundColor: color,
            color: color,
            opacity: 0.8
          }}
        />

        {/* Input */}
        <input
          type="range"
          min="0"
          max="100"
          value={value}
          onChange={(e) => onChange(parseInt(e.target.value))}
          className="absolute w-full h-4 opacity-0 cursor-pointer z-10"
        />

        {/* Runic Thumb */}
        <div 
            className="absolute w-3 h-3 rotate-45 border border-white/20 bg-slate-950 transform -translate-x-1/2 pointer-events-none transition-all duration-100 group-hover:scale-150 group-hover:border-white"
            style={{ 
                left: `${value}%`,
                boxShadow: `0 0 15px ${color}`,
                borderColor: color
            }}
        >
          <div className="absolute inset-0 bg-current opacity-20" style={{ backgroundColor: color }}></div>
        </div>
      </div>
    </div>
  );
};