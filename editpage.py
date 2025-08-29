import streamlit as st
from pymongo import MongoClient
import pandas as pd

#connecting to local database
client = MongoClient("mongodb://localhost:27017")
db = client["contactsApp"]
collection = db["contacts"]

def select_contact_to_edit():
    st.title("Update Contact")
    #fetch contacts
    contact_list = list(collection.find())
    if not contact_list:
        st.info("No contacts available.")
        return
    
    # # Convert contact list to DataFrame
    # df = pd.DataFrame(contact_list)
    # df = df[["name", "phone"]]  # Show only relevant columns
    # st.subheader("Contact List")
    # st.dataframe(df)

    # Create radio button options
    #converting it into a id of string datatype so that mongoDB understands
    options = {f"{c['Name']} — {c['Phone']}": str(c["_id"]) for c in contact_list}
    #captures user selection
    selected_label = st.radio("Select a contact to update:", list(options.keys()))
    # selected_label = st.selectbox("Select a contact to update:", list(options.keys()))

    if st.button("Edit Selected Contact"):
        st.session_state.edit_id = options[selected_label]
        st.session_state.page = "update"
        st.rerun()

# if __name__ == "__main__":
#     select_contact_to_edit()  # or add_form(), view_list()
