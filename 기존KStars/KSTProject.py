from 기존KStars.domain.Audio import Audio
from 기존KStars.domain.Header import Header
from 기존KStars.domain.ID import ID
from 기존KStars.domain.KData import KData
from 기존KStars.domain.Data import Data
from 기존KStars.domain.KFilePath import KFilePath
from 기존KStars.domain.Option import Option
from 기존KStars.domain.KTier import KTier
from 기존KStars.domain.DataType import DataType

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

    def initData(self):
        self.m_Header.initData()
        self.m_Audio.initData()
        self.m_KFilePath.initData()
        self.m_Option.initData()
        self.m_data = Data()
        self.m_KData = list()
        self.m_Option.StringOption = "0000000"

    def ProjectLoad(self, filePath):
        nVer = -1
        arrTemp = list()
        separator = list()
        strTempLine = ""
        endCheck = False

        reader = open(filePath, "r", encoding="utf-8")

        if reader.readline() == "<KStars>\n":

            while True:
                strTempLine = reader.readline()

                if strTempLine == "</Version>":
                    break
                arrTemp = strTempLine.split('\t')

                strTempLine = ""

                for test in arrTemp:
                    strTempLine += test

                separator.append('<')
                separator.append('>')

                strTempLine = strTempLine.replace(separator[0], ",")
                strTempLine = strTempLine.replace(separator[1], ",")

                arrTemp = strTempLine.split(",")
                if arrTemp[1] == "Version":
                    if arrTemp[2].index("1.0") > -1:
                        nVer = 1
                    endCheck = True

                if endCheck is True:
                    break

            if nVer == 1:
                main = KSTProject()
                main.ProjectLoad_KVer1(filePath)
            else:
                print("잘못된 경로입니다.")

            main.m_KFilePath.projectFilePath = filePath


    def ProjectLoad_KVer1(self, filePath):

        TempTierRealData = ""
        arrTemp = list()
        separator = list()
        strTempLine = ""
        returnValue = False
        english_version_tag = False
        korean_ver_participant = ""
        count1234a = 0
        reader = open(filePath, "r", encoding="utf-8")

        if reader.readline() == "<KStars>\n":

            while True:

                strTempLine = reader.readline()
                strTempLine = strTempLine.strip()


                if strTempLine == "</KStars>":
                    break

                arrTemp = strTempLine.split('\t')

                strTempLine = ""

                for test in arrTemp:
                    strTempLine += test

                separator.append('<')
                separator.append('>')

                strTempLine = strTempLine.replace(separator[0], ",")
                strTempLine = strTempLine.replace(separator[1], ",")

                arrTemp = strTempLine.split(",")

                if arrTemp[1] == "Version":
                    if arrTemp[2] != "1.0.0":
                        return False
                    else:
                        KSTProject.initData(self)
                        self.returnValue = True

                if arrTemp[1] == "Option":
                    nCount = 0

                    while True:

                        strTempLine = reader.readline()

                        strTempLine = strTempLine.strip()

                        if strTempLine == "</Option>":
                            break

                        arrTemp = strTempLine.split('\t')
                        strTempLine = ""

                        for test in arrTemp:
                            strTempLine += test

                        separator.append('<')
                        separator.append('>')

                        strTempLine = strTempLine.replace(separator[0], ",")
                        strTempLine = strTempLine.replace(separator[1], ",")

                        arrTemp = strTempLine.split(",")

                        if len(arrTemp) == 5:
                            if arrTemp[1] == "SpeakerList":
                                self.m_Option.SpeakerList.append(arrTemp[2])
                            elif arrTemp[1] == "StringOption":
                                self.m_Option.StringOption = arrTemp[2]
                            elif arrTemp[1] == "Dic":
                                self.m_arrCustom.append(arrTemp[2])
                            elif arrTemp[1] == "Dic_cn":
                                self.m_arrCustom_cn.append(arrTemp[2])

                if arrTemp[1] == "Header":
                    count = 0
                    while True:
                        strTempLine = reader.readline()
                        strTempLine = strTempLine.strip()

                        if strTempLine == "</Header>":
                            break

                        arrTemp = strTempLine.split("\t")
                        strTempLine = ""

                        for test in arrTemp:
                            strTempLine += test

                        separator.append('<')
                        separator.append('>')

                        strTempLine = strTempLine.replace(separator[0], ",")
                        strTempLine = strTempLine.replace(separator[1], ",")

                        arrTemp = strTempLine.split(",")

                        if arrTemp[1] == "Participants":
                            if len(arrTemp) == 5:
                                self.m_Header.arrParticipants.append(arrTemp[2])
                        elif arrTemp[1] == "BirthofCHI":
                            if len(arrTemp) == 5:
                                self.m_Header.BirthOfCHI = arrTemp[2]
                        elif arrTemp[1] == "BirthPlaceofCHI":
                            if len(arrTemp) == 5:
                                self.m_Header.BirthPlaceOfCHI = arrTemp[2]
                        elif arrTemp[1] == "Date":
                            if len(arrTemp) == 5:
                                self.m_Header.Date = arrTemp[2]
                        elif arrTemp[1] == "Location":
                            if len(arrTemp) == 5:
                                self.m_Header.Location = arrTemp[2]
                        elif arrTemp[1] == "Situation":
                            if len(arrTemp) == 5:
                                self.m_Header.Situation = arrTemp[2]
                        elif arrTemp[1] == "Media":
                            if len(arrTemp) == 5:
                                self.m_Header.Media = arrTemp[2]
                        elif arrTemp[1] == "Recording":
                            if len(arrTemp) == 5:
                                self.m_Header.Recording = arrTemp[2]
                        elif arrTemp[1] == "Transcriber":
                            if len(arrTemp) == 5:
                                self.m_Header.Transcriber = arrTemp[2]
                        elif arrTemp[1] == "Reviewer":
                            if len(arrTemp) == 5:
                                self.m_Header.Reviewer = arrTemp[2]
                        elif arrTemp[1] == "Comment":
                            if len(arrTemp) == 5:
                                self.m_Header.Comment = arrTemp[2]
                        elif arrTemp[1] == "ID":

                            tempID = ID()

                            self.m_Header.arrID.append(ID())
                            while True:

                                strTempLine = reader.readline()
                                strTempLine = strTempLine.strip()

                                if strTempLine == "</ID>":
                                    break

                                arrTemp = strTempLine.split("\t")
                                strTempLine = ""

                                for test in arrTemp:
                                    strTempLine += test

                                separator.append('<')
                                separator.append('>')

                                strTempLine = strTempLine.replace(separator[0], ",")
                                strTempLine = strTempLine.replace(separator[1], ",")

                                arrTemp = strTempLine.split(",")

                                if arrTemp[1] == "IDCorpus":
                                    if len(arrTemp) == 5:
                                        self.m_Header.arrID[count].Corpus = arrTemp[2]
                                elif arrTemp[1] == "IDCode":
                                    if len(arrTemp) == 5:
                                        self.m_Header.arrID[count].Code = arrTemp[2]
                                elif arrTemp[1] == "IDDateofBirth":
                                    if len(arrTemp) == 5:
                                        self.m_Header.arrID[count].DateOfBirth = arrTemp[2]
                                elif arrTemp[1] == "IDAge":
                                    if len(arrTemp) == 5:
                                        self.m_Header.arrID[count].Age = arrTemp[2]
                                elif arrTemp[1] == "IDSex":
                                    if len(arrTemp) == 5:
                                        self.m_Header.arrID[count].Sex = arrTemp[2]
                                elif arrTemp[1] == "IDGroup":
                                    if len(arrTemp) == 5:
                                        self.m_Header.arrID[count].Group = arrTemp[2]
                                elif arrTemp[1] == "IDRegion":
                                    if len(arrTemp) == 5:
                                        self.m_Header.arrID[count].Region = arrTemp[2]
                                elif arrTemp[1] == "IDSES":
                                    if len(arrTemp) == 5:
                                        self.m_Header.arrID[count].SES = arrTemp[2]
                                elif arrTemp[1] == "IDEdu":
                                    if len(arrTemp) == 5:
                                        self.m_Header.arrID[count].Edu = arrTemp[2]
                                elif arrTemp[1] == "IDRole":
                                    if len(arrTemp) == 5:
                                        self.m_Header.arrID[count].Role = arrTemp[2]
                                        count += 1

                if arrTemp[1] == "Data":
                    tempData = KData()

                    while True:
                        strTempLine = reader.readline()
                        strTempLine = strTempLine.strip()

                        if strTempLine == "</Data>":
                            break

                        arrTemp = strTempLine.split("\t")
                        strTempLine = ""

                        for test in arrTemp:
                            strTempLine += test

                        separator.append('<')
                        separator.append('>')

                        strTempLine = strTempLine.replace(separator[0], ",")
                        strTempLine = strTempLine.replace(separator[1], ",")

                        arrTemp = strTempLine.split(",")


                        if arrTemp[1] == "DataType":
                            if arrTemp[2] == "KData":
                                tempData.type = arrTemp[2]
                            if arrTemp[2] == "Empty":
                                tempData.type = DataType.Empty
                        if arrTemp[1] == "Speaker":
                            if len(arrTemp) == 5:
                                tempData.speaker = arrTemp[2]
                            else:
                                tempData.speaker = '@@'
                        if arrTemp[1] == "Tier":
                            tempTier = KTier()
                            while True:
                                strTempLine = reader.readline()
                                strTempLine = strTempLine.strip()

                                if strTempLine == "</Tier>":
                                    break

                                arrTemp = strTempLine.split("\t")
                                strTempLine = ""

                                for test in arrTemp:
                                    strTempLine += test

                                separator.append('<')
                                separator.append('>')

                                strTempLine = strTempLine.replace(separator[0], ",")
                                strTempLine = strTempLine.replace(separator[1], ",")

                                arrTemp = strTempLine.split(",")

                                if arrTemp[1] == "TierType":
                                        tempTier.type = arrTemp[2]
                                if arrTemp[1] == "Text":
                                    if len(arrTemp) > 4:
                                        tempTier.startText = arrTemp[2]
                                if arrTemp[1] == "EndText":
                                    if len(arrTemp) == 5:
                                        tempTier.EndText = arrTemp[2]
                                if arrTemp[1] == "Morpheme":
                                    if len(arrTemp) > 4:
                                        tempTier.MorpData = arrTemp[2]
                                if arrTemp[1] == "MU":
                                    if len(arrTemp) == 5:
                                        tempTier.MUData = arrTemp[2]
                                if arrTemp[1] == "TimePosition":
                                    tempTier.ST = arrTemp[2].split('/')[0]
                                    tempTier.ET = arrTemp[2].split('/')[1]
                            tempData.datas.append(tempTier)
                    self.m_KData.append(tempData)

                if arrTemp[1] == "Audio":

                    while True:
                        strTempLine = reader.readline()
                        strTempLine = strTempLine.strip()

                        if strTempLine == "</Audio>":
                            break

                        arrTemp = strTempLine.split("\t")
                        strTempLine = ""

                        for test in arrTemp:
                            strTempLine += test

                        separator.append('<')
                        separator.append('>')

                        strTempLine = strTempLine.replace(separator[0], ",")
                        strTempLine = strTempLine.replace(separator[1], ",")

                        arrTemp = strTempLine.split(",")

                        if arrTemp[1] == "AudioPath":
                            if len(arrTemp) == 5:
                                self.m_KFilePath.audioFilePath = arrTemp[2]
                                self.m_Audio.AudioPath.append(arrTemp[2])
                        if arrTemp[1] == "AudioFileIndex":
                            if len(arrTemp) == 5:
                                self.m_Audio.AudioFileIndex = arrTemp[2]
                        if arrTemp[1] == "AudioCurrentPosition":
                            if len(arrTemp[2]):
                                self.m_Audio.AudioCurrentPosition = arrTemp[2]


            print("SpeakerList : ", self.m_Option.SpeakerList)
            print("StringOption : ", self.m_Option.StringOption)
            print("Participants : ", self.m_Header.arrParticipants)

            for i in range(len(self.m_Header.arrID)):
                print("ID[", i, "] : ", self.m_Header.arrID[i].Code,
                      "/", self.m_Header.arrID[i].Age,
                      "/", self.m_Header.arrID[i].Sex, " 등등...")

            print("BirthPlaceOfChI : ", self.m_Header.BirthPlaceOfCHI)
            print("Location : ", self.m_Header.Location)
            print("Situation : ", self.m_Header.Situation)


            for i in range(len(self.m_KData)):
                print("Data[", i, "] : ", self.m_KData[i].type, "/", self.m_KData[i].speaker)
                for j in range(len(self.m_KData[i].datas)):
                    if j % 2 == 0:
                        print("Data[", i, "][", j, "] : ", self.m_KData[i].datas[j].startText)
                    elif j % 2 == 1:
                        print("Data[", i, "][", j, "] : ", self.m_KData[i].datas[j].MorpData)

            print("AudioPath : ", self.m_Audio.AudioPath)















if __name__ == "__main__":
    hi = KSTProject()
    hi.ProjectLoad("C:\\Users\\User\\PycharmProjects\\Cosmos\\기존KStars\\KStarsExam.txt")