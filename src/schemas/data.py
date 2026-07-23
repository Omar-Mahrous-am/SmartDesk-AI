from pydantic import BaseModel



class ProcessRequest(BaseModel):
    file_id:str =None
    chunk_size:int
    chunk_overlap:int   
    do_reset: int = 0
    