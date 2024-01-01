import streamlit as st
from Capp import request_automatic, manual_label_generator
from capp_new import manual_new, automatic_with_reasoning, create_top_ten_labels
import pandas as pd
import random
import json
from sample_conversations import example_conversations



def label_conversation_page():
    st.title("Label Generation for Conversations")

    # 0. Check if there are conversations to label
    if not st.session_state['conversation_dict']:
        st.warning("No conversations available to label.")
        st.stop()


    # 1. Generate labels for all the conversations (only once)
    if 'all_labels' not in st.session_state:
        all_labels = set()
        for convo_key, user_input in st.session_state['conversation_dict'].items():
            with st.spinner(f"Generating labels for {convo_key}..."):
                labels = manual_label_generator(user_input)
            all_labels.update(labels)
        st.session_state['all_labels'] = all_labels

    print("printing all labels")
    print(st.session_state['all_labels'])
    
    
    if 'top_labels' not in st.session_state:
        with st.spinner("Generating top labels..."):
            st.session_state['top_labels'] = create_top_ten_labels(list(st.session_state['all_labels']))

    
    if 'selected_labels' not in st.session_state:
        st.session_state['selected_labels'] = []

    if 'manual_labels' not in st.session_state:
        st.session_state['manual_labels'] = []

    if "top_labels" not in st.session_state:
        st.session_state['top_labels'] = []

    # 4. User selects labels from this dropdown
    print("printing top labels")
    print(st.session_state['top_labels'])
    selected_labels = st.multiselect(
        "Select labels:",
        options=st.session_state['top_labels']
    )
    print("printing selected labels")
    print(selected_labels)
    # selected_labels = ["Greeting", "Complaint", "Request", "Feedback"]
    st.session_state['selected_labels'] = selected_labels

    # 5. User adds some labels manually
    new_labels = st.text_input("Add new labels (comma-separated):")
    if st.button("Add Labels"):
        additional_labels = [label.strip() for label in new_labels.split(',') if label.strip()]
        st.session_state['manual_labels'].extend(additional_labels)  # Add new labels to manual_labels

    # 6. Show the final labels
    st.subheader("Final Labels for the Conversations:")
    final_labels = set(st.session_state['selected_labels'] + st.session_state['manual_labels'])
    st.session_state['final_labels'] = final_labels
    print(list(st.session_state['final_labels']))
    for label in final_labels:
        st.info(label)

    if st.button('Clear Final Labels'):
        st.session_state['final_labels'] = []
        st.session_state['selected_labels'] = []
        st.session_state['manual_labels'] = []
        st.experimental_rerun()

if __name__ == '__main__':
    label_conversation_page()