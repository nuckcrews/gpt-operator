import os
import pinecone
import openai
from .operation import Operation
import gptop.factory

__all__ = ["init"]


def init(openai_key, pinecone_key, pinecone_region, pinecone_index, operations_types: list[Operation.__class__] = []):
    if not openai_key or not pinecone_key or not pinecone_region or not pinecone_index:
        raise ValueError("All keys and region values must be provided.")

    openai.api_key = openai_key

    pinecone.init(
        api_key=pinecone_key,
        environment=pinecone_region
    )

    os.environ["PINECONE_INDEX"] = pinecone_index

    gptop.factory.allowed_operations = operations_types