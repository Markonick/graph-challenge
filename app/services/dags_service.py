from abc import ABC
from dataclasses import dataclass
import random
from typing import List, Tuple
import networkx as nx
import asyncio
import concurrent.futures

IS_CYCLIC = [
    False, True, True, False, False, True, False, False, False, True, 
    True, True, False, False, True, False, True, True, False, True, 
    True, False, True, False, True, False, True, False, True, False, 
    True, True, False, True, False, True, False, True, False, False, 
    False, True, True, False, False, False, True, False, True, True, 
    True, True, True, True, True, True, False, True, True, False, 
    False, True, False, False, True, False, False, True, False, True, 
    False, True, False, True, False, True, False, False, True, True, 
    True, True, False, True, True, True, True, False, False, False, 
    True, True, True, False, False, True, True, True, False, True, 
]

@dataclass
class Dag:
    graph: List[Tuple]

class DagsService:
    def __init__(self, ):
        self._graph = nx.DiGraph()

    def is_acyclic_graph(self, graph: List[Tuple]) -> bool:
        self._graph.add_edges_from(graph)
        return nx.is_directed_acyclic_graph(self._graph)

    def generate_directed_graph(self, acyclic: bool) -> List[Tuple]: 
        G = nx.gnp_random_graph(10, 0.5, directed=True)
        if acyclic:
            result = nx.DiGraph([(u,v, {'weight':random.randint(-10,10)}) for (u,v) in G.edges() if u<v])
        else:
            result = nx.DiGraph([(u,v, {'weight':random.randint(-10,10)}) for (u,v) in G.edges() if u>v])
        return list(result)

    def generate_dags(self, n: int) -> List[List[Tuple]]: 
        with concurrent.futures.ProcessPoolExecutor() as executor:
            graphs = []
            count = 0
            for result in executor.map(self.generate_directed_graph, [True]):
                graphs.append(result)
                print(count)
                count += 1
            return graphs