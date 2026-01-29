"""
Quick training test (small scale)
"""

from ai.train import train

# Train for just 10k steps as a test
train(total_timesteps=10000, model_name="btd6_test", log_interval=1)

print("\nTraining complete! Model saved to models/btd6_test_final.zip")
