from PyInquirer import prompt, ValidationError, Validator


class NotEmptyValidator(Validator):
    def validate(self, document):
        if not document.text:
            raise ValidationError(
                message="This field cannot be empty",
                cursor_position=len(document.text),
            )


def announce(val, prefix: str = ""):
    cyan = "\033[96m"
    default = "\033[0m"
    print("{0}{1}{2}{3}".format(prefix, cyan, val, default))


def prompt_confirm(name, message, default=True):
    try:
        return prompt(
            {
                "type": "confirm",
                "name": name,
                "message": message,
                "default": default,
            }
        ).get(name)
    except Exception as e:
        print(f"Error: {e}")
        return None


def prompt_string(name, message, default=None):
    try:
        return prompt(
            {
                "type": "input",
                "name": name,
                "message": message,
                "default": default if default else "",
                "validate": NotEmptyValidator,
            }
        ).get(name)
    except Exception as e:
        print(f"Error: {e}")
        return None


def prompt_list(name, message, choices, default=None):
    try:
        return prompt(
            {
                "type": "list",
                "name": name,
                "message": message,
                "choices": choices,
                "default": default,
            }
        ).get(name)
    except Exception as e:
        print(f"Error: {e}")
        return None