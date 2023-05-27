# Chat Model API

This Python script utilizes Flask to create an API for conversational AI models. It is built with Transformers and PyTorch libraries, and supports models hosted on Hugging Face's Model Hub.

## Setup

1.  **Python and Required Libraries**
    
    Make sure you have Python 3.6+ installed on your machine. You can download it from [Python's official website](https://www.python.org/downloads/).
    
    The following libraries are also needed: Flask, PyTorch, Transformers, tqdm. You can install these with pip:
    
    ```bash
    
    pip install flask torch transformers tqdm 

    ```
    
2.  **API Keys**
    
    For security reasons, the script checks if API requests are made with valid API keys. The valid keys are stored in `api_keys.txt`. You should add your keys to this file, with one key per line.
    
3.  **Models List**
    
    The available models are listed in `models.csv`. This CSV file has three columns:
    
    * The model's Hugging Face name
    * An internal name used by the script
    * A description of the model
    
    Models are downloaded and saved using their Hugging Face names, but they are saved locally and loaded with the internal name. Add any models you want to support to this file.
    

## Running the API

To start the API, run the `app.py` script:

```bash

python app.py 

```

The API endpoint will be available at `localhost:5000/api/v1/query`.

You can then make POST requests to this endpoint with the following JSON data:

```json

{
    "api_key": "<your_api_key>",
    "model": "<internal_model_name>",
    "prompt": "<your_prompt>"
} 

```

The API will return a JSON response with the generated text and the number of tokens in the prompt and response.

## Error Handling and Logging

The script logs warnings and errors to `app.log`. Invalid API keys and model names will generate warnings, while exceptions during model loading or text generation will generate errors.

## Saving Conversations

The script saves all conversations to `conversations.csv`, including the timestamp, API key used, prompt, and response.
