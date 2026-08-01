from enum import Enum



class LLMEnums(Enum):
    OPENAI="OPENAI"
    COHERE="COHERE"


class OPENAIEnums(Enum):
    USER="user"
    ASSISTANT="assistant"
    SYSTEM="system"
    