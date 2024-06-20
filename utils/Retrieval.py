## TODO Add imports
## TODO Add below:
# 1. errors/exception handling 
# 2. loggers
import os
import logging
import logging
from langchain_openai import ChatOpenAI
from utils.Utilities import get_top_documents


logger = logging.getLogger('app')

openai_api_key = os.getenv('OPENAI_API_KEY')


def GetAnswer(query, prev_context, templates):
    try:
        context = get_top_documents(query)
        # breakpoint()
        prompt = templates["sample_prompt_template"]
        prompt = prompt.format(prev_context=prev_context, context=context, query=query)
        # breakpoint()

        openai_llm = ChatOpenAI(model="gpt-3.5-turbo", max_tokens=1024, streaming=True)
        response = ""
        for chunk in openai_llm.stream(prompt):
            print(chunk.content, end="")
            response += chunk.content
        # breakpoint()
        return response, context

    except Exception as e:
        logger.error(f"Error in GetAnswer: {str(e)}")
        return "Sorry, I couldn't find an answer to your question."

