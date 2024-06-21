import json
from dotenv import load_dotenv
import os
from pymongo import MongoClient
import logging
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import MongoDBAtlasVectorSearch
import certifi
from data.vectors.create_vector_db import create_vector_documents

import warnings

# Suppress all warnings
warnings.filterwarnings("ignore")

os.environ['SSL_CERT_FILE'] = certifi.where()
openai_api_key = os.getenv('OPENAI_API_KEY')
db_name = os.getenv('DB_NAME')
collection_name = os.getenv('COLLECTION_NAME')
client = MongoClient(os.getenv('Mongo_DB_URI') + certifi.where())

collection = client[db_name][collection_name]

logger = logging.getLogger('app')

def initialize_vectorstore(vectorstore_path, embeddings):
    # breakpoint()
    checkpoint = read_checkpoint(vectorstore_path)
    if not checkpoint.get("vector_db_created", False):
        create_vector_documents()
        checkpoint["vector_db_created"] = True
        write_checkpoint(vectorstore_path, checkpoint)
    else:
        pass

def get_templates(path):
    with open(f"{path}/sample.txt", "r") as f:
        template_sample = f.read()
    return {"sample_prompt_template":template_sample}

def get_top_documents(response):
    try:
        embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
        vectorStore = MongoDBAtlasVectorSearch( collection, embeddings )
        # breakpoint()
        #fetching the similar documents embedded in mongo db
        # k=3 => getting 3 nearest (top) documents
        documents = vectorStore.similarity_search(response, K=12)
        combined_doc = " ".join([doc.page_content for doc in documents])
        # breakpoint()
        return combined_doc
    except Exception as e:
        logger.error(f"Error in GetAnswer: {str(e)}")
        return "Sorry, I couldn't find an answer to your question."

def init_config():
    with open('demo_bot/data/metadata/config.json') as fobj:
        config_data = json.load(fobj)
    return config_data

def read_checkpoint(vectorstore_path):
    checkpoint_file = os.path.join(vectorstore_path, 'vectorstore_checkpoint.json')
    if os.path.exists(checkpoint_file):
        with open(checkpoint_file, 'r') as f:
            return json.load(f)
    return {"vector_db_created": False}

def write_checkpoint(vectorstore_path, data):
    checkpoint_file = os.path.join(vectorstore_path, 'vectorstore_checkpoint.json')
    with open(checkpoint_file, 'w') as f:
        json.dump(data, f)