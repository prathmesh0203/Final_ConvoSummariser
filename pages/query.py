import streamlit as st
import http.client
import json

# Function to interact with your data API
def talk_with_data(query, convo_list):
    conn = http.client.HTTPConnection("34.147.4.82")
    payload = json.dumps({
        "data": {
            "user_query": query,
            "conversation_list": convo_list
        }
    })
    headers = {
        'accept': 'application/json',
        'X-API-Key': st.secrets["talk_with_data_xapi_key"],
        'Content-Type': 'application/json'
    }
    conn.request("POST", "/conversation", payload, headers)
    res = conn.getresponse()
    data = res.read()
    output = json.loads(data.decode("utf-8"))["data"]["app_output"]
    return output

# Initialize Streamlit app
st.set_page_config(page_title="Ask Questions", page_icon="🔍", layout="wide", initial_sidebar_state="auto")

# Ensure that the conversation_dict is initialized in the session state
if 'conversation_dict' not in st.session_state:
    st.session_state['conversation_dict'] = {}

# User interface to ask a question
st.title("Ask Questions Based on Conversations")

# Check if there are conversations to ask questions from
if st.session_state['conversation_dict']:
    st.subheader("Ask a question based on the gathered conversations:")

    # Input for the user query
    user_query = st.text_input("Enter your question:")

    # Button to submit the question and get the response
    if st.button("Ask Question"):
        if user_query:
            # Combine all conversations into a single list
            all_conversations = [item for sublist in st.session_state['conversation_dict'].values() for item in sublist]
            # Call the function with the user query and the combined list of all conversations
            response = talk_with_data(user_query, all_conversations)
            st.write("Response:")
            st.write(response)  # Display the response
        else:
            st.error("Please enter a question to ask.")
else:
    st.write("No conversations available. Please generate conversations first on the conversation generator page.")
