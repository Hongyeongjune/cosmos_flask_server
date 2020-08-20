import librosa
import os
import numpy as np

class CutAudio:
    def __init__(self, originalFile, startTime, endTime, userFileName):
        self.originalFile = originalFile
        self.startTime = startTime
        self.endTime = endTime
        self.userFileName = userFileName
        self.cutAndSave(self.originalFile,self.startTime,self.endTime,self.userFileName)

    def cutAndSave(self,originalFile, startTime, endTime, userFileName):
        (file_dir, file_id) = os.path.split(originalFile)
        print("file_dir:", file_dir)
        print("file_id:", file_id)

        # original audio
        # sr: sampling_rate (default값: 22500)
        y, sr = librosa.load(originalFile)

        # cut and save
        time = np.linspace(0, len(y)/sr, len(y))
        sec = len(y)/(len(y)/sr) # 1초 계산값
        start_point = round(startTime*sec)
        end_point = round(endTime*sec)

        y2 = y[start_point:end_point]
        librosa.output.write_wav('C:\sge\\'+userFileName+'.WAV', y2, sr) #여기 저장경로를 어떻게 해야할지 모르게쑴..

#테스트 '원본파일경로', 시작지점, 끝지점, 저장하고자 하는 파일명
a = CutAudio('기뻐요.WAV',4,5, 'userFileName')