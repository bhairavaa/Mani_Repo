import streamlit as st
from pymongo import MongoClient

#connecting to local database
client = MongoClient("mongodb://localhost:27017")
db = client["contactsApp"]
collection = db["contacts"]

def add_form():
    #Form Layout
    form_name = st.form("contacts_app",clear_on_submit=True)
    with form_name:
        st.title("User Info Page")
        name1=st.text_input("name", key = "name1")
        phone1 = st.text_input("Phone", key = "phone1")
        submitted = st.form_submit_button("Submit")

    #submit button
    if submitted:
        if name1 and phone1:
            # insert in MongoDB
            collection.insert_one({"name":name1,"phone":phone1})
            st.success("Contacts details submitted successfully")
        else:
            st.warning("Please fill both the fields")



