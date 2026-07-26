"""
Database interaction model for managing projects.

This module provides the `ProjectModel` class, responsible for handling all
database operations related to the 'projects' collection in MongoDB. It includes
functionality for creating projects, retrieving them, and implementing pagination.
"""
from .BaseDataModel import BaseDataModel
from .db_schemas import project
from .enums.DataBaseEnum import DataBaseEnum

class ProjectModel(BaseDataModel):
    """
    Model for interacting with the projects collection in MongoDB.

    Inherits from `BaseDataModel`. Manages project lifecycle and retrieval,
    supporting operations like get-or-create to simplify controller logic.

    Attributes:
        user_id (int | None): An optional user identifier to scope project access.
    """
    
    def __init__(self, db_client: object, user_id: int = None):
        """
        Initializes the ProjectModel and binds it to the projects collection.

        Args:
            db_client (object): The active MongoDB database instance.
            user_id (int, optional): The ID of the user requesting the model. Defaults to None.
        """
        super().__init__(db_client)
        self.user_id = user_id
        self.collection = self.db_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value]


    @classmethod
    async def create_instance(cls, db_client: object):
        """
        Asynchronous factory method to create an initialized ProjectModel instance.

        Args:
            db_client (object): The active MongoDB database instance.

        Returns:
            ProjectModel: A fully initialized instance with the collection and indexes prepared.
        """
        instance = cls(db_client)
        await instance.init_collection()
        return instance 


    async def init_collection(self):
        """
        Initializes the collection in the database.

        Checks if the projects collection exists. If not, it creates it and builds
        the necessary indexes (e.g., unique index on project_id) defined in the schema.
        """
        all_collection = await self.db_client.list_collection_names()

        if DataBaseEnum.COLLECTION_PROJECT_NAME.value not in all_collection:
            self.collection = self.db_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value]
            
            # Fetch and apply indexes defined in the project schema
            indexes = project.get_indexes()
            for index in indexes:
                await self.collection.create_index(index["key"], unique=index["unique"], name=index["name"])

        else:
            self.collection = self.db_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value]


    async def create_project(self, project_data: project):
        """
        Inserts a new project document into the database.

        Args:
            project_data (project): The validated Pydantic model representing the project.

        Returns:
            project: The project model updated with the database's inserted _id.
        """
        # Convert model to dict, using aliases (like _id) and excluding None values
        result = await self.collection.insert_one(project_data.dict(by_alias=True, exclude_none=True))
        project_data.id = result.inserted_id
        
        return project_data


    async def get_project_or_create_one(self, project_id: str = None, existing_project: project = None):
        """
        Retrieves a project by its string ID, creating it if it doesn't exist.

        This is a convenience method often used in upload/processing routes where
        the project context might be new.

        Args:
            project_id (str, optional): The unique string identifier of the project.
            existing_project (project, optional): (Unused in current implementation).

        Returns:
            project: The retrieved or newly created project model.
        """
        record = await self.collection.find_one(
            {"project_id": project_id}
        )
        
        # If the project isn't found, automatically initialize and save a new one
        if record is None:
            new_project = project(project_id=project_id)
            new_project = await self.create_project(new_project)
            return new_project
        
        return project(**record)
    

    async def get_all_projects(self, page: int = 1, page_size: int = 10):
        """
        Retrieves a paginated list of all projects in the database.

        Calculates total pages based on document count to assist frontend pagination
        components.

        Args:
            page (int, optional): The page number to retrieve (1-indexed). Defaults to 1.
            page_size (int, optional): The number of projects per page. Defaults to 10.

        Returns:
            tuple[list[project], int]: A tuple containing the list of project models
                for the requested page, and the total number of available pages.
        """
        # First, count total documents to determine the total number of pages
        total_documents = await self.collection.count_documents({})

        # Calculate pages, adding an extra page if there's a remainder
        total_pages = total_documents // page_size
        if total_documents % page_size > 0:
            total_pages += 1

        # Use skip and limit to fetch only the requested slice of data
        cursor = self.collection.find().skip((page - 1) * page_size).limit(page_size)
        
        projects = []

        # Asynchronously iterate over the cursor to avoid blocking the event loop
        async for doc in cursor:
            projects.append(project(**doc))

        return projects, total_pages
