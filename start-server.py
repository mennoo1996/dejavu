from flask import Flask, request, jsonify, redirect, url_for, abort
from flask_restful import Resource, Api
from json import dumps
from dejavu import Dejavu
from dejavu.recognize import FileRecognizer
from werkzeug.utils import secure_filename
import os
import base64
import json

app = Flask(__name__)
api = Api(app)

UPLOAD_FOLDER = './uploaded_files'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

ALLOWED_EXTENSIONS = set(['wav', 'mp3'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

with open('dejavu.cnf.SAMPLE') as f:
    config = json.load(f)



def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/test', methods=['GET', 'POST'])
def test():
    print(request.form)
    print(request.data)
    print(request.get_json())
    if request.method == 'POST':
        return jsonify({'message': request.get_json()['test']})
    else:
        return jsonify({'message': 'server is online'})


@app.route('/recognize', methods=['POST'])
def recognize():
    try:
        data = request.get_json()
        b64_string = data['file']
        extension = data['extension']

        filename = "file." + extension

        original = base64.decodestring(b64_string)
        with open(os.path.join(UPLOAD_FOLDER, filename), 'wb') as f:
            f.write(original)
            
        djv = Dejavu(config)
        song = djv.recognize(FileRecognizer, os.path.join(UPLOAD_FOLDER, filename))
        
        os.remove(os.path.join(UPLOAD_FOLDER, filename))
        return jsonify(song)
    except:
        return jsonify({'message': 'error'})

@app.route('/fingerprint', methods=['POST'])
def upload_file():
    try:
        data = request.get_json()
        b64_string = data['file']
        extension = data['extension']
        filename = "file." + extension

        original = base64.decodestring(b64_string)
        with open(os.path.join(UPLOAD_FOLDER, filename), 'wb') as f:
            f.write(original)
        
        djv = Dejavu(config)
        djv.fingerprint_file(os.path.join(UPLOAD_FOLDER, filename), song_name=data['song_name'])

        os.remove(os.path.join(UPLOAD_FOLDER, filename))

        return jsonify({'message': 'success'})
    except:
        return jsonify({'message': 'error'})
    

@app.route('/songs', methods=['GET'])
def get_songs():
    djv = Dejavu(config)
    songs = djv.get_song_list()
    print(songs)
    return jsonify(list(songs))

app.run(host='0.0.0.0', port='80')
