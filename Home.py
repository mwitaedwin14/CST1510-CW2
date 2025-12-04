# Home.py - YOUR FINAL WORKING VERSION
import streamlit as st
import pandas as pd
from datetime import datetime
from app.data.incidents import get_all_incidents, insert_incident

st.set_page_config(page_title="Cyber Intelligence Platform", page_icon="shield")

st.title("First Page")
st.subheader("This is a subheader")

name = st.text_input("Enter your name")
if st.button("Submit"):
    st.write(f"Hello, **{name}**!")

# Sample static data
df = pd.DataFrame({
    "User": ["Alice", "Bob", "Charlie", "David"],
    "Score": [52, 60, 88, 75]
})
st.dataframe(df)

# ==================== CYBER INCIDENTS SECTION ====================
st.subheader("Cyber Incidents")

df_incidents = get_all_incidents()

if df_incidents.empty:
    st.info("No incidents in database yet. Add one below!")
else:
    # Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Incidents", len(df_incidents))
    with col2:
        st.metric("High/Critical", len(df_incidents[df_incidents["severity"].isin(["High", "Critical"])]))
    with col3:
        st.metric("Open", len(df_incidents[df_incidents["status"] == "Open"]))

    # Bar chart
    severity_counts = df_incidents["severity"].value_counts()
    st.bar_chart(severity_counts)

    # Show table
    st.dataframe(df_incidents, use_container_width=True)

# ==================== ADD NEW INCIDENT FORM ====================
st.markdown("## Add New Incident")

with st.form("add_incident_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        date = st.date_input("Date of Incident", value=datetime.today())
        incident_type = st.selectbox("Type", ["Phishing", "Malware", "DDoS", "Brute Force", "Data Leak", "Insider Threat"])
    with col2:
        severity = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"])
        status = st.selectbox("Status", ["Open", "In Progress", "Resolved", "Closed"])

    description = st.text_area("Description")
    reported_by = st.text_input("Reported by (your name)", value="admin")

    submitted = st.form_submit_button("Submit Incident", type="primary")

    if submitted:
        # THIS IS THE CRITICAL FIX: convert date → string
        insert_incident(
            date=str(date),                    # ← Convert to string!
            incident_type=incident_type,
            severity=severity,
            status=status,
            description=description,
            reported_by=reported_by
        )
        st.success(f"Incident reported on {date}!")
        st.rerun()

st.caption("CST1510 - Multi-Domain Intelligence Platform | Week 9 Final Project")