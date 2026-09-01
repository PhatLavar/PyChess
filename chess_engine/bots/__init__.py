"""Computer-controlled players for PyChess."""

from chess_engine.bots.base import BaseBot
from chess_engine.bots.easy_bot import EasyBot
from chess_engine.bots.hard_bot import HardBot
from chess_engine.bots.impossible_bot import ImpossibleBot
from chess_engine.bots.master_bot import MasterBot
from chess_engine.bots.medium_bot import MediumBot

__all__ = [
    'BaseBot',
    'EasyBot',
    'MediumBot',
    'HardBot',
    'MasterBot',
    'ImpossibleBot'
]
