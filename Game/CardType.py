"""enum that describes the different types of `ASMACAG.Game.Card.Card`."""
from enum import Enum


class CardType(Enum):
    """enum that describes the different types of `ASMACAG.Game.Card.Card`."""
    NUMBER = 1
    """A `ASMACAG.Game.Card.Card` that contains a number."""
    MULT2 = 2
    """A `ASMACAG.Game.Card.Card` that multiplies the resulting score of using the next `ASMACAG.Game.Action.Action` 
    by 2."""
    DIV2 = 3
    """A `ASMACAG.Game.Card.Card` that divides the resulting score of using the next `ASMACAG.Game.Action.Action`
    by 2."""
