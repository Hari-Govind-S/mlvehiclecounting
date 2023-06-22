from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from ImageProcessor import *

app = Flask(__name__)
CORS(app)


statustxt = 'Successfully Loaded Server'

@app.route("/status")
def status():
    return {"Status": statustxt}

@app.route("/downloadfile")
def downloadfile():
    path = "output.avi";
    return send_file(path, as_attachment=True)

@app.route("/convert", methods=['POST'])
def convert():
    statustxt = 'Server is processing the file'
    filename = request.json['filename']
    model = request.json['model']
    print(model)
    out = Processor(filename,model)
    statustxt = 'Server is free'
    if(out == 1):
        resp = jsonify({"message":'Success'})
        return resp
    else:
        resp = jsonify({"message":'Error'})
        return resp

@app.route("/upload", methods=['POST'])
def upload():
    statustxt = 'Uploading File'
    file = request.files['file']
    file.save(f'uploads/{file.filename}')
    resp = jsonify({"message":'Success'})
    statustxt = 'Server is free'
    return resp

if __name__== "__main__":
    app.run(debug=True)