# Import library
import streamlit as st 
from PIL import Image

# Import pages
from StreamlitDashboard.dashboard import dashboard
from StreamlitDashboard.analysis import analysis
from StreamlitDashboard.paragraf_analisis_app import aplikasi
from StreamlitDashboard.about import about


# Set page config
st.set_page_config(
    page_title="Sentimen Analisi Marketplace Online",
    page_icon=":department_store:",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

# Load image in sidebar
st.sidebar.image('assets/gambar/icon_sentiment.png')


# Sidebar setup
st.sidebar.title("Project")

# Use session state to keep track of the current page
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

# Create buttons for navigation
if st.sidebar.button("Dashboard"):
    st.session_state.page = "Dashboard"
if st.sidebar.button("Proses Analisis"):
    st.session_state.page = "Proses Analisis"
if st.sidebar.button("Paragraf Analisis App"):
    st.session_state.page = "Paragraf Analisis App"
    
st.sidebar.title("Profil")

if st.sidebar.button("About Me"):
    st.session_state.page = "About Me"


# Page setup based on current session state
if st.session_state.page == "Dashboard":
    dashboard()

elif st.session_state.page == "Proses Analisis":
    analysis()

elif st.session_state.page == "Paragraf Analisis App":
    aplikasi()

elif st.session_state.page == "About Me":
    about()
    
    
    
















