# Knowledge Representation

## Overview

Knowledge representation (KR) is the study of how to encode knowledge in a form that AI systems can use for reasoning. The choice of representation affects what can be expressed and how efficiently it can be processed.

## Representation Requirements

### Expressiveness
What knowledge can be represented?

### Efficiency
How fast can we reason?

### Clarity
Is the representation understandable?

### Modularity
Can knowledge be organized and reused?

## Representation Formalisms

### Propositional Logic
Simple true/false statements.

```
p: "It is raining"
q: "The ground is wet"
p → q: "If it is raining, then the ground is wet"
```

**Limitations**: Can't express "all", "some", variables

### First-Order Logic (Predicate Logic)
Variables, quantifiers, predicates.

```
∀x (Dog(x) → Mammal(x))
"All dogs are mammals"

∃x (Dog(x) ∧ Brown(x))
"There exists a brown dog"
```

### Description Logic
Basis for ontologies (OWL).

```
Concept: Dog ⊑ Mammal
Role: hasPart
Axiom: Dog ⊑ ∃hasPart.Tail
```

### Semantic Networks
Graph-based representation.

```
[Dog] --is-a--> [Mammal]
[Dog] --has--> [Tail]
[Fido] --instance-of--> [Dog]
```

### Frames
Structured objects with slots.

```python
Dog = Frame(
    name="Dog",
    is_a="Mammal",
    slots={
        "legs": 4,
        "sound": "bark",
        "has_tail": True
    }
)
```

### Production Rules
IF-THEN rules.

```
IF temperature > 100 AND pressure > 10
THEN status = "critical"
```

### Ontologies
Formal specification of concepts and relationships.

```turtle
:Dog rdf:type owl:Class ;
     rdfs:subClassOf :Mammal .

:hasTail rdf:type owl:ObjectProperty ;
         rdfs:domain :Dog ;
         rdfs:range :Tail .
```

## Knowledge Graphs

### Structure
```
(subject, predicate, object)
(Einstein, bornIn, Germany)
(Einstein, wonAward, NobelPrize)
```

### Building Knowledge Graphs
```python
class KnowledgeGraph:
    def __init__(self):
        self.triples = set()
        self.entities = {}

    def add_triple(self, subject, predicate, obj):
        self.triples.add((subject, predicate, obj))

    def query(self, pattern):
        """Pattern: (subject, predicate, object) with None as wildcard"""
        results = []
        for triple in self.triples:
            if self.matches(triple, pattern):
                results.append(triple)
        return results

    def matches(self, triple, pattern):
        return all(p is None or t == p
                   for t, p in zip(triple, pattern))
```

### Embeddings
Learn vector representations of entities and relations.

```python
# TransE: h + r ≈ t
def transE_score(head, relation, tail):
    return -np.linalg.norm(head + relation - tail)
```

## Reasoning with Representations

### Inheritance
```python
def get_property(entity, property):
    if property in entity.slots:
        return entity.slots[property]
    elif entity.parent:
        return get_property(entity.parent, property)
    return None
```

### Classification
```python
def classify(instance, concepts):
    for concept in concepts:
        if satisfies_definition(instance, concept):
            return concept
    return None
```

### Subsumption
Is concept A more general than concept B?

```python
def subsumes(concept_a, concept_b):
    # A subsumes B if all instances of B are instances of A
    return concept_b.is_subclass_of(concept_a)
```

## Trade-offs

### Expressiveness vs. Tractability
| Formalism | Expressiveness | Reasoning Complexity |
|-----------|----------------|---------------------|
| Propositional | Low | NP-complete |
| Description Logic (EL) | Medium | Polynomial |
| Description Logic (SHIQ) | High | ExpTime |
| First-Order Logic | Very High | Undecidable |

### Closed vs. Open World Assumption
- **Closed World**: What's not known is false
- **Open World**: What's not known is unknown

## Applications

### Semantic Web
- RDF, OWL, SPARQL
- Linked data
- Knowledge graphs

### Expert Systems
- Rule bases
- Frame systems
- Diagnostic systems

### Natural Language Understanding
- Word sense disambiguation
- Semantic parsing
- Question answering

### Robotics
- World models
- Action planning
- Spatial reasoning

## Exercises

1. Model a domain in first-order logic
2. Build a simple semantic network
3. Create frame hierarchy with inheritance
4. Implement knowledge graph with queries
5. Compare expressiveness of different formalisms

## Key Insights

- **No universal representation**: Choose based on needs
- **Trade-offs are fundamental**: Expressiveness vs. efficiency
- **Semantics matter**: Formal semantics enable reasoning
- **Hybrid approaches**: Combine formalisms for best results

---

**Status**: Foundation established
**Last Updated**: December 2025
**Maintainer**: GRID Foundations Team
