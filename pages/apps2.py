import aiohttp
import streamlit as st
from Capp import request_automatic, manual_label_generator
from capp_new import manual_new, automatic_with_reasoning, create_top_labels
import pandas as pd
import random
import json
from sample_conversations import example_conversations
from concurrent.futures import ThreadPoolExecutor
import asyncio
import http.client
import matplotlib.pyplot as plt

# Set Streamlit page configuration
st.set_page_config(page_title="ConversationSummarizer!", page_icon="🦙", layout="wide", initial_sidebar_state="auto")
def display_hierarchy(data, level=0):
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, dict):  # If the value is a dictionary, create an expander
                with st.expander(f"{key}"):
                    display_hierarchy(value, level + 1)
            else:  
                st.markdown(f"* **{key}**: {value}")
    else:  
        st.write(data)
def calculate_label_frequency(citation_dict):
    label_frequency = {}

    # Iterate through each conversation and its labels
    for conversation, labels in citation_dict.items():
        for label, details in labels.items():
            # Construct the key name for checking label availability
            label = label.replace(" ", "_")
            availability_key = f"is_{label}_available"
            # Check if the label is present in the conversation
            if details.get(availability_key, 0) == 1:
                label_frequency[label] = label_frequency.get(label, 0) + 1

    return label_frequency


def display_label_frequency_bar_chart(label_frequency):
    # Create a bar chart with the frequency of labels
    labels = list(label_frequency.keys())
    counts = list(label_frequency.values())
    st.bar_chart(pd.DataFrame({'labels': labels, 'counts': counts}).set_index('labels'))


async def manual_label_citation(session, conversation, labels_list):
    labels_list = list(labels_list)  # Convert the set to a list for JSON serialization
    url = "http://34.147.4.82/conversation"
    payload = json.dumps({
        "data": {
            "convo": conversation,
            "labels": labels_list
        }
    })
    headers = {
        'accept': 'application/json',
        'X-API-Key': st.secrets["manual_label_citation"],
        'Content-Type': 'application/json'
    }

    async with session.post(url, data=payload, headers=headers) as response:
        data = await response.text()
        output = json.loads(data)
        return output.get("data", {}).get("app_output", "")

async def generate_all_citations(conversations, final_labels):
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(manual_label_citation(session, conv, final_labels)) for conv in conversations.values()]
        results = await asyncio.gather(*tasks)
        return dict(zip(conversations.keys(), results))

def label_conversation_page():
    st.title("Generate Citations")
    if 'conversation_dict' not in st.session_state or not st.session_state['conversation_dict']:
        st.error("No conversations available.")
        return

    if 'final_labels' not in st.session_state:
        st.error("No final labels available. Please generate labels first.")
        return

    if st.button("Generate Citations"):
        final_labels = st.session_state['final_labels']
        conversations = st.session_state['conversation_dict']

        with st.spinner("Generating citations..."):
            citation_dict = asyncio.run(generate_all_citations(conversations, final_labels))

        print(citation_dict)

        st.session_state['generated_citations'] = citation_dict
        
        for convo_name, citation in citation_dict.items():
            st.subheader(f"Citations for {convo_name}:")
            citation = display_hierarchy(citation)
            # st.write(citation)
        st.title("Label Frequency Across Conversations")

        label_frequency = calculate_label_frequency(citation_dict)

        # Display the bar chart
        display_label_frequency_bar_chart(label_frequency)
if __name__ == '__main__':
    label_conversation_page()