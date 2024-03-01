import streamlit as st

import google.generativeai as genai

from pypdf import PdfReader


genai.configure(api_key = "AAIzaSyBSul-Xy19E6MpXxa06ZdKQeJ9JgZ64Gl8")

chat_model = genai.GenerativeModel('gemini-pro')

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role":"assistant",
            "content":"Ask me Anything"
        }
    ]

container = st.container(height=600)
# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with container.chat_message(message["role"]):
        st.markdown(message["content"])

# Process and store Query and Response
def llm_function(query, uploaded_file=None):
    text = ""
    if uploaded_file:
        reader = PdfReader(uploaded_file)
        text = "\n\n".join([page.extract_text() for page in reader.pages])
    response = chat.send_message(query+"\n\n"+text)
    # response = model.generate_content(query)

    # Displaying the Assistant Message
    with container.chat_message("assistant"):
        st.markdown(response.text)

    # Storing the User Message
    st.session_state.messages.append(
        {
            "role":"user",
            "content": query
        }
    )

    # Storing the User Message
    st.session_state.messages.append(
        {
            "role":"assistant",
            "content": response.text
        }
    )

chat = chat_model.start_chat(history=[])

col1, col2 = st.columns((1, 4))

with col2:
# Accept user input
    query = st.chat_input("What's up? nigga")
    
if 'clicked' not in st.session_state:
    st.session_state.clicked = False
if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None
with col1:
# Create a button for file upload
    st.button('upload file', on_click=lambda: st.session_state.update(clicked=not(st.session_state.clicked)))
if st.session_state.clicked:
    uploaded_file = st.file_uploader("Choose a file")
    st.session_state.uploaded_file = uploaded_file
    if uploaded_file:
        st.write("Uploaded file")
        st.session_state.clicked = False

if query:
    # Displaying the User Message
    with container.chat_message("user"):
        st.markdown(query)

    llm_function(query, st.session_state.get('uploaded_file', None))
