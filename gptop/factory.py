from .operation import Operation

__all__ = [
    "allowed_operations",
    "create_operation",
    "create_operation_from_object"
]

allowed_operations = list[Operation.__class__]


def create_operation_from_object(obj: any):
    return create_operation(
        obj['id'],
        obj['type'],
        obj['name'],
        obj['description'],
        obj['metadata'],
        obj['schema']
    )


def create_operation(id: str, type: str, name: str, description: str, metadata: any, schema: any):
    for operation in allowed_operations:
        if type == operation.TYPE():
            return operation(
                id,
                type,
                name,
                description,
                metadata,
                schema
            )

    raise ValueError("Tried to create invalid operation type:", type)
