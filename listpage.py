import streamlit as st
from pymongo import MongoClient
import pandas as pd

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
        df= pd.DataFrame(data)
        st.dataframe(df)

        # Convert DataFrame to CSV
        csv = df.to_csv(index=False).encode("utf-8")

        # Download button
        st.download_button(
            label="📥 Download Contacts as CSV",
            data=csv,
            file_name="contacts_list.csv",
            mime="text/csv"
        )
    else:
        st.info("No Contacts found!")




