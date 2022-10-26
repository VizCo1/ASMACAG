
import math
import time
from Players import Player


class NOSLAPlayer(Player):
    def __init__(self, heuristic: "ASMACAG.Heuristics.Heuristic.Heuristic"):
        self.heuristic = heuristic

# region Methods
    def think(self, observation: "ASMACAG.Game.Observation.Observation", budget: float) -> "ASMACAG.Game.Action.Action":
        t0 = time.time()
        best_reward = -math.inf
        best_actions = []
        current_observation = observation.clone()
        while time.time() - t0 < budget * 0.9:
            observation.copy_into(current_observation)
            current_observation.randomise()
            possible_actions = []
            while not observation.game_parameters.forward_model.is_terminal(current_observation) \
                    and not observation.game_parameters.forward_model.is_turn_finished(current_observation):
                action = current_observation.get_random_action()
                observation.game_parameters.forward_model.step(current_observation, action)
                possible_actions.append(action)

            reward = self.heuristic.get_reward(current_observation)

            if reward >= best_reward:
                best_actions = possible_actions
                best_reward = reward

        return best_actions.pop(0)
# endregion

# region Overrides
    def __str__(self):
        return "NOSLAPlayer"
# endregion
