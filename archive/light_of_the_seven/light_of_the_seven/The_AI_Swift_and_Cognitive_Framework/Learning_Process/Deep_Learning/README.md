# Deep Learning

## Overview

Deep learning uses neural networks with multiple layers to learn hierarchical representations from data. It has achieved breakthrough results in vision, language, and many other domains.

## Neural Network Fundamentals

### Perceptron
```python
def perceptron(x, weights, bias):
    return activation(np.dot(weights, x) + bias)
```

### Multi-Layer Perceptron
```python
class MLP(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, output_dim)
        )

    def forward(self, x):
        return self.layers(x)
```

### Activation Functions
```python
# ReLU
relu = lambda x: max(0, x)

# Sigmoid
sigmoid = lambda x: 1 / (1 + np.exp(-x))

# Tanh
tanh = lambda x: np.tanh(x)

# Softmax
softmax = lambda x: np.exp(x) / np.sum(np.exp(x))
```

## Training

### Forward and Backward Pass
```python
# Forward pass
predictions = model(inputs)
loss = loss_function(predictions, targets)

# Backward pass
loss.backward()

# Update weights
optimizer.step()
optimizer.zero_grad()
```

### Loss Functions
```python
# Classification
cross_entropy = nn.CrossEntropyLoss()

# Regression
mse = nn.MSELoss()

# Binary classification
bce = nn.BCEWithLogitsLoss()
```

### Optimizers
```python
# SGD with momentum
optimizer = torch.optim.SGD(model.parameters(), lr=0.01, momentum=0.9)

# Adam
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# AdamW (with weight decay)
optimizer = torch.optim.AdamW(model.parameters(), lr=0.001, weight_decay=0.01)
```

## Convolutional Neural Networks (CNNs)

### Architecture
```python
class CNN(nn.Module):
    def __init__(self, num_classes):
        super().__init__()
        self.conv_layers = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.AdaptiveAvgPool2d(1)
        )
        self.fc = nn.Linear(128, num_classes)

    def forward(self, x):
        x = self.conv_layers(x)
        x = x.view(x.size(0), -1)
        return self.fc(x)
```

### Key Operations
- **Convolution**: Local feature extraction
- **Pooling**: Spatial downsampling
- **Batch Normalization**: Stabilize training

## Recurrent Neural Networks (RNNs)

### LSTM
```python
class LSTMModel(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim, num_layers):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.lstm = nn.LSTM(embed_dim, hidden_dim, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_dim, vocab_size)

    def forward(self, x, hidden=None):
        embed = self.embedding(x)
        output, hidden = self.lstm(embed, hidden)
        return self.fc(output), hidden
```

### GRU
```python
self.gru = nn.GRU(embed_dim, hidden_dim, num_layers, batch_first=True)
```

## Transformers

### Self-Attention
```python
class SelfAttention(nn.Module):
    def __init__(self, embed_dim, num_heads):
        super().__init__()
        self.attention = nn.MultiheadAttention(embed_dim, num_heads)

    def forward(self, x):
        attn_output, _ = self.attention(x, x, x)
        return attn_output
```

### Transformer Block
```python
class TransformerBlock(nn.Module):
    def __init__(self, embed_dim, num_heads, ff_dim, dropout=0.1):
        super().__init__()
        self.attention = nn.MultiheadAttention(embed_dim, num_heads)
        self.norm1 = nn.LayerNorm(embed_dim)
        self.norm2 = nn.LayerNorm(embed_dim)
        self.ff = nn.Sequential(
            nn.Linear(embed_dim, ff_dim),
            nn.GELU(),
            nn.Linear(ff_dim, embed_dim)
        )
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        # Self-attention with residual
        attn_out, _ = self.attention(x, x, x)
        x = self.norm1(x + self.dropout(attn_out))

        # Feed-forward with residual
        ff_out = self.ff(x)
        x = self.norm2(x + self.dropout(ff_out))

        return x
```

## Regularization

### Dropout
```python
self.dropout = nn.Dropout(p=0.5)
```

### Batch Normalization
```python
self.bn = nn.BatchNorm2d(num_features)
```

### Layer Normalization
```python
self.ln = nn.LayerNorm(embed_dim)
```

### Weight Decay
```python
optimizer = torch.optim.Adam(model.parameters(), weight_decay=1e-4)
```

## Training Techniques

### Learning Rate Scheduling
```python
# Step decay
scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=10, gamma=0.1)

# Cosine annealing
scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=100)

# Warmup
scheduler = torch.optim.lr_scheduler.LinearLR(optimizer, start_factor=0.1, total_iters=10)
```

### Data Augmentation
```python
transform = transforms.Compose([
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(10),
    transforms.ColorJitter(brightness=0.2, contrast=0.2),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])
```

### Mixed Precision Training
```python
scaler = torch.cuda.amp.GradScaler()

with torch.cuda.amp.autocast():
    output = model(input)
    loss = criterion(output, target)

scaler.scale(loss).backward()
scaler.step(optimizer)
scaler.update()
```

## Model Architectures

### Vision
- **ResNet**: Residual connections
- **EfficientNet**: Compound scaling
- **ViT**: Vision Transformer

### Language
- **BERT**: Bidirectional encoder
- **GPT**: Autoregressive decoder
- **T5**: Encoder-decoder

### Multimodal
- **CLIP**: Vision-language alignment
- **Stable Diffusion**: Text-to-image

## Exercises

1. Build and train CNN for image classification
2. Implement LSTM for sequence prediction
3. Create transformer from scratch
4. Apply transfer learning with pretrained model
5. Train with mixed precision

## Key Insights

- **Depth enables abstraction**: More layers learn higher-level features
- **Residual connections help**: Enable training very deep networks
- **Attention is powerful**: Transformers dominate many domains
- **Pretraining + finetuning**: Transfer learning is highly effective

---

**Status**: Foundation established
**Last Updated**: December 2025
**Maintainer**: GRID Foundations Team
