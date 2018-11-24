from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory, jsonify, Response
from werkzeug.utils import secure_filename
from flask_cors import CORS
import datetime
import seg
import os
from PIL import Image

UPLOAD_FOLDER = 'static'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__, static_url_path='', static_folder='static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'milad and sadaf are the best founders, it would be so wonderful to work with them'
CORS(app)


@app.route('/', methods=['GET', 'POST'])
def serverAngular():
    return app.send_static_file('index.html')


@app.route('/getOriginalFile')
def getOriginalFile():
    originalPath = 'img.png'
    return jsonify(path=originalPath)


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    # check if the post request has the file part
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    # if user does not select file, browser also
    # submit a empty part without filename
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        temp = Image.open(file)
        file = temp.resize((256, 256))

        filename = secure_filename('img.png')
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return Response('Success', status=200)


@app.route('/uploadMask', methods=['GET', 'POST'])
def upload_mask():
    # check if the post request has the file part
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    print(file.filename)
    # if user does not select file, browser also
    # submit a empty part without filename
    if file.filename == '':
        return redirect(request.url)
    if file:
        temp = Image.open(file)
        file = temp.resize((256, 256))

        filename = secure_filename('mask.png')
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return Response('Success', status=200)


@app.route('/getSegmentedFileWithThresh/<threshold>')
def getSegmentedFileWithThresh(threshold):
    threshold = int(threshold)
    maskPath = seg.segment_image('static/img.png', threshold)
    return jsonify(path=maskPath)


@app.route('/getSegmentedFileWithThreshAndMask/<threshold>')
def getSegmentedFileWithThreshAndMask(threshold):
    threshold = int(threshold)
    maskPath = seg.segment_image_with_mask(
        'static/img.png', 'static/mask.png', threshold)
    return jsonify(path=maskPath)


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.run(debug=True, threaded=True)
