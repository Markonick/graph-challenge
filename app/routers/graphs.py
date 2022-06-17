from dataclasses import dataclass
import dataclasses
import json
from fastapi import APIRouter, Depends, Response
from typing import List
from fastapi import status
from fastapi.responses import JSONResponse

from shared.types_common import AifiDagsRequest, AifiResponse
from shared.view_models import DagResult
from services.dags_service import DagsService

router = APIRouter(
    prefix="/api/graphs",
    tags=["graphs"],
    responses={404: {"description": "Not found"}},
)

@router.post("/acyclic", response_model=AifiResponse, status_code=200, )
async def get_is_dag_acyclic_and_cycles(
    request: AifiDagsRequest,
    dags_svc: DagsService=Depends(DagsService)
) -> AifiResponse:
    """Get a dataset based on a known dataset id."""
    try:
        is_acyclic, cycle = dags_svc.get_cycle(graph=request.graph)
    except Exception as e:
        raise
    
    return AifiResponse(content=json.dumps((is_acyclic, cycle)), status_code=200)

@router.post("", response_model=AifiResponse, status_code=200, )
async def get_graphs(
    request: AifiDagsRequest,
    dags_svc: DagsService=Depends(DagsService)
) -> AifiResponse:
    """Get a dataset based on a known dataset id."""
    try:
        result = [list(graph) for graph, is_acyclic in dags_svc.generate_graphs(
            number_of_graphs=request.number_of_graphs,
            number_of_nodes=request.number_of_nodes
        )]
    except Exception as e:
        raise

    return AifiResponse(content=json.dumps(result), status_code=200)

@router.post("/draw", response_model=AifiResponse, status_code=200, )
async def draw_graphs(
    request: AifiDagsRequest,
    dags_svc: DagsService=Depends(DagsService)
) -> AifiResponse:
    """Get a dataset based on a known dataset id."""
    try:
        result = dags_svc.draw_graphs(
            rows=request.rows,
            columns=request.columns,
            number_of_nodes=request.number_of_nodes
        )
    except Exception as e:
        raise
        
    return AifiResponse(content=json.dumps(result), status_code=200)