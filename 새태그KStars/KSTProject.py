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
    def ProjectLoad(self, filePath):

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
            main.ProjectLoad_KVer1(filePath)
        else:
            print("잘못된 경로입니다.")

        main.m_KFilePath.projectFilePath = filePath

    """
        KST파일을 불러오는 함수
    """
    def ProjectLoad_KVer1(self, filePath):
        reader = open(filePath, 'rt', encoding='utf-8')
        kstSoup = BeautifulSoup(reader, 'lxml-xml')

        # <Version> 태그안에 값 => 1.0.0
        self.Version = kstSoup.find('Version').string

        # <Version> 태그값을 출력
        print(self.Version)

        # <Option> 태그안에 있는 모든 값
        for SpeakerListElement in kstSoup.findAll('SpeakerList'):
            self.m_Option.SpeakerList.append(SpeakerListElement.string)
        self.m_Option.StringOption = kstSoup.find('StringOption').string

        # <Option> 태그값을 출력
        print(self.m_Option.SpeakerList)
        print(self.m_Option.StringOption)

        # <Header> 태그안에 있는 모든 값
        self.m_Header.speechType = kstSoup.find('SpeechType').string
        for ParticipantsElement in kstSoup.findAll('Participants'):
            self.m_Header.arrParticipants.append(ParticipantsElement.string)
        self.m_Header.BirthPlaceOfCHI = kstSoup.find('BirthPlaceofCHI').string
        self.m_Header.Location = kstSoup.find('Location').string
        self.m_Header.Situation = kstSoup.find('Situation').string
        self.m_Header.Recording = kstSoup.find('Recording').string
        self.m_Header.Transcriber = kstSoup.find('Transcriber').string
        self.m_Header.Reviewer = kstSoup.find('Reviewer').string
        self.m_Header.Comment = kstSoup.find('Comment').string

        # <Header> 태그값을 출력
        print(self.m_Header.speechType)
        print(self.m_Header.arrParticipants)
        print(self.m_Header.BirthPlaceOfCHI)
        print(self.m_Header.Location)
        print(self.m_Header.Situation)
        print(self.m_Header.Recording)
        print(self.m_Header.Transcriber)
        print(self.m_Header.Reviewer)
        print(self.m_Header.Comment)

        # <ID> 태그안에 있는 모든 값
        id = kstSoup.findAll('ID')
        for i in range(len(kstSoup.findAll('ID'))):
            self.m_Header.arrID.append(ID())
            self.m_Header.arrID[i].IDCorpus = id[i].IDCorpus.string
            self.m_Header.arrID[i].IDCode = id[i].IDCode.string
            self.m_Header.arrID[i].IDDateOfBirth = id[i].IDDateofBirth.string
            self.m_Header.arrID[i].IDAge = id[i].IDAge.string
            self.m_Header.arrID[i].IDSex = id[i].IDSex.string
            self.m_Header.arrID[i].IDGroup = id[i].IDGroup.string
            self.m_Header.arrID[i].IDRegion = id[i].IDRegion.string
            self.m_Header.arrID[i].IDSES = id[i].IDSES.string
            self.m_Header.arrID[i].IDEdu = id[i].IDEdu.string
            self.m_Header.arrID[i].IDRole = id[i].IDRole.string

        # <ID> 태그의 일정 부분을 출력
        for i in range(len(self.m_Header.arrID)):
            print("ID[", i, "] : ", self.m_Header.arrID[i].IDCode,
                  "/", self.m_Header.arrID[i].IDAge,
                  "/", self.m_Header.arrID[i].IDSex, " 등등...")

        for tierElement in kstSoup.findAll("Tier"):
            if tierElement['type'] == "KUtterance":
                self.m_KTierVer2.dataType = tierElement['type']
            elif tierElement['type'] == "KMorpheme":
                self.m_KTierMorpVer2.dataType = tierElement['type']

        data = kstSoup.findAll('Data')
        for i in range(int(len(kstSoup.findAll("Data"))/2)):
            self.m_KTierVer2.datas.append(KDataVer2())
            self.m_KTierVer2.datas[i].uid = data[i]['uid']
            self.m_KTierVer2.datas[i].speaker = data[i].Speaker.string
            self.m_KTierVer2.datas[i].text = data[i].Text.string
            self.m_KTierVer2.datas[i].time = data[i].Time.string

        num = int(len(kstSoup.findAll("Data"))/2)
        for i in range(int(len(kstSoup.findAll("Data"))/2)):
            self.m_KTierMorpVer2.datas.append(KMorpVer2())
            self.m_KTierMorpVer2.datas[i].uid = data[num+i]['uid']
            self.m_KTierMorpVer2.datas[i].speaker = data[num+i].Speaker.string
            self.m_KTierMorpVer2.datas[i].morp = data[num+i].MEtri.string
            self.m_KTierMorpVer2.datas[i].user = data[num+i].MUser.string

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
        self.m_Audio.AudioPath = kstSoup.find("AudioPath").string
        self.m_Audio.AudioFileIndex = kstSoup.find("AudioFileIndex").string
        self.m_Audio.AudioCurrentPosition = kstSoup.find("AudioCurrentPosition").string

        # <Audio> 태그 안에 값 출력
        print(self.m_Audio.AudioPath)
        print(self.m_Audio.AudioFileIndex)
        print(self.m_Audio.AudioCurrentPosition)

if __name__ == "__main__":
    hi = KSTProject()
    hi.ProjectLoad(os.getcwd() + "\\BeautifulSoupKST.kst")