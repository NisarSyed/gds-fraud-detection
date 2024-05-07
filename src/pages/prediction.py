import streamlit as st
from neo4j import GraphDatabase
from home import URI, USER, PASS
from queries import *
from joblib import load

if st.session_state.setdefault("user", None) is None:
    st.text("Connect to Neo4j Database to continue")
    st.page_link("home.py", label="Home", icon="🏠")
else:
    driver = GraphDatabase.driver(URI, auth=(USER,PASS))
    st.subheader("Predict Fraudulent Transactions 🔮")
    
    flag = st.checkbox("Quick Fill")
    
    with st.form(key="prediction_form"):
        st.write("Enter the transaction details below to predict if it is fraudulent.")
        
        if flag:
            st.write("Quick Fill enabled")
            result = get_random_client(driver)
            client_id = st.text_input("Client ID", value=result[0]["id"])
            client_name = st.text_input("Client Name", value=result[0]["name"])
            email = st.text_input("Email", value=result[0]["email"])
            ssn = st.text_input("SSN", value=result[0]["ssn"])
            phone = st.text_input("Phone", value=result[0]["phone"])
            amount = st.number_input("Amount", value=result[0]["amount"])
            transaction_with = st.selectbox("Transaction With", [result[0]["TxWith"][0]])
            transaction_type = st.selectbox("Transaction Type", [result[0]["TxType"][0]])
        else:
            client_id = st.text_input("Client ID")
            client_name = st.text_input("Client Name")
            email = st.text_input("Email")
            ssn = st.text_input("SSN")
            phone = st.text_input("Phone")
            amount = st.number_input("Amount")
            transaction_with = st.selectbox("Transaction With", ["Client", "Merchant", "Bank"])
            transaction_type = st.selectbox("Transaction Type", ["CashIn", "CashOut", "Payment", "Debit", "Transfer"])
        
        if st.form_submit_button("Predict"):
            if client_id and client_name and email and ssn and phone and amount and transaction_with and transaction_type:
                st.write("Prediction result here")
                clf = load('./src/fraud_model.joblib')
                features = get_features(driver, client_id)
                e = features[0]["e"]
                s = features[0]["s"]
                p = features[0]["p"]
                t = features[0]["t"]
                r = features[0]["r"]
                poc = features[0]["poc"]
                cs = features[0]["cs"]
                fs = features[0]["fs"]
                prediction = clf.predict([[e, s, p, t, r, poc, cs, fs]])[0]
                st.write(f"Prediction: {prediction}")
                st.form_submit_button("Reset")
            else:
                st.error("Please fill all the fields.")
    driver.close()