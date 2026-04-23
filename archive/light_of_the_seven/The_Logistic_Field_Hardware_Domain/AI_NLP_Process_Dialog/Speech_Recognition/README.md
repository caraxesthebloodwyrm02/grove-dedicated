# Speech Recognition

## Overview

Speech recognition (ASR - Automatic Speech Recognition) converts spoken language into text. Modern systems achieve near-human accuracy for many languages and domains.

## ASR Pipeline

```
Audio → Preprocessing → Feature Extraction → Acoustic Model → Language Model → Text
```

## Audio Preprocessing

### Sampling
```python
import librosa

# Load audio
audio, sr = librosa.load('speech.wav', sr=16000)

# Resample if needed
audio_resampled = librosa.resample(audio, orig_sr=sr, target_sr=16000)
```

### Noise Reduction
```python
import noisereduce as nr

# Reduce background noise
reduced_noise = nr.reduce_noise(y=audio, sr=sr)
```

### Voice Activity Detection
```python
def vad(audio, threshold=0.01):
    """Simple energy-based VAD"""
    energy = audio ** 2
    is_speech = energy > threshold
    return is_speech
```

## Feature Extraction

### Mel-Frequency Cepstral Coefficients (MFCCs)
```python
import librosa

# Extract MFCCs
mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13)

# Add delta and delta-delta
delta = librosa.feature.delta(mfccs)
delta2 = librosa.feature.delta(mfccs, order=2)
features = np.concatenate([mfccs, delta, delta2])
```

### Mel Spectrograms
```python
mel_spec = librosa.feature.melspectrogram(y=audio, sr=sr, n_mels=80)
log_mel = librosa.power_to_db(mel_spec)
```

### Filter Banks
```python
fbank = librosa.feature.melspectrogram(y=audio, sr=sr, n_mels=40)
```

## Traditional ASR

### Hidden Markov Models (HMM)
```
States: Phonemes or sub-phonemes
Observations: Acoustic features
Transitions: Phoneme sequences
```

### Gaussian Mixture Models (GMM)
Model emission probabilities for HMM states.

### Decoding
```
Best transcription = argmax P(audio|text) × P(text)
                   = argmax (Acoustic Model) × (Language Model)
```

## Neural ASR

### CTC (Connectionist Temporal Classification)
```python
import torch.nn as nn

class CTCModel(nn.Module):
    def __init__(self, input_dim, hidden_dim, vocab_size):
        self.encoder = nn.LSTM(input_dim, hidden_dim,
                               num_layers=3, bidirectional=True)
        self.fc = nn.Linear(hidden_dim * 2, vocab_size)

    def forward(self, x):
        output, _ = self.encoder(x)
        logits = self.fc(output)
        return F.log_softmax(logits, dim=-1)

# CTC Loss
ctc_loss = nn.CTCLoss(blank=0)
loss = ctc_loss(log_probs, targets, input_lengths, target_lengths)
```

### Attention-Based (Listen, Attend, Spell)
```python
class LAS(nn.Module):
    def __init__(self):
        self.encoder = Encoder()  # Pyramidal LSTM
        self.attention = Attention()
        self.decoder = Decoder()  # LSTM with attention

    def forward(self, audio, text):
        encoder_out = self.encoder(audio)
        output = self.decoder(text, encoder_out, self.attention)
        return output
```

### Transformer-Based (Wav2Vec, Whisper)
```python
from transformers import WhisperProcessor, WhisperForConditionalGeneration

processor = WhisperProcessor.from_pretrained("openai/whisper-base")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-base")

# Transcribe
input_features = processor(audio, sampling_rate=16000, return_tensors="pt")
predicted_ids = model.generate(input_features.input_features)
transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)
```

## Language Models

### N-gram LM
```python
# Probability of word sequence
P(w1, w2, w3) = P(w1) × P(w2|w1) × P(w3|w1,w2)

# Bigram approximation
P(w3|w1,w2) ≈ P(w3|w2)
```

### Neural LM
Transformer-based language models for rescoring.

## Decoding

### Greedy Decoding
Take most probable token at each step.

### Beam Search
```python
def beam_search_decode(model, audio, beam_size=5):
    beams = [(0.0, [])]  # (score, tokens)

    for t in range(max_len):
        candidates = []
        for score, tokens in beams:
            probs = model.step(audio, tokens)
            for token, prob in enumerate(probs):
                candidates.append((score + log(prob), tokens + [token]))

        beams = sorted(candidates, reverse=True)[:beam_size]

    return beams[0][1]
```

### Language Model Fusion
```
score = α × acoustic_score + β × lm_score + γ × length_penalty
```

## Evaluation

### Word Error Rate (WER)
```python
def wer(reference, hypothesis):
    # Levenshtein distance at word level
    r_words = reference.split()
    h_words = hypothesis.split()

    # Dynamic programming for edit distance
    d = edit_distance(r_words, h_words)

    return d / len(r_words)
```

### Character Error Rate (CER)
Same as WER but at character level.

## Challenges

### Noise and Reverberation
- Far-field microphones
- Background noise
- Room acoustics

### Accents and Dialects
- Regional variations
- Non-native speakers
- Code-switching

### Domain Adaptation
- Medical terminology
- Legal jargon
- Technical vocabulary

## Exercises

1. Extract MFCC features from audio
2. Build simple CTC-based ASR
3. Use Whisper for transcription
4. Calculate WER on test set
5. Add language model rescoring

## Key Insights

- **End-to-end is dominant**: CTC and attention-based models
- **Pre-training helps**: Wav2Vec, Whisper leverage large data
- **LM integration matters**: Improves accuracy significantly
- **Domain adaptation needed**: General models struggle with specialized vocabulary

---

**Status**: Foundation established
**Last Updated**: December 2025
**Maintainer**: GRID Foundations Team
