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
    prefix="/api/dags",
    tags=["dags"],
    responses={404: {"description": "Not found"}},
)

@router.post("/acyclic", response_model=AifiResponse, status_code=200, )
async def get_is_dag_acyclic(
    request: AifiDagsRequest,
    dags_svc: DagsService=Depends(DagsService)
) -> AifiResponse:
    """Get a dataset based on a known dataset id."""
    try:
        print(request)
        is_acyclic = dags_svc.is_acyclic_graph(request.graph)
    except Exception as e:
        raise
    
    return AifiResponse(content=is_acyclic, status_code=200)
