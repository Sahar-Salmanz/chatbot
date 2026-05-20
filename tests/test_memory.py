# Tests for history management in memory.
import pytest
from app.memory import ConversationMemory


def test_conversation_memory():
    memory = ConversationMemory()

    # Test adding user message
    memory.add_user_message("Hello, how are you?")
    assert memory.get_history() == [{"role": "user", "content": "Hello, how are you?"}]

    # Test adding assistant message
    memory.add_assistant_message("Hi! I'm good. How can I assist you today?")
    assert memory.get_history() == [
        {"role": "user", "content": "Hello, how are you?"},
        {"role": "assistant", "content": "Hi! I'm good. How can I assist you today?"}
    ]

    # Test clearing history
    memory.clear_history()
    assert memory.get_history() == []

    # Test saving history to file
    memory.add_user_message("Hello, how are you?")
    memory.add_assistant_message("Hi! I'm good. How can I assist you today?")
    memory.save_history("test_history.txt")
    with open("test_history.txt", 'r') as f:
        content = f.read()
        assert content == "user: Hello, how are you?\nassistant: Hi! I'm good. How can I assist you today?\n"
    
    