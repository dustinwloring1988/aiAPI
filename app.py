from flask import Flask, request, jsonify
import torch
from transformers import AutoModel, AutoTokenizer
from datetime import datetime
import csv
import os
import logging

# Setup logging
logging.basicConfig(filename='app.log', level=logging.INFO)

app = Flask(__name__)

# Constants
MODEL_PATH = 'model/'
API_KEYS_FILE = 'api_keys.txt'
MODEL_LIST_FILE = 'models.csv'
CONVERSATION_FILE = 'conversations.csv'

# Load API keys and models list
with open(API_KEYS_FILE, 'r') as file:
    valid_api_keys = file.read().splitlines()

valid_models = {}
with open(MODEL_LIST_FILE, 'r') as file:
    reader = csv.reader(file)
    next(reader, None)  # skip the headers
    for row in reader:
        huggingface_name = row[0]
        internal_name = row[1]
        description = row[2]
        valid_models[internal_name] = {
            'huggingface_name': huggingface_name,
            'description': description
        }

def validate_api_key(key):
    # Check if the provided key is in the list of valid keys
    if key in valid_api_keys:
        return True
    else:
        logging.warning(f"Invalid API Key attempted: {key}")
        return False

def validate_model(internal_name):
    # Check if the provided model is in the list of valid models
    if internal_name in valid_models:
        return True
    else:
        logging.warning(f"Invalid model attempted: {internal_name}")
        return False

def download_and_save_model(internal_name):
    huggingface_name = valid_models[internal_name]['huggingface_name']
    model = AutoModel.from_pretrained(huggingface_name)
    tokenizer = AutoTokenizer.from_pretrained(huggingface_name)
    model.save_pretrained(MODEL_PATH + internal_name)
    tokenizer.save_pretrained(MODEL_PATH + internal_name)

def load_model(internal_name):
    model = AutoModel.from_pretrained(MODEL_PATH + internal_name)
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH + internal_name)
    return model, tokenizer

def save_conversation(api_key, prompt, response):
    # save the conversation with timestamp
    with open(CONVERSATION_FILE, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now(), api_key, prompt, response])

@app.route('/api/v1/query', methods=['POST'])
def query_model():
    data = request.get_json()
    api_key = data.get('api_key')
    internal_name = data.get('model')
    prompt = data.get('prompt')

    if not validate_api_key(api_key):
        return jsonify({"error": "Invalid API key"}), 403
    if not validate_model(internal_name):
        return jsonify({"error": "Invalid model"}), 400
    
    try:
        if not os.path.exists(MODEL_PATH + internal_name):
            download_and_save_model(internal_name)

        model, tokenizer = load_model(internal_name)
        
        inputs = tokenizer.encode(prompt, return_tensors="pt")
        outputs = model.generate(inputs)
        response = tokenizer.decode(outputs[0])

        # count tokens
        prompt_tokens = len(inputs[0])
        response_tokens = len(outputs[0])

        save_conversation(api_key, prompt, response)

        return jsonify({
            'response': response,
            'prompt_tokens': prompt_tokens,
            'response_tokens': response_tokens
        })

    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
        return jsonify({"error": "An error occurred processing your request"}), 500


if __name__ == '__main__':
    app.run(debug=True)
