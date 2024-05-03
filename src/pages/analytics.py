import streamlit as st
from neo4j import GraphDatabase
from home import URI, USER, PASS
from queries import *

if st.session_state.setdefault("user", None) is None:
    st.text("Connect to Neo4j Database to continue")
    st.page_link("home.py", label="Home", icon="🏠")
else:
    st.subheader("View Graph Analytics 📊")
    
    type = st.selectbox("Select an option", [
        "", 
        "Labels", 
        "Relationships", 
        "Suspicious Clients",  
        "Custom Query"
    ])
    with GraphDatabase.driver(URI, auth=(USER,PASS)) as driver:
        match type:
            case "Labels":
                df = view_labels(driver)
                st.table(df)
            case "Relationships":
                df = view_relationships(driver)
                st.table(df)
            case "Suspicious Clients":
                df = view_shared_identifiers(driver)
                st.subheader(":red[Suspicious] Clients")
                st.write("These clients are labelled suspicious for having more than 2 shared identifiers (SSN/Email/Phone)")
                st.table(df)
            case "Custom Query":
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
        
    
   
        # query = st.text_area("Enter your custom query here")
        # if st.button("Run query"):
        #     df = run_query(driver, query)
        #     if df is not None:
        #         try:
        #             st.table(df)
        #         except Exception as e:
        #             st.write(df)
        #     else:
        #         st.error("Invalid query")