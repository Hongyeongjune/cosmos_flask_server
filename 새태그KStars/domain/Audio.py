class Audio:
    def __init__(self):
        self.AudioPath = list()
        self.AudioFileIndex = 0
        self.AudioCurrentPosition = 0.0

    def initData(self):
        self.AudioFileIndex = 0
        self.AudioCurrentPosition = 0
        self.AudioPath.clear()