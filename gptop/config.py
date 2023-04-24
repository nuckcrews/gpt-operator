import os
import pinecone
import openai


__all__ = ["init"]


def init(openai_key, pinecone_key, pinecone_region, pinecone_index):
    openai.api_key = openai_key

    pinecone.init(
        api_key=pinecone_key,
        environment=pinecone_region
    )

    os.environ["PINECONE_INDEX"] = pinecone_index
