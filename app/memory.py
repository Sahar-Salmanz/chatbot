"""
    Conversation memory for storing and managing chat history.
    LLMs are stateless, you send the full history every turn. 
    This class manages that state for you.
"""


class ConversationMemory:
    def __init__(self):
        self.history = []

    def add_user_message(self, content):
        self.history.append({"role": "user", "content": content})

    def add_assistant_message(self, content):
        self.history.append({"role": "assistant", "content": content})

    def get_history(self):
        return self.history
    
    def clear_history(self):
        self.history = []
    
    def save_history(self, file_name):
        with open(file_name, 'w') as f:
            for message in self.history:
                f.write(f'{message["role"]}: {message["content"]}\n')
