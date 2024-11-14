"""
This module initializes the FastAPI app and includes the routers.
"""

from fastapi import FastAPI
from dotenv import load_dotenv
import uvicorn
import os
from backend.app.routers import course
from backend.app.routers import login
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()

# Set CORS origins dynamically 
origins = [
    "http://localhost:3000",  # for local development
    "http://18.116.115.43"  # for production, should be set in your .env file
]

# Load the correct .env file based on the environment
environment = os.getenv("ENVIRONMENT")
env_file = f".env.{environment}"
load_dotenv(env_file)
frontend_url = os.getenv("FRONTEND_URL")
print(frontend_url)

@app.get("/")
async def root():
    return {"message": "Welcome to the application!"}

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(course.router)
app.include_router(login.router)

# Get IP from HOST and PORT in .env

if __name__ == "__main__":
    host = os.getenv("HOST")
    port = os.getenv("PORT")
    uvicorn.run(app, host=host, port=port)