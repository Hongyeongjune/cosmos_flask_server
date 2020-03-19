from enum import Enum


class Tier:
    def __init__(self):
        self.TypeIndex = 0
        self.type = Enum('TierType', 'Empty Comment')
        self.StartText = ""
        self.EndText =""
        self.datas = list()