import streamlit as st
from google import genai

client = genai.Client(api=st.secrets[])
st.subheader("Gemini API")







#Display existing messages
for message in st.seesion_state.messages:
