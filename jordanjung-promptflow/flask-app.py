import os
import logging
from flask import Flask, request, jsonify, send_from_directory
from promptflow.client import PFClient
from promptflow.connections import AzureOpenAIConnection
from promptflow.exceptions import UserErrorException
import traceback
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.ERROR,
                    format='%(asctime)s %(levelname)s: %(message)s',
                    handlers=[logging.FileHandler("app.log"),
                              logging.StreamHandler()])

app = Flask(__name__, static_folder='.')

# Set Azure Blob Storage connection string
connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
os.environ['AZURE_STORAGE_CONNECTION_STRING'] = connect_str

# Create PFClient with Azure OpenAI Connection
open_ai_connection = AzureOpenAIConnection(
    name="open_ai_connection",
    api_key=os.getenv('AZURE_OPENAI_API_KEY'),
    api_base=os.getenv('AZURE_OPENAI_ENDPOINT')
)
pf_client = PFClient(connections={"open_ai_connection": open_ai_connection})

# Set the relative path to your Prompt Flow directory
FLOW_DIR = 'jordanjung-promptflow'

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        user_input = request.json['user_input']
        cwd = os.getcwd()
        flow_path = os.path.join(cwd, FLOW_DIR)
        
        if not os.path.exists(flow_path):
            raise FileNotFoundError(f"The flow directory does not exist: {flow_path}")
        
        flow_result = pf_client.test(flow=flow_path, inputs={'user_input': user_input})
        llm_response = flow_result['llm_response']
        logging.error(f"Raw LLM response: {llm_response}")
        
        try:
            response_data = json.loads(llm_response)
            response_content = response_data['content']
            reference = response_data['reference']
        except json.JSONDecodeError:
            logging.error("Failed to parse LLM response as JSON")
            response_content = "Error: Failed to parse response"
            reference = "Unknown reference status"
        except KeyError as ke:
            logging.error(f"Missing key in response: {ke}")
            response_content = f"Error: Invalid response format - missing {ke}"
            reference = "Unknown reference status"
        
        logging.error(f"Generated response: {response_content}")
        logging.error(f"Reference: {reference}")
        
        return jsonify({
            'response': response_content,
            'reference': reference
        })
    
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        logging.error(error_msg)
        logging.error(traceback.format_exc())
        return jsonify({'error': error_msg}), 500

if __name__ == '__main__':
    # Get port from environment variable or use 5000 as default
    port = int(os.environ.get('PORT', 5000))
    # Run the Flask app, making it externally visible
    app.run(host='0.0.0.0', port=port, debug=False)