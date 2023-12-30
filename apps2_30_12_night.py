import streamlit as st
from Capp import request_automatic, manual_label_generator
from capp_new import manual_new, automatic_with_reasoning
import pandas as pd
import random
from sample_conversations import example_conversations

# Set Streamlit page configuration
st.set_page_config(page_title="ConversationSummarizer!", page_icon="🦙", layout="wide", initial_sidebar_state="auto")

# Initialize session state variables
def initialize_session_states():
    if 'user_input' not in st.session_state:
        st.session_state['user_input'] = None
    if 'labels' not in st.session_state:
        st.session_state['labels'] = []
    if 'unique_new_labels' not in st.session_state:
        st.session_state['unique_new_labels'] = []
    if 'final_labels' not in st.session_state:
        st.session_state['final_labels'] = []
    if 'output_auto_reasoning' not in st.session_state:
        st.session_state['output_auto_reasoning'] = None
    if 'selected_label' not in st.session_state:
        st.session_state['selected_label'] = None

initialize_session_states()

# Define all the functions here
def run_automatic_context(user_input):
    return request_automatic(user_input)

def run_manual_label_generator(user_input):
    return manual_label_generator(user_input)

def run_manual_new(selected_labels, user_input):
    return manual_new(selected_labels, user_input)

def run_automatic_with_reasoning(user_input):
    return automatic_with_reasoning(user_input)

def add_custom_css():
    custom_css = """
    <style>
        .hover-text:hover {
            transition: all 0.3s ease;
            font-size: 1.1em;
            font-weight: bold;
        }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)
def set_model_run_flag():
    st.session_state['model_run'] = True

def set_individual_run_flag(key):
    st.session_state['model_run'] = True
    st.session_state['run_key'] = key


def run_model():
    if app_choice == "Automatic Context":
        if 'conversation_dict' in st.session_state and st.session_state['conversation_dict']:
            # User selects how they want to process conversations
            process_option = st.radio("Choose how to run the model:",
                                    ('Run on Each Conversation Individually', 'Run on All Conversations Combined'),
                                    key='process_option')

            # Initialize a key in the session state to track if the model has been run
            if 'model_run' not in st.session_state:
                st.session_state['model_run'] = False

            if process_option == 'Run on All Conversations Combined':
                run_all = st.button("Run on All Conversations", on_click=set_model_run_flag)
                # if run_all:
                #     st.session_state['model_run'] = True  # Update the session state

            elif process_option == 'Run on Each Conversation Individually':
                for key in st.session_state['conversation_dict']:
                        st.button(f"Run on Conversation: {key}", key=key, on_click=set_individual_run_flag, args=(key,)) # Track which conversation is being processed

            # If the model_run flag is set, process the conversations accordingly
            if st.session_state['model_run']:
                if process_option == 'Run on All Conversations Combined':
                    combined_conversations = []
                    for conversation in st.session_state['conversation_dict'].values():
                        combined_conversations.extend(conversation)
                        combined_conversations.append("")

                    if combined_conversations:
                        st.subheader("Combined Conversations Results")
                        output = run_automatic_context(combined_conversations)
                        if output:
                            display_processed_conversation(output)
                            st.bar_chart(output)

                elif process_option == 'Run on Each Conversation Individually' and 'run_key' in st.session_state:
                    key = st.session_state['run_key']
                    conversation = st.session_state['conversation_dict'][key]
                    st.subheader(f"Results for conversation: {key}")
                    output = run_automatic_context(conversation)
                    if output:
                        display_processed_conversation(output)
                        st.bar_chart(output)

                st.session_state['model_run'] = False  # Reset the flag

        else:
            st.error("No conversations available to process. Please add conversations first.")




    elif app_choice == "Manually choose the labels":
        # Assuming you have a function to handle manual labeling
        handle_manual_labeling()

    elif app_choice == "Automatic Context With Reasoning":
        # Assuming you have a function to handle automatic context with reasoning
        handle_automatic_context_with_reasoning(user_input)

def annotate_text(text, annotations, label_colors, selected_label):
    annotated_text = text

    if selected_label in annotations:
        color = label_colors.get(selected_label, "grey")  # Default color if not found
        details = annotations[selected_label]

        for citation in details.get("citation_for_" + selected_label.replace(" ", "_"), []):
            annotated_text = annotated_text.replace(citation, f"<span style='color: {color};' title='{selected_label}'>{citation}</span>")

    return annotated_text

def show_annotations_if_selected(user_input, annotations, label_colors):
    selected_label = st.session_state.get('selected_label')

    # Check if user_input is a list of dictionaries
    if isinstance(user_input, list) and all(isinstance(exchange, dict) for exchange in user_input):
        for exchange in user_input:
            user_text = exchange.get("user", "")
            bot_text = exchange.get("bot", "")
            display_text = f"**User:** {user_text}" if user_text else f"**Bot:** {bot_text}"

            if not (user_text.strip() or bot_text.strip()):
                continue

            annotated_text = annotate_text(display_text, annotations, label_colors, selected_label)
            st.markdown(annotated_text, unsafe_allow_html=True)

    # Check if user_input is a string
    elif isinstance(user_input, str) and user_input.strip():
        annotated_text = annotate_text(user_input, annotations, label_colors, selected_label)
        st.markdown(f"**Conversation:** {annotated_text}", unsafe_allow_html=True)

    else:
        st.error("No valid conversation input found.")


def display_label_colors(label_colors):
    st.sidebar.title("Label Colors Reference")
    for label, color in label_colors.items():
        st.sidebar.markdown(f"<span style='color: {color};'>{label}</span>", unsafe_allow_html=True)

def display_processed_conversation(output):
    st.title("Processed Conversation")
    st.write(output)

def handle_automatic_context_with_reasoning(user_input):
    # Ensure output is only processed once or upon input change
    if 'output_auto_reasoning' not in st.session_state or user_input != st.session_state.get('last_processed_input'):
        st.session_state['output_auto_reasoning'] = run_automatic_with_reasoning(user_input)
        st.session_state['last_processed_input'] = user_input  # Track the last processed input
    
    st.title("Processed Conversation with Reasoning")
    if st.session_state['output_auto_reasoning']:
        st.write(st.session_state['output_auto_reasoning'])  # Display the output reasoning

        labels = list(st.session_state['output_auto_reasoning'].keys())
        colors = ["#" + ''.join(random.choices('0123456789ABCDEF', k=6)) for _ in labels]
        label_colors = dict(zip(labels, colors))

        display_label_colors(label_colors)  # Display label colors, if applicable

        # Update selected_label in the session state when a new label is selected
        def on_label_select():
            st.session_state['selected_label'] = st.session_state['label_selector']

        if 'label_selector' not in st.session_state:
            st.session_state['label_selector'] = labels[0]

        st.session_state['label_selector'] = st.selectbox('Select a label to highlight:', labels, index=labels.index(st.session_state['selected_label']) if st.session_state.get('selected_label') in labels else 0, on_change=on_label_select)

        show_annotations = st.checkbox('Show annotated conversation', value=True)

        if show_annotations and user_input:
            show_annotations_if_selected(user_input, st.session_state['output_auto_reasoning'], label_colors)


        # Display bar chart if selected
        show_bar_chart = st.checkbox('Show Bar Chart', value=True)
        if show_bar_chart and labels:
            label_dict = {}
            for label in labels:
                if label != "IIT Madras":  # Exclude "IIT Madras" label
                    label_entries = st.session_state['output_auto_reasoning'].get(label, {})
                    citations = label_entries.get(f'citation_for_{label.replace(" ", "_")}', [])
                    label_dict[label] = len(citations)
            st.bar_chart(label_dict)


def handle_manual_labeling():
    st.title("Choose the labels")
    selected_labels = st.multiselect("Choose labels:", options=st.session_state['labels'], default=[])

    new_labels = st.text_input("Add new labels (comma-separated):").strip()
    if new_labels and st.button("Add Labels"):
        additional_labels = [label.strip() for label in new_labels.split(',') if label.strip()]
        st.session_state['unique_new_labels'] = [label for label in additional_labels if label not in st.session_state['labels']]
        st.session_state['labels'].extend(st.session_state['unique_new_labels'])
        st.success(f"Added {len(st.session_state['unique_new_labels'])} new labels.")

    st.session_state['final_labels'] = list(set(selected_labels + st.session_state['unique_new_labels']))

    st.write("Currently selected and added labels:")
    for label in st.session_state['final_labels']:
        st.write(f"- {label}")

    if st.button("Submit and Process"):
        final_output = run_manual_new(st.session_state['final_labels'], user_input)
        st.write("Final Processed Output:")
        st.write(final_output)
        if isinstance(final_output, (dict, pd.DataFrame)):
            st.bar_chart(final_output)

# Streamlit app interface
st.sidebar.title("Choose your Mode")
app_choice = st.sidebar.selectbox("Choose your mode", ("Automatic Context", "Manually choose the labels", "Automatic Context With Reasoning"))
st.sidebar.write("Running", app_choice)

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

# st.title("Enter Conversation")
# use_predefined = st.checkbox("Try Default Conversation?")
# user_input = get_user_input(use_predefined) 
def get_or_use_saved_conversation(use_predefined, saved_conversation):
    if use_predefined:
        selected_example = st.selectbox("Choose a sample conversation", list(example_conversations.keys()))
        show_conversation = st.checkbox("Show selected conversation?")
        if show_conversation:
            st.text("Selected Conversation:")
            st.write(example_conversations[selected_example])
        return example_conversations[selected_example]
    elif saved_conversation:
        st.write("Using the saved conversation:")
        st.write(saved_conversation)
        return saved_conversation
    else:
        return st.text_area("Enter Here")
    
if 'final_list' not in st.session_state:
    st.session_state['final_list'] = []

# Display the title
st.title("View Stored Conversations")

# Check if there are conversations to display
if 'conversation_dict' in st.session_state and st.session_state['conversation_dict']:
    # Display the conversations
    for key, conversation in st.session_state['conversation_dict'].items():
        st.subheader(f"Conversation: {key}")
        st.write(conversation)
        st.markdown("---")  # Add a separator between conversations



if st.button("Run model"):
    run_model()

if app_choice == "Manually choose the labels":
    handle_manual_labeling()
