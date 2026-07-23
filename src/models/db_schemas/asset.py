from pydantic import BaseModel, Field
from typing import Optional
from bson.objectid import ObjectId


class Asset(BaseModel):
    id:Optional[ObjectId]=Field(None, alias="_id")
    asset_project_id:ObjectId
    asset_type:str
    asset_name:str=Field(...,min_length=1)
    asset_size:Optional[int]=None
    asset_config:Optional[dict]=None


    class Config:
        arbitrary_types_allowed = True


    @classmethod
    def get_indexes(cls):
        return [
            {
                "key":[("asset_project_id",1),("asset_name",1)],
                "name":"asset_project_id_asset_name_index_1",
                "unique":True
            }
        ]
