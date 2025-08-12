import streamlit as st
from pymongo import MongoClient
from bson.objectid import ObjectId


#connecting to local database
client = MongoClient("mongodb://localhost:27017")
db = client["contactsApp"]
collection = db["contacts"]

#delete function
def delete_form():
    st.title("Delete Contacts")
     #fetch the data
    contact_list = list(collection.find())


    # Dictionary to track selected contacts
    selected_contacts = []

    # Display each contact with a checkbox
    for contact in contact_list:
        contact_id = str(contact["_id"])
        contact_label = f"{contact['name']} — {contact['phone']}"
        #add to selected_contacts list
        if st.checkbox(contact_label, key=contact_id):
            selected_contacts.append(contact_id)

    #checks If contacts are present are not
    if not contact_list:
        st.info("No contacts to display")

    #display success msg is displayed before rerun. as streamlit read top-down approach
    if st.session_state.get("delete_success"): # this flag wont clear off after rerun. So it is used
        st.success("Successfully Deleted")
        st.session_state["delete_success"] = False  # Reset so it wont display uneseccarily

    #delete logic
    if st.button("Delete Selected Contacts"):
        if selected_contacts:
            for contact_id in selected_contacts:
                collection.delete_one({"_id": ObjectId(contact_id)})
            #the below keeps in memory whether delete button clicked and remmebers after rerun.
            st.session_state["delete_success"] = True  # Set flag before rerun
            st.rerun()
            
        else:
            st.warning("No contacts selected")
        











