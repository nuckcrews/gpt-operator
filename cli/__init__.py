from dotenv import load_dotenv

load_dotenv()

import os
import gptop as gptop

try:
    openai_key = os.getenv("OPENAI_API_KEY")
    pinecone_key = os.getenv("PINECONE_API_KEY")
    pinecone_region = os.getenv("PINECONE_REGION")
    pinecone_index = os.getenv("PINECONE_INDEX")

    if not openai_key or not pinecone_key or not pinecone_region or not pinecone_index:
        raise ValueError("One or more required environment variables are missing.")

    gptop.init(
        openai_key=openai_key,
        pinecone_key=pinecone_key,
        pinecone_region=pinecone_region,
        pinecone_index=pinecone_index,
        operation_tokens={}
    )
except ValueError as e:
    print(f"Error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")