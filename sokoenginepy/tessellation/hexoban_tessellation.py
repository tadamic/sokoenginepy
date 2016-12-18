from .. import board, snapshot
from .cell_orientation import CellOrientation
from .direction import Direction, UnknownDirectionError
from .helpers import COLUMN, ROW, index_1d, on_board_2d
from .tessellation import Tessellation

_CHR_TO_ATOMIC_MOVE = {
    snapshot.AtomicMove.Characters.LOWER_L.value: (Direction.LEFT, False),
    snapshot.AtomicMove.Characters.UPPER_L.value: (Direction.LEFT, True),
    snapshot.AtomicMove.Characters.LOWER_R.value: (Direction.RIGHT, False),
    snapshot.AtomicMove.Characters.UPPER_R.value: (Direction.RIGHT, True),
    snapshot.AtomicMove.Characters.LOWER_U.value: (Direction.NORTH_WEST, False),
    snapshot.AtomicMove.Characters.UPPER_U.value: (Direction.NORTH_WEST, True),
    snapshot.AtomicMove.Characters.LOWER_D.value: (Direction.SOUTH_EAST, False),
    snapshot.AtomicMove.Characters.UPPER_D.value: (Direction.SOUTH_EAST, True),
    snapshot.AtomicMove.Characters.LOWER_NE.value: (Direction.NORTH_EAST, False),
    snapshot.AtomicMove.Characters.UPPER_NE.value: (Direction.NORTH_EAST, True),
    snapshot.AtomicMove.Characters.LOWER_SW.value: (Direction.SOUTH_WEST, False),
    snapshot.AtomicMove.Characters.UPPER_SW.value: (Direction.SOUTH_WEST, True),
}

_ATOMIC_MOVE_TO_CHR = dict((v, k) for k, v in _CHR_TO_ATOMIC_MOVE.items())


class HexobanTessellation(Tessellation):
    """Implements :class:`.Tessellation` for Hexoban variant."""

    _LEGAL_DIRECTIONS = (
        Direction.LEFT,
        Direction.RIGHT,
        Direction.NORTH_EAST,
        Direction.NORTH_WEST,
        Direction.SOUTH_EAST,
        Direction.SOUTH_WEST,
    )

    @property
    def legal_directions(self):
        return self._LEGAL_DIRECTIONS

    @property
    def graph_type(self):
        return board.GraphType.DIRECTED

    def neighbor_position(self, position, direction, board_width, board_height):
        # if not on_board_1d(position, board_width, board_height):
        #     return None

        row = ROW(position, board_width)
        column = COLUMN(position, board_width)

        if direction == Direction.LEFT:
            column -= 1
        elif direction == Direction.RIGHT:
            column += 1
        elif direction == Direction.NORTH_EAST:
            column += row % 2
            row -= 1
        elif direction == Direction.NORTH_WEST:
            column -= (row + 1) % 2
            row -= 1
        elif direction == Direction.SOUTH_EAST:
            column += row % 2
            row += 1
        elif direction == Direction.SOUTH_WEST:
            column -= (row + 1) % 2
            row += 1
        else:
            raise UnknownDirectionError(direction)

        if on_board_2d(column, row, board_width, board_height):
            return index_1d(column, row, board_width)
        return None

    @property
    def _char_to_atomic_move_dict(self):
        return _CHR_TO_ATOMIC_MOVE

    @property
    def _atomic_move_to_char_dict(self):
        return _ATOMIC_MOVE_TO_CHR
