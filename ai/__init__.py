"""
AI package initialization
"""

from ai.env import BTD6Env
from ai.train import train, evaluate

__all__ = ["BTD6Env", "train", "evaluate"]
