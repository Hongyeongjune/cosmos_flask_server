from 기존KStars.domain.Tier import Tier


class Data:
    def __init__(self):
        self.DataType = ""
        self.speaker = ""
        self.ST = -1
        self.ET = -1
        self.datas = Tier()