from typing import Any, List, Optional
from enum import Enum, unique
from pydantic.dataclasses import dataclass


    
@dataclass
class DagResult:
    """Information about each dataset as a whole"""
    
    resul: str
    size: int
    type: str
    dataset_path: str
    images_path: str
    id: Optional[int] = None

@dataclass
class Model:
    """Information about each model as a whole"""

    name: str
    datasets: List[str]
    id: Optional[int] = None
    