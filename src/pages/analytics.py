import streamlit as st
from neo4j import GraphDatabase
from home import URI, USER, PASS
from queries import *

if st.session_state.setdefault("user", None) is None:
    st.text("Connect to Neo4j Database to continue")
    st.page_link("home.py", label="Home", icon="🏠")
else:
    st.subheader("View Graph Analytics 📊")
    with GraphDatabase.driver(URI, auth=(USER,PASS)) as driver:
        query = st.text_area("Enter your custom query here")
        if st.button("Run query"):
            df = run_query(driver, query)
            if df is not None:
                try:
                    st.table(df)
                except Exception as e:
                    st.write(df)
            else:
                st.error("Invalid query")