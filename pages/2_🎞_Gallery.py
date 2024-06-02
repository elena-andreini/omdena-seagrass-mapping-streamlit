import streamlit as st

st.title("Gallery :film_frames:")
st.markdown("*This page displays the images, masks and their predictions for Greece and Croatia regions*")

# Displaying the images
st.image("model_utils\Greece_images\image1.JPG", caption='Greece image1')
st.image("model_utils\Greece_images\image2.JPG", caption='Greece image2')
st.image("model_utils\Croatia_images\image1.JPG", caption='Croatia image1')
st.image("model_utils\Croatia_images\image2.JPG", caption='Croatia image2')



