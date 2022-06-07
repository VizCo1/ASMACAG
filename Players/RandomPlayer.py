"""Entity that plays a `ASMACAG.Game.Game.Game` by selecting random valid `ASMACAG.Game.Action.Action`."""
from Players import Player


class RandomPlayer(Player):
    """Entity that plays a `ASMACAG.Game.Game.Game` by selecting random valid `ASMACAG.Game.Action.Action`."""
    def __init__(self):
        super().__init__()

# region Methods
    def think(self, observation: "ASMACAG.Game.Observation.Observation", budget: float) -> "ASMACAG.Game.Action.Action":
        """Returns a randomly selected valid `ASMACAG.Game.Action.Action` to play given an
        `ASMACAG.Game.Observation.Observation`."""
        return observation.get_random_action()
# endregion

# region Overrides
    def __str__(self):
        return "RandomPlayer"
# endregion
