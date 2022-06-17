from pydantic.dataclasses import dataclass
from typing import List, Optional, Tuple


@dataclass 
class AifiDagsRequest:
    graph: Optional[List[Tuple]]=None
    acyclic: Optional[bool]=None
    rows: Optional[int] = 2
    columns: Optional[int] = 2
    number_of_nodes: Optional[int] = 10
    number_of_graphs: Optional[int] = 1

@dataclass 
class AifiResponse:
    content: str
    status_code: Optional[str] = None

