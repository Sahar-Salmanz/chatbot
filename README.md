# 🤖 LLM Chat App
A conversational AI chat application built with Streamlit and the Anthropic API. Features user authentication, persistent chat history, and automatic topic tracking, showing each user a ranked breakdown of what they talk about most.


## Features
- 💬 **LLM Chat**: real-time conversation powered by Claude (claude-opus-4-5 by default)
- 🔐 **User Auth**: sign up and log in with email/password (SHA-256 hashed)
- 🧠 **Topic Extraction**: every message is automatically classified using KeyBERT
- 📊 **Topic Rankings**: sidebar displays your top 5 most-discussed topics with counts and progress bars
- 🗄️ **SQLite Persistence**: users and topic stats are stored locally in app.db
- 🔄 **Conversation Memory**: full chat history is sent to the LLM on every turn for context


## Project Structure

```
chatbot/
├── ui.py                   # Streamlit entry point (auth, chat UI, sidebar)
├── main.py                 # CLI entry point
├── app/
│   ├── __init__.py
│   ├── config.py           # Env vars and Anthropic client setup
│   ├── client.py           # Anthropic API wrapper with error handling
│   ├── memory.py           # Conversation history manager
│   └── chat.py             # ChatSession (ties client + memory together)
├──data/
│   ├── __init__.py
│   ├── database.py         # SQLite setup, auth queries, topic upsert/fetch
│   └── topic_extractor.py  # KeyBERT-based topic extraction
├── tests/
│   ├── test_chat.py         
│   └── test_memory.py 
├── conftest.py
├── requirements.txt
└── README.md
```


## Getting Started
**1. Clone the repository**
```bash
git clone https://github.com/Sahar-Salmanz/chatbot.git
cd chatbot
```


**2. Install dependencies**
```bash
pip install -r requirements.txt
```


**3. Configure environment variables**

Create a .env file in the project root:
```env
ANTHROPIC_API_KEY=your_api_key_here
```

Get your API key at [Anthropic Console](console.anthropic.com).


**4. Run the app**
```bash
streamlit run ui.py
```

The app will open at [http://localhost:8501](http://localhost:8501). The SQLite database (`app.db`) is created automatically on first run.



## Requirements
```
streamlit
anthropic
python-dotenv
keybert
```

_Note: KeyBERT downloads a BERT model (~90 MB) on first use. Expect a 2–3 second delay on the first message after startup. Subsequent messages are fast._


## How It Works
Message flow
```
User types message
       │
       ▼
extract_topic()       ← KeyBERT scores keywords, returns top phrase
       │
       ▼
upsert_topic()        ← SQLite INSERT or INCREMENT count for this user
       │
       ▼
ChatSession.send_user_message()
       │
       ├── memory.add_user_message()
       ├── client.safe_generate_response()   ← Anthropic API call
       └── memory.add_assistant_message()
       │
       ▼
st.rerun()            ← sidebar stats refresh immediately
```


## Topic extraction

KeyBERT uses BERT embeddings to find the most semantically relevant keyword or keyphrase (1–2 words) in each message. A confidence threshold of 0.3 filters out weak matches so only meaningful topics are stored.

```python
# Example outputs
"How do I train a neural network?"  →  "Neural Network"
"Write a SQL query to join two tables"  →  "Sql Query"
"What's the weather like today?"  →  None  (below threshold)
```


## Database schema
```sql
CREATE TABLE users (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    name     TEXT,
    email    TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL          -- SHA-256 hashed
);

CREATE TABLE topic_stats (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    user_email TEXT NOT NULL,
    topic      TEXT NOT NULL,
    count      INTEGER DEFAULT 1,
    UNIQUE(user_email, topic)       -- upsert-safe
);
```


## Configuration Reference

|Variable|Default|Description|
|--------|-------|-----------|
|`ANTHROPIC_API_KEY`|-|Required. Your Anthropic API key|
|`ANTHROPIC_MODEL`|`claude-opus-4-5`|Model to use for responses|
|`ANTHROPIC_MAX_TOKENS`|`1000`|Max tokens per response|



## License
MIT