import streamlit as st
import pandas as pd
from datetime import datetime
from app.data.incidents import get_all_incidents, insert_incident

st.set_page_config(page_title="Cyber Intelligence Platform", page_icon="shield")

import sqlite3
sqlite3.connect('DATA/intelligence_platform.db', timeout=10.0)  # Increases lock timeout

from app.data.users import get_user_by_username, insert_user
import bcrypt

import google.generativeai as genai

GEMINI_API_KEY = "AIzaSyC3A3G2aVL_891cbAUOnY-Obc9ylr8Ul_0"  #

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# ============ LOGIN SYSTEM ============
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Login")
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Log In"):
            user = get_user_by_username(username)
            if user and bcrypt.checkpw(password.encode(), user[2].encode()):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Wrong username/password")
    with col2:
        st.subheader("Register")
        new_u = st.text_input("New username", key="reg_user")
        new_p = st.text_input("New password", type="password", key="reg_pass")
        if st.button("Register"):
            hashed = bcrypt.hashpw(new_p.encode(), bcrypt.gensalt())
            insert_user(new_u, hashed.decode())
            st.success("Account created!")
    st.stop()  # ← stops the app until logged in
else:
    st.sidebar.success(f"Welcome, {st.session_state.username}")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

st.sidebar.title("Gemini AI Assistant")
question = st.sidebar.text_input("Ask about incidents/data", key="ai_question")

if st.sidebar.button("Generate an Answer", key="ai_button"):
    if question.strip() == "":
        st.sidebar.error("Please type a question")
    else:
        # Get current data
        df_incidents = get_all_incidents()
        data_summary = f"""
        Current incidents: {len(df_incidents)}
        Most common type: {df_incidents['incident_type'].mode().iloc[0] if not df_incidents.empty else 'None'}
        High/Critical: {len(df_incidents[df_incidents['severity'].isin(['High', 'Critical'])])} 
        Open: {len(df_incidents[df_incidents['status'] == 'Open'])}
        """

        full_prompt = f"""
        You are a senior cybersecurity analyst.
        {data_summary}

        User question: {question}
        Give a short, professional answer.
        """


        with st.spinner("Gemini is thinking..."):
            import google.generativeai as genai

            genai.configure(api_key="AIzaSyC3A3G2aVL_891cbAUOnY-Obc9ylr8Ul_0")
            model = genai.GenerativeModel('gemini-1.5-flash-latest')
            response = model.generate_content(full_prompt)

        st.sidebar.success("Gemini Answer:")
        st.sidebar.write(response.text)


# Sidebar for domain navigation
st.sidebar.title("Domains")
domain = st.sidebar.radio("Select Domain", ["Cybersecurity", "Data Science", "IT Operations"])

if domain == "Cybersecurity":
    st.title("Cybersecurity Dashboard")
elif domain == "Data Science":
    st.title("Data Science Dashboard")
elif domain == "IT Operations":
    st.title("IT Operations Dashboard")


st.title("First Page")
st.subheader("Report your incidents:")

name = st.text_input("Enter your name")
if st.button("Submit"):
    st.write(f"Hello, **{name}**!")

# Sample static data
df = pd.DataFrame({
    "User": ["Alice", "Bob", "Charlie", "David"],
    "Score": [52, 60, 88, 75]
})
st.dataframe(df)

#CYBER INCIDENTS SECTION
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

# ADD NEW INCIDENT FORM
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

        insert_incident(
            date=str(date),
            incident_type=incident_type,
            severity=severity,
            status=status,
            description=description,
            reported_by=reported_by
        )
        st.success(f"Incident reported on {date}!")
        st.rerun()

st.caption("CST1510 - Multi-Domain Intelligence Platform")