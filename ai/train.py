"""
AI training script using Stable Baselines3
"""

import os
from ai.env import BTD6Env
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.callbacks import CheckpointCallback, EvalCallback

# Create output directory
models_dir = "models"
logs_dir = "logs"

os.makedirs(models_dir, exist_ok=True)
os.makedirs(logs_dir, exist_ok=True)


def train(
    total_timesteps: int = 100000,
    model_name: str = "btd6_ppo",
    log_interval: int = 10,
):
    """
    Train an RL agent on the BTD6 environment

    Args:
        total_timesteps: Total number of environment steps to train
        model_name: Name of the model to save
        log_interval: Logging interval
    """

    # Create environment
    env = DummyVecEnv([lambda: BTD6Env(render_mode=None)])

    # Create agent
    model = PPO(
        "MlpPolicy",
        env,
        verbose=1,
        learning_rate=3e-4,
        n_steps=2048,
        batch_size=64,
        n_epochs=10,
        gamma=0.99,
        gae_lambda=0.95,
        clip_range=0.2,
        tensorboard_log=None,  # Disable tensorboard for now
    )

    # Callbacks
    checkpoint_callback = CheckpointCallback(
        save_freq=10000,
        save_path=models_dir,
        name_prefix=model_name,
        save_replay_buffer=False,
    )

    # Train
    print(f"Training for {total_timesteps} timesteps...")
    model.learn(
        total_timesteps=total_timesteps,
        callback=checkpoint_callback,
        log_interval=log_interval,
        tb_log_name=model_name,
    )

    # Save final model
    model.save(os.path.join(models_dir, f"{model_name}_final"))
    print(f"Model saved to {models_dir}/{model_name}_final.zip")

    env.close()


def evaluate(model_path: str, episodes: int = 10, render: bool = True):
    """
    Evaluate a trained model

    Args:
        model_path: Path to the saved model
        episodes: Number of episodes to evaluate
        render: Whether to render the environment
    """

    env = BTD6Env(render_mode="human" if render else None)
    model = PPO.load(model_path)

    total_reward = 0
    for episode in range(episodes):
        obs, _ = env.reset()
        done = False
        episode_reward = 0

        while not done:
            action, _ = model.predict(obs, deterministic=True)
            obs, reward, terminated, truncated, _ = env.step(action)
            episode_reward += reward
            done = terminated or truncated

        total_reward += episode_reward
        print(f"Episode {episode + 1}: {episode_reward}")

    print(f"Average reward: {total_reward / episodes}")

    env.close()


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "eval":
        model_path = sys.argv[2] if len(sys.argv) > 2 else os.path.join(models_dir, "btd6_ppo_final")
        evaluate(model_path, episodes=5, render=True)
    else:
        train(total_timesteps=50000, model_name="btd6_ppo")
