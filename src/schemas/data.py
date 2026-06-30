from pydantic import BaseModel



class ProcessRequest(BaseModel):
    file_id:str
    chunk_size:int
    chunk_overlap:int   
    