import streamlit as st

def display_app_info():
    st.title("Welcome to the Conversation Analysis Platform")

    # Use markdown to add style to the text
    st.markdown("""
    ### About This App:
    Welcome to our **advanced Conversation Analysis Platform**, where meaningful insights are derived from dialogues between users and service bots. This sophisticated tool is designed to **streamline the analysis of conversations**, providing valuable labels and facilitating a deeper understanding of the discussed content.
    """, unsafe_allow_html=True)

    # Using columns to create a more structured layout
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        ### Page 1: Generate Conversation
        Effortlessly craft conversations by:
        - **Manually entering discussions**: Directly input your conversations into the system.
        - **Choosing from a curated selection of predefined dialogue scenarios**: Select from a variety of preset dialogues that best fit your analysis needs.
        - **Creating discussions based on specific situations tailored to your needs**: Generate conversations dynamically based on the situations you describe.
        """)
        st.info("🔥 Save your conversations for future reference, allowing you to accumulate and revisit a wealth of valuable interaction data.")

    with col2:
        st.markdown("""
        ### Page 2: Generate Results
        Utilize saved conversations to:
        - **Run our cutting-edge model** on the selected dialogue.
        - **Obtain comprehensive results**, revealing insightful labels discussed during the conversation.
        """)
        st.info("📊 Delve deep into the dialogue dynamics and understand the nuances of the conversation.")

    with col3:
        st.markdown("""
        ### Page 3: Explore Results
        Delve into the obtained results, gaining access to:
        - **A detailed breakdown of labels**: See which labels are most prominent and how they relate to your conversation.
        - **Citations for each selected label**: Providing context and background information to understand the relevance of each label.
        """)
    
    with col4:
        st.markdown("""
        ### Page 4: Query Insights
        Empower your exploration by:
        - **Asking queries based on the selected saved conversations**: Dive deeper into specific aspects of the conversation.
        - **Inputting entire conversations for a more comprehensive and nuanced understanding**: Get a holistic view of the conversation's dynamics.
        """)
        st.info("💡 Use these insights to refine your approach, understand key themes, and drive informed decisions.")

# Run the function to display the app info
display_app_info()
