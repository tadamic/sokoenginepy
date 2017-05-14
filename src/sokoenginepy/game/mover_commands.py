from abc import ABC, abstractmethod


class MoverCommand(ABC):
    def __init__(self, mover):
        self._mover = mover
        self._moves = []
        self._rendered_moves = []

    @abstractmethod
    def redo(self):
        """Redoes movement command."""
        pass

    @abstractmethod
    def undo(self):
        """Undoes movement command."""
        pass

    @property
    def mover(self):
        return self._mover

    @property
    def render(self):
        """
        Returns sequence of :class:`.AtomicMove` from last execution.

        This sequence is showing the moves like they would be rendered in GUI.
        Thus, it might be different between undo and redo execution.
        """
        return self._rendered_moves

    @property
    def moves(self):
        """Sequence of :class:`.AtomicMove` resulting from :meth:`.redo` call."""
        return self._moves


class SelectPusherCommand(MoverCommand):
    def __init__(self, mover, pusher_id):
        super().__init__(mover)
        self._new_pusher_id = pusher_id
        self._old_pusher_id = self._mover.selected_pusher

    def redo(self):
        self._mover.select_pusher(self._new_pusher_id)
        self._moves = self._mover.last_move
        self._rendered_moves = self._mover.last_move

    def undo(self):
        self._mover.select_pusher(self._old_pusher_id)
        self._rendered_moves = self._mover.last_move

    @property
    def old_pusher_id(self):
        return self._old_pusher_id

    @property
    def new_pusher_id(self):
        return self._new_pusher_id


class JumpCommand(MoverCommand):
    def __init__(self, mover, final_position):
        super().__init__(mover)
        self._initial_position = mover.state.pusher_position(
            mover.selected_pusher
        )
        self._final_position = final_position

    def redo(self):
        self._mover.jump(self._final_position)
        self._moves = self._mover.last_move
        self._rendered_moves = self._mover.last_move

    def undo(self):
        self._mover.jump(self._initial_position)
        self._rendered_moves = self._mover.last_move

    @property
    def initial_position(self):
        return self._initial_position

    @property
    def final_position(self):
        return self._final_position


class MoveCommand(MoverCommand):
    def __init__(self, mover, direction):
        super().__init__(mover)
        self._direction = direction

    @property
    def direction(self):
        return self._direction

    def redo(self):
        self._mover.move(self._direction)
        self._moves = self._mover.last_move
        self._rendered_moves = self._mover.last_move

    def undo(self):
        self._mover.last_move = self._moves
        self._mover.undo_last_move()
        self._rendered_moves = self._mover.last_move
