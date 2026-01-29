# Phase 2: AI Training - In Progress 🔄

## Overview
Train a reinforcement learning agent to play the simulated BTD6 game using PPO (Proximal Policy Optimization).

## Implementation

### Gymnasium Environment (`ai/env.py`)
Wraps the BTD6 game as a standard RL environment.

**Observation Space:**
- Flattened vector of size 423
- Contains:
  - Up to 100 balloons: position (x, y), health, type (4 values each)
  - Up to 10 towers: position (x, y) (2 values each)
  - Game info: lives, round, state (3 values)

**Action Space:**
- Discrete(4801)
- Grid-based tower placement (80x60 tiles) + "do nothing" action
- Each action maps to a position on the game map

**Rewards:**
- +0.1 per timestep survived
- -10 per life lost
- +1000 for winning
- -1000 for losing

### Training Script (`ai/train.py`)
Uses Stable Baselines3 PPO algorithm.

**Hyperparameters:**
- Learning rate: 3e-4
- Steps per update: 2048
- Batch size: 64
- Epochs: 10
- Gamma: 0.99
- GAE Lambda: 0.95
- Clip range: 0.2

**Training Command:**
```bash
python ai/train.py
# or for quick test:
python train_quick.py
```

**Evaluation:**
```bash
python ai/train.py eval models/btd6_ppo_final.zip
```

## Current Status

### Completed ✅
- Gymnasium environment wrapper
- Observation and action space definition
- Reward function
- PPO training pipeline
- Model checkpointing
- Evaluation script

### In Progress 🔄
- Training AI agent (10,000 timesteps test)
- Fine-tuning reward function
- Optimizing observation space

### TODO 📋
- [ ] Train for longer (50k-100k timesteps)
- [ ] Add curriculum learning (start easy, increase difficulty)
- [ ] Implement better reward shaping
- [ ] Add visual debugging for AI decisions
- [ ] Test against different scenarios

## Usage

### Train New Model
```python
from ai.train import train

train(
    total_timesteps=50000,
    model_name="my_btd6_agent",
    log_interval=10
)
```

### Evaluate Trained Model
```python
from ai.train import evaluate

evaluate(
    model_path="models/btd6_ppo_final.zip",
    episodes=10,
    render=True
)
```

### Use in Custom Code
```python
from ai.env import BTD6Env
from stable_baselines3 import PPO

env = BTD6Env()
model = PPO.load("models/btd6_ppo_final.zip")

obs, info = env.reset()
done = False

while not done:
    action, _ = model.predict(obs, deterministic=True)
    obs, reward, terminated, truncated, info = env.step(action)
    done = terminated or truncated
```

## Challenges

1. **Large Action Space**: 4801 possible actions makes exploration difficult
   - Solution: Consider reducing grid resolution or using continuous actions

2. **Sparse Rewards**: Agent only gets significant reward at end of episode
   - Solution: Add intermediate rewards (balloons popped, balloons in range, etc.)

3. **Long Episodes**: Each episode can be 1000 timesteps
   - Solution: Reduce max_steps or add time-based rewards

## Next Steps
See Phase 3: BTD6 Integration
