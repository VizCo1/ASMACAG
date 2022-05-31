"""A `ASMACAG.Game.GameState.GameState` view for a particular `ASMACAG.Players.Player.Player` where the
non-observable parts have been randomized."""
import Game


class Observation:
    """A `ASMACAG.Game.GameState.GameState` view for a particular `ASMACAG.Players.Player.Player` where the
    non-observable parts have been randomized."""
    def __init__(self, game_state: "ASMACAG.Game.GameState.GameState"):
        if game_state is not None:
            self.game_parameters = game_state.game_parameters
            self.current_turn = game_state.current_turn
            self.player_0_hand = game_state.player_0_hand.clone()
            self.player_1_hand = game_state.player_1_hand.clone()
            self.board = game_state.board.clone()
            self.main_deck = game_state.main_deck.clone()
            self.discard_deck = game_state.discard_deck.clone()
            self.player_0_score = game_state.player_0_score
            self.player_1_score = game_state.player_1_score
            self.factor = game_state.factor
            self.action_points_left = game_state.action_points_left
            self.randomise()

# region Methods
    def clone(self) -> "Observation":
        """Creates a deep copy of the `Observation` and returns it."""
        new_observation = Observation(None)
        new_observation.game_parameters = self.game_parameters
        new_observation.current_turn = self.current_turn
        new_observation.player_0_hand = self.player_0_hand.clone()
        new_observation.player_1_hand = self.player_1_hand.clone()
        new_observation.board = self.board.clone()
        new_observation.main_deck = self.main_deck.clone()
        new_observation.discard_deck = self.discard_deck.clone()
        new_observation.player_0_score = self.player_0_score
        new_observation.player_1_score = self.player_1_score
        new_observation.factor = self.factor
        new_observation.action_points_left = self.action_points_left 
        return new_observation

    def copy_into(self, other: "Observation") -> None:
        """Deep copies the `Observation` contents into another one."""
        other.game_parameters = self.game_parameters
        other.current_turn = self.current_turn
        self.player_0_hand.copy_into(other.player_0_hand)
        self.player_1_hand.copy_into(other.player_1_hand)
        self.board.copy_into(other.board)
        self.main_deck.copy_into(other.main_deck)
        self.discard_deck.copy_into(other.discard_deck)
        other.player_0_score = self.player_0_score
        other.player_1_score = self.player_1_score
        other.factor = self.factor
        other.action_points_left = self.action_points_left

    def randomise(self) -> None:
        """Randomises the `Observation` to get a new possible state of the `ASMACAG.Game.Game.Game`."""
        # shuffle together all non-visible cards in the main deck
        self.main_deck.add_cards(self.player_1_hand if self.current_turn == 0 else self.player_0_hand)
        self.main_deck.shuffle()

        # draw cards to opponent hand
        if self.current_turn == 0:
            for _ in range(self.game_parameters.amount_cards_on_hand):
                self.player_1_hand.add_card(self.main_deck.draw())
        else:
            for _ in range(self.game_parameters.amount_cards_on_hand):
                self.player_0_hand.add_card(self.main_deck.draw())

    def get_actions(self) -> "list[ASMACAG.Game.Action.Action]":
        """Gets a list of the currently possible `ASMACAG.Game.Action.Action`."""
        actions = []
        hand = self.player_0_hand if self.current_turn == 0 else self.player_1_hand
        
        for card in hand.get_cards():
            if card.get_type() == Game.CardType.NUMBER:
                for board_card in self.board.get_cards():
                    actions.append(Game.Action(card, board_card))
            else:
                actions.append(Game.Action(card))
        return actions
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
