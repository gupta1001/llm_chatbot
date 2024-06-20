from utils.BotConversation import BotConversation as bot_conv
import logging



logger = logging.getLogger('app')



def start_app(store, templates):
    # breakpoint()
    try:
        print("Started Demo Bot.\n")
        conversation = bot_conv()
        conversation.start_conversation()
        while True:
            query = input("Question: ").strip()
            print("question: ", query)

            if query.lower() == 'stop':
                print("Stopping!!!")
                break

            conversation.get_answer(query, templates)

            next_step = input("\n\nStart new, continue or stop? (start/continue/stop): ").strip().lower()

            if next_step == 'start':
                conversation.start_conversation()
            elif next_step == 'continue':
                conversation.continue_conversation()
            elif next_step == 'stop':
                print("Stopping!!!")
                break
    except Exception as e:
        logger.error(f"Error in start_app: {str(e)}")   