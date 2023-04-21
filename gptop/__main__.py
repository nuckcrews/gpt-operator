"""GPTOperator: Connects GPT to the world"""
from dotenv import load_dotenv

load_dotenv()

import gptop.cli

if __name__ == "__main__":
    gptop.cli.main()