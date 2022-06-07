"""Entity that plays a `ASMACAG.Game.Game.Game` by using the Online Evolution algorithm to evolve a list of
 `ASMACAG.Game.Action.Action` composing a turn."""
import random
import time

from Game import CardType
from Players import Player
from Players.Shared import TurnGenome


class OEPlayer(Player):
    """Entity that plays a `ASMACAG.Game.Game.Game` by using the Online Evolution algorithm to evolve a list of
     `ASMACAG.Game.Action.Action` composing a turn."""
    def __init__(self, population_size: int, mutation_rate: float, survival_rate: float,
                 heuristic: "ASMACAG.Game.Heuristic.Heuristic") -> None:
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.survival_rate = survival_rate
        self.heuristic = heuristic
        self.turn = []
        super().__init__()

# region Methods
    def think(self, observation: "ASMACAG.Game.Observation.Observation", budget: float) -> "ASMACAG.Game.Action.Action":
        """Returns a randomly selected valid `ASMACAG.Game.Action.Action` to play given an
        `ASMACAG.Game.Observation.Observation`."""
        if observation.action_points_left == observation.game_parameters.amount_action_points:
            self.turn.clear()
            self.compute_turn(observation, budget)
        return self.turn.pop(0)

    def compute_turn(self, observation: "ASMACAG.Game.Observation.Observation",
                     budget: float) -> None:
        """Computes a list of `ASMACAG.Game.Action.Action` for a complete turn using the Online Evolution algorithm and
        sets it as the turn."""
        t0 = time.time()
        population = []
        killed = []

        new_observation = observation.clone()
        # initial population
        for i in range(self.population_size):
            genome = TurnGenome()
            observation.copy_into(new_observation)
            genome.random(new_observation)
            if genome.get_actions()[0].get_played_card().get_type() == CardType.NUMBER and genome.get_actions()[0].get_board_card() is None:
                return
            if genome.get_actions()[1].get_played_card().get_type() == CardType.NUMBER and genome.get_actions()[1].get_board_card() is None:
                return
            if genome.get_actions()[2].get_played_card().get_type() == CardType.NUMBER and genome.get_actions()[2].get_board_card() is None:
                return
            population.append(genome)
            killed.append(genome)

        # main loop
        while time.time() - t0 < budget - 0.001:
            # evaluate the new genomes
            for genome in killed:
                observation.copy_into(new_observation)
                for action in genome.get_actions():
                    observation.game_parameters.forward_model.step(new_observation, action)
                genome.set_reward(self.heuristic.get_reward(new_observation))

            # kill the worst genomes
            killed.clear()
            population.sort(key=lambda g: g.get_reward(), reverse=True)
            first_killed_genome_index = int(self.survival_rate * self.population_size)
            for i in range(first_killed_genome_index, self.population_size):
                killed.append(population[i])

            # create new genomes using the remaining ones for crossover
            for killed_genome in killed:
                # decide parents
                parent_a_index = random.randrange(first_killed_genome_index)
                parent_b_index = random.randrange(first_killed_genome_index)
                while parent_a_index == parent_b_index and len(killed) > 1:
                    parent_b_index = random.randrange(first_killed_genome_index)

                # crossover
                observation.copy_into(new_observation)
                killed_genome.crossover(population[parent_a_index], population[parent_b_index], new_observation)

                # mutate
                if random.random() < self.mutation_rate:
                    observation.copy_into(new_observation)
                    killed_genome.mutate_at_random_index(new_observation)

        # select the best genome to use for the turn
        self.turn = population[0].get_actions()
# endregion

# region Overrides
    def __str__(self):
        return f"OEPlayer[{self.population_size!s}][{self.mutation_rate!s}][{self.survival_rate!s}]"
# endregion
