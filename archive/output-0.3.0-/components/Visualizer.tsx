import React, { useEffect, useRef } from 'react';
import { ModuleType } from '../types';

interface VisualizerProps {
  type: ModuleType;
  isActive: boolean;
  audioAnalyser?: AnalyserNode; // For Audio modes
}

const Visualizer: React.FC<VisualizerProps> = ({ type, isActive, audioAnalyser }) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const animationRef = useRef<number>(0);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Resize handler
    const resize = () => {
      canvas.width = canvas.parentElement?.clientWidth || window.innerWidth;
      canvas.height = canvas.parentElement?.clientHeight || 400;
    };
    window.addEventListener('resize', resize);
    resize();

    const draw = () => {
      if (!ctx || !canvas) return;
      
      const w = canvas.width;
      const h = canvas.height;
      const time = Date.now() * 0.001;

      // Clear
      ctx.clearRect(0, 0, w, h);

      // Base Grid (FabFilter style) - Dynamic opacity
      ctx.lineWidth = 1;
      ctx.strokeStyle = isActive ? '#1f1f1f' : '#111';
      ctx.beginPath();
      const gridSize = 40;
      for (let x = 0; x < w; x += gridSize) { ctx.moveTo(x, 0); ctx.lineTo(x, h); }
      for (let y = 0; y < h; y += gridSize) { ctx.moveTo(0, y); ctx.lineTo(w, y); }
      ctx.stroke();

      if (!isActive) {
        animationRef.current = requestAnimationFrame(draw);
        return;
      }

      if (type === ModuleType.LIVE_VOICE || type === ModuleType.TTS) {
        // --- REAL-TIME OSCILLOSCOPE WITH FREQUENCY COLOR ---
        if (audioAnalyser) {
            const bufferLength = audioAnalyser.fftSize;
            const dataArray = new Uint8Array(bufferLength);
            audioAnalyser.getByteTimeDomainData(dataArray);

            // Get Frequency data for color/thickness modulation
            const freqData = new Uint8Array(bufferLength);
            audioAnalyser.getByteFrequencyData(freqData);
            
            // Calculate average energy (volume) and dominant frequency (pitch approx)
            let sum = 0;
            let maxFreqVal = 0;
            let dominantBin = 0;
            for(let i=0; i<bufferLength; i++) {
                sum += freqData[i];
                if (freqData[i] > maxFreqVal) {
                    maxFreqVal = freqData[i];
                    dominantBin = i;
                }
            }
            const volume = sum / bufferLength; // 0-255 average
            
            // Map pitch (dominantBin) to Hue (0-360)
            // Lower bins = Bass (Red/Purple), Higher bins = Treble (Blue/Green)
            const pitchHue = (dominantBin / (bufferLength/4)) * 360; 
            const activeColor = `hsl(${200 + pitchHue}, 80%, 60%)`;
            const thickness = 2 + (volume / 20);

            ctx.lineWidth = thickness;
            ctx.strokeStyle = activeColor;
            ctx.shadowBlur = 4 + (volume / 10);
            ctx.shadowColor = activeColor;
            ctx.beginPath();

            const sliceWidth = w * 1.0 / bufferLength;
            let x = 0;

            for(let i = 0; i < bufferLength; i++) {
                const v = dataArray[i] / 128.0;
                const y = (v * h / 2); 

                if(i === 0) ctx.moveTo(x, y);
                else ctx.lineTo(x, y);

                x += sliceWidth;
            }

            ctx.lineTo(w, h/2);
            ctx.stroke();
            ctx.shadowBlur = 0;

            // Secondary Ghost Wave (Stereo illusion)
            ctx.strokeStyle = `hsla(${200 + pitchHue}, 80%, 60%, 0.3)`;
            ctx.lineWidth = 1;
            ctx.beginPath();
            x = 0;
            for(let i = 0; i < bufferLength; i++) {
                const v = dataArray[i] / 128.0;
                const y = (v * h / 2) + Math.sin(time * 5 + x * 0.01) * (10 + volume/5);
                if(i === 0) ctx.moveTo(x, y);
                else ctx.lineTo(x, y);
                x += sliceWidth;
            }
            ctx.stroke();
        }
      } else if (type === ModuleType.THINKING || type === ModuleType.RESEARCH) {
        // --- WAVE INTERFERENCE FIELD (Deep Think) ---
        ctx.strokeStyle = type === ModuleType.RESEARCH ? 'rgba(16, 185, 129, 0.5)' : 'rgba(168, 85, 247, 0.5)';
        ctx.lineWidth = 1.5;
        
        const lines = 8;
        const amplitude = 50;
        
        for (let i = 0; i < lines; i++) {
            ctx.beginPath();
            const freq = 0.01 + (i * 0.005);
            const phase = time * (1 + i * 0.2);
            
            for(let x = 0; x <= w; x += 5) {
                const y1 = Math.sin(x * freq + phase) * amplitude;
                const y2 = Math.sin(x * (freq * 2.5) - phase * 0.5) * (amplitude * 0.5);
                const y = h/2 + y1 + y2;
                if (x===0) ctx.moveTo(x, y);
                else ctx.lineTo(x, y);
            }
            ctx.globalAlpha = 1 - (i / lines); 
            ctx.stroke();
        }
        ctx.globalAlpha = 1;

      } else if (type === ModuleType.LOGIC_LAB) {
          // --- GEOMETRIC ---
          ctx.strokeStyle = '#3b82f6';
          const cx = w / 2;
          const cy = h / 2;
          
          for(let i=0; i<3; i++) {
              const rot = time * 0.1 * (i%2===0 ? 1 : -1) + i;
              const size = 100 + i * 60;
              ctx.beginPath();
              const sides = 4 + i;
              for(let s=0; s<=sides; s++) {
                  const angle = rot + (s/sides) * Math.PI * 2;
                  const px = cx + Math.cos(angle) * size;
                  const py = cy + Math.sin(angle) * size;
                  if (s===0) ctx.moveTo(px, py);
                  else ctx.lineTo(px, py);
              }
              ctx.stroke();
          }
      } else if (type === ModuleType.DEPENDENCY_MANAGER) {
           // --- DATA MATRIX / CONNECTED NODES ---
           const cx = w/2;
           const cy = h/2;
           ctx.fillStyle = '#10b981'; 
           ctx.strokeStyle = 'rgba(16, 185, 129, 0.2)';
           
           // Floating Grid of Nodes
           const rows = 5;
           const cols = 8;
           const cellW = w / cols;
           const cellH = h / rows;
           
           for(let r=0; r<rows; r++) {
               for(let c=0; c<cols; c++) {
                   const x = c * cellW + cellW/2;
                   const y = r * cellH + cellH/2;
                   
                   // Noise offset
                   const nx = Math.sin(time + r + c) * 20;
                   const ny = Math.cos(time + r * c) * 20;
                   
                   ctx.beginPath();
                   const size = (Math.sin(time * 2 + r + c) + 1) * 2 + 1;
                   ctx.arc(x + nx, y + ny, size, 0, Math.PI*2);
                   ctx.fill();
                   
                   // Connections
                   if (r > 0) {
                       const prevY = (r-1) * cellH + cellH/2 + Math.cos(time + (r-1) * c) * 20;
                       const prevX = c * cellW + cellW/2 + Math.sin(time + (r-1) + c) * 20;
                       if (Math.random() > 0.8) {
                           ctx.beginPath();
                           ctx.moveTo(x + nx, y + ny);
                           ctx.lineTo(prevX, prevY);
                           ctx.stroke();
                       }
                   }
               }
           }
      } else if (type === ModuleType.DECISION_HELPER) {
           // --- CONVERGENCE / TARGETING ---
           // Represents chaos organizing into a decision
           const cx = w / 2;
           const cy = h / 2;
           ctx.lineWidth = 2;
           
           // Central Focus Ring
           ctx.strokeStyle = '#3b82f6';
           ctx.beginPath();
           const r = 40 + Math.sin(time * 5) * 5;
           ctx.arc(cx, cy, r, 0, Math.PI * 2);
           ctx.stroke();

           // Converging Lines
           const lines = 6;
           for(let i=0; i<lines; i++) {
               const angle = (i / lines) * Math.PI * 2 + time * 0.5;
               
               // Start far out, wiggle in
               ctx.beginPath();
               for(let d=200; d>50; d-=5) {
                   const spread = (d - 50) * 0.2; // Chaos decreases as we get closer to center
                   const wiggle = Math.sin(d * 0.1 + time * 5) * spread;
                   const ax = cx + Math.cos(angle) * d + Math.cos(angle + Math.PI/2) * wiggle;
                   const ay = cy + Math.sin(angle) * d + Math.sin(angle + Math.PI/2) * wiggle;
                   
                   if (d===200) ctx.moveTo(ax, ay);
                   else ctx.lineTo(ax, ay);
               }
               ctx.strokeStyle = `rgba(59, 130, 246, ${0.1 + (Math.sin(time+i)*0.5+0.5)*0.5})`;
               ctx.stroke();
           }
           
           // Horizon Line (Stability)
           ctx.beginPath();
           ctx.moveTo(0, cy);
           ctx.lineTo(w, cy);
           ctx.strokeStyle = 'rgba(255, 255, 255, 0.1)';
           ctx.setLineDash([5, 15]);
           ctx.stroke();
           ctx.setLineDash([]);

      } else if (type === ModuleType.CODE_REVIEW) {
          // --- LASER SCANNING LINES ---
          // Simulates deep code scanning
          ctx.strokeStyle = 'rgba(192, 132, 252, 0.5)'; // Purple
          ctx.shadowBlur = 5;
          ctx.shadowColor = '#a855f7';
          
          const scanY = (Math.sin(time) * 0.5 + 0.5) * h;
          
          // The laser beam
          ctx.beginPath();
          ctx.moveTo(0, scanY);
          ctx.lineTo(w, scanY);
          ctx.lineWidth = 3;
          ctx.stroke();
          
          // Trailing digital artifacts
          ctx.fillStyle = 'rgba(168, 85, 247, 0.3)';
          for(let i=0; i<20; i++) {
              const x = Math.random() * w;
              const dist = Math.random() * 50;
              if (Math.random() > 0.5) {
                   // Above scan line
                   const y = scanY - dist;
                   if (y > 0) ctx.fillRect(x, y, 4, 2);
              } else {
                   // Below scan line
                   const y = scanY + dist;
                   if (y < h) ctx.fillRect(x, y, 4, 2);
              }
          }

      } else if (type === ModuleType.MISSION_CONTROL) {
           // --- RADAR SWEEP ---
           const cx = w/2;
           const cy = h/2;
           const maxR = Math.min(w,h) * 0.4;
           
           // Rings
           ctx.strokeStyle = '#6366f1'; // Indigo
           ctx.lineWidth = 1;
           ctx.beginPath(); ctx.arc(cx, cy, maxR, 0, Math.PI*2); ctx.stroke();
           ctx.beginPath(); ctx.arc(cx, cy, maxR*0.6, 0, Math.PI*2); ctx.stroke();
           ctx.beginPath(); ctx.arc(cx, cy, maxR*0.3, 0, Math.PI*2); ctx.stroke();
           
           // Crosshairs
           ctx.beginPath(); ctx.moveTo(cx-maxR, cy); ctx.lineTo(cx+maxR, cy); ctx.stroke();
           ctx.beginPath(); ctx.moveTo(cx, cy-maxR); ctx.lineTo(cx, cy+maxR); ctx.stroke();
           
           // The Sweep
           const angle = time * 2;
           ctx.beginPath();
           ctx.moveTo(cx, cy);
           ctx.arc(cx, cy, maxR, angle, angle + 0.5);
           ctx.lineTo(cx, cy);
           ctx.fillStyle = 'rgba(99, 102, 241, 0.2)';
           ctx.fill();
           
           // Blips
           ctx.fillStyle = '#fff';
           for(let i=0; i<5; i++) {
               const blipAngle = i * 2 + time * 0.1;
               const blipR = maxR * (0.3 + (i*0.15));
               const diff = (angle - blipAngle + Math.PI*4) % (Math.PI*2);
               if (diff < 0.5) {
                   const bx = cx + Math.cos(blipAngle) * blipR;
                   const by = cy + Math.sin(blipAngle) * blipR;
                   const alpha = 1 - (diff * 2);
                   ctx.globalAlpha = alpha;
                   ctx.beginPath(); ctx.arc(bx, by, 3, 0, Math.PI*2); ctx.fill();
               }
           }
           ctx.globalAlpha = 1;

      } else if (type === ModuleType.LOCAL_BRIDGE) {
          // --- DATA TUNNEL ---
          const cx = w/2;
          const cy = h/2;
          ctx.strokeStyle = '#10b981'; // Green
          ctx.lineWidth = 1;
          
          const layers = 8;
          const maxDim = Math.max(w,h) * 0.8;
          
          for (let i = 0; i < layers; i++) {
              const tOffset = (time * 0.5 + i / layers) % 1;
              const size = tOffset * maxDim;
              const alpha = tOffset; // Fade in as it approaches
              
              ctx.globalAlpha = alpha;
              ctx.strokeRect(cx - size/2, cy - size/2, size, size);
              
              // Connecting lines to corners
              if (i < layers - 1) {
                  const nextSize = ((tOffset + 1/layers)%1) * maxDim;
                  if (nextSize > size) {
                      ctx.beginPath();
                      ctx.moveTo(cx - size/2, cy - size/2); ctx.lineTo(cx - nextSize/2, cy - nextSize/2);
                      ctx.moveTo(cx + size/2, cy - size/2); ctx.lineTo(cx + nextSize/2, cy - nextSize/2);
                      ctx.moveTo(cx - size/2, cy + size/2); ctx.lineTo(cx - nextSize/2, cy + nextSize/2);
                      ctx.moveTo(cx + size/2, cy + size/2); ctx.lineTo(cx + nextSize/2, cy + nextSize/2);
                      ctx.stroke();
                  }
              }
          }
          ctx.globalAlpha = 1;

      } else if (type === ModuleType.SINE_WAVEFORM) {
          // --- SINE WAVEFORM INTELLIGENCE PULSE ---
          // A harmonic combination of sine waves representing "community energy"
          ctx.lineWidth = 2;
          
          const waves = 5;
          const baseColor = { h: 35, s: 100, l: 60 }; // Orange/Yellowish
          
          for(let i=0; i<waves; i++) {
              ctx.beginPath();
              
              // Frequency and Speed vary per wave
              const freq = 0.01 + (i * 0.005);
              const speed = (i + 1) * 2;
              const phase = i * Math.PI / 4;
              
              // Color shift
              ctx.strokeStyle = `hsla(${baseColor.h + i * 10}, ${baseColor.s}%, ${baseColor.l}%, ${0.3 + (i/waves)*0.5})`;
              
              for (let x = 0; x <= w; x += 2) {
                  // Composite wave function: Main Sine + Harmonic
                  const y = h/2 + 
                            Math.sin(x * freq + time * speed + phase) * (h/4) * Math.sin(time*0.5) +
                            Math.sin(x * (freq*2.5) - time) * 20;
                  
                  if (x===0) ctx.moveTo(x, y);
                  else ctx.lineTo(x, y);
              }
              ctx.stroke();
          }

      } else if (type === ModuleType.IMAGE_GEN || type === ModuleType.IMAGE_EDIT) {
          // --- DIGITAL RAIN ---
          const t = Date.now() * 0.002;
          ctx.fillStyle = '#10b981';
          for(let i=0; i<30; i++) {
              const x = ((Math.sin(i * 123.45) * 0.5 + 0.5) * w + t * 50) % w;
              const yBase = (Math.cos(i * 67.89) * 0.5 + 0.5) * h;
              const hBar = 20 + Math.random() * 40;
              const wBar = 2 + Math.random() * 4;
              ctx.globalAlpha = 0.3 + Math.random() * 0.5;
              ctx.fillRect(x, yBase, wBar, hBar);
          }
          ctx.globalAlpha = 1;
      }

      animationRef.current = requestAnimationFrame(draw);
    };

    draw();

    return () => {
      window.removeEventListener('resize', resize);
      if (animationRef.current) cancelAnimationFrame(animationRef.current);
    };
  }, [type, isActive, audioAnalyser]);

  return <canvas ref={canvasRef} className="absolute inset-0 w-full h-full pointer-events-none" />;
};

export default Visualizer;