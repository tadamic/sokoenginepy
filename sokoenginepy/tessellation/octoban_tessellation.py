from .. import utilities
from .cell_orientation import CellOrientation
from .direction import Direction, UnknownDirectionError
from .helpers import COLUMN, ROW, index_1d, on_board_2d
from .tessellation_base import TessellationBase

_GLOBALS = {}


def _init_module():
    """
    Avoiding circular dependnecies by not importing :mod:`.board` and
    :mod:`.snapshot` untill they are needed
    """
    from .. import board, snapshot
    _GLOBALS['graph_type'] = board.GraphType.DIRECTED
    _GLOBALS['chr_to_atomic_move'] = {
        snapshot.AtomicMove.Characters.LOWER_L.value: (Direction.LEFT, False),
        snapshot.AtomicMove.Characters.UPPER_L.value: (Direction.LEFT, True),
        snapshot.AtomicMove.Characters.LOWER_R.value: (Direction.RIGHT, False),
        snapshot.AtomicMove.Characters.UPPER_R.value: (Direction.RIGHT, True),
        snapshot.AtomicMove.Characters.LOWER_U.value: (Direction.UP, False),
        snapshot.AtomicMove.Characters.UPPER_U.value: (Direction.UP, True),
        snapshot.AtomicMove.Characters.LOWER_D.value: (Direction.DOWN, False),
        snapshot.AtomicMove.Characters.UPPER_D.value: (Direction.DOWN, True),
        snapshot.AtomicMove.Characters.LOWER_NW.value: (Direction.NORTH_WEST, False),
        snapshot.AtomicMove.Characters.UPPER_NW.value: (Direction.NORTH_WEST, True),
        snapshot.AtomicMove.Characters.LOWER_SE.value: (Direction.SOUTH_EAST, False),
        snapshot.AtomicMove.Characters.UPPER_SE.value: (Direction.SOUTH_EAST, True),
        snapshot.AtomicMove.Characters.LOWER_NE.value: (Direction.NORTH_EAST, False),
        snapshot.AtomicMove.Characters.UPPER_NE.value: (Direction.NORTH_EAST, True),
        snapshot.AtomicMove.Characters.LOWER_SW.value: (Direction.SOUTH_WEST, False),
        snapshot.AtomicMove.Characters.UPPER_SW.value: (Direction.SOUTH_WEST, True),
    }
    _GLOBALS['atomic_move_to_chr'] = utilities.inverted(
        _GLOBALS['chr_to_atomic_move']
    )


class OctobanTessellation(TessellationBase):
    _LEGAL_DIRECTIONS = (
        Direction.LEFT,
        Direction.RIGHT,
        Direction.UP,
        Direction.DOWN,
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
        if not _GLOBALS:
            _init_module()
        return _GLOBALS['graph_type']

    _NEIGHBOR_SHIFT = {
        Direction.LEFT: (0, -1),
        Direction.RIGHT: (0, 1),
        Direction.UP: (-1, 0),
        Direction.DOWN: (1, 0),
        Direction.NORTH_WEST: (-1, -1),
        Direction.NORTH_EAST: (-1, 1),
        Direction.SOUTH_WEST: (1, -1),
        Direction.SOUTH_EAST: (1, 1),
    }

    def neighbor_position(self, position, direction, board_width, board_height):
        # if not on_board_1d(position, board_width, board_height):
        #     return None

        if self.cell_orientation(position, board_width, board_height
                                ) != CellOrientation.OCTAGON and (
                                    direction == Direction.NORTH_EAST or
                                    direction == Direction.NORTH_WEST or
                                    direction == Direction.SOUTH_EAST or
                                    direction == Direction.SOUTH_WEST
                                ):
            return None

        row = ROW(position, board_width)
        column = COLUMN(position, board_width)
        row_shift, column_shift = self._NEIGHBOR_SHIFT.get(
            direction, (None, None)
        )

        if row_shift is None:
            raise UnknownDirectionError(direction)

        row += row_shift
        column += column_shift

        if on_board_2d(column, row, board_width, board_height):
            return index_1d(column, row, board_width)

        return None

    @property
    def _char_to_atomic_move_dict(self):
        if not _GLOBALS:
            _init_module()
        return _GLOBALS['chr_to_atomic_move']

    @property
    def _atomic_move_to_char_dict(self):
        if not _GLOBALS:
            _init_module()
        return _GLOBALS['atomic_move_to_chr']

    def cell_orientation(self, position, board_width, board_height):
        row = ROW(position, board_width)
        column = COLUMN(position, board_width)
        return (
            CellOrientation.OCTAGON
            if (column + (row % 2)) % 2 == 0 else CellOrientation.DEFAULT
        )

    def __str__(self):
        return "octoban"
