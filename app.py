from flask import Flask, jsonify, app
from flask import request

from 형태소분석.app import morpAPI2, morpAPI


@app.route("/cosmos/KStars/morp", methods=['POST'])
def cosmos_morp():
    data = request.json
    print(data)
    hi = morpAPI2(data['text'])
    moreResult = hi.showMorp2()

    data['analysisResult'] = moreResult
    print(type(data['analysisResult']))
    print(data['analysisResult'])
    return jsonify(data)

@app.route("/cosmos/KStars/morpList", methods=['POST'])
def cosmos_morp_board():
    data = request.json
    for i in range(len(data)):
        analysis = morpAPI2(data[i]['text'])
        resultList = analysis.showMorp2()
        data[i]['analysisResult'] = resultList

    return jsonify(data)


@app.route("/test", methods=['POST'])
def test():
    data = request.json
    # print(data)
    hi = morpAPI(data['text'])
    moreResult = hi.showMorp()

    # print(moreResult)
    data['analysisResult'] = moreResult

    return jsonify(data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)