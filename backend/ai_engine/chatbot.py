# backend/ai_engine/chatbot.py

from backend.utils.file_reader import read_documents
from backend.ai_engine.summarizer import summarize
from backend.utils.session_memory import add_user_message, get_user_context

def answer_question(user_id, question):
    # Log current message
    add_user_message(user_id, question)

    # Retrieve session memory
    previous_messages = get_user_context(user_id)

    # Merge context and question
    user_context = previous_messages + " " + question

    # Read all docs and pass to summarizer
    all_text = read_documents()
    context_plus_data = user_context + "\n\n" + all_text

    summary = summarize(context_plus_data, num_sentences=6)
    return summary
