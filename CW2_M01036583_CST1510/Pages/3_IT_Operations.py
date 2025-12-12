# pages/3_IT_Operations.py
import streamlit as st
import pandas as pd
from app.data.tickets import get_all_tickets, insert_ticket  # Assume Week 8

st.title("IT Operations Intelligence")

df_tickets = get_all_tickets()

if df_tickets.empty:
    st.info("No tickets yet. Add one below!")
else:
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Tickets", len(df_tickets))
    with col2:
        st.metric("Open Tickets", len(df_tickets[df_tickets["status"] == "Open"]))

    priority_counts = df_tickets["priority"].value_counts()
    st.bar_chart(priority_counts)

    st.dataframe(df_tickets, use_container_width=True)

# Add form (expand more – with assigned_to input)
st.markdown("## Add New Ticket")
with st.form("add_ticket"):
    ticket_id = st.text_input("Ticket ID")
    priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
    status = st.selectbox("Status", ["Open", "In Progress", "Resolved", "Closed"])
    category = st.selectbox("Category", ["Hardware", "Software", "Network"])
    subject = st.text_input("Subject")
    description = st.text_area("Description")
    assigned_to = st.text_input("Assigned To")
    if st.form_submit_button("Submit Ticket"):
        insert_ticket(ticket_id, priority, status, category, subject, description, "2025-12-10", assigned_to)
        st.success("Ticket added!")
        st.rerun()