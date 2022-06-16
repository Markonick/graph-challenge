from pydantic.dataclasses import dataclass
from typing import List, Optional, Tuple


@dataclass 
class AifiDagsRequest:
    graph: List[Tuple]

@dataclass 
class AifiResponse:
    content: str
    status_code: Optional[str] = None

