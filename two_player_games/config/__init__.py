from __future__ import annotations

from abc import ABC
from dataclasses import dataclass

from two_player_games.common import Category


@dataclass
class Config(ABC):
    category: Category
