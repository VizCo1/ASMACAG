"""Genome class representing a list of `ASMACAG.Game.Action.Action` composing a turn for use in both
`ASMACAG.Players.OEPlayer.OEPlayer` and `ASMACAG.Players.NTBEAPlayer.NTBEAPlayer`."""
import random

from Game import CardType


class TurnGenome:
    """Genome class representing a list of `ASMACAG.Game.Action.Action` composing a turn for use in both
    `ASMACAG.Players.OEPlayer.OEPlayer` and `ASMACAG.Players.NTBEAPlayer.NTBEAPlayer`."""

    def __init__(self) -> None:
        self.actions = []
        self.reward = 0

# region Methods
    def random(self, observation: "ASMACAG.Game.Observation.Observation") -> None:
        """Fills up this `ASMACAG.Players.TurnGenome.TurnGenome` with random valid `ASMACAG.Game.Action.Action`
        composing a turn. Note that the observation state is not preserved."""
        self.actions.clear()
        self.reward = 0
        while not observation.game_parameters.forward_model.is_terminal(observation) \
                and not observation.game_parameters.forward_model.is_turn_finished(observation):
            self.actions.append(observation.get_random_action())
            observation.game_parameters.forward_model.step(observation, self.actions[-1])

    def crossover(self, parent_a: "TurnGenome", parent_b: "TurnGenome",
                  observation: "ASMACAG.Game.Observation.Observation") -> None:
        """Fills up this `ASMACAG.Players.TurnGenome.TurnGenome` with `ASMACAG.Game.Action.Action` from the parents
        while making sure that the resulting turn is valid. Note that the observation state is not preserved."""
        self.reward = 0
        for i in range(observation.game_parameters.amount_action_points):
            # choose a random parent and add action at index if valid, otherwise use the other parent
            added = False
            if bool(random.getrandbits(1)):
                if observation.is_action_valid(parent_a.actions[i]):
                    parent_a.actions[i].copy_into(self.actions[i])
                    added = True
                elif observation.is_action_valid(parent_b.actions[i]):
                    parent_b.actions[i].copy_into(self.actions[i])
                    added = True
            else:
                if observation.is_action_valid(parent_b.actions[i]):
                    parent_b.actions[i].copy_into(self.actions[i])
                    added = True
                elif observation.is_action_valid(parent_a.actions[i]):
                    parent_a.actions[i].copy_into(self.actions[i])
                    added = True

            # if no action was added, add a random one
            if not added:
                self.actions[i] = observation.get_random_action()

            observation.game_parameters.forward_model.step(observation, self.actions[i])

    def mutate_at_random_index(self, observation: "ASMACAG.Game.Observation.Observation") -> None:
        """Mutates this `ASMACAG.Players.TurnGenome.TurnGenome` at a random `ASMACAG.Game.Action.Action` of the turn
        while keeping the whole turn valid. Note that the observation state is not preserved."""
        mutation_index = random.randint(0, len(self.actions) - 1)
        for i in range(len(self.actions)):
            if i == mutation_index:
                self.actions[i] = observation.get_random_action()
            elif i > mutation_index:
                if not observation.is_action_valid(self.actions[i]):
                    self.actions[i] = observation.get_random_action()

            observation.game_parameters.forward_model.step(observation, self.actions[i])

    def clone(self) -> "TurnGenome":
        """Returns a clone of this `ASMACAG.Players.TurnGenome.TurnGenome`."""
        clone = TurnGenome()
        clone.set_reward(self.get_reward())
        for action in self.get_actions():
            clone.actions.append(action.clone())
        return clone

    def copy_into(self, other: "TurnGenome") -> None:
        """Copies this `ASMACAG.Players.TurnGenome.TurnGenome` into another one."""
        other.set_reward(self.get_reward())
        for i in range(len(self.get_actions())):
            if i < len(other.get_actions()):
                self.get_actions()[i].copy_into(other.get_actions()[i])
            else:
                other.get_actions().append(self.get_actions()[i].clone())
# endregion

# region Getters and Setters
    def get_actions(self) -> "list[ASMACAG.Game.Action.Action]":
        """Returns the list of `ASMACAG.Game.Action.Action` composing this `ASMACAG.Players.TurnGenome.TurnGenome`."""
        return self.actions

    def get_reward(self) -> float:
        """Returns the reward of this `ASMACAG.Players.TurnGenome.TurnGenome`."""
        return self.reward

    def set_reward(self, reward: float) -> None:
        """Sets the reward of this `ASMACAG.Players.TurnGenome.TurnGenome`."""
        self.reward = reward
# endregion

# region Overrides
    def __str__(self):
        return f"TurnGenome [actions={self.actions}, reward={self.reward}]"
# endregion
