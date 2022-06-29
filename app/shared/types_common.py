from pydantic.dataclasses import dataclass
from typing import List, Optional, Tuple


@dataclass 
class AifiDagsRequest:
    graph: Optional[List[Tuple]]=None
    acyclic: Optional[bool]=None
    acyclic_flags_list: Optional[List[bool]]=None
    rows: Optional[int] = 2
    columns: Optional[int] = 2
    number_of_nodes: Optional[int] = 10
    number_of_graphs: Optional[int] = 1
    return_graph: Optional[bool] = True
    file_path: Optional[str] = None
    layout: Optional[str] = None
    n: Optional[int] = None

@dataclass 
class AifiResponse:
    content: str
    status_code: Optional[str] = None
