import streamlit as st
from pymongo import MongoClient

#connecting to local database
client = MongoClient("mongodb://localhost:27017")
db = client["contactsApp"]
collection = db["contacts"]


#checks the length of the name
def is_valid_name(name):
    return len(name.strip()) >= 3
#checks whether the input is digit and length of the phone number is exactly 10 digits
def is_valid_phone(phone):
    return phone.isdigit() and len(phone) == 10


def add_form():
    #Form Layout
    form_name = st.form("contacts_app",clear_on_submit=True)
    with form_name:
        st.title("User Info Page")
        name1=st.text_input("Name", key = "name1")
        phone1 = st.text_input("Phone", key = "phone1")
        submitted = st.form_submit_button("Submit")

    #submit button
    if submitted:
        if name1 and phone1:
            #check the conditions and verify
            if not is_valid_name(name1):
                st.error("Name must be at least 3 characters long.")
            elif not is_valid_phone(phone1):
                st.error("Phone number must be exactly 10 digits.")

            # insert in MongoDB
            else:
                collection.insert_one({"name":name1,"phone":phone1})
                st.success("Contacts details submitted successfully")
        else:
            st.warning("Please fill both the fields")



