"""
Pydantic schema definition for data chunks.

This module defines the structure and validation rules for text chunks,
which are generated during document processing and used for semantic search.
"""
from pydantic import BaseModel, Field, validator
from typing import Optional
from bson.objectid import ObjectId  


class DataChunk(BaseModel):
    """
    Pydantic schema representing a document text chunk.

    Used for data validation before database insertion. Chunks are the atomic
    units of text used in the RAG pipeline.

    Attributes:
        id (ObjectId | None): The MongoDB internal identifier, aliased as '_id'.
        chunk_project_id (ObjectId): The ID of the project this chunk belongs to.
        chunk_asset_id (ObjectId): The ID of the specific asset this chunk was generated from.
        chunk_order (int): The sequential position of this chunk in the original document.
        chunk_text (str): The actual text content of the chunk.
        chunk_metadata (dict): Additional information (e.g., page number, source).
    """
    id: Optional[ObjectId] = Field(None, alias="_id")
    chunk_project_id: ObjectId
    chunk_asset_id: ObjectId
    chunk_order: int = Field(..., gt=0)
    chunk_text: str = Field(..., min_length=1)
    chunk_metadata: dict
    
    class Config:
        """
        Pydantic configuration class.

        Allows arbitrary types like BSON ObjectIds to be used as fields
        without Pydantic raising validation errors.
        """
        arbitrary_types_allowed = True 

    @classmethod
    def get_indexes(cls):
        """
        Defines the MongoDB indexes required for the chunks collection.

        Returns:
            list[dict]: A list of index definitions, including a unique compound
                index on project ID and chunk order to prevent overlap/duplicates.
        """
        return [
            {
                "key": [("chunk_project_id", 1), ("chunk_order", 1)],
                "name": "chunk_project_id_chunk_order_index_1",
                "unique": True
            }
        ]
