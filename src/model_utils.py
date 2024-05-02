import tifffile as tiff
import tensorflow as tf
import numpy as np

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
    