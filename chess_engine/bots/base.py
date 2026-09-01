from abc import ABC, abstractmethod


class BaseBot(ABC):
    """Common interface implemented by every PyChess bot."""

    @abstractmethod
    def choose_move(self, game_state):
        """Return a legal ``(origin, target)`` move, or ``None``."""
        raise NotImplementedError
