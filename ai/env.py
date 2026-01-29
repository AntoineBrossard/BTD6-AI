"""
Gymnasium environment wrapper for BTD6 game
Converts the game into an RL environment
"""

import gymnasium as gym
import numpy as np
from gymnasium import spaces
from typing import Tuple, Dict, Any

from game import BTD6Game, GameState


class BTD6Env(gym.Env):
    """
    Gymnasium environment for BTD6.

    Action space: Discrete action representing tower placement position
        - 0-799: X coordinate (width = 800)
        - 0-599: Y coordinate (height = 600)
    Flattened to single action: action = x * 600 + y
    """

    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 60}

    def __init__(self, width: int = 800, height: int = 600, render_mode: str = None):
        super().__init__()

        self.width = width
        self.height = height
        self.render_mode = render_mode
        self.game = BTD6Game(width=width, height=height)

        # Action space: place tower at (x, y) or do nothing
        # We discretize the grid into 10x10 tiles for action space
        self.grid_resolution = 10
        self.tiles_x = width // self.grid_resolution
        self.tiles_y = height // self.grid_resolution
        self.num_actions = self.tiles_x * self.tiles_y + 1  # +1 for "do nothing"

        self.action_space = spaces.Discrete(self.num_actions)

        # Observation space
        # We'll use a flattened representation of game state
        # Max 100 balloons, max 10 towers, 2 values per entity + game info
        self.max_balloons = 100
        self.max_towers = 10

        obs_size = (
            self.max_balloons * 4  # balloon: x, y, health, type
            + self.max_towers * 2  # tower: x, y
            + 3  # game info: lives, round, state
        )

        self.observation_space = spaces.Box(
            low=0, high=max(width, height, 1000), shape=(obs_size,), dtype=np.float32
        )

        self.renderer = None
        if render_mode == "human":
            import pygame

            pygame.init()
            from game.renderer import BTD6Renderer

            self.renderer = BTD6Renderer(self.game, width, height)

        self.step_count = 0
        self.max_steps = 1000

    def reset(
        self, seed: int = None, options: Dict[str, Any] = None
    ) -> Tuple[np.ndarray, Dict[str, Any]]:
        """Reset environment"""
        super().reset(seed=seed)

        self.game = BTD6Game(width=self.width, height=self.height)
        self.step_count = 0

        return self._get_observation(), {}

    def step(self, action: int) -> Tuple[np.ndarray, float, bool, bool, Dict[str, Any]]:
        """
        Execute one step of the environment.

        Args:
            action: Integer from 0 to num_actions-1

        Returns:
            observation, reward, terminated, truncated, info
        """
        self.step_count += 1

        # Decode action to (x, y)
        if action < self.num_actions - 1:  # Not "do nothing"
            tile_x = action % self.tiles_x
            tile_y = action // self.tiles_x

            # Convert tile to pixel position (center of tile)
            x = tile_x * self.grid_resolution + self.grid_resolution // 2
            y = tile_y * self.grid_resolution + self.grid_resolution // 2

            self.game.place_tower(x, y)

        # Simulate game for a few frames
        dt = 1.0 / 60.0  # 60 FPS
        for _ in range(10):  # 10 frames per action
            self.game.update(dt)

            if self.game.state != GameState.RUNNING:
                break

        # Calculate reward
        reward = self._calculate_reward()

        # Check if done
        terminated = self.game.state in [GameState.WON, GameState.LOST]
        truncated = self.step_count >= self.max_steps

        if self.render_mode == "human":
            self.render()

        return (
            self._get_observation(),
            reward,
            terminated,
            truncated,
            {"state": self.game.state.name},
        )

    def render(self):
        """Render current game state"""
        if self.renderer:
            self.renderer.render()

    def _get_observation(self) -> np.ndarray:
        """Convert game state to observation array"""
        obs = []

        # Add balloons (pad to max_balloons)
        for i in range(self.max_balloons):
            if i < len(self.game.balloons):
                b = self.game.balloons[i]
                obs.extend([b.position.x, b.position.y, b.health, b.balloon_type.value])
            else:
                obs.extend([0, 0, 0, 0])

        # Add towers (pad to max_towers)
        for i in range(self.max_towers):
            if i < len(self.game.towers):
                t = self.game.towers[i]
                obs.extend([t.position.x, t.position.y])
            else:
                obs.extend([0, 0])

        # Add game info
        obs.extend([self.game.lives, self.game.round, self.game.state.value])

        return np.array(obs, dtype=np.float32)

    def _calculate_reward(self) -> float:
        """Calculate reward for this step"""
        reward = 0.0

        # Reward for surviving
        reward += 0.1

        # Reward for balloons killed (inferred from lives not lost)
        # This is implicit in the structure

        # Penalty for lost lives
        reward -= (self.game.max_lives - self.game.lives) * 10

        # Reward for winning
        if self.game.state == GameState.WON:
            reward += 1000

        # Penalty for losing
        if self.game.state == GameState.LOST:
            reward -= 1000

        return reward

    def close(self):
        """Close environment"""
        if self.renderer:
            self.renderer.close()
        super().close()
