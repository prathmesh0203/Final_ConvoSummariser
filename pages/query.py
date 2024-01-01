import streamlit as st
import http.client
import json
from capp_new import query_new_for_each_conversation, talk_with_data, query_answer_summarizer

def transform_conversations(data):
    transformed_data = []
    for conversation_name, exchanges in data.items():
        # Create a new dictionary with the conversation name as the key and the exchanges as the value
        conversation_dict = {conversation_name: exchanges}
        # Append this dictionary to the list
        transformed_data.append(conversation_dict)
    return transformed_data

def display_as_markdown(data, level=0):
    if isinstance(data, dict):
        for key, value in data.items():
            st.markdown(f"{'    ' * level}- **{key}**: ")
            display_as_markdown(value, level + 1)
    else:
        st.markdown(f"{'    ' * level}- {data}")

def display_hierarchy(data, level=0):
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, dict):  # If the value is a dictionary, create an expander
                with st.expander(f"{key}"):
                    display_hierarchy(value, level + 1)
            else:  # If the value is not a dictionary, display it directly
                st.markdown(f"* **{key}**: {value}")
    else:  # If the data is not a dictionary, display it directly
        st.write(data)
# Initialize Streamlit app
st.set_page_config(page_title="Ask Questions", page_icon="🔍", layout="wide", initial_sidebar_state="auto")

# Ensure that the conversation_dict is initialized in the session state
if 'conversation_dict' not in st.session_state:
    st.session_state['conversation_dict'] = {}

#print the whole dictioanry of saved conversations
# print(st.session_state['conversation_dict'])
new_data = transform_conversations(st.session_state['conversation_dict'])

# print("new data")
# print(new_data)


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
            response = query_new_for_each_conversation(user_query, new_data)
            final_string = query_answer_summarizer(response)
            st.write("Summarised Responces: ")
            st.write(final_string)
            print("                         ")
            print(final_string)
            # print(response)
            response = display_hierarchy(response) 
            st.write(response)
        else:
            st.error("Please enter a question to ask.")
else:
    st.write("No conversations available. Please generate conversations first on the conversation generator page.")
