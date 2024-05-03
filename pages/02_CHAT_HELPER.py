import vertexai
from vertexai.preview.generative_models import GenerativeModel, ChatSession
import streamlit as st

st.set_page_config(layout="wide")

st.image("VibezAl-horizontal with text.svg", width=200)

# Add the app name in the sidebar
st.sidebar.image("VibezAl-horizontal with text.svg", width=100)

# TODO(developer): Update and un-comment below lines
project_id = "lognos-agent"
location = "us-central1"
vertexai.init(project=project_id, location=location)

model = GenerativeModel("gemini-1.0-pro")
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat()

def get_chat_response(chat: ChatSession, prompt: str):
    response = chat.send_message(prompt)
    return response.text
st.markdown("##### CHAT HELPER")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
# Accept user input
if prompt := st.chat_input("write here"):
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        # st.write(prompt)
        # st.write(st.session_state.chat)
        response = get_chat_response(st.session_state.chat, prompt)
        st.markdown(response)
    # Add assistant message to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
    