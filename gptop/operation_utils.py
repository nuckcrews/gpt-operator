import os
from uuid import uuid4
import pinecone
import openai
from openai.embeddings_utils import get_embedding

openai.api_key = os.getenv("OPENAI_API_KEY")

pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"),
    environment=os.getenv("PINECONE_REGION")
)

INDEX_NAME = os.getenv("INDEX_NAME")

index = pinecone.Index(INDEX_NAME)


def create_operation(namespace, type, name, description, url, path, params):
    id = str(uuid4())

    content = "; ".join([
        f"Name: {name}",
        f"description: {description}",
        f"type: {type}",
        f"url: {url}",
        f"path: {path}",
        f"params: {params}"
    ])

    embedding = get_embedding(content, engine="text-embedding-ada-002")

    op = {
        "id": id,
        "name": name,
        "description": description,
        "type": type,
        "url": url,
        "path": path,
        "params": params
    }

    to_upsert = zip([id], [embedding], [op])

    print(f"Operation:\n{op}")

    with open("ops_list.txt", "a") as ops_list:
        ops_list.write(id)

    index.upsert(vectors=list(to_upsert), namespace=namespace)

    pass


def get_operation(namespace: str, id: str):
    result = index.fetch([id], namespace=namespace)
    vectors = result.get('vectors')
    vector = vectors.get(id)

    return vector.get('metadata')


def update_operation(namespace: str, id: str):
    pass


def remove_operation(namespace: str, id: str):
    index.delete(ids=[id], namespace=namespace)

    with open("ops_list.txt", "r") as input:
        with open("temp.txt", "w") as output:
            for line in input:
                if line.strip("\n") != id:
                    output.write(line)

    os.replace('temp.txt', 'ops_list.txt')

    print(f"Deleted: {id}")

def remove_namespace(namespace: str):
    index.delete(deleteAll='true', namespace=namespace)
    print(f"Deleted: {namespace}")
