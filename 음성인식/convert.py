import os

from flask import Flask, jsonify
from flask import request
from pydub import AudioSegment
from datetime import datetime

app = Flask(__name__)

@app.route("/convert", methods=['POST'])
def convert():
    data = request.json
    print(data)
    inputFile = data['filePath']
    print(inputFile)

    if inputFile.find(".wav") > 0:
        date = datetime.today().strftime("%Y-%m-%d_%H-%M-%S")
        print(date)
        if os.path.isfile(inputFile):
            sound = AudioSegment.from_wav(inputFile)
            sound.set_channels(2)
            outputFile = "C:\\Users\\User\\Desktop\\ChangeSound\\" + date + ".flac"
            print(outputFile)
            sound.export(outputFile, format="flac")

    elif inputFile.find(".mp3") > 0:
        date = datetime.today().strftime("%Y-%m-%d_%H-%M-%S")
        print(date)
        print(type(date))
        if os.path.isfile(inputFile):
            sound = AudioSegment.from_mp3(inputFile)
            sound.set_channels(2)
            outputFile = "C:\\Users\\User\\Desktop\\ChangeSound\\" + date + ".flac"
            print(outputFile)
            sound.export(outputFile, format="flac")

    data['filePath'] = outputFile
    print(data['filePath'])
    return jsonify(data)
