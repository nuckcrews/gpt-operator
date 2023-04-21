import os
from uuid import uuid4
import pinecone
from openai.embeddings_utils import get_embedding

INDEX_NAME = os.getenv("INDEX_NAME")

index = pinecone.Index(INDEX_NAME)

class Utils():

    @classmethod
    def create_operation(self, namespace, type, name, description, url, path, params):
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

        index.upsert(vectors=list(to_upsert), namespace=namespace)

        print(f"Created operation:\n{op}")

        with open("ops_list.txt", "a") as ops_list:
            ops_list.write(id)

    @classmethod
    def get_operation(self, namespace: str, id: str):
        result = index.fetch([id], namespace=namespace)
        vectors = result.get('vectors')
        vector = vectors.get(id)

        if not vector:
            return None

        return vector.get('metadata')

    @classmethod
    def update_operation(self, namespace, id, type, name, description, url, path, params):
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

        index.upsert(vectors=list(to_upsert), namespace=namespace)

        print(f"Updated operation: {op}")

    @classmethod
    def remove_operation(self, namespace: str, id: str):
        index.delete(ids=[id], namespace=namespace)

        with open("ops_list.txt", "r") as input:
            with open("temp.txt", "w") as output:
                for line in input:
                    if line.strip("\n") != id:
                        output.write(line)

        os.replace('temp.txt', 'ops_list.txt')

        print(f"Deleted: {id}")

    @classmethod
    def remove_namespace(self, namespace: str):
        index.delete(deleteAll='true', namespace=namespace)
        print(f"Deleted: {namespace}")
