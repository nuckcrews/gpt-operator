import os
import json
from uuid import uuid4
import pinecone
from openai.embeddings_utils import get_embedding

index = pinecone.Index(os.getenv("INDEX_NAME"))


class Utils():
    """
    A set of utility objects for managing operations
    """

    @classmethod
    def create_operation(self, namespace, type, name, description, url, path, schema):
        """
        Creates an operation, creates an embedding from it, and
        stores it in a vector database.
        - namespace: The namespace to store the embedding
        - type: The type of operation
        - url: The url of the operation
        - path: The path to the operation
        - schema: The schema of the operation
        - body: The body of the operation

        Also writes the operation ID to the `ops_list.txt` file
        """

        id = str(uuid4())

        content = "; ".join([
            f"Name: {name}",
            f"description: {description}",
            f"type: {type}",
            f"url: {url}",
            f"path: {path}",
            f"schema: {schema}"
        ])

        embedding = get_embedding(content, engine="text-embedding-ada-002")

        op = {
            "id": id,
            "name": name,
            "description": description,
            "type": type,
            "url": url,
            "path": path,
            "schema": json.dumps(json.loads(schema), separators=(',', ': '))
        }

        to_upsert = zip([id], [embedding], [op])

        index.upsert(vectors=list(to_upsert), namespace=namespace)

        print(f"Created operation:\n{op}")

        with open("ops_list.txt", "a") as ops_list:
            ops_list.write("\n" + id)

    @classmethod
    def get_operation(self, namespace: str, id: str):
        """
        Fetches an existing operation from the vector database.
        - namespace: The namespace to store the embedding
        - id: The identifier of the operation

        Returns: The operation represented in json
        """

        result = index.fetch([id], namespace=namespace)
        vectors = result.get('vectors')
        vector = vectors.get(id)

        if not vector:
            return None

        return vector.get('metadata')

    @classmethod
    def update_operation(self, namespace, id, type, name, description, url, path, schema):
        """
        Updates an existing operation, creates a new embedding, and
        overrides the existing operation in the vector database.
        - namespace: The namespace to store the embedding
        - id: The identifier of the operation
        - type: The type of operation
        - url: The url of the operation
        - path: The path to the operation
        - schema: The schema of the operation
        """

        content = "; ".join([
            f"Name: {name}",
            f"description: {description}",
            f"type: {type}",
            f"url: {url}",
            f"path: {path}",
            f"schema: {schema}"
        ])

        embedding = get_embedding(content, engine="text-embedding-ada-002")

        op = {
            "id": id,
            "name": name,
            "description": description,
            "type": type,
            "url": url,
            "path": path,
            "schema": schema
        }

        to_upsert = zip([id], [embedding], [op])

        index.upsert(vectors=list(to_upsert), namespace=namespace)

        print(f"Updated operation: {op}")

    @classmethod
    def remove_operation(self, namespace: str, id: str):
        """
        Removes an existing operation from the vector database.
        - namespace: The namespace to store the embedding
        - id: The identifier of the operation

        Also removes the operation ID from `ops_list.txt` file.
        """

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
        """
        [DANGEROUS] Deletes an entire namespace of operations.
        - namespace: The namespace in the vector database
        """

        index.delete(deleteAll='true', namespace=namespace)
        print(f"Deleted: {namespace}")
