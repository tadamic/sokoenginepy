import pytest

from sokoenginepy.board import (BoardConversionError, BoardCharacters,
                                is_board_string, is_box, is_empty_floor,
                                is_goal, is_pusher, is_wall,
                                parse_board_string)


class Describe_is_board_string:
    input = "0123456789\n\t bB$*p_pmM@+#_-|"

    def it_recognizes_board_string(self):
        assert is_board_string(self.input)

    def it_fails_on_illegal_characters(self):
        assert not is_board_string(self.input + "z")

    def it_fails_on_numeric_string(self):
        assert not is_board_string("42")

    def it_fails_on_blank_string(self):
        assert not is_board_string("")
        assert not is_board_string("    ")
        assert not is_board_string("   \r\n ")


class Describe_is_pusher:

    def it_correctly_categorizes(self):
        assert is_pusher(BoardCharacters.PUSHER)
        assert is_pusher(BoardCharacters.ALT_PUSHER1)
        assert is_pusher(BoardCharacters.ALT_PUSHER2)
        assert is_pusher(BoardCharacters.PUSHER_ON_GOAL)
        assert is_pusher(BoardCharacters.ALT_PUSHER_ON_GOAL1)
        assert is_pusher(BoardCharacters.ALT_PUSHER_ON_GOAL2)


class Describe_is_box:

    def it_correctly_categorizes(self):
        assert is_box(BoardCharacters.BOX)
        assert is_box(BoardCharacters.ALT_BOX1)
        assert is_box(BoardCharacters.BOX_ON_GOAL)
        assert is_box(BoardCharacters.ALT_BOX_ON_GOAL1)


class Describe_is_goal:

    def it_correctly_categorizes(self):
        assert is_goal(BoardCharacters.GOAL)
        assert is_goal(BoardCharacters.ALT_GOAL1)
        assert is_goal(BoardCharacters.PUSHER_ON_GOAL)
        assert is_goal(BoardCharacters.ALT_PUSHER_ON_GOAL1)
        assert is_goal(BoardCharacters.ALT_PUSHER_ON_GOAL2)
        assert is_goal(BoardCharacters.BOX_ON_GOAL)
        assert is_goal(BoardCharacters.ALT_BOX_ON_GOAL1)


class Describe_is_empty_floor:

    def it_correctly_categorizes(self):
        assert is_empty_floor(BoardCharacters.FLOOR)
        assert is_empty_floor(BoardCharacters.VISIBLE_FLOOR)
        assert is_empty_floor(BoardCharacters.ALT_VISIBLE_FLOOR1)


class Describe_is_wall:

    def it_correctly_categorizes(self):
        assert is_wall(BoardCharacters.WALL)


class Describe_parse_board_string:

    def it_parses_regular_board(self):
        src = " ##########\n    \n" +\
              " ## @ *   #\n" +\
              "##  $ ####\n" +\
              "# $.+ #\n" +\
              "#######\n"
        result = [
            " ##########",
            "           ",
            " ## @ *   #",
            "##  $ #### ",
            "# $.+ #    ",
            "#######    ",
            "           ",
        ]
        parsed = parse_board_string(src)
        assert parsed == result

    def it_parses_RLE_board(self):
        src = " ##########   |" +\
              " ## @ *   #|" +\
              "##  $ ####|" +\
              "# $.+ #|||" +\
              "#######   |"
        result = [
            " ##########   ",
            " ## @ *   #   ",
            "##  $ ####    ",
            "# $.+ #       ",
            "              ",
            "              ",
            "#######       ",
            "              ",
        ]
        parsed = parse_board_string(src)
        assert parsed == result

    def it_raises_on_illegal_characters(self):
        src = " ##########\n\n" +\
              " ##       #\n" +\
              "##   z####\n" +\
              "#   a #\n" +\
              "#######\n"
        with pytest.raises(BoardConversionError):
            parse_board_string(src)

    def it_discards_empty_but_not_blank_lines(self):
        src = " ##########\n    \n\n" +\
              " ## @ *   #\n\n" +\
              "##  $ ####\n\n" +\
              "# $.+ #\n\n" +\
              "#######\n\n"
        result = [
            " ##########",
            "           ",
            "           ",
            " ## @ *   #",
            "           ",
            "##  $ #### ",
            "           ",
            "# $.+ #    ",
            "           ",
            "#######    ",
            "           ",
            "           ",
        ]
        parsed = parse_board_string(src)
        assert parsed == result

    def it_discards_blank_boards(self):
        src = "              "
        parsed = parse_board_string(src)
        assert parsed == []
