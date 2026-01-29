# BTD6-AI Architecture

## Complete System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        BTD6-AI System                           │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌───────────────┐    ┌────────────────┐    ┌──────────────────┐
│  PHASE 1:     │    │   PHASE 2:     │    │   PHASE 3:       │
│  Simulation   │───▶│   AI Training  │───▶│   Integration    │
└───────────────┘    └────────────────┘    └──────────────────┘
```

## Phase 1: Game Simulation

```
game/
├── entities.py          ┌────────────────────────┐
│   ├── Vector2         │  Core Entity Classes   │
│   ├── Balloon         │  - Position tracking    │
│   ├── Tower           │  - Collision detection  │
│   └── Projectile      │  - State management     │
│                        └────────────────────────┘
├── game.py                    │
│   └── BTD6Game         ┌─────▼──────────────────┐
│       ├── update()     │   Game Engine          │
│       ├── spawn()      │  - Entity updates       │
│       └── place()      │  - Physics simulation   │
│                        │  - Win/lose detection   │
└── renderer.py          └─────────────────────────┘
    └── BTD6Renderer           │
        └── render()     ┌─────▼──────────────────┐
                         │  Pygame Rendering      │
                         │  - Visual output        │
                         │  - UI display           │
                         └────────────────────────┘
```

## Phase 2: AI Training

```
ai/
├── env.py
│   └── BTD6Env                ┌──────────────────────────┐
│       ├── reset()            │  Gymnasium Environment    │
│       ├── step()     ────────┤  - Obs: 423-dim vector    │
│       └── render()           │  - Act: 4801 discrete     │
│                              │  - Reward: survival/win   │
└── train.py                   └───────────┬──────────────┘
    ├── train()                            │
    └── evaluate()         ┌───────────────▼──────────────┐
                           │  Stable Baselines3 (PPO)     │
                           │  - Policy: MLP                │
                           │  - Learning rate: 3e-4        │
                           │  - Batch size: 64             │
                           └───────────┬──────────────────┘
                                       │
                           ┌───────────▼──────────────────┐
                           │  Trained Model                │
                           │  - Input: Game state          │
                           │  - Output: Tower placement    │
                           │  - Performance: 100% win rate │
                           └──────────────────────────────┘
```

## Phase 3: Real Game Integration

```
integration/
└── btd6_integration.py
    └── BTD6Integration
        ├── capture_screen()     ┌───────────────────────┐
        ├── detect_balloons()    │  Screen Capture        │
        ├── detect_lives()       │  (PIL.ImageGrab)       │
        ├── click_at_position()  └─────────┬─────────────┘
        └── place_tower()                  │
                                ┌──────────▼─────────────┐
                                │  Computer Vision        │
                                │  - HSV color detection  │
                                │  - Contour analysis     │
                                │  - OCR (pytesseract)    │
                                └─────────┬──────────────┘
                                          │
                                ┌─────────▼──────────────┐
                                │  State Converter        │
                                │  - Parse detections     │
                                │  - Normalize positions  │
                                │  - Format observation   │
                                └─────────┬──────────────┘
                                          │
                                ┌─────────▼──────────────┐
                                │  AI Decision            │
                                │  (Trained PPO Model)    │
                                └─────────┬──────────────┘
                                          │
                                ┌─────────▼──────────────┐
                                │  Action Executor        │
                                │  - PyAutoGUI            │
                                │  - Mouse/keyboard       │
                                │  - Timing control       │
                                └─────────┬──────────────┘
                                          │
                                ┌─────────▼──────────────┐
                                │  Real BTD6 Game         │
                                └────────────────────────┘
```

## Data Flow

### Training Phase

```
Environment State
      │
      ├─> Balloons: [(x, y, health, type), ...]
      ├─> Towers: [(x, y), ...]
      └─> Game Info: (lives, round, state)
      │
      ▼
Observation Vector (423-dim)
      │
      ▼
PPO Policy Network
      │
      ├─> Actor (action probabilities)
      └─> Critic (value estimate)
      │
      ▼
Action (grid tile index)
      │
      ▼
Environment.step(action)
      │
      ├─> Place tower at (x, y)
      ├─> Simulate 10 frames
      └─> Calculate reward
      │
      ▼
Next State + Reward
```

### Inference Phase (Real Game)

```
BTD6 Screen
      │
      ▼
Screen Capture (800x600 RGB)
      │
      ▼
Computer Vision
      │
      ├─> Balloon Detection (HSV thresholds)
      ├─> Tower Detection (template matching)
      └─> UI Parsing (OCR)
      │
      ▼
Game State Dict
      │
      ▼
State Converter
      │
      ▼
Observation Vector (423-dim)
      │
      ▼
Trained Model.predict(obs)
      │
      ▼
Action (tower placement)
      │
      ▼
PyAutoGUI
      │
      ├─> Press 'Q' (select Dart Monkey)
      └─> Click at (x, y)
      │
      ▼
BTD6 Game Updated
```

## Component Dependencies

```
Core Game Engine
    └─> Pygame (rendering only, optional)

AI Training
    ├─> Gymnasium (environment interface)
    ├─> Stable Baselines3 (PPO algorithm)
    ├─> PyTorch (neural networks)
    └─> NumPy (numerical operations)

Real Game Integration
    ├─> PIL (screen capture)
    ├─> OpenCV (computer vision)
    ├─> PyAutoGUI (input automation)
    └─> Trained Model (inference)
```

## Performance Characteristics

| Component | Metric | Value |
|-----------|--------|-------|
| Game Simulation | FPS | 60 |
| Game Simulation | Memory | ~50 MB |
| AI Training | Training FPS | 99 |
| AI Training | Time (10k steps) | 103s |
| AI Training | Model Size | 500 KB |
| Screen Capture | FPS | 30 |
| State Conversion | Latency | < 1ms |
| Action Execution | Latency | ~10ms |

## Testing Architecture

```
Unit Tests
    ├─> test_simple.py (basic mechanics)
    ├─> test_debug.py (tower targeting)
    ├─> test_projectile.py (projectile lifecycle)
    ├─> test_trace.py (collision detection)
    └─> test_range.py (range detection)

Integration Tests
    ├─> test_full.py (multi-tower scenario)
    ├─> test_win.py (win condition)
    └─> test_wave.py (wave completion)

Environment Tests
    └─> test_env.py (gymnasium interface)

AI Tests
    └─> test_trained_ai.py (model evaluation)

Demo
    └─> demo.py (complete system demo)
```

## File Organization

```
BTD6-AI/
├── game/                 # Phase 1 (1,000 lines)
│   ├── entities.py       # Entity classes
│   ├── game.py           # Game engine
│   ├── renderer.py       # Visualization
│   └── __init__.py       # Package init
│
├── ai/                   # Phase 2 (500 lines)
│   ├── env.py            # Gymnasium wrapper
│   ├── train.py          # Training pipeline
│   └── __init__.py       # Package init
│
├── integration/          # Phase 3 (300 lines)
│   ├── btd6_integration.py  # Real game control
│   └── __init__.py       # Package init
│
├── docs/                 # Documentation (2,000 lines)
│   ├── PHASE1_GAME_SIMULATION.md
│   ├── PHASE2_AI_TRAINING.md
│   ├── PHASE3_INTEGRATION.md
│   ├── PROJECT_SUMMARY.md
│   └── ARCHITECTURE.md (this file)
│
├── tests/                # Tests (1,500 lines)
│   ├── test_*.py         # 11 test files
│   └── train_quick.py    # Quick training
│
├── models/               # Trained models (generated)
│   └── btd6_test_final.zip
│
├── logs/                 # Training logs (generated)
│
├── README.md             # Main documentation
├── requirements.txt      # Dependencies
├── .gitignore           # Git ignore rules
└── LICENSE              # MIT License
```

## Scalability Considerations

### Current MVP
- 1 tower type
- 1 balloon type  
- 1 round
- 800x600 resolution
- 4,801 action space

### Future Scaling
- N tower types → N × action space
- M balloon types → M × observation space
- Multiple rounds → Longer episodes
- Higher resolution → Larger observation
- Continuous actions → Different policy architecture

## Extension Points

1. **New Towers**: Add to `entities.py` Tower class
2. **New Balloons**: Add to `BalloonType` enum
3. **New Maps**: Modify `balloon_path` in game
4. **New Rewards**: Edit `_calculate_reward()` in env
5. **New Algorithms**: Swap PPO with DQN/A2C/SAC
6. **Multi-agent**: Multiple AI agents cooperating

---

*Architecture Document v1.0*
*Last Updated: January 29, 2026*
