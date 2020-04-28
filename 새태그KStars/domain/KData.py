from enum import Enum


class KData:

    def __init__(self):
        self.type = Enum('DataType', 'Empty Comment Utterance')
        self.speaker = ""
        self.datas = list()