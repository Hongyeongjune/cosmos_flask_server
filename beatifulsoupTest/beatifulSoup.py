import os

from bs4 import BeautifulSoup

# # KST 파일 읽기
# fp = open("C:\\Users\\User\\PycharmProjects\\Cosmos\\beatifulsoupTest\\KStarsKST.kst", 'rt', encoding='UTF8')
#
# # 읽은 KST 파일을 Beautiful 라이브러리를 이용하여 분석
# soup = BeautifulSoup(fp, 'lxml-xml')
#
# # <Option> 태그안에 있는 모든 값을 출력
# for optionElement in soup.findAll('Option'):
#     print(optionElement)

print(os.path.abspath(".\다운로드"))
