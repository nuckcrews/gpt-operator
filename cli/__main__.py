"""GPTOperator: Connects GPT to the world"""
import cli.app as app

def main():
    try:
        app.main()
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)

if __name__ == "__main__":
    main()