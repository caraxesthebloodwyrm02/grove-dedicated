import { GoogleGenAI, Modality } from "@google/genai";
import { AspectRatio, ImageSize, VoiceName, LogicLevel, LogicStyle, CognitiveLoad, LogicResponse, DiagramType, DecisionResponse, CodeAuditResponse, GuidanceResponse, LogItem, PulseItem } from "../types";
import { base64ToUint8Array, decodeAudioData } from "./audioUtils";

// Helper to get a fresh client instance (important for key switching)
const getAiClient = () => new GoogleGenAI({ apiKey: process.env.API_KEY });

export async function generateImagePro(
  prompt: string,
  aspectRatio: AspectRatio,
  imageSize: ImageSize
): Promise<string[]> {
  const ai = getAiClient();
  const response = await ai.models.generateContent({
    model: 'gemini-3-pro-image-preview',
    contents: {
      parts: [{ text: prompt }],
    },
    config: {
      imageConfig: {
        aspectRatio: aspectRatio,
        imageSize: imageSize,
      },
    },
  });

  const images: string[] = [];
  if (response.candidates?.[0]?.content?.parts) {
    for (const part of response.candidates[0].content.parts) {
      if (part.inlineData) {
        images.push(`data:image/png;base64,${part.inlineData.data}`);
      }
    }
  }
  return images;
}

export async function editImage(
  base64Image: string,
  mimeType: string,
  prompt: string
): Promise<string[]> {
  const ai = getAiClient();
  const response = await ai.models.generateContent({
    model: 'gemini-2.5-flash-image',
    contents: {
      parts: [
        {
          inlineData: {
            data: base64Image,
            mimeType: mimeType,
          },
        },
        { text: prompt },
      ],
    },
  });

  const images: string[] = [];
  if (response.candidates?.[0]?.content?.parts) {
    for (const part of response.candidates[0].content.parts) {
      if (part.inlineData) {
        images.push(`data:image/png;base64,${part.inlineData.data}`);
      }
    }
  }
  return images;
}

export async function thinkDeeply(prompt: string, budget: number = 32768): Promise<string> {
  const ai = getAiClient();
  const response = await ai.models.generateContent({
    model: 'gemini-3-pro-preview',
    contents: prompt,
    config: {
      thinkingConfig: {
        thinkingBudget: budget, 
      },
    },
  });
  return response.text || "No response generated.";
}

export async function performResearch(query: string): Promise<LogicResponse> {
  const ai = getAiClient();
  
  // Using Flash for search as per guidelines
  const response = await ai.models.generateContent({
    model: 'gemini-2.5-flash',
    contents: `
      You are the "Mothership Research Node".
      Task: Research the following query using Google Search. Provide a comprehensive summary, key facts, and grounded sources.
      Query: "${query}"
      
      Output:
      Provide a clear, markdown formatted summary.
    `,
    config: {
      tools: [{ googleSearch: {} }],
    },
  });

  const groundingChunks = response.candidates?.[0]?.groundingMetadata?.groundingChunks || [];
  const urls = groundingChunks
    .map((c: any) => c.web?.uri)
    .filter((u: any) => u) as string[];

  // Wrap in LogicResponse for consistent UI rendering
  return {
    explanation: response.text || "No results found.",
    key_concepts: ["Search Result", "Live Data"],
    groundingUrls: urls,
    metadata: {}
  };
}

export async function askLogicLab(
  question: string,
  level: LogicLevel,
  style: LogicStyle,
  load: CognitiveLoad,
  diagramType: DiagramType = 'auto'
): Promise<LogicResponse> {
  const ai = getAiClient();
  const prompt = `
    You are the "Logic Lab", a module in a computational garden.
    Task: Explain the following concept related to computation, logic, or cognitive architecture.
    Question: "${question}"

    Constraints:
    - Target Audience Level: ${level}
    - Explanation Style: ${style}
    - Target Cognitive Load: ${load} (keep sentences ${load === 'low' ? 'simple and direct' : load === 'medium' ? 'balanced' : 'detailed and rigorous'}).
    - Requested Diagram Type: ${diagramType}

    Output Format:
    Return strictly valid JSON with the following schema:
    {
      "explanation": "The markdown formatted text explanation. Use clear headings.",
      "key_concepts": ["concept1", "concept2"],
      "diagram": {
        "type": "${diagramType}",
        "nodes": [{ "id": "n1", "label": "Start", "type": "start" }],
        "edges": [{ "from": "n1", "to": "n2", "label": "transition" }]
      },
      "chart": {
         "type": "bar" | "pie",
         "title": "Comparison Title",
         "labels": ["Item A", "Item B"],
         "datasets": [{ "label": "Metric", "data": [10, 20] }]
      },
      "metadata": {
        "level": "${level}",
        "style": "${style}",
        "cognitive_load": "${load}"
      }
    }
    
    Guidance:
    - If diagramType is 'flowchart' or 'flow':
      - Construct a logical, step-by-step flowchart.
      - REQUIRED Node Types: 'start' (initial state), 'process' (action), 'decision' (branching condition), 'end' (final state).
      - 'decision' nodes MUST have outgoing edges with clear labels (e.g. "Yes", "No", "True", "False").
      - Order nodes topologically in the list from start to end (e.g. n1 -> n2 -> n3).
    - If diagramType is 'automata':
      - Use node types 'state', 'start', 'end'.
      - Edges represent transitions based on inputs (e.g. label: "0", "a").
    - If diagramType is 'network':
      - Use node type 'concept'.
      - Create a web of related concepts. Edges should represent relationships (e.g. "is a", "has part", "relates to").
    - If the concept involves comparison, statistics, or ratios (e.g. Cognitive Load analysis, Big O notation comparisons), provide a "chart".
  `;

  const response = await ai.models.generateContent({
    model: 'gemini-3-pro-preview',
    contents: prompt,
    config: {
        responseMimeType: 'application/json',
        thinkingConfig: { thinkingBudget: 4096 }
    }
  });

  try {
      return JSON.parse(response.text || '{}');
  } catch (e) {
      throw new Error("Failed to parse Logic Lab response.");
  }
}

export async function analyzeDependencies(
  dependencyText: string
): Promise<LogicResponse> {
  const ai = getAiClient();
  const prompt = `
    You are the "Dependency Manager", a Mothership module for managing software libraries.
    Task: Analyze the following dependency list, requirements.txt, or lock file content (e.g. package-lock.json, poetry.lock). 
    Identify potential conflicts, deprecated packages, or suggest optimizations.
    
    Input Data:
    """
    ${dependencyText}
    """

    Output Format:
    Return strictly valid JSON with the following schema (reusing LogicResponse structure):
    {
      "explanation": "Analysis report using markdown. List critical updates, security risks, or compatibility notes.",
      "key_concepts": ["Package A", "Package B"],
      "diagram": {
        "type": "network",
        "nodes": [{ "id": "p1", "label": "Package Name", "type": "package" }],
        "edges": [{ "from": "p1", "to": "p2", "label": "depends_on" }]
      },
      "metadata": {
        "level": "advanced",
        "style": "summary",
        "cognitive_load": "medium"
      }
    }
    
    Guidance:
    - Visualize the dependency tree in the "diagram" field.
    - If the text is raw code, infer the imports.
    - If it is a lock file, parse the JSON/TOML structure to build the graph.
  `;

  const response = await ai.models.generateContent({
    model: 'gemini-3-pro-preview',
    contents: prompt,
    config: {
        responseMimeType: 'application/json',
        thinkingConfig: { thinkingBudget: 4096 }
    }
  });

  try {
      return JSON.parse(response.text || '{}');
  } catch (e) {
      throw new Error("Failed to parse Dependency Analysis response.");
  }
}

export async function consultArchitect(context: string): Promise<DecisionResponse> {
    const ai = getAiClient();
    const prompt = `
      You are the "Executive Incident Commander" for a high-stakes software environment.
      
      Your core philosophy is based on "Arkhipov Principles" of crisis management:
      1. EMOTIONAL REGULATION: Pause. Don't react to noise.
      2. VERIFICATION: Is the signal real or a ghost? (Use search to check major outages if implied).
      3. PROBABILISTIC THINKING: Weigh the cost of inaction vs mistake.
      4. REVERSIBILITY: Prioritize reversible actions over irreversible ones.

      Task: Analyze the following "Situation Report" from a developer and provide a decisive recommendation.
      
      Situation Report:
      "${context}"

      Output Format (Strict JSON):
      {
        "recommendation": "Short, punchy action verb phrase (e.g. 'INITIATE ROLLBACK', 'WAIT AND MONITOR', 'HOTFIX STAGING')",
        "confidence": number (0-100),
        "reasoning": "Concise explanation of why this is the best path.",
        "options": [
            { "label": "Option A", "pros": "...", "cons": "...", "risk_level": "low|medium|high|critical" },
            { "label": "Option B", "pros": "...", "cons": "...", "risk_level": "low|medium|high|critical" }
        ],
        "arkhipov_check": {
            "emotional_state": "Assessment of the user's panic level based on text",
            "verification_needed": "What data is missing?",
            "reversibility": "Is the recommended action reversible?"
        }
      }
    `;

    const response = await ai.models.generateContent({
        model: 'gemini-3-pro-preview',
        contents: prompt,
        config: {
            responseMimeType: 'application/json',
            tools: [{ googleSearch: {} }], // Allow searching to verify if cloud providers are down
            thinkingConfig: { thinkingBudget: 2048 } // Quick thinking
        }
    });

    try {
        return JSON.parse(response.text || '{}');
    } catch (e) {
        throw new Error("Failed to parse Decision response.");
    }
}

export async function performCodeAudit(
  code: string,
  grepQuery: string = "Find potential bugs and anti-patterns"
): Promise<CodeAuditResponse> {
  const ai = getAiClient();
  const prompt = `
    You are a Principal Software Engineer & Security Auditor.
    
    Task: Perform a deep "Structured Audit" and "Semantic Grep" on the provided code.
    
    1. SEMANTIC GREP:
       Execute the user's semantic query: "${grepQuery}".
       Unlike regex, look for the *concept* (e.g., if query is "unhandled promises", find 'async' calls without 'await' or '.catch', even if variable names differ).
    
    2. STRUCTURED AUDIT:
       Analyze the code for:
       - Security (Injection, XSS, Auth, Secrets)
       - Performance (O(n^2) loops, memory leaks, unnecessary re-renders)
       - Maintainability (Cognitive complexity, dead code, poor naming)
       - Correctness (Race conditions, off-by-one, type errors)
    
    Input Code:
    """
    ${code}
    """

    Output Format (Strict JSON):
    {
        "quality_score": 85,
        "summary": "One sentence summary of the code health.",
        "semantic_grep": {
            "query": "${grepQuery}",
            "matches": [
                { "line": 10, "content": "risky_function()", "note": "Matches query because..." }
            ]
        },
        "structured_audit": [
            {
                "category": "security",
                "severity": "critical",
                "description": "Hardcoded API key detected.",
                "suggestion": "Use process.env.API_KEY",
                "line": 5
            }
        ]
    }
  `;

  const response = await ai.models.generateContent({
    model: 'gemini-3-pro-preview',
    contents: prompt,
    config: {
        responseMimeType: 'application/json',
        thinkingConfig: { thinkingBudget: 8192 } // High budget for rigorous audit
    }
  });

  try {
      return JSON.parse(response.text || '{}');
  } catch (e) {
      throw new Error("Failed to parse Code Audit response.");
  }
}

export async function getMissionGuidance(logs: LogItem[]): Promise<GuidanceResponse> {
    const ai = getAiClient();
    
    const sessionHistory = logs.length > 0 
        ? logs.map(log => {
            let contentStr = '';
            if (typeof log.content === 'string') {
                contentStr = log.content;
            } else {
                contentStr = `[Complex Output Type: ${log.type}]`;
            }
            return `[${log.timestamp.toLocaleTimeString()}] ${log.sender.toUpperCase()}: ${contentStr}`;
        }).slice(-15).join('\n')
        : "Session initialized. No significant actions taken yet. User is on the launchpad.";

    const prompt = `
        You are "Mission Control" (Flight Director) for a high-fidelity creative cockpit.
        
        Input Context (Recent Session Logs):
        """
        ${sessionHistory}
        """

        Task:
        1. Analyze the user's recent actions (or lack thereof).
        2. Create a "Careful Analogy" for their current workflow (e.g., "You are sculpting the marble before polishing," or "You are navigating through a nebula of data").
        3. Determine the "Coherence Score" (0-100) of their session. Are they focused or erratic?
        4. Offer high-level strategic guidance.

        Output Format (Strict JSON):
        {
            "mission_status": "Short status (e.g. 'Trajectory Nominal', 'High Entropy Detected', 'Pre-flight Check')",
            "coherence_score": 85,
            "analogy": "One sentence poetic/sci-fi analogy describing the user's current creative process.",
            "guidance": "2-3 sentences of strategic advice. Be helpful but act like a calm, experienced flight director.",
            "detected_intent": "What they seem to be building/doing.",
            "next_steps": ["Step 1", "Step 2"]
        }
    `;

    const response = await ai.models.generateContent({
        model: 'gemini-3-pro-preview',
        contents: prompt,
        config: {
            responseMimeType: 'application/json',
            thinkingConfig: { thinkingBudget: 4096 }
        }
    });

    try {
        return JSON.parse(response.text || '{}');
    } catch (e) {
        throw new Error("Failed to parse Mission Guidance.");
    }
}

export async function analyzeOpenSourcePulse(pulseData: PulseItem[]): Promise<string> {
    const ai = getAiClient();
    const dataStr = JSON.stringify(pulseData, null, 2);
    
    const prompt = `
      You are an expert Open Source Analyst & DevRel Intelligence Officer.
      
      Task: Analyze this live feed of trending repositories, models, and community news (GitHub, HuggingFace, Mistral).
      Identify the "Meta" — what is the community focusing on right now?
      
      Input Data:
      ${dataStr}
      
      Output:
      A concise, high-energy status report (3-4 sentences max). Use technical terminology.
      Mention key players like Mistral AI if they appear in the data.
      Conclude with a "Signal Strength" rating (e.g. "Signal: High // Coherence: 98%").
    `;

    const response = await ai.models.generateContent({
        model: 'gemini-3-pro-preview',
        contents: prompt,
        config: {
            thinkingConfig: { thinkingBudget: 2048 }
        }
    });
    
    return response.text || "Signal lost.";
}

export async function generateSpeech(text: string, voice: VoiceName = 'Kore'): Promise<AudioBuffer | null> {
  const ai = getAiClient();
  const response = await ai.models.generateContent({
    model: 'gemini-2.5-flash-preview-tts',
    contents: [{ parts: [{ text }] }],
    config: {
      responseModalities: [Modality.AUDIO],
      speechConfig: {
        voiceConfig: {
          prebuiltVoiceConfig: { voiceName: voice },
        },
      },
    },
  });

  const base64Audio = response.candidates?.[0]?.content?.parts?.[0]?.inlineData?.data;
  if (!base64Audio) return null;

  const audioContext = new (window.AudioContext || (window as any).webkitAudioContext)({ sampleRate: 24000 });
  return await decodeAudioData(base64ToUint8Array(base64Audio), audioContext, 24000, 1);
}