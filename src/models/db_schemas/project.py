"""
Pydantic schema definition for projects.

This module defines the data structure and validation rules for project documents.
Projects serve as the top-level container for assets and document chunks.
"""
from pydantic import BaseModel, Field, validator
from typing import Optional
from bson.objectid import ObjectId


class project(BaseModel):
    """
    Pydantic schema representing a user project.

    Used for validating data before inserting into the projects collection
    and for deserializing database records.

    Attributes:
        id (ObjectId | None): The MongoDB internal identifier, aliased as '_id'.
        project_id (str): The unique string identifier for the project provided by the client.
    """
    id: Optional[ObjectId] = Field(None, alias="_id")
    project_id: str = Field(..., min_length=1)

    @validator("project_id")
    def project_id_validator(cls, value):
        """
        Validates that the project_id contains only alphanumeric characters.

        This is crucial because the project_id is often used as a directory name
        in the filesystem, and preventing special characters mitigates path traversal
        or invalid directory name errors.

        Args:
            value (str): The provided project ID string.

        Returns:
            str: The validated project ID.

        Raises:
            ValueError: If the string is not purely alphanumeric.
        """
        if not value.isalnum():
            raise ValueError("project_id must be alphanumeric")
        return value

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
        Defines the MongoDB indexes required for the projects collection.

        Returns:
            list[dict]: A list of index definitions, specifically ensuring that
                the string `project_id` is unique across the entire database.
        """
        return [{"key": [("project_id", 1)], "name": "project_id_index_1", "unique": True}]
