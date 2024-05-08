import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import utils_v2
from model_utils import *

import tifffile as tiff
import tensorflow as tf
# import numpy as np

# Loading the images & masks as an array


    
def show_image(image_path) :
    im =load_image()
    
#####
def display_image(url, caption=None):
    st.markdown("<p></p>",unsafe_allow_html=True)
    image_url = url
    st.image(image_url, caption=caption, use_column_width=True)
    st.markdown("<p></p>",unsafe_allow_html=True)


##############

# Streamlit app
def dp_main(image_file):
    model = utils_v2.retrieve_model()
    
    if image_file is not None:
        # Display the chosen image
        image = load_image(image_file)
        X = preprocess_image(image)
        y = model.predict(X)
        y = np.squeeze(y, axis=0)
        
        # Create a plot
        plt.axis('off')
        fig, (ax1, ax2) = plt.subplots(1, 2)
        ax1.imshow(image[:, :, 3])
        ax2.imshow(y)
        # Display the image in streamlit
        st.pyplot(fig)
        
        # Make a prediction and display it
        # prediction = predict(load_image(image_file))
        # st.write("Prediction: ", prediction[1])
        # st.write("Confidence: ", prediction[2])
       
        # st.write("Prediction: ", y[1])
        # st.write("Confidence: ", y[2])

        # Create two columns with equal width
        col1, col2 = st.columns(2)
        
        # In the first column, add a header and some content
        with col1:
            st.header("Prediction")
            st.write(y[1])
        
        # In the second column, add a header and some content
        with col2:
            st.header("Confidence")
            st.write(y[2])


