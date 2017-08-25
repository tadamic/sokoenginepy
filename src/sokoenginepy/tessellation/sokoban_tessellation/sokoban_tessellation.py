from ...utilities import COLUMN, ROW, index_1d, inverted, is_on_board_2d
from ..direction import Direction, UnknownDirectionError
from ..tessellation_base import (TessellationBase,
                                 TessellationBaseInheritableDocstrings)


class SokobanTessellation(
    TessellationBase, metaclass=TessellationBaseInheritableDocstrings
):
    _LEGAL_DIRECTIONS = (
        Direction.LEFT, Direction.RIGHT, Direction.UP, Direction.DOWN
    )

    _CHR_TO_ATOMIC_MOVE = None
    _ATOMIC_MOVE_TO_CHR = None

    @property
    @copy_ancestor_docstring
    def legal_directions(self):
        return self._LEGAL_DIRECTIONS

    @property
    @copy_ancestor_docstring
    def graph_type(self):
        from ... import board
        return board.GraphType.DIRECTED

    _NEIGHBOR_SHIFT = {
        Direction.LEFT: (0, -1),
        Direction.RIGHT: (0, 1),
        Direction.UP: (-1, 0),
        Direction.DOWN: (1, 0),
    }

    @copy_ancestor_docstring
    def neighbor_position(self, position, direction, board_width, board_height):
        # if not is_on_board_1d(position, board_width, board_height):
        #     return None

        row = ROW(position, board_width)
        column = COLUMN(position, board_width)
        row_shift, column_shift = self._NEIGHBOR_SHIFT.get(
            direction, (None, None)
        )

        if row_shift is None:
            raise UnknownDirectionError(direction)

        row += row_shift
        column += column_shift

        if is_on_board_2d(column, row, board_width, board_height):
            return index_1d(column, row, board_width)

        return None

    @property
    def _char_to_atomic_move_dict(self):
        if not self.__class__._CHR_TO_ATOMIC_MOVE:
            from ... import snapshot
            self.__class__._CHR_TO_ATOMIC_MOVE = {
                snapshot.AtomicMoveCharacters.l: (Direction.LEFT, False),
                snapshot.AtomicMoveCharacters.L: (Direction.LEFT, True),
                snapshot.AtomicMoveCharacters.r: (Direction.RIGHT, False),
                snapshot.AtomicMoveCharacters.R: (Direction.RIGHT, True),
                snapshot.AtomicMoveCharacters.u: (Direction.UP, False),
                snapshot.AtomicMoveCharacters.U: (Direction.UP, True),
                snapshot.AtomicMoveCharacters.d: (Direction.DOWN, False),
                snapshot.AtomicMoveCharacters.D: (Direction.DOWN, True),
            }
        return self._CHR_TO_ATOMIC_MOVE

    @property
    def _atomic_move_to_char_dict(self):
        if not self.__class__._ATOMIC_MOVE_TO_CHR:
            self.__class__._ATOMIC_MOVE_TO_CHR = inverted(
                self._char_to_atomic_move_dict
            )
        return self._ATOMIC_MOVE_TO_CHR

    def __str__(self):
        return "sokoban"
