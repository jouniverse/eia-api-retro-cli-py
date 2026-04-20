# Import API key from .env file
from dotenv import load_dotenv
import os

load_dotenv()  # load .env file
API_KEY = os.getenv("API_KEY")
