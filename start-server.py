from flask import Flask, request, jsonify, redirect, url_for, abort
from flask_restful import Resource, Api
from json import dumps
from dejavu import Dejavu
from dejavu.recognize import FileRecognizer
from werkzeug.utils import secure_filename
import os
import base64
import json
import traceback

app = Flask(__name__)
api = Api(app)
print("kappa")
global uid
uid = 0
print("keepo")
print(uid)

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
        global uid
        data = request.get_json()
        b64_string = data['file']
        extension = data['extension']
    except:
        abort(400)
    try:
        filename = "file-" + str(uid) + "." + extension
        print(filename)

        original = base64.decodestring(b64_string)
        with open(os.path.join(UPLOAD_FOLDER, filename), 'wb') as f:
            f.write(original)
            
        djv = Dejavu(config)
        song = djv.recognize(FileRecognizer, os.path.join(UPLOAD_FOLDER, filename))
        uid += 1
    except:
        traceback.print_exc()
        abort(500)

        #os.remove(os.path.join(UPLOAD_FOLDER, filename))
    print(song)
    if (song['confidence'] < 0.5 and song['matches'] < 10) or song['matches'] < 4:
        abort(404)
    else:
        return jsonify(song)

@app.route('/fingerprint', methods=['POST'])
def upload_file():
    try:
        data = request.get_json()
        print('a')
        print(data['extension'])
        print('b')
        #print(data)
        b64_string = data['file']
        extension = data['extension']
    except:
        abort(400)
    try:
        filename = "file." + extension

        original = base64.decodestring(b64_string)
        with open(os.path.join(UPLOAD_FOLDER, filename), 'wb') as f:
            f.write(original)
        
        djv = Dejavu(config)
        djv.fingerprint_file(os.path.join(UPLOAD_FOLDER, filename), song_name=data['song_name'], song_artist=data['song_artist'])

        os.remove(os.path.join(UPLOAD_FOLDER, filename))

        return jsonify({'message': 'success'})
    except:
        abort(500)
    

@app.route('/songs', methods=['GET'])
def get_songs():
    djv = Dejavu(config)
    songs = djv.get_song_list()
    print(songs)
    return jsonify(list(songs))

@app.route('/songs-detailed', methods=['GET'])
def get_songs_detailed():
    djv = Dejavu(config)
    songs = djv.get_songs_detailed()
    return jsonify(list(songs))

@app.route('/delete-song', methods=['POST'])
def delete_song():
    try:
        data = request.get_json()
        song_id = data['song_id']
    except:
        abort(400)
    try:
        djv = Dejavu(config)
        print('calling dejavu.delete_song')
        djv.delete_song(song_id)

        return jsonify({'message': 'success'})
    except:
        abort(500)

uid = 0
app.run(host='0.0.0.0', port='80')


