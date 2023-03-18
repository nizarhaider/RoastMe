from flask import Flask, render_template, request, jsonify
# from google.cloud import storage
import io
import pandas as pd
from model import find_closest_match 
import numpy as np
import os
import shutil
import ast
import json
import imghdr

app = Flask(__name__)
app.debug=True

# # Load data
# client = storage.Client()
# bucket = client.get_bucket("roastbucket")
# blob = bucket.get_blob("data_with_embeddings.csv")
# data = blob.download_as_string()
# df = pd.read_csv(io.StringIO(data.decode('utf-8')))

@app.route('/')
def index():

    basedir = os.path.abspath(os.path.dirname(__file__))
    folder = os.path.join(basedir, "static", "images")
    if os.path.exists(folder):
        shutil.rmtree(folder)
    os.mkdir(folder)

    return render_template('index.html')

@app.route('/landing')
def home():

    return render_template('landing_page.html')

@app.route('/', methods=['POST'])
def handle_form(): 
    basedir = os.path.abspath(os.path.dirname(__file__))

    df= pd.read_csv('combined.csv')
    df["embeddings"] = df["embeddings"].apply(lambda x: np.array(list(map(float, x.replace("[", "").replace("]", "").split()))))
    base_image =  os.path.join("static", "images")
    if 'image' not in request.files:
        return jsonify({'fun_pass': 'No image file found in the request'})
    image_file = request.files['image']
    if image_file.filename == '':
        return jsonify({'fun_pass': 'No image file selected'})
    image_file.save(os.path.join(base_image, image_file.filename))

    # image = request.files.get('image')
    user_img_path = os.path.join(base_image, image_file.filename)
    if imghdr.what(user_img_path) == None:
        return jsonify({"fun_pass": "Invalid image type. I only support png, jpg or jpeg at the moment :/ "})

    fun_pass,result = find_closest_match(df,user_img_path)
    
    if fun_pass != "True":
        # print(fun_pass)
        print("it didn't :()")
        return jsonify({"fun_pass": fun_pass})
    else:
        # print(fun_pass) 

        comments, match_img = result
        comments = ast.literal_eval(comments)
        match_img.save(os.path.join(base_image, "match.jpg"))
        match_img_path = os.path.join(base_image, "match.jpg")
        # user_img_path = os.path.join('static/images', "user.jpg")
        comments=json.dumps(comments)
        response = {'comments': comments, 'match_img': match_img_path, 'user_img': user_img_path, "fun_pass": fun_pass}
        print(fun_pass)
        return jsonify(response)
        
if __name__ == '__main__':
    app.run()
