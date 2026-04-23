import { Knobs, Band, House } from '../types';

/**
 * Simulates the complex relationship between magical input knobs and the resulting spectral bands.
 * Now influenced by the inherent magical properties of the selected House.
 */
export const calculateSpectrum = (knobs: Knobs, house: House): Band[] => {
  const {
    canon_tightness,
    signal_clarity,
    noise,
    auth,
    bandwidth,
    emotion_gain,
    mystery,
    practicality
  } = knobs;

  // Base calculations
  let clarityVal = (signal_clarity * 1.2) - (noise * 0.5) + (canon_tightness * 0.1);
  let noiseVal = noise - (canon_tightness * 0.3) + (Math.random() * 5);
  let authVal = (auth * 0.7) + (canon_tightness * 0.3);
  let bandwidthVal = bandwidth - (emotion_gain * 0.2) + (practicality * 0.1);
  let mysteryVal = mystery - (signal_clarity * 0.2) + (noise * 0.1);
  let collisionVal = ((noise * bandwidth) / 100) * 1.5;
  let emotionVal = emotion_gain + (mystery * 0.2);
  let practicalityVal = practicality;

  // House Modifiers
  switch (house) {
    case House.Gryffindor:
      emotionVal *= 1.4;   // Passionate
      authVal *= 1.2;      // Leadership
      noiseVal *= 1.2;     // Sometimes reckless
      clarityVal *= 0.9;   // Less focus on detail
      break;
    case House.Slytherin:
      mysteryVal *= 1.3;   // Cunning/Hidden depths
      authVal *= 1.3;      // Ambition
      practicalityVal *= 1.2; // Resourceful
      emotionVal *= 0.9;   // Controlled
      break;
    case House.Ravenclaw:
      clarityVal *= 1.4;   // Wit/Wisdom
      bandwidthVal *= 1.3; // Knowledge capacity
      noiseVal *= 0.6;     // Precision
      emotionVal *= 0.8;   // Logical
      break;
    case House.Hufflepuff:
      noiseVal *= 0.5;     // Hard work filters interference
      collisionVal *= 0.6; // Harmonious/Loyal
      bandwidthVal *= 1.1; // Steady
      mysteryVal *= 0.8;   // Open/Honest
      break;
  }

  // Clamp values between 0 and 100
  const clamp = (n: number) => Math.max(0, Math.min(100, n));

  return [
    { id: "clarity", label: "Clarity", value: Math.round(clamp(clarityVal)), color: "#60a5fa" },
    { id: "noise", label: "Noise", value: Math.round(clamp(noiseVal)), color: "#f87171" },
    { id: "auth", label: "Auth", value: Math.round(clamp(authVal)), color: "#34d399" },
    { id: "density", label: "Bandwidth", value: Math.round(clamp(bandwidthVal)), color: "#fbbf24" },
    { id: "mystery", label: "Mystery", value: Math.round(clamp(mysteryVal)), color: "#a78bfa" },
    { id: "collision", label: "Masking", value: Math.round(clamp(collisionVal)), color: "#fb7185" },
    { id: "emotion", label: "Emotion", value: Math.round(clamp(emotionVal)), color: "#f472b6" }
  ];
};