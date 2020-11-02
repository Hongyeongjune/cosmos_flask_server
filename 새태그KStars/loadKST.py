import errno
import os

from bs4 import BeautifulSoup

from 새태그KStars.domain.KDataVer2 import KDataVer2
from 새태그KStars.domain.Audio import Audio
from 새태그KStars.domain.Data import Data
from 새태그KStars.domain.Header import Header
from 새태그KStars.domain.ID import ID
from 새태그KStars.domain.KFilePath import KFilePath
from 새태그KStars.domain.KMorpVer2 import KMorpVer2
from 새태그KStars.domain.KTierMorpVer2 import KTierMorpVer2
from 새태그KStars.domain.KTierVer2 import KTierVer2
from 새태그KStars.domain.Option import Option

from flask import Flask, jsonify
from flask import request
from xml.etree.ElementTree import Element, SubElement, ElementTree

app = Flask(__name__)

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
    cloudPath = os.path.abspath("\\home\\ubuntu\\kst")
    hi = KSTProject()
    # data = hi.ProjectLoad(localPath + "\\guest\\temp\\BeautifulSoupKST.kst", data)
    data = hi.ProjectLoad(cloudPath + "\\guest\\temp\\BeautifulSoupKST.kst", data)
    print(data)

    return jsonify(data)