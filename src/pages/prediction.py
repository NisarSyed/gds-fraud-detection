import streamlit as st

if st.session_state.setdefault("user", None) is None:
    st.text("Connect to Neo4j Database to continue")
    st.page_link("home.py", label="Home", icon="🏠")
else:
    st.subheader("Predict Fraudulent Transactions 🔮")
    
    with st.form(key="prediction_form"):
        st.write("Enter the transaction details below to predict if it is fraudulent.")
        
        transaction_id = st.text_input(label="Transaction ID")
        step = st.number_input(label="Step", min_value=0, max_value=200)
        type = st.selectbox(label="Type", options=["CASH_IN", "CASH_OUT", "DEBIT", "PAYMENT", "TRANSFER"])
        amount = st.number_input(label="Amount", min_value=0.0, step=0.01)
        name_orig = st.text_input(label="Name Orig")
        oldbalance_org = st.number_input(label="Old Balance Orig", min_value=0.0, step=0.01)
        newbalance_orig = st.number_input(label="New Balance Orig", min_value=0.0, step=0.01)
        name_dest = st.text_input(label="Name Dest")
        oldbalance_dest = st.number_input(label="Old Balance Dest", min_value=0.0, step=0.01)
        newbalance_dest = st.number_input(label="New Balance Dest", min_value=0.0, step=0.01)
        
        if st.form_submit_button("Predict"):
            # Call the prediction function here
            st.write("Prediction result here")
            
            # Reset form fields
            st.form_submit_button("Reset")