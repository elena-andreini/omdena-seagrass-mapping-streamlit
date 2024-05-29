import cv2
import keras
import numpy as np
from scipy import stats
import tensorflow.keras.backend as K

# Loss function definitions
@keras.saving.register_keras_serializable()
def focal_tversky_loss(y_true, y_pred, alpha=0.7, gamma=3, smooth=1e-5):
    # Calculations are applied along batch_size, img_height, img_width
    axes = [0, 1, 2]
    tp = K.sum(y_true * y_pred, axis=axes)
    fn = K.sum(y_true, axis=axes) - tp
    fp = K.sum(y_pred, axis=axes) - tp
    tversky = (tp + smooth)/(tp + alpha*fn + (1-alpha)*fp + smooth)
    tversky_avg = K.mean(tversky)
    return K.pow((1-tversky_avg), gamma)

@keras.saving.register_keras_serializable()
def dice_score(y_true, y_pred, class_weights=None, smooth=1e-5):
    # Calculations are applied along batch_size, img_height, img_width
    axes = [0, 1, 2]
    intersection = K.sum(y_true * y_pred, axis=axes)
    dice = (2. * intersection + smooth) / (K.sum(y_true, axis=axes) + K.sum(y_pred, axis=axes) + smooth)
    if class_weights is not None:
        dice_avg = K.mean(dice * class_weights)
    else:
        dice_avg = K.mean(dice)
    return dice_avg

@keras.saving.register_keras_serializable()
def total_loss(y_true, y_pred):
    ft_loss = focal_tversky_loss(y_true, y_pred, alpha=0.7, gamma=3, smooth=1e-5)
    dice_loss = 1 - dice_score(y_true, y_pred, class_weights=None,smooth=1e-5)
    return dice_loss + (2 * ft_loss)

# Image pre-processing functions
# Helps remove sun glint from images
def deglint_image(image_arr, mask_arr):
    deglinted_img = np.zeros(image_arr.shape)
    for i in range(7):
        band_i = image_arr[:, :, i]
        nir_band = image_arr[:, :, 7]
        slope, y_inter, r_val, p_val, std_err = stats.linregress(x=nir_band.ravel(), y=band_i.ravel())
    
        water_mask = (mask_arr==1)
        deglinted_img[:, :, i][water_mask] = band_i[water_mask] - (slope*(nir_band[water_mask] - nir_band[water_mask].min()))
        deglinted_img[:, :, i] = cv2.medianBlur(deglinted_img[:, :, i].astype('float32'), 3)
        deglinted_img[:, :, i][~water_mask] = band_i[~water_mask]
        deglinted_img[:, :, i] = np.where(deglinted_img[:, :, i] < 0, 0, deglinted_img[:, :, i])
    deglinted_img[:, :, 7:] = image_arr[:, :, 7:]
    return deglinted_img

# Helps calculate Depth invariant index between 2 bands using Lyzenga method 
def calculate_dii(band_1, band_2, mask_arr):
    band_1_transformed = np.log(band_1 + 1)
    band_2_transformed = np.log(band_2 + 1)
    water_mask = (mask_arr==1)
    dii = np.zeros(band_1.shape)
    
    cov_matrix = np.cov(band_1_transformed[water_mask].ravel(), band_2_transformed[water_mask].ravel())
    a = (cov_matrix[0, 0] - cov_matrix[1, 1]) / (cov_matrix[0, 1])
    att_coef_ratio = a + np.sqrt(a**2 + 1)
    
    dii[water_mask] = band_1_transformed[water_mask] - (att_coef_ratio * band_2_transformed[water_mask])
    dii[~water_mask] = (band_1_transformed[~water_mask] + band_2_transformed[~water_mask])/2
    return dii

# Helps mask out land for pre-processing
def swm_land_mask(img_arr, threshold):
    swm = (img_arr[:, :, 1] + img_arr[:, :, 2]) / (img_arr[:, :, 7] + img_arr[:, :, 11] + 1e-3)
    mask = swm > threshold
    mask_arr = cv2.medianBlur(mask.astype('float32'), 3)
    return mask_arr

def preprocess_image_mask(image_arr, mask_arr):
    # Deglint the image (bands 1-6 using band 8 as reference)
    deglinted_image = deglint_image(image_arr, mask_arr)

    # Apply water column correction 
    dii_b2_b3 = calculate_dii(deglinted_image[:, :, 1], deglinted_image[:, :, 2], mask_arr)
    image_arr_final = np.dstack((deglinted_image, dii_b2_b3))

    # Image preprocessing
    min_vals = image_arr_final.min(axis=(0, 1), keepdims=True) # image_arr shape is (256, 256, num_bands)
    max_vals = image_arr_final.max(axis=(0, 1), keepdims=True)
    image_arr_normalized = (image_arr_final - min_vals) / (max_vals - min_vals + 1e-3)

    return image_arr_normalized.astype('float32')