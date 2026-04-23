export interface Knobs {
  canon_tightness: number;
  signal_clarity: number;
  noise: number;
  auth: number;
  bandwidth: number;
  emotion_gain: number;
  mystery: number;
  practicality: number;
  [key: string]: number;
}

export interface Band {
  id: string;
  label: string;
  value: number;
  color: string;
}

export interface AnalyzerState {
  bands: Band[];
  note: string;
}

export interface AppState {
  app: {
    name: string;
    version: string;
  };
  dataset: {
    id: string;
    kind: string;
    name: string;
    description: string;
  };
  knobs: Knobs;
  analyzer: AnalyzerState;
  at: string;
}

export enum House {
  Gryffindor = 'Gryffindor',
  Slytherin = 'Slytherin',
  Ravenclaw = 'Ravenclaw',
  Hufflepuff = 'Hufflepuff'
}

// Sophisticated, cinematic color palettes
export const HOUSE_COLORS: Record<House, { primary: string; secondary: string; accent: string; glow: string }> = {
  [House.Gryffindor]: { 
    primary: '#4a0404',   // Deep Crimson
    secondary: '#740001', // Scarlet
    accent: '#d3a625',    // Gold
    glow: 'rgba(211, 166, 37, 0.6)'
  },
  [House.Slytherin]: { 
    primary: '#0d1f14',   // Dark Green
    secondary: '#1a472a', // Emerald
    accent: '#a0b3b0',    // Silver/Platinum
    glow: 'rgba(160, 179, 176, 0.5)'
  },
  [House.Ravenclaw]: { 
    primary: '#0e1a40',   // Midnight Blue
    secondary: '#222f5b', // Sapphire
    accent: '#946b2d',    // Bronze
    glow: 'rgba(148, 107, 45, 0.6)'
  },
  [House.Hufflepuff]: { 
    primary: '#241c10',   // Charcoal/Earth
    secondary: '#372e29', // Dark Brown
    accent: '#ecb939',    // Badger Yellow
    glow: 'rgba(236, 185, 57, 0.5)'
  },
};