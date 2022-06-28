"""Main program that reproduces the specific experiments performed during the development of ASMACAG and its associated
project."""
from Game import *
from Players import *
from Heuristics import *


if __name__ == '__main__':
    amount_of_games = 1000                              # number of games to play
    budget = 1                                          # time to think for the players (in seconds)
    verbose = False                                     # whether to print messages
    enforce_time = True                                 # whether the player time to think is going to be enforced
    parameters = GameParameters()                       # parameters for the game itself
    save_name = f"out/reproduce_experiments.csv"        # where the games' summary is going to be saved
    save_file = open(save_name, "w")
    dimensions = [38, 38, 38]
    initial_players = [
                       # MCTS experiments
                       OSLAPlayer(SimpleHeuristic()), MCTSPlayer(SimpleHeuristic(), 0.5),
                       OSLAPlayer(SimpleHeuristic()), MCTSPlayer(SimpleHeuristic(), 1.414),
                       OSLAPlayer(SimpleHeuristic()), MCTSPlayer(SimpleHeuristic(), 3),
                       OSLAPlayer(SimpleHeuristic()), MCTSPlayer(SimpleHeuristic(), 8),
                       OSLAPlayer(SimpleHeuristic()), MCTSPlayer(SimpleHeuristic(), 14),
                       OSLAPlayer(SimpleHeuristic()), MCTSPlayer(SimpleHeuristic(), 20),
                       OSLAPlayer(SimpleHeuristic()), MCTSPlayer(SimpleHeuristic(), 30),
                       OSLAPlayer(SimpleHeuristic()), MCTSPlayer(SimpleHeuristic(), 45),

                       # OE experiments
                       OSLAPlayer(SimpleHeuristic()), OEPlayer(SimpleHeuristic(), 75, 0.15, 0.35),
                       OSLAPlayer(SimpleHeuristic()), OEPlayer(SimpleHeuristic(), 25, 0.15, 0.35),
                       OSLAPlayer(SimpleHeuristic()), OEPlayer(SimpleHeuristic(), 125, 0.15, 0.35),
                       OSLAPlayer(SimpleHeuristic()), OEPlayer(SimpleHeuristic(), 175, 0.15, 0.35),
                       OSLAPlayer(SimpleHeuristic()), OEPlayer(SimpleHeuristic(), 75, 0.05, 0.35),
                       OSLAPlayer(SimpleHeuristic()), OEPlayer(SimpleHeuristic(), 75, 0.25, 0.35),
                       OSLAPlayer(SimpleHeuristic()), OEPlayer(SimpleHeuristic(), 75, 0.35, 0.35),
                       OSLAPlayer(SimpleHeuristic()), OEPlayer(SimpleHeuristic(), 75, 0.15, 0.05),
                       OSLAPlayer(SimpleHeuristic()), OEPlayer(SimpleHeuristic(), 75, 0.15, 0.15),
                       OSLAPlayer(SimpleHeuristic()), OEPlayer(SimpleHeuristic(), 75, 0.15, 0.55),
                       OSLAPlayer(SimpleHeuristic()), OEPlayer(SimpleHeuristic(), 75, 0.15, 0.75),

                       # NTBEA experiments
                       OSLAPlayer(SimpleHeuristic()), NTBEAPlayer(SimpleHeuristic(), dimensions, 8, 20, 0.3, 500),
                       OSLAPlayer(SimpleHeuristic()), NTBEAPlayer(SimpleHeuristic(), dimensions, 8, 5, 0.3, 500),
                       OSLAPlayer(SimpleHeuristic()), NTBEAPlayer(SimpleHeuristic(), dimensions, 8, 10, 0.3, 500),
                       OSLAPlayer(SimpleHeuristic()), NTBEAPlayer(SimpleHeuristic(), dimensions, 8, 50, 0.3, 500),
                       OSLAPlayer(SimpleHeuristic()), NTBEAPlayer(SimpleHeuristic(), dimensions, 8, 120, 0.3, 500),
                       OSLAPlayer(SimpleHeuristic()), NTBEAPlayer(SimpleHeuristic(), dimensions, 8, 20, 0.05, 500),
                       OSLAPlayer(SimpleHeuristic()), NTBEAPlayer(SimpleHeuristic(), dimensions, 8, 20, 0.15, 500),
                       OSLAPlayer(SimpleHeuristic()), NTBEAPlayer(SimpleHeuristic(), dimensions, 8, 20, 0.55, 500),
                       OSLAPlayer(SimpleHeuristic()), NTBEAPlayer(SimpleHeuristic(), dimensions, 8, 20, 0.8, 500),
                       OSLAPlayer(SimpleHeuristic()), NTBEAPlayer(SimpleHeuristic(), dimensions, 8, 20, 0.3, 50),
                       OSLAPlayer(SimpleHeuristic()), NTBEAPlayer(SimpleHeuristic(), dimensions, 8, 20, 0.3, 100),
                       OSLAPlayer(SimpleHeuristic()), NTBEAPlayer(SimpleHeuristic(), dimensions, 8, 20, 0.3, 1000),
                       OSLAPlayer(SimpleHeuristic()), NTBEAPlayer(SimpleHeuristic(), dimensions, 8, 20, 0.3, 3000),

                       # final experiments
                       RandomPlayer(), OSLAPlayer(SimpleHeuristic()),

                       RandomPlayer(), MCTSPlayer(SimpleHeuristic(), 8),

                       RandomPlayer(), OEPlayer(SimpleHeuristic(), 125, 0.15, 0.15),

                       RandomPlayer(), NTBEAPlayer(SimpleHeuristic(), dimensions, 8, 5, 0.55, 1000),

                       OSLAPlayer(SimpleHeuristic()), MCTSPlayer(SimpleHeuristic(), 8),

                       OSLAPlayer(SimpleHeuristic()), OEPlayer(SimpleHeuristic(), 125, 0.15, 0.15),

                       OSLAPlayer(SimpleHeuristic()), NTBEAPlayer(SimpleHeuristic(), dimensions, 8, 5, 0.55, 1000),

                       MCTSPlayer(SimpleHeuristic(), 8), OEPlayer(SimpleHeuristic(), 125, 0.15, 0.15),

                       MCTSPlayer(SimpleHeuristic(), 8), NTBEAPlayer(SimpleHeuristic(), dimensions, 8, 5, 0.55, 1000),

                       OEPlayer(SimpleHeuristic(), 125, 0.15, 0.15),
                       NTBEAPlayer(SimpleHeuristic(), dimensions, 8, 5, 0.55, 1000)]

    while len(initial_players) > 0:
        players = initial_players[:2].copy()
        first_player_wins = 0
        second_player_wins = 0
        ties = 0
        save_file.write(f"{initial_players[0]!s},{initial_players[1]!s}\n")
        for i in range(amount_of_games):
            game = Game(parameters)
            game.run(players[0], players[1], budget, verbose, enforce_time)

            if game.get_winner() == 0:
                if (i % 2) == 0:
                    first_player_wins += 1
                else:
                    second_player_wins += 1
            elif game.get_winner() == 1:
                if (i % 2) == 0:
                    second_player_wins += 1
                else:
                    first_player_wins += 1
            else:
                ties += 1

            if verbose:
                print("")
                print("*** ------------------------------------------------- ")
                if game.get_winner() != -1:
                    print(f"*** The winner is the player: {game.get_winner()!s} [{players[game.get_winner()]!s}]")
                    print(f"*** [{initial_players[0]!s}]: {first_player_wins!s}."
                          f" [{initial_players[1]!s}]: {second_player_wins!s}."
                          f" Ties: {ties!s}")
                else:
                    print("*** There is a Tie.")
                    print(f"*** [{initial_players[0]!s}]: {first_player_wins!s}."
                          f" [{initial_players[1]!s}]: {second_player_wins!s}."
                          f" Ties: {ties!s}")
                    print("*** ------------------------------------------------- ")
            else:
                print(f"[{initial_players[0]!s}]: {first_player_wins!s}."
                      f" [{initial_players[1]!s}]: {second_player_wins!s}."
                      f" Ties: {ties!s}")

            players.reverse()

        save_file.write(f"{first_player_wins!s},{second_player_wins!s},{ties!s}\n")
        save_file.flush()
        initial_players.pop(0)
        initial_players.pop(0)
    save_file.close()
