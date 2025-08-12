import streamlit as st
from addpage import add_form
from listpage import view_list
from deletepage import delete_form
from editpage import select_contact_to_edit
from updatepage import edit_contact_form
# Initialize session state
if "page" not in st.session_state: #checks if the user has already visited the page
    st.session_state.page = "Home"

# form1=st.form("Home",clear_on_submit= True)
# Navigation logic
if st.session_state.page == "Home":
    st.title("Welcome to Contact App")
    #add button
    if st.button("Add Contact"):
        st.session_state.page = "add"
        st.rerun()

    #list button
    if st.button("View Contacts"):
        st.session_state.page = "view"
        st.rerun()
    
    #Delete button
    if st.button("Delete Contacts"):
        st.session_state.page = "delete"
        st.rerun()

    #edit contact
    if st.button("Update Contacts"):
        st.session_state.page = "edit"
        st.rerun()

elif st.session_state.page == "add":
    add_form()
    #Show back button only on addpage
    if st.button("Back"):
        st.session_state.page = "Home"
        st.rerun()
elif st.session_state.page == "view":
    view_list()
    #Show back button only on listpage
    if st.button("Back"):
        st.session_state.page = "Home"
        st.rerun()
elif st.session_state.page == "delete":
    delete_form()
    #Show back button only on deletepage
    if st.button("Back"):
        st.session_state.page = "Home"
        st.rerun()
elif st.session_state.page == "edit":
    select_contact_to_edit()
    #Show back button only on edit page
    if st.button("Back"):
        st.session_state.page = "Home"
        st.rerun()
elif st.session_state.page == "update":
    edit_contact_form()
    #Show back button only on update page
    if st.button("Back"):
        st.session_state.page = "Home"
        st.rerun()


    