from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

import os
import gptop as gptop
from .operations.http import HTTP

# Initialize GPTOP with API keys and other configurations
gptop.init(
    openai_key=os.getenv("OPENAI_API_KEY"),
    pinecone_key=os.getenv("PINECONE_API_KEY"),
    pinecone_region=os.getenv("PINECONE_REGION"),
    pinecone_index=os.getenv("PINECONE_INDEX"),
    operations_types=[HTTP]
)