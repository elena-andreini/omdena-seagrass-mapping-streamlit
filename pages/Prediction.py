import os
import tifffile
import numpy as np
import streamlit as st
import tensorflow as tf
import matplotlib.pyplot as plt
from model_utils.utils import total_loss, swm_land_mask, preprocess_image_mask


@st.cache_resource
def retreive_model(model_path):
    model = tf.keras.models.load_model(model_path, custom_objects = {"total_loss": total_loss})
    return model

def prediction(model,image,class_names):
    image = np.expand_dims(image, axis=0)
    predicted_probs = model.predict(image)
    predicted_probs = np.squeeze(predicted_probs)
    predicted_mask = np.argmax(predicted_probs, axis=-1)
    return predicted_mask

def display_class_confidence(y_pred, class_names):
    num_classes = len(class_names)
    _, pixel_counts = np.unique(y_pred, return_counts=True) 

    st.write("**Proportions of each class:**")
    for class_idx, class_name in enumerate(class_names):
        confidence_score = (pixel_counts[class_idx] / y_pred.size)* 100
        confidence_score = "{:.2f}%".format(confidence_score)
        st.info(f"Proportion of {class_name}: {confidence_score}")

def main():
    st.title("Detecting the seagrass presence")
    st.markdown("This app is for prediction of seagrass in the mediterranean sea.")
    
    image_file = st.file_uploader("Drop the picture of the location", type = ['tif'])

    class_names = ['seagrass','water','land']
    
    model = retreive_model('./saved_models/unet_summer_images_augmented_wcc_final.h5')

    if image_file is not None:
        with open("temp.tif", "wb") as f:
            f.write(image_file.read())

        # Read the TIFF image from the saved file
        col1, col2 = st.columns(2)
        image = tifffile.imread("temp.tif")

        # Min-Max Scaling the image to bring pixel values between 0-1 for RGB channels only specifically for visualization
        rgb_image = image[:, :, [3, 2, 1]]
        img_array = np.divide(rgb_image - rgb_image.min(), rgb_image.max() - rgb_image.min())

        with col1:
            st.subheader('Original Image')
            st.image(img_array, use_column_width=True)

        st.sidebar.markdown("Click on the predict button below to predict the mask of the image.")
        button = st.sidebar.button("Predict")

        if button:
            mask_arr = swm_land_mask(image, threshold=0.9)
            image = preprocess_image_mask(image, mask_arr)
            predicted_mask = prediction(model, image, class_names)
            cmap = plt.colormaps.get_cmap('viridis')
            colored_mask = cmap(predicted_mask/2)
            colored_mask = (colored_mask * 255).astype(np.uint8)

            # Display masked image in Streamlit
            with col2:
                st.subheader('Predicted Mask')
                st.image(colored_mask, use_column_width=True)

            st.write("The purple color in the mask is the seagrass, blue color is the water and yellow color is the land.")
            display_class_confidence(predicted_mask, class_names)
            
        os.remove("temp.tif")
    

if __name__=="__main__":
    main()


