# -*- coding: utf-8 -*-
import os
from flask import Flask, jsonify, app
from flask import request
from konlpy.tag import Kkma

Kkma = Kkma()

class KKma:
    text = "기본"  # 분석할 대상
    data = " "  # api를 통해서 받은 분석결과 json
    result = " "  # data를 리스트로 변환한 분석결과변수-변수이름 고치기

    def __init__(self, userFile):

        self.text = self.setText(userFile)

        print("--현재분석문장-- ")
        print(self.text)

        print("\n")

    def setText(self, userFile):

        # myFile = open(userFile, "r", encoding="utf-8")
        # self.text = myFile.readlines()
        self.text = userFile

        return self.text

    def showmorp(self):
        okja = self.text

        # okja = []
        # for line in self.text:
        #     okja.append(line)

        sentences_tag = []
        count = 0

        f = open('result.txt', 'w', encoding='utf-8')
        # for sentence in okja:

        print("분석 문장: ", okja)

        morph = Kkma.pos(okja)
        print(morph)
            # count = count + 1
            # print(count, "번째 문장 분석결과 : ", morph)
            # print("\n")

            # f.writelines(str(morph))
            # f.writelines("\n")

        return morph
        # f.close()

if __name__ == '__main__':
    data = KKma("안녕하세요.")
    data.showmorp()
    print(data)


# hi = KKma("C:\\Users\\cjdrn\\python\\text1.txt")
# hi.showmorp()
# if __name__ == '__main__':
#
#     app.run(host='0.0.0.0', port=5000, debug=True)




