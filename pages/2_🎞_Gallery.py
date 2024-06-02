import streamlit as st
import os

st.title("Gallery :film_frames:")
st.markdown("*This page displays the images, masks and their predictions for Greece and Croatia regions*")

base_path = "model_utils"
# Displaying the images
st.image(os.path.join(base_path, "Greece_images", "image1.JPG"), caption='Greece image1')
st.image(os.path.join(base_path, "Greece_images", "image2.JPG"), caption='Greece image2')
st.image(os.path.join(base_path, "Croatia_images", "image1.JPG"), caption='Croatia image1')
st.image(os.path.join(base_path, "Croatia_images", "image2.JPG"), caption='Croatia image2')