import firebase_admin
from firebase_admin import db , credentials
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
cred_path = os.path.join(BASE_DIR, "credentials.json")
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred, {"databaseURL": "https://my-servease-default-rtdb.asia-southeast1.firebasedatabase.app/"})

# creating reference to root node
ref = db.reference("/")

# retrieving data from root node
# data = ref.get()

def get_email_by_username(username : str) -> str:
    # Reference to the users node
    users_ref = db.reference("/customers")
    all_customers = users_ref.get()

    if not all_customers:
        return "No Customers found."

    #
    for user_id, user_data in all_customers.items():
        if user_data.get("username") == username:
            return user_data.get("email")

    return f"No user found with username '{username}'"

# email = get_email_by_username('bilaltahir2128')
# print(email)