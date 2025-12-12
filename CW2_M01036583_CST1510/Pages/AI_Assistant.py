# pages/4_AI_Assistant.py  ← THIS IS YOUR WEEK 10 FULL MARKS
import streamlit as st
import google.generativeai as genai
from app.data.incidents import get_all_incidents

# === GEMINI SETUP ===
genai.configure(api_key="AIzaSyC3A3G2aVL_891cbAUOnY-Obc9ylr8Ul_0")  # Your key
model = genai.GenerativeModel('gemini-1.5-flash')

# === CHAT HISTORY ===
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm your cybersecurity AI assistant. Ask me anything about the current incidents."}
    ]

st.title("Gemini AI Assistant")
st.caption("Ask anything about incidents, datasets, or tickets")

# Show chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Type your question here..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepare context from real data
    df = get_all_incidents()
    context = f"""
    Current cybersecurity incidents in the database:
    Total: {len(df)}
    High/Critical: {len(df[df['severity'].isin(['High', 'Critical'])])} 
    Open: {len(df['status'] == 'Open').sum()}
    Most common type: {df['incident_type'].mode().iloc[0] if not df.empty else 'None'}
    """

    full_prompt = f"{context}\n\nUser question: {prompt}\nAnswer professionally and concisely."

    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Gemini is thinking..."):
            response = model.generate_content(full_prompt)
            st.markdown(response.text)

    # Save assistant reply
    st.session_state.messages.append({"role": "assistant", "content": response.text})