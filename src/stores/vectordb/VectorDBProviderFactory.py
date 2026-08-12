from src.stores.vectordb.VectorDBInterface import VectorDBInterface
from src.stores.vectordb.VectorDBEnums import VectorDBEnum
from src.stores.vectordb.providers.QdrantDBProvider import QdrantDBProvider
from src.controllers.BaseController import BaseController

class VectorDBProviderFactory:
    def __init__(self,config):
        self.config=config
        self.base_controller=BaseController()

    def create(self,vector_db:str=VectorDBEnum.QDRANT.value,db_path:str=None, distance_method:str=None)->VectorDBInterface:
        if vector_db==VectorDBEnum.QDRANT.value:
            return QdrantDBProvider(db_path=self.base_controller.get_database_path("qdrant_db"), distance_method=self.config.VECTOR_DB_DISTANCE_METHOD)
        else:
            raise ValueError("Invalid vector db")
       

    