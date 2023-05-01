import os
import json
from .handler import handle
from gptop.operation_utils import OperationUtils
from .utils import announce, prompt_confirm, prompt_list, prompt_string

# Define command names
create_command_name = "create_operation"
update_command_name = "update_operation"
get_command_name = "get_operation"
remove_command_name = "remove_operation"
clear_namespace_command_name = "clear_namespace"
prompt_command_name = "prompt"


def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    namespace = prompt_string('namespace', "Namespace:")

    keep_going = True
    while keep_going:
        command = prompt_list(
            'command',
            'What command would you like to run? (Select one)', [
                create_command_name,
                update_command_name,
                get_command_name,
                remove_command_name,
                clear_namespace_command_name,
                prompt_command_name
            ]
        )

        if command == create_command_name:
            from_file = prompt_confirm('from_file', "Create from file?")
            if from_file:
                file_path = prompt_string('file_path', "Path to file:")
                with open(file_path, "r") as file:
                    obj = json.load(file)

                operation_type = obj.get("type")
                name = obj.get("name")
                description = obj.get("description")
                metadata = json.dumps(obj.get("metadata"), separators=(',', ': '))
                schema = json.dumps(obj.get("schema"), separators=(',', ': '))
            else:
                operation_type = prompt_list(
                    'type',
                    'Type (Select one):', [
                        'COMMAND',
                        'DOWNLOAD',
                        'HTTP'
                    ],
                )
                name = prompt_string('name', "Name:")
                description = prompt_string('description', "Description:")
                metadata = prompt_string('metadata', 'Metadata:')
                schema = prompt_string('schema', "Schema:")

            op = OperationUtils.create_operation(namespace, operation_type,
                                                 name, description, metadata, schema)

            with open("./example/ops_list.txt", "a") as ops_list:
                ops_list.write("\n" + op.id)

            announce(op, prefix="Created operation:\n")

        elif command == get_command_name:
            operation_id = prompt_string('id', "Operation ID:")
            result = OperationUtils.get_operation(namespace=namespace, id=operation_id)

            if not result:
                announce("Operation does not exist")
            else:
                announce(result, prefix="Operation:\n")

        elif command == update_command_name:
            operation_id = prompt_string('id', "Operation ID:")
            op = OperationUtils.get_operation(namespace=namespace, id=operation_id)
            announce(op, prefix="Existing Operation:\n")

            if op:
                operation_type = prompt_list(
                    'type',
                    'Type (Select one):', [
                        'COMMAND',
                        'DOWNLOAD',
                        'HTTP'
                    ],
                    op.type
                )
                name = prompt_string('name', "Name:", op.name)
                description = prompt_string(
                    'description', "Description:", op.description)
                metadata = prompt_string('metadata', 'Metadata:', op.metadata)
                schema = prompt_string('schema', "Schema:", op.schema)

                op = OperationUtils.update_operation(namespace, operation_id, operation_type, name,
                                                     description, metadata, schema)

                announce(op, prefix="Updated operation:\n")
            else:
                announce("Operation does not exist")

        elif command == remove_command_name:
            operation_id = prompt_string('id', "Operation ID:")
            OperationUtils.remove_operation(namespace=namespace, id=operation_id)

            with open("./example/ops_list.txt", "r") as input:
                with open("./example/temp.txt", "w") as output:
                    for line in input:
                        if line.strip("\n") != operation_id:
                            output.write(line)

            # Replaced os.replace with os.rename for better compatibility
            os.rename('./example/temp.txt', './example/ops_list.txt')  # Change made: Replaced os.replace with os.rename

            announce(operation_id, prefix="Deleted: ")

        elif command == clear_namespace_command_name:
            confirmed = prompt_confirm('confirmed', 'Are you sure?', False)
            if confirmed:
                OperationUtils.remove_namespace(namespace=namespace)
                announce(namespace, prefix="Deleted: ")

        elif command == prompt_command_name:
            pmt = prompt_string('pmt', "Prompt:")
            handle(namespace, pmt)

        keep_going = prompt_confirm('keep_going', 'Do you want to continue?')


if __name__ == "__main__":
    main()