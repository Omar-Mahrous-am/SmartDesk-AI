"""
Base data model for the SmartDesk AI database interaction layer.

This module provides the `BaseDataModel` class, which serves as the foundational
class for all database models, ensuring they share a common database client
and application settings.
"""
from src.helpers import get_settings, Settings


class BaseDataModel:
    """
    A foundational data model class intended to be inherited by other models.

    This class centralizes the initialization of the database client and application
    settings, promoting code reusability and consistent configuration across
    all collections in the database.

    Attributes:
        db_client (object): The active MongoDB client/database instance.
        app_settings (Settings): The validated application settings object.
    """
    def __init__(self, db_client: object):
        """
        Initializes the BaseDataModel.

        Args:
            db_client (object): The MongoDB database instance to be used for queries.
        """
        self.db_client = db_client
        
        # Load application settings for use in derived models (e.g., config values)
        self.app_settings = get_settings()
