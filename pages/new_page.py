import streamlit as st
from Capp import request_automatic, manual_label_generator
from capp_new import manual_new, automatic_with_reasoning
import pandas as pd
import random
from sample_conversations import example_conversations

# Set Streamlit page configuration
st.set_page_config(page_title="ConversationSummarizer!", page_icon="🦙", layout="wide", initial_sidebar_state="auto")


#show the stored conversations from the generate_conversation page

def run_automatic_context(user_input):
    return request_automatic(user_input)

def run_manual_label_generator(user_input):
    return manual_label_generator(user_input)

def run_manual_new(selected_labels, user_input):
    return manual_new(selected_labels, user_input)

def run_automatic_with_reasoning(user_input):
    return automatic_with_reasoning(user_input)

def display_processed_conversation(output):
    st.title("Processed Conversation")
    st.write(output)

st.sidebar.title("Choose your Mode")
app_choice = st.sidebar.selectbox("Choose your mode", ("Automatic Context", "Manually choose the labels", "Automatic Context With Reasoning"))
st.sidebar.write("Running", app_choice)


if 'conversation_dict' in st.session_state and st.session_state['conversation_dict']:
    # Display the individual conversations
    for key, conversation in st.session_state['conversation_dict'].items():
        st.subheader(f"Conversation: {key}")
        st.write(conversation)
        st.markdown("---")  # Add a separator between conversations
    
    # Option to run the model on all conversations combined
    if st.button("Run on All Conversations Combined"):
        combined_conversations = []
        for conversation in st.session_state['conversation_dict'].values():
            # Assuming each conversation is a list of strings
            combined_conversations.extend(conversation)
            combined_conversations.append("")  # Add an empty string as a separator between conversations

        if combined_conversations:
            # Call your model function with the combined list of all conversations
            output = run_automatic_context(combined_conversations)
            if output:  # Check if the output is not empty
                st.subheader("Combined Conversations Results")
                display_processed_conversation(output)
                st.bar_chart(output)
        else:
            st.error("No conversations are available to process.")


