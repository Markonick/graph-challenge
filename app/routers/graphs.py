from dataclasses import dataclass
import dataclasses
import functools
import json
from tkinter.messagebox import RETRY
from fastapi import APIRouter, Depends, Response
from typing import List
from fastapi import status
from fastapi.responses import JSONResponse
from pydantic import Json

from shared.types_common import AifiDagsRequest, AifiResponse
from shared.view_models import DagResult
from services.graphs_service import GraphsService

router = APIRouter(
    prefix="/api/graphs",
    tags=["graphs"],
    responses={404: {"description": "Not found"}},
)
import sys

class recursionlimit:
    def __init__(self, limit):
        self.limit = limit

    def __enter__(self):
        self.old_limit = sys.getrecursionlimit()
        sys.setrecursionlimit(self.limit)

    def __exit__(self, type, value, tb):
        sys.setrecursionlimit(self.old_limit)

def memo(func):
    cache = {}

    def wrapped(*args):
        if args in cache:
            return cache[args]
        else:
            cache[args] = func(*args)
            return cache[args]
        
    return wrapped

def fib_gen(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b
@memo
def fib(n):
    with recursionlimit(15000):
        if n == 0:
            return 0
        elif n == 1 or n == 2:
            return 1
        else:
            return fib(n-1) + fib(n-2)
        
@router.post("/fibo", response_model=AifiResponse, status_code=200, )
async def get_fibo(
    request: AifiDagsRequest,
) -> AifiResponse:
    """Returns fibonacci of n"""
    # result = fib(request.n)
    result = list(fib_gen(request.n))
    return AifiResponse(content=json.dumps(result), status_code=201)

@router.post("/acyclic/custom", response_model=AifiResponse, status_code=200, )
async def get_is_dag_acyclic(
    request: AifiDagsRequest,
    dags_svc: GraphsService=Depends(GraphsService)
) -> AifiResponse:
    """Returns whether a graph is acyclic."""
    try:
        is_acyclic = dags_svc.is_acyclic_graph_custom(edges=request.graph)
    except Exception as e:
        raise
    
    return AifiResponse(content=json.dumps(is_acyclic), status_code=201)

# @router.post("/acyclic", response_model=AifiResponse, status_code=200, )
# async def get_is_dag_acyclic_and_cycles(
#     request: AifiDagsRequest,
#     dags_svc: GraphsService=Depends(GraphsService)
# ) -> AifiResponse:
#     """Returns whether a graph is acyclic."""
#     try:
#         is_acyclic, cycle = dags_svc.get_cycle(graph=request.graph)
#     except Exception as e:
#         raise
    
#     return AifiResponse(content=json.dumps((is_acyclic, cycle)), status_code=201)

@router.post("", response_model=AifiResponse, status_code=200, )
async def get_graphs(
    request: AifiDagsRequest,
    dags_svc: GraphsService=Depends(GraphsService)
) -> AifiResponse:
    """POST that creates graph(s) and returns them as a (list of if many graphs) list of tuples (edges) based on whether
    we need it to be acyclic or not and by defining the number of nodes."""
    try:
        result = dags_svc.generate_graphs(
                    acyclic_flags_list=request.acyclic_flags_list,
                    number_of_graphs=request.number_of_graphs,
                    number_of_nodes=request.number_of_nodes
                )
        if not request.return_graph:
            result = []
        
    except Exception as e:
        raise

    return AifiResponse(content=json.dumps(result), status_code=200)

@router.post("/draw", response_model=AifiResponse, status_code=200, )
async def draw_graphs(
    request: AifiDagsRequest,
    dags_svc: GraphsService=Depends(GraphsService)
) -> AifiResponse:
    """POST that creates a resource (in this case a PDF file) 
    and can return the actual graph in list of tuple format if requested."""
    try:
        result = dags_svc.draw_graphs(
            acyclic_flags_list=request.acyclic_flags_list,
            columns=request.columns,
            number_of_nodes=request.number_of_nodes,
            rows=request.rows,
            file_path=request.file_path,
            layout=request.layout,
        )
        
        if not request.return_graph:
            result = []
    except Exception as e:
        raise

    return AifiResponse(content=json.dumps(result), status_code=200)