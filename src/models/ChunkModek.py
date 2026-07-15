from .BaseDataModel import BaseDataModel
from .db_schemas.data_chunk import DataChunk    
from .enums.DataBaseEnum import DataBaseEnum
from bson.objectid import ObjectId
from pymongo import InsertOne


class ChunkModel(BaseDataModel):

    def __init__(self,db_client:object):
        super().__init__(db_client)
        self.collection=self.db_client[DataBaseEnum.COLLECTION_CHUNK_NAME.value]



    @classmethod
    async def create_instance(cls,db_client:object):
        instance=cls(db_client)
        await instance.init_collection()
        return instance 


    async def init_collection(self,db_client:object=None):

        all_collection=await self.db_client.list_collection_names()

        if DataBaseEnum.COLLECTION_CHUNK_NAME.value not in all_collection:
            self.collection=self.db_client[DataBaseEnum.COLLECTION_CHUNK_NAME.value]
            indexes=DataChunk.get_indexes()
            for index in indexes:
                await self.collection.create_index(index["key"],unique=index["unique"],name=index["name"])
        else:
            self.collection=self.db_client[DataBaseEnum.COLLECTION_CHUNK_NAME.value]    
            
    
    
    
    
    
    async def create_chunk(self,chunk:DataChunk):
        result=await self.collection.insert_one(chunk.dict())
        chunk._id=result.inserted_id
        return  chunk






    async def get_chunk(self,chunk_id:str=None):
            record= await self.collection.find_one(
                {"_id": ObjectId(chunk_id)}
            )
            if record is None:
                return None 
            return DataChunk(**record) 


    async def insert_many_chunks(self,chunks:list,batch_size:int=100):

        for i in range(0,len(chunks),batch_size):
            batch=chunks[i:i+batch_size]
            await self.collection.bulk_write([InsertOne(chunk.dict()) for chunk in batch])


        return len(chunks)



    async def delete_chunks_by_project_id(self,project_id:ObjectId):

        result= await self.collection.delete_many({"chunk_project_id":project_id})

        return result.deleted_count 


     
