import streamlit as st 


st.set_page_config(
        page_title="Sentimen Analisis Marketplace Online",
        page_icon=":department_store:",
        layout="wide",
        initial_sidebar_state="expanded"
    )



from PIL import Image
from StreamlitDashboard.dashboard import dashboard
from StreamlitDashboard.analysis import analysis
from StreamlitDashboard.paragraf_analisis_app import aplikasi
from StreamlitDashboard.about import about
from StreamlitDashboard.eda import eda



def load_image(image_path):
    return Image.open(image_path)

def setup_sidebar():
    st.sidebar.image(load_image('assets/gambar/sidebar.png'))
    st.sidebar.title("Project")

    # Inisialisasi state
    if "page" not in st.session_state:
        st.session_state.page = "Dashboard"

    # Button Navigation
    if st.sidebar.button("Dashboard"):
        st.session_state.page = "Dashboard"
    if st.sidebar.button("Exploratory Data Analisis"):
        st.session_state.page = "Exploratory Data Analisis"
    if st.sidebar.button("Preprocessing Data"):
        st.session_state.page = "Preprocessing Data"
        
    st.sidebar.title("Apps")
    
    if st.sidebar.button("Paragraf Analisis Apps"):
        st.session_state.page = "Paragraf Analisis App"
    
    st.sidebar.title("My Profil")
    
    if st.sidebar.button("About Me"):
        st.session_state.page = "About Me"


def run_app():
    setup_sidebar()

    if st.session_state.page == "Dashboard":
        dashboard()
    elif st.session_state.page == "Exploratory Data Analisis":
        eda()
    elif st.session_state.page == "Preprocessing Data":
        analysis()
    elif st.session_state.page == "Paragraf Analisis App":
        aplikasi()
    elif st.session_state.page == "About Me":
        about()

if __name__ == "__main__":
    run_app()
