from pydantic import BaseModel,Field,validator
from typing import Optional
from bson.objectid import ObjectId
class project(BaseModel):
    _id:Optional[ObjectId]= None
    project_id:str=Field(...,min_length=1)


    @validator("project_id")
    def project_id_validator(cls,value):
        if not value.isalnum():
            raise ValueError("project_id must be alphanumeric")
        return value


    class Config:
        arbitrary_types_allowed = True

      

