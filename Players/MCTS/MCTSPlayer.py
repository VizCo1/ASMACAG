"""Entity that plays a `ASMACAG.Game.Game.Game` by using the Monte Carlo Tree Search algorithm to choose all
 `ASMACAG.Game.Action.Action` in a turn."""
import time

from Players import Player
from Players.MCTS.MCTSNode import MCTSNode


class MCTSPlayer(Player):
    """Entity that plays a `ASMACAG.Game.Game.Game` by using the Monte Carlo Tree Search algorithm to choose all
     `ASMACAG.Game.Action.Action` in a turn."""
    def __init__(self, heuristic: "ASMACAG.Heuristics.Heuristic.Heuristic", c_value: float):
        self.heuristic = heuristic
        self.c_value = c_value
        self.turn = []
        super().__init__()

# region Methods
    def think(self, observation: "ASMACAG.Game.Observation.Observation", budget: float) -> "ASMACAG.Game.Action.Action":
        """Computes a list of `ASMACAG.Game.Action.Action` for a complete turn using the Monte Carlo Tree Search
        algorithm and returns them in order each time it's called during the turn."""
        if observation.action_points_left == observation.game_parameters.amount_action_points:
            self.turn.clear()
            self.compute_turn(observation, budget)
        return self.turn.pop(0)

    def compute_turn(self, observation: "ASMACAG.Game.Observation.Observation",
                     budget: float) -> None:
        """Computes a list of `ASMACAG.Game.Action.Action` for a complete turn using the Monte Carlo Tree Search
        algorithm and sets it as the turn."""
        # initial tree setup
        t0 = time.time()
        root = MCTSNode(observation, self.heuristic, None)
        root.extend()
        current_node = root

        # main loop
        # note that the 0.12 value must be enough seconds to transverse the tree, so low spec computers or more complex
        # rule sets and parameters may need it bumped up, tested working properly with the default parameters on an
        # Intel Core i7-4790 CPU @ 3.60GHz running Ubuntu 20.04.4 LTS and Python 3.9.7
        while time.time() - t0 < budget - 0.12:
            best_child = current_node.get_best_child_by_ucb(self.c_value)
            if best_child.get_amount_of_children() > 0:
                current_node = best_child
            else:
                if not best_child.get_is_unvisited() and not best_child.get_is_terminal():
                    best_child.extend()
                    best_child = best_child.get_random_child()
                best_child.backpropagate(best_child.rollout())
                current_node = root

        # retrieve the turn
        current_node = root
        for i in range(observation.game_parameters.amount_action_points):
            best_child = current_node.get_best_child_by_average()
            self.turn.append(best_child.get_action() if best_child is not None else None)
            current_node = best_child
# endregion

# region Overrides
    def __str__(self):
        return f"MCTSPlayer[{self.c_value}]"
# endregion
