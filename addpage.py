import streamlit as st
from pymongo import MongoClient
import pandas as pd


#connecting to local database
client = MongoClient("mongodb://localhost:27017")
db = client["contactsApp"]
collection = db["contacts"]
# check duplicates at database level itself even if the app logic misses,so code is here
collection.create_index("Phone", unique=True)


#checks the length of the name
def is_valid_name(name):
    # if not name.isdigit():
        return len(name.strip()) >= 3 and len(name.strip()) <=25
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
        submitted = st.form_submit_button("Add Contact")

    existing = collection.find_one({"Phone": phone1}) # insert in MongoDB
    #submit button
    if submitted:
        if name1 and phone1:
            #check the conditions and verify
            if not is_valid_name(name1):
                st.error("Name must be at least 3 characters long.")
            # elif name1.isdigit():  # this logic allows numbers in name
            #     st.error("Name cannot be Numerical")
            elif any(char.isdigit() for char in name1): #checks any numbers in name 
                st.error("Name cannot contain numbers.")
            elif not is_valid_phone(phone1):
                st.error("Phone number must be exactly 10 digits.")

            # insert in MongoDB
            # existing = collection.find_one({"Phone": phone1})
            elif existing:
                st.error("🚫 A contact with this phone number already exists.")
            else:
                collection.insert_one({"Name": name1, "Phone": phone1})
                st.success("✅ Contact details submitted successfully.")
            # else:
            #     collection.insert_one({"Name":name1,"Phone":phone1})
            #     st.success("Contacts details submitted successfully")
        else:
            st.warning("Please fill both the fields")
            
    #adding File upload widget
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

    #initialsing the session_state
    if "csv_uploaded" not in st.session_state:
        st.session_state["csv_uploaded"] = False #means csv not been uploaded
    if "result_count" not in st.session_state:
        st.session_state["result_count"] = 0



    #validating the csv files and session state
    if uploaded_file and not st.session_state["csv_uploaded"]:
        try: #try clause should always have except or final clause
            df_bulk = pd.read_csv(uploaded_file) #pd.read_csv() converts uploaded csv into structured table
            required_columns = {"Name","Phone"}
            if required_columns.issubset(df_bulk.columns): #checks whether the required columns are present in the uploaded csv
                st.dataframe(df_bulk) #users can preview the csv file
            else:
                st.error(f"CSV must contain : {','.join(required_columns)}")
        except Exception as e:
            st.error(f"Error reading CSV: {e}")     

      #to add bulk_contacts into database
        if st.button("Add Contacts in Bulk"): #in that button
            contacts_dict = df_bulk.to_dict(orient="records") #converts the csv in df_bulk into dictonary and store it as records in mongoDB   
            # result = collection.insert_many(contacts_dict) #inserts bulk contacts into the database
            # Get existing phone numbers from DB
            existing_phones = set(str(doc.get("Phone")).strip() for doc in collection.find({}, {"Phone": 1}) if doc.get("Phone"))
            # Filter out duplicates
            #check csv also for duplicates
            seen_phones = set()
            new_contacts = []
            duplicate_phones = []
            # for contact in contacts_dict:
            #     # Skip rows missing Name or Phone
            #     if not contact.get("Name") or not contact.get("Phone"):
            #         continue
            #     #checks and converts if any float to str
            #     phone_raw = contact.get("Phone")
            #     phone = str(int(float(phone_raw))) if isinstance(phone_raw, float) else str(phone_raw).strip()
            #     if phone in existing_phones or phone in seen_phones:
            #         duplicate_phones.append(phone)
            #     else:
            #         seen_phones.add(phone)
            #         new_contacts.append(contact)
            invalid_contacts = []  # Optional: track invalid rows

            for contact in contacts_dict:
                name = contact.get("Name", "").strip()
                phone_raw = contact.get("Phone")

                # Skip rows missing Name or Phone
                if not name or not phone_raw:
                    continue

                # Convert phone to string
                phone = str(int(float(phone_raw))) if isinstance(phone_raw, float) else str(phone_raw).strip()

                # Validate name and phone
                if not is_valid_name(name) or any(char.isdigit() for char in name):
                    invalid_contacts.append(f"{name} ({phone})")
                    continue
                if not is_valid_phone(phone):
                    invalid_contacts.append(f"{name} ({phone})")
                    continue

                # Check for duplicates
                if phone in existing_phones or phone in seen_phones:
                    duplicate_phones.append(phone)
                else:
                    seen_phones.add(phone)
                    new_contacts.append({"Name": name, "Phone": phone})


            # To log what is being inserted
            st.write("Contacts to be inserted:", new_contacts)

            st.session_state["duplicate_phones"] = duplicate_phones #store duplicated even if no new insert happens
            # Insert only unique contacts
            if new_contacts:
                
                try:
                    result = collection.insert_many(new_contacts)
                    st.session_state["csv_uploaded"] = True #csv has been uploaded
                    st.session_state["result_count"] = len(result.inserted_ids) # Instead of relying on result after rerun, saves the count before rerun:
                    
                    # Store formatted contact info for success message
                    added_contacts = [
                        f"{contact.get('Name', 'Unnamed')} ({str(contact['Phone']).strip()})"
                        for contact in new_contacts
                    ]
                    st.session_state["added_contacts"] = added_contacts
                    st.session_state["invalid_contacts"] = invalid_contacts

                    st.rerun() #reruns the page
                except Exception as e:
                    st.error(f"Unexpected error during bulk insert: {e}")
            else:
                # All contacts were duplicates
                st.session_state["csv_uploaded"] = True
                st.session_state["result_count"] = 0
                st.session_state["added_contacts"] = []
                st.session_state["invalid_contacts"] = invalid_contacts
                st.rerun()


    # ✅ Success message for added contacts
    if st.session_state.get("csv_uploaded"):
        if "added_contacts" in st.session_state:
            st.success(
                f"✅ Added {st.session_state['result_count']} contacts successfully! "
                f"These contacts were added: {', '.join(st.session_state['added_contacts'])}"
            )
        
        st.session_state["added_contacts"] = []
            
        # 🔴 Error message for duplicates
        if "duplicate_phones" in st.session_state and st.session_state["duplicate_phones"]:
            st.error(
                f"🚫 Skipped {len(st.session_state['duplicate_phones'])} duplicate contacts. "
                f"These phone numbers already exist: {', '.join(st.session_state['duplicate_phones'])}"
            )
        st.session_state["duplicate_phones"] = []  # Optional cleanup
    st.session_state["csv_uploaded"] = False


    # ⚠️ Warning for invalid rows
    if "invalid_contacts" in st.session_state and st.session_state["invalid_contacts"]:
        st.warning(
            f"⚠️ Skipped {len(st.session_state['invalid_contacts'])} invalid contacts due to formatting issues. "
            f"Examples: {', '.join(st.session_state['invalid_contacts'][:5])}"
        )
        st.session_state["invalid_contacts"] = []  # Optional cleanup


       