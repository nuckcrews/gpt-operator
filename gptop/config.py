import os
import pinecone
import openai


__all__ = ["init"]


def init(openai_key, pinecone_key, pinecone_region, pinecone_index, operation_tokens: dict):
    if not openai_key or not pinecone_key or not pinecone_region or not pinecone_index:
        raise ValueError("All keys and region values must be provided.")

    try:
        openai.api_key = openai_key
    except Exception as e:
        raise ValueError(f"Error setting OpenAI key: {e}")

    try:
        pinecone.init(
            api_key=pinecone_key,
            environment=pinecone_region
        )
    except Exception as e:
        raise ValueError(f"Error initializing Pinecone: {e}")

    try:
        os.environ["PINECONE_INDEX"] = pinecone_index
    except Exception as e:
        raise ValueError(f"Error setting Pinecone index: {e}")

    for key, value in operation_tokens.items():
        if not key or not value:
            raise ValueError("All operation tokens must have valid keys and values.")
        try:
            os.environ[key + "_token"] = value
        except Exception as e:
            raise ValueError(f"Error setting operation token for {key}: {e}")