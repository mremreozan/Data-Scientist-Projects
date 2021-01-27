from flask import Flask, render_template, flash, request, redirect, url_for, jsonify
import logging
from flask_cors import CORS  # The typical way to import flask-cors
from preprocessing import preprocess
from predict import predict
import pandas as pd
import os
import pickle

app = Flask("__name__")
port = int(os.environ.get("PORT", 5000))
logging.basicConfig(level=logging.INFO)
#cors = CORS(app, resources={r"/*": {"origins": "*"}})
CORS(app, resources=r'/*', allow_headers='Content-Type')

@app.route('/', methods=["GET"])
#@cross_origin(allow_headers=['Content-Type'])
def index():
    if request.method == "GET":
        return "Alive"
    else:
        return "Server not working"

@app.route('/predict', methods=["POST", "GET"])
def predict_page():
    if request.method == 'POST':

        response = {}
        json_file = request.json
        
        # Now, we call json data with process function and then we pass it through our model.
        cleaned_json_df = preprocess(json_file)

        if type(cleaned_json_df)==str:
            response["error"] = cleaned_json_df
            return jsonify(response)

        model = pickle.load(open('model/models/model.pkl','rb'))
        y_pred_new = predict(cleaned_json_df, model) 
        y_pred_new = y_pred_new.tolist()
        response["prediction"] = y_pred_new

        return jsonify(response)
    
    elif request.method == 'GET':
        return """<xmp>
            Here is the data format for the POST request:
            {
                "data": {
                        "area": int,
                        "property-type": "APARTMENT" | "HOUSE" | "OTHERS",
                        "rooms-number": int,
                        "zip-code": int,
                        "land-area": Optional[int],
                        "garden": Optional[bool],
                        "garden-area": Optional[int],
                        "equipped-kitchen": Optional[bool],
                        "full-address": Optional[str],
                        "swimmingpool": Opional[bool],
                        "furnished": Opional[bool],
                        "open-fire": Optional[bool],
                        "terrace": Optional[bool],
                        "terrace-area": Optional[int],
                        "facades-number": Optional[int],
                        "building-state": Optional["NEW" | "GOOD" | "TO RENOVATE" | "JUST RENOVATED" | "TO REBUILD"]
                }
            }
            </xmp>"""
    

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=port)
