import os
import pinecone
import openai
from .operation import Operation
import gptop.factory

__all__ = ["init"]


def init(openai_key, pinecone_key, pinecone_region, pinecone_index, operations_types: list[Operation.__class__] = []):
    # Check if all required keys and values are provided
    if not openai_key or not pinecone_key or not pinecone_region or not pinecone_index:
        raise ValueError("All keys and region values must be provided.")

    # Set OpenAI API key
    openai.api_key = openai_key

    # Initialize Pinecone with provided API key and region
    pinecone.init(
        api_key=pinecone_key,
        environment=pinecone_region
    )

    # Set Pinecone index as an environment variable
    os.environ["PINECONE_INDEX"] = pinecone_index

    # Set allowed operations for GPT-OP
    gptop.factory.allowed_operations = operations_types