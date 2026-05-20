""" 
UI for the LLM chat application using Streamlit.
"""
import streamlit as st
from app.chat import ChatSession


st.title(":robot: Chat with LLM")
if "chat" not in st.session_state:
    st.session_state.chat = ChatSession()

for msg in st.session_state.chat.memory.get_history():
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Message"):
    with st.chat_message("user"):
        st.write(prompt)
    response = st.session_state.chat.send_user_message(prompt)
    with st.chat_message("assistant"):
        st.write(response)