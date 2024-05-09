import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))
import streamlit as st
import pages


# Mmapping page names to their respective functions
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

