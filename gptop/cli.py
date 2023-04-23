import os
import json
from PyInquirer import prompt
from .src.operation_utils import Utils
from .src.operator import Operator


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
                schema = json.dumps(obj.get("schema"), separators=(',', ': '))
            else:
                type = prompt_list(
                    'type',
                    'Type (Select one):', [
                        'POST',
                        'GET',
                        'PUT',
                        'PATCH',
                        'DELETE'
                    ]
                )
                name = prompt_string('name', "Name:")
                description = prompt_string('description', "Description:")
                url = prompt_string('url', 'URL:')
                path = prompt_string('path', 'Path:')
                schema = prompt_string('schema', "Schema:")

            Utils.create_operation(namespace, type, name,
                                   description, url, path, schema)

        elif command == get_command_name:
            id = prompt_string('id', "Operation ID:")
            result = Utils.get_operation(namespace=namespace, id=id)

            if not result:
                print("Operation does not exist")
            else:
                print(result)

        elif command == update_command_name:
            id = prompt_string('id', "Operation ID:")
            op = Utils.get_operation(namespace=namespace, id=id)

            if op:
                type = prompt_list(
                    'type',
                    'Type (Select one):', [
                        'POST',
                        'GET',
                        'PUT',
                        'PATCH',
                        'DELETE'
                    ],
                    op.get('type')
                )
                name = prompt_string('name', "Name:", op.get('name'))
                description = prompt_string(
                    'description', "Description:", op.get('description'))
                url = prompt_string('url', 'URL:', op.get('url'))
                path = prompt_string('path', 'Path:', op.get('path'))
                schema = prompt_string('schema', "Schema:", op.get('schema'))

                Utils.update_operation(
                    namespace, id, type, name, description, url, path, schema)
            else:
                print("Operation does not exist")

        elif command == remove_command_name:
            id = prompt_string('id', "Operation ID:")
            Utils.remove_operation(namespace=namespace, id=id)

        elif command == remove_namespace_command_name:
            confirmed = prompt_confirm('confirmed', 'Are you sure?', False)
            if confirmed:
                Utils.remove_namespace(namespace=namespace)

        elif command == prompt_command_name:
            pmt = prompt_string('pmt', "Prompt:")
            operator = Operator(namespace=namespace)
            operator.handle(pmt)

        keep_going = prompt_confirm('keep_going', 'Do you want to continue?')


# MARK: -  Helper Methods

def prompt_confirm(name, message, default=True):
    return prompt(
        {
            'type': 'confirm',
            'name': name,
            'message': message,
            'default': default
        }
    ).get(name)


def prompt_string(name, message, default=None):
    return prompt(
        {
            'type': 'input',
            'name': name,
            'message': message,
            'default': default if default else ""
        }
    ).get(name)


def prompt_list(name, message, choices, default=None):
    return prompt(
        {
            'type': 'list',
            'name': name,
            'message': message,
            'choices': choices,
            'default': default
        }
    ).get(name)


if __name__ == "__main__":
    main()
