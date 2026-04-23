import React, { useEffect, useRef } from 'react';

interface Props {
  mode: 'idle' | 'text' | 'image' | 'voice' | 'processing';
  intensity: number; // 0 to 1
}

const CodeContextVisualizer: React.FC<Props> = ({ mode, intensity }) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const frameRef = useRef<number>(0);
  const timeRef = useRef<number>(0);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const draw = () => {
      timeRef.current += 0.02; 
      const t = timeRef.current;
      const w = canvas.width;
      const h = canvas.height;

      // Clear with fade for trails
      ctx.fillStyle = 'rgba(10, 10, 10, 0.2)'; 
      ctx.fillRect(0, 0, w, h);
      
      // Subtle Grid Background
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.05)';
      ctx.lineWidth = 1;
      ctx.beginPath();
      const gridSize = 20;
      const offsetX = (t * 5) % gridSize;
      for(let x=offsetX; x<=w; x+=gridSize) { ctx.moveTo(x,0); ctx.lineTo(x,h); }
      ctx.stroke();

      if (mode === 'processing') {
          // PROCESSING: Complex computation with depth and data flow
          const layers = 3;

          // Rotating background grid for depth
          ctx.save();
          ctx.translate(w / 2, h / 2);
          ctx.rotate(t * 0.1);
          const grid_size_proc = 40;
          ctx.strokeStyle = 'rgba(168, 85, 247, 0.1)'; // Faint purple
          ctx.lineWidth = 0.5;
          ctx.beginPath();
          for (let i = -w; i < w; i += grid_size_proc) {
              ctx.moveTo(i, -h); ctx.lineTo(i, h);
              ctx.moveTo(-w, i); ctx.lineTo(w, i);
          }
          ctx.stroke();
          ctx.restore();

          // Multi-Wave Interference
          for(let l=0; l<layers; l++) {
              ctx.beginPath();
              ctx.strokeStyle = l === 0 ? '#a855f7' : (l===1 ? '#6366f1' : '#ec4899'); // Purple, Indigo, Pink
              ctx.lineWidth = 1.5;
              const speed = (l + 1) * 3;
              const freq = (l + 1) * 0.03;
              const amp = (h/3) * (Math.sin(t + l) * 0.5 + 1); // Breathing amplitude
              for (let x = 0; x < w; x+=3) {
                  const y = h/2 + Math.sin(x * freq + t * speed) * amp * Math.cos(x * 0.01 - t); 
                  if (x===0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
              }
              ctx.stroke();
          }
          
          // Data Particles flowing on waves
          ctx.fillStyle = '#fff';
          const numParticles = 20;
          for (let i=0; i < numParticles; i++) {
              const l = i % layers;
              const speed = (l + 1) * 3;
              const freq = (l + 1) * 0.03;
              const amp = (h/3) * (Math.sin(t + l) * 0.5 + 1);
              const x = ((t * (20 + l*5)) + (i/numParticles * w)) % w;
              const y = h/2 + Math.sin(x * freq + t * speed) * amp * Math.cos(x * 0.01 - t); 
              ctx.beginPath();
              ctx.arc(x, y, 1.5, 0, Math.PI * 2);
              ctx.fill();
          }

      } else if (mode === 'text') {
          // TEXT: Smooth data stream
          ctx.beginPath();
          ctx.strokeStyle = '#3b82f6'; // Blue
          ctx.lineWidth = 2;
          ctx.shadowBlur = 5;
          ctx.shadowColor = '#3b82f6';
          const amp = Math.max(0.2, intensity) * (h/3);
          for (let x = 0; x < w; x+=2) {
              const y = h/2 + Math.sin(x * 0.1 + t * 5) * amp * Math.sin(x * 0.05 + t);
              if (x===0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
          }
          ctx.stroke();
          ctx.shadowBlur = 0;

      } else if (mode === 'image') {
          // IMAGE: More dynamic raster scanning
          ctx.strokeStyle = '#10b981'; // Emerald
          ctx.fillStyle = 'rgba(16, 185, 129, 0.3)';
          
          const scanY = (Math.sin(t * 2) * 0.5 + 0.5) * h;
          ctx.beginPath();
          ctx.moveTo(0, scanY); ctx.lineTo(w, scanY);
          ctx.strokeStyle = 'rgba(16, 185, 129, 0.8)';
          ctx.lineWidth = 2;
          ctx.stroke();

          // Scanline glitch effect
          if (Math.random() > 0.95) {
              ctx.lineWidth = 4;
              ctx.strokeStyle = '#fff';
              ctx.beginPath();
              ctx.moveTo(Math.random() * w * 0.2, scanY);
              ctx.lineTo(w - Math.random() * w * 0.2, scanY);
              ctx.stroke();
          }

          // Pixel blocks density based on intensity
          const blockCount = 5 + Math.floor(intensity * 30);
          const blockSize = 8;
          for(let i=0; i<blockCount; i++) {
              const x = Math.floor(Math.random() * (w/blockSize)) * blockSize;
              const y = Math.floor(Math.random() * (h/blockSize)) * blockSize;
              if (Math.abs(y - scanY) < 30 || Math.random() > 0.9) {
                  ctx.fillRect(x, y, blockSize-1, blockSize-1);
              }
          }
          
          // Corner Brackets with jitter
          const m = 5; const l = 10;
          const jitterX = (Math.random() - 0.5) * intensity * 2;
          const jitterY = (Math.random() - 0.5) * intensity * 2;
          ctx.strokeStyle = '#10b981'; ctx.lineWidth = 2;
          ctx.beginPath();
          ctx.moveTo(m + jitterX, m + l + jitterY); ctx.lineTo(m + jitterX, m + jitterY); ctx.lineTo(m + l + jitterX, m + jitterY);
          ctx.moveTo(w - m - l - jitterX, m + jitterY); ctx.lineTo(w - m - jitterX, m + jitterY); ctx.lineTo(w - m - jitterX, m + l + jitterY);
          ctx.moveTo(m + jitterX, h - m - l - jitterY); ctx.lineTo(m + jitterX, h - m - jitterY); ctx.lineTo(m + l + jitterX, h - m - jitterY);
          ctx.moveTo(w - m - l - jitterX, h - m - jitterY); ctx.lineTo(w - m - jitterX, h - m - jitterY); ctx.lineTo(w - m - jitterX, h - m - l - jitterY);
          ctx.stroke();

      } else if (mode === 'voice') {
          // VOICE: Refined Audio Spectrum
          const bars = 40;
          const barW = w / bars;

          // Background ambient wave
          ctx.beginPath();
          ctx.lineWidth = 1;
          ctx.strokeStyle = `rgba(248, 113, 113, ${0.3 * intensity})`;
          for(let i=0; i<=w; i++) {
              const y = h/2 + Math.sin(i*0.05 + t*4) * (h * 0.1 * intensity);
              if(i===0) ctx.moveTo(i, y); else ctx.lineTo(i,y);
          }
          ctx.stroke();

          // Dynamic color based on intensity
          const lightness = 50 + (20 * intensity);
          ctx.fillStyle = `hsl(0, 80%, ${lightness}%)`;
          
          for(let i=0; i<bars; i++) {
              const xFromCenter = Math.abs(i - bars/2) / (bars/2);
              const wave = Math.sin(t * 8 + i * 0.5) * 0.5 + 0.5;
              const shape = Math.cos(xFromCenter * Math.PI / 2);
              const hScale = (intensity * 0.8 + 0.2);
              const barH = (h * 0.8) * wave * shape * hScale + (h*0.1);
              const x = i * barW;
              const y = (h - barH) / 2;
              ctx.fillRect(x + 1, y, barW - 2, barH);
          }

      } else {
          // IDLE: Breathing LED
          ctx.fillStyle = 'rgba(50, 50, 50, 0.5)';
          const r = 2 + Math.sin(t * 2) * 1;
          ctx.beginPath();
          ctx.arc(w/2, h/2, r, 0, Math.PI*2);
          ctx.fill();
          
          ctx.strokeStyle = `rgba(50, 50, 50, ${0.3 * (1 - ((t*0.5)%1))})`;
          ctx.beginPath();
          ctx.arc(w/2, h/2, r + ((t*0.5)%1)*20, 0, Math.PI*2);
          ctx.stroke();
      }

      frameRef.current = requestAnimationFrame(draw);
    };

    const resize = () => {
        canvas.width = canvas.parentElement?.clientWidth || 300;
        canvas.height = canvas.parentElement?.clientHeight || 60;
    };
    resize();
    window.addEventListener('resize', resize);
    draw();

    return () => {
        window.removeEventListener('resize', resize);
        cancelAnimationFrame(frameRef.current);
    };
  }, [mode, intensity]);

  const getStatusColor = () => {
      switch(mode) {
          case 'processing': return 'bg-purple-500 animate-pulse';
          case 'image': return 'bg-emerald-500';
          case 'voice': return 'bg-red-500 animate-pulse';
          case 'text': return 'bg-blue-500';
          default: return 'bg-neutral-600';
      }
  }

  return (
    <div className="w-full h-14 bg-neutral-950/80 border-b border-neutral-800 rounded-t-lg overflow-hidden relative mb-2 shadow-inner">
        <canvas ref={canvasRef} className="w-full h-full block" />
        <div className="absolute top-1 right-2 flex items-center gap-1">
             <div className={`w-1.5 h-1.5 rounded-full ${getStatusColor()}`}></div>
             <span className="text-[9px] font-mono text-neutral-500 uppercase tracking-wider">
                {mode === 'idle' ? 'STANDBY' : `INPUT: ${mode.toUpperCase()}`}
            </span>
        </div>
    </div>
  );
};

export default CodeContextVisualizer;