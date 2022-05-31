from abc import ABC, abstractmethod


class Player(ABC):
    """Abstract base class for an entity with a defined behaviour for playing a `ASMACAG.Game.Game.Game`."""
    
    @abstractmethod
    def think(self, observation: "ASMACAG.Game.Observation.Observation", budget: int) -> "ASMACAG.Game.Action.Action":
        """Returns an `ASMACAG.Game.Action.Action` to play given an `ASMACAG.Game.Observation.Observation`. It must
        return an action within the given budget of time (in seconds)."""
        pass
