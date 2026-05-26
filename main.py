"""
    CLI
    Main entry point for the chatbot application. 
    This script initializes the chat session and handles user input in a loop until the user decides to exit.
"""
from app.chat import ChatSession


def main():
    print("Chatbot started. Type 'quit' or 'exit' to stop.\n")
    chat_session = ChatSession()

    while True:
        user_input = input("You: ").strip()

        if not user_input:
            continue
        if user_input.lower() in ["exit", "quit", "q"]:
            print("Exiting chat session. Goodbye!")
            break
        response = chat_session.send_user_message(user_input)
        print(f"Assistant: {response}\n")

if __name__ == "__main__":
    main()
    