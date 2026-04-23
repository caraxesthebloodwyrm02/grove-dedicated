# Machine Translation

## Overview

Machine translation (MT) automatically translates text from one language to another. Modern neural MT systems achieve near-human quality for many language pairs.

## Evolution of MT

### Rule-Based MT
- Linguistic rules for translation
- Dictionaries and grammars
- High quality for narrow domains
- Expensive to build and maintain

### Statistical MT
- Learn from parallel corpora
- Phrase-based models
- Language models for fluency
- Dominated 2000s-2015

### Neural MT
- End-to-end deep learning
- Encoder-decoder architecture
- Attention mechanisms
- Current state-of-the-art

## Neural MT Architecture

### Encoder-Decoder
```python
class Seq2Seq(nn.Module):
    def __init__(self, src_vocab, tgt_vocab, embed_dim, hidden_dim):
        self.encoder = nn.LSTM(embed_dim, hidden_dim)
        self.decoder = nn.LSTM(embed_dim, hidden_dim)
        self.src_embed = nn.Embedding(src_vocab, embed_dim)
        self.tgt_embed = nn.Embedding(tgt_vocab, embed_dim)
        self.output = nn.Linear(hidden_dim, tgt_vocab)

    def forward(self, src, tgt):
        # Encode source
        src_embedded = self.src_embed(src)
        _, (hidden, cell) = self.encoder(src_embedded)

        # Decode target
        tgt_embedded = self.tgt_embed(tgt)
        output, _ = self.decoder(tgt_embedded, (hidden, cell))

        return self.output(output)
```

### Attention Mechanism
```python
class Attention(nn.Module):
    def forward(self, decoder_hidden, encoder_outputs):
        # Calculate attention scores
        scores = torch.bmm(encoder_outputs, decoder_hidden.unsqueeze(2))
        weights = F.softmax(scores, dim=1)

        # Weighted sum of encoder outputs
        context = torch.bmm(weights.transpose(1, 2), encoder_outputs)
        return context, weights
```

### Transformer-Based MT
```python
from transformers import MarianMTModel, MarianTokenizer

model_name = 'Helsinki-NLP/opus-mt-en-de'
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

text = "Hello, how are you?"
inputs = tokenizer(text, return_tensors="pt")
outputs = model.generate(**inputs)
translation = tokenizer.decode(outputs[0], skip_special_tokens=True)
```

## Training

### Parallel Corpora
Aligned sentence pairs in source and target languages.

### Training Objective
```python
# Cross-entropy loss on target tokens
loss = F.cross_entropy(predictions, targets, ignore_index=PAD_IDX)
```

### Techniques
- **Teacher forcing**: Use ground truth as decoder input
- **Label smoothing**: Soften target distribution
- **Back-translation**: Generate synthetic parallel data

## Decoding Strategies

### Greedy Decoding
```python
def greedy_decode(model, src, max_len):
    output = [BOS_IDX]
    for _ in range(max_len):
        pred = model(src, output)
        next_token = pred[-1].argmax()
        output.append(next_token)
        if next_token == EOS_IDX:
            break
    return output
```

### Beam Search
```python
def beam_search(model, src, beam_size, max_len):
    beams = [(0, [BOS_IDX])]  # (score, sequence)

    for _ in range(max_len):
        candidates = []
        for score, seq in beams:
            if seq[-1] == EOS_IDX:
                candidates.append((score, seq))
                continue

            pred = model(src, seq)
            probs = F.log_softmax(pred[-1], dim=-1)
            top_k = probs.topk(beam_size)

            for prob, idx in zip(top_k.values, top_k.indices):
                candidates.append((score + prob, seq + [idx]))

        beams = sorted(candidates, reverse=True)[:beam_size]

    return beams[0][1]
```

## Evaluation

### BLEU Score
```python
from nltk.translate.bleu_score import sentence_bleu
reference = [['the', 'cat', 'sat']]
candidate = ['the', 'cat', 'sat']
score = sentence_bleu(reference, candidate)
```

### Human Evaluation
- Fluency: Is the translation grammatical?
- Adequacy: Is the meaning preserved?
- Overall quality ratings

## Challenges

### Low-Resource Languages
- Limited parallel data
- Transfer learning from related languages
- Multilingual models

### Domain Adaptation
- General models struggle with specialized text
- Fine-tuning on domain data
- Terminology management

### Long Documents
- Context beyond sentence level
- Document-level coherence
- Coreference resolution

## Exercises

1. Build simple encoder-decoder MT
2. Add attention mechanism
3. Implement beam search decoding
4. Evaluate with BLEU score
5. Fine-tune pre-trained MT model

## Key Insights

- **Attention is crucial**: Enables handling long sentences
- **Transformers excel**: Parallel computation, better quality
- **Data quality matters**: Clean parallel data is essential
- **Evaluation is imperfect**: BLEU doesn't capture everything

---

**Status**: Foundation established
**Last Updated**: December 2025
**Maintainer**: GRID Foundations Team
