import errno
import os

from flask import Flask, jsonify
from flask import request
from xml.etree.ElementTree import Element, SubElement, ElementTree

app = Flask(__name__)

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
    localPath = os.path.abspath("C:/Users/User/eclipse-workspace/K-Stars/src/main/java/kr/ac/skuniv/cosmos")

    if data['userDto']['user'] == "guest":
        tree.write(localPath + "\\guest\\temp\\" + data['userDto']['fileName'] + ".kst", encoding="utf-8")
    elif data['userDto']['user'] == "user":
        try:
            if not(os.path.isdir(localPath + "\\user\\" + data['userDto']['id'])):
                os.makedirs(os.path.join(localPath + "\\user\\" + data['userDto']['id']))
                tree.write(localPath + "\\user\\" + data['userDto']['id'] + "\\" + data['userDto']['fileName'] + ".kst", encoding="utf-8")
            if os.path.isdir(localPath + "\\user\\" + data['userDto']['id']):
                tree.write(localPath + "\\user\\" + data['userDto']['id'] + "\\" + data['userDto']['fileName'] + ".kst", encoding="utf-8")
        except OSError as e:
            if e.errno != errno.EEXIST:
                    print("Failed to create directory!!!!!")
                    raise

    return jsonify(data)