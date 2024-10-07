import streamlit as st
from pages.functions import add_user_to_firestore, fetch_user_from_firestore, hash_password, check_password

def login_ui():

    # Streamlit app layout
    st.markdown("""
        <style>
        .app-spacing {
            margin-top: -70px;
            margin-bottom: -30px;
        }
        </style>
        """, unsafe_allow_html=True)

    app_name = """
        <div class='app-spacing' style="padding:4px">
        <h1 style='text-align: center; color: #22686E; font-size: 50px;'>Bone Fracture Detection System</h1>
        </div>
        """
    st.markdown(app_name, unsafe_allow_html=True)
    

    _,col1,_ = st.columns([0.9,2,1])

    with col1:
        st.divider()
        st.markdown("""
        <style>
        .app-spacing {
            margin-top: -30px;
            margin-bottom: -30px;
        }
        </style>
        """, unsafe_allow_html=True)

        header = """
            <div class='app-spacing' style="padding:4px">
            <h1 style='text-align: center; color: #22686E; font-size: 30px;'>Login</h1>
            </div>
            """
        st.markdown(header, unsafe_allow_html=True)
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login", type="primary", use_container_width=True):
            if username and password:
                user_data = fetch_user_from_firestore(username)
                if user_data:
                    # Check if the password matches the hashed password stored in Firestore
                    if check_password(user_data['password'], password):
                        st.success("Login successful!")
                        st.session_state.user = username  # Store the username in session state
                        st.session_state.user_data = user_data  # Store user data in session state
                        return True  # Indicate that login was successful
                    else:
                        st.error("Incorrect password. Please try again.")
                else:
                    # If the user doesn't exist, create a new user entry
                    new_user_data = {
                        "username": username,
                        "password": hash_password(password),  # Hash the password before storing
                    }
                    add_user_to_firestore(username, new_user_data)
                    st.success("New user created and logged in!")
                    st.session_state.user = username  # Store the username in session state
                    return True  # Indicate that login was successful
            else:
                st.error("Please enter both username and password")
        return False  # Indicate that login was not successful

if login_ui():
    st.switch_page("pages/app.py")  # Switch to the app page if login is successful

_,col1,_ = st.columns([0.9,2,1])

with col1:
    if st.button("Continue without login", type="secondary", use_container_width=True):
        st.session_state.user = "guest"  # Set session state for guest user
        st.switch_page("pages/app.py")
