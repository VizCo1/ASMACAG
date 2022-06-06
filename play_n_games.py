"""Main program that plays a set number of `ASMACAG.Game.Game.Game` between any number of pairs of
 `ASMACAG.Players.Player.Player`."""
from Game import *
from Players import *
from Heuristics import *

if __name__ == '__main__':
    amount_of_games = 10                              # number of games to play
    budget = 1                                          # time to think for the players (in seconds)
    verbose = True                                     # whether to print messages
    enforce_time = True                                 # whether the player time to think is going to be enforced
    parameters = GameParameters()                       # parameters for the game itself
    save_name = f"out/mcts.csv"                         # where the games' summary is going to be saved
    save_file = open(save_name, "w")
    initial_players = [OSLAPlayer(), MCTSPlayer(SimpleHeuristic(), 0.5),
                       OSLAPlayer(), MCTSPlayer(SimpleHeuristic(), 1.414),
                       OSLAPlayer(), MCTSPlayer(SimpleHeuristic(), 3),
                       OSLAPlayer(), MCTSPlayer(SimpleHeuristic(), 8),
                       OSLAPlayer(), MCTSPlayer(SimpleHeuristic(), 14),
                       OSLAPlayer(), MCTSPlayer(SimpleHeuristic(), 20),
                       OSLAPlayer(), MCTSPlayer(SimpleHeuristic(), 30),
                       OSLAPlayer(), MCTSPlayer(SimpleHeuristic(), 45)]

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


