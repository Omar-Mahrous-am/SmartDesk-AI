"""
Project management controller for the SmartDesk AI application.

This module provides the `ProjectController` class, which handles project-level
operations, primarily focusing on managing the physical directory structure
for different projects on the server.
"""
from .BaseController import BaseController
from fastapi import UploadFile
from src.models.enums.ResponseSignal import ResponseSignal
import os

class ProjectController(BaseController):
    """
    Controller responsible for project-related filesystem operations.

    This class manages the creation and retrieval of project-specific directories
    where uploaded files and assets are stored.
    """
    
    def __init__(self):
        """
        Initializes the ProjectController.
        """
        super().__init__()

    def get_project_path(self, project_id: str):
        """
        Retrieves the absolute or relative path to a project's storage directory.

        If the directory for the specified project ID does not exist, this method
        creates it automatically to ensure subsequent file operations succeed.

        Args:
            project_id (str): The unique identifier for the project.

        Returns:
            str: The path to the project's dedicated storage directory.
        """
        # Construct the path by appending the project ID to the base files directory
        project_dir = os.path.join(
            self.files_dir,
            project_id
        )

        # Ensure the project directory structure exists on disk before returning
        if not os.path.exists(project_dir):
            os.makedirs(project_dir)

        return project_dir
