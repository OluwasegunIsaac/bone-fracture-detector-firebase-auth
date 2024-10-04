import streamlit as st
from PIL import Image

st.set_page_config(layout="wide")


logo_path = "assets/logo.png"  # Path to your logo
logo = Image.open(logo_path)
logo = logo.resize((700, 140))  # Resize the logo
_, col1,_ = st.columns([1,2.5,1.3])
with col1:
    st.image(logo, use_column_width=True)

# Hiding the sidebar using custom CSS
hide_sidebar_style = """
    <style>
    /* Hide the Streamlit sidebar */
    [data-testid="stSidebar"] {
        display: none;
    }
    </style>
"""
st.markdown(hide_sidebar_style, unsafe_allow_html=True)


# --- PAGE SETUP ---
login = st.Page(page="pages/login.py", title="Login Page", icon=":material/home:", default=True)
app = st.Page(page="pages/app.py", title="Bone Fracture Detection", icon=":material/home:")


# --- NAVIGATION SETUP ---
pg = st.navigation(pages=[login, app])

pg.run()
