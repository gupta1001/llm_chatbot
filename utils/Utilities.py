## TODO Add imports
import json
## TODO Add below:
# 1. errors/exception handling 
# 2. loggers
from dotenv import load_dotenv
import os
from pymongo import MongoClient
import logging
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import MongoDBAtlasVectorSearch
import certifi

import warnings

# Suppress all warnings
warnings.filterwarnings("ignore")

os.environ['SSL_CERT_FILE'] = certifi.where()
openai_api_key = os.getenv('OPENAI_API_KEY')
db_name = os.getenv('DB_NAME')
collection_name = os.getenv('COLLECTION_NAME')
client = MongoClient(os.getenv('Mongo_DB_URI') + certifi.where())

collection = client[db_name][collection_name]

def initialize_vectorstore(vectorstore_path, embeddings):
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
        logging.error(f"Error in GetAnswer: {str(e)}")
        return "Sorry, I couldn't find an answer to your question."

def init_config():
    with open('demo_bot/data/metadata/config.json') as fobj:
        config_data = json.load(fobj)
    return config_data
