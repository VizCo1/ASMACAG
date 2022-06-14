"""Defines a basic default set of rules for a `ASMACAG.Game.Game.Game`."""
from typing import Union
import Game
from Game.Rules import ForwardModel


class SimpleForwardModel(ForwardModel):
    """Defines a basic default set of rules for a `ASMACAG.Game.Game.Game`."""

    # region Methods
    def step(self, game_state: "Union[ASMACAG.Game.GameState.GameState, ASMACAG.Game.Observation.Observation]",
             action: "ASMACAG.Game.Action.Action") -> bool:
        """Moves a `ASMACAG.Game.GameState.GameState` or `ASMACAG.Game.Observation.Observation` forward by playing
        the `ASMACAG.Game.Action.Action`. Returns false if the `ASMACAG.Game.Action.Action` couldn't be played."""
        game_state.action_points_left -= 1

        if game_state.current_turn == 0:
            hand = game_state.player_0_hand
        else:
            hand = game_state.player_1_hand

        if action is None:
            # invalid action: no action returned
            game_state.discard_deck.add_card(hand.get_cards()[0])
            hand.remove(hand.get_cards()[0])
            self.give_min_score(game_state)
            return False
        elif action.get_played_card() not in hand:
            # invalid action: selected card is not in hand, give min score and remove first card in hand
            game_state.discard_deck.add_card(hand.get_cards()[0])
            hand.remove(hand.get_cards()[0])
            self.give_min_score(game_state)
            return False
        else:
            if action.get_played_card().get_type() == Game.CardType.NUMBER:
                # number action
                if action.get_board_card() is None or action.get_board_card() not in game_state.board:
                    # invalid number action: no card on board to play, give min score and remove played card form hand
                    game_state.discard_deck.add_card(action.get_played_card())
                    hand.remove(action.get_played_card())
                    self.give_min_score(game_state)
                    return False
                else:
                    # valid number action
                    score = action.get_played_card().get_number() - action.get_board_card().get_number()
                    if game_state.factor != 1:
                        score *= game_state.factor
                        game_state.factor = 1

                    if game_state.current_turn == 0:
                        game_state.player_0_score += score
                    else:
                        game_state.player_1_score += score

                    game_state.discard_deck.add_card(action.get_played_card())
                    game_state.discard_deck.add_card(action.get_board_card())
                    hand.remove(action.get_played_card())
                    game_state.board.remove(action.get_board_card())
            else:
                # special action
                if action.get_played_card().get_type() == Game.CardType.MULT2:
                    game_state.factor *= 2
                else:
                    game_state.factor /= 2

                game_state.discard_deck.add_card(action.get_played_card())
                hand.remove(action.get_played_card())

    def on_turn_ended(self, game_state: "Union[ASMACAG.Game.GameState.GameState,"
                                        "ASMACAG.Game.Observation.Observation]") -> None:
        """Moves the `ASMACAG.Game.GameState.GameState` or `ASMACAG.Game.Observation.Observation` when the
        `ASMACAG.Players.Player.Player` turn is finished."""
        if self.is_turn_finished(game_state):
            game_state.current_turn = (game_state.current_turn + 1) % 2
            game_state.action_points_left = game_state.game_parameters.amount_action_points

    def is_terminal(self, game_state: "Union[ASMACAG.Game.GameState.GameState,"
                                      "ASMACAG.Game.Observation.Observation]") -> bool:
        """Tests a `ASMACAG.Game.GameState.GameState` or `ASMACAG.Game.Observation.Observation` against a finish
        condition and returns whether it has finished."""
        return game_state.player_0_hand.get_empty() and game_state.player_1_hand.get_empty() \
            or game_state.board.get_empty()

    def is_turn_finished(self, game_state: "Union[ASMACAG.Game.GameState.GameState,"
                                           "ASMACAG.Game.Observation.Observation]") -> bool:
        """Tests a `ASMACAG.Game.GameState.GameState` or `ASMACAG.Game.Observation.Observation` against the end turn
        condition and returns whether the turn has finished."""
        return game_state.action_points_left <= 0 \
            or (game_state.current_turn == 0 and game_state.player_0_hand.get_empty()) \
            or (game_state.current_turn == 1 and game_state.player_1_hand.get_empty())

    def give_min_score(self, game_state: "Union[ASMACAG.Game.GameState.GameState,"
                                         "ASMACAG.Game.Observation.Observation]") -> None:
        """Calculates the minimum possible score for the `ASMACAG.Game.GameState.GameState` or
        `ASMACAG.Game.Observation.Observation` and adds it to the current player."""
        score = pow(2, game_state.game_parameters.amount_action_points - 1) \
            * (game_state.game_parameters.min_number - game_state.game_parameters.max_number)

        if game_state.current_turn == 0:
            game_state.player_0_score += score
        else:
            game_state.player_1_score += score
# endregion

# region Overrides
    def __str__(self):
        return "SimpleForwardModel"
# endregion
