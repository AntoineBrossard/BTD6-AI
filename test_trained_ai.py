"""
Test the trained AI model
"""

from ai.env import BTD6Env
from stable_baselines3 import PPO

# Load trained model
model = PPO.load("models/btd6_test_final.zip")
print("Model loaded successfully!")

# Create environment
env = BTD6Env(render_mode=None)

# Run 5 test episodes
print("\n=== Testing Trained AI ===\n")

wins = 0
losses = 0

for episode in range(5):
    obs, info = env.reset()
    episode_reward = 0
    done = False
    steps = 0
    
    while not done:
        # Get AI action
        action, _ = model.predict(obs, deterministic=True)
        
        # Execute action
        obs, reward, terminated, truncated, info = env.step(action)
        episode_reward += reward
        steps += 1
        done = terminated or truncated
    
    # Check result
    state = info.get('state', 'UNKNOWN')
    if state == 'WON':
        wins += 1
        result = "✅ WON"
    elif state == 'LOST':
        losses += 1
        result = "❌ LOST"
    else:
        result = f"⚠️ {state}"
    
    print(f"Episode {episode + 1}: {result} | Reward: {episode_reward:.2f} | Steps: {steps}")

print(f"\n=== Results ===")
print(f"Wins: {wins}/5 ({wins*20}%)")
print(f"Losses: {losses}/5 ({losses*20}%)")
print(f"Win rate: {wins/5*100:.1f}%")

env.close()
