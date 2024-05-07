import streamlit as st

quick_fill = False
def on_quick_fill_click():
    return not quick_fill

def reset():
    quick_fill = False

if st.session_state.setdefault("user", None) is None:
    st.text("Connect to Neo4j Database to continue")
    st.page_link("home.py", label="Home", icon="🏠")
else:
    st.subheader("Predict Fraudulent Transactions 🔮")
    
    flag = st.button("Quick Fill", on_click=on_quick_fill_click)
    st.button("Reset", on_click=reset)
    with st.form(key="prediction_form"):
        st.write("Enter the transaction details below to predict if it is fraudulent.")
        
        if flag:
            st.write("Quick Fill enabled")
            st.text_input("Client ID", value="1")
            st.text_input("Client Name", value="John Doe")
            st.text_input("Email", value="johndoe@gmail.com")
            st.text_input("SSN", value="123-45-6789")
            st.text_input("Phone", value="123-456-7890")
            st.number_input("Amount", value=1000)
            st.selectbox("Transaction With", ["Client"])
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
            # Call the prediction function here
            st.write("Prediction result here")
            
            # Reset form fields
            st.form_submit_button("Reset") 