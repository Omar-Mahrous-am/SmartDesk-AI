from pydantic import BaseModel
from typing import List


class PushRequest(BaseModel):
    do_rest:Optional[int]=0
    