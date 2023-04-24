from PyInquirer import prompt


def announce(val, prefix: str = ""):
    cyan = '\033[96m'
    default = '\033[0m'
    print("{0}{1}{2}{3}".format(prefix, cyan, val, default))


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
