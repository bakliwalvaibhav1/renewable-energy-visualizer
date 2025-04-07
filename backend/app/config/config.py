import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Ensure required variables are present or raise errors
SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = os.environ["ALGORITHM"]
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"])
LOG_LEVEL = os.environ["LOG_LEVEL"]