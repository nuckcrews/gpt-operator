import json
from gptop.operator import Operator
from .utils import announce

def handle(namespace: str, prompt: str):
    """
    Asks the operator to find and execute relevant
    operations based on the provided prompt.
    - prompt: The prompt the operator should handle

    Returns: The output generated from the executed operation(s)
    """
    operator_instance = Operator(namespace=namespace)

    print("Finding operations...")
    found_operations = operator_instance.find(prompt=prompt)
    if not found_operations:
        print("Found no operations")
        return
    announce(f"Found {len(found_operations)} operations")

    print("Picking an operation...")
    selected_operations = operator_instance.pick(prompt=prompt, operations=found_operations)
    if not selected_operations[0]:
        announce("No operation picked")
        return
    selected_operation = selected_operations[0]
    announce(selected_operation.name, prefix="Picked operation:\n")

    print("Preparing for execution...")
    prepared_input = operator_instance.prepare(prompt=prompt, operation=selected_operation)
    announce(prepared_input, prefix="Operation prepared with input:\n")

    print("Executing operation...")
    execution_result = operator_instance.execute(operation=selected_operation, input=prepared_input)
    announce(execution_result, prefix="Execution result:\n")

    print("Reacting to result...")
    reaction_result = operator_instance.react(prompt=prompt, operation=selected_operation,
                              values=json.dumps(prepared_input), result=execution_result)
    announce(reaction_result, "Reaction:\n")