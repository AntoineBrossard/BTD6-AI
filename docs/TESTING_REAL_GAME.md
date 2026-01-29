# Testing with Real BTD6 Game

## Quick Start

### Step 1: Prepare BTD6
1. Launch Bloons Tower Defense 6
2. Start a new game on **Monkey Meadow** (easiest map)
3. Set difficulty to **Easy**
4. Keep the game window **fully visible** (don't minimize)
5. Stay at the starting screen (don't start the round)

### Step 2: Run Calibration Test
```bash
python test_real_game.py
```

This script will:
1. Ask you to position your mouse to calibrate the game region
2. Capture a screenshot and save it
3. Test balloon detection
4. Test tower placement (places ONE Dart Monkey)

### Step 3: Check Results
- `btd6_capture.png` - Your captured screen (verify it looks correct)
- Tower placement - Check if a Dart Monkey appeared in your game

## Important Notes

### Current Limitations
The AI was trained on our **simplified simulation**, not real BTD6. To fully work with the real game, you need:

1. **Better Detection** ✅ Framework ready, needs tuning
   - Currently detects red balloons only
   - Need to add detection for all balloon colors
   
2. **State Conversion** 📋 Not yet implemented
   - Real game state → AI observation format
   - Need to match the 423-dimensional vector

3. **UI Parsing** 📋 Not yet implemented
   - Lives counter (OCR)
   - Money counter (OCR)
   - Round number

4. **Fine-tuning** 📋 Needed
   - Click timing adjustments
   - Hotkey mapping for your BTD6 version
   - Resolution/scaling handling

### What Works Now
✅ Screen capture from any window region
✅ Mouse/keyboard control (pyautogui)
✅ Basic red balloon detection (HSV color filtering)
✅ Tower placement commands

### What Needs Work
🔄 Detect all balloon types (blue, green, yellow, etc.)
🔄 Parse game UI elements
🔄 Convert real game state to AI format
🔄 Handle different resolutions
🔄 Real-time performance optimization

## Manual Testing Steps

### 1. Screen Capture Only
```python
from integration import BTD6Integration

# Create integration with your game window coordinates
integration = BTD6Integration(game_window_region=(100, 100, 800, 600))

# Capture and save
screen = integration.capture_screen()

import cv2
cv2.imwrite("test_capture.png", screen)
print("Check test_capture.png to verify capture")
```

### 2. Balloon Detection Test
```python
from integration import BTD6Integration
import cv2

integration = BTD6Integration()

# Start a round in BTD6, then:
screen = integration.capture_screen()
balloons = integration.detect_balloons(screen)

print(f"Detected {len(balloons)} balloons:")
for b in balloons:
    print(f"  - Position: ({b['x']}, {b['y']}), Type: {b['type']}")
```

### 3. Tower Placement Test
```python
from integration import BTD6Integration
import time

integration = BTD6Integration(game_window_region=(100, 100, 800, 600))

# Wait for you to focus BTD6 window
time.sleep(3)

# Place tower at center
integration.place_tower("dart_monkey", 400, 300)
```

## Common Issues & Solutions

### Issue: Screen capture is black/wrong area
**Solution**: Recalibrate your game window region. Run `test_real_game.py` again and carefully position your mouse.

### Issue: Tower won't place
**Solutions**:
- Check if 'Q' is the correct hotkey for Dart Monkey in your BTD6 version
- Ensure game window has focus
- Check if you have enough money ($170 for Dart Monkey)
- Verify click coordinates are within the playable area

### Issue: Balloon detection finds nothing
**Solutions**:
- Start a round so balloons appear
- Check `btd6_capture.png` - are balloons visible?
- Red balloons work best (adjust HSV thresholds in `btd6_integration.py` for others)

### Issue: Controls too fast/slow
**Solution**: Adjust `pyautogui.PAUSE` value in `btd6_integration.py`:
```python
pyautogui.PAUSE = 0.1  # Increase for slower actions
```

### Issue: Game uses different hotkeys
**Solution**: Modify `place_tower()` in `integration/btd6_integration.py`:
```python
def place_tower(self, tower_type: str, x: int, y: int):
    # Change 'q' to your game's hotkey
    pyautogui.press('d')  # Example: 'D' for Dart Monkey
    time.sleep(0.1)
    self.click_at_position(x, y)
```

## Advanced: Full AI Integration

To get the AI actually playing (not just the framework), you'll need to:

### 1. Implement State Parser
```python
def parse_game_state(screen):
    """Convert real game screen to AI observation"""
    balloons = detect_all_balloon_types(screen)  # All colors
    towers = detect_towers(screen)  # Template matching
    lives = parse_lives_ocr(screen)  # OCR for lives counter
    
    # Convert to 423-dim vector matching training format
    obs = convert_to_observation_vector(balloons, towers, lives)
    return obs
```

### 2. Create Control Loop
```python
from integration import BTD6Integration
from stable_baselines3 import PPO

integration = BTD6Integration(game_window_region=(100, 100, 800, 600))
model = PPO.load("models/btd6_test_final.zip")

# Start round in BTD6
integration.start_round()

while True:
    # Capture
    screen = integration.capture_screen()
    
    # Parse
    obs = parse_game_state(screen)  # You need to implement this
    
    # Decide
    action, _ = model.predict(obs)
    
    # Act
    if action < 4800:  # Place tower
        x, y = action_to_position(action)
        integration.place_tower("dart_monkey", x, y)
    
    time.sleep(0.1)  # Control loop rate
    
    # Check game over
    if integration.is_game_over(screen):
        break
```

### 3. Alternative: Train on Real Game
Instead of adapting the simulation-trained AI, you could:
1. Collect real game data (screens + manual actions)
2. Train directly on real game using imitation learning
3. Fine-tune with reinforcement learning

## Safety Features

The integration includes safety features:
- **Failsafe**: Move mouse to screen corner to abort (pyautogui built-in)
- **Window focus check**: Won't click if wrong window active (can add)
- **Rate limiting**: Delays between actions prevent spam

## Performance Tips

1. **Run at 30 FPS**: Reduce capture rate for better performance
2. **Use smaller region**: Capture only play area, not whole screen
3. **Optimize CV**: Use numpy operations, avoid Python loops
4. **Cache templates**: Load tower templates once, reuse

## Next Steps

1. **Start Simple**: Test each component individually (capture, detect, place)
2. **Iterate**: Get each working before combining
3. **Calibrate**: Adjust thresholds, timings, coordinates for your setup
4. **Extend**: Add more balloon types, towers, game modes

## Need Help?

Check the implementation files:
- `integration/btd6_integration.py` - Main integration code
- `test_real_game.py` - Testing script
- `docs/PHASE3_INTEGRATION.md` - Detailed integration docs

The framework is there - now it's about tuning it to your specific BTD6 setup!
