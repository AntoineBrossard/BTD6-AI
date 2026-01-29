# Phase 3: BTD6 Integration - TODO 📋

## Overview
Connect the trained AI agent to the real Bloons Tower Defense 6 game through screen capture and input automation.

## Architecture

```
Real BTD6 Game
    ↓ (screen capture)
Screen Parser
    ↓ (game state)
State Converter
    ↓ (observation vector)
Trained AI Agent
    ↓ (action)
Action Executor
    ↓ (mouse/keyboard)
Real BTD6 Game
```

## Implementation

### Screen Capture (`integration/btd6_integration.py`)
- Uses `PIL.ImageGrab` for screen capture
- Configurable game window region
- Real-time frame capture

### Computer Vision
Detect game elements:
- **Balloons**: Color-based segmentation (HSV thresholds)
- **Towers**: Template matching
- **Lives**: OCR (Optical Character Recognition)
- **Round number**: OCR
- **Game state**: Screen pattern recognition

### Input Automation
- **pyautogui** for mouse/keyboard control
- Tower placement: Key press + click
- Start round: Space bar
- Failsafe: Move mouse to corner to abort

### State Conversion
Convert real game state to AI's expected observation format:
1. Detect balloons from screen → positions and types
2. Detect towers → positions
3. Read UI elements → lives, round, etc.
4. Normalize to match simulation observation space

## Challenges

### 1. Screen Detection Accuracy
**Problem**: Computer vision may miss or misidentify balloons
**Solution**: 
- Use multiple detection methods (color + shape + motion)
- Add confidence thresholds
- Implement error correction

### 2. Timing Issues
**Problem**: Real game runs at different speed than simulation
**Solution**:
- Add frame synchronization
- Adjust action timing
- Buffer observations

### 3. Observation Mismatch
**Problem**: Real game state may not match simulated observation format
**Solution**:
- Train AI with domain randomization
- Add observation normalization layer
- Fine-tune on real game data

### 4. Action Precision
**Problem**: Mouse clicks may not be pixel-perfect
**Solution**:
- Add click position calibration
- Use game's own UI when possible
- Implement retry logic

## Usage

### Basic Test
```python
from integration import BTD6Integration

integration = BTD6Integration(game_window_region=(0, 0, 800, 600))

# Capture screen
screen = integration.capture_screen()

# Detect balloons
balloons = integration.detect_balloons(screen)
print(f"Found {len(balloons)} balloons")

# Place tower
integration.place_tower("dart_monkey", x=200, y=300)

# Start round
integration.start_round()
```

### Full AI Integration
```python
from integration import BTD6Integration
from stable_baselines3 import PPO
import time

integration = BTD6Integration()
model = PPO.load("models/btd6_ppo_final.zip")

while True:
    # Capture and parse screen
    screen = integration.capture_screen()
    balloons = integration.detect_balloons(screen)
    towers = integration.detect_towers(screen)
    lives = integration.detect_lives(screen)
    
    # Convert to observation
    obs = integration.convert_to_observation(balloons, towers, lives)
    
    # Get AI action
    action, _ = model.predict(obs)
    
    # Execute action
    if action < 4800:  # Place tower
        x, y = integration.action_to_position(action)
        integration.place_tower("dart_monkey", x, y)
    
    time.sleep(0.1)  # Rate limit
    
    # Check game over
    if integration.is_game_over(screen):
        break
```

## TODO

### High Priority
- [ ] Implement robust balloon detection (multiple colors)
- [ ] Add tower detection (template matching)
- [ ] Implement OCR for lives/round
- [ ] Create observation converter
- [ ] Add action executor with timing
- [ ] Test on real BTD6 game

### Medium Priority
- [ ] Add game state detection (menu, playing, game over)
- [ ] Implement round start detection
- [ ] Add calibration tool for screen region
- [ ] Create debugging visualizer
- [ ] Add performance metrics

### Low Priority
- [ ] Support multiple resolutions
- [ ] Add support for different tower types
- [ ] Implement upgrade system integration
- [ ] Add multi-round support
- [ ] Create replay system

## Testing Strategy

1. **Unit Tests**: Test each component separately
   - Screen capture
   - Balloon detection
   - Input automation

2. **Integration Tests**: Test full pipeline
   - Capture → Detect → Convert → Act

3. **Live Tests**: Run against real game
   - Start with single tower placement
   - Progress to full round
   - Evaluate success rate

## Legal & Ethical Considerations

- This is for educational/research purposes only
- Automated gameplay may violate game's Terms of Service
- Use responsibly and at your own risk
- Do not use for competitive advantage or online play

## Next Steps

1. Complete balloon detection algorithm
2. Test screen capture on actual BTD6
3. Implement basic tower placement
4. Create observation converter
5. Test AI on real game with manual verification
