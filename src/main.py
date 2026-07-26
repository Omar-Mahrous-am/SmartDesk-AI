"""
Main application entry point for SmartDesk AI.

This module initializes the FastAPI application, loads environment variables,
establishes the database connection to MongoDB, and registers the application routes.
It serves as the central hub tying the project's infrastructure and routing together.
"""
import os
from fastapi import FastAPI
from dotenv import load_dotenv

# =====================================================
# Load Environment Variables
# =====================================================
# Load environment variables before importing other project modules
# to ensure configurations like MongoDB URI are available.
load_dotenv("src/.env")

from src.routes import base, data
from motor.motor_asyncio import AsyncIOMotorClient
from src.helpers import config


app = FastAPI()

# =====================================================
# Application Lifespan Events
# =====================================================

@app.on_event("startup")
async def start_up():
    """
    Handles application startup operations.

    This function is triggered when the FastAPI server starts. It reads the
    application settings and establishes an asynchronous connection to the 
    MongoDB database, attaching the client and database instances to the 
    app state for global access.
    """
    settings = config.get_settings()
    
    # Initialize asynchronous MongoDB client using Motor
    app.mongodb_client = AsyncIOMotorClient(settings.MONGODB_URL)
    # Store the specific database instance for use in controllers/models
    app.mongodb = app.mongodb_client[settings.MONGODB]
    
    print("Connected to MongoDB")

@app.on_event("shutdown")
async def shutdown():
    """
    Handles application shutdown operations.

    This function is triggered when the FastAPI server stops. It ensures
    that the MongoDB connection is properly closed to prevent connection leaks.
    """
    app.mongodb_client.close()
    print("Closed MongoDB connection")  


# =====================================================
# Route Registration
# =====================================================

# Register the base routes (e.g., health checks or general endpoints)
app.include_router(base.base_router)

# Register data processing routes (e.g., upload, process, chunks)
app.include_router(data.data_router)

@app.get("/")
def home():
    """
    Root endpoint for the SmartDesk AI API.

    Provides a simple heartbeat check to verify the API is running
    and accessible.

    Returns:
        dict: A welcome message indicating the API status.
    """
    return {"message": "SmartDesk AI API is running"}
