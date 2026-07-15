from .BaseDataModel import BaseDataModel
from .db_schemas import project
from .enums.DataBaseEnum import DataBaseEnum

class ProjectModel(BaseDataModel):
    def __init__(self,db_client:object,user_id:int=None):
        super().__init__(db_client)
        self.user_id=user_id
        self.collection=self.db_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value]


    @classmethod
    async def create_instance(cls,db_client:object):
        instance=cls(db_client)
        await instance.init_collection()
        return instance 


    async def init_collection(self):
        all_collection=await self.db_client.list_collection_names()

        if DataBaseEnum.COLLECTION_PROJECT_NAME.value not in all_collection:
            self.collection=self.db_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value]
            indexes=project.get_indexes()
            for index in indexes:
                await self.collection.create_index(index["key"],unique=index["unique"],name=index["name"])

        else:
            self.collection=self.db_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value]


        
    

    async def create_project(self,project:project):
        result=await self.collection.insert_one(project.dict(by_alias=True,exclude_none=True))
        project._id=result.inserted_id
        return  project


    async def get_project_or_create_one(self,project_id:str=None,existing_project:project=None):
            record= await self.collection.find_one(
                {"project_id": project_id}
            )
            if record is None:
                new_project=project(project_id=project_id)
                new_project=await self.create_project(new_project)
                return new_project
            
            return project(**record)
    

    async def get_all_projects(self,page:int=1,page_size:int=10):

        #count_docs

        total_documents= await self.collection.count_documents({})

        total_pages=total_documents // page_size

        if total_documents%page_size >0:
            total_pages+=1

        
        cursor=self.collection.find().skip((   page-1)*page_size).limit(page_size)
        

        projects=[]

        async for doc in cursor:
            projects.append(project(**doc))

        

        return projects ,total_pages

                
            

        

