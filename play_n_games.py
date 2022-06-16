"""Main program that plays a set number of `ASMACAG.Game.Game.Game` between any number of pairs of
 `ASMACAG.Players.Player.Player`."""
from Game import *
from Players import *
from Heuristics import *


if __name__ == '__main__':
    amount_of_games = 1000                              # number of games to play
    budget = 1                                          # time to think for the players (in seconds)
    verbose = False                                     # whether to print messages
    enforce_time = True                                 # whether the player time to think is going to be enforced
    parameters = GameParameters()                       # parameters for the game itself
    save_name = f"out/final.csv"                        # where the games' summary is going to be saved
    save_file = open(save_name, "w")
    dimensions = [38, 38, 38]
    initial_players = [RandomPlayer(), OSLAPlayer(SimpleHeuristic()),

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
        initial_players.pop(0)
        initial_players.pop(0)
    save_file.close()
