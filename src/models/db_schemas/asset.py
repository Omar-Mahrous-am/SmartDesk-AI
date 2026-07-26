"""
Pydantic schema definition for assets.

This module defines the data structure and validation rules for asset documents
stored in the MongoDB database. Assets represent files or resources uploaded
and processed by the application.
"""
from pydantic import BaseModel, Field
from typing import Optional
from bson.objectid import ObjectId


class Asset(BaseModel):
    """
    Pydantic schema representing a project asset.

    Used for validating data before inserting into the database and for
    deserializing database records back into Python objects.

    Attributes:
        id (ObjectId | None): The MongoDB internal identifier, aliased as '_id'.
        asset_project_id (ObjectId): The ID of the project this asset belongs to.
        asset_type (str): The classification of the asset (e.g., 'file', 'image').
        asset_name (str): The unique identifier/name for the asset.
        asset_size (int | None): The size of the asset in bytes.
        asset_config (dict | None): Optional configuration or metadata for the asset.
    """
    id: Optional[ObjectId] = Field(None, alias="_id")
    asset_project_id: ObjectId
    asset_type: str
    asset_name: str = Field(..., min_length=1)
    asset_size: Optional[int] = None
    asset_config: Optional[dict] = None

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
        Defines the MongoDB indexes required for the assets collection.

        Returns:
            list[dict]: A list of index definitions, including a unique compound
                index on project ID and asset name to prevent duplicates within a project.
        """
        return [
            {
                "key": [("asset_project_id", 1), ("asset_name", 1)],
                "name": "asset_project_id_asset_name_index_1",
                "unique": True
            }
        ]
