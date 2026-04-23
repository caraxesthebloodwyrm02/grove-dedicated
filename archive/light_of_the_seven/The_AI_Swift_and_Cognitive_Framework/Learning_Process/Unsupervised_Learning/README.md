# Unsupervised Learning

## Overview

Unsupervised learning finds patterns in data without labeled examples. It's used for clustering, dimensionality reduction, anomaly detection, and discovering hidden structure.

## Clustering

### K-Means
```python
from sklearn.cluster import KMeans

kmeans = KMeans(n_clusters=3, random_state=42)
clusters = kmeans.fit_predict(X)
centroids = kmeans.cluster_centers_
```

#### Choosing K
```python
# Elbow method
inertias = []
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(X)
    inertias.append(kmeans.inertia_)

# Silhouette score
from sklearn.metrics import silhouette_score
scores = []
for k in range(2, 11):
    kmeans = KMeans(n_clusters=k)
    labels = kmeans.fit_predict(X)
    scores.append(silhouette_score(X, labels))
```

### Hierarchical Clustering
```python
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram, linkage

# Agglomerative clustering
model = AgglomerativeClustering(n_clusters=3)
clusters = model.fit_predict(X)

# Dendrogram
Z = linkage(X, method='ward')
dendrogram(Z)
```

### DBSCAN
Density-based clustering, finds arbitrary shapes.

```python
from sklearn.cluster import DBSCAN

dbscan = DBSCAN(eps=0.5, min_samples=5)
clusters = dbscan.fit_predict(X)
# -1 indicates noise points
```

### Gaussian Mixture Models
Probabilistic clustering.

```python
from sklearn.mixture import GaussianMixture

gmm = GaussianMixture(n_components=3)
gmm.fit(X)
clusters = gmm.predict(X)
probabilities = gmm.predict_proba(X)
```

## Dimensionality Reduction

### Principal Component Analysis (PCA)
```python
from sklearn.decomposition import PCA

pca = PCA(n_components=2)
X_reduced = pca.fit_transform(X)

# Explained variance
print(pca.explained_variance_ratio_)
print(f"Total: {sum(pca.explained_variance_ratio_):.2%}")
```

### t-SNE
Non-linear dimensionality reduction for visualization.

```python
from sklearn.manifold import TSNE

tsne = TSNE(n_components=2, perplexity=30)
X_embedded = tsne.fit_transform(X)
```

### UMAP
Faster alternative to t-SNE.

```python
import umap

reducer = umap.UMAP(n_components=2)
X_embedded = reducer.fit_transform(X)
```

### Autoencoders
Neural network approach.

```python
import torch.nn as nn

class Autoencoder(nn.Module):
    def __init__(self, input_dim, latent_dim):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 128),
            nn.ReLU(),
            nn.Linear(128, latent_dim)
        )
        self.decoder = nn.Sequential(
            nn.Linear(latent_dim, 128),
            nn.ReLU(),
            nn.Linear(128, input_dim)
        )

    def forward(self, x):
        latent = self.encoder(x)
        reconstructed = self.decoder(latent)
        return reconstructed, latent
```

## Anomaly Detection

### Isolation Forest
```python
from sklearn.ensemble import IsolationForest

iso_forest = IsolationForest(contamination=0.1)
predictions = iso_forest.fit_predict(X)
# -1 for anomalies, 1 for normal
```

### One-Class SVM
```python
from sklearn.svm import OneClassSVM

ocsvm = OneClassSVM(nu=0.1)
predictions = ocsvm.fit_predict(X)
```

### Local Outlier Factor
```python
from sklearn.neighbors import LocalOutlierFactor

lof = LocalOutlierFactor(n_neighbors=20)
predictions = lof.fit_predict(X)
```

### Statistical Methods
```python
# Z-score
from scipy import stats
z_scores = stats.zscore(X)
anomalies = (np.abs(z_scores) > 3).any(axis=1)

# IQR method
Q1 = np.percentile(X, 25, axis=0)
Q3 = np.percentile(X, 75, axis=0)
IQR = Q3 - Q1
anomalies = ((X < Q1 - 1.5*IQR) | (X > Q3 + 1.5*IQR)).any(axis=1)
```

## Association Rules

### Apriori Algorithm
```python
from mlxtend.frequent_patterns import apriori, association_rules

# Find frequent itemsets
frequent_itemsets = apriori(df, min_support=0.05, use_colnames=True)

# Generate rules
rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1.0)
```

## Evaluation

### Clustering Metrics

#### Internal Metrics (no labels)
```python
from sklearn.metrics import silhouette_score, calinski_harabasz_score

silhouette = silhouette_score(X, labels)
calinski = calinski_harabasz_score(X, labels)
```

#### External Metrics (with labels)
```python
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score

ari = adjusted_rand_score(true_labels, predicted_labels)
nmi = normalized_mutual_info_score(true_labels, predicted_labels)
```

### Dimensionality Reduction Evaluation
- Reconstruction error
- Preserved variance
- Visualization quality
- Downstream task performance

## Exercises

1. Cluster customer data with K-means
2. Visualize high-dimensional data with t-SNE
3. Detect anomalies in time series
4. Find association rules in transaction data
5. Compare clustering algorithms on same dataset

## Key Insights

- **No ground truth**: Evaluation is harder than supervised
- **Preprocessing matters**: Scaling affects distance-based methods
- **Multiple algorithms**: Different methods find different patterns
- **Domain knowledge helps**: Interpret results with context

---

**Status**: Foundation established
**Last Updated**: December 2025
**Maintainer**: GRID Foundations Team
