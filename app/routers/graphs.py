from dataclasses import dataclass
import dataclasses
import json
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

@router.post("/acyclic", response_model=AifiResponse, status_code=200, )
async def get_is_dag_acyclic_and_cycles(
    request: AifiDagsRequest,
    dags_svc: GraphsService=Depends(GraphsService)
) -> AifiResponse:
    """Returns whether a graph is acyclic."""
    try:
        is_acyclic, cycle = dags_svc.get_cycle(graph=request.graph)
    except Exception as e:
        raise
    
    return AifiResponse(content=json.dumps((is_acyclic, cycle)), status_code=201)

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