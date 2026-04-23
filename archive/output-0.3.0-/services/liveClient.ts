import { GoogleGenAI, LiveServerMessage, Modality } from "@google/genai";
import { base64ToUint8Array, createPcmBlob, decodeAudioData } from "./audioUtils";
import { VoiceName } from "../types";

interface LiveSessionConfig {
  voiceName: VoiceName;
  onOpen: () => void;
  onMessage: (message: LiveServerMessage) => void;
  onError: (error: ErrorEvent) => void;
  onClose: (event: CloseEvent) => void;
  onAudioData: (buffer: AudioBuffer) => void;
}

export class LiveClient {
  private ai: GoogleGenAI;
  private session: any = null;
  private sessionPromise: Promise<any> | null = null;
  private inputAudioContext: AudioContext | null = null;
  private config: LiveSessionConfig;
  private stream: MediaStream | null = null;
  private processor: ScriptProcessorNode | null = null;
  private source: MediaStreamAudioSourceNode | null = null;

  constructor(config: LiveSessionConfig) {
    this.ai = new GoogleGenAI({ apiKey: process.env.API_KEY });
    this.config = config;
  }

  public async connect() {
    this.inputAudioContext = new (window.AudioContext || (window as any).webkitAudioContext)({ sampleRate: 16000 });
    
    this.sessionPromise = this.ai.live.connect({
      model: 'gemini-2.5-flash-native-audio-preview-09-2025',
      callbacks: {
        onopen: () => {
          this.config.onOpen();
          this.startAudioInput();
        },
        onmessage: async (msg: LiveServerMessage) => {
          this.config.onMessage(msg);
          
          const base64Audio = msg.serverContent?.modelTurn?.parts?.[0]?.inlineData?.data;
          if (base64Audio) {
             const audioContext = new (window.AudioContext || (window as any).webkitAudioContext)({ sampleRate: 24000 });
             const buffer = await decodeAudioData(base64ToUint8Array(base64Audio), audioContext, 24000, 1);
             this.config.onAudioData(buffer);
          }
        },
        onerror: this.config.onError,
        onclose: this.config.onClose,
      },
      config: {
        responseModalities: [Modality.AUDIO],
        speechConfig: {
          voiceConfig: { prebuiltVoiceConfig: { voiceName: this.config.voiceName } },
        },
        systemInstruction: "You are a helpful, creative assistant in a high-tech creative studio. You can see the user's video feed if enabled.",
      },
    });

    try {
        this.session = await this.sessionPromise;
    } catch (e) {
        console.error("Connection failed", e);
    }
  }

  public sendImage(base64Data: string) {
    if (this.sessionPromise) {
        this.sessionPromise.then(session => {
             session.sendRealtimeInput({
                  media: { data: base64Data, mimeType: 'image/jpeg' }
             });
        });
    }
  }

  private async startAudioInput() {
    if (!this.inputAudioContext) return;
    
    try {
      this.stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      this.source = this.inputAudioContext.createMediaStreamSource(this.stream);
      this.processor = this.inputAudioContext.createScriptProcessor(4096, 1, 1);

      this.processor.onaudioprocess = (e) => {
        const inputData = e.inputBuffer.getChannelData(0);
        const pcmBlob = createPcmBlob(inputData);
        
        if (this.sessionPromise) {
            this.sessionPromise.then(session => {
                session.sendRealtimeInput({ media: pcmBlob });
            });
        }
      };

      this.source.connect(this.processor);
      this.processor.connect(this.inputAudioContext.destination);
    } catch (err) {
      console.error("Error accessing microphone:", err);
    }
  }

  public disconnect() {
    if (this.stream) {
      this.stream.getTracks().forEach(track => track.stop());
    }
    if (this.processor && this.source) {
      this.source.disconnect(this.processor);
      this.processor.disconnect();
    }
    if (this.inputAudioContext) {
      this.inputAudioContext.close();
    }
  }
}