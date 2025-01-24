import streamlit as st
import google.generativeai as genai
from pymongo import MongoClient
import json

# MongoDB Configuration
client = MongoClient("mongodb+srv://nagsupratim8:cmXzynT1ANQMufEe@cluster0.ksv5a.mongodb.net/knowledge_base?retryWrites=true&w=majority&appName=Cluster0")
db = client['knowledge_base']
collection = db['responses']

# Configure Google Generative AI
genai.configure(api_key="AIzaSyDKlEV9cYN378j8emwqpcPpVa3Nc_GCdAo")
model = genai.GenerativeModel("gemini-1.5-flash")


def query_knowledge_base(query):
    """Query MongoDB and generate a response using the model."""
    documents = collection.find({})
    knowledge_base = [doc['text'] for doc in documents]
    
    context = "\n".join([f"- {item}" for item in knowledge_base])
    prompt = f"The following is a knowledge base of responses:\n{context}\n\nBased on this knowledge base, answer the following question:\n\n{query}"

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Streamlit UI
st.set_page_config(page_title="College Knowledge Base", page_icon=":mortar_board:", layout="centered")

# Page Title and Description
st.title("College Knowledge Base")
st.write("Ask any questions related to college life, academics, and more.")

# User input for query
query = st.text_input("Ask your question here:")

if query:
    response = query_knowledge_base(query)
    st.subheader("Response:")
    st.write(response)
else:
    st.write("Enter a question to get started.")

# Add new data to MongoDB (this part can be extended for admin functionality)
st.markdown("---")
st.write("**Admin**: Add new data to the knowledge base.")
new_data = st.text_area("New Data Text", height=100)

if st.button("Add Data") and new_data:
    collection.insert_one({'text': new_data})
    st.success("Data added successfully.")

# JSON Upload Section
st.markdown("---")
st.write("**Admin**: Upload a JSON file to bulk add data to the knowledge base.")
uploaded_file = st.file_uploader("Upload a JSON file", type=["json"])

if uploaded_file:
    try:
        # Parse the uploaded JSON file
        data = json.load(uploaded_file)
        if isinstance(data, list):
            # Insert all entries into the collection
            collection.insert_many(data)
            st.success(f"{len(data)} records added successfully.")
        else:
            st.error("The JSON file must contain an array of objects.")
    except Exception as e:
        st.error(f"Failed to process the file: {e}")
