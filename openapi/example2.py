from bs4 import BeautifulSoup
import requests

url = "https://corona-live.com/city/8/"
html = requests.get(url)
# (1) ULR의 Html 파일을 파싱 및 트리 생성
soup = BeautifulSoup(html.content, 'html5lib')

print(soup)

# <div class="Layout__SBox-c6bc3z-0 kbjBmr DomesticRow__Cases-sc-23u5or-1 dbXrXs">3</div>

# (2) 첫 <p> 태그의 값 얻기
# first_paragraph = soup.find('p')  # or just soup.p

# 첫번째 p를 찾아 라인을 리턴
# assert str(soup.find('p')) == '<p id="p1">This is the first paragraph.</p>'

# p의 text 속성
# first_paragraph_text = soup.p.text
# first_paragraph_words = soup.p.text.split()

# assert first_paragraph_words == ['This', 'is', 'the', 'first', 'paragraph.']
# print(first_paragraph_words)
