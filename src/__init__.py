from dotenv import load_dotenv

load_dotenv()

import os
import src.gptop as gptop

gptop.init(
    openai_key=os.getenv("OPENAI_API_KEY"),
    pinecone_key=os.getenv("PINECONE_API_KEY"),
    pinecone_region=os.getenv("PINECONE_REGION"),
    pinecone_index=os.getenv("PINECONE_INDEX")
)
