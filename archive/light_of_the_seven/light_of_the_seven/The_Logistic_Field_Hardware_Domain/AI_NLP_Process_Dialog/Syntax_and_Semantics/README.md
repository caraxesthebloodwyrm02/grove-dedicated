# Syntax and Semantics (NLP)

## Overview

Syntax deals with the structure of sentences (how words combine), while semantics deals with meaning (what sentences mean). Together they enable deep understanding of natural language.

## Syntax

### Grammatical Categories

#### Parts of Speech
- **Noun (N)**: person, place, thing
- **Verb (V)**: action, state
- **Adjective (Adj)**: modifies noun
- **Adverb (Adv)**: modifies verb
- **Determiner (Det)**: the, a, this
- **Preposition (P)**: in, on, at
- **Conjunction (Conj)**: and, or, but

#### Phrases
- **Noun Phrase (NP)**: "the big dog"
- **Verb Phrase (VP)**: "runs quickly"
- **Prepositional Phrase (PP)**: "in the house"

### Syntactic Structures

#### Phrase Structure Rules
```
S  → NP VP
NP → (Det) (Adj)* N (PP)*
VP → V (NP) (PP)* (Adv)*
PP → P NP
```

#### X-Bar Theory
```
XP → (Specifier) X'
X' → X (Complement)
```

### Syntactic Relations

#### Subject and Object
```
"John [subject] saw Mary [object]"
```

#### Agreement
```
"The dog runs" (singular)
"The dogs run" (plural)
```

#### Movement
```
"What did you see __?"
(wh-movement from object position)
```

## Semantics

### Lexical Semantics
Meaning of individual words.

#### Word Senses
```
"bank" → financial institution
"bank" → river edge
```

#### Semantic Relations
- **Synonymy**: big/large
- **Antonymy**: hot/cold
- **Hyponymy**: dog is-a animal
- **Meronymy**: wheel part-of car

### Compositional Semantics
How word meanings combine.

#### Principle of Compositionality
The meaning of a complex expression is determined by:
1. Meanings of its parts
2. How they are combined

#### Lambda Calculus
```
"every" = λP.λQ.∀x[P(x) → Q(x)]
"student" = λx.student(x)
"sleeps" = λx.sleep(x)

"every student sleeps" = ∀x[student(x) → sleep(x)]
```

### Formal Semantics

#### First-Order Logic
```
"John loves Mary"
→ loves(john, mary)

"Every student passed"
→ ∀x[student(x) → passed(x)]

"Some student failed"
→ ∃x[student(x) ∧ failed(x)]
```

#### Model-Theoretic Semantics
```
Model M = (D, I)
D: Domain of entities
I: Interpretation function

I(john) = some entity in D
I(loves) = set of pairs in D×D
```

### Semantic Roles
```
"John gave Mary a book"

Agent: John (doer)
Theme: book (thing affected)
Recipient: Mary (receiver)
```

### Word Sense Disambiguation
```python
from nltk.wsd import lesk

sentence = "I went to the bank to deposit money"
word = "bank"
sense = lesk(sentence.split(), word)
# Returns: Synset('bank.n.01') - financial institution
```

## Pragmatics

### Speech Acts
- **Locutionary**: What is said
- **Illocutionary**: What is meant (request, promise, etc.)
- **Perlocutionary**: Effect on hearer

### Implicature
```
A: "Can you pass the salt?"
B: (passes salt)

Literal: Yes/No question
Implied: Request to pass salt
```

### Reference Resolution
```
"John saw Bill. He waved."
Who is "he"? (John or Bill)
```

## Computational Approaches

### Semantic Parsing
```python
# Text to logical form
"What is the capital of France?"
→ answer(x, capital(france, x))
```

### Semantic Similarity
```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
emb1 = model.encode("The cat sat on the mat")
emb2 = model.encode("A feline rested on the rug")
similarity = cosine_similarity(emb1, emb2)
```

### Natural Language Inference
```python
from transformers import pipeline

nli = pipeline('text-classification', model='roberta-large-mnli')
result = nli("A man is playing guitar. [SEP] A person is making music.")
# Entailment, Contradiction, or Neutral
```

## Exercises

1. Parse sentence and identify constituents
2. Translate sentence to first-order logic
3. Identify semantic roles in sentences
4. Implement word sense disambiguation
5. Build semantic similarity system

## Key Insights

- **Syntax constrains meaning**: Structure affects interpretation
- **Compositionality is powerful**: Build complex from simple
- **Ambiguity is pervasive**: Multiple parses, multiple meanings
- **Context matters**: Pragmatics resolves ambiguity

---

**Status**: Foundation established
**Last Updated**: December 2025
**Maintainer**: GRID Foundations Team
