import json

def llm_response(obj: any) -> str:
    """
    Extracts the top result from the LLM output
    """

    try:
        return obj["choices"][0]["message"]["content"]
    except:
        return None

def llm_json(obj: any):
    """
    Extracts the top result from the LLM output
    and converts it to JSON
    """

    try:
        result = obj["choices"][0]["message"]["content"]
        return json.loads(result)
    except:
        return None

def announce(val, prefix: str=""):
    cyan = '\033[96m'
    default = '\033[0m'
    print("{0}{1}{2}{3}".format( prefix, cyan, val, default))