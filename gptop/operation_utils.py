import os
import json
from uuid import uuid4
import pinecone
from openai.embeddings_utils import get_embedding
from .operation import Operation


__all__ = ["OperationUtils"]


class OperationUtils():
    """
    A set of utility objects for managing operations
    """

    @classmethod
    def create_operation(self, namespace, type, name, description, metadata, schema):
        """
        Creates an operation, creates an embedding from it, and
        stores it in a vector database.
        - namespace: The namespace to store the embedding
        - type: The type of operation
        - metadata: The predefined metadata of the operation
        - schema: The schema of the operation

        Also writes the operation ID to the `ops_list.txt` file

        Returns: The created operation
        """

        index = pinecone.Index(os.getenv("PINECONE_INDEX"))

        id = str(uuid4())

        operation = Operation(
            id=id,
            type=type,
            name=name,
            description=description,
            metadata=json.dumps(json.loads(metadata), separators=(',', ': ')),
            schema=json.dumps(json.loads(schema), separators=(',', ': '))
        )

        embedding = get_embedding(operation.embedding_obj(),
                                  engine="text-embedding-ada-002")

        to_upsert = zip([id], [embedding], [operation.vector_metadata()])

        index.upsert(vectors=list(to_upsert), namespace=namespace)

        return operation

    @classmethod
    def get_operation(self, namespace: str, id: str):
        """
        Fetches an existing operation from the vector database.
        - namespace: The namespace to store the embedding
        - id: The identifier of the operation

        Returns: The operation represented
        """
        index = pinecone.Index(os.getenv("PINECONE_INDEX"))

        result = index.fetch([id], namespace=namespace)
        vectors = result.get('vectors')
        vector = vectors.get(id)

        if not vector:
            return None

        obj = vector.get('metadata')
        return Operation.from_obj(obj)

    @classmethod
    def update_operation(self, namespace, id, type, name, description, metadata, schema):
        """
        Updates an existing operation, creates a new embedding, and
        overrides the existing operation in the vector database.
        - namespace: The namespace to store the embedding
        - id: The identifier of the operation
        - type: The type of operation
        - metadata: The predefined metadata of the operation
        - schema: The schema of the operation

        Returns: The updated operation
        """

        operation = Operation(
            id=id,
            type=type,
            name=name,
            description=description,
            metadata=json.dumps(json.loads(metadata), separators=(',', ': ')),
            schema=json.dumps(json.loads(schema), separators=(',', ': '))
        )

        index = pinecone.Index(os.getenv("PINECONE_INDEX"))

        embedding = get_embedding(operation.embedding_obj(),
                                  engine="text-embedding-ada-002")

        to_upsert = zip([id], [embedding], [operation.vector_metadata()])

        index.upsert(vectors=list(to_upsert), namespace=namespace)

        return operation

    # def uploadOperations(self, path):


    @classmethod
    def remove_operation(self, namespace: str, id: str):
        """
        Removes an existing operation from the vector database.
        - namespace: The namespace to store the embedding
        - id: The identifier of the operation

        Also removes the operation ID from `ops_list.txt` file.
        """

        index = pinecone.Index(os.getenv("PINECONE_INDEX"))

        index.delete(ids=[id], namespace=namespace)

    @classmethod
    def remove_namespace(self, namespace: str):
        """
        [DANGEROUS] Deletes an entire namespace of operations.
        - namespace: The namespace in the vector database
        """
        index = pinecone.Index(os.getenv("PINECONE_INDEX"))

        index.delete(deleteAll='true', namespace=namespace)
