from neo4j import GraphDatabase
from dotenv import load_dotenv
import os
import streamlit as st 
import pandas as pd
import time

load_dotenv()

URI = os.getenv("NEO4J_URI")
USER = os.getenv("NEO4J_USER")
PASS = os.getenv("NEO4J_PASS")


def main():
    col1, col2, col3 = st.columns(3, gap="large")
    
    with col1:    
        st.header(":blue[Neo4j] Fraud Detection")
    
    with col3:
        st.image("images/fraud-detection.png", width=150)
        
    with st.sidebar:
        st.title("Neo4j Fraud Detection")
        st.markdown("---")
        st.markdown("### About")
        st.info(
            "This is a Neo4j Fraud Detection project. "
            "The goal is to display analytics regarding financial fraud using Neo4j and using Machine Learning models to predict fraud in financial transactions"
        )
        st.markdown("---")
        st.markdown("### Queries to run")
        st.markdown("---")
        st.markdown("### Connect to database to continue")
        
    if st.session_state.setdefault("user", None) is None:
        user = st.text_input(label="Username")
        password = st.text_input(label="Password", type="password")
        if st.button(
            label="Login", on_click=on_login_click, args=(user, password)
        ):
            st.error("Invalid user name or password.")
    else:
        
        st.button("Disconnect", on_click=on_logout_click)
        with GraphDatabase.driver(URI, auth=(USER,PASS)) as driver:
            query = st.text_area("Enter your query here")
            if st.button("Run query"):
                df = run_query(driver, query)
                if df is not None:
                    st.dataframe(df)
                else:
                    st.error("Invalid query")
           


def run_query(driver, query):
    with driver.session() as session:
        try:
            result = session.run(query)
        except Exception as e:
            return None
        
        return pd.DataFrame(result.data())

def on_login_click(user, password):
    if authenticate(user=user, password=password):
        st.session_state["user"] = user


def on_logout_click():
    st.session_state["user"] = None
    


def authenticate(user, password):
    return user == USER and password == PASS


if __name__ == "__main__":
    main()
    
    # with st.form(key='my_form'):
    #     username = st.text_input('Username')
    #     password = st.text_input('Password', type='password')
    #     st.form_submit_button('Connect')
    # AUTH = (username, password)
    
     
    # if (username == USER and password == PASS):
    #     st.success("Connected to Neo4j database")
    #     with GraphDatabase.driver(URI, auth=AUTH) as driver:
    #         with driver.session() as session:
    #             result = session.run("MATCH (n:Merchant) RETURN DISTINCT n.name LIMIT 10")
    #             df = pd.DataFrame([r.values() for r in result], columns=result.keys())
    #             st.dataframe(df)
    # elif (username != USER and password != PASS) and (len(username) != 0 and len(password) != 0):
    #     st.error("Invalid credentials")
    
        
# if __name__ == "__main__":
#     main()
    
# def main():
#     