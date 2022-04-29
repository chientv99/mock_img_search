from datetime import datetime

from flask import Flask, jsonify, render_template, request, send_from_directory
from PIL import Image
from flask_cors import CORS

from image_search import (autofaiss_img_search, image_paths_to_product_list)
from mongo import get_database

app = Flask(__name__)
CORS(app)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']

        # Save query image
        img = Image.open(file.stream)  # PIL image
        uploaded_img_path = "static/uploaded/" + datetime.now().isoformat().replace(":", ".") + "_" + file.filename
        img.save(uploaded_img_path)

        # Run search
        scores = autofaiss_img_search(uploaded_img_path)
        images = image_paths_to_product_list(ret)

        return jsonify({
            "product": scores,
        })
    else:
        return 0

db = get_database()

@app.route('/search', methods=["POST"])
def search():
    file = request.files['file']
    model_name = request.form['model_name']
    
    # Save query image
    img = Image.open(file.stream)  # PIL image
    uploaded_img_path = "static/uploaded/" + datetime.now().isoformat().replace(":", ".") + "_" + file.filename
    img = img.convert('RGB')
    img.save(uploaded_img_path)

    products = []


    # start time
    start_time = datetime.now()
    if model_name == 'autofaiss':
        ret = autofaiss_img_search(uploaded_img_path)
    return jsonify({
        "products": ret,
        "elapsed_time": elapsed_time.microseconds / 1000
    })

@app.route('/images/<path:path>')
def image(path):
    return send_from_directory('images', path)

if __name__=="__main__":
    app.run("0.0.0.0", debug=False)
