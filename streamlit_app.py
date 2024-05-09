import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))
import streamlit as st
import utils_v2
import pages

########
# from streamlit_extras.let_it_rain import rain
# from streamlit_extras.colored_header import colored_header
# from page_utils import font_modifier, display_image

########
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """


def make_font_poppins():
    with open("src/styles.css") as css:
        st.markdown(f'<style>{css.read()}</style>' , unsafe_allow_html= True)

    # Render the custom CSS style
    st.markdown("<link href='https://fonts.googleapis.com/css2?family=Poppins:wght@500&display=swap' rel='stylesheet'>", unsafe_allow_html=True)

    # Hide Streamlit style
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

########

def display_image(url, caption=None):
    st.markdown("<p></p>",unsafe_allow_html=True)
    image_url = url
    st.image(image_url, caption=caption, use_column_width=True)
    st.markdown("<p></p>",unsafe_allow_html=True)

########



# Create a dictionary to map page names to their respective functions
pages = {
    "Home": pages.homepage,
    "About": pages.about,
    "Classify Image": pages.classify,
    "User Guide": pages.guide,
    "Datasets": pages.datasets,
    "Repository": pages.repository,
    "Gallery": pages.gallery
}
# Create a sidebar with page selection
page_selection = st.sidebar.radio("Where do you want to go?", list(pages.keys()))
# Run the selected page function
pages[page_selection]()

