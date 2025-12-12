# pages/2_Data_Science.py
import streamlit as st
import pandas as pd
from app.data.datasets import get_all_datasets, insert_dataset  # Assume you have these from Week 8

st.title("Data Science Intelligence")

df_datasets = get_all_datasets()

if df_datasets.empty:
    st.info("No datasets yet. Add one below!")
else:
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Datasets", len(df_datasets))
    with col2:
        st.metric("Total Size (MB)", df_datasets['file_size_mb'].sum())

    category_counts = df_datasets["category"].value_counts()
    st.bar_chart(category_counts)

    st.dataframe(df_datasets, use_container_width=True)

# Add form (expand more – with file size input)
st.markdown("## Add New Dataset")
with st.form("add_dataset"):
    name = st.text_input("Dataset Name")
    category = st.selectbox("Category", ["Threat Intelligence", "Network Logs", "User Behavior"])
    source = st.text_input("Source")
    record_count = st.number_input("Record Count", min_value=0)
    file_size_mb = st.number_input("File Size (MB)", min_value=0.0)
    if st.form_submit_button("Submit Dataset"):
        insert_dataset(name, category, source, "2025-12-10", record_count, file_size_mb)
        st.success("Dataset added!")
        st.rerun()