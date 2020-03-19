# 개체명 분석기

import urllib3
import re
import json
from collections import OrderedDict
from pprint import pprint


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
        print("현재분석코드 " + self.analysisCode)
        print("현재분석문장 " + self.text)
        self.data = self.setData()
        self.result = self.result(self.data)

    '''
    사용자가 분석할 텍스트 파일 저장
    '''

    def setText(self, userFile):

        myFile = open(userFile, "r", encoding="utf-8")
        self.text = myFile.read()
        return self.text

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

    def showMorp(self):
        print("형태소분석결과 ")
        strnum = len(self.result)  # 총문장갯수
        print(strnum)
        morpnum = len(self.result[0]['morp'])  # 하나의 문장당 형태소 갯수
        print(morpnum)

        wordnum = len(self.result[0]['word'])  # 하나의 문장단 단어 갯수
        print(wordnum)

        with open('morpAPI.txt', 'w', encoding="utf-8") as make_file:
            for i in range(strnum):
                for j in range(morpnum - 1):
                    str = ''
                    str = self.result[i]['morp'][j]['lemma'] + ":" + self.result[i]['morp'][j]['type']

                    if self.result[i]['morp'][j]['position'] - self.result[i]['morp'][j - 1]['position'] == 4:

                        print("  ", end="")
                        print(str, end="")

                    else:
                        # str=str.replace("\"\"",)
                        print(str, end="")

                    json.dump(str, make_file, ensure_ascii=False, indent=4)

        myFile = open("C:\\Users\\cjdrn\\python\\morpAPI.txt", "r", encoding="utf-8")

        text = myFile.readline()

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

        # print(text)
        self.setOutput(text)

    def setOutput(self, str):
        with open('morpAPI.txt', 'w', encoding="utf-8") as make_file:
            json.dump(str, make_file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    hi = morpAPI("C:\\Users\\cjdrn\\python\\text1.txt")
    hi.showMorp()


