from utils.Retrieval import GetAnswer
import logging

logger = logging.getLogger('bot_conversation')

class BotConversation:
    def __init__(self) -> None:
        self.conversation_context = ""

    def start_conversation(self):
        self.conversation_context = ""
        print("Starting new conversation ...\n\n")

    def continue_conversation(self):
        print("Continuing current conversation ...\n\n")

    def get_answer(self, query, templates):
        # breakpoint()
        self.truncate_context() 
        self.conversation_context += query
        answer,docs = GetAnswer(query, self.conversation_context, templates)
        self.conversation_context += "\n\n question: "+query +", ans: "+answer + ", prev_docs: "+docs+" \n\n"
        return answer
    
    def truncate_context(self):
        max_length = 10000
        if len(self.conversation_context) > max_length:
            self.conversation_context = self.conversation_context[-max_length:]
