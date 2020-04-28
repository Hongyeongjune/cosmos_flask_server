import os
from konlpy.tag import Okt, Komoran, Hannanum, Kkma
from eunjeon import Mecab

file = open(os.getcwd() + '\\text1.txt', 'r', encoding='utf-8')
lines = file.readlines()

okja = []
for line in lines:
    okja.append(line)
file.close()

Okt = Okt()
komoran = Komoran()
hannanum = Hannanum()
kkma = Kkma()
mecab = Mecab()

sentences_tag = []

for sentence in okja:
    morph = Okt.pos(sentence)
    print("Twitter : ", morph)

for sentence in okja:
    morph = komoran.pos(sentence)
    print("Komoran : ", morph)

for sentence in okja:
    morph = hannanum.pos(sentence)
    print("hannanum : ", morph)

for sentence in okja:
    morph = kkma.pos(sentence)
    print("kkma : ", morph)

for sentence in okja:
    morph = mecab.pos(sentence)
    print("mecab : ", morph)




