"""
Database interaction model for managing document chunks.

This module provides the `ChunkModel` class, which handles all database operations
related to storing and retrieving text chunks generated during document processing.
These chunks are typically used in Retrieval-Augmented Generation (RAG) pipelines.
"""
from .BaseDataModel import BaseDataModel
from .db_schemas.data_chunk import DataChunk    
from .enums.DataBaseEnum import DataBaseEnum
from bson.objectid import ObjectId
from pymongo import InsertOne


class ChunkModel(BaseDataModel):
    """
    Model for interacting with the chunks collection in MongoDB.

    Inherits from `BaseDataModel`. Manages the insertion (both single and bulk)
    and deletion of text chunk documents, ensuring that chunks are properly 
    linked to their respective projects.
    """

    def __init__(self, db_client: object):
        """
        Initializes the ChunkModel and binds it to the chunks collection.

        Args:
            db_client (object): The active MongoDB database instance.
        """
        super().__init__(db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTION_CHUNK_NAME.value]

    @classmethod
    async def create_instance(cls, db_client: object):
        """
        Asynchronous factory method to create an initialized ChunkModel instance.

        Args:
            db_client (object): The active MongoDB database instance.

        Returns:
            ChunkModel: A fully initialized instance with the collection and indexes prepared.
        """
        instance = cls(db_client)
        await instance.init_collection()
        return instance 

    async def init_collection(self, db_client: object = None):
        """
        Initializes the chunks collection and creates necessary indexes.

        This ensures that indexes (like the unique compound index on project ID and order)
        are created if the collection is being initialized for the first time.
        """
        all_collection = await self.db_client.list_collection_names()

        if DataBaseEnum.COLLECTION_CHUNK_NAME.value not in all_collection:
            self.collection = self.db_client[DataBaseEnum.COLLECTION_CHUNK_NAME.value]
            
            # Fetch and apply indexes defined in the DataChunk schema
            indexes = DataChunk.get_indexes()
            for index in indexes:
                await self.collection.create_index(index["key"], unique=index["unique"], name=index["name"])
        else:
            self.collection = self.db_client[DataBaseEnum.COLLECTION_CHUNK_NAME.value]    

    async def create_chunk(self, chunk: DataChunk):
        """
        Inserts a single chunk document into the database.

        Args:
            chunk (DataChunk): The validated chunk model to insert.

        Returns:
            DataChunk: The chunk model updated with the database's inserted _id.
        """
        result = await self.collection.insert_one(chunk.dict())
        chunk._id = result.inserted_id
        return chunk

    async def get_chunk(self, chunk_id: str = None):
        """
        Retrieves a specific chunk by its MongoDB ObjectId.

        Args:
            chunk_id (str, optional): The string representation of the chunk's ObjectId.

        Returns:
            DataChunk | None: The populated chunk model if found, otherwise None.
        """
        record = await self.collection.find_one(
            {"_id": ObjectId(chunk_id)}
        )
        if record is None:
            return None 
        return DataChunk(**record) 

    async def insert_many_chunks(self, chunks: list, batch_size: int = 100):
        """
        Inserts multiple chunk documents efficiently using MongoDB bulk write operations.

        This is crucial for performance when processing large documents that produce
        hundreds or thousands of chunks.

        Args:
            chunks (list): A list of DataChunk Pydantic models.
            batch_size (int, optional): The number of chunks to insert per bulk operation.
                Defaults to 100 to balance memory usage and network round trips.

        Returns:
            int: The total number of chunks processed.
        """
        for i in range(0, len(chunks), batch_size):
            # Slice the chunks list into manageable batches
            batch = chunks[i:i + batch_size]
            
            # Prepare and execute the bulk write operation for the current batch
            await self.collection.bulk_write([InsertOne(chunk.dict()) for chunk in batch])

        return len(chunks)

    async def delete_chunks_by_project_id(self, project_id: ObjectId):
        """
        Deletes all chunks associated with a specific project.

        This is used when re-processing a document to clear out stale chunks
        before inserting the newly generated ones, preventing duplicate key errors.

        Args:
            project_id (ObjectId): The MongoDB ObjectId of the project.

        Returns:
            int: The number of chunk documents deleted.
        """
        result = await self.collection.delete_many({"chunk_project_id": project_id})

        return result.deleted_count 
