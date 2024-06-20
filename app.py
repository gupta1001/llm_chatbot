from __future__ import print_function
from utils.Start import start_app
import openai
from langchain_community.embeddings import OpenAIEmbeddings
import logging
from utils.Utilities import initialize_vectorstore, \
    get_templates, init_config
from datetime import date
from operator import itemgetter
import os

##### init logging
logger = logging.getLogger('app')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh = logging.FileHandler(f'demo_bot/data/logs/Demo_bot_events_{date.today().strftime("%d-%m-%y")}.log')
fh.setFormatter(formatter)
logger.addHandler(fh)
####

# import warnings

# # Suppress all warnings
# warnings.filterwarnings("ignore")

api_key = os.getenv('OPENAI_API_KEY')

if __name__ == "__main__":
    try:
        print('Starting Demo Bot ...\n')
        openai.api_key = api_key
        
        # print(openai.Model.list())
        # breakpoint()
        openai.api_base = 'https://api.openai.com/v1'
        config_data = init_config()
        vectorstore_path, prompt_template_path = itemgetter('vectorstore_path', 'prompt_template_path')(config_data)
        embeddings = OpenAIEmbeddings(openai_api_key=openai.api_key) 
        store = initialize_vectorstore(vectorstore_path, embeddings)
        templates = get_templates(prompt_template_path)
        logger.info(f'Bot initialization completed.')
        # breakpoint()
        start_app(store, templates)
    except Exception as err:
        logger.error(f"Error encountered in function: [main]: {str(err)}")

 

