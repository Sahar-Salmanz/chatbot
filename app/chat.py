# chat logic, message loop
from .memory import ConversationMemory
from .client import AnthropicClient

class ChatSession:
    def __init__(self, system_prompt="You are a helpful assistant."):
        self.client = AnthropicClient()
        self.memory = ConversationMemory()
        self.system_prompt = system_prompt

    def send_user_message(self, content):
        self.memory.add_user_message(content)
        response = self.client.safe_generate_response(
            messages = self.memory.get_history(), 
            system = self.system_prompt
        )
        self.memory.add_assistant_message(response)
        return response
    
    def clear(self):
        self.memory.clear_history()