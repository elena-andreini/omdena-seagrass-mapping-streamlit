import streamlit as st
import matplotlib.pyplot as plt
import numpy as np


import tifffile as tiff
import tensorflow as tf
# import numpy as np

# Loading the images & masks as an array
def load_image(image_path, band_idxs=range(12)):
    print(f'image path {image_path}')
    img_arr = tiff.imread(image_path)[:, :, band_idxs]
    print(f'image {image_path} loaded')
    return img_arr
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

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ["SM_FRAMEWORK"] = "tf.keras"
from tensorflow import keras
import segmentation_models as sm
import mlflow
from mlflow.tracking import MlflowClient
# from env import *
# import streamlit as st

@keras.saving.register_keras_serializable(package="my_package", name="dice_loss_plus_2focal_loss")
def dice_loss_plus_2focal_loss(y_true, y_pred):
    # Compute dice loss
    dice_loss = sm.losses.DiceLoss(class_weights=weights)(y_true, y_pred)

    # Compute focal loss
    focal_loss = sm.losses.CategoricalFocalLoss()(y_true, y_pred)

    # Combine dice loss and focal loss with a weighting factor
    total_loss = dice_loss + (2 * focal_loss)

    return total_loss

@st.cache_resource
def retrieve_model():
    client = MlflowClient()
    ##### Direct injection of values instead of using environment VALES
    MLFLOW_TRACKING_URI = 'https://dagshub.com/Omdena/TriesteItalyChapter_MappingSeagrassMeadows.mlflow'
    RUN_ID = '42909ca2a5ef4a4c94e5fe030380e5e8'
    #####
  #  MLFLOW_TRACKING_URI = os.getenv('MLFLOW_TRACKING_URI')
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    # RUN_ID = os.getenv('best_model_run_id')
    print(f'retrieving the model with run_id {RUN_ID}')
    custom_objects = {"dice_loss_plus_2focal_loss": dice_loss_plus_2focal_loss}
    with keras.saving.custom_object_scope(custom_objects):
        model = mlflow.pyfunc.load_model("runs:/" + RUN_ID + "/model")
    print(f'model with run_id {RUN_ID} retrieved')
    return model
#########

# Streamlit app
def dp_main(image_file):
    model = retrieve_model()
    
    # st.title("Mapping seagrass with Satellite Imagery and Deep Learning")
    # st.write("Choose an image to classify")
    
    # Choose an image file in the sidebar
    # image_file = st.sidebar.file_uploader("Choose an image file", type=["tif"])
    
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
        return fig
        # Make a prediction and display it
        #prediction = predict(load_image(image_file))
        #st.write("Prediction: ", prediction[1])
        #st.write("Confidence: ", prediction[2])

# Choose an image file in the sidebar
img_file = st.sidebar.file_uploader("Choose an image file", type=["tif"])
fg = dp_main(img_file)
pyplot(fg)
