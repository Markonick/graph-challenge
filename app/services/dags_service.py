from abc import ABC
from dataclasses import dataclass
import random
from typing import List, Tuple
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import asyncio
import concurrent.futures
import time
import datetime

IS_ACYCLIC = [
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

    def get_cycle(self, graph: List[Tuple]) -> Tuple[bool, List[List], ]:
        is_acyclic = self.is_acyclic_graph(graph)
        result = None
        if not is_acyclic:
            nx_graph = nx.DiGraph(graph)
            for cycle in nx.simple_cycles(nx_graph):
                return is_acyclic, cycle

    def generate_directed_graph(self, number_of_nodes: int, is_acyclic: bool) -> List[Tuple]: 
        G = nx.gnp_random_graph(number_of_nodes, 1, directed=True)

        if is_acyclic:
            result = nx.DiGraph([(u, v, {'weight':random.randint(0,10)}) for (u, v) in G.edges() if u < v])
        else:
            result = nx.DiGraph([(u, v, {'weight':random.randint(0,10)}) for (u, v) in G.edges() if u > v])
        return result

    def generate_graphs(self, number_of_graphs: int, number_of_nodes: int) -> List[List[Tuple]]:
        with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
            graphs = []
            args = [(number_of_nodes, IS_ACYCLIC[i]) for i in range(number_of_graphs)]
            for i, graph in enumerate(executor.map(self.generate_directed_graph, *zip(*args))):
                graphs.append((graph, IS_ACYCLIC[i]))
            
            return graphs
    
    def draw_graphs(self, rows: int, columns: int, number_of_nodes: int) -> None:
        start = time.time()
        fig, axes = plt.subplots(nrows=rows, ncols=columns, figsize=(20, 30))
        graphs = self.generate_graphs(number_of_graphs=rows*columns, number_of_nodes=number_of_nodes)
        pdf_file_name = "graphs_plot.pdf"
      
        with PdfPages(pdf_file_name) as pdf:
            for r in range(rows):
                for c in range(columns):
                    index = r*(columns) + c
                    is_acyclic = graphs[index][1]
                    color = 'k' if is_acyclic else 'r'
                    font_color = 'w' if is_acyclic else 'k'
                    print(color)
                    colors = {"node_color": color, "edge_color" : color, "font_color": font_color}
                    nx.draw_networkx(graphs[index][0], ax=axes[r, c], **colors)
            pdf.savefig( fig )
        end = time.time()
        print(end - start)
