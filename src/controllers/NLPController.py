import json
from src.controllers.BaseController import BaseController   
from src.models.db_schemas import project,DataChunk
from typing import List
from stores.llm.LLMEnums import DocumentTypeEnum 
import json   
class NLPController(BaseController):
    def __init__(self, vectordb_client,generation_client,embedding_client):
        self.vectordb_client=vectordb_client
        self.generation_client=generation_client
        self.embedding_client=embedding_client


    def create_collection_name(self,project_id:str):
        return f"collection_{project_id}".strip().lower()
    
    
    
    def reset_vectordb_collection(self,project:project):
        collection_name=self.create_collection_name(project_id=project.project_id)
        return self.vectordb_client.delete_collection(collection_name)


    def get_vector_collection_info(self,project:project):
        collection_name=self.create_collection_name(project_id=project.project_id)
        collection_info=self.vectordb_client.get_collection_info(collection_name=collection_name)
        return json.loads(json.dumps(collection_info,default=lambda x:x.__dict__))
        

    def index_into_vectordb(self,project:project,chunks:List[DataChunk],chunks_ids:List[int],do_rest=False):

        #get_collection_name
        collection_name=self.create_collection_name(project_id=project.project_id)


        #manage_items
        texts=[c.chunk_text for c in chunks ]
        metadata=[c.chunk_metadata for c in chunks ]

        vectors=[
            self.embedding_client.embed_text(text,document_type=DocumentTypeEnum.DOCUMENT.value) for text in texts 

        ]



        #create_collection_if_not_exists
        _=self.vectordb_client.create_collection(collection_name=collection_name,embedding_size=self.embedding_client.get_embedding_model_size(),do_reset=do_rest)

        #insert_into_vector_db
        _=self.vectordb_client.insert_many_collections(collection_name=collection_name,texts=texts,vectors=vectors,metadata=metadata,batch_size=50,chunks_ids=chunks_ids)


        return True


    def search_vector_db_collection(self,project:project,text:str,limit:int):
        collection_name=self.create_collection_name(project_id=project.project_id)
        vector=self.embedding_client.embed_text(text=text,document_type=DocumentTypeEnum.QUERY.value)
        if not vector or len(vector)==0:
            return False

        
        search_results=self.vectordb_client.search(collection_name=collection_name,query_vector=vector,limit=limit)

        if not search_results:
            return False
       
        return json.loads(json.dumps(search_results,default=lambda x:x.__dict__))


        






        

