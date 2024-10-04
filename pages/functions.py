import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st
import bcrypt

def init_firebase():
    """Initialize Firebase using credentials from secrets.toml."""
    if not firebase_admin._apps:  # Check if Firebase is already initialized
        firebase_secrets = st.secrets["firebase"]
        
        cred = credentials.Certificate({
            "type": firebase_secrets["type"],
            "project_id": firebase_secrets["project_id"],
            "private_key_id": firebase_secrets["private_key_id"],
            "private_key": firebase_secrets["private_key"].replace("\\n", "\n"),
            "client_email": firebase_secrets["client_email"],
            "client_id": firebase_secrets["client_id"],
            "auth_uri": firebase_secrets["auth_uri"],
            "token_uri": firebase_secrets["token_uri"],
            "auth_provider_x509_cert_url": firebase_secrets["auth_provider_x509_cert_url"],
            "client_x509_cert_url": firebase_secrets["client_x509_cert_url"]
        })
        
        # Initialize Firebase
        firebase_admin.initialize_app(cred)

def get_firestore_client():
    """Initialize and return Firestore client."""
    init_firebase()  # Ensure Firebase is initialized before accessing Firestore
    db = firestore.client()
    return db

def add_user_to_firestore(username, data):
    """Add or update user data in Firestore."""
    db = get_firestore_client()
    db.collection("users").document(username).set(data)
    return f"User '{username}' data added/updated in Firestore."

def fetch_user_from_firestore(username):
    """Fetch user data from Firestore."""
    db = get_firestore_client()
    user_doc = db.collection("users").document(username).get()
    return user_doc.to_dict() if user_doc.exists else None

def hash_password(password):
    """Hash a password using bcrypt."""
    salt = bcrypt.gensalt()  # Generate a salt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)  # Hash the password
    return hashed_password.decode('utf-8')  # Return as string

def check_password(hashed_password, user_password):
    """Check if the provided password matches the hashed password."""
    return bcrypt.checkpw(user_password.encode('utf-8'), hashed_password.encode('utf-8'))
