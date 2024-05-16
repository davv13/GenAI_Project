__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import os
import uuid
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import Chroma as ChromaDB
import sqlite3


PERSIST_DIRECTORY = "chromadb/"

st.set_page_config(page_title='Hotel Recommendation Assistant')
api_key = st.secrets["OPENAI_API_KEY"] if 'OPENAI_API_KEY' in st.secrets else os.getenv('OPENAI_API_KEY')
if not api_key:
    st.error("API key not found. Please set it as an environment variable or in secrets.toml.")
    st.stop()

PROMPT_TEMPLATE = """
You are an AI trained specifically to provide personalized hotel recommendations based on data from ChromaDB. 
Your responses must directly utilize this data to provide accurate and relevant recommendations. 
Provide recommendations based on the user's preferences mentioned in the query.

Remember to always maintain a friendly and approachable demeanor. When the user greets you or engages in any small talk, respond warmly and politely. 

Encourage further interaction by asking follow-up questions if needed to clarify the user's needs or to deepen the dialogue. 

Recommendations are to be based only on the following context:
{context}
---
Provide hotel recommendations based on the above context: {question}
"""
st.markdown("""
<style>
    .reportview-container .main .block-container { padding-top: 5rem; }
    h1 { text-align: center; color: #FFF; }
    .chatbox-container { position: fixed; bottom: 5rem; left: 50%; transform: translate(-50%, 0); width: 90%; }
    .chat-message { color: white; background-color: #333; border-radius: 5px; padding: 10px; margin-bottom: 10px; }
    .chat-input { color: white; background-color: #333; border-radius: 5px; padding: 10px; margin-top: 20px; }
    .chat-input ::placeholder, input::placeholder, textarea, .stTextInput > div > div > input::placeholder, .stTextArea > textarea { color: white !important; opacity: 1; }
</style>
<h1>Hotel Recommendation Assistant</h1>
""", unsafe_allow_html=True)

vectorstore = ChromaDB(persist_directory=PERSIST_DIRECTORY, embedding_function=OpenAIEmbeddings(api_key=api_key))

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

def submit_query():
    if st.session_state.query_text:
        st.session_state.chat_history.append(("You:", st.session_state.query_text))
        try:
            results = vectorstore.similarity_search_with_relevance_scores(st.session_state.query_text, k=3)
            context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])

            prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
            prompt = prompt_template.format(context=context_text, question=st.session_state.query_text)

            model = ChatOpenAI(model_name='gpt-4-turbo-2024-04-09')
            query_result = model.predict(prompt)

            if len(results) == 0 or results[0][1] < 0.7:
                st.session_state.chat_history.append(("Bot:", "I'm sorry, I couldn't find an answer to your question. Could you provide more details or ask another question?"))
            else:
                st.session_state.chat_history.append(("Bot:", query_result))
                
            st.session_state.query_text = ""

        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.session_state.chat_history.append(("Bot:", "An error occurred while processing your request. Please try again later."))

query_text = st.text_input("", placeholder="Ask a question...", key="query_text", on_change=submit_query)
submit = st.button('Submit', on_click=submit_query)

for message_type, message_text in reversed(st.session_state.chat_history):
    unique_key = str(uuid.uuid4())
    st.text_area(label="", value=f"{message_type} {message_text}", height=110, key=unique_key, disabled=True)
