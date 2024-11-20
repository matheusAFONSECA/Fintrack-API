import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import uvicorn
from fastapi import FastAPI
from src.fintrack_api.api import router

# Initialize the FastAPI application
app = FastAPI()

# Include the API router
app.include_router(router)

if __name__ == "__main__":
    # Run the application with Uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
