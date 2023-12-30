import streamlit as st
import json
import random

# Function to inject custom CSS for highlighting text
def add_custom_css():
    custom_css = """
    <style>
        .highlight-text {
            transition: all 0.3s ease;
            font-weight: bold;
            background-color: yellow;
        }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

# Function to annotate text with citations based on the selected label
def annotate_text(text, annotations, selected_label):
    if selected_label in annotations:
        color = label_colors.get(selected_label, "grey")  # Color for the selected label
        for citation in annotations[selected_label].get("citation_for_" + selected_label.replace(" ", "_"), []):
            text = text.replace(citation, f"<span class='highlight-text' style='color: {color};'>{citation}</span>")
    return text

add_custom_css()  # Inject custom CSS

# Attempt to retrieve final_output and user_input for the current conversation
selected_conversation_name = st.selectbox("Choose a conversation to view:", list(st.session_state.get('conversation_dict', {}).keys()))
unique_key = f"conversation_{selected_conversation_name}"

if unique_key in st.session_state:
    final_output = st.session_state[unique_key].get('final_output', {})
    conversation = st.session_state[unique_key].get('user_input', [])
else:
    st.error("No data available for this conversation. Please go back and submit a conversation first.")
    st.stop()

# Generate colors for labels and create a dropdown for selecting labels
labels = final_output.keys()
colors = ["#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for i in labels]
label_colors = dict(zip(labels, colors))

if labels:
    selected_label = st.selectbox('Select a label to highlight:', labels)
else:
    st.warning("No labels available to select.")
    st.stop()



st.title("Annotated Conversation")

# Display the conversation with annotations
for i, exchange in enumerate(conversation):
    user_text = exchange.get("user", "")
    bot_text = exchange.get("bot", "")
    
    annotated_user_text = annotate_text(user_text, final_output, selected_label)
    annotated_bot_text = annotate_text(bot_text, final_output, selected_label)
    
    if user_text:
        st.markdown(f"**User:** {annotated_user_text}", unsafe_allow_html=True)
    if bot_text:
        st.markdown(f"**Bot:** {annotated_bot_text}", unsafe_allow_html=True)

# Update label_dict creation to be more robust
label_dict = {}
if final_output:
    for label, details in final_output.items():
        if "citation_for_" + label.replace(" ", "_") in details:
            label_dict[label] = len(details["citation_for_" + label.replace(" ", "_")])

# Display a bar chart with citation counts
if label_dict:
    st.bar_chart(label_dict)
else:
    st.write("No citation data available to display.")
