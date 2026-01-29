"""
Autonomous AI BTD6 Player
The AI observes the game and makes decisions independently
"""

import time
import pyautogui
from integration import BTD6Integration
import keyboard
from stable_baselines3 import PPO
import numpy as np
import cv2

print("=" * 60)
print("BTD6-AI: Autonomous Player")
print("=" * 60)
print()

print("📋 SETUP INSTRUCTIONS:")
print("-" * 60)
print("1. Open Bloons Tower Defense 6")
print("2. Start a new game on Monkey Meadow (beginner map)")
print("3. Set difficulty to Easy")
print("4. Position the game window so it's fully visible")
print("5. Wait at the start screen (don't start the round yet)")
print()
input("Press ENTER when BTD6 is ready...")

print("\n🎯 CALIBRATION:")
print("-" * 60)
print("Move your mouse to the TOP-LEFT corner of the game play area")
print("You have 5 seconds...")
time.sleep(5)
top_left = pyautogui.position()
print(f"✅ Top-left: {top_left}")

print("\nNow move your mouse to the BOTTOM-RIGHT corner of the game play area")
print("You have 5 seconds...")
time.sleep(5)
bottom_right = pyautogui.position()
print(f"✅ Bottom-right: {bottom_right}")

game_region = (
    top_left.x,
    top_left.y,
    bottom_right.x - top_left.x,
    bottom_right.y - top_left.y
)
print(f"\n✅ Game region: {game_region}")

# Initialize integration
integration = BTD6Integration(game_window_region=game_region)

print("\n🤖 LOADING AI MODEL:")
print("-" * 60)

try:
    model = PPO.load("models/btd6_test_final.zip")
    print("✅ Model loaded successfully")
except FileNotFoundError:
    print("❌ No trained model found. Run: python train_quick.py")
    exit(1)

# Game state tracking
placed_towers = []
current_lives = 100
current_money = 650  # Starting money on Easy
round_number = 1
round_in_progress = False
last_round_start_time = 0
money_spent = 0

# Quit flag + listener (replaces keyboard.is_pressed)
quit_flag = False

def _on_press(key):
    global quit_flag
    try:
        if key.char == 'q':
            quit_flag = True
            return False
    except AttributeError:
        pass

listener = keyboard.Listener(on_press=_on_press)
listener.start()

# Grid system for actions (must match training environment)
# Training uses 800x600 with grid_resolution=10
grid_resolution = 10
tiles_x = 800 // grid_resolution  # 80 tiles
tiles_y = 600 // grid_resolution  # 60 tiles
num_actions = tiles_x * tiles_y + 1  # +1 for do nothing (matches env.py)

def action_to_position(action: int):
    """Convert action index to screen position"""
    tile_x = action % tiles_x
    tile_y = action // tiles_x
    # Convert tile to pixel in 800x600 space
    x = tile_x * grid_resolution + grid_resolution // 2
    y = tile_y * grid_resolution + grid_resolution // 2
    # Scale to actual game region
    scale_x = game_region[2] / 800
    scale_y = game_region[3] / 600
    return int(x * scale_x), int(y * scale_y)

def build_observation(balloons_list, towers_list, lives=100, money=650, game_state=1):
    """Build observation for the AI model (must match env.py format)"""
    max_balloons = 100
    max_towers = 10
    # Training env uses 800x600
    width = 800
    height = 600
    obs = []

    # Balloon data: x, y, health, type (raw pixel values, not normalized)
    for i in range(max_balloons):
        if i < len(balloons_list):
            b = balloons_list[i]
            # Scale detected positions to 800x600 space
            scale_x = width / game_region[2]
            scale_y = height / game_region[3]
            obs.extend([b["x"] * scale_x, b["y"] * scale_y, 1, 1])  # health=1, type=1
        else:
            obs.extend([0, 0, 0, 0])

    # Tower data: x, y (raw pixel values)
    for i in range(max_towers):
        if i < len(towers_list):
            t = towers_list[i]
            # Towers are stored in scaled coordinates already
            obs.extend([t[0], t[1]])
        else:
            obs.extend([0, 0])

    # Game info: lives, round, state (raw values like env.py)
    obs.extend([lives, round_number, game_state])
    return np.array(obs, dtype=np.float32)

def place_tower_with_keybind(x, y):
    """Place tower using 'z' keybind then click"""
    global current_money, money_spent
    
    # Cost of dart monkey
    tower_cost = 200
    if current_money < tower_cost:
        return False
    
    try:
        # Press 'z' to select dart monkey
        pyautogui.press('z')
        time.sleep(0.2)
        
        # Click to place
        screen_x = game_region[0] + x
        screen_y = game_region[1] + y
        pyautogui.click(screen_x, screen_y)
        time.sleep(0.2)
        
        # Update money
        current_money -= tower_cost
        money_spent += tower_cost
        
        return True
    except Exception as e:
        print(f"❌ Tower placement failed: {e}")
        return False

def try_start_round():
    """Attempt to start the next round"""
    global round_in_progress, last_round_start_time, round_number
    
    # Don't spam start
    if time.time() - last_round_start_time < 5:
        return False
    
    try:
        # Try to find and click start button
        used_click = integration.start_round_auto()
        if used_click or True:  # Always attempt
            round_in_progress = True
            last_round_start_time = time.time()
            round_number += 1
            print(f"▶️ Starting round {round_number}")
            return True
    except Exception as e:
        print(f"❌ Failed to start round: {e}")
    
    return False

print("\n🎮 AUTONOMOUS AI GAMEPLAY:")
print("-" * 60)
print("The AI will now play autonomously!")
print("Press 'q' to stop the AI at any time")
print("\nStarting in 3 seconds...")
time.sleep(3)

# Main AI loop
frame_count = 0
try:
    while True:
        # Check for quit
        if quit_flag:
            print("\n⏹️ Stopped by user")
            break
        
        frame_count += 1
        
        # Capture game state
        screen = integration.capture_screen()
        detected_balloons = integration.detect_balloons(screen)
        
        # Check if round is still active
        if round_in_progress and len(detected_balloons) == 0 and frame_count % 30 == 0:
            # Might be round over
            round_in_progress = False
            current_money += 100  # Rough estimate of round reward
        
        # Determine game state: 1 = running, 0 = not started, 2 = won, 3 = lost
        game_state = 1 if round_in_progress else 0
        
        # Build observation (must match training env format)
        obs = build_observation(detected_balloons, placed_towers, current_lives, current_money, game_state)
        
        # Get AI decision
        action, _ = model.predict(obs, deterministic=True)
        action = int(action)
        
        # Execute action
        if action < tiles_x * tiles_y:
            # Place tower action
            x, y = action_to_position(action)
            if place_tower_with_keybind(x, y):
                # Store tower position in 800x600 space for observation
                tile_x = action % tiles_x
                tile_y = action // tiles_x
                tower_x = tile_x * grid_resolution + grid_resolution // 2
                tower_y = tile_y * grid_resolution + grid_resolution // 2
                placed_towers.append((tower_x, tower_y))
                print(f"🗼 Placed tower #{len(placed_towers)} at ({x}, {y}) | Money: ${current_money}")
        
        # Action == tiles_x * tiles_y is "do nothing" in env.py
        # Auto-start rounds when not in progress to keep game moving
        if not round_in_progress and frame_count % 50 == 0:
            try_start_round()
        
        # Status update every 50 frames
        if frame_count % 50 == 0:
            print(f"📊 Status: Round {round_number} | Towers: {len(placed_towers)} | Balloons: {len(detected_balloons)} | Money: ${current_money}")
        
        # Control frame rate
        time.sleep(0.1)
        
        # Safety limit
        if frame_count > 10000:
            print("\n⏱️ Frame limit reached")
            break

except KeyboardInterrupt:
    print("\n⏹️ Interrupted by user")
finally:
    listener.stop()

print("\n" + "=" * 60)
print("📊 GAME SUMMARY:")
print("=" * 60)
print(f"Towers placed: {len(placed_towers)}")
print(f"Money spent: ${money_spent}")
print(f"Rounds completed: {round_number - 1}")
print(f"Total frames: {frame_count}")
print("=" * 60)
