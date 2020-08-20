import os

localPath = os.path.abspath("C:/Users/User/eclipse-workspace/K-Stars/src/main/java/kr/ac/skuniv/cosmos")
if not (os.path.isdir(localPath + "\\user\\sge")):
    os.makedirs(os.path.join(localPath + "\\user\\" + "sge"))