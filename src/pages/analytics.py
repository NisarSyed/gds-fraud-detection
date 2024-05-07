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
        "Stats",
        "Nodes", 
        "Relationships",
        "Transactions", 
        "Suspicious FPF",
        "FPF",
        "Similar To",
        "Working with FPFs",
        "SPF",
        "Custom Query"
    ])
    with GraphDatabase.driver(URI, auth=(USER,PASS)) as driver:
        match type:
            case "Stats":
                st.subheader("Overall Stats")
                st.write("These are the overall stats our database, extracted using the APOC library.")
                df = view_stats(driver)
                st.dataframe(df)
            case "Nodes":
                st.subheader("Node Labels")
                st.write("These are the different node labels in our database, along with the count of each label.")
                df = view_labels(driver)
                st.table(df)
            case "Relationships":
                st.subheader("Relationship Types")
                st.write("These are the different relationship types in our database, along with the count of each relationship.")
                df = view_relationships(driver)
                st.table(df)
            case "Transactions":
                st.subheader("Transactions")
                st.write("These are the types of transactions in our database.")
                df = view_transactions(driver)
                st.table(df)
            case "Suspicious FPF":
                st.subheader(":red[Suspicious] First Party Fraudsters")
                st.write("These clients are labelled suspicious for having more than 2 shared identifiers (SSN/Email/Phone)")
                df = view_shared_identifiers(driver)
                st.table(df)
            case "FPF":
                st.subheader(":red[Confirmed] First Party Fraudsters")
                st.write("These clients are confirmed to be first party fraudsters.")
                df = view_fp_fraudsters(driver)
                st.table(df)
            case "Similar To":
                st.subheader("Similar Clients")
                st.write("These are the clients who are similar to each other based on node similarity algorithms.")
                df = view_similar_clients(driver)
                st.table(df)
            case "Working with FPFs":
                st.subheader("Working with First Party Fraudsters")
                st.write("These are the clients who transact with first party fraudsters, but aren't labelled as fraudsters themselves.")
                df = view_fp_transactions(driver)
                st.table(df)
            case "SPF":
                st.subheader(":red[Confirmed] Second Party Fraudsters")
                st.write("These clients are confirmed to be second party fraudsters.")
                df = view_sp_fraudsters(driver)
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