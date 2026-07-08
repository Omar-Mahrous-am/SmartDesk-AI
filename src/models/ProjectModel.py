from .BaseDataModel import BaseDataModel
from .db_schemas import project
from .enums.DataBaseEnum import DataBaseEnum

class ProjectModel(BaseDataModel):
    def __init__(self,db_client:object,user_id:int):
        super().__init__(db_client)
        self.user_id=user_id
        self.collection=self.db_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value]
    

    async def create_project(self,project:project):
        result=await self.collection.insert_one(project.dict())
        project._id=result.inserted_id
        return  project


    async def get_project_or_create_one(self,project_id:str=None,project:project=None):
            record= await self.collection.find_one(
                "project_id"==project_id

            )
            if record:
                return record
            else:
                return await self.create_project(project)

        

