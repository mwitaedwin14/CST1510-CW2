import streamlit as st
from google import genai

client = genai.Client(api=st.secrets["AIzaSyC3A3G2aVL_891cbAUOnY-Obc9ylr8Ul_0"])
st.subheader("Gemini API")

response = client.models.generate_content("Explain how AI works in a few words.")
print(response.text)


#Display existing messages
for message in st.seesion_state.messages:
