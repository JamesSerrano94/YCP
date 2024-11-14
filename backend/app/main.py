"""
This module initializes the FastAPI app and includes the routers.
"""

from fastapi import FastAPI
from dotenv import load_dotenv
import uvicorn
import os
from backend.app.routers import course, login
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables
load_dotenv()
environment = os.getenv("ENVIRONMENT", "development")  # Default to "development" if ENVIRONMENT is not set
env_file = f".env.{environment}"
load_dotenv(env_file)

# Get environment-specific configurations
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
backend_host = os.getenv("HOST", "0.0.0.0")
backend_port = int(os.getenv("PORT", 443))  # Default to HTTPS port

# Path to SSL certificate and key (use Let's Encrypt paths)
ssl_certfile = "/etc/letsencrypt/live/api.yalecoursemap.com/fullchain.pem"
ssl_keyfile = "/etc/letsencrypt/live/api.yalecoursemap.com/privkey.pem"

# Initialize FastAPI app
app = FastAPI()

# Configure CORS
origins = [
    frontend_url,
    "https://yalecoursemap.com"  # production frontend
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(course.router)
app.include_router(login.router)

# Define a root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the application!"}

# Run the app with Uvicorn, using SSL certificates for HTTPS
if __name__ == "__main__":
    uvicorn.run(
        app,
        host=backend_host,
        port=backend_port,
        ssl_certfile=ssl_certfile,
        ssl_keyfile=ssl_keyfile
    )
