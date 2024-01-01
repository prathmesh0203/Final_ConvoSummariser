import streamlit as st
from Capp import request_automatic, manual_label_generator
from capp_new import manual_new, automatic_with_reasoning, manual_label_citation, create_top_labels
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

    # Initialize a common list to store all generated labels
    if 'final_label_list' not in st.session_state:
        st.session_state['final_label_list'] = set()

    if 'labels_generated' not in st.session_state:
        st.session_state['labels_generated'] = False

    if 'conversation_dict' not in st.session_state or not st.session_state['conversation_dict']:
        st.error("No conversations available. Please generate conversations first on the conversation generator page.")
        return

    # Generate labels for all conversations and store them in final_label_list
    if not st.session_state['labels_generated']:
        for convo_key, user_input in st.session_state['conversation_dict'].items():
            with st.spinner(f"Generating labels for {convo_key}..."):
                labels = manual_label_generator(user_input)
            st.session_state['final_label_list'].update(labels)
        st.session_state['labels_generated'] = True

    st.sidebar.header("All Generated Labels")
    if st.session_state['final_label_list']:
        for label in st.session_state['final_label_list']:
            st.sidebar.info(label)
    else:
        st.sidebar.write("No labels generated yet.")

    conversation_names = list(st.session_state['conversation_dict'].keys())
    selected_conversation_name = st.selectbox("Choose a conversation to label:", conversation_names)

    unique_key = f"conversation_{selected_conversation_name}"

    # Initialize conversation-specific session state
    if unique_key not in st.session_state:
        st.session_state[unique_key] = {'additional_labels': [], 'generated_labels': [], 'user_input': None, 'top_labels': None}

    if selected_conversation_name:
        st.subheader(f"Selected Conversation: {selected_conversation_name}")
        user_input = st.session_state['conversation_dict'][selected_conversation_name]
        st.session_state[unique_key]['user_input'] = user_input
        st.write(user_input)

        # Generate top labels only if they haven't been generated for this conversation
        if st.session_state[unique_key]['top_labels'] is None:
            with st.spinner("Generating top labels..."):
                st.session_state[unique_key]['top_labels'] = create_top_labels(list(st.session_state['final_label_list']), user_input)

        # Allow users to select labels from the top labels
        st.subheader("Select Labels:")
        selected_labels = st.multiselect("Choose labels:", options=st.session_state[unique_key]['top_labels'], key='selected_labels_key')
        
        new_labels = st.text_input("Add new labels (comma-separated):", key='new_labels_key')
        if st.button("Add Labels", key='add_labels_button'):
            if new_labels:
                additional_labels = [label.strip() for label in new_labels.split(',') if label.strip()]
                st.session_state[unique_key]['additional_labels'].extend(additional_labels)
                st.session_state['final_label_list'].update(additional_labels)  # Update final_label_list with additional labels

        # Combine selected and additional labels for the final list
        st.subheader("Final Labels for the Conversation:")
        final_labels = list(set(selected_labels + st.session_state[unique_key]['additional_labels']))
        for label in final_labels:
            st.write(label)

        if st.button("Submit and Process"):
            if final_labels:
                with st.spinner("Processing..."):
                    final_output = manual_label_citation(user_input, final_labels)
                st.write("Final Processed Output:")

                # Storing this conversation in the session state to be used in the animation page
                st.session_state[unique_key].update({'final_output': final_output, 'user_input': user_input})

                st.write(final_output)

                label_citation_counts = {label: len(details.get(f'citation_for_{label.replace(" ", "_")}', [])) for label, details in final_output.items()}
                
                sorted_labels = sorted(label_citation_counts.items(), key=lambda x: x[1], reverse=True)

                labels, citation_counts = zip(*sorted_labels)

                st.bar_chart(data=dict(zip(labels, citation_counts)))

if __name__ == '__main__':
    label_conversation_page()





