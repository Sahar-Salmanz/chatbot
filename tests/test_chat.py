# Use a mock API client for testing
# Verify that messages are passed and responses are stored correctly

import pytest
from unittest.mock import patch
from app.chat import ChatSession


@patch("app.chat.AnthropicClient")
def test_chatbot(MockAnthropicClient):
    # Configure the mock to return predictable responses
    mock_client = MockAnthropicClient.return_value
    mock_client.safe_generate_response.side_effect = [
        "I'm good, thank you! How can I assist you today?",
        "The weather is sunny with a high of 25°C."
    ]
 
    chatbot = ChatSession()
 
    # Simulate a conversation
    chatbot.send_user_message("Hello, how are you?")
    chatbot.send_user_message("What is the weather like today?")
 
    # Check that the history is stored correctly on chatbot.memory (not a separate instance)
    history = chatbot.memory.get_history()
    assert len(history) == 4  # 2 user messages + 2 assistant responses
 
    assert history[0]['role'] == 'user'
    assert history[0]['content'] == "Hello, how are you?"
 
    assert history[1]['role'] == 'assistant'
    assert history[1]['content'] == "I'm good, thank you! How can I assist you today?"
 
    assert history[2]['role'] == 'user'
    assert history[2]['content'] == "What is the weather like today?"
 
    assert history[3]['role'] == 'assistant'
    assert history[3]['content'] == "The weather is sunny with a high of 25°C."
 
 
@patch("app.chat.AnthropicClient")
def test_chatbot_passes_history_to_client(MockAnthropicClient):
    # Verify that the full conversation history is passed on each API call.
    # We capture deep copies inside a side_effect function because call_args_list
    # holds references to the same list object, by the time we read it after both
    # sends, the list has grown and all entries reflect the final state.
    mock_client = MockAnthropicClient.return_value
    captured = []
 
    def capture_and_respond(messages, system=None):
        captured.append(list(messages))  # snapshot at call time
        return "Mock response."
 
    mock_client.safe_generate_response.side_effect = capture_and_respond
 
    chatbot = ChatSession()
    chatbot.send_user_message("First message")
    chatbot.send_user_message("Second message")
 
    # First call: only the first user message was in history
    assert len(captured[0]) == 1
    assert captured[0][0] == {"role": "user", "content": "First message"}
 
    # Second call: first user + first assistant + second user
    assert len(captured[1]) == 3
    assert captured[1][0] == {"role": "user", "content": "First message"}
    assert captured[1][1] == {"role": "assistant", "content": "Mock response."}
    assert captured[1][2] == {"role": "user", "content": "Second message"}
 
 
@patch("app.chat.AnthropicClient")
def test_chatbot_uses_system_prompt(MockAnthropicClient):
    # Verify that the system prompt is passed to the client
    mock_client = MockAnthropicClient.return_value
    mock_client.safe_generate_response.return_value = "Mock response."
 
    system_prompt = "You are a weather assistant."
    chatbot = ChatSession(system_prompt=system_prompt)
    chatbot.send_user_message("Hello")
 
    call_kwargs = mock_client.safe_generate_response.call_args[1]
    assert call_kwargs["system"] == system_prompt