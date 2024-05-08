import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import utils_v2
from model_utils import *



# Streamlit app
def main(image_file):
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


