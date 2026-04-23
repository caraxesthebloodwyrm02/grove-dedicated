# Context-Aware Systems

## Overview

Context-aware systems sense and respond to the user's environment, situation, and state. They use contextual information to provide more relevant and timely services without explicit user input.

## Types of Context

### User Context
- **Identity**: Who is the user?
- **Preferences**: What do they like?
- **History**: What have they done?
- **Goals**: What are they trying to achieve?

### Environmental Context
- **Location**: Where are they?
- **Time**: When is it?
- **Weather**: What are conditions?
- **Nearby**: What's around them?

### Device Context
- **Capabilities**: What can the device do?
- **Resources**: Battery, connectivity, storage
- **Sensors**: Available inputs
- **Display**: Screen size, orientation

### Social Context
- **Companions**: Who are they with?
- **Activity**: What are they doing?
- **Relationships**: Social connections
- **Norms**: Cultural/social expectations

## Context Acquisition

### Sensors
```python
class ContextSensors:
    def get_location(self):
        return gps.get_coordinates()

    def get_activity(self):
        return accelerometer.classify_motion()

    def get_ambient(self):
        return {
            'light': light_sensor.read(),
            'noise': microphone.get_db_level(),
            'temperature': thermometer.read()
        }
```

### Inference
```python
def infer_context(raw_signals):
    # Combine signals to infer higher-level context
    if is_moving(accelerometer) and is_outdoors(light):
        activity = "commuting"
    elif is_stationary(accelerometer) and is_quiet(microphone):
        activity = "working"
    return activity
```

### User Input
- Explicit declarations
- Calendar events
- Social check-ins
- Manual overrides

## Context Modeling

### Feature Representation
```python
context_vector = {
    'time_of_day': encode_time(now()),
    'day_of_week': encode_day(today()),
    'location_type': classify_location(coords),
    'activity': current_activity,
    'device_state': get_device_state(),
    'social_context': detect_social_situation()
}
```

### Context History
```python
class ContextHistory:
    def __init__(self, window_size=100):
        self.history = deque(maxlen=window_size)

    def add(self, context, timestamp):
        self.history.append((context, timestamp))

    def get_pattern(self, time_range):
        relevant = [c for c, t in self.history
                    if t in time_range]
        return aggregate(relevant)
```

### Probabilistic Models
```python
# Hidden Markov Model for context
class ContextHMM:
    def __init__(self, states, observations):
        self.transition = init_transition_matrix(states)
        self.emission = init_emission_matrix(states, observations)

    def predict_context(self, observations):
        return viterbi(observations, self.transition, self.emission)
```

## Context-Aware Adaptation

### Rule-Based
```python
adaptation_rules = {
    ('meeting', 'work'): {'notifications': 'silent', 'display': 'dim'},
    ('driving', 'car'): {'interface': 'voice', 'notifications': 'urgent_only'},
    ('home', 'evening'): {'mode': 'relaxed', 'suggestions': 'entertainment'},
}

def adapt(context):
    key = (context.activity, context.location_type)
    if key in adaptation_rules:
        apply_settings(adaptation_rules[key])
```

### Learning-Based
```python
class ContextualPredictor:
    def __init__(self):
        self.model = train_context_model()

    def predict_action(self, context):
        return self.model.predict(context.to_vector())

    def update(self, context, action, reward):
        self.model.partial_fit(context.to_vector(), action, reward)
```

## Applications

### Smart Notifications
```python
def should_notify(notification, context):
    urgency = notification.priority
    interruptibility = estimate_interruptibility(context)

    if urgency > interruptibility:
        return True
    else:
        queue_for_later(notification)
        return False
```

### Adaptive Interfaces
```python
def adapt_interface(context):
    if context.ambient_light < threshold:
        enable_dark_mode()

    if context.is_moving:
        increase_button_size()
        simplify_layout()

    if context.noise_level > threshold:
        enable_haptic_feedback()
```

### Location-Based Services
```python
def location_trigger(user, location):
    if is_near(location, user.home):
        suggest_home_automation()
    elif is_near(location, user.work):
        show_work_dashboard()
    elif is_retail_location(location):
        show_relevant_offers()
```

## Privacy and Ethics

### Transparency
- Show what context is being collected
- Explain how it's being used
- Allow users to view their data

### Control
- Granular permissions
- Easy opt-out
- Manual override options

### Data Protection
- Minimize collection
- Local processing when possible
- Secure transmission and storage

## Challenges

### Uncertainty
Context inference is probabilistic; handle errors gracefully.

### Battery/Resources
Continuous sensing drains resources; balance accuracy vs. efficiency.

### Privacy
Rich context data is sensitive; protect user information.

### Complexity
Many context dimensions; avoid overwhelming users with adaptations.

## Exercises

1. Build a simple activity recognizer from accelerometer data
2. Design context-aware notification system
3. Implement location-based triggers
4. Create adaptive UI based on ambient conditions
5. Add privacy controls to context collection

## Key Insights

- **Context enriches interaction**: More relevant without explicit input
- **Inference is imperfect**: Design for uncertainty
- **Privacy is paramount**: Context data is sensitive
- **Less can be more**: Don't over-adapt

---

**Status**: Foundation established
**Last Updated**: December 2025
**Maintainer**: GRID Foundations Team
