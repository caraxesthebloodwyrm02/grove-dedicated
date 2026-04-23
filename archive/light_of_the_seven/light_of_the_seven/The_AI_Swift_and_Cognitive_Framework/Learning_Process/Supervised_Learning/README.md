# Supervised Learning

## Overview

Supervised learning trains models on labeled data to predict outputs for new inputs. It's the most common ML paradigm, used for classification (discrete outputs) and regression (continuous outputs).

## Classification

### Binary Classification
Two classes: positive/negative, spam/not-spam, etc.

```python
from sklearn.linear_model import LogisticRegression

model = LogisticRegression()
model.fit(X_train, y_train)
predictions = model.predict(X_test)
probabilities = model.predict_proba(X_test)
```

### Multi-Class Classification
More than two classes.

```python
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)
predictions = model.predict(X_test)
```

### Multi-Label Classification
Multiple labels per instance.

```python
from sklearn.multioutput import MultiOutputClassifier

base_model = RandomForestClassifier()
model = MultiOutputClassifier(base_model)
model.fit(X_train, y_train)  # y_train has multiple columns
```

## Regression

### Linear Regression
```python
from sklearn.linear_model import LinearRegression

model = LinearRegression()
model.fit(X_train, y_train)
predictions = model.predict(X_test)
```

### Polynomial Regression
```python
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline

model = Pipeline([
    ('poly', PolynomialFeatures(degree=3)),
    ('linear', LinearRegression())
])
model.fit(X_train, y_train)
```

### Regularized Regression
```python
from sklearn.linear_model import Ridge, Lasso, ElasticNet

ridge = Ridge(alpha=1.0)  # L2 regularization
lasso = Lasso(alpha=0.1)  # L1 regularization
elastic = ElasticNet(alpha=0.1, l1_ratio=0.5)  # Both
```

## Common Algorithms

### Decision Trees
```python
from sklearn.tree import DecisionTreeClassifier

model = DecisionTreeClassifier(max_depth=5)
model.fit(X_train, y_train)

# Visualize
from sklearn.tree import plot_tree
plot_tree(model, feature_names=feature_names)
```

### Random Forest
```python
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    min_samples_split=5
)
model.fit(X_train, y_train)

# Feature importance
importances = model.feature_importances_
```

### Gradient Boosting
```python
from sklearn.ensemble import GradientBoostingClassifier
# Or use XGBoost/LightGBM for better performance

model = GradientBoostingClassifier(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=3
)
model.fit(X_train, y_train)
```

### Support Vector Machines
```python
from sklearn.svm import SVC

model = SVC(kernel='rbf', C=1.0, gamma='scale')
model.fit(X_train, y_train)
```

### K-Nearest Neighbors
```python
from sklearn.neighbors import KNeighborsClassifier

model = KNeighborsClassifier(n_neighbors=5)
model.fit(X_train, y_train)
```

## Evaluation Metrics

### Classification Metrics

#### Confusion Matrix
```python
from sklearn.metrics import confusion_matrix, classification_report

cm = confusion_matrix(y_true, y_pred)
print(classification_report(y_true, y_pred))
```

#### ROC and AUC
```python
from sklearn.metrics import roc_curve, auc

fpr, tpr, thresholds = roc_curve(y_true, y_scores)
roc_auc = auc(fpr, tpr)
```

### Regression Metrics
```python
from sklearn.metrics import mean_squared_error, r2_score

mse = mean_squared_error(y_true, y_pred)
r2 = r2_score(y_true, y_pred)
```

## Handling Imbalanced Data

### Resampling
```python
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler

# Oversampling minority class
smote = SMOTE()
X_resampled, y_resampled = smote.fit_resample(X, y)

# Undersampling majority class
rus = RandomUnderSampler()
X_resampled, y_resampled = rus.fit_resample(X, y)
```

### Class Weights
```python
model = RandomForestClassifier(class_weight='balanced')
# Or specify weights: class_weight={0: 1, 1: 10}
```

### Threshold Adjustment
```python
# Get probabilities
probs = model.predict_proba(X_test)[:, 1]

# Adjust threshold
threshold = 0.3  # Lower threshold for minority class
predictions = (probs >= threshold).astype(int)
```

## Model Interpretation

### Feature Importance
```python
# Tree-based models
importances = model.feature_importances_

# Permutation importance
from sklearn.inspection import permutation_importance
result = permutation_importance(model, X_test, y_test)
```

### SHAP Values
```python
import shap

explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)
shap.summary_plot(shap_values, X_test)
```

## Exercises

1. Build classifier for binary classification problem
2. Compare linear vs. tree-based models
3. Handle imbalanced dataset
4. Interpret model with SHAP values
5. Build regression model with regularization

## Key Insights

- **Choose metric carefully**: Accuracy isn't always best
- **Handle imbalance**: Real data is often imbalanced
- **Interpret models**: Understanding matters for trust
- **Ensemble methods often win**: Random Forest, XGBoost

---

**Status**: Foundation established
**Last Updated**: December 2025
**Maintainer**: GRID Foundations Team
