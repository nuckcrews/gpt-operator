import json

def llm_response(obj: any) -> str:
    """
    Extracts the top result from the LLM output
    """

    try:
        # Get the content of the first choice in the LLM output
        return obj["choices"][0]["message"]["content"]
    except KeyError:
        # Return None if the required keys are not found
        return None

def llm_json(obj: any):
    """
    Extracts the top result from the LLM output
    and converts it to JSON
    """

    try:
        # Get the content of the first choice in the LLM output
        result = obj["choices"][0]["message"]["content"]
        # Convert the content to JSON and return it
        return json.loads(result)
    except (KeyError, json.JSONDecodeError):
        # Return None if the required keys are not found or if the content is not valid JSON
        return None