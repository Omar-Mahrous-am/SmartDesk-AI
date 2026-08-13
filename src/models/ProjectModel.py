"""
Database interaction model for managing projects.

This module provides the `ProjectModel` class, responsible for handling all
database operations related to the 'projects' collection in MongoDB. It includes
functionality for creating projects, retrieving them, and implementing pagination.
"""
from .BaseDataModel import BaseDataModel
from .db_schemas import Project
from .enums.DataBaseEnum import DataBaseEnum
from sqlalchemy.future import select
from sqlalchemy import func

class ProjectModel(BaseDataModel):
    """
    Model for interacting with the projects collection in MongoDB.

    Inherits from `BaseDataModel`. Manages project lifecycle and retrieval,
    supporting operations like get-or-create to simplify controller logic.

    Attributes:
        user_id (int | None): An optional user identifier to scope project access.
    """
    
    def __init__(self, db_client: object):
        """
        Initializes the ProjectModel and binds it to the projects collection.

        Args:
            db_client (object): The active MongoDB database instance.
            user_id (int, optional): The ID of the user requesting the model. Defaults to None.
        """
        super().__init__(db_client)
        self.db_client = db_client



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
        return instance 
    async def create_project(self, project: Project):
        """
        Inserts a new project document into the database.

        Args:
            project_data (project): The validated Pydantic model representing the project.

        Returns:
            project: The project model updated with the database's inserted _id.
        """
        # Convert model to dict, using aliases (like _id) and excluding None values

        async with self.db_client() as session:
            async with session.begin():
                session.add(project)
            await session.commit()
            await session.refresh(project)

        return project


    async def get_project_or_create_one(self, project_id: str = None, existing_project: Project = None):
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
        async with self.db_client() as session:
            async with session.begin():
                query=select(Project).where(Project.project_id==project_id)
                
                project=await session.execute(query)
                project=project.scalar_one_or_none()
                
                if project is None:
                    project_rec=Project(project_id=project_id)                    
                    project=await self.create_project(project=project_rec)
                    return  project
                else:
                    return project          



    

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
        async with self.db_client() as session:
            async with session.begin():
                total_documents=await session.exec(select(func.count(Project.project_id)))
                total_documents=total_documents.scalar_one_or_none()

                total_pages=total_documents//page_size
                if total_documents%page_size > 0:
                    total_pages+=1


                query=select(Project).offset((page-1)*page_size).limit(page_size)
                projects=await session.execute(query).scalars().all()
                return projects,total_pages 
                    
                


                
        
