# Anthropic API wrapper
from .config import Config

class AnthropicClient:
    def __init__(self):
        self.api_key = Config.api_key
        self.client = Config.client
        self.model_name = Config.model_name
        self.max_tokens = Config.max_tokens

    def generate_response(self, messages, system=None):
        # Generate a response using the messages API
        kwargs = dict(
            model=self.model_name,
            max_tokens=self.max_tokens,
            messages=messages
        )
        if system:
            kwargs["system"] = system
 
        response = self.client.messages.create(**kwargs)
        return response.content[0].text
    
    # Error handling for network failure or bad response
    def safe_generate_response(self, messages, system=None):
        try:
            return self.generate_response(messages, system=system)
        except Exception as e:
            print(f"Error generating response: {e}")
            return "Sorry, I couldn't generate a response at this time. Please try later."
        