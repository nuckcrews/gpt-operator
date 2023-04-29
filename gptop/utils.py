import json

def llm_response(obj: any) -> str:
    """
    Extracts the top result from the LLM output
    """

    try:
        return obj["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError):
        return None

def llm_json(obj: any):
    """
    Extracts the top result from the LLM output
    and converts it to JSON
    """

    try:
        result = obj["choices"][0]["message"]["content"]
        return json.loads(result)
    except (KeyError, IndexError, TypeError, json.JSONDecodeError):
        return None