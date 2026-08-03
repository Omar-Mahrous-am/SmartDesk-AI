from typing import List
from src.stores.vectordb.VectorDBInterface import VectorDBInterface
import logging
from src.stores.vectordb.VectorDBEnums import DistanceMethodEnum
from qdrant_client import QdrantClient, models



logger = logging.getLogger(__name__)    

class QdrantDB(VectorDBInterface):
    def __init__(self,db_path:str=None, distance_method:str=None):
        self.db_path=db_path
        #distance method enum check 
        self.distance_method=None
        if distance_method==DistanceMethodEnum.COSINE.value:
            self.distance_method=DistanceMethodEnum.COSINE.value
        elif distance_method==DistanceMethodEnum.DOT_PRODUCT.value:
            self.distance_method=DistanceMethodEnum.DOT_PRODUCT.value    
        else:
            self.logger.error("Invalid distance method")
            self.distance_method=DistanceMethodEnum.COSINE.value
        


        self.client=None
        self.logger.info("QdrantDB initialized")
        self.logger.info(f"DB Path: {self.db_path}")
        self.logger.info(f"Distance Method: {self.distance_method}")

    def connect(self):
        if self.db_path:
            self.client=QdrantClient(url=self.db_path)
            self.logger.info("QdrantDB connected")
        else:
            self.logger.error("QdrantDB not connected")

    def dis_connect(self):  
        self.client=None
        self.logger.info("QdrantDB disconnected")



    
    def is_collection_exists(self,collection_name:str):
        return self.client.collection_exists(collection_name=collection_name)

    
    def list_all_collections(self)->List[str]:
        return self.client.get_collections()
        

    def get_collection_info(self,collection_name:str)->dict:
        return self.client.get_collection(collection_name=collection_name)


    def create_collection(self,collection_name:str,embedding_size:int,do_reset:bool=False):
        if do_reset==1:
            self.delete_collection(collection_name)

        if not self.is_collection_exists(collection_name):
            self.client.create_collection(collection_name=collection_name,
                                                vectors_config=models.VectorParams(size=embedding_size,distance=self.distance_method))

            return True    
        else:
            self.logger.error("Collection already exists")
            return False
        
    
    def delete_collection(self,collection_name:str):
        if self.is_collection_exists(collection_name):
            self.client.delete_collection(collection_name=collection_name)
        else:
            self.logger.error("Collection not found")


    def insert_one_collection(self,collection_name:str,embedding:List[float],metadata:dict=None,record_id:str=None):
        if self.is_collection_exists(collection_name):
            self.client.upload_records(collection_name=collection_name,
                                records=[models.Record(id=record_id,vector=embedding,payload=metadata)])

            self.logger.info("Point inserted successfully")
            return True    
        else:
            self.logger.error("Collection not found")
            return False

    
    
    def insert_many_collections(self,collection_name:str,texts:list=None,vectors:list,metadata:List[dict]=None,record_ids:List[str]=None,batch_size:int=50):

        if metadata is None:
            metadata=[None] * len(vectors)

        if record_ids is None:
            record_ids=list(range(0,len(texts)))
        

        


        if self.is_collection_exists(collection_name=collection_name):

            for i in range(0,len(texts),batch_size):
                batch_end=i+batch_size

                try:
                    self.client.upload_records(collection_name=collection_name,
                                    records=models.Record(id=record_ids[i:batch_end],vector=vectors[i:batch_end],payload=metadata[i:batch_end]))
                except Exception as e:
                    self.logger.error(e)
                    return False

            return True    
        else:
            self.logger.error("Collection not found")
            return False


    
    
    
    def serach_by_vector(self,collection_name:str,vector:List[float],limit:int=5):
        
        if self.is_collection_exists(collection_name=collection_name):
            self.client.search(collection_name=collection_name,query_vector=vector,limit=limit)    
        else:
            self.logger.error("Collection not found")
            return False    
