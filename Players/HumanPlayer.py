"""Entity that lets a human player play an `ASMACAG.Game.Game.Game` by using console inputs."""
from Players import Player


class HumanPlayer(Player):
    """Entity that lets a human player play an `ASMACAG.Game.Game.Game` by using console inputs."""
    def __init__(self):
        super().__init__()

# region Methods
    def think(self, observation: "ASMACAG.Game.Observation.Observation", budget: float) -> "ASMACAG.Game.Action.Action":
        """Requests the user to decide what `ASMACAG.Game.Action.Action` to play using the console."""
        actions = observation.get_actions()
        print("Actions that can be played: ")
        i = 0
        for action in actions:
            print(f"{i!s}->{action!s}")
            i += 1

        action_index = -1
        while action_index < 0 or action_index >= len(actions):
            action_index = int(input("Select the action index: "))
        return actions[action_index]
# endregion

# region Overrides
    def __str__(self):
        return "HumanPlayer"
# endregion
