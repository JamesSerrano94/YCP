"""
Gemini settings, in one place.

Gemini offers an OpenAI-compatible endpoint, so the existing OpenAI SDK code
keeps working: only the client, the base URL and the model names change.
The API key is read from the GEMINI_API_KEY environment variable and must
never be written into the code.
"""

import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # picks up backend/.env when running locally; Vercel sets real env vars

GEMINI_BASE_URL = os.getenv(
    "GEMINI_BASE_URL",
    "https://generativelanguage.googleapis.com/v1beta/openai/",
)

# Free-tier text model. Change it with the GEMINI_CHAT_MODEL variable if Google
# retires this one.
CHAT_MODEL = os.getenv("GEMINI_CHAT_MODEL", "gemini-3.5-flash-lite")

# Text embedding model. 768 dimensions keeps the precomputed course file small.
EMBEDDING_MODEL = os.getenv("GEMINI_EMBEDDING_MODEL", "gemini-embedding-001")
EMBEDDING_DIMENSIONS = 768


def get_api_key():
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        raise RuntimeError(
            "GEMINI_API_KEY is not set. Add it to backend/.env locally, "
            "or to the project's Environment Variables on Vercel."
        )
    return key


def make_client(api_key=None):
    """An OpenAI SDK client pointed at Gemini."""
    return OpenAI(api_key=api_key or get_api_key(), base_url=GEMINI_BASE_URL)
