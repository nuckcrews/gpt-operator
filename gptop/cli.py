from PyInquirer import prompt
from gptop.operation_utils import create_operation, get_operation, update_operation, remove_operation, remove_namespace


create_command_name = "create_operation"
update_command_name = "update_operation"
get_command_name = "get_operation"
remove_command_name = "remove_operation"
remove_namespace_command_name = "remove_namespace_operation"
prompt_command_name = "prompt"


command_prompt = {
    'type': 'list',
    'name': 'command',
    'message': 'What command would you like to run? (Select One)',
    'choices': [
            create_command_name,
            update_command_name,
            get_command_name,
            remove_command_name,
            remove_namespace_command_name,
            prompt_command_name
    ]
}


def prompt_confirm(name, message, default=True):
    return prompt(
        {
            'type': 'confirm',
            'name': name,
            'message': message,
            'default': default
        }
    ).get(name)

def prompt_string(name, message):
    return prompt(
        {
            'type': 'input',
            'name': name,
            'message': message
        }
    ).get(name)


def prompt_list(name, message, choices):
    return prompt(
        {
            'type': 'list',
            'name': name,
            'message': message,
            'choices': choices
        }
    ).get(name)


def main():
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

            create_operation(namespace, type, name, description, url, path, params)

        elif command == get_command_name:
            id = prompt_string('id', "Operation ID:")
            result = get_operation(namespace=namespace, id=id)
            print(result)

        elif command == update_command_name:
            update_operation()

        elif command == remove_command_name:
            id = prompt_string('id', "Operation ID:")
            remove_operation(namespace=namespace, id=id)

        elif command == remove_namespace_command_name:
            confirmed = prompt_confirm('confirmed', 'Are you sure?', False)
            if confirmed:
                remove_namespace(namespace=namespace)

        keep_going = prompt_confirm('keep_going', 'Do you want to continue?')




if __name__ == "__main__":
    main()
