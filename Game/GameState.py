"""Contains the state of a `ASMACAG.Game.Game.Game`."""
import Game


class GameState:
    """Contains the state of a `ASMACAG.Game.Game.Game`."""
    def __init__(self, game_parameters: "ASMACAG.Game.GameParameters.GameParameters"):
        self.game_parameters = game_parameters
        self.current_turn = 0
        self.player_0_hand = Game.CardCollection()
        self.player_1_hand = Game.CardCollection()
        self.board = Game.CardCollection()
        self.main_deck = Game.CardCollection()
        self.discard_deck = Game.CardCollection()
        self.player_0_score = 0
        self.player_1_score = 0
        self.factor = 1
        self.action_points_left = 0

# region Methods
    def get_observation(self) -> "ASMACAG.Game.Observation.Observation":
        """Gets a `ASMACAG.Game.Observation.Observation` representing this `GameState` with its non-observable parts
        randomised."""
        return Game.Observation(self)

    def reset(self) -> None:
        """Resets and sets up the `GameState` so that is ready for a new `ASMACAG.Game.Game.Game`. Must be called by
        `ASMACAG.Game.Game.Game.run`."""
        self.current_turn = 0
        self.player_0_hand.clear()
        self.player_1_hand.clear()
        self.board.clear()
        self.main_deck.clear()
        self.discard_deck.clear()
        self.player_0_score = 0
        self.player_1_score = 0
        self.factor = 1
        self.action_points_left = self.game_parameters.amount_action_points

        # add number cards to the deck
        for n in range(self.game_parameters.min_number, self.game_parameters.max_number + 1):
            if n == self.game_parameters.min_number or n == self.game_parameters.max_number:
                for _ in range(self.game_parameters.amount_cards_limit_number):
                    self.main_deck.add_card(Game.Card(Game.CardType.NUMBER, n))
            else:
                for _ in range(self.game_parameters.amount_cards_normal_number):
                    self.main_deck.add_card(Game.Card(Game.CardType.NUMBER, n))

        # add special cards to the deck
        for _ in range(self.game_parameters.amount_cards_mult2):
            self.main_deck.add_card(Game.Card(Game.CardType.MULT2))
        for _ in range(self.game_parameters.amount_cards_div2):
            self.main_deck.add_card(Game.Card(Game.CardType.DIV2))

        # shuffle the deck
        self.main_deck.shuffle()
        
        # draw cards into players' hands
        for _ in range(self.game_parameters.amount_cards_on_hand):
            self.player_0_hand.add_card(self.main_deck.draw())
            self.player_1_hand.add_card(self.main_deck.draw())

        # draw cards into the board, only number cards
        special_cards = Game.CardCollection()
        for _ in range(self.game_parameters.amount_cards_on_board):
            card = self.main_deck.draw()
            while card.get_type() != Game.CardType.NUMBER:
                special_cards.add_card(card)
                card = self.main_deck.draw()
            self.board.add_card(card)

        # add special cards again and shuffle the deck
        self.main_deck.add_cards(special_cards)
        self.main_deck.shuffle()
# endregion

# region Overrides
    def __str__(self):
        return (f"TURN: {self.current_turn!s}\n"
                f"BOARD: {self.board!s}\n"
                f"HAND P1: {self.player_0_hand!s}\n"
                f"SCORE P1: {self.player_0_score!s}\n"
                f"HAND P2: {self.player_1_hand!s}\n"
                f"SCORE P2: {self.player_1_score!s}\n"
                f"FACTOR: {self.factor!s}\n"
                f"ACTION POINTS LEFT: {self.action_points_left!s}")
# endregion
