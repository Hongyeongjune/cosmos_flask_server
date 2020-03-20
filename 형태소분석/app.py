from flask import Flask , jsonify
from flask import request
from pydub import AudioSegment
from datetime import datetime

import urllib3
import re
import json
from collections import OrderedDict
from pprint import pprint

answer = ''
jsonString = OrderedDict()
analysis_data = ""

class morpAPI2:
    openApiURL = "http://aiopen.etri.re.kr:8000/WiseNLU"
    accessKey = "9cf5e5b7-55b3-4369-9921-726d59b3b6e5"
    analysisCode = "morp"  # 개체명 분석 코드
    text = "기본"  # 분석할 대상
    data = ""  # api를 통해서 받은 분석결과 json
    result = ""  # data를 리스트로 변환한 분석결과변수-변수이름 고치기
    k = 0

    def __init__(self, userFile):

        self.text = self.setText(userFile)
        print(type(self.text))
        print("현재분석코드 " + self.analysisCode)
        print("현재분석문장 " + self.text)
        self.data = self.setData()
        self.result = self.result(self.data)

    '''
    사용자가 분석할 텍스트 파일 저장
    '''

    def setText(self, userFile):

        '''
        myFile = open(userFile, "r", encoding="utf-8")
        self.text = myFile.read()
        return self.text
        '''
        # '''
        self.text = userFile
        return self.text
        # '''

    '''
    api로부터 json 값을 가져오기
    '''

    def setData(self):
        requestJson = {
            "access_key": self.accessKey,
            "argument": {
                "text": self.text,
                "analysis_code": self.analysisCode
            }
        }

        http = urllib3.PoolManager()

        response = http.request(
            "POST",
            self.openApiURL,
            headers={"Content-Type": "application/json; charset=UTF-8"},
            body=json.dumps(requestJson)  # json파일로 api를 받음
        )

        self.data = str(response.data, "utf-8")
        return self.data

    '''
    josn데이터에서 필요한 데이터값 가져오기
    '''

    def result(self, data):
        test = json.loads(data)
        self.result = test['return_object']['sentence']
        return self.result

    '''
    형태소 분석부분
    '''

    def showMorp2(self, analysis_data=dict()):
        test = ''
        print("형태소분석결과 ")
        strnum = len(self.result)  # 총문장갯수
        print(strnum)
        morpnum = len(self.result[0]['morp'])  # 하나의 문장당 형태소 갯수
        print(morpnum)

        wordnum = len(self.result[0]['word'])  # 하나의 문장단 단어 갯수
        print(wordnum)

        analysis_data['key'] = list()
        analysis_data['value'] = list()

        with open('morpAPI.txt', 'w', encoding="utf-8") as make_file:
            for i in range(strnum):
                for j in range(morpnum - 1):
                    str = ''

                    # str = self.result[i]['morp'][j]['lemma'] + ":" + self.result[i]['morp'][j]['type']

                    analysis_data['key'].append(self.result[i]['morp'][j]['lemma'])
                    analysis_data['value'].append(self.result[i]['morp'][j]['type'])
                    jsonString = json.dumps(analysis_data, ensure_ascii=False, indent=4)

                    if self.result[i]['morp'][j]['position'] - self.result[i]['morp'][j - 1]['position'] == 4:

                        print("  ", end="")
                        # answer += "  "
                        print(str, end="")
                        # answer += str

                    else:
                        # str=str.replace("\"\"",)
                        print(str, end="")
                        # answer += str

                    json.dump(str, make_file, ensure_ascii=False, indent=4)

        myFile = open("/home/ubuntu/virtual_cosmos/cosmos_flask_server/형태소분석/morpAPI.txt", "r", encoding="utf-8")
        # myFile = open("C:\\Users\\User\\PycharmProjects\\Cosmos\\형태소분석\\morpAPI.txt", "r", encoding="utf-8")

        text = myFile.readline()
        print("\n")
        print(type(test))
        print("\n")
        print(test)
        '''
        if self.text==" + ":
            self.text=self.text.replace("  + "," aa")
        else :
            self.text=self.text.replace("\"","")
            print(self.text)

       # print(self.text)
        self.text=self.text.replace("\"","")
        self.setOutput(self.text)

        '''
        text = text.replace("\"\"", " / ")

        text = text.replace("\"\"", " /")
        text = text.replace("\"", "")

        print("\n")
        print(type(text))
        print(text)
        print("\n")

        # print(text)
        self.setOutput(text)

        # print(answer)
        # return answer

        return jsonString



        # return jsonString

    def setOutput(self, str):
        with open('morpAPI.txt', 'w', encoding="utf-8") as make_file:
            json.dump(str, make_file, ensure_ascii=False, indent=4)

class morpAPI:
    openApiURL = "http://aiopen.etri.re.kr:8000/WiseNLU"
    accessKey = "9cf5e5b7-55b3-4369-9921-726d59b3b6e5"
    analysisCode = "morp"  # 개체명 분석 코드
    text = "기본"  # 분석할 대상
    data = ""  # api를 통해서 받은 분석결과 json
    result = ""  # data를 리스트로 변환한 분석결과변수-변수이름 고치기
    k = 0

    def __init__(self, userFile):

        self.text = self.setText(userFile)
        print(type(self.text))
        print("현재분석코드 " + self.analysisCode)
        print("현재분석문장 " + self.text)
        self.data = self.setData()
        self.result = self.result(self.data)

    '''
    사용자가 분석할 텍스트 파일 저장
    '''

    def setText(self, userFile):

        '''
        myFile = open(userFile, "r", encoding="utf-8")
        self.text = myFile.read()
        return self.text
        '''
        # '''
        self.text = userFile
        return self.text
        # '''

    '''
    api로부터 json 값을 가져오기
    '''

    def setData(self):
        requestJson = {
            "access_key": self.accessKey,
            "argument": {
                "text": self.text,
                "analysis_code": self.analysisCode
            }
        }

        http = urllib3.PoolManager()

        response = http.request(
            "POST",
            self.openApiURL,
            headers={"Content-Type": "application/json; charset=UTF-8"},
            body=json.dumps(requestJson)  # json파일로 api를 받음
        )

        self.data = str(response.data, "utf-8")
        return self.data

    '''
    josn데이터에서 필요한 데이터값 가져오기
    '''

    def result(self, data):
        test = json.loads(data)
        print(test)
        self.result = test['return_object']['sentence']
        return self.result

    '''
    형태소 분석부분
    '''

    def showMorp(self, answer = ""): #analysis_data = dict()):
        test = ''
        print("형태소분석결과 ")
        strnum = len(self.result)  # 총문장갯수
        print(strnum)
        morpnum = len(self.result[0]['morp'])  # 하나의 문장당 형태소 갯수
        print(morpnum)

        wordnum = len(self.result[0]['word'])  # 하나의 문장단 단어 갯수
        print(wordnum)

        # analysis_data['key'] = list()
        # analysis_data['value'] = list()

        with open('morpAPI.txt', 'w', encoding="utf-8") as make_file:
            for i in range(strnum):
                for j in range(morpnum - 1):
                    str = ''

                    str = self.result[i]['morp'][j]['lemma'] + ":" + self.result[i]['morp'][j]['type']


                    # analysis_data['key'].append(self.result[i]['morp'][j]['lemma'])
                    # analysis_data['value'].append(self.result[i]['morp'][j]['type'])
                    # jsonString = json.dumps(analysis_data, ensure_ascii=False, indent=4)

                    if self.result[i]['morp'][j]['position'] - self.result[i]['morp'][j - 1]['position'] == 4:

                        print("  ", end="")
                        answer += "  "
                        print(str, end="")
                        answer += str

                    else:
                        # str=str.replace("\"\"",)
                        print(str, end="")
                        answer += str

                    json.dump(str, make_file, ensure_ascii=False, indent=4)

        # myFile = open("C:\\Users\\User\\PycharmProjects\\Cosmos\\morpAPI.txt", "r", encoding="utf-8")
        myFile = open("/home/ubuntu/virtual_cosmos/cosmos_flask_server/morpAPI.txt", "r", encoding="utf-8")

        text = myFile.readline()
        print("\n")
        print(type(test))
        print("\n")
        print(test)
        '''
        if self.text==" + ":
            self.text=self.text.replace("  + "," aa")
        else :
            self.text=self.text.replace("\"","")
            print(self.text)

       # print(self.text)
        self.text=self.text.replace("\"","")
        self.setOutput(self.text)

        '''
        text = text.replace("\"\"", " / ")

        text = text.replace("\"\"", " /")
        text = text.replace("\"", "")

        print("\n")
        print(type(text))
        print(text)
        print("\n")

        # print(text)
        self.setOutput(text)

        print(answer)
        return answer



        # return jsonString

    def setOutput(self, str):
        with open('morpAPI.txt', 'w', encoding="utf-8") as make_file:
            json.dump(str, make_file, ensure_ascii=False, indent=4)


# if __name__ == "__main__":
#     hi = morpAPI("C:\\Users\\User\\PycharmProjects\\Cosmos\\text1.txt")
#     hi.showMorp()

app = Flask(__name__)

# @app.route('/')
# def hello_world():
#     hi = morpAPI("C:\\Users\\User\\PycharmProjects\\Cosmos\\text1.txt")
#     morpResult = hi.showMorp()
#
#     return morpResult

@app.route('/')
def hello_world():
    hi = morpAPI("엑소브레인은 내 몸 바깥에 있는 인공 두뇌라는 뜻으로, 세계 최고인공지능 기술 선도라는 비전을 달성하기 위한 과학기술정보통신부 소프트웨어 분야의 국가 혁신기술 개발형 연구개발 과제이다.")
    morpResult = hi.showMorp()

    return morpResult

class AnalysisAPI():
    morp = ""
    code = ""


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

@app.route("/test2", methods=['POST'])
def test2():
    data = request.json
    print(data)
    hi = morpAPI2(data['text'])
    moreResult = hi.showMorp2()

    data['analysisResult'] = moreResult
    print(type(data['analysisResult']))
    print(data['analysisResult'])
    return jsonify(data)
