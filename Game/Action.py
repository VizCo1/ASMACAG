"""An `ASMACAG.Game.Action.Action` describes the `ASMACAG.Game.Card.Card` played and on what `ASMACAG.Game.Card.Card` it
 has been played."""


class Action:
    """An `Action` describes the `ASMACAG.Game.Card.Card` played and on what `ASMACAG.Game.Card.Card` it has been
    played."""

    def __init__(self, played_card: "ASMACAG.Game.Card.Card", board_card: "ASMACAG.Game.Card.Card" = None):
        self.played_card = played_card
        self.board_card = board_card

# region Methods
    def clone(self) -> "Action":
        """Creates a deep copy of the `Action` and returns it."""
        new_action = Action(self.played_card.clone(), self.board_card.clone() if self.board_card is not None else None)
        return new_action

    def copy_into(self, other: "Action") -> None:
        """Deep copies the `Action` contents into another one."""
        self.played_card.copy_into(other.played_card)
        if self.board_card is not None:
            if other.board_card is None:
                other.board_card = self.board_card.clone()
            else:
                self.board_card.copy_into(other.board_card)
        else:
            other.board_card = None
# endregion

# region Getters and setters
    def get_played_card(self) -> "ASMACAG.Game.Card.Card":
        """Returns the `ASMACAG.Game.Card.Card` played."""
        return self.played_card

    def get_board_card(self) -> "ASMACAG.Game.Card.Card":
        """Returns the `ASMACAG.Game.Card.Card` on which the `Action.get_played_card` has been played (if the
        `ASMACAG.Game.Card.Card.get_type` of the `Action.get_played_card` is
        `ASMACAG.Game.CardType.CardType.NUMBER`)."""
        return self.board_card
# endregion

# region Overrides
    def __str__(self):
        return f"[{self.played_card!s}] on [{self.board_card if self.board_card is not None else 'nothing'!s}]"
# endregion
