"""Entity that plays a `ASMACAG.Game.Game.Game` by selecting the best `ASMACAG.Game.Action.Action` found with a greedy
one step lookahead search based on an `ASMACAG.Heuristics.Heuristic.Heuristic`."""
import math
from Players import Player


class OSLAPlayer(Player):
    """Entity that plays a `ASMACAG.Game.Game.Game` by selecting the best `ASMACAG.Game.Action.Action` found with a
    greedy one step lookahead search based on an `ASMACAG.Heuristics.Heuristic.Heuristic`."""
    def __init__(self, heuristic: "ASMACAG.Heuristics.Heuristic.Heuristic"):
        self.heuristic = heuristic

# region Methods
    def think(self, observation: "ASMACAG.Game.Observation.Observation", budget: float) -> "ASMACAG.Game.Action.Action":
        """Returns a randomly selected valid `ASMACAG.Game.Action.Action` to play given an
        `ASMACAG.Game.Observation.Observation`."""
        best_reward = -math.inf
        best_action = None
        current_observation = observation.clone()
        for action in observation.get_actions():
            observation.copy_into(current_observation)
            observation.game_parameters.forward_model.step(current_observation, action)
            reward = self.heuristic.get_reward(current_observation)
            if reward >= best_reward:
                best_action = action
                best_reward = reward
        return best_action
# endregion

# region Overrides
    def __str__(self):
        return "OSLAPlayer"
# endregion
