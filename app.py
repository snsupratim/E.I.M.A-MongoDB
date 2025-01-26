from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import google.generativeai as genai
import csv
import json
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# MongoDB Configuration
client = MongoClient(os.getenv('MONGO_URI'))
db = client['knowledge_base']
collection = db['responses']

# Configure Google Generative AI
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel("gemini-1.5-flash")

# Insert dataset into MongoDB if not already present
if collection.count_documents({}) == 0:
    with open('dataset.json', 'r') as file:
        data = json.load(file)
    sanitized_data = [{'text': item['text']} for item in data if 'text' in item]
    collection.insert_many(sanitized_data)
    print(f"Dataset inserted into MongoDB. {len(sanitized_data)} records added.")

def query_knowledge_base(query):
    documents = collection.find({})
    knowledge_base = [doc.get('text', '') for doc in documents if 'text' in doc]

    if not knowledge_base:
        return "The knowledge base is empty or improperly configured."

    context = "\n".join([f"- {item}" for item in knowledge_base])
    prompt = f"The following is a knowledge base of responses:\n{context}\n\nBased on this knowledge base, answer the following question:\n\n{query}"

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"An error occurred: {str(e)}"

@app.route('/', methods=['GET', 'POST'])
def index():
    response = None
    query = None

    if request.method == 'POST':
        query = request.form['query']
        response = query_knowledge_base(query)
    
    return render_template('index.html', response=response, query=query)

@app.route('/add', methods=['POST'])
def add_data():
    data = request.get_json()
    if 'text' in data and isinstance(data['text'], str):
        collection.insert_one({'text': data['text']})
        return jsonify({'message': 'Data added successfully'}), 200
    return jsonify({'error': 'Invalid data format'}), 400

@app.route('/upload-data', methods=['POST'])
def upload_data():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        # Handle JSON files
        if file.filename.endswith('.json'):
            data = json.load(file)
            if isinstance(data, list):
                sanitized_data = [{'text': item['text']} for item in data if 'text' in item]
                collection.insert_many(sanitized_data)
                return jsonify({'message': f'{len(sanitized_data)} records added successfully'}), 200
            return jsonify({'error': 'Invalid JSON format. Must be a list of objects.'}), 400

        # Handle CSV files
        elif file.filename.endswith('.csv'):
            csv_data = []
            csv_reader = csv.DictReader(file.stream.read().decode('utf-8').splitlines())
            for row in csv_reader:
                if 'text' in row:
                    csv_data.append({'text': row['text']})
            if csv_data:
                collection.insert_many(csv_data)
                return jsonify({'message': f'{len(csv_data)} records added successfully'}), 200
            return jsonify({'error': 'CSV file is empty or improperly formatted'}), 400

        # Unsupported file type
        else:
            return jsonify({'error': 'Unsupported file format. Please upload a JSON or CSV file.'}), 400

    except Exception as e:
        return jsonify({'error': f'Failed to process file: {str(e)}'}), 400



if __name__ == '__main__':
    app.run(debug=True)
