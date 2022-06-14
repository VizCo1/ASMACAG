import copy
import math
import random
import time
from Players.NTBEA.Bandit1D import Bandit1D
from Players.NTBEA.Bandit2D import Bandit2D
from Players.NTBEA.FitnessEvaluator import FitnessEvaluator


# --------------------------------------------------------------
# NTBEA Algorithm
# --------------------------------------------------------------


class NTBEAPlayer:
    def __init__(self, heuristic, l_dimensions, c_value, n_neighbours, mutation_probability, initializations):
        self.c_value = c_value  # C parameter for ucb
        self.n_neighbours = n_neighbours  # Number of neighbours in ntbea iteration
        self.l_bandits1D = []  # 1D bandits
        self.l_bandits2D = []  # 2D bandits
        self.n_dimensions = len(l_dimensions)  # Dimension of the problem (i.e. number of parameters)

        self.l_dimensions = l_dimensions  # List of number of possible values of each parameter
        self.n_bandits1D = self.n_dimensions  # Number of 1D bandits
        self.n_bandits2D = (self.n_dimensions * (self.n_dimensions - 1)) / 2  # Number of 2D bandits

        self.create_bandits()  # Initialize the 1D and 2D bandits
        self.fitness = FitnessEvaluator(heuristic)
        self.heuristic = heuristic
        self.l_currents = []  # List of the selected individuals

        self.turn = []  # List of the selected individuals
        self.initializations = initializations
        self.mutation_probability = mutation_probability

    # --------------------------------------------------------------------
    # Initialize the bandits
    # --------------------------------------------------------------------
    def create_bandits(self):
        # Create empty 1D bandits
        for i in range(self.n_dimensions):
            new_bandit = Bandit1D(self.c_value)
            self.l_bandits1D.append(new_bandit)

        # Create empty 2D bandits
        for i in range(0, self.n_dimensions - 1):
            for j in range(i + 1, self.n_dimensions):
                new_bandit = Bandit2D(self.c_value)
                self.l_bandits2D.append(new_bandit)

    def think(self, observation: "ASMACAG.Game.Observation.Observation", budget: float) -> "ASMACAG.Game.Action.Action":
        """Returns an `ASMACAG.Game.Action.Action` to play given an
        `ASMACAG.Game.Observation.Observation`."""
        if observation.action_points_left == observation.game_parameters.amount_action_points:
            self.turn.clear()
            self.l_bandits1D.clear()
            self.l_bandits2D.clear()
            self.create_bandits()
            self.l_currents.clear()
            self.turn.clear()
            self.compute_turn(observation, budget, self.initializations)
        return self.turn.pop(0)

    # --------------------------------------------------------------------
    # Run the NTBEA algorithm
    # --------------------------------------------------------------------
    def compute_turn(self, observation, budget, initializations):
        t0 = time.time()
        current, score = self.valid_initialization(observation, initializations)
        new_observation = observation.clone()
        while time.time() - t0 < budget - 0.001:
            population = self.get_neighbours(current, self.n_neighbours, self.mutation_probability)  # get neigbours
            new_current = self.get_best_individual(population)  # Get best neighbour using bandits
            observation.copy_into(new_observation)
            new_score = self.fitness.evaluate(new_current, new_observation)  # Get the score of the new current individual
            if new_score > score:
                current = new_current
                score = new_score
            self.update_bandits(new_current, new_score)  # Update bandits
        self.turn = self.fitness.ntbea_to_turn(current)

    def valid_initialization(self, observation, initializations):
        population = []
        best_individual = None
        best_score = -math.inf
        new_observation = observation.clone()
        for i in range(initializations):
            observation.copy_into(new_observation)
            individual = self.get_random_individual_valid(new_observation)
            population.append(individual)
            score = self.heuristic.get_reward(new_observation)  # Get the score of the current individual
            self.update_bandits(individual, score)  # Update bandits
            if score > best_score:
                best_score = score
                best_individual = individual
        return best_individual, best_score

    # --------------------------------------------------------------------
    # return random individual moving observation forwards
    # --------------------------------------------------------------------
    def get_random_individual_valid(self, observation):
        individual = []
        for i in range(self.n_dimensions):
            act = observation.get_random_action()
            n = self.fitness.get_parameter_from_action(act)
            individual.append(n)
            observation.game_parameters.forward_model.step(observation, act)
        return individual

    # --------------------------------------------------------------------
    #  Update the bandits
    # --------------------------------------------------------------------
    # Given an individual (i.e. [1,3,4]) update all the bandits
    def update_bandits(self, individual, score):
        # 1D
        for i in range(self.n_bandits1D):
            element = individual[i]
            self.l_bandits1D[i].update(element, score)

        # 2D
        k = 0
        for i in range(0, self.n_dimensions - 1):
            for j in range(i + 1, self.n_dimensions):
                element1 = individual[i]
                element2 = individual[j]
                self.l_bandits2D[k].update(element1, element2, score)
                k += 1

    # --------------------------------------------------------------------
    # Returns the mean of all ucb of each bandit
    # An element not in a bandit returns a big number
    # --------------------------------------------------------------------
    def get_total_ucb(self, individual):
        acm = 0

        # 1D
        for i in range(0, self.n_dimensions):
            element = individual[i]
            acm += self.l_bandits1D[i].ucb(element)
            i += 1

        # 2D
        k = 0
        for i in range(0, self.n_dimensions - 1):
            for j in range(i + 1, self.n_dimensions):
                element1 = individual[i]
                element2 = individual[j]
                acm += self.l_bandits2D[k].ucb(element1, element2)
                k += 1

        return acm / (self.n_bandits1D + self.n_bandits2D)

    # --------------------------------------------------------------------
    # Obtain n_neighbours from an individual
    # Change at least one parameter (randomly chosen).
    # The rest can be changed depending of the mutation probability
    # --------------------------------------------------------------------
    def get_neighbours(self, individual, n_neighbours, mutation_probability):
        population = []
        while len(population) < n_neighbours:
            neighbour = copy.copy(individual)
            i = random.randint(0, self.n_dimensions - 1)  # the parameter to be changed
            for j in range(self.n_dimensions):
                if i == j:  # The parameter chosen is always mutated
                    self.mutate_gen(neighbour, j)
                else:  # The rest can be mutated depending of the mutation prob.
                    n = random.random()
                    if n < mutation_probability:
                        self.mutate_gen(neighbour, j)
            if not neighbour in population:
                if not neighbour in self.l_currents:
                    population.append(neighbour)
        return population

    # --------------------------------------------------------------------
    # Mutate the j-th gen of an individual
    # The mutation consists of change the value of the j-th gen using a different valid one
    # --------------------------------------------------------------------
    def mutate_gen(self, individual, j):
        prev_value = individual[j]
        new_value = random.randint(0, self.l_dimensions[j] - 1)
        while new_value == prev_value:  # if it is the same, try again
            new_value = random.randint(0, self.l_dimensions[j] - 1)

        individual[j] = new_value

    # --------------------------------------------------------------------
    # Get best individual from a population. It is the one with greater ucb
    # --------------------------------------------------------------------
    def get_best_individual(self, population):
        best_ucb = -math.inf
        best_individual = population[0]

        for individual in population:
            ucb = self.get_total_ucb(individual)
            if ucb > best_ucb:
                best_ucb = ucb
                best_individual = individual

        return best_individual

    def __str__(self):
        return f"NTBEA[{self.c_value}][{self.n_neighbours}][{self.mutation_probability}][{self.initializations}]"