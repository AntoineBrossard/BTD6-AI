"""
Test the gymnasium environment
"""

from ai.env import BTD6Env

# Create environment
env = BTD6Env(render_mode=None)

# Test reset
obs, info = env.reset()
print(f"Observation shape: {obs.shape}")
print(f"Action space: {env.action_space}")
print(f"Initial observation (first 20 values): {obs[:20]}")

# Test a few steps
total_reward = 0
for step in range(10):
    action = env.action_space.sample()  # Random action
    obs, reward, terminated, truncated, info = env.step(action)
    total_reward += reward
    
    print(f"\nStep {step+1}: action={action}, reward={reward:.2f}, terminated={terminated}, truncated={truncated}")
    
    if terminated or truncated:
        print("Episode ended!")
        break

print(f"\nTotal reward: {total_reward:.2f}")
env.close()
