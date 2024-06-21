from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from pymongo import MongoClient
from langchain_community.document_loaders import UnstructuredMarkdownLoader
import logging
from langchain_community.embeddings.openai import OpenAIEmbeddings
from langchain_community.vectorstores import MongoDBAtlasVectorSearch
import certifi
import warnings
warnings.filterwarnings("ignore")


logger = logging.getLogger('app')


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
    file_path = os.getenv('DIRECTORY_PATH')
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

def create_vector_documents():
    data = create_document_chunks()
    # breakpoint()
    try:
        embeddings = OpenAIEmbeddings(openai_api_key = api_key)
        vectorStore = MongoDBAtlasVectorSearch.from_documents(data, embeddings, collection=collection)
    except Exception as e:
        logger.error(f'error in creating document embeddings: {e}')


