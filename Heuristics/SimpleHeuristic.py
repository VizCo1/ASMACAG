from Heuristics import Heuristic


class SimpleHeuristic(Heuristic):
    """Defines a simple reward for the current `ASMACAG.Players.Player.Player` given an
    `ASMACAG.Game.Observation.Observation` by using the current score difference."""

# region Methods
    def get_reward(self, observation: "ASMACAG.Game.Observation.Observation") -> float:
        """Returns a reward for the current `ASMACAG.Players.Player.Player` given an
        `ASMACAG.Game.Observation.Observation` by using the current score difference."""
        if observation.current_turn == 0:
            return observation.player_0_score - observation.player_1_score
        else:
            return observation.player_1_score - observation.player_0_score
# endregion
