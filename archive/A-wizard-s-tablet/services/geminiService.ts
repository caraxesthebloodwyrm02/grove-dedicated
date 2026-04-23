import { GoogleGenAI } from "@google/genai";
import { AppState, House } from "../types";

const getSystemInstruction = (house: House) => `
You are the Head of Arithmancy at Hogwarts.
Your House allegiance is ${house}, which influences your tone (Gryffindor: bold/direct; Slytherin: cunning/ambitious; Ravenclaw: analytical/witty; Hufflepuff: supportive/practical).
Your task is to analyze the "Magical Signature" data provided in JSON format.
The data includes "knobs" (input parameters) and "analyzer" (output spectral bands).

Analyze the relationship between the inputs and outputs.
Identify critical issues (e.g., High Noise + Low Clarity is dangerous spellwork).
Provide 3 distinct, actionable recommendations to stabilize or enhance the spell matrix.
Keep the response strictly formatted as a JSON object with this schema:
{
  "summary": "A one sentence overview of the current magical field status.",
  "status": "STABLE" | "VOLATILE" | "CRITICAL",
  "insights": [
    { "title": "Insight Title", "description": "Short explanation", "type": "warning" | "info" | "success" },
    ... (max 3)
  ]
}
Do not return Markdown code blocks. Return raw JSON.
`;

export const analyzeMagicalSignature = async (state: AppState, house: House) => {
  try {
    const apiKey = process.env.API_KEY;
    if (!apiKey) throw new Error("API Key not found");

    const ai = new GoogleGenAI({ apiKey });
    
    // We strip the history to save tokens, just sending current state
    const context = JSON.stringify({
      knobs: state.knobs,
      bands: state.analyzer.bands
    });

    const response = await ai.models.generateContent({
      model: 'gemini-2.5-flash',
      contents: `Current Magical Metrics: ${context}`,
      config: {
        systemInstruction: getSystemInstruction(house),
        responseMimeType: 'application/json'
      }
    });

    const text = response.text;
    if (!text) return null;
    
    return JSON.parse(text);
  } catch (error) {
    console.error("Arithmancy Analysis Failed:", error);
    return null;
  }
};
