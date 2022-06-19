from dataclasses import dataclass
import dataclasses
import json
import os
from typing import List, Tuple
import pytest
from starlette.testclient import TestClient
from fastapi import status

from shared.types_common import AifiDagsRequest, AifiResponse
from shared.utils_fastapi import create_app
from .main import app
# app = create_app()

@pytest.fixture
def cycle_graph_input() -> AifiDagsRequest:
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
def dag_graph_input() -> AifiDagsRequest:
    graph = [
        ["A", "B"],
        ["B", "C"],
        ["C", "D"],
        ["D", "E"]
    ]

    return AifiDagsRequest(graph=graph, )
graphs_base_url = os.environ.get("GRAPHS_BASE_URL")
graphs_base_url = "http://localhost:8000/api/graphs"


def post_handler(endpoint: str, request: AifiDagsRequest):
    with TestClient(app,) as client:
        headers = {"content-type": "application/json"}
        try:
            r =  client.post(url="http://localhost:8000/api/graphs/acyclic", headers=headers, data=json.dumps(dataclasses.asdict(request)))
        except Exception as e:
            print(e)
            r = str(e)
        print(r)
        return AifiResponse(**json.loads(r.content))

def test_dag_should_return_true(dag_graph_input: AifiDagsRequest):
    endpoint = f"{graphs_base_url}/acyclic"
    result = post_handler(endpoint=endpoint, request=dag_graph_input)

    assert json.loads(result.status_code) == 201
    content = json.loads(result.content)
    assert content[0] == True
    assert content[1] == None

def test_cycle_graph_should_return_true(cycle_graph_input: AifiDagsRequest):
    endpoint = f"{graphs_base_url}/acyclic"
    result = post_handler(endpoint=endpoint, request=cycle_graph_input)

    assert json.loads(result.status_code) == 201
    content = json.loads(result.content)
    assert content[0] == False
    assert sorted(content[1]) == ['C', 'D']
        