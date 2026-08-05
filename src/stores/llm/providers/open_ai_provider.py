from src.stores.llm.LLMInterface import LLMInterface
from openai import OpenAI
import logging
from src.stores.llm.LLMEnums import OPENAIEnums 





class OpenAIProvider(LLMInterface):
    def __init__(self,api_key:str,api_url:str=None,
                default_input_max_characters:int=1000,
                default_output_max_characters:int=1000,
                default_tempreture:float=0.1):
        self.api_key=api_key
        self.api_url=api_url

        self.default_input_max_characters = default_input_max_characters
        self.default_output_max_characters = default_output_max_characters
        self.default_tempreture = default_tempreture

        self.generation_model_id=None
        self.embeddings_model_id=None
        self.embedding_size=None

        self.client=OpenAI(
            api_key=self.api_key,
            base_url=self.api_url if self.api_url and len(self.api_url)>0 else None
        ) 

        self.logger=logging.getLogger(__name__) 

        self.enums=OPENAIEnums

            
    
    
    
    
    def set_generation_model(self, model_id:str) -> None:
        self.generation_model_id = model_id

    def set_embeddings_model(self, model_id:str,embedding_size:int) -> None:  
        self.embeddings_model_id = model_id   
        self.embedding_size = embedding_size 
    
    def process_text(self,text:str) -> str:
        return text[:self.default_input_max_characters].strip()



    def generate_text(self, prompt:str,chat_history:list=[],max_output_tokens:int=None,temprature:float=None) -> str:
        if not self.client:
            self.logger.error("OpenAI client is not initialized")
            return None

        if not self.generation_model_id:
            self.logger.error("Generation model id is not set")
            return None 
        
        max_tokens=max_output_tokens if max_output_tokens else self.default_output_max_characters
        temprature=temprature if temprature else self.default_tempreture
        chat_history.append(self.construct_prompt(prompt,OPENAIEnums.USER.value))

        response = self.client.chat.completions.create(
            model=self.generation_model_id,
            messages=chat_history,
            max_tokens=max_tokens,
            temperature=temprature
        )

        if not response or not response.choices or len(response.choices)==0 or response.choices[0].message is None or not response.choices[0].message.content:
            self.logger.error("No response from OpenAI client")
            return None

        return response.choices[0].message.content  


    def construct_prompt(self,prompt:str,role:str) -> list[]:

        return {'role':role,'content':self.process_text(prompt)}



        
    

    def embed_text(self, text:str,document_type:str) -> list[float]:
        raise NotImplementedError("embed_text method is not implemented yet")
    

    def construct_prompt(self,prompt:str,role:str) -> str:
        raise NotImplementedError("construct_prompt method is not implemented yet")


    def embed_text(self, text:str,document_type:str=None) -> list[float]:
        if not self.client:
            self.logger.error("OpenAI client is not initialized")
            return None

        if not self.embeddings_model_id:
            self.logger.error("Embeddings model id is not set")
            return None



        
        response=self.client.embeddings.create(
            input=text,
            model=self.embeddings_model_id
        )  

        if not response or not response.data or len(response.data)==0 or response.data[0].embedding is None or len(response.data[0].embedding)!=self.embedding_size:
            self.logger.error("No response from OpenAI client")
            return None


        return response.data[0].embedding



        



    
        

