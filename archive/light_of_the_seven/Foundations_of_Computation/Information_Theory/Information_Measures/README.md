# Information Measures

## Overview

Information measures quantify the amount, quality, and characteristics of information in data. These metrics form the basis for analyzing systems, optimizing compression, and understanding data relationships.

## Fundamental Measures

### Shannon Information (Self-Information)

The amount of information gained from an event:

$$I(x) = -\log_2 P(x) = \log_2 \frac{1}{P(x)}$$

- Measured in **bits** (base 2)
- Certain event (P=1): 0 bits
- Unlikely event (P→0): High information content
- Fair coin flip (P=0.5): 1 bit

### Shannon Entropy

Average information per symbol:

$$H(X) = -\sum_{x} p(x) \log_2 p(x)$$

**Properties**:
- Quantifies uncertainty in random variable
- Maximum for uniform distribution
- Zero for deterministic outcomes
- Units: bits per symbol

### Joint Entropy

Entropy of multiple variables:

$$H(X,Y) = -\sum_{x,y} p(x,y) \log_2 p(x,y)$$

**Intuition**: Uncertainty when observing both variables together

### Conditional Entropy

Uncertainty in Y given knowledge of X:

$$H(Y|X) = -\sum_{x} p(x) \sum_{y} p(y|x) \log_2 p(y|x)$$

**Interpretation**: Remaining uncertainty after observing X

## Information-Theoretic Quantities

### Mutual Information

Information X contains about Y:

$$I(X;Y) = H(X) - H(X|Y) = H(Y) - H(Y|X)$$

**Alternative formula**:
$$I(X;Y) = \sum_{x,y} p(x,y) \log_2 \frac{p(x,y)}{p(x)p(y)}$$

**Properties**:
- Symmetric: I(X;Y) = I(Y;X)
- Non-negative: I(X;Y) ≥ 0
- Zero if independent
- Measures dependency strength

### Information Gain

Reduction in entropy through feature observation:

$$\text{IG}(Y|X) = H(Y) - H(Y|X)$$

**Applications**:
- Decision tree splitting criteria
- Feature selection for machine learning
- Identifying discriminative features

### Relative Entropy (KL Divergence)

Distance between probability distributions:

$$D_{KL}(P||Q) = \sum_{x} p(x) \log_2 \frac{p(x)}{q(x)}$$

**Properties**:
- Non-symmetric
- Non-negative
- Zero only when P = Q
- Not a true metric (triangle inequality fails)

### Jensen-Shannon Distance

Symmetric divergence measure:

$$JS(P||Q) = \frac{1}{2}D_{KL}(P||M) + \frac{1}{2}D_{KL}(Q||M)$$

where $M = \frac{P+Q}{2}$

**Advantages**:
- Symmetric
- Bounded: 0 ≤ JS ≤ 1
- Always defined (numerically stable)

## Derived Measures

### Channel Capacity

Maximum information rate over noisy channel:

$$C = \max_{p(x)} I(X;Y)$$

**Shannon's Noisy Channel Coding Theorem**:
$$C = \log_2(1 + \text{SNR})$$ (Gaussian channel)

### Perplexity

Measures quality of probability distributions:

$$\text{Perplexity}(X) = 2^{H(X)}$$

**Interpretation**:
- Geometric mean of inverse probabilities
- Used in language model evaluation
- Lower perplexity = better model

### Cross-Entropy

Entropy between true and predicted distributions:

$$H(p, q) = -\sum_{x} p(x) \log_2 q(x)$$

**Relationship**:
$$H(p,q) = H(p) + D_{KL}(p||q)$$

**Application**: Loss function in machine learning

## Information Dynamics

### Entropy Rate

Entropy per symbol in stochastic process:

$$H_\mu = \lim_{n \to \infty} \frac{1}{n}H(X_1, X_2, \ldots, X_n)$$

**Properties**:
- Measures "randomness" of process
- Independent processes have sum entropy rates
- Markov processes: $H_\mu = H(X_n|X_{n-1})$

### Channel Mutual Information Rate

Information flow per time step:

$$I_\mu = \lim_{n \to \infty} \frac{1}{n}I(X_1...X_n; Y_1...Y_n)$$

## Advanced Information Measures

### Renyi Entropy

Parametric generalization:

$$H_\alpha(X) = \frac{1}{1-\alpha}\log_2\sum_{x}p(x)^\alpha$$

**Special cases**:
- α → 1: Shannon entropy
- α = 2: Collision entropy
- α → ∞: Min-entropy

### Fisher Information

Sensitivity of distribution to parameter changes:

$$I(\theta) = -E\left[\frac{d^2}{d\theta^2}\log p(x|\theta)\right]$$

**Applications**:
- Parameter estimation quality
- Cramér-Rao lower bound
- Neural network analysis

### Quantum Information

Extensions to quantum systems:

$$S(\rho) = -\text{tr}(\rho \log_2 \rho)$$

- Von Neumann entropy
- Quantum mutual information
- Entanglement measures

## Practical Computation

### From Empirical Data

For samples from distribution:
$$\hat{H} = -\sum_x \frac{n_x}{N} \log_2\frac{n_x}{N}$$

where $n_x$ = count of outcome x, N = total samples

### Bias Correction Methods

Raw estimates are biased:
- **Miller-Madow**: +k/(2N) correction
- **Chao-Shen**: Minimax optimal
- **Bayesian**: Prior-based approaches

### Computational Stability

- Avoid log(0): Replace with pseudocount
- Use log-space arithmetic for products
- Normalize for numerical stability

## Applications

### Machine Learning

- **Decision Trees**: Information gain for splits
- **Classification**: Cross-entropy loss
- **Feature Selection**: Mutual information ranking
- **Clustering**: Entropy-based criteria

### Data Analysis

- **Distribution Comparison**: KL divergence
- **Anomaly Detection**: Entropy changes
- **Time Series**: Entropy rate analysis
- **Network Analysis**: Information flow

### Compression

- **Theoretical Bound**: Shannon entropy
- **Optimal Length**: -log₂ P(x) bits per symbol
- **Huffman Coding**: Achieves near-optimal
- **Arithmetic Coding**: Approaches Shannon limit

### Communication

- **Channel Capacity**: Maximum sustainable rate
- **Coding Theory**: Information limits
- **Modulation**: Efficient symbol mapping
- **Bandwidth**: Information per Hz

## Information Hierarchy

```
Entropy (uncertainty measure)
    ├── Self-Information (single outcome)
    ├── Joint Entropy (multiple variables)
    ├── Conditional Entropy (with knowledge)
    └── Mutual Information (shared information)
         ├── Information Gain (feature value)
         └── Channel Capacity (max transmission)
```

## Tools & Implementation

### Python Libraries

```python
# scipy
from scipy.stats import entropy

# Custom calculations
def calculate_entropy(probabilities):
    return -np.sum(probabilities * np.log2(probabilities + 1e-10))

def mutual_information(joint_dist, p_x, p_y):
    return np.sum(joint_dist * np.log2(joint_dist / (p_x[:, None] * p_y[None, :]) + 1e-10))
```

## Exercises

1. Calculate entropy from frequency data
2. Compare distributions using KL divergence
3. Compute mutual information for variables
4. Estimate channel capacity
5. Optimize compression using information measures

## Key Insights

- **Information is quantifiable**: Mathematical measures for information content
- **Entropy is fundamental**: Limits on compression and transmission
- **Trade-offs exist**: Accuracy vs. complexity, detail vs. generality
- **Information flows**: Between systems with measurable efficiency

## Related Topics

- **Entropy and Information**: Conceptual foundations
- **Data Compression**: Practical application
- **Shannon's Theory**: Mathematical framework
- **Error Correction Codes**: Using redundancy based on information theory

---

**Status**: Framework established
**Last Updated**: December 2025
**Maintainer**: GRID Foundations Team
