from PyInquirer import prompt
from gptop.operation_utils import create_operation


create_command_name = "create_operation"
update_command_name = "update_operation"
get_command_name = "get_operation"
remove_command_name = "remove_operation"
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
            prompt_command_name
    ]
}


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
    command = prompt_list(
        'command',
        'What command would you like to run? (Select one)', [
            create_command_name,
            update_command_name,
            get_command_name,
            remove_command_name,
            prompt_command_name
        ]
    )

    print(command)

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
        description = prompt_string(
            'description', "Description:")
        url = prompt_string('url', 'URL:')
        path = prompt_string('path', 'Path:')
        params = prompt_string('params', "Parameters:")

        create_operation(type, name, description, url, path, params)


if __name__ == "__main__":
    main()
