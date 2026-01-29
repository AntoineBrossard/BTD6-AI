# BTD6-AI: Artificial Intelligence for Bloons Tower Defense 6

An AI agent trained to play Bloons Tower Defense 6 through reinforcement learning. This project implements a complete 3-phase approach: (1) game simulation, (2) AI training, (3) real game integration.

## 🎯 Project Goals

Build an AI that can:
1. ✅ Master the simulated BTD6 mechanics
2. 🔄 Learn optimal tower placement strategies
3. 📋 Control the real BTD6 game autonomously

## 📁 Project Structure

```
BTD6-AI/
├── game/              # Phase 1: Game simulation engine
│   ├── entities.py    # Balloons, towers, projectiles
│   ├── game.py        # Core game logic
│   └── renderer.py    # Pygame visualization
├── ai/                # Phase 2: Reinforcement learning
│   ├── env.py         # Gymnasium environment wrapper
│   └── train.py       # PPO training pipeline
├── integration/       # Phase 3: Real game integration
│   └── btd6_integration.py  # Screen capture & control
├── docs/              # Phase documentation
└── tests/             # Various test scripts
```

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/BTD6-AI.git
cd BTD6-AI

# Install dependencies
pip install -r requirements.txt
```

### Test the Game Simulation

```bash
# Test basic mechanics
python test_simple.py

# Test with multiple towers (visual)
python test_full.py

# Test win condition
python test_win.py
```

### Train the AI

```bash
# Quick training test (10k steps, ~2 minutes)
python train_quick.py

# Full training (50k steps, ~15 minutes)
python ai/train.py

# Evaluate trained model
python ai/train.py eval models/btd6_ppo_final.zip
```

### Test with Real BTD6 Game (Phase 3)

```bash
# Interactive testing with your actual game
python test_real_game.py
```

**Setup:**
1. Open BTD6 and start a game on Monkey Meadow (Easy)
2. Run the test script
3. Follow the calibration prompts
4. Watch it place a test tower!

See [Testing Real Game Guide](docs/TESTING_REAL_GAME.md) for detailed instructions.

## 📊 Current Status

### Phase 1: Game Simulation ✅ COMPLETE
- ✅ Accurate balloon physics and pathfinding
- ✅ Tower targeting and firing mechanics
- ✅ Projectile collision detection
- ✅ Balloon splitting system
- ✅ Win/lose conditions
- ✅ Visual rendering with Pygame

**MVP Scope:**
- 1 tower type (Dart Monkey)
- 1 balloon type (RED)
- 1 round (6 balloons)
- No upgrades

### Phase 2: AI Training 🔄 IN PROGRESS
- ✅ Gymnasium environment wrapper
- ✅ PPO training pipeline
- ✅ Action space: 4801 discrete actions (grid-based placement)
- ✅ Observation space: 423-dimensional vector
- 🔄 Training in progress (10k timesteps completed)

**Performance:**
- Early training: Random placement
- Target: 90%+ win rate on Round 1

### Phase 3: Real Game Integration 📋 TODO
- ✅ Screen capture framework
- ✅ Basic balloon detection (color-based)
- ✅ Input automation (pyautogui)
- 📋 State converter (real game → AI observation)
- 📋 Full integration pipeline
- 📋 Testing on actual BTD6

## 🎮 How It Works

### Phase 1: Simulation
The game engine accurately recreates BTD6 mechanics:
- Balloons follow a precise path with waypoint tracking
- Towers detect balloons within range and fire projectiles
- Projectiles home in on targets and deal damage
- Balloons split into weaker types when hit

### Phase 2: AI Training
The AI learns through reinforcement learning:
1. **Observation**: Game state (balloon positions, tower locations, lives)
2. **Action**: Where to place the next tower (or do nothing)
3. **Reward**: +0.1 per survival, +1000 for win, -1000 for loss
4. **Algorithm**: PPO (Proximal Policy Optimization)

### Phase 3: Real Game Integration
The trained AI controls the real game:
1. **Screen Capture**: Grab BTD6 window
2. **Computer Vision**: Detect balloons, towers, UI
3. **State Conversion**: Transform to AI's expected format
4. **Action Execution**: Mouse clicks to place towers
5. **Loop**: Repeat at game speed

## 📖 Documentation

Detailed documentation for each phase:
- [Phase 1: Game Simulation](docs/PHASE1_GAME_SIMULATION.md)
- [Phase 2: AI Training](docs/PHASE2_AI_TRAINING.md)
- [Phase 3: BTD6 Integration](docs/PHASE3_INTEGRATION.md)
- [Testing with Real BTD6](docs/TESTING_REAL_GAME.md) ⭐ **Start here for real game testing!**
- [Architecture Overview](docs/ARCHITECTURE.md)

## 🧪 Testing

All core mechanics tested and verified:

```bash
# Individual component tests
python test_simple.py      # Basic game mechanics
python test_debug.py       # Tower targeting
python test_projectile.py  # Projectile lifecycle
python test_trace.py       # Collision detection
python test_full.py        # Multi-tower scenario
python test_win.py         # Win condition
python test_wave.py        # Wave completion

# Environment tests
python test_env.py         # Gymnasium environment
```

## 🛠️ Technical Stack

- **Game Engine**: Python, Pygame
- **AI Framework**: Stable Baselines3 (PPO), Gymnasium
- **Deep Learning**: PyTorch
- **Computer Vision**: OpenCV, PIL
- **Automation**: PyAutoGUI

## 📈 Future Enhancements

### Near-term
- [ ] Multiple tower types (Tack Shooter, Sniper, etc.)
- [ ] Multiple balloon types (Blue, Green, Yellow, etc.)
- [ ] Multiple rounds
- [ ] Tower upgrades
- [ ] Better reward shaping

### Long-term
- [ ] Full game integration with real BTD6
- [ ] Support for all towers and upgrades
- [ ] Multi-round strategies
- [ ] Different map layouts
- [ ] Multiplayer support

## ⚠️ Disclaimer

This project is for **educational and research purposes only**. Automated gameplay may violate the game's Terms of Service. Use responsibly and do not use for competitive advantage or online play.

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📧 Contact

Antoine Brossard - [GitHub](https://github.com/yourusername)

## 🙏 Acknowledgments

- Ninja Kiwi for creating Bloons Tower Defense 6
- Stable Baselines3 team for the RL framework
- OpenAI Gymnasium for the environment standard
