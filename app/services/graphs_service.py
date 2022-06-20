from abc import ABC
from dataclasses import dataclass
import math
import random
from typing import Any, List, Optional, Tuple
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import concurrent.futures
import time
import numpy as np

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


class GraphsService:
    def __init__(self, ):
        self._graph = nx.DiGraph()

    def is_acyclic_graph(self, graph: List[Tuple]) -> bool:
        """
        Method that is exposed to the api. Responsible for returning a boolean flag on 
        whether the input graph is acyclic (a DAG) or not. 
        Also called by get_cycle()
        """
        self._graph.add_edges_from(graph)
        return nx.is_directed_acyclic_graph(self._graph)

    def get_cycle(self, graph: List[Tuple]) -> Tuple[bool, List[List]]:
        """
         Method that is exposed to the api. Responsible for returning a boolean flag on 
        whether the input graph is acyclic (a DAG) or not + the actual cycle if found | None. 
        """
        is_acyclic = self.is_acyclic_graph(graph)
        cycle = None
        if not is_acyclic:
            nx_graph = nx.DiGraph(graph)
            for cycle in nx.simple_cycles(nx_graph):
                return is_acyclic, cycle
        return is_acyclic, cycle

    def _generate_random_generic_graph(self, number_of_nodes: int) -> Any:
        """
        Private method, responsible for generating a random graph.
        Called by _generate_dag()
        """
        p = 2 / number_of_nodes # twaked this ratio to get a reasonably visible graph by controlling the connections between nodes
        return nx.gnp_random_graph(n=number_of_nodes, p=p, seed=2, directed=True)

    def _generate_dag(self, number_of_nodes: int) -> Any:
        """
        Private method, responsible for generating an acyclic graph by applying random weights and making sure
        that the edges all point to the same direction (u > v).
        Called by _generate_directed_graph()
        """
        G = self._generate_random_generic_graph(number_of_nodes=number_of_nodes)
        result = nx.DiGraph([(u, v, {'weight':random.randint(0,10)}) for (u, v) in G.edges() if u > v])

        return result

    def _generate_cycle_graph(self, number_of_nodes: int) -> Any:
        """
        Private method, responsible for generating a cycle graph.
        Called by _generate_directed_graph()
        """
        G = self._generate_random_generic_graph(number_of_nodes=number_of_nodes)
        result = nx.DiGraph([(u, v, {'weight':random.randint(0,10)}) for (u, v) in G.edges()])
        return result
        

    def _generate_directed_graph(self, number_of_nodes: int, is_acyclic: bool) -> Any:
        """
        Private method, responsible for generating an acyclic or cycle graph.
        Called by generate_graphs()
        """
        if is_acyclic:
            result = self._generate_dag(number_of_nodes=number_of_nodes)
        else:
            result = self._generate_cycle_graph(number_of_nodes=number_of_nodes)
        return result

    def generate_graphs(
        self,
        acyclic_flags_list: List[bool],
        number_of_graphs: int,
        number_of_nodes: int,
        rows: Optional[int] = None,
        max_workers: Optional[int] = 1
    ) -> List[Tuple[bool, Any]]:
        """
        Method that is exposed to the api. Responsible for generating the graphs.
        Can be called by draw_graphs()
        """
        # with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as executor:
        #     futures = []
        #     graphs = []

        #     chunksize = math.floor(number_of_graphs/workers)
        #     args = []

        #     for i in range(workers):
        #         start = i*chunksize
        #         end = start + chunksize
        #         args.append([(number_of_nodes, acyclic_flags_list[i]) for i in range(start,end)])
        #         futures.append(
        #             executor.map(self._generate_directed_graph, *zip(*args[i]), chunksize=chunksize)
        #         )

        #     for i, future in enumerate(futures):
        #         for graph in future:
        #             edges = graph.edges()
        #             graphs.append(list(edges))
                    
        #     return list(zip(acyclic_flags_list, graphs))
            # return graphs

        # The following single threaded code takes the same time to execute as the ThreadPool counterpart 
        # of the ProcessPool solution above (without chunksize - not applicable to ThreadPoolExecutor), which
        # implies that this is not an I/O bound but rather a CPU bound process, however
        # ProcessPoolExecutor did exhibit far inferior performance and did not have time to look into this

        graphs = []
        for is_acyclic in acyclic_flags_list:
            graph = self._generate_directed_graph(number_of_nodes, is_acyclic)
            graphs.append((is_acyclic, list(graph.edges())))

        return graphs
        
    def draw_graphs(
        self,
        acyclic_flags_list: List[bool],
        rows: int,
        columns: int,
        number_of_nodes: int,
        file_path: str,
        max_workers: Optional[int] = 1,
        layout: Optional[str] = None
    ) -> List[Tuple[bool, Any]]:
        """
        Method that is exposed to the api. Responsible for drawing graphs to file
        """
        start = time.time()
        graphs = self.generate_graphs(
            acyclic_flags_list=acyclic_flags_list,
            number_of_graphs=rows*columns,
            number_of_nodes=number_of_nodes,
            max_workers=max_workers
        )
        
        pdf_file_path = file_path
        with PdfPages(pdf_file_path) as pdf:
    #         workers = 25
    #         with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as executor:
    #             futures = []
    #             chunksize = math.floor((rows*columns)/workers)
    #             args = []
               
    #             for r in range(rows):
    #                 start = r*chunksize
    #                 end = start + chunksize
    #                 args = (acyclic_flags_list[start:end], columns, graphs[start:end], pdf)
    #                 futures.append(
    #                     executor.map(self.draw_rows, args, chunksize=chunksize)
    #                 )

    #             for i, future in enumerate(futures):
    #                 for k in future:
    #                     print(k.result())

    #     end = time.time()
    #     print(end - start)
    #     return graphs
   
            for r in range(rows):
                fig, axes = plt.subplots(nrows=1, ncols=columns, figsize=(20, 20))

                if type(axes) != np.ndarray:
                    axes = [axes]
                    
                for c in range(columns):
                    index = r*(columns) + c
                    is_acyclic = acyclic_flags_list[index]
                    color = 'r' if is_acyclic else 'k'
                    font_color = 'k' if is_acyclic else 'w'
                    colors = {"node_color": color, "edge_color" : color, "font_color": font_color}
                    G = graphs[index][1]
                    pos = nx.spectral_layout(G)
                    nx.draw_networkx(nx.DiGraph(G), ax=axes[c],  **colors)
                    plt.close(fig) # Close figure on each row to not get Memory warning for too many figs open!
                pdf.savefig(fig)

                # for c in range(columns):
                #     index = r*(columns) + c
                #     is_acyclic = acyclic_flags_list[index]
                #     color = 'r' if is_acyclic else 'k'
                #     font_color = 'k' if is_acyclic else 'w'
                #     colors = {"node_color": color, "edge_color" : color, "font_color": font_color, "alpha":0.7}
                            
                #     G = graphs[index][1]
                #     G = nx.DiGraph(G)
                #     pos = None

                #     if layout:
                #         graph_layout = getattr(nx, layout)
                #         pos = graph_layout(G)
                            
                #     nx.draw_networkx(G, ax=axes[c], **colors)
                #     plt.close(fig) # Close figure on each row to not get Memory warning for too many figs open!
                # pdf.savefig(fig)

        end = time.time()
        print(end - start)

        return graphs