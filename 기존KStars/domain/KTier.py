from enum import Enum


class KTier:
    def __init__(self):
        self.TypeIndex = 0
        self.type = Enum('TierType', 'Empty Comment')
        self.ST = -1
        self.ET = -1
        self.startText = ""
        self.EndText = ""
        self.MorpData = ""
        self.MUData = ""
        self.datas = list()