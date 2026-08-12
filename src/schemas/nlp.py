from pydantic import BaseModel
from typing import List, Optional


class PushRequest(BaseModel):
    do_rest:Optional[int]=0
    page_size:Optional[int]=50


class SearchRequest(BaseModel):
    text:str
    limit:Optional[int]=5
    