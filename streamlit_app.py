import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import utils_v2
from model_utils import *
# Streamlit app
def main():
    model = utils_v2.retrieve_model()
    
    st.title("Mapping seagrass with Satellite Imagery and Deep Learning")
    st.write("Choose an image to classify")
    
    # Choose an image file in the sidebar
    image_file = st.sidebar.file_uploader("Choose an image file", type=["tif"])
    
    if image_file is not None:
        # Display the chosen image
        image = load_image(image_file)
        X = preprocess_image(image)
        y = model.predict(X)
        y = np.squeeze(y, axis=0)
        #st.image(image, caption="Chosen Image", use_column_width=True)
        # Create a plot
        plt.axis('off')
        fig, (ax1, ax2) = plt.subplots(1, 2)
        ax1.imshow(image[:, :, 3])
        ax2.imshow(y)
        # Display the image in streamlit
        st.pyplot(fig)
        # Make a prediction and display it
        #prediction = predict(load_image(image_file))
        #st.write("Prediction: ", prediction[1])
        #st.write("Confidence: ", prediction[2])


if __name__ == "__main__":
    main()