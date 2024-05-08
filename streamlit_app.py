import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import utils_v2
# from env import *
from model_utils import *
from display_page import dp_main

########
from streamlit_extras.let_it_rain import rain
from streamlit_extras.colored_header import colored_header
# from page_utils import font_modifier, display_image

########

def display_image(url, caption=None):
    st.markdown("<p></p>",unsafe_allow_html=True)
    image_url = url
    st.image(image_url, caption=caption, use_column_width=True)
    st.markdown("<p></p>",unsafe_allow_html=True)

########
def homepage():
    # st.title("Home Page")
    # st.write("Welcome to the home page!")
    ################### HEADER SECTION #######################
    display_image('https://cdn-images-1.medium.com/max/800/0*vBDO0wwrvAIS5e1D.png')
    
    st.markdown("<h1 style='text-align: center; color: #F5EFE6;'>Mapping Seagrass Meadows with Satellite Imagery and Computer Vision</h1>",
                unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: #FFFFD0; font-family: Segoe UI;'>A web-based pixel-level Classification Model for identifying seagrass in sattelite images</h3>", unsafe_allow_html=True)
    
    display_image('https://upload.wikimedia.org/wikipedia/commons/4/45/Sanc0209_-_Flickr_-_NOAA_Photo_Library.jpg')

def about():
    st.title("About Page")
    st.write("This is the about page.")
def contact():
    # st.title("Contact Page")
    # st.write("Contact us at example@example.com")
    img_file = st.file_uploader("Choose an image to classify", type=["tif"])
    dp_main(img_file)
# Create a dictionary to map page names to their respective functions
pages = {
    "Home": homepage,
    "About": about,
    "Classify Image": contact
}
# Create a sidebar with page selection
page_selection = st.sidebar.radio("Go to", list(pages.keys()))
# Run the selected page function
pages[page_selection]()


################### HEADER SECTION #######################
# display_image('https://cdn-images-1.medium.com/max/800/0*vBDO0wwrvAIS5e1D.png')

# st.markdown("<h1 style='text-align: center; color: #F5EFE6;'>Mapping Seagrass Meadows with Satellite Imagery and Computer Vision</h1>",
            #unsafe_allow_html=True)
# st.markdown("<h4 style='text-align: center; color: #FFFFD0; font-family: Segoe UI;'>A web-based pixel-level Classification Model for identifying seagrass in sattelite images</h3>", unsafe_allow_html=True)

# display_image('https://upload.wikimedia.org/wikipedia/commons/4/45/Sanc0209_-_Flickr_-_NOAA_Photo_Library.jpg')


################### FILE UPLOAD SECTION #######################
# uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])



########
# st.markdown("<h4 style='text-align: center; font-family: Segoe UI;'>A web-based pixel-level Classification Model for identifying seagrass in sattelite images</h1>", unsafe_allow_html=True)
# st.title("Mapping seagrass with Satellite Imagery, Deep Learning and Computer Vision")
# st.write("Choose an image to classify")
    

#######

# make_font_poppins()
########

#########
# import os
# import sys
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


