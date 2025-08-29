import streamlit as st
from addpage import add_form
from listpage import view_list
from deletepage import delete_form
from editpage import select_contact_to_edit
from updatepage import edit_contact_form
# Initialize session state
if "page" not in st.session_state: #checks if the user has already visited the page
    st.session_state.page = "Home"


# Inject custom CSS
st.markdown("""
    <style>
    button {
        font-size: 30px;
        line-height: 30px;
        padding: 22px;
    }
    </style>
""", unsafe_allow_html=True)


st.title("📇 Contact Manager")

# Navigation logic
if st.session_state.page == "Home":
    st.markdown("Welcome to your personal contact book. Choose an action below:")
    # st.title("Welcome to Contact App")
    #add 2 columns
    col1 , col2 =st.columns([1,1])
    with col1:
        #add button
        if st.button("➕ Add Contact",use_container_width=True):
            st.session_state.page = "add"
            st.rerun()

        #list button
        if st.button("🔍 View Contacts",use_container_width=True):
            st.session_state.page = "view"
            st.rerun()
    
    with col2:
                #edit contact
        if st.button("📝 Update Contacts",use_container_width=True):
            st.session_state.page = "edit"
            st.rerun()

        #Delete button
        if st.button("❌ Delete Contacts",use_container_width=True):
            st.session_state.page = "delete"
            st.rerun()

elif st.session_state.page == "add":
    st.markdown("Enter Contact Details Below:")
    add_form()
    #Show back button only on addpage
    if st.button("Back"):
        st.session_state.page = "Home"
        st.rerun()
elif st.session_state.page == "view":
    st.markdown("View Contact Details Below:")
    view_list()
    #Show back button only on listpage
    if st.button("Back"):
        st.session_state.page = "Home"
        st.rerun()
elif st.session_state.page == "delete":
    st.markdown("Select Contact(s) To Be Deleted Below:")
    delete_form()
    #Show back button only on deletepage
    if st.button("Back"):
        st.session_state.page = "Home"
        st.rerun()
elif st.session_state.page == "edit":
    # st.markdown("Select Contact To Be Updated Below:")
    select_contact_to_edit()
    #Show back button only on edit page
    if st.button("Back"):
        st.session_state.page = "Home"
        st.rerun()
elif st.session_state.page == "update":
    st.markdown("Update Contact Details Below:")
    edit_contact_form()
    #Show back button only on update page
    if st.button("Back"):
        st.session_state.page = "Home"
        st.rerun()


