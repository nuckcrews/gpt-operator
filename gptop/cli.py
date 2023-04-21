import os
from PyInquirer import prompt
from gptop.operation_utils import Utils
from gptop.operator import Operator


create_command_name = "create_operation"
update_command_name = "update_operation"
get_command_name = "get_operation"
remove_command_name = "remove_operation"
remove_namespace_command_name = "remove_namespace_operation"
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
            params = prompt_string('params', "Parameters:")

            Utils.create_operation(namespace, type, name,
                                   description, url, path, params)

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
                params = prompt_string(
                    'params', "Parameters:", op.get('params'))
                Utils.update_operation(
                    namespace, id, type, name, description, url, path, params)
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


def prompt_string(name, message, default=""):
    return prompt(
        {
            'type': 'input',
            'name': name,
            'message': message,
            'default': default
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
