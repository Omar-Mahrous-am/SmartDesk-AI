from enum import Enum



class LLMEnums(Enum):
    OPENAI="OPENAI"
    COHERE="COHERE"


class OPENAIEnums(Enum):
    USER="user"
    ASSISTANT="assistant"
    SYSTEM="system"


class COHEREEnums(Enum):
    USER="USER"
    ASSISTANT="CHATBOT"
    SYSTEM="SYSTEM"

    DOCUMENT="search_document"
    QUERY="search_query"


class DocumentTypeEnum(Enum):
    QUERY="query"
    DOCUMENT="document"

