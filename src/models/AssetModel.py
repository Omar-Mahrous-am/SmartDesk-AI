"""
Database interaction model for managing assets.

This module provides the `AssetModel` class, responsible for all CRUD
operations related to the 'assets' collection in MongoDB, including
creating assets and retrieving project-specific assets.
"""
from .BaseDataModel import BaseDataModel
from .db_schemas import Asset
from .enums.DataBaseEnum import DataBaseEnum
from bson import ObjectId

class AssetModel(BaseDataModel):
    """
    Model for interacting with the assets collection in MongoDB.

    Inherits from `BaseDataModel` to utilize the shared database client.
    Handles the lifecycle of asset documents (like uploaded files), 
    ensuring they are properly indexed and stored.
    """

    def __init__(self, db_client: object):
        """
        Initializes the AssetModel and binds it to the assets collection.

        Args:
            db_client (object): The active MongoDB database instance.
        """
        super().__init__(db_client=db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTION_ASSET_NAME.value]

    @classmethod
    async def create_instance(cls, db_client: object):
        """
        Asynchronous factory method to create an initialized AssetModel instance.

        This ensures that necessary database initialization (like index creation)
        completes before the model is used.

        Args:
            db_client (object): The active MongoDB database instance.

        Returns:
            AssetModel: A fully initialized instance of the model.
        """
        instance = cls(db_client)
        await instance.init_collection()
        return instance

    async def init_collection(self):
        """
        Initializes the collection in the database.

        Checks if the assets collection exists. If it doesn't, it forces
        the creation of the collection (by accessing it) and builds all
        required indexes defined in the `Asset` schema to ensure query performance
        and data integrity (e.g., unique constraints).
        """
        all_collections = await self.db_client.list_collection_names()
        if DataBaseEnum.COLLECTION_ASSET_NAME.value not in all_collections:
            self.collection = self.db_client[DataBaseEnum.COLLECTION_ASSET_NAME.value]
            
            # Fetch index definitions from the Pydantic schema and create them
            indexes = Asset.get_indexes()
            for index in indexes:
                await self.collection.create_index(
                    index["key"],
                    name=index["name"],
                    unique=index["unique"]
                )

    async def create_asset(self, asset: Asset):
        """
        Inserts a new asset document into the database.

        Args:
            asset (Asset): The validated Pydantic model representing the asset.

        Returns:
            Asset: The asset model updated with the generated database ID.
        """
        # Convert the Pydantic model to a dictionary, respecting aliases (e.g., '_id')
        # and excluding unset values to keep the database document clean
        result = await self.collection.insert_one(asset.dict(by_alias=True, exclude_unset=True))
        
        # Populate the Pydantic model with the generated MongoDB ObjectId
        asset.id = result.inserted_id

        return asset

    async def get_all_project_assets(self, asset_project_id: str, asset_type: str):
        """
        Retrieves all assets associated with a specific project and type.

        Args:
            asset_project_id (str): The string or ObjectId of the project.
            asset_type (str): The type of asset to filter by (e.g., 'file').

        Returns:
            list[Asset]: A list of populated Asset Pydantic models.
        """
        # Convert the string ID to a MongoDB ObjectId if necessary for querying
        records = await self.collection.find({
            "asset_project_id": ObjectId(asset_project_id) if isinstance(asset_project_id, str) else asset_project_id,
            "asset_type": asset_type,
        }).to_list(length=None)

        # Deserialize the raw database dictionaries back into Pydantic models
        return [
            Asset(**record)
            for record in records
        ]

    async def get_asset_record(self, asset_project_id: str, asset_name: str):
        """
        Retrieves a single asset record by its project ID and name.

        Args:
            asset_project_id (str): The string or ObjectId of the project.
            asset_name (str): The unique name/identifier of the asset.

        Returns:
            Asset | None: The populated Asset model if found, otherwise None.
        """
        record = await self.collection.find_one({
            "asset_project_id": ObjectId(asset_project_id) if isinstance(asset_project_id, str) else asset_project_id,
            "asset_name": asset_name,
        })

        if record:
            return Asset(**record)
        
        return None

