"""A `ASMACAG.Game.Card.Card` has a `ASMACAG.Game.CardType.CardType`. It also has a number if it is a
`ASMACAG.Game.CardType.CardType.NUMBER`."""
import Game


class Card:
    """A `Card` has a `ASMACAG.Game.CardType.CardType`. It also has a number if it is a
    `ASMACAG.Game.CardType.CardType.NUMBER`."""

    def __init__(self, card_type: "ASMACAG.Game.CardType.CardType", number: int = None):
        self.card_type = card_type
        self.number = number

# region Methods
    def clone(self) -> "Card":
        """Creates a copy of the `Card` and returns it."""
        new_card = Card(self.card_type, self.number)
        return new_card

    def copy_into(self, other: "Card") -> None:
        """Copies the `Card` contents into another one."""
        other.card_type = self.card_type
        other.number = self.number
# endregion

# region Getters and setters
    def get_type(self) -> "ASMACAG.Game.CardType.CardType":
        """Returns the type of the `Card` as a `ASMACAG.Game.CardType.CardType`."""
        return self.card_type

    def get_number(self) -> int:
        """Returns the number of the `Card` (if `Card.get_type` is `ASMACAG.Game.CardType.CardType.NUMBER`)."""
        return self.number
# endregion

# region Overrides
    def __str__(self):
        return f"{self.card_type!s}{f' {self.number}' if self.card_type == Game.CardType.NUMBER else ''!s}"

    def __eq__(self, other):
        return isinstance(other, Card) and other.card_type == other.card_type and self.number == other.number

    def __hash__(self):
        # note that this may not generate a unique hash for parameter sets that are not the default ones
        return self.number + 1 if self.card_type == Game.CardType.NUMBER else self.card_type.value - 2
# endregion
