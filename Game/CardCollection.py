"""An ordered collection of `ASMACAG.Game.Card.Card` that can be used to define a deck, hand, table..."""
import random
from typing import Iterable


class CardCollection:
    """An ordered collection of `ASMACAG.Game.Card.Card` that can be used to define a deck, hand, table..."""
    def __init__(self):
        self.cards = []

# region Methods
    def clear(self) -> None:
        """Empties the `CardCollection`."""
        self.cards.clear()

    def add_card(self, card: "ASMACAG.Game.Card.Card") -> "None":
        """Adds a `ASMACAG.Game.Card.Card` to the `CardCollection`."""
        self.cards.append(card)

    def add_cards(self, cards: "Iterable[ASMACAG.Game.Card.Card]") -> "None":
        """Adds any iterable collection of `ASMACAG.Game.Card.Card` to the `CardCollection`."""
        self.cards.extend(cards)

    def shuffle(self) -> None:
        """Shuffles the `CardCollection`."""
        random.shuffle(self.cards)

    def draw(self) -> "ASMACAG.Game.Card.Card":
        """Removes and returns the first `ASMACAG.Game.Card.Card` from the `CardCollection`."""
        card = self.cards[0]
        self.cards.pop(0)
        return card

    def remove(self, card: "ASMACAG.Game.Card.Card") -> None:
        """Removes the fist occurrence of the specified `ASMACAG.Game.Card.Card` from the `CardCollection`."""
        self.cards.remove(card)

    def clone(self) -> "CardCollection":
        """Creates a deep copy of the `CardCollection` and returns it."""
        new_card_collection = CardCollection()

        for card in self.cards:
            new_card_collection.add_card(card.clone())

        return new_card_collection

    def copy_into(self, other: "CardCollection") -> None:
        """Deep copies the `CardCollection` contents into another one."""
        if len(self) >= len(other):
            for cardIndex in range(len(other)):
                self.get_card(cardIndex).copy_into(other.get_card(cardIndex))

            for card in range(len(other), len(self.cards)):
                other.add_card(self.cards[card].clone())

        else:
            del other.cards[len(self):]
            for cardIndex in range(len(self)):
                self.get_card(cardIndex).copy_into(other.get_card(cardIndex))
# endregion

# region Getters and setters
    def get_empty(self) -> bool:
        """Returns a bool stating whether the `CardCollection` is empty."""
        if self.cards:
            return False
        return True

    def get_cards(self) -> "list[ASMACAG.Game.Card.Card]":
        """Returns the ordered list of `ASMACAG.Game.Card.Card` contained in the `CardCollection`."""
        return self.cards

    def get_card(self, index: int) -> "ASMACAG.Game.Card.Card":
        """Returns the `ASMACAG.Game.Card.Card` contained in the `CardCollection` at the specified index."""
        return self.cards[index]
# endregion

# region Overrides
    def __str__(self):
        s = ""
        for card in self.cards:
            s += f"[{card!s}] "
        return s

    def __iter__(self):
        return self.cards.__iter__()

    def __len__(self):
        return len(self.cards)
# endregion
