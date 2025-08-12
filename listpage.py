import streamlit as st
from pymongo import MongoClient

#connecting to local database
client = MongoClient("mongodb://localhost:27017")
db = client["contactsApp"]
collection = db["contacts"]

#view list function
def view_list():
    #fetch the data
    data = list(collection.find())

    #to clean data- not to show MongoDbs default object id
    for item in data:
        item.pop("_id",None)

    #display data
    st.title("List of Contacts")
    if data:
        st.dataframe(data)
    else:
        st.info("No Contacts found!")


