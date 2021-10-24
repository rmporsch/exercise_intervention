from pydantic import BaseModel
from typing import List, Optional
from chalicelib.data_schemas import BaseData


class ResponseUserData(BaseModel):
    user_id: str
    data: List[BaseData]


class RequestUserData(BaseModel):
    user_id: str
    num_items: int
    table: Optional[str]
