<div align="center">
  <img  src="https://user-images.githubusercontent.com/33267791/233712514-b47aabb4-1821-4f67-8214-33d6fe2d6402.png" alt="GPTOP Logo" />
</div>

# GPT Operator

Empower your GPT applications with external operations

## Setup

1. If you don’t have Python installed, [install it from here](https://www.python.org/downloads/)

2. Clone this repository

3. Navigate into the project directory

   ```bash
   $ cd gpt-operator
   ```

4. Create a new virtual environment

   ```bash
   $ virtualenv virt
   $ source virt/bin/activate
   ```

5. Install the requirements

   ```bash
   $ pip install -r requirements.txt
   ```

6. Make a copy of the example environment variables file

   ```bash
   $ cp .env.example .env
   ```

7. Add your [OpenAI API key](https://beta.openai.com/account/api-keys) to the newly created `.env` file

8. Add your [Pinecone API key and Region](https://docs.pinecone.io/docs/quickstart) to the newly created `.env` file

## Usage

1. Run the application

    ```bash
    $ ./run.sh
    ```

## Contributing

All contributions are welcome! Reach out for more information.
