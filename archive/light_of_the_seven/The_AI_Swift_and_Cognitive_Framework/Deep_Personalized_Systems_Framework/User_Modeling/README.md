# User Modeling

## Overview

User modeling creates computational representations of users to enable personalization. Models capture user characteristics, preferences, knowledge, goals, and behavior patterns.

## Types of User Models

### Demographic Models
Static attributes about the user.

```python
class DemographicModel:
    def __init__(self):
        self.age_group = None
        self.location = None
        self.language = None
        self.occupation = None
        self.education = None
```

### Behavioral Models
Patterns derived from user actions.

```python
class BehavioralModel:
    def __init__(self):
        self.click_history = []
        self.purchase_history = []
        self.session_patterns = []
        self.feature_usage = Counter()
        self.time_patterns = defaultdict(list)
```

### Preference Models
Explicit and inferred likes/dislikes.

```python
class PreferenceModel:
    def __init__(self):
        self.explicit_ratings = {}  # Item -> rating
        self.implicit_preferences = {}  # Category -> score
        self.preference_vector = None  # Learned embedding
```

### Knowledge Models
What the user knows (for educational systems).

```python
class KnowledgeModel:
    def __init__(self):
        self.concepts = {}  # Concept -> mastery level
        self.skills = {}  # Skill -> proficiency
        self.misconceptions = set()
```

### Goal Models
What the user is trying to achieve.

```python
class GoalModel:
    def __init__(self):
        self.current_task = None
        self.session_goal = None
        self.long_term_goals = []
        self.constraints = []
```

## Building User Models

### Data Collection

#### Explicit Data
- Registration information
- Preference settings
- Ratings and reviews
- Survey responses

#### Implicit Data
- Browsing history
- Click patterns
- Time spent
- Search queries
- Purchase behavior

### Feature Engineering
```python
def extract_user_features(user_data):
    features = {}

    # Recency, Frequency, Monetary (RFM)
    features['recency'] = days_since_last_activity(user_data)
    features['frequency'] = activity_count(user_data, days=30)
    features['monetary'] = total_spend(user_data)

    # Engagement
    features['avg_session_length'] = mean(user_data.session_lengths)
    features['pages_per_session'] = mean(user_data.pages_per_session)

    # Preferences
    features['category_distribution'] = category_histogram(user_data)
    features['price_sensitivity'] = estimate_price_sensitivity(user_data)

    return features
```

### Model Learning

#### Explicit Models
```python
# Learn preference weights from ratings
def learn_preferences(ratings, item_features):
    X = np.array([item_features[item] for item, _ in ratings])
    y = np.array([rating for _, rating in ratings])

    model = LinearRegression()
    model.fit(X, y)

    return model.coef_  # Preference weights
```

#### Embedding Models
```python
# Learn user embedding from interactions
class UserEmbedding(nn.Module):
    def __init__(self, n_users, n_items, dim):
        self.user_embed = nn.Embedding(n_users, dim)
        self.item_embed = nn.Embedding(n_items, dim)

    def forward(self, user_id, item_id):
        user_vec = self.user_embed(user_id)
        item_vec = self.item_embed(item_id)
        return torch.dot(user_vec, item_vec)
```

## Model Maintenance

### Incremental Updates
```python
class IncrementalUserModel:
    def __init__(self, decay_rate=0.95):
        self.preferences = defaultdict(float)
        self.decay_rate = decay_rate

    def update(self, item, signal):
        # Decay old preferences
        for key in self.preferences:
            self.preferences[key] *= self.decay_rate

        # Add new signal
        for feature in item.features:
            self.preferences[feature] += signal
```

### Forgetting and Decay
```python
def apply_temporal_decay(model, current_time):
    for item, (score, timestamp) in model.items():
        age = current_time - timestamp
        decay_factor = np.exp(-age / half_life)
        model[item] = score * decay_factor
```

### Concept Drift
```python
class DriftDetector:
    def __init__(self, window_size=100):
        self.recent_behavior = deque(maxlen=window_size)
        self.baseline = None

    def detect_drift(self, new_behavior):
        self.recent_behavior.append(new_behavior)

        if self.baseline is None:
            self.baseline = self.compute_baseline()
            return False

        current = self.compute_current()
        drift_score = self.compare(self.baseline, current)

        if drift_score > threshold:
            self.baseline = current  # Reset baseline
            return True
        return False
```

## Privacy-Preserving User Modeling

### Data Minimization
```python
def minimal_user_model(full_data):
    # Keep only necessary features
    return {
        'preference_vector': compute_preferences(full_data),
        'segment': assign_segment(full_data),
        # Don't store raw behavior
    }
```

### Differential Privacy
```python
def private_preference_learning(ratings, epsilon):
    # Add noise to gradient updates
    sensitivity = compute_sensitivity()
    noise_scale = sensitivity / epsilon

    for epoch in range(epochs):
        gradient = compute_gradient(ratings)
        noisy_gradient = gradient + np.random.laplace(0, noise_scale)
        update_model(noisy_gradient)
```

### Federated User Models
```python
# On-device model training
class FederatedUserModel:
    def local_update(self, local_data):
        # Train on device
        gradient = compute_local_gradient(local_data)
        return gradient  # Send only gradient, not data

    def aggregate_updates(self, gradients):
        # Server aggregates without seeing data
        avg_gradient = np.mean(gradients, axis=0)
        self.global_model.apply_gradient(avg_gradient)
```

## Evaluation

### Model Accuracy
- Prediction error (RMSE, MAE)
- Classification accuracy
- Ranking metrics (NDCG, MRR)

### Model Coverage
- What fraction of users have models?
- How complete are individual models?

### Model Freshness
- How recent is the data?
- How quickly do models update?

## Exercises

1. Build demographic + behavioral hybrid model
2. Implement temporal decay for preferences
3. Create knowledge model for learning system
4. Add differential privacy to user model
5. Detect preference drift over time

## Key Insights

- **Multiple model types**: Combine demographic, behavioral, preference
- **Models decay**: User preferences change over time
- **Privacy matters**: Minimize data, add noise, federate
- **Evaluation is hard**: Accuracy isn't everything

---

**Status**: Foundation established
**Last Updated**: December 2025
**Maintainer**: GRID Foundations Team
