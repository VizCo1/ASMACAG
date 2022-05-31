from abc import ABC, abstractmethod


class Heuristic(ABC):
    """Abstract base class that defines a reward for the current `ASMACAG.Players.Player.Player` given an
    `ASMACAG.Game.Observation.Observation`."""

    @abstractmethod
    def get_reward(self, observation: "ASMACAG.Game.Observation.Observation") -> float:
        """Returns a reward for the current `ASMACAG.Players.Player.Player` given an
        `ASMACAG.Game.Observation.Observation`."""
        pass
