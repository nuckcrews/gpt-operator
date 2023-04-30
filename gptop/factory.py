from .operation import Operation

__all__ = [
    "allowed_operations",
    "create_operation",
    "create_operation_from_object"
]

# List of allowed operation classes
allowed_operations = list[Operation.__class__]

def create_operation_from_object(obj: any) -> Operation:
    """
    Create an operation instance from a given object.

    :param obj: The object containing the operation data.
    :return: An instance of the corresponding operation class.
    """
    return create_operation(
        obj['id'],
        obj['type'],
        obj['name'],
        obj['description'],
        obj['metadata'],
        obj['schema']
    )

def create_operation(id: str, type: str, name: str, description: str, metadata: any, schema: any) -> Operation:
    """
    Create an operation instance based on the provided parameters.

    :param id: The unique identifier of the operation.
    :param type: The type of the operation.
    :param name: The name of the operation.
    :param description: A description of the operation.
    :param metadata: Additional metadata for the operation.
    :param schema: The schema of the operation.
    :return: An instance of the corresponding operation class.
    """
    for operation_class in allowed_operations:
        if type == operation_class.TYPE():
            return operation_class(
                id,
                type,
                name,
                description,
                metadata,
                schema
            )

    raise ValueError("Tried to create invalid operation type:", type)