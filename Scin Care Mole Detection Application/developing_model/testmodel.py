from tensorflow import keras
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.preprocessing import image
from keras.models import load_model
import numpy as np


def load_image(filename):
    # load the image
    img = load_img(filename, target_size=(200, 200))
    # convert to array
    img = img_to_array(img)
    # reshape into a single sample with 3 channels
    img = img.reshape(1, 200, 200, 3)
    # center pixel data
    img = img.astype('float32')
    img = img - [123.68, 116.779, 103.939]
    return img

# load an image and predict the class
def predict(filename):
    # load the image
    img = load_image(filename)
    # load model
    model = load_model('second_model.h5')
    # predict the class
    result = model.predict(img)
    result = result[0][0]
     
    return result
    


print(predict('dataset/skin cancer/SET_E/E990.BMP'))