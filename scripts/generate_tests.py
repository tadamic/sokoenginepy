#!/usr/bin/env python

from unipath import Path
from collections import OrderedDict
from pyexcel_ods3 import get_data
from inspect import getsourcefile
from os.path import abspath

# Directory where this file is found

basedir = Path(abspath(getsourcefile(lambda: 0))).ancestor(1)
SOURCE_ROOT = basedir.ancestor(1)
RES_DIR = SOURCE_ROOT.child('res')
TEST_CASES_DIR = RES_DIR.child('test_cases')
TESTS_DIR = SOURCE_ROOT.child('tests')
VARIANT_TESTS_DIR = TESTS_DIR.child('variant')


class SpecGenerator(object):

    VARIANTS = ['sokoban', 'trioban', 'hexoban', 'octoban']
    TEST_TYPES = ['board', 'tessellation']

    DIRECTIONS = ['l', 'r', 'u', 'd', 'nw', 'sw', 'ne', 'se']
    DIRECTIONS_HASH = dict(zip(
        DIRECTIONS,
        ["Direction.LEFT", "Direction.RIGHT", "Direction.UP",
         "Direction.DOWN", "Direction.NORTH_WEST", "Direction.SOUTH_WEST",
         "Direction.NORTH_EAST", "Direction.SOUTH_EAST"]
    ))
    RESULTS_HASH = dict(zip(
        DIRECTIONS,
        ["result_{0}".format(d) for d in DIRECTIONS]
    ))

    def generate(self):
        self.write_header()

        for variant in type(self).VARIANTS:
            print('Generating test cases for {0}...'.format(variant))
            test_cases = self.get_test_cases(variant)

            for test_type in self.TEST_TYPES:
                self.output = []
                self.generate_test_class(variant, test_type)
                for test_case in test_cases:
                    test_case['test_type'] = test_type
                    self.generate_test_case_output(test_case)

                with open(str(self.output_file_path()), 'a') as f:
                    for line in self.output:
                        f.write(line)
                    f.write("\n")

    def write_header(self):
        with open(str(self.output_file_path()), 'w') as f:
            f.write("# Generated by generate_tests.py usind data from res/test_cases\n\n")
            f.write("import pytest\n")
            f.write("from hamcrest import assert_that, equal_to\n")
            f.write("from sokoengine.variant.tessellation import Tessellation, INDEX, on_board_1D\n")
            f.write("from sokoengine import IllegalDirectionError\n")
            f.write("from sokoengine import CellOrientation, Direction\n\n\n")

            f.write("def triangle_points_down(position, board_width, board_height):\n")
            f.write("    return Tessellation.factory('trioban').cell_orientation(\n")
            f.write("        position, board_width, board_height\n")
            f.write("    ) == CellOrientation.TRIANGLE_DOWN\n\n")

            f.write("def is_octagon(position, board_width, board_height):\n")
            f.write("    return Tessellation.factory('octoban').cell_orientation(\n")
            f.write("        position, board_width, board_height\n")
            f.write("    ) == CellOrientation.OCTAGON\n\n\n")

    def get_test_cases(self, variant):
        data = get_data(str(self.input_file_path(variant)))
        sheet1 = data[list(data.keys())[0]]
        rows = [
            row[:12] for row in sheet1
            if len(row) > 0 and len(row[0]) > 0
        ]
        header = rows[0]
        raw_cases = [OrderedDict(zip(header, row)) for row in rows[1:]]

        cases = []
        for case in raw_cases:
            case['variant'] = variant
            case['width'] = int(case['board_dimensions'].split(',')[0].strip())
            case['height'] = int(case['board_dimensions'].split(',')[1].strip())
            case['row'] = int(case['test_position'].split(',')[1].strip())
            case['column'] = int(case['test_position'].split(',')[0].strip())
            cases.append(case)

        return cases

    def generate_test_class(self, variant, test_type):
        self.output.append("class {0}{1}AutogeneratedSpecMixin(object):\n".format(variant.capitalize(), test_type.capitalize()))
        self.output.append('    class Describe_neighbor_position(object):\n')
        self.output.append('\n')

    def generate_test_case_output(self, test_case):
        self.output.append('        def test_autogenerated_{0}(self):\n'.format(test_case['test_name']))
        self.output.append('            width = {0}\n'.format(test_case['width']))
        self.output.append('            height = {0}\n'.format(test_case['height']))
        self.output.append('            row = {0}\n'.format(test_case['row']))
        self.output.append('            column = {0}\n'.format(test_case['column']))
        self.output.append('            index = INDEX(column, row, width)\n')

        if test_case['test_type'] == 'tessellation':
            self.output.append('            t = Tessellation.factory("{0}")'.format(test_case['variant']))
        else:
            self.output.append('            b = {0}Board(width, height)'.format(test_case['variant'].capitalize()))
        self.output.append('\n')

        if test_case['test_position_requrement'] != 'nil':
            self.output.append('\n')
            self.output.append("            assert_that({0}, equal_to(True))".format(
                test_case['test_position_requrement'].replace(
                    "&&", "and"
                ).replace("||", "or").replace("!", "not ")
            ))
            self.output.append('\n\n')
        else:
            self.output.append('\n')

        for direction in self.DIRECTIONS:
            if test_case['test_type'] == 'tessellation':
                if self.is_result_illegal_position(test_case, direction):
                    self.output.append("            assert_that(not on_board_1D(\n")
                    self.output.append("                t.neighbor_position(index, {0}, width, height),\n".format(self.DIRECTIONS_HASH[direction]))
                    self.output.append("                width, height\n")
                    self.output.append("            ))\n")
                elif self.is_result_illegal_direction(test_case, direction):
                    self.output.append("            with pytest.raises(IllegalDirectionError):\n")
                    self.output.append("                t.neighbor_position(index, {0}, width, height)\n".format(self.DIRECTIONS_HASH[direction]))
                else:
                    self.output.append("            assert_that(\n")
                    self.output.append("                t.neighbor_position(index, {0}, width, height) == \n".format(self.DIRECTIONS_HASH[direction]))
                    self.output.append("                INDEX({0}, width)\n".format(test_case[self.RESULTS_HASH[direction]]))
                    self.output.append("            )\n")
            else:
                if (
                    self.is_result_illegal_position(test_case, direction) or
                    self.is_result_illegal_direction(test_case, direction)
                ):
                    self.output.append("            assert_that(not on_board_1D(\n")
                    self.output.append("                b.neighbor(index, {0}),\n".format(self.DIRECTIONS_HASH[direction]))
                    self.output.append("                width, height\n")
                    self.output.append("            ))\n")
                else:
                    self.output.append("            assert_that(\n")
                    self.output.append("                b.neighbor(index, {0}) == \n".format(self.DIRECTIONS_HASH[direction]))
                    self.output.append("                INDEX({0}, width)\n".format(test_case[self.RESULTS_HASH[direction]]))
                    self.output.append("            )\n")

        self.output.append('\n')

    def input_file_path(self, variant):
        return TEST_CASES_DIR.child(
            '{0}_test_cases.ods'.format(variant.strip().lower())
        )

    def output_file_path(self):
        return VARIANT_TESTS_DIR.child('autogenerated.py')

    def is_result_illegal_direction(self, test_case, direction):
        return test_case[self.RESULTS_HASH[direction]] == "IllegalDirection"

    def is_result_illegal_position(self, test_case, direction):
        return test_case[self.RESULTS_HASH[direction]] == "OfBoardPosition"


def main():
    generator = SpecGenerator()
    generator.generate()


if __name__ == "__main__":
    main()
