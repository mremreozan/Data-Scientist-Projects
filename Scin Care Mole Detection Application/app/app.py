# coding=utf-8
import os
import numpy as np

# Keras
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
#from gevent.pywsgi import WSGIServer
import logging
from flask_cors import CORS  # The typical way to import flask-cors

UPLOAD_FOLDER = 'uploads'

# Define a flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
port = int(os.environ.get("PORT", 5000))
logging.basicConfig(level=logging.INFO)
CORS(app, resources=r'/*', allow_headers='Content-Type')

# Load your trained model
model = tf.keras.models.load_model('models/second_model.h5')

@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            app.config['UPLOAD_FOLDER'], secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        return model_predict(file_path, model)
    return None

def model_predict(img_path, model):

    img = image.load_img(img_path, target_size=(200, 200))
    img = image.img_to_array(img)
    img = img.reshape(1, 200, 200, 3)
    img = img.astype('float32')
    img = img - [123.68, 116.779, 103.939]
    result = model.predict(img)
    result = result[0][0]

    if result == 0.0:
        return "Don't worry, it is not serious, this patient doesn't need to see a doctor!"
    else:
        return "This patient need to see a doctor!"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=port)