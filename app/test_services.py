from dataclasses import dataclass
import dataclasses
import json
import os
from typing import List, Tuple
import pytest

from services.graphs_service import GraphsService
from shared.types_common import AifiDagsRequest

@pytest.fixture
def dag_input() -> List[Tuple]:
    graph = [
        [1, 2],
        [2, 3],
        [3, 4],
        [4, 5],
    ]

    return AifiDagsRequest(graph=graph, )

@pytest.fixture
def cyclic_graph_input() -> List[Tuple]:
    graph = [
        ["A", "B"],
        ["B", "A"],
        ["C", "D"],
        ["D", "B"],
        ["D", "C"],
        ["C", "D"]
    ]

    return AifiDagsRequest(graph=graph, )

@pytest.fixture
def get_2_acyclic_graphs_request() -> List[List[Tuple]]:
    return AifiDagsRequest(acyclic_flags_list=[True, True], number_of_graphs=2, number_of_nodes=10)

@pytest.fixture
def get_2_cyclic_graphs_request() -> List[List[Tuple]]:
    return AifiDagsRequest(acyclic_flags_list=[False, False], number_of_graphs=2, number_of_nodes=10)

@pytest.fixture
def get_2_mixed_graphs_request() -> List[List[Tuple]]:
    return AifiDagsRequest(acyclic_flags_list=[False, True], number_of_graphs=2, number_of_nodes=10)

def graphs_svc():
    return GraphsService()

def test_graph_should_be_acyclic(dag_input: AifiDagsRequest):
    is_acyclic = graphs_svc().is_acyclic_graph(graph=dag_input.graph)

    assert is_acyclic == True

def test_graph_should_not_be_acyclic(cyclic_graph_input: AifiDagsRequest):
    is_acyclic = graphs_svc().is_acyclic_graph(graph=cyclic_graph_input.graph)

    assert is_acyclic == False

def test_passing_a_cyclic_graph_should_return_cycle(cyclic_graph_input: AifiDagsRequest):
    is_acyclic, cycle = graphs_svc().get_cycle(graph=cyclic_graph_input.graph)

    assert is_acyclic == False
    assert sorted(cycle) == ["C", "D"]

def test_passing_a_dag_graph_should_return_null_cycle(dag_input: AifiDagsRequest):
    is_acyclic, cycle = graphs_svc().get_cycle(graph=dag_input.graph)

    assert is_acyclic == True
    assert cycle == None

def test_service_returns_2_acyclic_graphs(get_2_acyclic_graphs_request: AifiDagsRequest):
    graphs = graphs_svc().generate_graphs(
         acyclic_flags_list=get_2_acyclic_graphs_request.acyclic_flags_list,
         number_of_graphs=get_2_acyclic_graphs_request.number_of_graphs, 
         number_of_nodes=get_2_acyclic_graphs_request.number_of_nodes,
    )
    assert len(graphs) == 2

    first_graph_is_acyclic = graphs_svc().is_acyclic_graph(graph=graphs[0][1])
    second_graph_is_acyclic = graphs_svc().is_acyclic_graph(graph=graphs[1][1])

    print(graphs[0][1])
    assert first_graph_is_acyclic == True
    assert second_graph_is_acyclic == True

def test_service_returns_2_cyclic_graphs(get_2_cyclic_graphs_request: AifiDagsRequest):
    graphs = graphs_svc().generate_graphs(
         acyclic_flags_list=get_2_cyclic_graphs_request.acyclic_flags_list,
         number_of_graphs=get_2_cyclic_graphs_request.number_of_graphs, 
         number_of_nodes=get_2_cyclic_graphs_request.number_of_nodes,
    )

    assert len(graphs) == 2
    
    first_graph_is_acyclic = graphs_svc().is_acyclic_graph(graph=graphs[0][1])
    second_graph_is_acyclic = graphs_svc().is_acyclic_graph(graph=graphs[1][1])

    print(graphs[0][1])
    assert first_graph_is_acyclic == False
    assert second_graph_is_acyclic == False

def test_service_returns_1_cyclic_1_acyclic_graphs(get_2_mixed_graphs_request: AifiDagsRequest):
    graphs = graphs_svc().generate_graphs(
         acyclic_flags_list=get_2_mixed_graphs_request.acyclic_flags_list,
         number_of_graphs=get_2_mixed_graphs_request.number_of_graphs, 
         number_of_nodes=get_2_mixed_graphs_request.number_of_nodes,
    )

    assert len(graphs) == 2
    
    first_graph_is_acyclic = graphs_svc().is_acyclic_graph(graph=graphs[0][1])
    second_graph_is_acyclic = graphs_svc().is_acyclic_graph(graph=graphs[1][1])

    assert first_graph_is_acyclic == False
    assert second_graph_is_acyclic == True


