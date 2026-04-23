# Reinforcement Learning

## Overview

Reinforcement learning (RL) trains agents to make decisions by interacting with an environment. The agent learns to maximize cumulative reward through trial and error.

## Core Concepts

### The RL Framework
```
Agent ←→ Environment

Agent observes state s
Agent takes action a
Environment returns reward r and next state s'
Agent updates policy
Repeat
```

### Key Components
- **State (s)**: Current situation
- **Action (a)**: What agent can do
- **Reward (r)**: Feedback signal
- **Policy (π)**: Strategy for choosing actions
- **Value function (V)**: Expected future reward

### Markov Decision Process (MDP)
```
MDP = (S, A, P, R, γ)
- S: State space
- A: Action space
- P: Transition probabilities P(s'|s,a)
- R: Reward function R(s,a,s')
- γ: Discount factor (0 < γ ≤ 1)
```

## Value-Based Methods

### Q-Learning
Learn action-value function Q(s,a).

```python
def q_learning(env, episodes, alpha=0.1, gamma=0.99, epsilon=0.1):
    Q = defaultdict(lambda: np.zeros(env.action_space.n))

    for episode in range(episodes):
        state = env.reset()
        done = False

        while not done:
            # Epsilon-greedy action selection
            if random.random() < epsilon:
                action = env.action_space.sample()
            else:
                action = np.argmax(Q[state])

            next_state, reward, done, _ = env.step(action)

            # Q-learning update
            best_next = np.max(Q[next_state])
            Q[state][action] += alpha * (
                reward + gamma * best_next - Q[state][action]
            )

            state = next_state

    return Q
```

### Deep Q-Network (DQN)
Neural network approximates Q-function.

```python
class DQN(nn.Module):
    def __init__(self, state_dim, action_dim):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(state_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.ReLU(),
            nn.Linear(128, action_dim)
        )

    def forward(self, state):
        return self.network(state)

# Experience replay buffer
class ReplayBuffer:
    def __init__(self, capacity):
        self.buffer = deque(maxlen=capacity)

    def push(self, state, action, reward, next_state, done):
        self.buffer.append((state, action, reward, next_state, done))

    def sample(self, batch_size):
        return random.sample(self.buffer, batch_size)
```

## Policy-Based Methods

### REINFORCE
Direct policy gradient.

```python
class PolicyNetwork(nn.Module):
    def __init__(self, state_dim, action_dim):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(state_dim, 128),
            nn.ReLU(),
            nn.Linear(128, action_dim),
            nn.Softmax(dim=-1)
        )

    def forward(self, state):
        return self.network(state)

def reinforce(env, policy, optimizer, episodes, gamma=0.99):
    for episode in range(episodes):
        states, actions, rewards = [], [], []
        state = env.reset()
        done = False

        while not done:
            probs = policy(torch.FloatTensor(state))
            action = torch.multinomial(probs, 1).item()
            next_state, reward, done, _ = env.step(action)

            states.append(state)
            actions.append(action)
            rewards.append(reward)
            state = next_state

        # Compute returns
        returns = []
        G = 0
        for r in reversed(rewards):
            G = r + gamma * G
            returns.insert(0, G)
        returns = torch.FloatTensor(returns)
        returns = (returns - returns.mean()) / (returns.std() + 1e-8)

        # Policy gradient update
        optimizer.zero_grad()
        for state, action, G in zip(states, actions, returns):
            probs = policy(torch.FloatTensor(state))
            loss = -torch.log(probs[action]) * G
            loss.backward()
        optimizer.step()
```

## Actor-Critic Methods

### A2C (Advantage Actor-Critic)
```python
class ActorCritic(nn.Module):
    def __init__(self, state_dim, action_dim):
        super().__init__()
        self.shared = nn.Sequential(
            nn.Linear(state_dim, 128),
            nn.ReLU()
        )
        self.actor = nn.Linear(128, action_dim)
        self.critic = nn.Linear(128, 1)

    def forward(self, state):
        shared = self.shared(state)
        policy = F.softmax(self.actor(shared), dim=-1)
        value = self.critic(shared)
        return policy, value
```

### PPO (Proximal Policy Optimization)
Stable policy updates with clipping.

```python
def ppo_update(policy, old_policy, states, actions, returns, advantages,
               epsilon=0.2, epochs=10):
    for _ in range(epochs):
        probs = policy(states)
        old_probs = old_policy(states).detach()

        ratio = probs[range(len(actions)), actions] / \
                old_probs[range(len(actions)), actions]

        # Clipped objective
        surr1 = ratio * advantages
        surr2 = torch.clamp(ratio, 1-epsilon, 1+epsilon) * advantages
        policy_loss = -torch.min(surr1, surr2).mean()

        # Update
        optimizer.zero_grad()
        policy_loss.backward()
        optimizer.step()
```

## Exploration Strategies

### Epsilon-Greedy
```python
def epsilon_greedy(Q, state, epsilon):
    if random.random() < epsilon:
        return random.choice(actions)
    return np.argmax(Q[state])
```

### Boltzmann (Softmax)
```python
def boltzmann(Q, state, temperature):
    q_values = Q[state]
    probs = np.exp(q_values / temperature)
    probs /= probs.sum()
    return np.random.choice(actions, p=probs)
```

### UCB (Upper Confidence Bound)
```python
def ucb(Q, N, state, c=2):
    ucb_values = Q[state] + c * np.sqrt(np.log(sum(N[state])) / (N[state] + 1e-8))
    return np.argmax(ucb_values)
```

## Applications

### Game Playing
- Atari games (DQN)
- Go (AlphaGo)
- Chess (AlphaZero)

### Robotics
- Manipulation
- Locomotion
- Navigation

### Resource Management
- Data center cooling
- Traffic control
- Portfolio optimization

### Hardware Design (NAS)
```python
# Neural Architecture Search with RL
def hardware_aware_nas(search_space, target_latency):
    agent = PolicyNetwork(state_dim, action_dim)

    for episode in range(episodes):
        # Sample architecture
        architecture = agent.sample_architecture()

        # Evaluate
        accuracy = train_and_evaluate(architecture)
        latency = measure_latency(architecture)

        # Reward: accuracy with latency penalty
        reward = accuracy - lambda * max(0, latency - target_latency)

        # Update policy
        agent.update(reward)
```

## Exercises

1. Implement Q-learning for GridWorld
2. Train DQN on CartPole
3. Implement REINFORCE algorithm
4. Compare exploration strategies
5. Apply RL to simple optimization problem

## Key Insights

- **Exploration vs. exploitation**: Balance is crucial
- **Reward design matters**: Shapes learned behavior
- **Sample efficiency**: RL often needs many interactions
- **Stability challenges**: Training can be unstable

---

**Status**: Foundation established
**Last Updated**: December 2025
**Maintainer**: GRID Foundations Team
