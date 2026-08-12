from src.stores.llm.providers import CoHereProvider as CohereProvider, open_ai_provider
from src.stores.llm.LLMEnums import LLMEnums

class LLMProviderFactory:

    def __init__(self, config: dict):
        self.config = config 

    def create(self, provider: str):
        if provider == LLMEnums.OPENAI.value:
            return open_ai_provider.OpenAIProvider(
                api_key=self.config.OPEN_API_KEYS,
                api_url=self.config.OPEN_API_URL,
                default_input_max_characters=self.config.INPUT_DEFAULT_MAX_CHARACTERS,
                default_output_max_characters=self.config.GENERATION_DEFAULT_MAX_TOKENS,
                default_tempreture=self.config.GENERATION_DEFAULT_TEMPERATURE
            )

        if provider == LLMEnums.COHERE.value:
            return CohereProvider.CohereProvider(
                api_key=self.config.COHERE_API_KEY,
                default_input_max_characters=self.config.INPUT_DEFAULT_MAX_CHARACTERS,
                default_output_max_characters=self.config.GENERATION_DEFAULT_MAX_TOKENS,
                default_tempreture=self.config.GENERATION_DEFAULT_TEMPERATURE
            )

        raise ValueError(f"Unsupported LLM provider: {provider}")
