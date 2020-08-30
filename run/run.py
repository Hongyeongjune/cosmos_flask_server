import errno
import os
from enum import Enum
from bs4 import BeautifulSoup

from konlpy.tag import Kkma

import urllib3
import json

from flask import Flask, jsonify, app
from flask import request
from xml.etree.ElementTree import Element, SubElement, ElementTree
from collections import OrderedDict

app = Flask(__name__)

class KDataVer2:
    def __init__(self):
        self.uid = ""
        self.speaker = ""
        self.text = ""
        self.time = ""
class Audio:
    def __init__(self):
        self.AudioPath = list()
        self.AudioFileIndex = 0
        self.AudioCurrentPosition = 0.0

    def initData(self):
        self.AudioFileIndex = 0
        self.AudioCurrentPosition = 0
        self.AudioPath.clear()
class Data:
    def __init__(self):
        self.DataType = ""
        self.speaker = ""
        self.ST = -1
        self.ET = -1
        self.datas = Tier()
class Tier:
    def __init__(self):
        self.TypeIndex = 0
        self.type = Enum('TierType', 'Empty Comment')
        self.StartText = ""
        self.EndText =""
        self.datas = list()
class Header:

    def __init__(self):
        self.speechType = ""
        self.arrParticipants = list()
        self.arrID = list()
        self.Language = ""
        self.BirthOfCHI = ""
        self.BirthPlaceOfCHI = ""
        self.Date = ""
        self.Location = ""
        self.Situation = ""
        self.Media = ""
        self.Recording = ""
        self.Transcriber = ""
        self.Reviewer = ""
        self.Comment = ""


    def initData(self):
        self.speechType = ""
        self.arrParticipants.clear()
        self.arrID = list()
        self.BirthOfCHI = ""
        self.BirthPlaceOfCHI = ""
        self.Date = ""
        self.Location = ""
        self.Situation = ""
        self.Media = ""
        self.Recording = ""
        self.Transcriber = ""
        self.Reviewer = ""
        self.Comment = ""
class ID:
    def __init__(self):
        self.IDCorpus = ""
        self.IDCode = ""
        self.IDDateOfBirth = ""
        self.IDAge = ""
        self.IDSex = ""
        self.IDGroup = ""
        self.IDRegion = ""
        self.IDSES = ""
        self.IDEdu = ""
        self.IDRole = ""
class KFilePath:
    def __init__(self):
        self.projectFilePath = ""
        self.audioFilePath = ""

    def initData(self):
        self.projectFilePath = ""
        self.audioFilePath = ""
class KMorpVer2:
    def __init__(self):
        self.uid = ""
        self.speaker = ""
        self.morp = ""
        self.user = ""
class KTierMorpVer2:

    def __init__(self):
        self.dataType = ""
        self.datas = list()
class KTierVer2:

    def __init__(self):
        self.dataType = ""
        self.datas = list()
class Option:
    def __init__(self):
        self.indent = 5
        self.SpeakerList = list()
        self.StringOption = "0000000"

    def initData(self):
        self.indent = ""
        self.SpeakerList = list()
        self.StringOption = "0000000"

@app.route("/cosmos/KStars/create/kst", methods=['POST'])
def cosmos_create_file():
    # request.josn = 스프링에서 restTemplate로 보낸 json데이터를 담는다.
    data = request.json
    print(data)

    #기억이 안남
    def indent(node, level=0):
        i = "\n" + level * " " * 4
        if len(node):
            if not node.text or not node.text.strip():
                node.text = i + " " * 4
            if not node.tail or not node.tail.strip():
                node.tail = i
            for node in node:
                indent(node, level + 1)
            if not node.tail or not node.tail.strip():
                node.tail = i
        else:
            if level and (not node.tail or not node.tail.strip()):
                node.tail = i

    # BeautifulSoup 라이브러리를 사용해서 kst 파일 생성.
    # Root = KStars
    root = Element('KStars')

    # <Version>
    SubElement(root, 'Version').text = data['version']

    # <Option>
    Option = SubElement(root, 'Option')
    # <Option> => <SpeakerList>
    for i in range(len(data['m_Option']["speakerList"])):
        SubElement(Option, "SpeakerList").text = data['m_Option']["speakerList"][i]
    # <Option> => <StringOption>
    SubElement(Option, "StringOption").text = data['m_Option']["stringOption"]

    # <Header>
    Header = SubElement(root, 'Header')
    # <Header> => <SpeechType>
    SubElement(Header, "SpeechType").text = data['m_header']['speechType']
    # <Header> => <Participants>
    for i in range(len(data['m_header']['arrParticipants'])):
        SubElement(Header, "Participants").text = data['m_header']['arrParticipants'][i]
    # <Header> => <BirthPlaceofCHI>
    SubElement(Header, "BirthPlaceOfCHI").text = data['m_header']['birthPlaceOfCHI']
    # <Header> => <Location>
    SubElement(Header, "Location").text = data['m_header']['location']
    # <Header> => <Situation>
    SubElement(Header, "Situation").text = data['m_header']['situation']
    # <Header> => <Recording>
    SubElement(Header, "Recording").text = data['m_header']['recording']
    # <Header> => <Transcriber>
    SubElement(Header, "Transcriber").text = data['m_header']['transcriber']
    # <Header> => <Reviewer>
    SubElement(Header, "Reviewer").text = data['m_header']['reviewer']
    # <Header> => <Comment>
    SubElement(Header, "Comment").text = data['m_header']['comment']

    # <Header> => <ID>
    for i in range(len(data['m_header']['arrID'])):
        UserID = SubElement(Header, "ID")
        # <Header> => <ID> => <IDCorpus>
        SubElement(UserID, "IDCorpus").text = data['m_header']['arrID'][i]['corpus']
        # <Header> => <ID> => <IDCode>
        SubElement(UserID, "IDCode").text = data['m_header']['arrID'][i]['code']
        # <Header> => <ID> => <IDDateOfBirth>
        SubElement(UserID, "IDDateOfBirth").text = data['m_header']['arrID'][i]['dateOfBirth']
        # <Header> => <ID> => <IDAge>
        SubElement(UserID, "IDAge").text = data['m_header']['arrID'][i]['age']
        # <Header> => <ID> => <IDSex>
        SubElement(UserID, "IDSex").text = data['m_header']['arrID'][i]['sex']
        # <Header> => <ID> => <IDGroup>
        SubElement(UserID, "IDGroup").text = data['m_header']['arrID'][i]['group']
        # <Header> => <ID> => <IDRegion>
        SubElement(UserID, "IDRegion").text = data['m_header']['arrID'][i]['region']
        # <Header> => <ID> => <IDSES>
        SubElement(UserID, "IDSES").text = data['m_header']['arrID'][i]['ses']
        # <Header> => <ID> => <IDEdu>
        SubElement(UserID, "IDEdu").text = data['m_header']['arrID'][i]['edu']
        # <Header> => <ID> => <IDRole>
        SubElement(UserID, "IDRole").text = data['m_header']['arrID'][i]['role']
    # <Tier type = "KUtterance">
    KUtterance = SubElement(root, "Tier")
    KUtterance.attrib['type'] = data['m_KTierVer2']['dataType']
    # <Tier type = "KUtterance"> => <Data>
    for i in range(len(data['m_KTierVer2']['datas'])):
        DataUtter = SubElement(KUtterance, "Data")
        # <Tier type = "KUtterance"> => <Data uid = "?">
        DataUtter.attrib['uid'] = data['m_KTierVer2']['datas'][i]['uid']
        # <Tier type = "KUtterance"> => <Data uid = "?"> => <Speaker>
        SubElement(DataUtter, 'Speaker').text = data['m_KTierVer2']['datas'][i]['speaker']
        # <Tier type = "KUtterance"> => <Data uid = "?"> => <Text>
        SubElement(DataUtter, 'Text').text = data['m_KTierVer2']['datas'][i]['text']
        # <Tier type = "KUtterance"> => <Data uid = "?"> => <Time>
        SubElement(DataUtter, 'Time').text = data['m_KTierVer2']['datas'][i]['time']

    KMorpheme = SubElement(root, "Tier")
    KMorpheme.attrib['type'] = data['m_KTierMorpVer2']['dataType']
    for i in range(len(data['m_KTierMorpVer2']['datas'])):
        DataMorp = SubElement(KMorpheme, "Data")
        DataMorp.attrib['uid'] = data['m_KTierMorpVer2']['datas'][i]['uid']
        SubElement(DataMorp, 'Speaker').text = data['m_KTierMorpVer2']['datas'][i]['speaker']
        SubElement(DataMorp, 'MEtri').text = data['m_KTierMorpVer2']['datas'][i]['morp']
        SubElement(DataMorp, 'MUser').text = data['m_KTierMorpVer2']['datas'][i]['user']


    Audio = SubElement(root, "Audio")
    for i in range(len(data['m_Audio']['audioPath'])):
        SubElement(Audio, 'AudioPath').text = data['m_Audio']['audioPath'][i]
    SubElement(Audio, 'AudioFileIndex').text = data['m_Audio']['audioFileIndex']
    SubElement(Audio, 'AudioCurrentPosition').text = data['m_Audio']['audioCurrentPosition']
    indent(root)

    tree = ElementTree(root)
    # localPath = os.path.abspath("C:/Users/User/eclipse-workspace/K-Stars/src/main/java/kr/ac/skuniv/cosmos")
    cloudPath = os.path.abspath("/home/ubuntu/kst")

    if data['userDto']['user'] == "guest":
        # tree.write(localPath + "\\guest\\temp\\" + data['userDto']['fileName'] + ".kst", encoding="utf-8")
        tree.write(cloudPath + "/guest/temp/" + data['userDto']['fileName'] + ".kst", encoding="utf-8")
    elif data['userDto']['user'] == "user":
        try:
            # if not(os.path.isdir(localPath + "\\user\\" + data['userDto']['id'])):
            #     os.makedirs(os.path.join(localPath + "\\user\\" + data['userDto']['id']))
            #     tree.write(localPath + "\\user\\" + data['userDto']['id'] + "\\" + data['userDto']['fileName'] + ".kst", encoding="utf-8")
            # if os.path.isdir(localPath + "\\user\\" + data['userDto']['id']):
            #     tree.write(localPath + "\\user\\" + data['userDto']['id'] + "\\" + data['userDto']['fileName'] + ".kst", encoding="utf-8")
            if not (os.path.isdir(cloudPath + "\\user\\" + data['userDto']['id'])):
                os.makedirs(os.path.join(cloudPath + "\\user\\" + data['userDto']['id']))
                tree.write(cloudPath + "\\user\\" + data['userDto']['id'] + "\\" + data['userDto']['fileName'] + ".kst",
                           encoding="utf-8")
            if os.path.isdir(cloudPath + "\\user\\" + data['userDto']['id']):
                tree.write(cloudPath + "\\user\\" + data['userDto']['id'] + "\\" + data['userDto']['fileName'] + ".kst",
                           encoding="utf-8")
        except OSError as e:
            if e.errno != errno.EEXIST:
                print("Failed to create directory!!!!!")
                raise

    return jsonify(data)

class KSTProject:
    Version = "1.0.0"
    m_Header = Header()
    m_data = Data()
    m_KData = list()
    m_KFilePath = KFilePath()
    m_Option = Option()
    m_Audio = Audio()
    m_arrCustom = list()
    m_arrCustom_cn = list()
    m_KTierVer2 = KTierVer2()
    m_KTierMorpVer2 = KTierMorpVer2()


    """
        KST파일에 맞는 형식인지 아닌지 체크하는 함수
    """
    def ProjectLoad(self, filePath, data):

        nVer = 0

        reader = open(filePath, 'rt', encoding='utf-8')
        kstSoup = BeautifulSoup(reader, 'lxml-xml')

        project = kstSoup.find('KStars')

        if project is None:
            print("KST 파일이 아닙니다.")
        else:
            project = kstSoup.find('Version')

            if project.string.index("1.0") > -1:
                nVer = 1

        """
            KST파일이 맞다면 KST파일을 불러오는 함수 실행
        """
        if nVer == 1:
            main = KSTProject()
            return(main.ProjectLoad_KVer1(filePath, data))
        else:
            print("잘못된 경로입니다.")

            # main.m_KFilePath.projectFilePath = filePath

    """
        KST파일을 불러오는 함수
    """
    def ProjectLoad_KVer1(self, filePath, data):

        print("진짜데이터 : ", data)

        reader = open(filePath, 'rt', encoding='utf-8')
        kstSoup = BeautifulSoup(reader, 'lxml-xml')

        # <Version> 태그안에 값 => 1.0.0
        # kstSoup.find('Version').string => Kst 파일을 BeautifulSoup 라이브러리로 읽었음.
        # self.Version => 파이썬의 KstProject()의 구조체인데 사실 필요없었던거 였음.
        self.Version = kstSoup.find('Version').string
        # <Version> 태그값을 출력
        data['version'] = self.Version
        # data['version'] = kstSoup.find('Version').string
        print(data['version'])

        # <Option> 태그안에 있는 모든 값
        i = 0
        for SpeakerListElement in kstSoup.findAll('SpeakerList'):
            self.m_Option.SpeakerList.append(SpeakerListElement.string)
            if i == 0:
                data['m_Option']["speakerList"][i] = self.m_Option.SpeakerList[i]
            else :
                data['m_Option']["speakerList"].append(self.m_Option.SpeakerList[i])
            i+=1
        self.m_Option.StringOption = kstSoup.find('StringOption').string
        data['m_Option']["stringOption"] = self.m_Option.StringOption

        # <Option> 태그값을 출력
        for i in range(len(data['m_Option']["speakerList"])):
            print(data['m_Option']["speakerList"][i])
        print(data['m_Option']["stringOption"])

        # <Header> 태그안에 있는 모든 값
        i = 0
        self.m_Header.speechType = kstSoup.find('SpeechType').string
        data['m_header']['speechType'] = self.m_Header.speechType
        for ParticipantsElement in kstSoup.findAll('Participants'):
            self.m_Header.arrParticipants.append(ParticipantsElement.string)
            if i == 0:
                data['m_header']['arrParticipants'][i] = self.m_Header.arrParticipants[i]
            else :
                data['m_header']['arrParticipants'].append(self.m_Header.arrParticipants[i])
            i+=1
        self.m_Header.BirthPlaceOfCHI = kstSoup.find('BirthPlaceofCHI').string
        data['m_header']['birthPlaceOfCHI'] = self.m_Header.BirthPlaceOfCHI
        self.m_Header.Location = kstSoup.find('Location').string
        data['m_header']['location'] = self.m_Header.Location
        self.m_Header.Situation = kstSoup.find('Situation').string
        data['m_header']['situation'] = self.m_Header.Situation
        self.m_Header.Recording = kstSoup.find('Recording').string
        data['m_header']['recording'] = self.m_Header.Recording
        self.m_Header.Transcriber = kstSoup.find('Transcriber').string
        data['m_header']['transcriber'] = self.m_Header.Transcriber
        self.m_Header.Reviewer = kstSoup.find('Reviewer').string
        data['m_header']['reviewer'] = self.m_Header.Reviewer
        self.m_Header.Comment = kstSoup.find('Comment').string
        data['m_header']['comment'] = self.m_Header.Comment

        # <Header> 태그값을 출력
        print(data['m_header']['speechType'])
        for i in range(len(data['m_header']['arrParticipants'])):
            print(data['m_header']['arrParticipants'][i])
        print(data['m_Option']["stringOption"])
        print(data['m_header']['birthPlaceOfCHI'])
        print(data['m_header']['location'])
        print(data['m_header']['situation'])
        print(data['m_header']['recording'])
        print(data['m_header']['transcriber'])
        print(data['m_header']['reviewer'])
        print(data['m_header']['comment'])

        # <ID> 태그안에 있는 모든 값
        id = kstSoup.findAll('ID')
        for i in range(len(kstSoup.findAll('ID'))):
            self.m_Header.arrID.append(ID())
            if i == 0:
                self.m_Header.arrID[i].IDCorpus = id[i].IDCorpus.string
                data['m_header']['arrID'][i]['corpus'] = self.m_Header.arrID[i].IDCorpus
                self.m_Header.arrID[i].IDCode = id[i].IDCode.string
                data['m_header']['arrID'][i]['code'] = self.m_Header.arrID[i].IDCode
                self.m_Header.arrID[i].IDDateOfBirth = id[i].IDDateofBirth.string
                data['m_header']['arrID'][i]['dateOfBirth'] = self.m_Header.arrID[i].IDDateOfBirth
                self.m_Header.arrID[i].IDAge = id[i].IDAge.string
                data['m_header']['arrID'][i]['age'] = self.m_Header.arrID[i].IDAge
                self.m_Header.arrID[i].IDSex = id[i].IDSex.string
                data['m_header']['arrID'][i]['sex'] = self.m_Header.arrID[i].IDSex
                self.m_Header.arrID[i].IDGroup = id[i].IDGroup.string
                data['m_header']['arrID'][i]['group'] = self.m_Header.arrID[i].IDGroup
                self.m_Header.arrID[i].IDRegion = id[i].IDRegion.string
                data['m_header']['arrID'][i]['region'] = self.m_Header.arrID[i].IDRegion
                self.m_Header.arrID[i].IDSES = id[i].IDSES.string
                data['m_header']['arrID'][i]['ses'] = self.m_Header.arrID[i].IDSES
                self.m_Header.arrID[i].IDEdu = id[i].IDEdu.string
                data['m_header']['arrID'][i]['edu'] = self.m_Header.arrID[i].IDEdu
                self.m_Header.arrID[i].IDRole = id[i].IDRole.string
                data['m_header']['arrID'][i]['role'] = self.m_Header.arrID[i].IDRole
            else :
                data['m_header']['arrID'].append(data['m_header']['arrID'][0])
                self.m_Header.arrID[i].IDCorpus = id[i].IDCorpus.string
                data['m_header']['arrID'][i]['corpus'] = self.m_Header.arrID[i].IDCorpus
                self.m_Header.arrID[i].IDCode = id[i].IDCode.string
                data['m_header']['arrID'][i]['code'] = self.m_Header.arrID[i].IDCode
                self.m_Header.arrID[i].IDDateOfBirth = id[i].IDDateofBirth.string
                data['m_header']['arrID'][i]['dateOfBirth'] = self.m_Header.arrID[i].IDDateOfBirth
                self.m_Header.arrID[i].IDAge = id[i].IDAge.string
                data['m_header']['arrID'][i]['age'] = self.m_Header.arrID[i].IDAge
                self.m_Header.arrID[i].IDSex = id[i].IDSex.string
                data['m_header']['arrID'][i]['sex'] = self.m_Header.arrID[i].IDSex
                self.m_Header.arrID[i].IDGroup = id[i].IDGroup.string
                data['m_header']['arrID'][i]['group'] = self.m_Header.arrID[i].IDGroup
                self.m_Header.arrID[i].IDRegion = id[i].IDRegion.string
                data['m_header']['arrID'][i]['region'] = self.m_Header.arrID[i].IDRegion
                self.m_Header.arrID[i].IDSES = id[i].IDSES.string
                data['m_header']['arrID'][i]['ses'] = self.m_Header.arrID[i].IDSES
                self.m_Header.arrID[i].IDEdu = id[i].IDEdu.string
                data['m_header']['arrID'][i]['edu'] = self.m_Header.arrID[i].IDEdu
                self.m_Header.arrID[i].IDRole = id[i].IDRole.string
                data['m_header']['arrID'][i]['role'] = self.m_Header.arrID[i].IDRole

        # <ID> 태그의 일정 부분을 출력
        for i in range(len(data['m_header']['arrID'])):
            print("ID[", i, "] : ", data['m_header']['arrID'][i])

        for tierElement in kstSoup.findAll("Tier"):
            if tierElement['type'] == "KUtterance":
                self.m_KTierVer2.dataType = tierElement['type']
                data['m_KTierVer2']['dataType'] = self.m_KTierVer2.dataType
            elif tierElement['type'] == "KMorpheme":
                self.m_KTierMorpVer2.dataType = tierElement['type']
                data['m_KTierMorpVer2']['dataType'] = self.m_KTierMorpVer2.dataType

        dataTag = kstSoup.findAll('Data')
        for i in range(int(len(kstSoup.findAll("Data"))/2)):
            self.m_KTierVer2.datas.append(KDataVer2())
            if i == 0:
                self.m_KTierVer2.datas[i].uid = dataTag[i]['uid']
                self.m_KTierVer2.datas[i].speaker = dataTag[i].Speaker.string
                self.m_KTierVer2.datas[i].text = dataTag[i].Text.string
                self.m_KTierVer2.datas[i].time = dataTag[i].Time.string
                data['m_KTierVer2']['datas'][i]['uid'] = self.m_KTierVer2.datas[i].uid
                data['m_KTierVer2']['datas'][i]['speaker'] = self.m_KTierVer2.datas[i].speaker
                data['m_KTierVer2']['datas'][i]['text'] = self.m_KTierVer2.datas[i].text
                data['m_KTierVer2']['datas'][i]['time'] = self.m_KTierVer2.datas[i].time
            else :
                data['m_KTierVer2']['datas'].append(data['m_KTierVer2']['datas'][0])
                self.m_KTierVer2.datas[i].uid = dataTag[i]['uid']
                self.m_KTierVer2.datas[i].speaker = dataTag[i].Speaker.string
                self.m_KTierVer2.datas[i].text = dataTag[i].Text.string
                self.m_KTierVer2.datas[i].time = dataTag[i].Time.string
                data['m_KTierVer2']['datas'][i]['uid'] = self.m_KTierVer2.datas[i].uid
                data['m_KTierVer2']['datas'][i]['speaker'] = self.m_KTierVer2.datas[i].speaker
                data['m_KTierVer2']['datas'][i]['text'] = self.m_KTierVer2.datas[i].text
                data['m_KTierVer2']['datas'][i]['time'] = self.m_KTierVer2.datas[i].time

        num = int(len(kstSoup.findAll("Data"))/2)
        for i in range(int(len(kstSoup.findAll("Data"))/2)):
            self.m_KTierMorpVer2.datas.append(KMorpVer2())
            if i == 0 :
                self.m_KTierMorpVer2.datas[i].uid = dataTag[num + i]['uid']
                self.m_KTierMorpVer2.datas[i].speaker = dataTag[num + i].Speaker.string
                self.m_KTierMorpVer2.datas[i].morp = dataTag[num + i].MEtri.string
                self.m_KTierMorpVer2.datas[i].user = dataTag[num + i].MUser.string
                data['m_KTierMorpVer2']['datas'][i]['uid'] = self.m_KTierMorpVer2.datas[i].uid
                data['m_KTierMorpVer2']['datas'][i]['speaker'] = self.m_KTierMorpVer2.datas[i].speaker
                data['m_KTierMorpVer2']['datas'][i]['morp'] = self.m_KTierMorpVer2.datas[i].morp
                data['m_KTierMorpVer2']['datas'][i]['user'] = self.m_KTierMorpVer2.datas[i].user
            else :
                data['m_KTierMorpVer2']['datas'].append(data['m_KTierMorpVer2']['datas'][0])
                self.m_KTierMorpVer2.datas[i].uid = dataTag[num + i]['uid']
                self.m_KTierMorpVer2.datas[i].speaker = dataTag[num + i].Speaker.string
                self.m_KTierMorpVer2.datas[i].morp = dataTag[num + i].MEtri.string
                self.m_KTierMorpVer2.datas[i].user = dataTag[num + i].MUser.string
                data['m_KTierMorpVer2']['datas'][i]['uid'] = self.m_KTierMorpVer2.datas[i].uid
                data['m_KTierMorpVer2']['datas'][i]['speaker'] = self.m_KTierMorpVer2.datas[i].speaker
                data['m_KTierMorpVer2']['datas'][i]['morp'] = self.m_KTierMorpVer2.datas[i].morp
                data['m_KTierMorpVer2']['datas'][i]['user'] = self.m_KTierMorpVer2.datas[i].user

        # <Tier type = "KUtterance"> 태그의 Data 값 출력
        for i in range(len(self.m_KTierVer2.datas)):
            print("Data[", i, "] : ", self.m_KTierVer2.datas[i].uid,
                  "/", self.m_KTierVer2.datas[i].speaker,
                  "/", self.m_KTierVer2.datas[i].text,
                  "/", self.m_KTierVer2.datas[i].time)

        # <Tier type = "KMorpheme"> 태그의 Data 값 출력
        for i in range(len(self.m_KTierMorpVer2.datas)):
            print("Data[", i, "] : ", self.m_KTierMorpVer2.datas[i].uid,
                  "/", self.m_KTierMorpVer2.datas[i].speaker,
                  "/", self.m_KTierMorpVer2.datas[i].morp,
                  "/", self.m_KTierMorpVer2.datas[i].user)

        # <Audio> 태그 안에 모든 값
        for AudioPathElement in kstSoup.findAll('AudioPath'):
            self.m_Audio.AudioPath.append(AudioPathElement.string)
            if i == 0:
                data['m_Audio']['audioPath'][i] = self.m_Audio.AudioPath[i]
            elif len(self.m_Audio.AudioPath) != 1:
                data['m_Audio']['audioPath'].append(self.m_Audio.AudioPath[i])
                # print(i, "\n")
            i+=1

        self.m_Audio.AudioFileIndex = kstSoup.find("AudioFileIndex").string
        data['m_Audio']['audioFileIndex'] = self.m_Audio.AudioFileIndex
        self.m_Audio.AudioCurrentPosition = kstSoup.find("AudioCurrentPosition").string
        data['m_Audio']['audioCurrentPosition'] = self.m_Audio.AudioCurrentPosition

        # <Audio> 태그 안에 값 출력
        print(self.m_Audio.AudioPath)
        print(self.m_Audio.AudioFileIndex)
        print(self.m_Audio.AudioCurrentPosition)

        print("수정된 진짜 데이터 : ", data)
        return data

@app.route("/cosmos/KStars/load/kst", methods=['POST'])
def cosmos_load_file():
    data = request.json
    print(data)

    # localPath = os.path.abspath("C:/Users/User/eclipse-workspace/K-Stars/src/main/java/kr/ac/skuniv/cosmos")
    cloudPath = os.path.abspath("/home/ubuntu/kst")
    hi = KSTProject()
    # data = hi.ProjectLoad(localPath + "\\guest\\temp\\BeautifulSoupKST.kst", data)
    data = hi.ProjectLoad(cloudPath + "\\guest\\temp\\BeautifulSoupKST.kst", data)
    print(data)

    return jsonify(data)

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

        # myFile = open("C:/Users/User/PycharmProjects/Cosmos/형태소분석/morpAPI.txt", "r", encoding="utf-8")
        myFile = open("/home/ubuntu/cosmos_flask/cosmos_flask_server/run/morpAPI.txt", "r", encoding="utf-8")
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

    def showMorp(self, answer=""):  # analysis_data = dict()):
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


# @app.route('/')
# def hello_world():
#     hi = morpAPI("C:\\Users\\User\\PycharmProjects\\Cosmos\\text1.txt")
#     morpResult = hi.showMorp()
#
#     return morpResult

@app.route('/')
def hello_world():
    hi = morpAPI(
        "엑소브레인은 내 몸 바깥에 있는 인공 두뇌라는 뜻으로, 세계 최고인공지능 기술 선도라는 비전을 달성하기 위한 과학기술정보통신부 소프트웨어 분야의 국가 혁신기술 개발형 연구개발 과제이다.")
    morpResult = hi.showMorp()

    return morpResult

class AnalysisAPI():
    morp = ""
    code = ""


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
            # count = count + 1
            # print(count, "번째 문장 분석결과 : ", morph)
            # print("\n")

            # f.writelines(str(morph))
            # f.writelines("\n")

        return morph
        # f.close()r

@app.route("/cosmos/KStars/morpList/KoNLPy", methods=['POST'])
def cosmos_morp_konlpy_board():
    data = request.json

    for i in range(len(data)):
        analysis = KKma(data[i]['text'])
        resultList = analysis.showmorp()
        data[i]['analysisResult'] = resultList

    for i in range(len(data)):
        print(data[i]['analysisResult'])

    return jsonify(data)

adadadsdad = "adsaddsadadsadad"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
