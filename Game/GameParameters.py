"""Contains the parameters for a `ASMACAG.Game.Game.Game`. Note that these are assumed to be static and therefore
are always shallow copied. Do not modify them after instatiating."""
import Game.Rules as Rules


class GameParameters:
    """Contains the parameters for a `ASMACAG.Game.Game.Game`. Note that these are assumed to be static and therefore
    are always shallow copied. Do not modify them after instatiating."""
    def __init__(self,
                 amount_cards_on_hand=9,
                 amount_cards_on_board=20,
                 amount_action_points=3,
                 min_number=1,
                 max_number=6,
                 amount_cards_limit_number=5,
                 amount_cards_normal_number=8,
                 amount_cards_mult2=6,
                 amount_cards_div2=6,
                 seed=None,
                 randomise_hidden_info=True,
                 forward_model: Rules.ForwardModel = Rules.SimpleForwardModel()):
        self.amount_cards_on_hand = amount_cards_on_hand
        self.amount_cards_on_board = amount_cards_on_board
        self.amount_action_points = amount_action_points
        self.min_number = min_number
        self.max_number = max_number
        self.amount_cards_limit_number = amount_cards_limit_number
        self.amount_cards_normal_number = amount_cards_normal_number
        self.amount_cards_mult2 = amount_cards_mult2
        self.amount_cards_div2 = amount_cards_div2
        self.seed = seed
        self.randomise_hidden_info = randomise_hidden_info
        self.forward_model = forward_model

    def __str__(self):
        return f"{self.amount_cards_on_hand} {self.amount_cards_on_board} {self.amount_action_points} " \
               f"{self.min_number} {self.max_number} {self.amount_cards_limit_number} " \
               f"{self.amount_cards_normal_number} {self.amount_cards_mult2} {self.amount_cards_div2} {self.seed} " \
               f"{self.forward_model}"
