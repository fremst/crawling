# https://www.inflearn.com/course/%ED%8C%8C%EC%9D%B4%EC%8D%AC-%ED%81%AC%EB%A1%A4%EB%A7%81-%EA%B8%B0%EC%B4%88/unit/93650?tab=curriculum

import time
import warnings
import csv
import pyautogui

from selenium import webdriver

from selenium.webdriver import ActionChains

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.common.exceptions import NoSuchElementException

# 크롬 드라이버 자동 업데이트
from webdriver_manager.chrome import ChromeDriverManager

# keyword = pyautogui.prompt('검색어를 입력하세요')
keyword = '고용'

# 설정
chrome_options = Options()

# 브라우저 자동 종료 방지
chrome_options.add_experimental_option("detach", True)

# 불필요한 에러 메시지 미출력
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])  # 셀레니움 로그 무시
warnings.filterwarnings("ignore", category=DeprecationWarning)  # Deprecated warning 무시

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
action = ActionChains(driver)

# 웹페이지 이동
driver.get('https://www.bigkinds.or.kr/v2/news/index.do')
driver.implicitly_wait(5)  # 로딩까지 5초간 대기
driver.maximize_window()  # 화면 최대화

driver.find_element(By.LINK_TEXT, '기간').click()
driver.find_element(By.CSS_SELECTOR, '.radio-btn:nth-child(2)').click()

search = driver.find_element(By.CSS_SELECTOR, '#total-search-key')
search.click()
search.send_keys(keyword)
search.send_keys(Keys.ENTER)

f = open(r"./data.csv", 'w', encoding='CP949', newline='')
csvWriter = csv.writer(f)
csvWriter.writerow([keyword])

try:
    for ii in range(0, 2):
        for i in range(1, 11):
            result_tag_name = '#news-results > div:nth-child(' + str(i) + ')'
            result_tag = driver.find_element(By.CSS_SELECTOR, result_tag_name + ' > div')
            action.move_to_element(result_tag).perform()

            title_element = driver.find_element(By.CSS_SELECTOR,
                                                result_tag_name + ' > div > div.cont > a > div > strong > span')
            title = title_element.text
            content_element = driver.find_element(By.CSS_SELECTOR,
                                                  result_tag_name + ' > div > div.cont > div > div > a')
            press_element = driver.find_element(By.CSS_SELECTOR,
                                                result_tag_name + '> div > div.cont > div > div > a')
            press = content_element.text
            link = content_element.get_attribute('href')

            csvWriter.writerow([title, press, link])
        next_btn = driver.find_element(By.CSS_SELECTOR,
                                       '#news-results-tab > div.data-result-ac.pc-only.paging-v2-wrp.btm > div.data-result-btm > div > div > div > div > div:nth-child(7) > a')
        action.move_to_element(next_btn).perform()
        next_btn.click()
except Exception as e:
    print(e)
    pass
driver.quit()
f.close()