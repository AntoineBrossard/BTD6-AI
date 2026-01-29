# Quick Start: Test with Your BTD6 Game

## One-Command Test

```bash
python test_real_game.py
```

## What It Does

1. ✅ **Calibrates** - You point to game corners
2. ✅ **Captures** - Takes screenshot, saves to `btd6_capture.png`
3. ✅ **Detects** - Finds red balloons on screen
4. ✅ **Controls** - Places ONE test tower in your game

## Before You Run

- [ ] BTD6 is open
- [ ] New game on Monkey Meadow (Easy)
- [ ] At start screen (round not started)
- [ ] Game window fully visible

## What to Expect

### ✅ Success Looks Like:
- Screenshot saved correctly
- A Dart Monkey appears in your game center
- Console shows "✅ Tower placement executed!"

### ⚠️ If Nothing Happens:
1. Check game window has focus
2. Try adjusting `pyautogui.PAUSE` in code
3. Verify 'Q' hotkey works for Dart Monkey
4. Check you have enough money ($170)

## Current Limitations

The AI is **simulation-trained**, not real-game-trained:
- ✅ Can capture screen
- ✅ Can control game (place towers)
- ⚠️ Needs work to fully "see" real game state
- ⚠️ Needs calibration for your specific setup

## To Make It Fully Work

You'll need to implement (framework provided):
1. Parse all balloon colors (not just red)
2. Detect your tower placements
3. Read lives/money from UI (OCR)
4. Convert to AI's expected format

See `docs/TESTING_REAL_GAME.md` for step-by-step guide!

## Quick Debug

```python
# Just test screen capture
from integration import BTD6Integration
integration = BTD6Integration()
screen = integration.capture_screen()

import cv2
cv2.imwrite("debug.png", screen)
# Check debug.png
```

---

**The good news**: Framework is built and working!
**Your job**: Calibrate detection and controls for your setup.

Happy testing! 🎮
