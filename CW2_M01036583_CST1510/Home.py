# Home.py
import streamlit as st
import pandas as pd
from datetime import datetime
from app.data.incidents import get_all_incidents, insert_incident
from app.data.db import connect_database
from app.data.schema import create_all_tables
import google.generativeai as genai

#GEMINI AI SETUP
genai.configure(api_key="AIzaSyC3A3G2aVL_891cbAUOnY-Obc9ylr8Ul_0")
model = genai.GenerativeModel('gemini-1.5-flash')  # THIS ONE WORKS

#DATABASE INITIALIZATION
if 'db_initialized' not in st.session_state:
    conn = connect_database()
    create_all_tables()

    # Load real data from CSVs
    pd.read_csv('DATA/cyber_incidents.csv').to_sql('cyber_incidents', conn, if_exists='replace', index=False)
    pd.read_csv('DATA/datasets_metadata.csv').to_sql('datasets_metadata', conn, if_exists='replace', index=False)
    pd.read_csv('DATA/it_tickets.csv').to_sql('it_tickets', conn, if_exists='replace', index=False)

    conn.close()
    st.session_state.db_initialized = True
    st.success("Database loaded with real data!")

st.set_page_config(page_title="Multi-Domain Intelligence Platform", page_icon="shield")

#LOGIN SYSTEM
from app.data.users import get_user_by_username, insert_user
import bcrypt

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
            st.success("Account created! Now log in.")
    st.stop()
else:
    st.sidebar.success(f"Welcome, {st.session_state.username}")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

#GEMINI AI ASSISTANT
st.sidebar.title("Gemini AI Assistant")
question = st.sidebar.text_input("Ask about incidents/data", key="ai_q")

if st.sidebar.button("Get Answer", key="ai_btn"):
    if question.strip():
        df = get_all_incidents()
        summary = f"""
        Total incidents: {len(df)}
        Open: {len(df[df['status'] == 'Open'])}
        High/Critical: {len(df[df['severity'].isin(['High', 'Critical'])])} 
        Most common: {df['incident_type'].mode().iloc[0] if not df.empty else 'None'}
        """
        with st.spinner("Thinking..."):
            response = model.generate_content(f"{summary}\n\nQuestion: {question}")
            st.sidebar.success(response.text)
    else:
        st.sidebar.error("Type a question!")

#MULTI-DOMAIN NAVIGATION
st.sidebar.title("Domains")
domain = st.sidebar.radio("Select Domain", ["Cybersecurity", "Data Science", "IT Operations"])

#MAIN CONTENT BASED ON DOMAIN
if domain == "Cybersecurity":
    st.title("Cybersecurity Dashboard")

    df_incidents = get_all_incidents()

    if df_incidents.empty:
        st.info("No incidents in database yet. Add one below!")
    else:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Incidents", len(df_incidents))
        with col2:
            st.metric("High/Critical", len(df_incidents[df_incidents["severity"].isin(["High", "Critical"])]))
        with col3:
            st.metric("Open", len(df_incidents[df_incidents["status"] == "Open"]))

        st.bar_chart(df_incidents["severity"].value_counts())
        st.dataframe(df_incidents, use_container_width=True)

    # ONE AND ONLY INCIDENT FORM
    st.markdown("## Add New Incident")
    with st.form("add_incident_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            date = st.date_input("Date of Incident", value=datetime.today())
            incident_type = st.selectbox("Type",
                                         ["Phishing", "Malware", "DDoS", "Brute Force", "Data Leak", "Insider Threat"])
        with col2:
            severity = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"])
            status = st.selectbox("Status", ["Open", "In Progress", "Resolved", "Closed"])

        description = st.text_area("Description")
        reported_by = st.text_input("Reported by", value=st.session_state.username or "admin")

        if st.form_submit_button("Submit Incident"):
            insert_incident(str(date), incident_type, severity, status, description, reported_by)
            st.success(f"Incident reported on {date}!")
            st.rerun()

elif domain == "Data Science":
    st.title("Data Science Dashboard")
    df = pd.read_csv("DATA/datasets_metadata.csv")
    st.metric("Total Datasets", len(df))
    st.dataframe(df, use_container_width=True)
    if 'category' in df.columns:
        st.bar_chart(df["category"].value_counts())

elif domain == "IT Operations":
    st.title("IT Operations Dashboard")
    df = pd.read_csv("DATA/it_tickets.csv")
    st.metric("Open Tickets", len(df[df["status"] == "Open"]))
    st.dataframe(df, use_container_width=True)
    if 'priority' in df.columns:
        st.bar_chart(df["priority"].value_counts())

st.caption("CST1510 – Multi-Domain Intelligence Platform")