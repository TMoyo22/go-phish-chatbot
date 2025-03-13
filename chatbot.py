import streamlit as st
import google.generativeai as genai

# Get API key from secrets
try:
    API_KEY = st.secrets["GEMINI"]["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception as e:
    st.error(
        "Error accessing API key from secrets. Please set up your .streamlit/secrets.toml file."
    )
    st.stop()

st.set_page_config(page_title="GoPhish Chatbot", page_icon="🤖")

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown(
    """
     <h1>🤖<span style="color:turquoise;">Go</span>Phish! ChatBot</h1>
     """,
    unsafe_allow_html=True,
)

st.write("Ask me anything you want to know about Cybersecurity!")


if st.button("Clear chat"):
    st.session_state.messages = []
    st.rerun()

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Input for new message
if prompt := st.chat_input("Ask something..."):
    # Modify prompt to make responses shorter
    concise_prompt = f"""
    {prompt}
    
    Provide a concise response to: {prompt}. 
    Do not answer questions that are not related to cybersecurity. 
    Maintain a friendly, conversational and humanized tone. 
    Your answer must be the maximum 3-5 sentences. 
    Avoid providing responses that are not prompted. 
    """

    # Show user message (only original prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Get response from Gemini
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Configure model with shorter response settings
                model = genai.GenerativeModel(
                    "gemini-1.5-flash",
                    generation_config={
                        "max_output_tokens": 200,  # Limit token count for shorter responses
                        "temperature": 0.7,  # More focused answers
                    },
                )

                # Generate response using the modified prompt
                response = model.generate_content(concise_prompt)

                # Display response
                st.write(response.text)

                # Save to chat history
                st.session_state.messages.append(
                    {"role": "assistant", "content": response.text}
                )
            except Exception as e:
                st.error(f"Error: {str(e)}")
