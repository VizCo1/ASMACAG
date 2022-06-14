"""Module containing different `ASMACAG.Players.Player.Player` to evaluate a `ASMACAG.Game.GameState.GameState` or an
`ASMACAG.Game.Observation.Observation`."""
# import all the separate files to make the Players folder act as a single module
from Players.Player import Player
from Players.RandomPlayer import RandomPlayer
from Players.OSLAPlayer import OSLAPlayer
from Players.HumanPlayer import HumanPlayer
from Players.MCTS import MCTSPlayer
from Players.OEPlayer import OEPlayer
from Players.NTBEA import NTBEAPlayer
