import streamlit as st

output = 0
conversation = 0



#showing output in json format
import json
import streamlit as st
import random
# print(json.dumps(output, indent=4))
label_dict = {}

all_labels = output.keys()
all_labels_without_madras = [label for label in all_labels if label != "IIT Madras"]
for label in all_labels_without_madras:
    label_dict[label] = len(output[label]['citation_for_'+label.replace(" ", "_")])
    
labels = output.keys()
   

colors = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
                for i in range(len(labels))]

label_colors = dict(zip(labels, colors))

def add_custom_css():
    custom_css = """
    <style>
        .highlight-text {
            transition: all 0.3s ease;
            font-weight: bold;
        }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

def annotate_text(text, annotations, selected_label):
    for label, details in annotations.items():
        if label == selected_label:
            color = label_colors.get(label, "grey")  # Color for the selected label
            for citation in details.get("citation_for_" + label.replace(" ", "_"), []):
                # Add a span with custom class and style for the selected label
                text = text.replace(citation, f"<span class='highlight-text' style='color: {color};'>{citation}</span>")
    return text

add_custom_css()  # Inject custom CSS
selected_label = st.selectbox('Select a label to highlight:', list(label_colors.keys()))

# def display_label_colors():
#     st.sidebar.title("Label Colors Reference")
#     for label, color in label_colors.items():
#         st.sidebar.markdown(f"<span style='color: {color};'>{label}</span>", unsafe_allow_html=True)

# display_label_colors()

st.title("Annotated Conversation")

for i, exchange in enumerate(conversation):
    user_text = exchange.get("user", "")
    bot_text = exchange.get("bot", "")
    
    # Annotate text based on the selected label
    annotated_user_text = annotate_text(user_text, output, selected_label)
    annotated_bot_text = annotate_text(bot_text, output, selected_label)
    
    # Display annotated text
    if user_text:
        st.markdown(f"**User:** {annotated_user_text}", unsafe_allow_html=True)
    if bot_text:
        st.markdown(f"**Bot:** {annotated_bot_text}", unsafe_allow_html=True)


label_dict = {}
all_labels = output.keys()
all_labels_without_madras = [label for label in all_labels if label is not "IIT Madras"]
for label in all_labels_without_madras:
    label_dict[label] = len(output[label]['citation_for_'+label.replace(" ", "_")])
print(label_dict)
st.bar_chart(label_dict)