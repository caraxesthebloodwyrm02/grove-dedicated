# Parsing Techniques (NLP)

## Overview

Parsing in NLP analyzes the grammatical structure of sentences. It identifies how words relate to each other and builds tree structures representing syntactic relationships.

## Types of Parsing

### Constituency Parsing
Breaks sentences into nested constituents (phrases).

```
        S
       / \
      NP  VP
     /   / \
   The  V   NP
       |   / \
      saw Det  N
           |   |
          the cat
```

### Dependency Parsing
Shows relationships between words directly.

```
saw (ROOT)
├── I (nsubj)
└── cat (dobj)
    └── the (det)
```

## Constituency Parsing

### Context-Free Grammar
```
S  → NP VP
NP → Det N | Det Adj N | NP PP
VP → V | V NP | V NP PP
PP → P NP
```

### CKY Algorithm
Bottom-up chart parsing.

```python
def cky_parse(words, grammar):
    n = len(words)
    table = [[set() for _ in range(n+1)] for _ in range(n+1)]

    # Fill diagonal (single words)
    for i, word in enumerate(words):
        for rule in grammar.rules:
            if rule.rhs == [word]:
                table[i][i+1].add(rule.lhs)

    # Fill upper triangle
    for length in range(2, n+1):
        for i in range(n - length + 1):
            j = i + length
            for k in range(i+1, j):
                for rule in grammar.rules:
                    if len(rule.rhs) == 2:
                        B, C = rule.rhs
                        if B in table[i][k] and C in table[k][j]:
                            table[i][j].add(rule.lhs)

    return 'S' in table[0][n]
```

### Probabilistic CFG
```python
# Rules with probabilities
S → NP VP [1.0]
NP → Det N [0.6]
NP → Det Adj N [0.4]
```

## Dependency Parsing

### Transition-Based Parsing
```python
class ArcStandard:
    def __init__(self):
        self.stack = []
        self.buffer = []
        self.arcs = []

    def shift(self):
        self.stack.append(self.buffer.pop(0))

    def left_arc(self, label):
        dependent = self.stack.pop(-2)
        head = self.stack[-1]
        self.arcs.append((head, label, dependent))

    def right_arc(self, label):
        dependent = self.stack.pop()
        head = self.stack[-1]
        self.arcs.append((head, label, dependent))
```

### Graph-Based Parsing
Find maximum spanning tree over possible arcs.

```python
def eisner_parse(scores):
    """
    Eisner's algorithm for projective dependency parsing.
    scores[i][j] = score of arc from i to j
    """
    n = len(scores)
    # Dynamic programming over spans
    # Returns highest-scoring projective tree
    pass
```

### Neural Dependency Parser
```python
class DependencyParser(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim, num_labels):
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.lstm = nn.LSTM(embed_dim, hidden_dim, bidirectional=True)
        self.arc_scorer = nn.Bilinear(hidden_dim*2, hidden_dim*2, 1)
        self.label_scorer = nn.Bilinear(hidden_dim*2, hidden_dim*2, num_labels)

    def forward(self, words):
        embeds = self.embedding(words)
        hidden, _ = self.lstm(embeds)

        # Score all possible arcs
        arc_scores = self.arc_scorer(hidden, hidden)

        return arc_scores
```

## Semantic Parsing

### Meaning Representation
```
"What is the capital of France?"
→ answer(capital(france))

"Show me flights from Boston to Seattle"
→ flight(from=boston, to=seattle)
```

### Semantic Role Labeling
```
"John gave Mary a book"
give.01
├── ARG0: John (giver)
├── ARG1: book (thing given)
└── ARG2: Mary (recipient)
```

## Using Modern Tools

### spaCy
```python
import spacy
nlp = spacy.load('en_core_web_sm')
doc = nlp("The quick brown fox jumps over the lazy dog")

# Dependency parse
for token in doc:
    print(f"{token.text} --{token.dep_}--> {token.head.text}")

# Noun chunks (constituency-like)
for chunk in doc.noun_chunks:
    print(chunk.text)
```

### Stanza
```python
import stanza
nlp = stanza.Pipeline('en')
doc = nlp("The cat sat on the mat")

for sentence in doc.sentences:
    for word in sentence.words:
        print(f"{word.text}: {word.deprel} -> {word.head}")
```

## Evaluation

### Labeled Attachment Score (LAS)
Percentage of words with correct head AND label.

### Unlabeled Attachment Score (UAS)
Percentage of words with correct head.

### PARSEVAL Metrics
For constituency: Precision, Recall, F1 on brackets.

## Exercises

1. Implement CKY parser
2. Build transition-based dependency parser
3. Train neural dependency parser
4. Convert between constituency and dependency
5. Evaluate parser on treebank

## Key Insights

- **Dependencies are popular**: Simpler, language-independent
- **Neural parsers dominate**: End-to-end learning
- **Ambiguity is pervasive**: Many valid parses exist
- **Context helps**: Transformers improve parsing

---

**Status**: Foundation established
**Last Updated**: December 2025
**Maintainer**: GRID Foundations Team
