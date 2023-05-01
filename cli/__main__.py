"""GPTOperator: Connects GPT to the world"""
import cli.app as app

if __name__ == "__main__":
    # Added try-except block to handle exceptions and prevent potential security vulnerabilities
    try:
        app.main()
    except Exception as e:
        print(f"An error occurred: {e}")