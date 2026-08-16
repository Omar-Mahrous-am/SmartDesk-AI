from enum import Enum


class VectorDBEnum(Enum):
    QDRANT="QDRANT"
    PGVECTOR="PGVECTOR"


class DistanceMethodEnum(Enum):
    COSINE="Cosine"
    DOT_PRODUCT="Dot"

class PgVectorTableschemaEnums(Enum):
    TEXT="text"
    VECTOR="vector"
    ID='id'
    CHUNK_ID='chunk_id'
    METADATA='metadata'
    _PREFIX='pgvector'

class PgVectorDistanceMethodEnum(Enum):
    COSINE='vector_cosine_ops'
    DOT_PRODUCT='vector_l2_ops'

class PgVectorVectorIndexMethodEnum(Enum):
    IVFFLAT='ivfflat'
    HNSW='hnsw'


    
