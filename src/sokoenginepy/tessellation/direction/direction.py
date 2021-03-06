from enum import IntEnum


class UnknownDirectionError(ValueError):
    pass


class Direction(IntEnum):
    """Directions of movement."""
    UP = 0
    NORTH_EAST = 1
    RIGHT = 2
    SOUTH_EAST = 3
    DOWN = 4
    SOUTH_WEST = 5
    LEFT = 6
    NORTH_WEST = 7

    def __repr__(self):
        return "Direction." + self.name

    @property
    def opposite(self):
        return _OPPOSITE.get(self, None)


_OPPOSITE = {
    Direction.UP: Direction.DOWN,
    Direction.DOWN: Direction.UP,
    Direction.LEFT: Direction.RIGHT,
    Direction.RIGHT: Direction.LEFT,
    Direction.NORTH_WEST: Direction.SOUTH_EAST,
    Direction.SOUTH_EAST: Direction.NORTH_WEST,
    Direction.NORTH_EAST: Direction.SOUTH_WEST,
    Direction.SOUTH_WEST: Direction.NORTH_EAST
}
