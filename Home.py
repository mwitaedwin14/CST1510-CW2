import streamlit as st
import pandas as pd
from app.data.incidents import get_all_incidents

st.title("first page")
st.subheader("This is a subheader")

name = st.text_input("Enter your name")
if st.button("Submit"):
    st.subheader(f"Hello, {name}")

df = pd.Dataframe({
    "User": ["Alice", "Bob", "Charlie", "David"],
    "Score": [52, 60, 88]
})

st.dataframe(df)

st.subheader("Cyber incidents")
df_incidents = get_all_incidents()

#Metrics
col1, col2 = st.columns(2)

with col1:
    st.metric("High",df_incidents["severity"]== "High"].shape[0])

with col2:
    st.metric("Incidents",df_incidents["severity"].count(), "1")


#Bar chart
    severity_counts = df_incidents["severity"].value_counts().reset_index()
    severity_counts.columms = ["severity", "count"]

    st.bar-chart(severity_counts.set_index("severity"))

#Add incidents
st.markdown("## Add incidents ##")
with st.form("Add new incident"):
    date = st.date_input("Enter a date")
    incident_type = st.selectbox("Incident type", ["Malware", "Phishing", "DDoS"])
    severity = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"])
    status

