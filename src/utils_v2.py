import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ["SM_FRAMEWORK"] = "tf.keras"
from tensorflow import keras
import segmentation_models as sm
import mlflow
from mlflow.tracking import MlflowClient
from env import *
import streamlit as st

@keras.saving.register_keras_serializable(package="my_package", name="dice_loss_plus_2focal_loss")
def dice_loss_plus_2focal_loss(y_true, y_pred):
    # Compute dice loss
    dice_loss = sm.losses.DiceLoss(class_weights=weights)(y_true, y_pred)

    # Compute focal loss
    focal_loss = sm.losses.CategoricalFocalLoss()(y_true, y_pred)

    # Combine dice loss and focal loss with a weighting factor
    total_loss = dice_loss + (2 * focal_loss)

    return total_loss


#set_secrets()
get_model_info()



@st.cache_resource
def retrieve_model():
    client = MlflowClient()
    MLFLOW_TRACKING_URI = os.getenv('MLFLOW_TRACKING_URI')
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    RUN_ID = os.getenv('best_model_run_id')
    print(f'retrieving the model with run_id {RUN_ID}')
    custom_objects = {"dice_loss_plus_2focal_loss": dice_loss_plus_2focal_loss}
    with keras.saving.custom_object_scope(custom_objects):
        model = mlflow.pyfunc.load_model("runs:/" + RUN_ID + "/model")
    print(f'model with run_id {RUN_ID} retrieved')
    return model

    
