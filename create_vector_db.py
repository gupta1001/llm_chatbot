from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from pymongo import MongoClient
from langchain_community.document_loaders import UnstructuredMarkdownLoader
import logging
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import MongoDBAtlasVectorSearch
import certifi
from datetime import date

import warnings

# Suppress all warnings
warnings.filterwarnings("ignore")

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
fh = logging.FileHandler(f'demo_bot/data/logs/YourScript_events_{date.today().strftime("%d-%m-%y")}.log')
fh.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(fh)
####





os.environ['SSL_CERT_FILE'] = certifi.where()
client = MongoClient(os.getenv('Mongo_DB_URI') + certifi.where())
api_key = os.getenv('OPENAI_API_KEY')
db_name = os.getenv('DB_NAME')
collection_name = os.getenv('COLLECTION_NAME')
# breakpoint()



collection = client[db_name][collection_name]

def create_document_chunks():
    logger.info('Creating document chunks...')
    docs = []
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

    # only to test if document split was happening properly

    # file_path1 = '/Users/prankurgupta/Desktop/demo_bot/demo_bot_data/ubuntu-docs/brand-store.md'
    # loader = UnstructuredMarkdownLoader(file_path1)
    # data = loader.load()
    # documents = text_splitter.split_documents(data)


    # breakpoint()
    file_path = '/Users/prankurgupta/Desktop/demo_bot/demo_bot_data/ubuntu-docs'
    loaded_files = []
    for subdir, _, files in os.walk(file_path):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(subdir, file)
                logger.info(f'Loading file: {file_path}')
                print(f'Loading file: {file_path}')
                loader = UnstructuredMarkdownLoader(file_path)
                docs.extend(loader.load())
                loaded_files.append(file_path)
    logger.info(f'all files: {loaded_files}')

    # Split the documents into chunks
    documents = text_splitter.split_documents(docs)
    return documents

def create_vectore_documents():
    data = create_document_chunks()
    # breakpoint()
    embeddings = OpenAIEmbeddings(openai_api_key = api_key)
    vectorStore = MongoDBAtlasVectorSearch.from_documents(data, embeddings, collection=collection)

create_vectore_documents()

