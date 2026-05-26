from keybert import KeyBERT


_model = None # Lazy-load so it doesn't slow down app startup

def get_model():
    global _model
    if _model is None:
        _model = KeyBERT()
    return _model

def extract_topic(message):
    """
    Extract the top keyword/topic from a message using KeyBERT.
    Returns a Title-Cased string (e.g. "Machine Learning") or None
    if no keyword exceeds the confidence threshold.
    """
    keywords = get_model().extract_keywords(
        message,
        keyphrase_ngram_range=(1, 2),
        stop_words="english",
        top_n=1
    )

    if keywords and keywords[0][1] > 0.3: # confidence threshold
        return keywords[0][0].title()
    return None