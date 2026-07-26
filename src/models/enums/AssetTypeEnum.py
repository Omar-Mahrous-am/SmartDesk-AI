"""
Enumerations for asset types.

This module provides standard definitions for the different kinds of assets
the system can process and store.
"""
from enum import Enum


class AssetTypeEnum(Enum):
    """
    Standardizes the types of assets supported by the application.

    Using an Enum prevents hardcoded strings and typos throughout the codebase.

    Attributes:
        FILE: Represents a physical document file (e.g., PDF, DOCX).
        IMAGE: Represents an image file.
        URL: Represents a web resource or link.
    """
    FILE = "file"
    IMAGE = "image"
    URL = "url"
