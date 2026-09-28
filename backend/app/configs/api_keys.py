# app/configs/api_keys.py
import os


class APIKeysConfig:
    # Keys come from environment variables, never from the code.
    yale_course_search_api = os.getenv("YALE_COURSE_SEARCH_API_KEY")
    gemini_api = os.getenv("GEMINI_API_KEY")
