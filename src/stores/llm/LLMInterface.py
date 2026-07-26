from abc import ABC, abstractmethod


class LLMInterface(ABC):
    def __init__(self):
        pass
    @abstractmethod
    def set_generation_model(self, model_id:str) -> None:
        pass


    @abstractmethod
    def set_embeddings_model(self, model_id:str) -> None:
        pass    
    
    @abstractmethod
    def generate_text(self, prompt: str,max_output_tokens:int,temprature:float=0.5) -> str:
        pass

    @abstractmethod
    def embed_text(self, text: str,document_type:str ) -> list[float]:
        pass


    @abstractmethod
    def construct_prompt(self,prompt:str,role:str) -> str:
        pass  

    
      





    