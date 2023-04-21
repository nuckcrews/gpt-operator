
def llm_response(obj: any) -> str:
        """
        Extracts the top result from the LLM output
        """

        try:
            return obj["choices"][0]["message"]["content"]
        except:
            return None