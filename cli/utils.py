from PyInquirer import prompt

# Function to print a colored message
def announce(message, prefix: str = ""):
    cyan = '\033[96m'
    default = '\033[0m'
    print("{0}{1}{2}{3}".format(prefix, cyan, message, default))

# Function to prompt a confirmation question
def prompt_confirm(question_name, question_message, default=True):
    return prompt(
        {
            'type': 'confirm',
            'name': question_name,
            'message': question_message,
            'default': default
        }
    ).get(question_name)

# Function to prompt a string input question
def prompt_string(question_name, question_message, default=None):
    return prompt(
        {
            'type': 'input',
            'name': question_name,
            'message': question_message,
            'default': default if default else "",
            'validate': lambda val: len(val) > 0 or "Please enter a non-empty value"
        }
    ).get(question_name)

# Function to prompt a list selection question
def prompt_list(question_name, question_message, choices, default=None):
    return prompt(
        {
            'type': 'list',
            'name': question_name,
            'message': question_message,
            'choices': choices,
            'default': default
        }
    ).get(question_name)