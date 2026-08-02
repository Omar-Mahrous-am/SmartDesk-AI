from src.stores.llm.providers import CohereProvider, open_ai_provider   
from src.stores.llm.LLMEnums import LLMEnums

class LLMProviderFactory:

    def __init__(self, config: dict):
        self.config = config 

    def create(self, provider: str):
        if provider == LLMEnums.OPENAI.value:
            return open_ai_provider.OpenAIProvider(
                api_key=self.config.get("OPEN_API_KEYS"),
                api_url=self.config.get("OPEN_API_URL"),
                default_input_max_characters=self.config.get("INPUT_DEFAULT_MAX_CHARACTERS", 1000),
                default_output_max_characters=self.config.get("GENERATION_DEFAULT_MAX_TOKENS", 1000),
                default_tempreture=self.config.get("GENERATION_DEFAULT_TEMPERATURE", 0.1)
            )

        if provider == LLMEnums.COHERE.value:
            return CohereProvider.CohereProvider(
                api_key=self.config.get("COHERE_API_KEY"),
                default_input_max_characters=self.config.get("INPUT_DEFAULT_MAX_CHARACTERS", 1000),
                default_output_max_characters=self.config.get("GENERATION_DEFAULT_MAX_TOKENS", 1000),
                default_tempreture=self.config.get("GENERATION_DEFAULT_TEMPERATURE", 0.1)
            )    

        raise ValueError(f"Unsupported LLM provider: {provider}")
