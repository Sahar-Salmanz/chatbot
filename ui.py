""" 
UI for the LLM chat application using Streamlit.
"""
import streamlit as st
from app.chat import ChatSession
from data.database import init_db, get_db, upsert_topic, get_top_topics
from data.topic_extractor import extract_topic
import hashlib


init_db()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login_user(name, email, password):
    with get_db() as conn:
        user = conn.execute(
            "SELECT * FROM users WHERE email = ? AND password = ?",
            (email, hash_password(password))
        ).fetchone()
    return user

def register_user(name, email, password):
    try:
        with get_db() as conn:
            conn.execute(
                "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                (name, email, hash_password(password))
            )
        return True
    except Exception:
        return False # email already exists


# Sidebar stats
def show_topic_stats():
    user_email = st.session_state.user_email
    topics = get_top_topics(user_email, limit=5)

    st.sidebar.markdown("---")
    st.sidebar.markdown("#### Your top topics")

    if not topics:
        st.sidebar.caption("No topics yet! Start chatting!")
        return
    
    total = sum(t["count"] for t in topics)

    for i, row in enumerate(topics):
        medal = [":1st_place_medal:", ":2nd_place_medal:", ":3rd_place_medal:"][i] if i < 3 else f"{i + 1}."
        pct = row["count"] / total

        col1, col2 = st.sidebar.columns([3, 1])
        col1.markdown(f"{medal} **{row['topic']}**")
        col2.markdown(f"`{row['count']}x`")
        st.sidebar.progress(pct)

    st.sidebar.caption(f"{total} messages tracked")


# Sidebar
def show_auth_sidebar():
    with st.sidebar:
        st.title("Welcome")

        tab1, tab2 = st.tabs(["Log in", "Sign up"])

        with tab1:
            st.subheader("Log in")
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")

            if st.button("Log in", use_container_width=True):
                user = login_user("", email, password)
                #TODO: add login logic
                if user:
                    st.session_state.logged_in = True
                    st.session_state.user_email = email
                    st.session_state.username = user["name"]
                    st.rerun()
                else:
                    st.error("Invalid email or password")

        with tab2:
            st.subheader("sign up")
            name = st.text_input("Username", key="signup_name")
            email = st.text_input("Email", key="signup_email")
            password = st.text_input("Password", key="signup_password", type="password")

            if st.button("Create account", use_container_width=True):
                #TODO: add sign up logic
                if register_user(name, email, password):
                    st.session_state.logged_in = True
                    st.session_state.user_email = email
                    st.session_state.username = name
                    st.rerun()
                else:
                    st.error("Email already in use")

# Main app
def show_main_app():
    st.sidebar.markdown(f":bust_in_silhouette: **{st.session_state.get('username', st.session_state.user_email)}**")
    st.sidebar.caption(st.session_state.user_email)

    if st.sidebar.button("Log out"):
        st.session_state.clear()
        st.rerun()

    show_topic_stats() # Rankings appear here

    # Main chat area
    st.title(":robot: Chat with LLM")
    st.write(f"Welcome back {st.session_state.get('username', 'User')}!")
    
    # Init chat session once per login
    if "chat" not in st.session_state:
        st.session_state.chat = ChatSession()

    # Render chat history
    for msg in st.session_state.chat.memory.get_history():
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Handle new user message
    if prompt := st.chat_input("Message"):
        # Show user bubble immediately
        with st.chat_message("user"):
            st.write(prompt)
        
        # Extract topic and persist to DB before waiting for LLM
        topic = extract_topic(prompt)
        if topic:
            upsert_topic(st.session_state.user_email, topic)

        # Get LLM response
        with st.chat_message("assistant"):
            with st.spinner("Thinking ..."):
                response = st.session_state.chat.send_user_message(prompt)
            st.write(response)

        # Rerun so sidebar stats update immediately
        st.rerun()



if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if st.session_state.logged_in:
    show_main_app()

else:
    st.title(":robot: Chat with LLM")
    st.write("Use the sidebar to log in or create an account.")
    show_auth_sidebar()

