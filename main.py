import requests
from bs4 import BeautifulSoup
import pyautogui

keyword = pyautogui.alert('검색어를 입력하세요')
print(keyword)

# response = requests.get("https://www.naver.com")
response = requests.get("https://www.bigkinds.or.kr/v2/news/index.do")
html = response.text
soup = BeautifulSoup(html, 'html.parser')
links = soup.select(".title-elipsis")
for link in links:
    title = link.text
    print(title)
# word = soup.select_one('#NM_set_home_btn')
# print(word.get('href'))
# https://www.youtube.com/watch?v=U1amkBqKF5g&list=PLNO7MWpu0eeUFdGMirV8_EkiLETqj8xA4&index=3&ab_channel=%EC%8A%A4%ED%83%80%ED%8A%B8%EC%BD%94%EB%94%A9