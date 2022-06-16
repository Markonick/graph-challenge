from abc import ABC
from typing import List, Tuple
import networkx as nx


class DagsService:
    def __init__(self, ):
        self._graph = nx.DiGraph()

    def is_acyclic_graph(self, graph: List[Tuple]) -> bool:
        self._graph.add_edges_from(graph)
        return nx.is_directed_acyclic_graph(self._graph)