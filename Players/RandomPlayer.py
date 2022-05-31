"""Entity that plays a `ASMACAG.Game.Game.Game` by selecting random valid actions."""
import random
from Players import Player


class RandomPlayer(Player):
    """Entity that plays a `ASMACAG.Game.Game.Game` by selecting random valid actions."""
    def __init__(self):
        super().__init__()

# region Methods
    def think(self, observation: "ASMACAG.Game.Observation.Observation", budget: int) -> "ASMACAG.Game.Action.Action":
        """Returns a randomly selected valid `ASMACAG.Game.Action.Action` to play given an
        `ASMACAG.Game.Observation.Observation`."""
        return random.choice(observation.get_actions())
# endregion

# region Overrides
    def __str__(self):
        return "RandomPlayer"
# endregion
