try:
    from graph_tool import Graph
    from .board_graph_graphtool import BoardGraphGraphtool as BoardGraph
except ImportError:
    from .board_graph_networkx import BoardGraphNetworkx as BoardGraph

from .graph_type import GraphType
