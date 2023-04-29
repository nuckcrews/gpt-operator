<div align="center">
  <img  src="https://user-images.githubusercontent.com/33267791/233712514-b47aabb4-1821-4f67-8214-33d6fe2d6402.png" alt="GPTOP Logo" />
</div>

# GPT Operator

**Enhance your GPT applications with external operations**

GPT Operator (`gptop`) serves as a [call operator](https://en.wikipedia.org/wiki/Operator_assistance) for your application. Simply provide `gptop` with a prompt, and it will determine the required external operation to fulfill the prompt and, if desired, execute that operation on your behalf.

## Features

* Execute operations based on a given prompt
* Create, update, and remove operations in vector database

## Requirements

* Pinecone Vector Database Index
* OpenAI access to gpt-4

## Installation

Install the released version via pip:

```bash
$ pip install gptop
```

[WARNING] The package is currently in Alpha stage, so please exercise caution before using it in production.

## Repository Setup

If you don’t have Python installed, [download it here](https://www.python.org/downloads/).

1. Clone this repository.

2. Navigate to the project directory:

   ```bash
   $ cd gpt-operator
   ```

3. Create a new virtual environment:

   ```bash
   $ virtualenv virt
   $ source virt/bin/activate
   ```

4. Install the requirements:

   ```bash
   $ pip install -r requirements.txt
   ```

5. Make a copy of the example environment variables file:

   ```bash
   $ cp .env.example .env
   ```

6. Add your [OpenAI API key](https://beta.openai.com/account/api-keys) to the newly created `.env` file.

7. Add your [Pinecone API key and Region](https://docs.pinecone.io/docs/quickstart) to the newly created `.env` file.

## CLI

1. Run the application:

    ```bash
    $ ./run.sh
    ```

To set up an operation on your machine, please see the [example](https://github.com/ncrews35/gpt-operator/tree/mainline/example).

## Contributing

We are actively looking for new contributors to help improve and expand the GPT Operator repository. All contributions are welcome! Please feel free to reach out for more information on how you can contribute.
