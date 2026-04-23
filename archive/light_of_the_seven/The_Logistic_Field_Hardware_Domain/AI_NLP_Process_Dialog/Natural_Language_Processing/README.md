# Natural Language Processing

## Overview

Natural Language Processing (NLP) is the field of AI focused on enabling computers to understand, interpret, and generate human language. It bridges linguistics, computer science, and machine learning.

## NLP Pipeline

```
Text → Tokenization → POS Tagging → Parsing → NER → Semantic Analysis → Application
```

## Core Tasks

### Tokenization
Split text into tokens (words, subwords, characters).

```python
# Word tokenization
text = "Hello, world!"
tokens = text.split()  # Simple
# Better: use nltk or spacy

# Subword tokenization (BPE, WordPiece)
from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
tokens = tokenizer.tokenize("Hello, world!")
```

### Part-of-Speech Tagging
Label words with grammatical categories.

```python
import spacy
nlp = spacy.load('en_core_web_sm')
doc = nlp("The quick brown fox jumps")
for token in doc:
    print(f"{token.text}: {token.pos_}")
# The: DET, quick: ADJ, brown: ADJ, fox: NOUN, jumps: VERB
```

### Named Entity Recognition
Identify and classify named entities.

```python
doc = nlp("Apple Inc. was founded by Steve Jobs in California.")
for ent in doc.ents:
    print(f"{ent.text}: {ent.label_}")
# Apple Inc.: ORG, Steve Jobs: PERSON, California: GPE
```

### Dependency Parsing
Analyze grammatical structure.

```python
doc = nlp("The cat sat on the mat")
for token in doc:
    print(f"{token.text} --{token.dep_}--> {token.head.text}")
```

### Sentiment Analysis
Determine emotional tone.

```python
from transformers import pipeline
sentiment = pipeline('sentiment-analysis')
result = sentiment("I love this product!")
# [{'label': 'POSITIVE', 'score': 0.9998}]
```

## Text Representation

### Bag of Words
```python
from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(documents)
```

### TF-IDF
```python
from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(documents)
```

### Word Embeddings
```python
# Word2Vec
from gensim.models import Word2Vec
model = Word2Vec(sentences, vector_size=100, window=5)
vector = model.wv['word']

# Pre-trained embeddings
import gensim.downloader
glove = gensim.downloader.load('glove-wiki-gigaword-100')
```

### Contextual Embeddings
```python
from transformers import AutoModel, AutoTokenizer
model = AutoModel.from_pretrained('bert-base-uncased')
tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')

inputs = tokenizer("Hello world", return_tensors="pt")
outputs = model(**inputs)
embeddings = outputs.last_hidden_state
```

## Modern NLP with Transformers

### Text Classification
```python
from transformers import pipeline
classifier = pipeline('text-classification')
result = classifier("This movie was great!")
```

### Question Answering
```python
qa = pipeline('question-answering')
result = qa(question="What is NLP?",
            context="NLP is natural language processing...")
```

### Text Generation
```python
generator = pipeline('text-generation')
result = generator("Once upon a time", max_length=50)
```

### Summarization
```python
summarizer = pipeline('summarization')
result = summarizer(long_text, max_length=100)
```

## Evaluation Metrics

### Classification
- Accuracy, Precision, Recall, F1

### Generation
- BLEU, ROUGE, METEOR
- Perplexity

### Semantic Similarity
- Cosine similarity
- Word Mover's Distance

## Exercises

1. Build text classification pipeline
2. Implement named entity recognition
3. Train word embeddings on custom corpus
4. Fine-tune BERT for sentiment analysis
5. Build simple question-answering system

## Key Insights

- **Transformers dominate**: Pre-trained models are state-of-the-art
- **Transfer learning works**: Fine-tune, don't train from scratch
- **Context matters**: Contextual embeddings outperform static
- **Evaluation is hard**: Multiple metrics needed

---

**Status**: Foundation established
**Last Updated**: December 2025
**Maintainer**: GRID Foundations Team
