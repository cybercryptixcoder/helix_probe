
import random

def chatbot(input_string):
    responses = [
        "Hello, World!",
        "I'm good, thanks. How can I assist you today?",
        "Sorry to hear that. Is there anything I can do to help you feel better?",
        "I don't understand what you mean by '{input_string}'. Can you explain?",
    ]
    response = random.choice(responses)
    return response
