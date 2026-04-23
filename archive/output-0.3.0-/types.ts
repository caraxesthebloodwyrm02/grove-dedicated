import React from 'react';

export enum ModuleType {
  IMAGE_GEN = 'IMAGE_GEN',
  IMAGE_EDIT = 'IMAGE_EDIT',
  THINKING = 'THINKING',
  LIVE_VOICE = 'LIVE_VOICE',
  TTS = 'TTS',
  LOGIC_LAB = 'LOGIC_LAB',
  DEPENDENCY_MANAGER = 'DEPENDENCY_MANAGER',
  RESEARCH = 'RESEARCH',
  DECISION_HELPER = 'DECISION_HELPER',
  CODE_REVIEW = 'CODE_REVIEW',
  MISSION_CONTROL = 'MISSION_CONTROL',
  LOCAL_BRIDGE = 'LOCAL_BRIDGE',
  SINE_WAVEFORM = 'SINE_WAVEFORM'
}

export interface ModuleConfig {
  id: string;
  type: ModuleType;
  title: string;
  description: string;
}

export type AspectRatio = "1:1" | "2:3" | "3:2" | "3:4" | "4:3" | "9:16" | "16:9" | "21:9";
export type ImageSize = "1K" | "2K" | "4K";
export type VoiceName = 'Puck' | 'Charon' | 'Kore' | 'Fenrir' | 'Zephyr';

// Logic Lab Types
export type LogicLevel = 'beginner' | 'intermediate' | 'advanced';
export type LogicStyle = 'step_by_step' | 'summary';
export type CognitiveLoad = 'low' | 'medium' | 'high';
export type DiagramType = 'tree' | 'automata' | 'flow' | 'network' | 'auto';

export interface DiagramNode {
    id: string;
    label: string;
    type?: 'start' | 'end' | 'state' | 'process' | 'decision' | 'concept' | 'package';
    x?: number; 
    y?: number;
}

export interface DiagramEdge {
    from: string;
    to: string;
    label?: string;
}

export interface ChartData {
  type: 'bar' | 'pie';
  title: string;
  labels: string[];
  datasets: {
    label: string;
    data: number[];
  }[];
}

export interface LogicResponse {
    explanation: string;
    key_concepts: string[];
    diagram?: {
        type: DiagramType;
        nodes: DiagramNode[];
        edges: DiagramEdge[];
    };
    chart?: ChartData;
    groundingUrls?: string[];
    metadata: {
        level?: LogicLevel;
        style?: LogicStyle;
        cognitive_load?: CognitiveLoad;
    }
}

export interface DecisionResponse {
    recommendation: string; // The primary action (e.g. "ROLLBACK")
    confidence: number; // 0-100
    reasoning: string; // Concise rationale
    options: {
        label: string;
        pros: string;
        cons: string;
        risk_level: 'low' | 'medium' | 'high' | 'critical';
    }[];
    arkhipov_check: {
        emotional_state: string;
        verification_needed: string;
        reversibility: string;
    }
}

export interface CodeAuditResponse {
    quality_score: number; // 0-100
    summary: string;
    semantic_grep: {
        query: string;
        matches: { line: number, content: string, note: string }[];
    };
    structured_audit: {
        category: 'security' | 'performance' | 'maintainability' | 'correctness';
        severity: 'critical' | 'high' | 'medium' | 'low';
        description: string;
        suggestion: string;
        line?: number;
    }[];
}

export interface GuidanceResponse {
    mission_status: string; // e.g. "Orbit Stable", "Turbulence Detected"
    coherence_score: number; // 0-100, how connected the user's tasks are
    analogy: string; // A metaphor for the user's current workflow
    guidance: string; // Strategic advice
    detected_intent: string; // What the AI thinks the user is trying to build
    next_steps: string[];
}

export interface GridNode {
    id: string;
    title: string;
    domain: string;
    description: string;
    defaultParams: {
        question: string;
        level: LogicLevel;
        style: LogicStyle;
        load: CognitiveLoad;
        diagramType: DiagramType;
    };
}

export interface PulseItem {
    id: string;
    source: 'GITHUB' | 'HUGGINGFACE' | 'MISTRAL';
    title: string;
    description: string;
    metric: string; // e.g., "1.2k stars", "New Release"
    url: string;
}

export interface Preset<T> {
  name: string;
  data: T;
}

export interface LogItem {
  id: string;
  timestamp: Date;
  sender: 'user' | 'model' | 'system';
  content: string | React.ReactNode;
  type: 'text' | 'image' | 'audio' | 'info' | 'error';
}

// Global declaration for the AI Studio key selection
declare global {
  interface AIStudio {
    hasSelectedApiKey: () => Promise<boolean>;
    openSelectKey: () => Promise<void>;
  }
  interface Window {
    aistudio?: AIStudio;
  }
}