import os
import pinecone
import openai


__all__ = ["init"]


def init(openai_key, pinecone_key, pinecone_region, pinecone_index, operation_tokens: dict):
    if not openai_key or not pinecone_key or not pinecone_region or not pinecone_index:
        raise ValueError("All keys and region values must be provided.")

    openai.api_key = openai_key

    pinecone.init(
        api_key=pinecone_key,
        environment=pinecone_region
    )

    os.environ["PINECONE_INDEX"] = pinecone_index

    for key, value in operation_tokens.items():
        if not key or not value:
            raise ValueError("All operation tokens must have valid keys and values.")
        os.environ[key + "_token"] = value