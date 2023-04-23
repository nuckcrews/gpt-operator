import json
from .src.operator import Operator
from .utils import announce

def handle(namespace: str, prompt: str):
    """
    Asks the operator to find and execute relevant
    operations based on the provided prompt.
    - prompt: The prompt the operator should handle

    Returns: The output generated from the executed operation(s)
    """
    operator = Operator(namespace=namespace)

    print("Finding operations...")
    operations = operator.find(prompt=prompt)
    if not operations:
        print("Found no operations")
        return
    print(f"Found {len(operations)} operations")

    print("Picking an operation...")
    operation = operator.pick(prompt=prompt, operations=operations)
    if not operation:
        announce("No operation picked")
        return
    announce(operation.name, prefix="Picked operation:\n")

    print("Preparing for execution...")
    data = operator.prepare(prompt=prompt, operation=operation)
    announce(data, prefix="Operation prepared with data:\n")

    print("Executing operation...")
    result = operator.execute(operation=operation, params=data.get(
        "params"), body=data.get("body"))
    announce(result, prefix="Execution result:\n")

    print("Reacting to result...")
    reaction = operator.react(prompt=prompt, operation=operation,
                          values=json.dumps(data), result=result)
    announce(reaction, "Reaction:\n")
