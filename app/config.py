# settings and env vars
from dotenv import load_dotenv
load_dotenv()

import anthropic
import os

class Config:
    # Anthropic API key
    api_key = os.getenv("ANTHROPIC_API_KEY")

    # Anthropic model to use
    model_name = os.getenv("ANTHROPIC_MODEL", "claude-opus-4-5")

    # Anthropic API client
    client = anthropic.Anthropic(api_key=api_key)

    # Max tokens for the response
    max_tokens = int(os.getenv("ANTHROPIC_MAX_TOKENS", 1000))
