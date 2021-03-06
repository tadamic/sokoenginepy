from itertools import permutations

import pytest

from sokoenginepy import (BoardCell, BoardCellCharacters, BoardGraph,
                          Direction, GraphType, SokobanBoard, Tessellation)
from sokoenginepy.utilities import index_1d


class DescribeBoardGraph:
    class describe_getitem:
        def it_returns_board_cell_on_position(self, board_graph):
            assert isinstance(board_graph[0], BoardCell)

        def it_raises_IndexError_for_illegal_position(self, board_graph):
            with pytest.raises(IndexError):
                board_graph[42000]

    class describe_setitem:
        def it_sets_board_cell_on_position(self, board_graph):
            board_graph[0].is_in_playable_area = True
            board_graph[0].is_deadlock = True
            board_graph[0].is_wall = True

            bc = BoardCell(BoardCellCharacters.PUSHER)
            bc.is_in_playable_area = False
            bc.is_deadlock = False

            board_graph[0] = bc

            assert not board_graph[0].is_wall
            assert board_graph[0].has_pusher
            assert not board_graph[0].is_in_playable_area
            assert not board_graph[0].is_deadlock

    class describe_contains:
        def it_detects_if_position_is_in_graph(self, board_graph):
            assert 0 in board_graph
            assert 42000 not in board_graph

    class describe_vertices_count:
        def it_returns_number_of_graph_vertices(
            self, board_graph, board_width, board_height
        ):
            assert board_graph.vertices_count == board_width * board_height

    class describe_edges_count:
        def it_returns_number_of_graph_edges(self, board_graph):
            assert board_graph.edges_count == 776

    class describe_has_edge:
        def it_returs_true_if_edge_in_given_direction_exists(
            self, board_graph
        ):
            assert board_graph.has_edge(0, 1, Direction.RIGHT)

        def it_returns_false_if_there_is_no_edge_in_given_direction(
            self, board_graph
        ):
            assert not board_graph.has_edge(0, 1, Direction.LEFT)

        def it_returns_false_if_any_of_parameter_vertices_are_off_board(
            self, board_graph
        ):
            assert not board_graph.has_edge(42000, 1, Direction.LEFT)
            assert not board_graph.has_edge(0, 42000, Direction.LEFT)
            assert not board_graph.has_edge(24000, 42000, Direction.LEFT)

    class describe_out_edges_count:
        def it_returns_number_of_edges_going_from_source_to_target_vertex(
            self, board_graph
        ):
            assert board_graph.out_edges_count(0, 1) == 1

        def it_returns_zero_if_any_of_parameter_vertices_are_off_board(
            self, board_graph
        ):
            assert board_graph.out_edges_count(42000, 1) == 0
            assert board_graph.out_edges_count(0, 42000) == 0
            assert board_graph.out_edges_count(24000, 42000) == 0

    class describe_remove_all_edges:
        def it_removes_all_eges_from_graph(self, board_graph):
            board_graph.remove_all_edges()
            assert board_graph.edges_count == 0

    class describe_add_edge:
        def it_adds_edge_between_two_vertices(self, board_graph):
            board_graph.remove_all_edges()
            board_graph.add_edge(0, 1, Direction.LEFT)
            assert board_graph.edges_count == 1
            assert board_graph.has_edge(0, 1, Direction.LEFT)

        def it_raises_IndexError_if_any_of_vertices_if_off_board(
            self, board_graph
        ):
            board_graph.remove_all_edges()

            with pytest.raises(IndexError):
                board_graph.add_edge(42000, 1, Direction.LEFT)
            with pytest.raises(IndexError):
                board_graph.add_edge(0, 42000, Direction.LEFT)
            with pytest.raises(IndexError):
                board_graph.add_edge(42000, 42000, Direction.LEFT)

        def it_allows_adding_duplicate_edges(self):
            board_graph = BoardGraph(2, 2, GraphType.DIRECTED)
            board_graph.add_edge(0, 1, Direction.LEFT)
            board_graph.add_edge(0, 1, Direction.LEFT)
            assert board_graph.edges_count == 1
            assert board_graph.has_edge(0, 1, Direction.LEFT)

            board_graph = BoardGraph(2, 2, GraphType.DIRECTED_MULTI)
            board_graph.add_edge(0, 1, Direction.LEFT)
            board_graph.add_edge(0, 1, Direction.LEFT)
            assert board_graph.edges_count == 2
            assert board_graph.has_edge(0, 1, Direction.LEFT)

    class describe_out_edge_weight:
        def it_returns_max_weigth_for_wall_cell_target(self, board_graph):
            board_graph[1].is_wall = True
            if Direction.__module__.startswith('sokoenginepy.'):
                assert board_graph.out_edge_weight(
                    1
                ) > len(Direction)
            else:
                assert board_graph.out_edge_weight(
                    1
                ) > Direction.__len__()

        def it_returns_max_weigth_for_pusher_cell_target(self, board_graph):
            board_graph[1].has_pusher = True
            if Direction.__module__.startswith('sokoenginepy.'):
                assert board_graph.out_edge_weight(
                    1
                ) > len(Direction)
            else:
                assert board_graph.out_edge_weight(
                    1
                ) > Direction.__len__()

        def it_returns_max_weigth_for_box_cell_target(self, board_graph):
            board_graph[1].has_box = True
            if Direction.__module__.startswith('sokoenginepy.'):
                assert board_graph.out_edge_weight(
                    1
                ) > len(Direction)
            else:
                assert board_graph.out_edge_weight(
                    1
                ) > Direction.__len__()

        def it_returns_one_for_other_cells(self, board_graph):
            board_graph[1].clear()
            assert board_graph.out_edge_weight(1) == 1
            board_graph[1].has_goal = True
            assert board_graph.out_edge_weight(1) == 1

        def it_raises_IndexError_for_off_board_target_positions(
            self, board_graph
        ):
            with pytest.raises(IndexError):
                board_graph.out_edge_weight(42000)

    class describe_neighbor:
        def it_returns_neighbor_position_in_given_direction(self, board_graph):
            assert board_graph.neighbor(0, Direction.RIGHT) == 1

        def it_returns_none_for_off_board_direction(self, board_graph):
            assert board_graph.neighbor(0, Direction.UP) is None

        def it_raises_IndexError_for_off_board_source_position(
            self, board_graph
        ):
            with pytest.raises(IndexError):
                board_graph.neighbor(42000, Direction.UP)

    class describe_wall_neighbors:
        def it_returns_positons_of_walls_for_given_vertice(self):
            board_str = "\n".join([
                # 123456
                "#######",  # 0
                "#.$# @#",  # 1
                "#######",  # 2
            ])
            board_graph = SokobanBoard(board_str=board_str).graph
            wall_neighbors = board_graph.wall_neighbors(0)
            assert index_1d(0, 1, 7) in wall_neighbors
            assert index_1d(1, 0, 7) in wall_neighbors

        def it_raises_IndexError_for_off_board_source_position(
            self, board_graph
        ):
            with pytest.raises(IndexError):
                board_graph.wall_neighbors(42000)

    class describe_all_neighbors:
        def it_returns_positions_of_all_neghbor_vertices_for_given_vertice(
            self, board_graph, board_width
        ):
            all_neighbors = board_graph.all_neighbors(0)
            assert index_1d(0, 1, board_width) in all_neighbors
            assert index_1d(1, 1, board_width) not in all_neighbors
            assert index_1d(1, 0, board_width) in all_neighbors

        def it_raises_IndexError_for_off_board_source_position(
            self, board_graph
        ):
            with pytest.raises(IndexError):
                board_graph.all_neighbors(42000)

    class describe_shortest_path:
        def it_raises_IndexError_for_off_board_paramteres(self, board_graph):
            with pytest.raises(IndexError):
                board_graph.shortest_path(42000, 0)
            with pytest.raises(IndexError):
                board_graph.shortest_path(0, 42000)
            with pytest.raises(IndexError):
                board_graph.shortest_path(42000, 42000)

    class describe_djikstra_path:
        def it_raises_IndexError_for_off_board_paramteres(self, board_graph):
            with pytest.raises(IndexError):
                board_graph.dijkstra_path(42000, 0)
            with pytest.raises(IndexError):
                board_graph.dijkstra_path(0, 42000)
            with pytest.raises(IndexError):
                board_graph.dijkstra_path(42000, 42000)

    class describe_find_jump_path:
        def it_returns_sequence_of_positions_defining_shortest_path_for_pusher_jump(
            self, board_graph, board_width
        ):
            start_position = index_1d(11, 8, board_width)
            end_position = index_1d(8, 5, board_width)
            expected = board_graph.positions_path_to_directions_path(
                board_graph.find_jump_path(start_position, end_position)
            )

            assert tuple(expected) in permutations([
                Direction.UP,
                Direction.UP,
                Direction.UP,
                Direction.LEFT,
                Direction.LEFT,
                Direction.LEFT,
            ])

        def it_raises_IndexError_for_off_board_paramteres(self, board_graph):
            with pytest.raises(IndexError):
                board_graph.shortest_path(42000, 0)
            with pytest.raises(IndexError):
                board_graph.shortest_path(0, 42000)
            with pytest.raises(IndexError):
                board_graph.shortest_path(42000, 42000)

    class describe_find_move_path:
        def it_returns_sequence_of_positions_defining_shortest_path_for_pusher_movement_without_pushing_boxes(
            self, board_graph, board_width
        ):
            start_position = index_1d(11, 8, board_width)
            end_position = index_1d(8, 5, board_width)
            expected = board_graph.positions_path_to_directions_path(
                board_graph.find_move_path(start_position, end_position)
            )

            assert tuple(expected) in permutations([
                Direction.LEFT,
                Direction.LEFT,
                Direction.LEFT,
                Direction.UP,
                Direction.UP,
                Direction.UP,
            ])

        def it_raises_IndexError_for_off_board_paramteres(self, board_graph):
            with pytest.raises(IndexError):
                board_graph.shortest_path(42000, 0)
            with pytest.raises(IndexError):
                board_graph.shortest_path(0, 42000)
            with pytest.raises(IndexError):
                board_graph.shortest_path(42000, 42000)

        def it_returns_empty_sequence_if_movement_is_blocked(
            self, board_graph, board_width
        ):
            assert board_graph.find_move_path(index_1d(11, 8, board_width),
                                              0) == []

    class describe_positions_path_to_directions_path:
        def it_converts_path(
            self, board_graph, positions_path, directions_path
        ):
            calculated_directions_path = board_graph.positions_path_to_directions_path(
                positions_path
            )
            assert calculated_directions_path == directions_path

        def it_raises_IndexError_if_path_has_off_board_positions(
            self, board_graph, board_width
        ):
            path = [index_1d(-1, -1, board_width)]
            with pytest.raises(IndexError):
                board_graph.positions_path_to_directions_path(path)

            path = [index_1d(0, 0, board_width), index_1d(-1, -1, board_width)]
            with pytest.raises(IndexError):
                board_graph.positions_path_to_directions_path(path)

        def it_returns_empty_path_if_source_path_is_to_short(
            self, board_graph
        ):
            assert board_graph.positions_path_to_directions_path([]) == []
            assert board_graph.positions_path_to_directions_path([1]) == []

    class describe_mark_play_area:
        board_str = "\n".join([
            # 123456
            "#######",  # 0
            "#.$# @#",  # 1
            "#######",  # 2
            "#     #",  # 3
            "#######",  # 4
        ])
        board_graph = SokobanBoard(board_str=board_str).graph

        expected_playable_cells = [
            index_1d(1, 1, 7),
            index_1d(2, 1, 7),
            index_1d(4, 1, 7),
            index_1d(5, 1, 7),
        ]

        def it_calculates_playable_area_of_board_marking_all_playable_cells(
            self
        ):
            self.board_graph.mark_play_area()
            for pos in range(self.board_graph.vertices_count):
                if pos in self.expected_playable_cells:
                    assert self.board_graph[pos].is_in_playable_area
                else:
                    assert not self.board_graph[pos].is_in_playable_area

    class describe_positions_reachable_by_pusher:
        board_str = "\n".join([
            # 123456
            "#######",  # 0
            "#.$  @#",  # 1
            "# # ###",  # 2
            "#   #  ",  # 3
            "#####  ",  # 4
        ])
        board_graph = SokobanBoard(board_str=board_str).graph

        def it_returns_list_of_positions_reachable_by_pusher_movement_only(
            self
        ):
            expected = [
                index_1d(5, 1, 7),
                index_1d(4, 1, 7),
                index_1d(3, 1, 7),
                index_1d(3, 2, 7),
                index_1d(3, 3, 7),
                index_1d(2, 3, 7),
                index_1d(1, 3, 7),
                index_1d(1, 2, 7),
                index_1d(1, 1, 7),
            ]
            assert self.board_graph.positions_reachable_by_pusher(
                pusher_position=index_1d(5, 1, 7)
            ) == expected

        def it_doesnt_require_that_start_position_actually_contain_pusher(
            self
        ):
            expected = [
                index_1d(4, 1, 7),
                index_1d(3, 1, 7),
                index_1d(3, 2, 7),
                index_1d(3, 3, 7),
                index_1d(2, 3, 7),
                index_1d(1, 3, 7),
                index_1d(1, 2, 7),
                index_1d(1, 1, 7),
            ]
            assert self.board_graph.positions_reachable_by_pusher(
                pusher_position=index_1d(4, 1, 7)
            ) == expected

        def it_can_exclude_some_positions(self):
            expected = [
                index_1d(5, 1, 7),
                index_1d(4, 1, 7),
                index_1d(3, 1, 7),
                index_1d(3, 2, 7),
            ]
            excluded = [
                index_1d(3, 3, 7),
                index_1d(2, 3, 7),
                index_1d(1, 3, 7),
                index_1d(1, 2, 7),
                index_1d(1, 1, 7),
            ]
            assert self.board_graph.positions_reachable_by_pusher(
                pusher_position=index_1d(5, 1, 7), excluded_positions=excluded
            ) == expected

        def it_raises_if_start_position_is_of_board(self):
            with pytest.raises(IndexError):
                self.board_graph.positions_reachable_by_pusher(42000)

    class describe_normalized_pusher_position:
        board_str = "\n".join([
            # 123456
            "#######",  # 0
            "#.$  @#",  # 1
            "# # ###",  # 2
            "#   #  ",  # 3
            "#####  ",  # 4
        ])
        board_graph = SokobanBoard(board_str=board_str).graph

        def it_returns_top_left_position_of_pusher_in_his_reachable_area(self):
            assert self.board_graph.normalized_pusher_position(
                pusher_position=index_1d(5, 1, 7)
            ) == index_1d(1, 1, 7)

        def it_doesnt_require_that_start_position_actually_contain_pusher(
            self
        ):
            assert self.board_graph.normalized_pusher_position(
                pusher_position=index_1d(4, 1, 7)
            ) == index_1d(1, 1, 7)

        def it_can_exclude_some_positions(self):
            assert self.board_graph.normalized_pusher_position(
                pusher_position=index_1d(4, 1, 7),
                excluded_positions=[index_1d(1, 1, 7)]
            ) == index_1d(3, 1, 7)

        def it_raises_if_start_position_is_of_board(self):
            with pytest.raises(IndexError):
                self.board_graph.normalized_pusher_position(42000)

    class describe_path_destination:
        def it_calculates_destination_position_from_source_and_directions_path(
            self, board_graph, board_width
        ):
            directions_path = [Direction.UP, Direction.RIGHT]
            start_position = index_1d(11, 8, board_width)
            assert board_graph.path_destination(
                start_position, directions_path
            ) == index_1d(12, 7, board_width)

        def it_silently_stops_search_on_first_off_board_position(
            self, board_graph, board_width
        ):
            directions_path = [Direction.DOWN, Direction.DOWN, Direction.DOWN]
            start_position = index_1d(11, 8, board_width)
            assert board_graph.path_destination(
                start_position, directions_path
            ) == index_1d(11, 10, board_width)

        def it_silently_stops_search_on_illegal_direction(
            self, board_graph, board_width
        ):
            directions_path = [Direction.DOWN, Direction.NORTH_WEST]
            start_position = index_1d(11, 8, board_width)
            assert board_graph.path_destination(
                start_position, directions_path
            ) == index_1d(11, 9, board_width)

        def it_raises_if_start_position_is_of_board(self, board_graph):
            with pytest.raises(IndexError):
                board_graph.path_destination(42000, []),

    class describe__reachables:
        board_str = "\n".join([
            # 123456
            "#######",  # 0
            "#.$# @#",  # 1
            "#######",  # 2
            "#     #",  # 3
            "#######",  # 4
        ])
        board_graph = SokobanBoard(board_str=board_str).graph

        def it_calculates_all_positions_reachable_from_root(self):
            if not hasattr(self.board_graph, '_reachables'):
                return

            root = index_1d(5, 1, 7)
            assert self.board_graph._reachables(root) == [
                root, index_1d(4, 1, 7)
            ]

        def it_skips_explicitly_excluded_positions(self):
            if not hasattr(self.board_graph, '_reachables'):
                return

            root = index_1d(5, 1, 7)
            assert self.board_graph._reachables(
                root, excluded_positions=[root]
            ) == [index_1d(4, 1, 7)]
            root = index_1d(5, 1, 7)
            assert self.board_graph._reachables(
                root, excluded_positions=[index_1d(4, 1, 7)]
            ) == [root]

    class describe_reconfigure_edges:
        def it_reconfigures_all_edges_in_board(self):
            graph = BoardGraph(2, 2, GraphType.DIRECTED)
            graph.reconfigure_edges(Tessellation.SOKOBAN.value)

            assert graph.edges_count == 8
            assert graph.has_edge(0, 1, Direction.RIGHT)
            assert graph.has_edge(1, 0, Direction.LEFT)
            assert graph.has_edge(0, 2, Direction.DOWN)
            assert graph.has_edge(2, 0, Direction.UP)
            assert graph.has_edge(2, 3, Direction.RIGHT)
            assert graph.has_edge(3, 2, Direction.LEFT)
            assert graph.has_edge(1, 3, Direction.DOWN)
            assert graph.has_edge(3, 1, Direction.UP)

        def it_doesnt_create_duplicate_direction_edges_in_multidigraph(self):
            graph = BoardGraph(2, 2, GraphType.DIRECTED_MULTI)
            graph.reconfigure_edges(Tessellation.TRIOBAN.value)
            assert graph.out_edges_count(0, 1) == 2
            assert graph.out_edges_count(1, 0) == 2
