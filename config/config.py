import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    ASANA_API_TOKEN = os.getenv("ASANA_API_TOKEN")
    ASANA_WORKSPACE_GID = os.getenv("ASANA_WORKSPACE_GID")