from dotenv import load_dotenv

load_dotenv()

import os
import pinecone
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"),
    environment=os.getenv("PINECONE_REGION")
)