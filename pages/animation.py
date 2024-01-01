import streamlit as st
import random

# Inject custom CSS for highlighting text
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
# Function to annotate text with citations based on the selected label
def annotate_text(text, annotations, selected_label):
    if selected_label in annotations:
        color = label_colors.get(selected_label, "grey")  # Color for the selected label
        for citation in annotations[selected_label].get("citation_for_" + selected_label.replace(" ", "_"), []):
            text = text.replace(citation, f"<span class='highlight-text' style='color: {color};'>{citation}</span>")
    return text

# Start of the Streamlit app
add_custom_css()  # Inject custom CSS

# 2. Retrieve and Prepare Data
if 'generated_citations' in st.session_state and 'conversation_dict' in st.session_state:
    all_conversations = st.session_state['conversation_dict']
    all_annotations = st.session_state['generated_citations']
    
    # Prepare labels and colors
    all_labels = set()
    for conv_annotations in all_annotations.values():
        all_labels.update(conv_annotations.keys())
    label_colors = {label: "#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for label in all_labels}
else:
    st.error("No data available. Please make sure conversations and annotations are loaded.")
    st.stop()

# 3. User Interaction
if all_labels:
    selected_label = st.selectbox('Select a label to highlight:', list(all_labels))
else:
    st.warning("No labels available to select.")
    st.stop()

# 4. Display Annotated Conversations
st.title("Annotated Conversations")

for convo_name, conversation in all_conversations.items():
    st.subheader(f"Annotated Conversation for {convo_name}")
    final_output = (all_annotations.get(convo_name, {}))
    
    # Display the conversation with annotations
    for exchange in conversation:
        user_text = exchange.get("user", "")
        bot_text = exchange.get("bot", "")
        
        annotated_user_text = annotate_text(user_text, final_output, selected_label)
        annotated_bot_text = annotate_text(bot_text, final_output, selected_label)
        
        if user_text:
            st.markdown(f"**User:** {annotated_user_text}", unsafe_allow_html=True)
        if bot_text:
            st.markdown(f"**Bot:** {annotated_bot_text}", unsafe_allow_html=True)