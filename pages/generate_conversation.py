import streamlit as st
import http.client
import json
from sample_conversations import example_conversations

st.set_page_config(page_title="Generate Conversation", page_icon="🌄", layout="wide", initial_sidebar_state="auto")

# Initialize session state variables
if 'conversation_list' not in st.session_state:
    st.session_state['conversation_list'] = []
if 'conversation_count' not in st.session_state:
    st.session_state['conversation_count'] = 1
if 'final_list' not in st.session_state:
    st.session_state['final_list'] = []



def generate_convo(conversation):
    conn = http.client.HTTPConnection("34.147.4.82")
    payload = json.dumps({
        "data": {
            "text": f"{conversation}"
        }
    })
    headers = {
        'accept': 'application/json',
        'X-API-Key': st.secrets["conversation_generation_xapi_key"],
        'Content-Type': 'application/json'
    }
    conn.request("POST", "/conversation", payload, headers)

    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")

def get_user_input(use_predefined):
    if use_predefined:
        selected_example = st.selectbox("Choose a sample conversation", list(example_conversations.keys()))
        show_conversation = st.checkbox("Show selected conversation?")
        if show_conversation:
            st.text("Selected Conversation:")
            st.write(example_conversations[selected_example])
        return example_conversations[selected_example]
    else:
        return st.text_area("Enter Here")

if 'conversation_dict' not in st.session_state:
    st.session_state['conversation_dict'] = {}
if 'manual_count' not in st.session_state:
    st.session_state['manual_count'] = 1

def display_conversation_generator():
    st.title("Generate Conversation")

    # Initialize or retrieve the current conversation and its key
    if 'current_conversation' not in st.session_state:
        st.session_state['current_conversation'] = ""
        st.session_state['conversation_key'] = ""

    conversation_source = st.radio("Choose the conversation source:",
                                  ('Use predefined conversation','Generate based on situation','Enter conversation manually'))

    if conversation_source == 'Use predefined conversation':
        selected_example = st.selectbox("Choose a sample conversation", list(example_conversations.keys()))
        st.session_state['current_conversation'] = example_conversations[selected_example]
        st.session_state['conversation_key'] = selected_example

    elif conversation_source == 'Enter conversation manually':
        st.session_state['current_conversation'] = st.text_area("Enter conversation manually:", key='manual_input')

    elif conversation_source == 'Generate based on situation':
        situation = st.text_area("Describe the situation for the conversation:", key='situation_input')
        if st.button("Generate Conversation"):
            generated_conversation = generate_convo(situation)
            generated_conversation = json.loads(generated_conversation)["data"]["app_output"]["conversation"]
            st.write("Generated Conversation:")
            st.write(generated_conversation)
            st.session_state['current_conversation'] = generated_conversation
            st.session_state['conversation_key'] = situation

    # Allow the user to provide a unique name for the conversation
    if st.session_state['current_conversation']:
        conversation_name = st.text_input("Enter a unique name for this conversation (will be used as the key):", key='conversation_name')

        if st.button("Add Conversation to Dictionary", key='add_button'):
            if conversation_name and st.session_state['current_conversation']:
                if conversation_name not in st.session_state.get('conversation_dict', {}):
                    st.session_state.setdefault('conversation_dict', {})[conversation_name] = st.session_state['current_conversation']
                    st.success(f"Conversation '{conversation_name}' added. Total conversations stored: {len(st.session_state['conversation_dict'])}")
                    st.session_state['current_conversation'] = ""  # Clear the current conversation
                    st.session_state['conversation_key'] = ""  # Clear the conversation key
                else:
                    st.error(f"A conversation with the name '{conversation_name}' already exists.")
            else:
                st.error("Please provide a unique name and ensure a conversation is selected or generated.")

    # Display the final dictionary of conversations
    if st.session_state.get('conversation_dict'):
        st.subheader("Saved Conversations:")
        for key, convo in st.session_state['conversation_dict'].items():
            st.text(f"Name: {key}")
            st.write(convo)

if __name__ == "__main__":
    display_conversation_generator()
