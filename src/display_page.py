import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import utils_v2
from model_utils import *

import tifffile as tiff
import tensorflow as tf
# import numpy as np

# Loading the images & masks as an array

def preprocess_image(image_arr, num_bands=12):
     # Image preprocessing
    image_arr = image_arr.astype('float32')
    min_vals = tf.reduce_min(image_arr, axis=(0, 1), keepdims=True) # image_arr shape is (256, 256, num_bands)
    max_vals = tf.reduce_max(image_arr, axis=(0, 1), keepdims=True)
    image_arr_normalized = tf.divide(tf.subtract(image_arr, min_vals), tf.subtract(max_vals, min_vals)+tf.constant(1e-3, dtype=tf.float32))
    # Setting shapes of images & masks
    image_arr_normalized.set_shape([256, 256, num_bands])
    image_arr_normalized = np.expand_dims(image_arr_normalized, axis=0)  # expand dimension for batch size
    return image_arr_normalized
    
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


