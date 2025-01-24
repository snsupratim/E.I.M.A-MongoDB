from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import google.generativeai as genai
import json
from bson.objectid import ObjectId

app = Flask(__name__)

# MongoDB Configuration
client = MongoClient('mongodb+srv://nagsupratim8:cmXzynT1ANQMufEe@cluster0.ksv5a.mongodb.net/knowledge_base?retryWrites=true&w=majority&appName=Cluster0')
db = client['knowledge_base']
collection = db['responses']

# Configure Google Generative AI
genai.configure(api_key="AIzaSyDKlEV9cYN378j8emwqpcPpVa3Nc_GCdAo")
model = genai.GenerativeModel("gemini-1.5-flash")

# Insert dataset into MongoDB if not already present
if collection.count_documents({}) == 0:
    with open('dataset.json', 'r') as file:
        data = json.load(file)
    collection.insert_many(data)
    print("Dataset inserted into MongoDB.")

def query_knowledge_base(query):
    """
    Query MongoDB and generate a response using the Generative AI model.
    """
    documents = collection.find({})
    knowledge_base = [doc['text'] for doc in documents]
    
    context = "\n".join([f"- {item}" for item in knowledge_base])
    prompt = f"The following is a knowledge base of responses:\n{context}\n\nBased on this knowledge base, answer the following question:\n\n{query}"

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"An error occurred: {str(e)}"

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Main route to handle queries and generate responses.
    """
    response = None
    query = None

    if request.method == 'POST':
        query = request.form['query']
        response = query_knowledge_base(query)
    
    return render_template('index.html', response=response, query=query)

@app.route('/add', methods=['POST'])
def add_data():
    """
    Add new data to the MongoDB knowledge base.
    """
    data = request.get_json()
    if 'text' in data:
        # Insert new data into MongoDB
        collection.insert_one({'text': data['text']})
        return jsonify({'message': 'Data added successfully'}), 200
    return jsonify({'error': 'Invalid data format'}), 400

@app.route('/upload-json', methods=['POST'])
def upload_json():
    """
    Upload a JSON file and add its contents to the MongoDB knowledge base.
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        data = json.load(file)
        if isinstance(data, list):
            collection.insert_many(data)
            return jsonify({'message': f'{len(data)} records added successfully'}), 200
        return jsonify({'error': 'Invalid JSON format. Must be a list of objects.'}), 400
    except Exception as e:
        return jsonify({'error': f'Failed to process file: {str(e)}'}), 400

@app.route('/get-all', methods=['GET'])
def get_all_data():
    """
    Retrieve all data from the MongoDB knowledge base.
    """
    documents = collection.find({})
    data = [{'id': str(doc['_id']), 'text': doc['text']} for doc in documents]
    return jsonify(data), 200

@app.route('/delete/<id>', methods=['DELETE'])
def delete_data(id):
    """
    Delete a specific record from the MongoDB knowledge base by ID.
    """
    try:
        result = collection.delete_one({'_id': ObjectId(id)})
        if result.deleted_count > 0:
            return jsonify({'message': 'Data deleted successfully'}), 200
        return jsonify({'error': 'No data found with the given ID'}), 404
    except Exception as e:
        return jsonify({'error': f'Invalid ID format: {str(e)}'}), 400

if __name__ == '__main__':
    app.run(debug=True)
