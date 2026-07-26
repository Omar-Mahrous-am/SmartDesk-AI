"""
Base API routes for the SmartDesk application.

This module defines the foundational routes, such as the root endpoint,
primarily used for health checks and basic application verification.
"""

from fastapi import APIRouter
import os
from dotenv import load_dotenv

# Ensure environment variables are loaded for the base route
load_dotenv(".env")

base_router = APIRouter(prefix="/api/v1", tags=["api_v1"])

@base_router.get("/")
async def welcome():
    """
    Root endpoint for the API.

    Returns a simple welcome message including the application name.
    Useful as a lightweight health check to verify the server is running.

    Returns:
        dict: A JSON response containing the welcome message.
    """
    app_name = os.getenv("APP_NAME")
    return {"message": "Welcome to " + str(app_name)}