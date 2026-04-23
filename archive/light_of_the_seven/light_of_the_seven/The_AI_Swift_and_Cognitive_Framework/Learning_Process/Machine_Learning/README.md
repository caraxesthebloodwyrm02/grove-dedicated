# Machine Learning

## Overview

Machine learning enables computers to learn from data without being explicitly programmed. This module covers fundamental concepts, algorithms, and practices that underpin all ML applications.

## Core Concepts

### The ML Pipeline
```
1. Problem Definition → What are we predicting?
2. Data Collection → Gather relevant data
3. Data Preparation → Clean, transform, split
4. Feature Engineering → Create informative features
5. Model Selection → Choose appropriate algorithm
6. Training → Fit model to data
7. Evaluation → Measure performance
8. Deployment → Put model into production
9. Monitoring → Track performance over time
```

### Types of Learning

| Type | Input | Output | Example |
|------|-------|--------|---------|
| Supervised | Labeled data | Predictions | Spam detection |
| Unsupervised | Unlabeled data | Patterns | Customer segmentation |
| Reinforcement | Environment | Actions | Game playing |
| Semi-supervised | Mixed labels | Predictions | Web content classification |

## Data Preparation

### Train/Validation/Test Split
```python
from sklearn.model_selection import train_test_split

# First split: separate test set
X_temp, X_test, y_temp, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Second split: separate validation set
X_train, X_val, y_train, y_val = train_test_split(
    X_temp, y_temp, test_size=0.25, random_state=42
)
# Result: 60% train, 20% val, 20% test
```

### Feature Scaling
```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler

# Standardization (mean=0, std=1)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_train)

# Normalization (0-1 range)
normalizer = MinMaxScaler()
X_normalized = normalizer.fit_transform(X_train)
```

### Handling Missing Data
```python
from sklearn.impute import SimpleImputer

# Mean imputation
imputer = SimpleImputer(strategy='mean')
X_imputed = imputer.fit_transform(X)

# More sophisticated: KNN imputation
from sklearn.impute import KNNImputer
knn_imputer = KNNImputer(n_neighbors=5)
```

## Model Evaluation

### Classification Metrics
```python
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

accuracy = accuracy_score(y_true, y_pred)
precision = precision_score(y_true, y_pred)
recall = recall_score(y_true, y_pred)
f1 = f1_score(y_true, y_pred)
```

### Regression Metrics
```python
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

mse = mean_squared_error(y_true, y_pred)
rmse = np.sqrt(mse)
mae = mean_absolute_error(y_true, y_pred)
r2 = r2_score(y_true, y_pred)
```

### Cross-Validation
```python
from sklearn.model_selection import cross_val_score

scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')
print(f"Mean: {scores.mean():.3f}, Std: {scores.std():.3f}")
```

## Common Algorithms

### Linear Models
- Linear Regression
- Logistic Regression
- Ridge/Lasso Regression

### Tree-Based
- Decision Trees
- Random Forest
- Gradient Boosting (XGBoost, LightGBM)

### Instance-Based
- K-Nearest Neighbors
- Support Vector Machines

### Ensemble Methods
- Bagging
- Boosting
- Stacking

## Hyperparameter Tuning

### Grid Search
```python
from sklearn.model_selection import GridSearchCV

param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [5, 10, 15],
    'min_samples_split': [2, 5, 10]
}

grid_search = GridSearchCV(
    RandomForestClassifier(),
    param_grid,
    cv=5,
    scoring='accuracy'
)
grid_search.fit(X_train, y_train)
best_params = grid_search.best_params_
```

### Random Search
```python
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import randint, uniform

param_dist = {
    'n_estimators': randint(100, 500),
    'max_depth': randint(5, 20),
    'min_samples_split': randint(2, 20)
}

random_search = RandomizedSearchCV(
    RandomForestClassifier(),
    param_dist,
    n_iter=50,
    cv=5
)
```

## Overfitting and Regularization

### Detecting Overfitting
```
Training accuracy: 99%
Validation accuracy: 75%
→ Large gap indicates overfitting
```

### Regularization Techniques
- L1 (Lasso): Sparse solutions
- L2 (Ridge): Small weights
- Dropout: Random neuron deactivation
- Early stopping: Stop before overfitting

## Feature Engineering

### Creating Features
```python
# Polynomial features
from sklearn.preprocessing import PolynomialFeatures
poly = PolynomialFeatures(degree=2)
X_poly = poly.fit_transform(X)

# Interaction features
df['feature_interaction'] = df['feature1'] * df['feature2']

# Binning
df['age_group'] = pd.cut(df['age'], bins=[0, 18, 35, 50, 100])
```

### Feature Selection
```python
from sklearn.feature_selection import SelectKBest, f_classif

selector = SelectKBest(f_classif, k=10)
X_selected = selector.fit_transform(X, y)
```

## Exercises

1. Build end-to-end ML pipeline for classification
2. Compare multiple algorithms on same dataset
3. Implement cross-validation from scratch
4. Tune hyperparameters with grid search
5. Analyze feature importance

## Key Insights

- **Data quality matters most**: Garbage in, garbage out
- **Simple models first**: Start simple, add complexity as needed
- **Validation is essential**: Always hold out test data
- **Feature engineering is powerful**: Often more impactful than algorithm choice

---

**Status**: Foundation established
**Last Updated**: December 2025
**Maintainer**: GRID Foundations Team
