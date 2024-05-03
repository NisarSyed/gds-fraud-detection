from neo4j import GraphDatabase
from dotenv import load_dotenv
import os
import streamlit as st 
import pandas as pd

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
        st.title("Welcome to our CS-343 Project")
        st.markdown("---")
        st.markdown("### About")
        st.info(
            "This is a Neo4j Fraud Detection app. "
            "The goal is to display analytics regarding financial fraud using Neo4j and to predict fraud in financial transactions using machine learning models."
        )
        st.markdown("---")
              
    if st.session_state.setdefault("user", None) is None:
        st.text("Connect to Neo4j Database to continue")
        
        user = st.text_input(label="Username")
        password = st.text_input(label="Password", type="password")
        if st.button(
            label="Login", on_click=on_login_click, args=(user, password)
        ):
            st.error("Invalid user name or password.")
    else:
        
        st.sidebar.button("Disconnect", on_click=on_logout_click)
        
        #Display information about the app and what it can do
        st.write("This app allows you to view graph analytics and predict fraudulent transactions. Please select one of the options below.")
        
        # Display options with placeholder
        st.page_link("pages/prediction.py", label="Prediction", icon="🔮")
        st.page_link("pages/analytics.py", label="Graph Analytics", icon="📊")
            
            
def on_login_click(user, password):
    if authenticate(user=user, password=password):
        st.session_state["user"] = user

def on_logout_click():
    st.session_state["user"] = None

def authenticate(user, password):
    return user == USER and password == PASS

if __name__ == "__main__":
    main()