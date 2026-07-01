from pydantic import BaseModel,Field,validator
from typing import Optional
from bson.objectid import ObjectId  



class DataChunk(BaseModel):
    _id:Optional[ObjectId]=None
    chunk_project_id:ObjectId
    chunk_order:int=Field(...,gt=0)
    chunk_content:str=Field(...,min_length=1)
    chunk_metadata:dict
    



    class Config:
        arbitrary_types_allowed = True  




    
    
