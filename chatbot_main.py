from dotenv import load_dotenv
from backend.core import run_llm
import streamlit as st
from streamlit_chat import message

load_dotenv()

st.set_page_config(page_title="OnePiece-ChatBot", page_icon=":robot:")
st.header("Welcome to OnePiece - ChatBot")

prompt = st.text_input("Ask your question", placeholder="Enter your input here...")

if ( 'chat_answers_history' not in st.session_state 
    and 'chat_history' not in st.session_state
    and 'user_prompt_history' not in st.session_state
    ):
    st.session_state['chat_answers_history'] = []
    st.session_state['chat_history'] = []
    st.session_state['user_prompt_history'] = []

if prompt:
    with st.spinner("Generating response..."):
        generated_response = run_llm(prompt, chat_history=st.session_state['chat_history'])

        st.session_state['user_prompt_history'].append(prompt)
        st.session_state['chat_answers_history'].append(generated_response)
        st.session_state['chat_history'].append(('human', prompt))
        st.session_state['chat_history'].append(('ai',generated_response))

if st.session_state['chat_answers_history']:
    for gen_response, user_query in zip(st.session_state['chat_answers_history'], st.session_state['user_prompt_history']):
        message(user_query, is_user=True)
        message(gen_response)