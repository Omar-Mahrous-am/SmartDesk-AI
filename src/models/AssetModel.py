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
from sqlalchemy import select

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
        self.db_client = db_client
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
        return instance

    async def create_asset(self, asset: Asset):
        """
        Inserts a new asset document into the database.

        Args:
            asset (Asset): The validated Pydantic model representing the asset.

        Returns:
            Asset: The asset model updated with the generated database ID.
        """
        async with self.db_client() as session:
            async with session.begin():
                session.add(asset)
            await session.commit()
            await session.refresh(asset)

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
        async with self.db_client() as session:
            async with session.begin():
                query=select(Asset).where(Asset.asset_project_id==asset_project_id,Asset.asset_type==asset_type)
                result = await session.execute(query)
                results = result.scalars().all()
                return results
        

    async def get_asset_record(self, asset_project_id: str, asset_id: str):
        """
        Retrieves a single asset record by its project ID and name.

        Args:
            asset_project_id (str): The string or ObjectId of the project.
            asset_name (str): The unique name/identifier of the asset.

        Returns:
            Asset | None: The populated Asset model if found, otherwise None.
        """
        async with self.db_client() as session:
            async with session.begin():
                query=select(Asset).where(Asset.asset_project_id==asset_project_id,Asset.asset_id==asset_id)
                result = await session.execute(query)
                result = result.scalar_one_or_none()
                return result

        

