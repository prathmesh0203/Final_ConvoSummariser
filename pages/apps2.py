import streamlit as st
from Capp import request_automatic, manual_label_generator
from capp_new import manual_new, automatic_with_reasoning, manual_label_citation
import pandas as pd
import random
import json
from sample_conversations import example_conversations

# Set Streamlit page configuration
st.set_page_config(page_title="ConversationSummarizer!", page_icon="🦙", layout="wide", initial_sidebar_state="auto")

# def run_manual_label_generator(user_input):
#     return manual_label_generator(user_input)



def label_conversation_page():
    st.title("Label Conversation")

    if 'conversation_dict' not in st.session_state or not st.session_state['conversation_dict']:
        st.error("No conversations available. Please generate conversations first on the conversation generator page.")
        return

    conversation_names = list(st.session_state['conversation_dict'].keys())
    selected_conversation_name = st.selectbox("Choose a conversation to label:", conversation_names)

    unique_key = f"conversation_{selected_conversation_name}"

    # Initialize conversation-specific session state
    if unique_key not in st.session_state:
        st.session_state[unique_key] = {'additional_labels': [], 'generated_labels': [], 'user_input': None}

    if selected_conversation_name:
        st.subheader(f"Selected Conversation: {selected_conversation_name}")
        user_input = st.session_state['conversation_dict'][selected_conversation_name]
        st.session_state[unique_key]['user_input'] = user_input  # Store user input in the conversation-specific state
        st.write(user_input)

        # Button to generate labels for the selected conversation
        if st.button("Generate Labels for Selected Conversation"):
            generated_labels = manual_label_generator(user_input)
            st.session_state[unique_key]['generated_labels'] = generated_labels  # Store generated labels in the conversation-specific state

        # Allow users to select labels from the generated ones
        if 'generated_labels' in st.session_state[unique_key] and st.session_state[unique_key]['generated_labels']:
            st.subheader("Select Labels:")
            selected_labels = st.multiselect("Choose labels:", options=st.session_state[unique_key]['generated_labels'], key='selected_labels_key')

            new_labels = st.text_input("Add new labels (comma-separated):", key='new_labels_key')
            if st.button("Add Labels", key='add_labels_button'):
                if new_labels:
                    additional_labels = [label.strip() for label in new_labels.split(',') if label.strip()]
                    st.session_state[unique_key]['additional_labels'].extend(additional_labels)  # Update additional labels list in the conversation-specific state

            # Combine selected and additional labels for the final list
            st.subheader("Final Labels for the Conversation:")
            final_labels = list(set(selected_labels + st.session_state[unique_key]['additional_labels']))
            for label in final_labels:
                st.write(label)

            if st.button("Submit and Process"):
                if final_labels:
                    final_output = manual_label_citation(user_input, final_labels)
                    st.write("Final Processed Output:")

                    # Storing this conversation in the session state to be used in the animation page
                    st.session_state[unique_key].update({'final_output': final_output, 'user_input': user_input})

                    st.write(final_output)

                    label_citation_counts = {label: len(details.get(f'citation_for_{label.replace(" ", "_")}', [])) for label, details in final_output.items()}
                    
                    sorted_labels = sorted(label_citation_counts.items(), key=lambda x: x[1], reverse=True)

                    labels, citation_counts = zip(*sorted_labels)

                    st.bar_chart(data=dict(zip(labels, citation_counts)))

if __name__ == "__main__":
    label_conversation_page()





