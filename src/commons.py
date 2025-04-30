# pyright: strict

from enum import Enum, auto

class BoardSlot(Enum):
    """
    Variants for the possible board slots.
    """

    Empty = auto()
    Cross = auto()
    Circle = auto()

# Representation of the board
type BoardLike = list[BoardSlot]
