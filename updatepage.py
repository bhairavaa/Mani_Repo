import streamlit as st
from pymongo import MongoClient
from bson.objectid import ObjectId

#connecting to local database
client = MongoClient("mongodb://localhost:27017")
db = client["contactsApp"]
collection = db["contacts"]

#edit contact function
def edit_contact_form():
    with st.form("update_form",clear_on_submit=True):
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

        #display the success message
        if st.session_state.get("update_success"):
            st.success("Contact updated successfully")
            st.session_state["update_success"] = False #Resetting the flag

        #check new name and digits
        #checks the length of the new name
        def is_valid_name(new_name):
            return len(name.strip()) >= 3 and len(name.strip()) <=25
        #checks whether the input is digit and length of the new phone number is exactly 10 digits
        def is_valid_phone(new_phone):
            return new_phone.isdigit() and len(new_phone) == 10

        if st.form_submit_button("Update"):
            if new_name and new_phone:
                #check the conditions and verify
                if not is_valid_name(new_name):
                    st.error("Name must be at least 3 characters long.")
                elif not is_valid_phone(new_phone):
                    st.error("Phone number must be exactly 10 digits.")
                else:
                 #To update in database
                    collection.update_one(
                        {"_id": ObjectId(contact_id)},
                        {"$set": {"name": new_name, "phone": new_phone}}
                    )
                    # storing in temporary flag that button is clicked 
                    st.session_state["update_success"] = True #setting the flag
                    st.rerun()




