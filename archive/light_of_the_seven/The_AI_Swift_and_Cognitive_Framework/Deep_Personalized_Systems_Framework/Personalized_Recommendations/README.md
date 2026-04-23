# Personalized Recommendations

## Overview

Recommendation systems predict user preferences and suggest relevant items. They power content discovery across e-commerce, streaming, social media, and many other domains.

## Recommendation Approaches

### 1. Collaborative Filtering
Find similar users or items based on behavior patterns.

#### User-Based CF
"Users who liked what you liked also liked..."

```python
def user_based_cf(target_user, all_users, items):
    similarities = {}
    for user in all_users:
        if user != target_user:
            similarities[user] = cosine_similarity(
                target_user.ratings, user.ratings
            )

    similar_users = top_k(similarities, k=50)

    recommendations = {}
    for item in items:
        if item not in target_user.rated:
            score = weighted_average(
                [u.ratings[item] for u in similar_users if item in u.rated],
                [similarities[u] for u in similar_users if item in u.rated]
            )
            recommendations[item] = score

    return top_k(recommendations, k=10)
```

#### Item-Based CF
"Items similar to what you liked..."

```python
def item_based_cf(target_user, item_similarities):
    recommendations = {}

    for candidate_item in all_items:
        if candidate_item not in target_user.rated:
            score = 0
            for rated_item, rating in target_user.ratings.items():
                similarity = item_similarities[rated_item][candidate_item]
                score += similarity * rating
            recommendations[candidate_item] = score

    return top_k(recommendations, k=10)
```

### 2. Content-Based Filtering
Recommend items similar to what user liked based on item features.

```python
def content_based(user_profile, items):
    recommendations = {}

    for item in items:
        if item not in user_profile.seen:
            similarity = cosine_similarity(
                user_profile.preference_vector,
                item.feature_vector
            )
            recommendations[item] = similarity

    return top_k(recommendations, k=10)
```

### 3. Matrix Factorization
Learn latent factors for users and items.

```python
# Simplified SVD-based approach
def matrix_factorization(ratings_matrix, k_factors=50):
    U, sigma, Vt = svd(ratings_matrix, k=k_factors)

    user_factors = U @ np.diag(np.sqrt(sigma))
    item_factors = np.diag(np.sqrt(sigma)) @ Vt

    predicted_ratings = user_factors @ item_factors
    return predicted_ratings
```

### 4. Deep Learning Approaches

#### Neural Collaborative Filtering
```python
class NCF(nn.Module):
    def __init__(self, n_users, n_items, embedding_dim):
        self.user_embedding = nn.Embedding(n_users, embedding_dim)
        self.item_embedding = nn.Embedding(n_items, embedding_dim)
        self.mlp = nn.Sequential(
            nn.Linear(embedding_dim * 2, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 1)
        )

    def forward(self, user_id, item_id):
        user_vec = self.user_embedding(user_id)
        item_vec = self.item_embedding(item_id)
        concat = torch.cat([user_vec, item_vec], dim=1)
        return self.mlp(concat)
```

### 5. Hybrid Systems
Combine multiple approaches.

```python
def hybrid_recommendation(user, items):
    cf_scores = collaborative_filtering(user, items)
    cb_scores = content_based(user, items)
    popularity_scores = get_popularity(items)

    final_scores = {}
    for item in items:
        final_scores[item] = (
            0.5 * cf_scores.get(item, 0) +
            0.3 * cb_scores.get(item, 0) +
            0.2 * popularity_scores.get(item, 0)
        )

    return top_k(final_scores, k=10)
```

## Handling Challenges

### Cold Start

#### New Users
```python
def new_user_recommendations(user_demographics):
    # Use demographics to find similar users
    similar_users = find_demographic_matches(user_demographics)

    # Recommend popular items among similar users
    return popular_among(similar_users)
```

#### New Items
```python
def new_item_promotion(item):
    # Use content features to find similar items
    similar_items = find_content_similar(item)

    # Recommend to users who liked similar items
    target_users = users_who_liked(similar_items)
    return target_users
```

### Diversity and Serendipity
```python
def diversify_recommendations(recommendations, diversity_weight=0.3):
    diverse_list = [recommendations[0]]

    for item in recommendations[1:]:
        diversity_score = min_distance(item, diverse_list)
        relevance_score = item.score

        combined = (1 - diversity_weight) * relevance_score + \
                   diversity_weight * diversity_score

        if combined > threshold:
            diverse_list.append(item)

    return diverse_list
```

### Filter Bubbles
```python
def break_filter_bubble(recommendations, exploration_rate=0.1):
    n_explore = int(len(recommendations) * exploration_rate)

    # Replace some recommendations with diverse options
    explore_items = sample_from_different_categories(
        exclude=user.history,
        n=n_explore
    )

    return recommendations[:-n_explore] + explore_items
```

## Evaluation Metrics

### Accuracy Metrics
```python
def precision_at_k(recommended, relevant, k):
    recommended_k = recommended[:k]
    hits = len(set(recommended_k) & set(relevant))
    return hits / k

def recall_at_k(recommended, relevant, k):
    recommended_k = recommended[:k]
    hits = len(set(recommended_k) & set(relevant))
    return hits / len(relevant)

def ndcg_at_k(recommended, relevant, k):
    dcg = sum(1 / np.log2(i + 2)
              for i, item in enumerate(recommended[:k])
              if item in relevant)
    idcg = sum(1 / np.log2(i + 2)
               for i in range(min(k, len(relevant))))
    return dcg / idcg if idcg > 0 else 0
```

### Beyond Accuracy
- **Diversity**: How different are recommendations?
- **Novelty**: How unknown are recommended items?
- **Serendipity**: How surprising yet relevant?
- **Coverage**: What fraction of items get recommended?

## Real-Time Recommendations

### Two-Stage Architecture
```
Stage 1: Candidate Generation (fast, broad)
    - Retrieve 1000s of candidates
    - Use simple models (ANN, hashing)

Stage 2: Ranking (slower, precise)
    - Score candidates with complex model
    - Return top-k
```

### Caching and Precomputation
```python
class RecommendationCache:
    def __init__(self, ttl=3600):
        self.cache = {}
        self.ttl = ttl

    def get(self, user_id):
        if user_id in self.cache:
            recs, timestamp = self.cache[user_id]
            if time.time() - timestamp < self.ttl:
                return recs
        return None

    def set(self, user_id, recommendations):
        self.cache[user_id] = (recommendations, time.time())
```

## Exercises

1. Implement user-based collaborative filtering
2. Build content-based recommender for articles
3. Create hybrid system combining CF and CB
4. Add diversity to recommendation list
5. Evaluate recommender with precision@k and NDCG

## Key Insights

- **No single best approach**: Hybrid systems often win
- **Cold start is hard**: Plan for new users and items
- **Diversity matters**: Don't just optimize accuracy
- **Scale requires architecture**: Two-stage, caching, precomputation

---

**Status**: Foundation established
**Last Updated**: December 2025
**Maintainer**: GRID Foundations Team
