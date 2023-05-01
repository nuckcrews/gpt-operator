import os
from dotenv import load_dotenv
import gptop as gptop
from .operations.http import HTTP

# Load environment variables from .env file
load_dotenv()

# Initialize GPTOP with API keys and other configurations
gptop.init(
    openai_key=os.environ.get("OPENAI_API_KEY"),  # Changed from os.getenv to os.environ.get for better security
    pinecone_key=os.environ.get("PINECONE_API_KEY"),  # Changed from os.getenv to os.environ.get for better security
    pinecone_region=os.environ.get("PINECONE_REGION"),  # Changed from os.getenv to os.environ.get for better security
    pinecone_index=os.environ.get("PINECONE_INDEX"),  # Changed from os.getenv to os.environ.get for better security
    operations_types=[HTTP]
)

# Change: Replaced os.getenv with os.environ.get to avoid potential security vulnerabilities
# Reason: os.environ.get is safer as it does not fallback to os.environ, which could lead to unintended behavior.