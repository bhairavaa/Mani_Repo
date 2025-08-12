import streamlit as st
from pymongo import MongoClient
from bson.objectid import ObjectId

#connecting to local database
client = MongoClient("mongodb://localhost:27017")
db = client["contactsApp"]
collection = db["contacts"]

#edit contact function
def edit_contact_form():
    st.title("Edit Contact")
    #getting that selected contact and storing it
    contact_id = st.session_state.get("edit_id") #edit_it is got from updatepage.py the one which is selected there
    if not contact_id:
        st.warning("No contact selected.")
        return
    
    contact_e = collection.find_one({"_id": ObjectId(contact_id)})
    if not contact_e:
        st.error("Contact not found.")
        return

    # Pre-fill form
    new_name = st.text_input("Name", value=contact_e["name"])
    new_phone = st.text_input("Phone Number", value=contact_e["phone"])

    if st.button("Update"):
        collection.update_one(
            {"_id": ObjectId(contact_id)},
            {"$set": {"name": new_name, "phone": new_phone}}
        )
        st.success("Contact updated successfully.")
        st.session_state.page = "edit"
        st.rerun()

