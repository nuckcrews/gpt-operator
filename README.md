<div align="center">
  <img  src="https://user-images.githubusercontent.com/33267791/233712514-b47aabb4-1821-4f67-8214-33d6fe2d6402.png" alt="GPTOP Logo" />
</div>

# GPT Operator

**Empower your GPT applications with external operations**

GPT Operator (`gptop`) acts as a [call operator](https://en.wikipedia.org/wiki/Operator_assistance) for your application. Provide `gptop` with a prompt and it will figure out what external operaton you need to fulfill that prompt and optionally execute that operation on your behalf.

## Features

* Execute operations based on a given prompt
* Create, update, and remove operations in vector database

## Requirements

* Pinecone Vector Database Index
* OpenAI access to gpt-4

## Setup

If you don’t have Python installed, [install it from here](https://www.python.org/downloads/)

1. Clone this repository

2. Navigate into the project directory

   ```bash
   $ cd gpt-operator
   ```

3. Create a new virtual environment

   ```bash
   $ virtualenv virt
   $ source virt/bin/activate
   ```

4. Install the requirements

   ```bash
   $ pip install -r requirements.txt
   ```

5. Make a copy of the example environment variables file

   ```bash
   $ cp .env.example .env
   ```

6. Add your [OpenAI API key](https://beta.openai.com/account/api-keys) to the newly created `.env` file

7. Add your [Pinecone API key and Region](https://docs.pinecone.io/docs/quickstart) to the newly created `.env` file

## Usage

1. Run the application

    ```bash
    $ ./run.sh
    ```

To set up an operation on your machine, please see the [example](https://github.com/ncrews35/gpt-operator/tree/mainline/example).

## Contributing

All contributions are welcome! Reach out for more information.
