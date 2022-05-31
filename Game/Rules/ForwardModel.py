from abc import ABC, abstractmethod
from typing import Union


class ForwardModel(ABC):
    """Abstract base class that defines the rules of a `ASMACAG.Game.Game.Game`."""

    @abstractmethod
    def step(self, game_state: "Union[ASMACAG.Game.GameState.GameState, ASMACAG.Game.Observation.Observation]",
             action: "ASMACAG.Game.Action.Action") -> bool:
        """Moves a `ASMACAG.Game.GameState.GameState` or `ASMACAG.Game.Observation.Observation` forward by playing
        the `ASMACAG.Game.Action.Action`. Returns false if the `ASMACAG.Game.Action.Action` couldn't be played."""
        pass

    @abstractmethod
    def on_turn_ended(self, game_state: "Union[ASMACAG.Game.GameState.GameState,"
                                        "ASMACAG.Game.Observation.Observation]") -> None:
        """Moves the `ASMACAG.Game.GameState.GameState` or `ASMACAG.Game.Observation.Observation` when the
        `ASMACAG.Players.Player.Player` turn is finished."""
        pass

    @abstractmethod
    def is_terminal(self, game_state: "Union[ASMACAG.Game.GameState.GameState,"
                                      "ASMACAG.Game.Observation.Observation]") -> bool:
        """Tests a `ASMACAG.Game.GameState.GameState` or `ASMACAG.Game.Observation.Observation` against a finish
        condition and returns whether it has finished."""
        pass
