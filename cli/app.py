import os
import json
from .handler import handle
from gptop.operation_utils import Utils
from .utils import announce, prompt_confirm, prompt_list, prompt_string


create_command_name = "create_operation"
update_command_name = "update_operation"
get_command_name = "get_operation"
remove_command_name = "remove_operation"
remove_namespace_command_name = "remove_namespace"
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
                remove_namespace_command_name,
                prompt_command_name
            ]
        )

        if command == create_command_name:
            from_file = prompt_confirm('from_file', "Create from file?")
            if from_file:
                file_path = prompt_string('file_path', "Path to file:")
                file = open(file_path, "r")
                obj = file.read()
                print(obj)
                obj = json.loads(obj)
                file.close()

                type = obj.get("type")
                name = obj.get("name")
                description = obj.get("description")
                url = obj.get("url")
                path = obj.get("path")
                auth = obj.get("auth")
                schema = json.dumps(obj.get("schema"), separators=(',', ': '))
            else:
                type = prompt_list(
                    'type',
                    'Type (Select one):', [
                        'POST', 'GET', 'PUT', 'PATCH', 'DELETE'],
                )
                name = prompt_string('name', "Name:")
                description = prompt_string('description', "Description:")
                url = prompt_string('url', 'URL:')
                path = prompt_string('path', 'Path:')
                auth = prompt_confirm(
                    'auth', 'Requires Authentication:', False)
                schema = prompt_string('schema', "Schema:")

            op = Utils.create_operation(namespace, type, name,
                                        description, url, path, auth, schema)

            with open("./example/ops_list.txt", "a") as ops_list:
                ops_list.write("\n" + op.id)

            announce(op, prefix="Created operation:\n")

        elif command == get_command_name:
            id = prompt_string('id', "Operation ID:")
            result = Utils.get_operation(namespace=namespace, id=id)

            if not result:
                announce("Operation does not exist")
            else:
                announce(result, prefix="Operation:\n")

        elif command == update_command_name:
            id = prompt_string('id', "Operation ID:")
            op = Utils.get_operation(namespace=namespace, id=id)
            announce(op, prefix="Existing Operation:\n")

            if op:
                type = prompt_list(
                    'type',
                    'Type (Select one):', [
                        'POST', 'GET', 'PUT', 'PATCH', 'DELETE'],
                    op.type
                )
                name = prompt_string('name', "Name:", op.name)
                description = prompt_string(
                    'description', "Description:", op.description)
                url = prompt_string('url', 'URL:', op.url)
                path = prompt_string('path', 'Path:', op.path)
                auth = prompt_confirm(
                    'auth', 'Requires Authentication:', op.requires_auth)
                schema = prompt_string('schema', "Schema:", op.schema)

                op = Utils.update_operation(namespace, id, type, name,
                                            description, url, path, auth, schema)

                announce(op, prefix="Updated operation:\n")
            else:
                announce("Operation does not exist")

        elif command == remove_command_name:
            id = prompt_string('id', "Operation ID:")
            Utils.remove_operation(namespace=namespace, id=id)

            with open("./example/ops_list.txt", "r") as input:
                with open("./example/temp.txt", "w") as output:
                    for line in input:
                        if line.strip("\n") != id:
                            output.write(line)

            os.replace('./example/temp.txt', './example/ops_list.txt')

            announce(id, prefix="Deleted: ")

        elif command == remove_namespace_command_name:
            confirmed = prompt_confirm('confirmed', 'Are you sure?', False)
            if confirmed:
                Utils.remove_namespace(namespace=namespace)
                announce(namespace, prefix="Deleted: ")

        elif command == prompt_command_name:
            pmt = prompt_string('pmt', "Prompt:")
            handle(namespace, pmt)

        keep_going = prompt_confirm('keep_going', 'Do you want to continue?')


if __name__ == "__main__":
    main()
