import os
from dotenv import load_dotenv
import gptop as gptop
from .operations.http import HTTP

# Load environment variables from .env file
load_dotenv()

# Initialize GPTOP with API keys and other configurations
gptop.init(
    openai_key=os.environ.get("OPENAI_API_KEY"),
    pinecone_key=os.environ.get("PINECONE_API_KEY"),
    pinecone_region=os.environ.get("PINECONE_REGION"),
    pinecone_index=os.environ.get("PINECONE_INDEX"),
    operations_types=[HTTP]
)