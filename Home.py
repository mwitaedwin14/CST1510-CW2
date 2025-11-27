import streamlit as st
import pandas as pd
from app.data.incidents
import (get_all_incidents)

st.title("First Page")
st.subheader("This is a subheader")

name = st.text_input("Enter your name")
if st.button("Submit"):
    st.subheader(f"Hello, {name}")

# Fixed DataFrame creation (corrected spelling and balanced data)
df = pd.DataFrame({
    "User": ["Alice", "Bob", "Charlie", "David"],
    "Score": [52, 60, 88, 75]  # Added missing value to match 4 users
})

st.dataframe(df)

st.subheader("Cyber incidents")
df_incidents = get_all_incidents()

# Metrics - fixed syntax errors
col1, col2 = st.columns(2)

with col1:
    st.metric("High", df_incidents[df_incidents["severity"] == "High"].shape[0])

with col2:
    st.metric("Incidents", df_incidents.shape[0])  # Fixed: use shape[0] for total count

# Bar chart - fixed syntax errors
severity_counts = df_incidents["severity"].value_counts().reset_index()
severity_counts.columns = ["severity", "count"]  # Fixed spelling: 'columns' not 'columms'

st.bar_chart(severity_counts.set_index("severity"))  # Fixed: underscore not hyphen

# Add incidents
st.markdown("## Add incidents ##")
with st.form("Add new incident"):
    date = st.date_input("Enter a date")
    incident_type = st.selectbox("Incident type", ["Malware", "Phishing", "DDoS"])
    severity = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"])
    status = st.selectbox("Status", ["Open", "Closed", "In Progress", "Resolved"])
    description = st.text_input("Enter description")
    submitted = st.form_submit_button("Submit")

if submitted:
    # You'll need to import or define insert_incident function
    from app.data.incidents import insert_incident  # Add this import
    insert_incident(date, incident_type, severity, status, description)
    st.success("Incident added")
    st.rerun()