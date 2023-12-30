import streamlit as st
from pathlib import Path
import json
from streamlit_extras.switch_page_button import switch_page
from streamlit.source_util import _on_pages_changed, get_pages

FOURTH_PAGE_NAME = "query"
THIRD_PAGE_NAME = "apps2"
SECOND_PAGE_NAME = "generate_conversation"
DEFAULT_PAGE = "login.py"


# all pages request
def get_all_pages():
    default_pages = get_pages(DEFAULT_PAGE)

    pages_path = Path("pages.json")

    if pages_path.exists():
        saved_default_pages = json.loads(pages_path.read_text())
    else:
        saved_default_pages = default_pages.copy()
        pages_path.write_text(json.dumps(default_pages, indent=4))

    return saved_default_pages


# clear all page but not login page
def clear_all_but_first_page():
    current_pages = get_pages(DEFAULT_PAGE)

    if len(current_pages.keys()) == 1:
        return

    get_all_pages()

    # Remove all but the first page
    key, val = list(current_pages.items())[0]
    current_pages.clear()
    current_pages[key] = val

    _on_pages_changed.send()


# show all pages
def show_all_pages():
    current_pages = get_pages(DEFAULT_PAGE)

    saved_pages = get_all_pages()

    # Replace all the missing pages
    for key in saved_pages:
        if key not in current_pages:
            current_pages[key] = saved_pages[key]

    _on_pages_changed.send()


# Hide default page
def hide_page(name: str):
    current_pages = get_pages(DEFAULT_PAGE)

    for key, val in current_pages.items():
        if val["page_name"] == name:
            del current_pages[key]
            _on_pages_changed.send()
            break


# calling only default(login) page  
clear_all_but_first_page()

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)

def sidebar_style():
    st.markdown("""
    <style>
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        font-family: 'Arial', sans-serif; /* Change the font family */
        font-size: 16px;  /* Change the font size */
        line-height: 1.5; /* Change the line height */
        color: #000;  /* Change to black color */
    }
    </style>
    """, unsafe_allow_html=True)

# Apply the sidebar style
sidebar_style()

# local_css("style.css")

# Rest of your Streamlit code...
st.sidebar.info("""
    **About This App:**

    Welcome to our advanced Conversation Analysis Platform, where meaningful insights are derived from dialogues between users and service bots. This sophisticated tool is designed to streamline the analysis of conversations, providing valuable labels and facilitating a deeper understanding of the discussed content.

    **Page 1: Generate Conversation**
    Effortlessly craft conversations by:
    - Manually entering discussions.
    - Choosing from a curated selection of predefined dialogue scenarios.
    - Creating discussions based on specific situations tailored to your needs.
    Save your conversations for future reference, allowing you to accumulate and revisit a wealth of valuable interaction data.

    **Page 2: Generate Results**
    Utilize saved conversations to:
    - Run our cutting-edge model on the selected dialogue.
    - Obtain comprehensive results, revealing insightful labels discussed during the conversation.

    **Page 3: Explore Results**
    Delve into the obtained results, gaining access to:
    - A detailed breakdown of labels.
    - Citations for each selected label, providing context and background information.

    **Page 4: Query Insights**
    Empower your exploration by:
    - Asking queries based on the selected saved conversations.
    - Inputting entire conversations for a more comprehensive and nuanced understanding.
""")

st.title("Conversation Analyzer App")
st.title("Welcome!")


# Login form
def login():
    st.header("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        # Check if both username and password match
        if username == st.secrets["USERNAME"] and password == st.secrets["ACCESS_CODE"]:
            st.success(f"Logged In Successfully as {username}!")
            # Redirect to the desired page
            show_all_pages()  # Call all pages
            switch_page(SECOND_PAGE_NAME)  # Switch to the second page
        else:
            st.error("Invalid username or password")
            clear_all_but_first_page() 


# Run the Streamlit app
if __name__ == '__main__':
    login()
    