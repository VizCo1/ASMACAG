"""Main program that plays a `ASMACAG.Game.Game.Game` between two `ASMACAG.Players.Player.Player`."""
import random
from Game import *
from Players import *

if __name__ == '__main__':
    budget = 10                                      # time to think for the players (in seconds)
    verbose = True                                  # whether to print messages
    enforce_time = True                             # whether the player time to think is going to be enforced
    save_name = "out/test.txt"                      # where the game is going to be saved, can be None
    parameters = GameParameters()                   # parameters for the game itself, set seed here to repeat a game
    players = [RandomPlayer(), OSLAPlayer()]        # list of players

    game = Game(parameters)
    game.set_save_file(save_name)

    # who starts is determined randomly
    if random.randint(0, 1):
        players.reverse()

    game.run(players[0], players[1], budget, verbose, enforce_time)

    if verbose:
        print("")
        print("*** ------------------------------------------------- ")
        if game.get_winner() != -1:
            print(f"*** The winner is the player: {game.get_winner()!s} [{players[game.get_winner()]!s}]")
        else:
            print("*** There is a Tie.")
        print("*** ------------------------------------------------- ")
